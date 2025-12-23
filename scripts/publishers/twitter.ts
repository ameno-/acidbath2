/**
 * Twitter/X Publisher Implementation
 * Handles publishing content to Twitter as threaded tweets with image support
 */

import { BasePublisher } from './base-publisher.js';
import {
  Publisher,
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';
import { API_ENDPOINTS, PLATFORM_LIMITS } from '../config/publish-config.js';
import { splitIntoThreads } from '../utils/content-formatter.js';
import { promises as fs } from 'fs';
import * as path from 'path';

/**
 * Twitter thread tweet object for API v2
 */
interface TwitterTweet {
  text: string;
  reply?: {
    in_reply_to_tweet_id: string;
  };
  media?: {
    media_ids: string[];
  };
}

/**
 * Twitter API v2 tweet response
 */
interface TwitterTweetResponse {
  data: {
    id: string;
    text: string;
  };
}

/**
 * Twitter media upload response
 */
interface TwitterMediaResponse {
  media_id_string: string;
  media_key: string;
}

/**
 * Twitter Publisher - handles publishing content as threads
 */
export class TwitterPublisher extends BasePublisher implements Publisher {
  readonly platform = 'twitter';

  constructor(options: PublisherOptions) {
    super(options, 'twitter');
  }

  /**
   * Validate Twitter API credentials are configured
   */
  async validate(): Promise<boolean> {
    const requiredEnvVars = [
      'TWITTER_API_KEY',
      'TWITTER_API_SECRET',
      'TWITTER_ACCESS_TOKEN',
      'TWITTER_ACCESS_SECRET',
    ];

    const missing = requiredEnvVars.filter(envVar => !process.env[envVar]);

    if (missing.length > 0) {
      this.logError(`Missing required environment variables: ${missing.join(', ')}`);
      return false;
    }

    this.log('Twitter credentials validated');
    return true;
  }

  /**
   * Publish content to Twitter as a thread
   */
  protected async publishContent(content: PlatformContent): Promise<PublishResult> {
    try {
      // Validate content
      if (!content.valid) {
        const errors = (content.validationErrors || []).join('; ');
        return {
          success: false,
          platform: this.platform,
          error: `Content validation failed: ${errors}`,
        };
      }

      // Check character count
      if (content.characterCount > PLATFORM_LIMITS.twitter.maxTweetLength) {
        this.log(
          `Content exceeds single tweet (${content.characterCount} chars). Creating thread...`
        );
      }

      // Read twitter-thread.md file from derivatives
      const threadContent = await this.readThreadFile(content.metadata?.slug);

      if (!threadContent) {
        return {
          success: false,
          platform: this.platform,
          error: 'Could not read twitter-thread.md derivative file',
        };
      }

      // Split content into tweets
      const tweets = splitIntoThreads(threadContent, PLATFORM_LIMITS.twitter.maxTweetLength);

      if (tweets.length === 0) {
        return {
          success: false,
          platform: this.platform,
          error: 'No valid tweets to publish',
        };
      }

      // Check thread length limit
      if (tweets.length > PLATFORM_LIMITS.twitter.maxThreadLength) {
        return {
          success: false,
          platform: this.platform,
          error: `Thread too long: ${tweets.length} tweets > ${PLATFORM_LIMITS.twitter.maxThreadLength} max`,
        };
      }

      // Create thread
      const threadResult = await this.createThread(tweets, content);

      if (threadResult.success) {
        // Save publish log
        await this.savePublishLog(content.metadata?.slug, threadResult);
      }

      return threadResult;
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
   * Read twitter-thread.md file from derivatives
   */
  private async readThreadFile(slug?: string): Promise<string | null> {
    if (!slug) {
      this.logError('Slug is required to read thread file');
      return null;
    }

    try {
      const threadPath = path.join(
        process.cwd(),
        'content',
        'derivatives',
        slug,
        'twitter-thread.md'
      );

      this.log(`Reading thread file: ${threadPath}`);
      const content = await fs.readFile(threadPath, 'utf-8');

      return content;
    } catch (error: any) {
      this.logError(`Failed to read thread file: ${error.message}`);
      return null;
    }
  }

  /**
   * Create a tweet thread on Twitter
   */
  private async createThread(
    tweets: string[],
    content: PlatformContent
  ): Promise<PublishResult> {
    try {
      let firstTweetId: string | null = null;
      const tweetIds: string[] = [];

      // Post each tweet in the thread
      for (let i = 0; i < tweets.length; i++) {
        const tweetText = tweets[i];

        // Add conversation indicators
        let text = tweetText;
        if (tweets.length > 1) {
          text = `${text}\n\n[${i + 1}/${tweets.length}]`;
        }

        // Add canonical URL and tags to last tweet
        if (i === tweets.length - 1) {
          const hashtags = content.tags.join(' ');
          text = `${text}\n\nRead more: ${content.canonicalUrl}`;
          if (hashtags) {
            text = `${text}\n${hashtags}`;
          }
        }

        // Create tweet
        const tweetResponse = await this.postTweet(text, firstTweetId);

        if (!tweetResponse.success) {
          return {
            success: false,
            platform: this.platform,
            error: `Failed to post tweet ${i + 1}/${tweets.length}: ${tweetResponse.error}`,
          };
        }

        const tweetId = tweetResponse.tweetId!;
        tweetIds.push(tweetId);

        // Set first tweet ID for reply chain
        if (i === 0) {
          firstTweetId = tweetId;
        }

        this.log(`Posted tweet ${i + 1}/${tweets.length} (ID: ${tweetId})`);
      }

      // Return success with URL to first tweet
      const tweetUrl = `https://twitter.com/i/web/status/${firstTweetId}`;

      return {
        success: true,
        platform: this.platform,
        url: tweetUrl,
        metadata: {
          tweetCount: tweets.length,
          firstTweetId,
          tweetIds,
          postedAt: new Date().toISOString(),
        },
      };
    } catch (error: any) {
      this.logError('Failed to create thread:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Failed to create thread',
      };
    }
  }

  /**
   * Post a single tweet to Twitter
   */
  private async postTweet(
    text: string,
    replyToId?: string | null
  ): Promise<{ success: boolean; tweetId?: string; error?: string }> {
    try {
      const apiKey = process.env.TWITTER_API_KEY;
      const apiSecret = process.env.TWITTER_API_SECRET;
      const accessToken = process.env.TWITTER_ACCESS_TOKEN;
      const accessSecret = process.env.TWITTER_ACCESS_SECRET;

      if (!apiKey || !apiSecret || !accessToken || !accessSecret) {
        return {
          success: false,
          error: 'Missing Twitter API credentials',
        };
      }

      // Validate tweet length
      if (text.length > PLATFORM_LIMITS.twitter.maxTweetLength) {
        return {
          success: false,
          error: `Tweet text too long: ${text.length} > ${PLATFORM_LIMITS.twitter.maxTweetLength}`,
        };
      }

      // Build tweet payload
      const tweetData: TwitterTweet = {
        text,
      };

      if (replyToId) {
        tweetData.reply = {
          in_reply_to_tweet_id: replyToId,
        };
      }

      // Create OAuth signature
      const authHeader = this.buildOAuthHeader(
        'POST',
        `${API_ENDPOINTS.twitter.base}${API_ENDPOINTS.twitter.tweet}`,
        apiKey,
        apiSecret,
        accessToken,
        accessSecret
      );

      // Post tweet
      const response = await this.fetch(
        `${API_ENDPOINTS.twitter.base}${API_ENDPOINTS.twitter.tweet}`,
        {
          method: 'POST',
          headers: {
            Authorization: authHeader,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(tweetData),
        }
      );

      const responseData = (await response.json()) as TwitterTweetResponse;

      if (!responseData.data || !responseData.data.id) {
        return {
          success: false,
          error: 'Invalid response from Twitter API',
        };
      }

      return {
        success: true,
        tweetId: responseData.data.id,
      };
    } catch (error: any) {
      this.logError('Failed to post tweet:', error);
      return {
        success: false,
        error: error.message || 'Failed to post tweet',
      };
    }
  }

  /**
   * Build OAuth 1.0a authorization header for Twitter API v2
   * This is a simplified implementation - production code should use a proper OAuth library
   */
  private buildOAuthHeader(
    method: string,
    url: string,
    apiKey: string,
    apiSecret: string,
    accessToken: string,
    accessSecret: string
  ): string {
    // Create OAuth parameters
    const oauthParams: Record<string, string> = {
      oauth_consumer_key: apiKey,
      oauth_token: accessToken,
      oauth_signature_method: 'HMAC-SHA1',
      oauth_timestamp: Math.floor(Date.now() / 1000).toString(),
      oauth_nonce: this.generateNonce(),
      oauth_version: '1.0',
    };

    // Build parameter string
    const params = Object.keys(oauthParams)
      .sort()
      .map(key => `${key}=${oauthParams[key]}`)
      .join('&');

    // Create signature base string
    const baseString = `${method}&${encodeURIComponent(url)}&${encodeURIComponent(params)}`;

    // Create signing key
    const signingKey = `${encodeURIComponent(apiSecret)}&${encodeURIComponent(accessSecret)}`;

    // Create signature using HMAC-SHA1
    // Note: In a real implementation, use crypto.createHmac
    const crypto = require('crypto');
    const signature = crypto
      .createHmac('sha1', signingKey)
      .update(baseString)
      .digest('base64');

    // Add signature to params
    oauthParams.oauth_signature = signature;

    // Build authorization header
    const headerParams = Object.keys(oauthParams)
      .sort()
      .map(key => `${key}="${encodeURIComponent(oauthParams[key])}"`)
      .join(', ');

    return `OAuth ${headerParams}`;
  }

  /**
   * Generate a random nonce for OAuth
   */
  private generateNonce(): string {
    const crypto = require('crypto');
    return crypto.randomBytes(16).toString('hex');
  }
}
