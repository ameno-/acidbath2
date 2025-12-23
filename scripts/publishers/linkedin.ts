/**
 * LinkedIn Publisher Implementation
 * Handles publishing content to LinkedIn personal and organization pages
 * Supports rich media, hashtag management, and LinkedIn API v2
 */

import { BasePublisher } from './base-publisher.js';
import {
  Publisher,
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';
import { API_ENDPOINTS, PLATFORM_LIMITS, validatePlatformEnv } from '../config/publish-config.js';
import { promises as fs } from 'fs';
import * as path from 'path';

/**
 * LinkedIn API v2 request payload for creating a post
 */
interface LinkedInPostPayload {
  author: string;
  lifecycleState: string;
  specificContent: {
    'com.linkedin.ugc.UGCPost': {
      shareContent: {
        shareMediaCategory: string;
        media?: Array<{
          status: string;
          description?: {
            text: string;
          };
          media: string;
        }>;
        shareCommentary: {
          text: string;
        };
      };
    };
  };
  visibility: {
    'com.linkedin.ugc.MemberNetworkVisibility': string;
  };
}

/**
 * LinkedIn article payload for publishing longer-form content
 */
interface LinkedInArticlePayload {
  title: string;
  description: string;
  content: string;
  canonicalUrl?: string;
  coverImage?: string;
}

export class LinkedInPublisher extends BasePublisher implements Publisher {
  readonly platform = 'linkedin';
  private accessToken: string;
  private organizationId: string | null;

  constructor(options: PublisherOptions) {
    super(options, 'linkedin');
    this.accessToken = options.config.accessToken || '';
    this.organizationId = options.config.organizationId || null;
  }

  /**
   * Validate LinkedIn configuration
   * Checks for required access token and verifies credentials
   */
  async validate(): Promise<boolean> {
    try {
      // Check environment variables
      const envValidation = validatePlatformEnv('linkedin');
      if (!envValidation.valid) {
        this.logError('Missing environment variables:', envValidation.missing.join(', '));
        return false;
      }

      // Verify access token
      if (!this.accessToken) {
        this.logError('LinkedIn access token not configured');
        return false;
      }

      // Test API connectivity
      const response = await this.fetch(`${API_ENDPOINTS.linkedin.base}/me`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      this.log('LinkedIn API validation successful, user ID:', data.id);
      return true;
    } catch (error: any) {
      this.logError('LinkedIn validation failed:', error.message);
      return false;
    }
  }

  /**
   * Publish content to LinkedIn
   * Handles both personal posts and organization posts
   */
  protected async publishContent(content: PlatformContent): Promise<PublishResult> {
    try {
      // Validate content
      if (!content.valid) {
        return {
          success: false,
          platform: this.platform,
          error: `Invalid content: ${content.validationErrors?.join(', ')}`,
        };
      }

      // Determine which endpoint to use
      const isOrganizationPost = !!this.organizationId;

      // Prepare the post payload
      const payload = this.preparePostPayload(content);

      // Create the post
      const result = await this.createPost(payload, isOrganizationPost);

      if (!result.success) {
        return result;
      }

      // Save publish log
      await this.savePublishLog(content.metadata?.slug || 'unknown', {
        success: true,
        platform: this.platform,
        url: result.url,
        metadata: {
          linkedInUrn: result.metadata?.linkedInUrn,
          postType: 'ugc',
        },
      });

      return result;
    } catch (error: any) {
      this.logError('Failed to publish to LinkedIn:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Unknown error during publishing',
      };
    }
  }

  /**
   * Prepare LinkedIn post payload from content
   * Formats content to LinkedIn specifications with hashtags
   */
  private preparePostPayload(content: PlatformContent): LinkedInPostPayload {
    // Format content with hashtags
    let postText = this.formatPostContent(content);

    // Truncate to LinkedIn's character limit
    if (postText.length > PLATFORM_LIMITS.linkedin.maxPostLength) {
      postText = postText.substring(0, PLATFORM_LIMITS.linkedin.maxPostLength - 3) + '...';
    }

    // Build the payload
    const payload: LinkedInPostPayload = {
      author: `urn:li:person:${this.getPersonUrn()}`,
      lifecycleState: 'PUBLISHED',
      specificContent: {
        'com.linkedin.ugc.UGCPost': {
          shareContent: {
            shareMediaCategory: content.coverImage ? 'IMAGE' : 'NONE',
            shareCommentary: {
              text: postText,
            },
          },
        },
      },
      visibility: {
        'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
      },
    };

    // Add cover image if available
    if (content.coverImage) {
      payload.specificContent['com.linkedin.ugc.UGCPost'].shareContent.media = [
        {
          status: 'READY',
          media: content.coverImage,
          description: {
            text: content.title,
          },
        },
      ];
    }

    return payload;
  }

  /**
   * Format post content with title, excerpt, and hashtags
   */
  private formatPostContent(content: PlatformContent): string {
    const parts: string[] = [];

    // Add title
    if (content.title) {
      parts.push(`${content.title}\n`);
    }

    // Add excerpt
    if (content.excerpt) {
      parts.push(`${content.excerpt}\n`);
    }

    // Add canonical URL for attribution
    parts.push(`\nRead more: ${content.canonicalUrl}`);

    // Add hashtags
    if (content.tags && content.tags.length > 0) {
      const hashtags = content.tags
        .slice(0, 5) // Limit to 5 hashtags
        .map(tag => `#${tag.replace(/\s+/g, '')}`)
        .join(' ');
      parts.push(`\n\n${hashtags}`);
    }

    return parts.join('');
  }

  /**
   * Create a post via LinkedIn API v2
   */
  private async createPost(
    payload: LinkedInPostPayload,
    isOrganizationPost: boolean
  ): Promise<PublishResult> {
    try {
      const url = isOrganizationPost
        ? `${API_ENDPOINTS.linkedin.base}${API_ENDPOINTS.linkedin.posts}?author=urn:li:organization:${this.organizationId}`
        : `${API_ENDPOINTS.linkedin.base}${API_ENDPOINTS.linkedin.posts}`;

      this.log(`Creating LinkedIn post (${isOrganizationPost ? 'organization' : 'personal'})...`);

      const response = await this.fetch(url, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify(payload),
      });

      // LinkedIn returns 201 Created with Location header
      if (response.status !== 201 && response.status !== 200) {
        throw new Error(`LinkedIn API returned ${response.status}`);
      }

      // Extract post URN from response headers or body
      const locationHeader = response.headers.get('x-restli-id');
      const linkedInUrn = locationHeader || `urn:li:ugcPost:unknown`;

      // Construct LinkedIn post URL
      const postUrl = `https://www.linkedin.com/feed/update/${linkedInUrn}`;

      this.log(`Successfully published to LinkedIn: ${postUrl}`);

      return {
        success: true,
        platform: this.platform,
        url: postUrl,
        metadata: {
          linkedInUrn,
          postType: 'ugc',
        },
      };
    } catch (error: any) {
      this.logError('Failed to create LinkedIn post:', error);

      // Check if it's a rate limit error
      if (error.message.includes('429')) {
        throw new Error('LinkedIn rate limit exceeded');
      }

      // Check if it's an auth error
      if (error.message.includes('401') || error.message.includes('403')) {
        throw new Error(`LinkedIn authentication failed: ${error.message}`);
      }

      throw error;
    }
  }

  /**
   * Get the current user's LinkedIn person URN
   * This would normally come from the config or be fetched from the API
   */
  private getPersonUrn(): string {
    // This is a placeholder - in production, this would be fetched from LinkedIn's /me endpoint
    // and cached in the configuration
    return process.env.LINKEDIN_PERSON_URN || '0';
  }

  /**
   * Read LinkedIn-specific post content from derivatives directory
   */
  private async readLinkedInContent(slug: string): Promise<string> {
    const contentPath = path.join(
      process.cwd(),
      'content',
      'derivatives',
      slug,
      'linkedin-post.md'
    );

    try {
      return await fs.readFile(contentPath, 'utf-8');
    } catch (error: any) {
      this.logError(`Failed to read LinkedIn content from ${contentPath}:`, error);
      throw new Error(`Could not read LinkedIn post content for slug: ${slug}`);
    }
  }
}
