/**
 * Base abstract class for all platform publishers
 * Implements common functionality like rate limiting, retry logic, and error handling
 */

import {
  Publisher,
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';
import { RATE_LIMITS, getRetryConfig } from '../config/publish-config.js';
import { promises as fs } from 'fs';
import * as path from 'path';

export abstract class BasePublisher implements Publisher {
  abstract readonly platform: string;
  protected config: PublisherOptions;
  protected dryRun: boolean;
  protected verbose: boolean;

  // Rate limiting state
  private requestTimestamps: number[] = [];
  private rateLimit;

  constructor(options: PublisherOptions, platform: string) {
    this.config = options;
    this.dryRun = options.dryRun || false;
    this.verbose = options.verbose || false;
    this.rateLimit = RATE_LIMITS[platform] || {
      maxRequests: 100,
      windowMs: 60000,
    };
  }

  /**
   * Validate that the publisher is properly configured
   * Subclasses should implement platform-specific validation
   */
  abstract validate(): Promise<boolean>;

  /**
   * Publish content to the platform
   * Subclasses must implement platform-specific publishing logic
   */
  protected abstract publishContent(content: PlatformContent): Promise<PublishResult>;

  /**
   * Public publish method with rate limiting, retries, and error handling
   */
  async publish(content: PlatformContent): Promise<PublishResult> {
    try {
      // Validate configuration
      const isValid = await this.validate();
      if (!isValid) {
        return {
          success: false,
          platform: this.platform,
          error: 'Publisher configuration is invalid',
        };
      }

      // Check rate limits
      await this.enforceRateLimit();

      // Dry run mode
      if (this.dryRun) {
        this.log('DRY RUN: Would publish to ' + this.platform);
        this.log('Content:', JSON.stringify(content, null, 2));
        return {
          success: true,
          platform: this.platform,
          url: `https://dry-run.example.com/${content.platform}/${content.title}`,
          metadata: { dryRun: true },
        };
      }

      // Attempt publishing with retries
      return await this.publishWithRetry(content);
    } catch (error: any) {
      this.logError('Publish failed:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Unknown error',
      };
    }
  }

  /**
   * Publish with automatic retry logic
   */
  private async publishWithRetry(content: PlatformContent): Promise<PublishResult> {
    const retryConfig = getRetryConfig(this.platform);
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= retryConfig.maxRetries; attempt++) {
      try {
        this.log(`Attempt ${attempt}/${retryConfig.maxRetries}`);
        const result = await this.publishContent(content);

        if (result.success) {
          this.log(`Successfully published to ${this.platform}`);
          return result;
        }

        // If not successful but no exception, treat as error
        lastError = new Error(result.error || 'Unknown error');
      } catch (error: any) {
        lastError = error;
        this.logError(`Attempt ${attempt} failed:`, error);

        // Don't retry on authentication errors
        if (this.isAuthError(error)) {
          return {
            success: false,
            platform: this.platform,
            error: `Authentication failed: ${error.message}`,
          };
        }

        // Wait before retrying
        if (attempt < retryConfig.maxRetries) {
          const delay = Math.min(
            retryConfig.initialDelayMs * Math.pow(retryConfig.backoffMultiplier, attempt - 1),
            retryConfig.maxDelayMs
          );
          this.log(`Waiting ${delay}ms before retry...`);
          await this.sleep(delay);
        }
      }
    }

    return {
      success: false,
      platform: this.platform,
      error: `Failed after ${retryConfig.maxRetries} attempts: ${lastError?.message}`,
    };
  }

  /**
   * Check if content has already been published to this platform
   */
  async isPublished(slug: string): Promise<boolean> {
    try {
      const logPath = this.getPublishLogPath(slug);
      const logData = await fs.readFile(logPath, 'utf-8');
      const log = JSON.parse(logData);
      return log[this.platform]?.published === true;
    } catch {
      return false;
    }
  }

  /**
   * Get the URL of previously published content
   */
  async getPublishedUrl(slug: string): Promise<string | null> {
    try {
      const logPath = this.getPublishLogPath(slug);
      const logData = await fs.readFile(logPath, 'utf-8');
      const log = JSON.parse(logData);
      return log[this.platform]?.url || null;
    } catch {
      return null;
    }
  }

  /**
   * Save publish result to log file
   */
  protected async savePublishLog(slug: string, result: PublishResult): Promise<void> {
    try {
      const logPath = this.getPublishLogPath(slug);
      let log: Record<string, any> = {};

      // Read existing log if it exists
      try {
        const existing = await fs.readFile(logPath, 'utf-8');
        log = JSON.parse(existing);
      } catch {
        // File doesn't exist yet, that's okay
      }

      // Update log for this platform
      log[this.platform] = {
        published: result.success,
        url: result.url,
        publishedAt: new Date().toISOString(),
        error: result.error,
        metadata: result.metadata,
      };

      // Ensure directory exists
      await fs.mkdir(path.dirname(logPath), { recursive: true });

      // Write log
      await fs.writeFile(logPath, JSON.stringify(log, null, 2));
      this.log(`Publish log updated: ${logPath}`);
    } catch (error: any) {
      this.logError('Failed to save publish log:', error);
    }
  }

  /**
   * Enforce rate limiting
   */
  private async enforceRateLimit(): Promise<void> {
    const now = Date.now();
    const windowStart = now - this.rateLimit.windowMs;

    // Remove timestamps outside the window
    this.requestTimestamps = this.requestTimestamps.filter(ts => ts > windowStart);

    // Check if we're at the limit
    if (this.requestTimestamps.length >= this.rateLimit.maxRequests) {
      const oldestRequest = this.requestTimestamps[0];
      const waitTime = oldestRequest + this.rateLimit.windowMs - now;

      if (waitTime > 0) {
        this.log(`Rate limit reached. Waiting ${waitTime}ms...`);
        await this.sleep(waitTime);
      }
    }

    // Record this request
    this.requestTimestamps.push(now);
  }

  /**
   * Check if an error is an authentication error
   */
  protected isAuthError(error: any): boolean {
    const authKeywords = ['auth', 'unauthorized', '401', '403', 'forbidden', 'token'];
    const errorMessage = (error.message || '').toLowerCase();
    return authKeywords.some(keyword => errorMessage.includes(keyword));
  }

  /**
   * Get path to publish log for a slug
   */
  protected getPublishLogPath(slug: string): string {
    return path.join(process.cwd(), 'content', 'derivatives', slug, 'publish-log.json');
  }

  /**
   * Sleep for specified milliseconds
   */
  protected sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Log message if verbose mode is enabled
   */
  protected log(...args: any[]): void {
    if (this.verbose || this.dryRun) {
      console.log(`[${this.platform}]`, ...args);
    }
  }

  /**
   * Log error message
   */
  protected logError(...args: any[]): void {
    console.error(`[${this.platform} ERROR]`, ...args);
  }

  /**
   * Make HTTP request with fetch
   */
  protected async fetch(
    url: string,
    options: RequestInit = {}
  ): Promise<Response> {
    this.log(`HTTP ${options.method || 'GET'} ${url}`);

    const response = await fetch(url, {
      ...options,
      headers: {
        'User-Agent': 'ACIDBATH-Publisher/1.0',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(
        `HTTP ${response.status}: ${response.statusText}`
      );
    }

    return response;
  }
}
