/**
 * Core TypeScript types and interfaces for multi-channel publishing
 */

/**
 * Represents the result of a publishing operation to a platform
 */
export interface PublishResult {
  success: boolean;
  platform: string;
  url?: string;
  error?: string;
  metadata?: Record<string, any>;
  publishedAt?: Date;
}

/**
 * Configuration for a specific publishing platform
 */
export interface PublishConfig {
  platform: string;
  enabled: boolean;
  apiKey?: string;
  apiSecret?: string;
  accessToken?: string;
  accessSecret?: string;
  clientId?: string;
  clientSecret?: string;
  organizationId?: string;
  publicationId?: string;
  dryRun?: boolean;
  staged?: boolean;
}

/**
 * Platform-specific content after transformation
 */
export interface PlatformContent {
  platform: string;
  title: string;
  content: string;
  excerpt?: string;
  tags: string[];
  canonicalUrl: string;
  coverImage?: string;
  characterCount: number;
  valid: boolean;
  validationErrors?: string[];
  metadata?: Record<string, any>;
}

/**
 * Metadata extracted from blog post for publishing
 */
export interface PostMetadata {
  slug: string;
  title: string;
  description: string;
  tags: string[];
  publishedDate: string;
  canonicalUrl: string;
  coverImage?: string;
  author: string;
  wordCount: number;
  readingTime: number;
}

/**
 * Base interface that all platform publishers must implement
 */
export interface Publisher {
  readonly platform: string;

  /**
   * Validate that the publisher is properly configured
   */
  validate(): Promise<boolean>;

  /**
   * Publish content to the platform
   */
  publish(content: PlatformContent): Promise<PublishResult>;

  /**
   * Check if content has already been published to this platform
   */
  isPublished(slug: string): Promise<boolean>;

  /**
   * Get the URL of previously published content
   */
  getPublishedUrl(slug: string): Promise<string | null>;
}

/**
 * Options for the main publish-all orchestrator
 */
export interface PublishOptions {
  slug: string;
  platforms?: string[];
  dryRun?: boolean;
  staged?: boolean;
  force?: boolean;
}

/**
 * Complete report of a multi-platform publish operation
 */
export interface PublishReport {
  slug: string;
  startedAt: Date;
  completedAt: Date;
  totalPlatforms: number;
  successfulPlatforms: number;
  failedPlatforms: number;
  results: PublishResult[];
  summary: string;
}

/**
 * Rate limiting configuration
 */
export interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
  retryAfterMs?: number;
}

/**
 * Publisher options passed to constructors
 */
export interface PublisherOptions {
  config: PublishConfig;
  dryRun?: boolean;
  verbose?: boolean;
}
