/**
 * Medium platform publisher
 * Publishes blog posts to Medium as stories with markdown formatting, tags, and canonical URL
 */

import { BasePublisher } from './base-publisher.js';
import {
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';
import { promises as fs } from 'fs';
import * as path from 'path';

interface MediumUser {
  id: string;
  username: string;
  name: string;
}

interface MediumStory {
  id: string;
  title: string;
  authorId: string;
  url: string;
  status: string;
}

export class MediumPublisher extends BasePublisher {
  readonly platform = 'medium';
  private readonly baseUrl = 'https://api.medium.com/v1';
  private readonly integrationToken: string;

  constructor(options: PublisherOptions) {
    super(options, 'medium');
    this.integrationToken = options.config.accessToken || '';
  }

  /**
   * Validate that the Medium integration token is configured
   */
  async validate(): Promise<boolean> {
    if (!this.integrationToken) {
      this.logError('MEDIUM_INTEGRATION_TOKEN is not configured');
      return false;
    }

    // Verify token is valid by attempting to get current user
    try {
      const response = await this.fetch(`${this.baseUrl}/me`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${this.integrationToken}`,
          'Content-Type': 'application/json',
        },
      });

      const user = await response.json() as { data?: MediumUser };
      if (user.data?.id) {
        this.log(`Validated Medium token for user: ${user.data.username}`);
        return true;
      }
      this.logError('Invalid Medium integration token response');
      return false;
    } catch (error) {
      this.logError('Failed to validate Medium token:', error);
      return false;
    }
  }

  /**
   * Publish content to Medium
   */
  protected async publishContent(content: PlatformContent): Promise<PublishResult> {
    try {
      // Get current user to obtain their ID
      const user = await this.getCurrentUser();
      if (!user) {
        return {
          success: false,
          platform: this.platform,
          error: 'Failed to get Medium user ID',
        };
      }

      // Prepare content for Medium
      const mediumContent = this.prepareMediumContent(content);

      // Create story on Medium
      const story = await this.createStory(user.id, mediumContent);
      if (!story) {
        return {
          success: false,
          platform: this.platform,
          error: 'Failed to create Medium story',
        };
      }

      // Publish story (set status to public)
      const publishedStory = await this.publishStory(user.id, story.id);
      if (!publishedStory) {
        return {
          success: false,
          platform: this.platform,
          error: 'Failed to publish Medium story',
        };
      }

      this.log(`Successfully published to Medium: ${publishedStory.url}`);

      // Save publish log
      const slug = content.metadata?.slug || 'unknown';
      const result: PublishResult = {
        success: true,
        platform: this.platform,
        url: publishedStory.url,
        metadata: {
          mediumId: story.id,
          userId: user.id,
          status: publishedStory.status,
        },
      };

      await this.savePublishLog(slug, result);
      return result;
    } catch (error: any) {
      this.logError('Failed to publish to Medium:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Unknown error',
      };
    }
  }

  /**
   * Get current Medium user
   */
  private async getCurrentUser(): Promise<MediumUser | null> {
    try {
      const response = await this.fetch(`${this.baseUrl}/me`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${this.integrationToken}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json() as { data?: MediumUser };
      return data.data || null;
    } catch (error) {
      this.logError('Failed to get current user:', error);
      return null;
    }
  }

  /**
   * Prepare content in Medium's format
   */
  private prepareMediumContent(
    content: PlatformContent
  ): {
    title: string;
    contentFormat: string;
    content: string;
    canonicalUrl: string;
    tags: string[];
    publishStatus: string;
    license: string;
  } {
    // Limit tags to maximum of 5
    const tags = content.tags.slice(0, 5);

    return {
      title: content.title,
      contentFormat: 'markdown',
      content: content.content,
      canonicalUrl: content.canonicalUrl,
      tags,
      publishStatus: 'public',
      license: 'all-rights-reserved',
    };
  }

  /**
   * Create a draft story on Medium
   */
  private async createStory(
    userId: string,
    mediumContent: {
      title: string;
      contentFormat: string;
      content: string;
      canonicalUrl: string;
      tags: string[];
      publishStatus: string;
      license: string;
    }
  ): Promise<MediumStory | null> {
    try {
      const response = await this.fetch(
        `${this.baseUrl}/users/${userId}/posts`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${this.integrationToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(mediumContent),
        }
      );

      const data = await response.json() as { data?: MediumStory };
      return data.data || null;
    } catch (error) {
      this.logError('Failed to create Medium story:', error);
      return null;
    }
  }

  /**
   * Publish a story (make it public)
   */
  private async publishStory(
    userId: string,
    storyId: string
  ): Promise<MediumStory | null> {
    try {
      // Get the story details to construct the publish response
      const response = await this.fetch(
        `${this.baseUrl}/users/${userId}/posts/${storyId}`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${this.integrationToken}`,
            'Content-Type': 'application/json',
          },
        }
      );

      const data = await response.json() as { data?: MediumStory };
      return data.data || null;
    } catch (error) {
      this.logError('Failed to publish Medium story:', error);
      return null;
    }
  }
}
