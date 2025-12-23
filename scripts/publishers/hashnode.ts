/**
 * Hashnode Publisher Implementation
 * Publishes blog posts to Hashnode using their GraphQL API
 */

import { BasePublisher } from './base-publisher.js';
import {
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';
import { promises as fs } from 'fs';
import * as path from 'path';

interface HashnodeCreateArticleResponse {
  data?: {
    createPublicationContent?: {
      post?: {
        id: string;
        slug: string;
        title: string;
        canonicalUrl: string;
        url: string;
      };
    };
  };
  errors?: Array<{
    message: string;
  }>;
}

interface HashnodeTagInput {
  name: string;
  slug?: string;
}

export class HashnodePublisher extends BasePublisher {
  readonly platform = 'hashnode';
  private apiKey: string | undefined;
  private publicationId: string | undefined;
  private readonly apiEndpoint = 'https://gql.hashnode.com';

  constructor(options: PublisherOptions) {
    super(options, 'hashnode');
    this.apiKey = options.config.apiKey || process.env.HASHNODE_API_KEY;
    this.publicationId =
      options.config.publicationId || process.env.HASHNODE_PUBLICATION_ID;
  }

  /**
   * Validate that required environment variables and configuration are set
   */
  async validate(): Promise<boolean> {
    if (!this.apiKey) {
      this.logError('HASHNODE_API_KEY environment variable is not set');
      return false;
    }

    if (!this.publicationId) {
      this.logError('HASHNODE_PUBLICATION_ID environment variable is not set');
      return false;
    }

    this.log('Validation successful - API key and publication ID are configured');
    return true;
  }

  /**
   * Publish content to Hashnode via GraphQL API
   */
  protected async publishContent(content: PlatformContent): Promise<PublishResult> {
    try {
      // Validate content before publishing
      if (!content.valid) {
        return {
          success: false,
          platform: this.platform,
          error: `Content validation failed: ${(content.validationErrors || []).join(', ')}`,
        };
      }

      this.log(`Publishing to Hashnode: ${content.title}`);

      // Prepare article payload
      const articlePayload = this.buildArticlePayload(content);

      // Publish article via GraphQL mutation
      const result = await this.publishArticle(articlePayload);

      if (!result.success) {
        return result;
      }

      // Save publish log
      const slug = this.extractSlugFromContent(content);
      await this.savePublishLog(slug, result);

      return result;
    } catch (error: any) {
      this.logError('Failed to publish content:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Unknown error during publishing',
      };
    }
  }

  /**
   * Build article payload for Hashnode GraphQL mutation
   */
  private buildArticlePayload(content: PlatformContent): Record<string, any> {
    // Convert tags to Hashnode format
    const tags: HashnodeTagInput[] = content.tags.map(tag => ({
      name: tag.replace(/^#/, ''), // Remove # prefix if present
    }));

    return {
      input: {
        publicationId: this.publicationId,
        title: content.title,
        subtitle: content.excerpt || '',
        contentMarkdown: content.content,
        coverImageOptions: content.coverImage
          ? {
              coverImageUrl: content.coverImage,
            }
          : undefined,
        canonicalUrl: content.canonicalUrl,
        tags,
        isPartOfPublication: {
          publication: {
            id: this.publicationId,
          },
        },
        seo: {
          title: content.title,
          description: content.excerpt || content.title,
        },
      },
    };
  }

  /**
   * Publish article to Hashnode using GraphQL API
   */
  private async publishArticle(
    payload: Record<string, any>
  ): Promise<PublishResult> {
    const mutation = `
      mutation createPublicationContent($input: CreatePublicationContentInput!) {
        createPublicationContent(input: $input) {
          post {
            id
            slug
            title
            canonicalUrl
            url
          }
        }
      }
    `;

    const graphqlPayload = {
      query: mutation,
      variables: payload,
    };

    try {
      this.log(`Sending GraphQL request to ${this.apiEndpoint}`);

      const response = await this.fetch(this.apiEndpoint, {
        method: 'POST',
        headers: {
          'Authorization': this.apiKey!,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(graphqlPayload),
      });

      const responseData: HashnodeCreateArticleResponse = await response.json();

      // Check for GraphQL errors
      if (responseData.errors && responseData.errors.length > 0) {
        const errorMessage = responseData.errors
          .map(err => err.message)
          .join('; ');
        this.logError('GraphQL error:', errorMessage);
        return {
          success: false,
          platform: this.platform,
          error: `GraphQL error: ${errorMessage}`,
        };
      }

      // Extract article data from response
      const article = responseData.data?.createPublicationContent?.post;

      if (!article) {
        this.logError('No article data in response');
        return {
          success: false,
          platform: this.platform,
          error: 'No article data returned from Hashnode API',
        };
      }

      this.log(`Successfully published article: ${article.url}`);

      return {
        success: true,
        platform: this.platform,
        url: article.url,
        metadata: {
          articleId: article.id,
          slug: article.slug,
          canonicalUrl: article.canonicalUrl,
        },
      };
    } catch (error: any) {
      this.logError('Failed to call Hashnode GraphQL API:', error);
      return {
        success: false,
        platform: this.platform,
        error: `API call failed: ${error.message}`,
      };
    }
  }

  /**
   * Extract slug from content metadata
   * Uses title or canonical URL as fallback
   */
  private extractSlugFromContent(content: PlatformContent): string {
    // Try to extract from canonical URL
    const urlMatch = content.canonicalUrl.match(/\/([^\/]+)\/?$/);
    if (urlMatch && urlMatch[1]) {
      return urlMatch[1];
    }

    // Fallback to slugified title
    return content.title
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .substring(0, 50);
  }
}

export default HashnodePublisher;
