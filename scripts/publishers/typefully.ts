/**
 * Typefully Publisher
 *
 * Unified publisher for multiple social platforms via Typefully API.
 * Handles: X (Twitter), LinkedIn, Bluesky, Threads, Mastodon
 *
 * Typefully simplifies social publishing by providing a single API
 * that manages authentication, rate limits, and cross-posting.
 */

import { BasePublisher } from './base-publisher.js';
import {
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';

/**
 * Platform-specific content for Typefully API
 */
interface TypefullyPlatformContent {
  enabled: boolean;
  posts: { text: string; media_ids?: string[] }[];
  settings?: Record<string, any>;
}

/**
 * Typefully API draft response
 */
interface TypefullyDraftResponse {
  id: number;
  social_set_id: number;
  status: 'draft' | 'scheduled' | 'publishing' | 'published' | 'error';
  private_url: string;
  share_url?: string;
  scheduled_date?: string;
  published_at?: string;
  x_published_url?: string;
  linkedin_published_url?: string;
  bluesky_published_url?: string;
  threads_published_url?: string;
  mastodon_published_url?: string;
}

/**
 * Typefully API error response
 */
interface TypefullyError {
  error: {
    code: string;
    message: string;
    details?: { field: string; message: string }[];
  };
}

/**
 * Options for Typefully publishing
 */
export interface TypefullyPublisherOptions extends PublisherOptions {
  /**
   * Which platforms to enable in Typefully
   * If not specified, enables all available platforms
   */
  enabledPlatforms?: ('x' | 'linkedin' | 'bluesky' | 'threads' | 'mastodon')[];

  /**
   * When to publish: 'now', 'next-free-slot', or ISO 8601 datetime
   */
  publishAt?: 'now' | 'next-free-slot' | string;

  /**
   * Tags to apply to the draft in Typefully
   */
  tags?: string[];
}

export class TypefullyPublisher extends BasePublisher {
  readonly platform = 'typefully';

  private apiKey: string;
  private socialSetId: string;
  private baseUrl = 'https://api.typefully.com';
  private enabledPlatforms: string[];
  private publishAt: string;
  private typefullyTags: string[];

  constructor(options: TypefullyPublisherOptions) {
    super(options, 'typefully');

    this.apiKey = options.config.apiKey || process.env.TYPEFULLY_API_KEY || '';
    this.socialSetId = options.config.organizationId || process.env.TYPEFULLY_SOCIAL_SET_ID || '';
    this.enabledPlatforms = options.enabledPlatforms || ['x', 'linkedin', 'bluesky', 'threads', 'mastodon'];
    this.publishAt = options.publishAt || 'now';
    this.typefullyTags = options.tags || [];
  }

  async validate(): Promise<boolean> {
    if (!this.apiKey) {
      this.logError('TYPEFULLY_API_KEY is not set');
      return false;
    }

    if (!this.socialSetId) {
      this.logError('TYPEFULLY_SOCIAL_SET_ID is not set');
      return false;
    }

    try {
      // Test API connection
      const response = await this.fetch(`${this.baseUrl}/v2/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        this.log('Typefully API connection validated');
        return true;
      }

      return false;
    } catch (error: any) {
      this.logError('Failed to validate Typefully API:', error.message);
      return false;
    }
  }

  protected async publishContent(content: PlatformContent): Promise<PublishResult> {
    // Build platform-specific content based on character limits
    const platforms = this.buildPlatformContent(content);

    // Create draft and optionally publish
    const draftBody: Record<string, any> = {
      platforms,
      draft_title: content.title,
    };

    if (this.typefullyTags.length > 0) {
      draftBody.tags = this.typefullyTags;
    }

    if (!this.dryRun) {
      draftBody.publish_at = this.publishAt;
    }

    try {
      const response = await this.fetch(
        `${this.baseUrl}/v2/social-sets/${this.socialSetId}/drafts`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(draftBody),
        }
      );

      const data = await response.json() as TypefullyDraftResponse;

      // Collect all published URLs
      const publishedUrls: Record<string, string> = {};
      if (data.x_published_url) publishedUrls.x = data.x_published_url;
      if (data.linkedin_published_url) publishedUrls.linkedin = data.linkedin_published_url;
      if (data.bluesky_published_url) publishedUrls.bluesky = data.bluesky_published_url;
      if (data.threads_published_url) publishedUrls.threads = data.threads_published_url;
      if (data.mastodon_published_url) publishedUrls.mastodon = data.mastodon_published_url;

      const result: PublishResult = {
        success: true,
        platform: 'typefully',
        url: data.private_url,
        metadata: {
          draftId: data.id,
          status: data.status,
          publishedUrls,
          scheduledDate: data.scheduled_date,
          publishedAt: data.published_at,
        },
      };

      // Save publish log
      if (content.metadata?.slug) {
        await this.savePublishLog(content.metadata.slug, result);
      }

      return result;
    } catch (error: any) {
      // Handle Typefully-specific errors
      if (error.message.includes('429')) {
        return {
          success: false,
          platform: 'typefully',
          error: 'Rate limit exceeded. Try again later.',
        };
      }

      return {
        success: false,
        platform: 'typefully',
        error: error.message || 'Unknown error publishing to Typefully',
      };
    }
  }

  /**
   * Build platform-specific content with appropriate character limits
   */
  private buildPlatformContent(content: PlatformContent): Record<string, TypefullyPlatformContent> {
    const platforms: Record<string, TypefullyPlatformContent> = {};

    // X (Twitter) - 280 chars per tweet, supports threads
    if (this.enabledPlatforms.includes('x')) {
      platforms.x = {
        enabled: true,
        posts: this.splitIntoTweets(content.content, 280),
      };
    }

    // LinkedIn - up to 3000 chars
    if (this.enabledPlatforms.includes('linkedin')) {
      platforms.linkedin = {
        enabled: true,
        posts: [{ text: this.truncate(content.content, 3000) }],
      };
    }

    // Bluesky - 300 chars
    if (this.enabledPlatforms.includes('bluesky')) {
      platforms.bluesky = {
        enabled: true,
        posts: [{ text: this.truncate(content.content, 300) }],
      };
    }

    // Threads - 500 chars
    if (this.enabledPlatforms.includes('threads')) {
      platforms.threads = {
        enabled: true,
        posts: [{ text: this.truncate(content.content, 500) }],
      };
    }

    // Mastodon - 500 chars (default, can vary by instance)
    if (this.enabledPlatforms.includes('mastodon')) {
      platforms.mastodon = {
        enabled: true,
        posts: [{ text: this.truncate(content.content, 500) }],
      };
    }

    return platforms;
  }

  /**
   * Split content into tweet-sized chunks for X threads
   */
  private splitIntoTweets(text: string, maxLength: number = 280): { text: string }[] {
    const tweets: { text: string }[] = [];

    // If content fits in one tweet, return as-is
    if (text.length <= maxLength) {
      return [{ text }];
    }

    // Split by paragraphs first, then by sentences
    const paragraphs = text.split('\n\n').filter(p => p.trim());

    let currentTweet = '';

    for (const paragraph of paragraphs) {
      // If adding this paragraph exceeds limit, save current and start new
      if ((currentTweet + '\n\n' + paragraph).length > maxLength) {
        if (currentTweet.trim()) {
          tweets.push({ text: currentTweet.trim() });
        }

        // If paragraph itself is too long, split by sentences
        if (paragraph.length > maxLength) {
          const sentences = paragraph.match(/[^.!?]+[.!?]+/g) || [paragraph];
          currentTweet = '';

          for (const sentence of sentences) {
            if ((currentTweet + ' ' + sentence).length > maxLength) {
              if (currentTweet.trim()) {
                tweets.push({ text: currentTweet.trim() });
              }
              currentTweet = sentence.trim();
            } else {
              currentTweet = (currentTweet + ' ' + sentence).trim();
            }
          }
        } else {
          currentTweet = paragraph;
        }
      } else {
        currentTweet = currentTweet ? currentTweet + '\n\n' + paragraph : paragraph;
      }
    }

    // Don't forget the last tweet
    if (currentTweet.trim()) {
      tweets.push({ text: currentTweet.trim() });
    }

    return tweets;
  }

  /**
   * Truncate text to max length with ellipsis
   */
  private truncate(text: string, maxLength: number): string {
    if (text.length <= maxLength) {
      return text;
    }

    // Find last space before limit to avoid cutting words
    const truncated = text.slice(0, maxLength - 3);
    const lastSpace = truncated.lastIndexOf(' ');

    if (lastSpace > maxLength * 0.8) {
      return truncated.slice(0, lastSpace) + '...';
    }

    return truncated + '...';
  }

  /**
   * Get published URLs for all Typefully platforms
   */
  async getPublishedUrls(slug: string): Promise<Record<string, string>> {
    try {
      const logPath = this.getPublishLogPath(slug);
      const { promises: fs } = await import('fs');
      const logData = await fs.readFile(logPath, 'utf-8');
      const log = JSON.parse(logData);

      return log.typefully?.metadata?.publishedUrls || {};
    } catch {
      return {};
    }
  }
}

/**
 * Create a Typefully publisher with default configuration
 */
export function createTypefullyPublisher(options?: Partial<TypefullyPublisherOptions>): TypefullyPublisher {
  return new TypefullyPublisher({
    config: {
      platform: 'typefully',
      enabled: true,
      apiKey: process.env.TYPEFULLY_API_KEY,
      organizationId: process.env.TYPEFULLY_SOCIAL_SET_ID,
    },
    dryRun: options?.dryRun || false,
    verbose: options?.verbose || false,
    enabledPlatforms: options?.enabledPlatforms,
    publishAt: options?.publishAt,
    tags: options?.tags,
  });
}
