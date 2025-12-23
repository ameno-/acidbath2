/**
 * Dev.to Publisher Implementation
 * Handles publishing content to the Dev.to platform via REST API
 */

import { BasePublisher } from './base-publisher.js';
import {
  Publisher,
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';
import { API_ENDPOINTS } from '../config/publish-config.js';
import { promises as fs } from 'fs';
import * as path from 'path';

interface DevToArticle {
  article: {
    title: string;
    body_markdown: string;
    published: boolean;
    tags?: string[];
    canonical_url?: string;
    cover_image_url?: string;
    series?: string;
  };
}

interface DevToResponse {
  id: number;
  title: string;
  slug: string;
  url: string;
  published: boolean;
  canonical_url?: string;
}

export class DevToPublisher extends BasePublisher implements Publisher {
  readonly platform = 'devto';
  private apiKey: string;

  constructor(options: PublisherOptions) {
    super(options, 'devto');
    this.apiKey = options.config.apiKey || process.env.DEVTO_API_KEY || '';
  }

  /**
   * Validate that the publisher is properly configured
   * Checks for required DEVTO_API_KEY environment variable
   */
  async validate(): Promise<boolean> {
    if (!this.apiKey || this.apiKey.trim().length === 0) {
      this.logError('DEVTO_API_KEY environment variable is not set');
      return false;
    }

    try {
      // Test API key by making a simple authenticated request
      const response = await this.fetch(`${API_ENDPOINTS.devto.base}/user`, {
        method: 'GET',
        headers: {
          'api-key': this.apiKey,
          'Content-Type': 'application/json',
        },
      });

      const data = (await response.json()) as any;
      this.log('API key validation successful, user:', data.username);
      return true;
    } catch (error: any) {
      this.logError('API key validation failed:', error.message);
      return false;
    }
  }

  /**
   * Publish content to Dev.to
   * Creates an article with frontmatter, tags, and canonical URL
   */
  protected async publishContent(content: PlatformContent): Promise<PublishResult> {
    try {
      // Validate content
      if (!content.valid) {
        return {
          success: false,
          platform: this.platform,
          error: `Invalid content: ${(content.validationErrors || []).join(', ')}`,
        };
      }

      // Check content limits
      if (content.title.length > 128) {
        return {
          success: false,
          platform: this.platform,
          error: `Title exceeds 128 character limit (${content.title.length} characters)`,
        };
      }

      if (content.characterCount > 1000000) {
        return {
          success: false,
          platform: this.platform,
          error: `Content exceeds 1,000,000 character limit (${content.characterCount} characters)`,
        };
      }

      if (content.tags.length > 4) {
        return {
          success: false,
          platform: this.platform,
          error: `Too many tags. Dev.to supports max 4 tags, provided ${content.tags.length}`,
        };
      }

      // Prepare tags (max 4, limit each to 30 characters for Dev.to)
      const tags = content.tags.slice(0, 4).map(tag =>
        tag.substring(0, 30).toLowerCase().replace(/\s+/g, '-')
      );

      // Build article payload with Dev.to flavor markdown
      const article: DevToArticle = {
        article: {
          title: content.title,
          body_markdown: this.formatMarkdown(content.content),
          published: true,
          tags,
          canonical_url: content.canonicalUrl,
        },
      };

      // Add cover image if available
      if (content.coverImage) {
        article.article.cover_image_url = content.coverImage;
      }

      // Add series if provided in metadata
      if (content.metadata?.series) {
        article.article.series = content.metadata.series;
      }

      this.log('Publishing to Dev.to with article:', {
        title: article.article.title,
        tags: article.article.tags,
        canonical_url: article.article.canonical_url,
        has_cover: !!article.article.cover_image_url,
      });

      // Create the article via API
      const response = await this.fetch(
        `${API_ENDPOINTS.devto.base}${API_ENDPOINTS.devto.articles}`,
        {
          method: 'POST',
          headers: {
            'api-key': this.apiKey,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(article),
        }
      );

      const responseData = (await response.json()) as DevToResponse;

      this.log('Article published successfully:', {
        id: responseData.id,
        url: responseData.url,
        slug: responseData.slug,
      });

      // Save publish log
      const slug = content.metadata?.slug || this.extractSlug(content.title);
      await this.savePublishLog(slug, {
        success: true,
        platform: this.platform,
        url: responseData.url,
        metadata: {
          id: responseData.id,
          slug: responseData.slug,
          publishedAt: new Date().toISOString(),
        },
      });

      return {
        success: true,
        platform: this.platform,
        url: responseData.url,
        metadata: {
          id: responseData.id,
          slug: responseData.slug,
        },
      };
    } catch (error: any) {
      this.logError('Failed to publish to Dev.to:', error);

      // Handle specific Dev.to API errors
      if (error.message.includes('401') || error.message.includes('403')) {
        return {
          success: false,
          platform: this.platform,
          error: 'Authentication failed - invalid or expired API key',
        };
      }

      if (error.message.includes('422')) {
        return {
          success: false,
          platform: this.platform,
          error: 'Invalid article content - please check title, body, and tags',
        };
      }

      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Unknown error while publishing to Dev.to',
      };
    }
  }

  /**
   * Format markdown for Dev.to flavor
   * Dev.to supports a subset of Markdown with some extensions
   */
  private formatMarkdown(content: string): string {
    // Dev.to uses standard Markdown but with some specific handling
    // Remove any frontmatter if present
    let markdown = content.replace(/^---[\s\S]*?---\s*/, '');

    // Ensure proper spacing around headers
    markdown = markdown.replace(/([^\n])\n(#{1,6}\s)/g, '$1\n\n$2');

    // Ensure code blocks are properly formatted
    markdown = markdown.replace(/^```([a-z]*)\n/gm, '```$1\n');

    // Dev.to supports {% embed %} tags for embeds
    // But standard markdown is also fine

    return markdown.trim();
  }

  /**
   * Extract slug from title for logging
   */
  private extractSlug(title: string): string {
    return title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 50);
  }
}
