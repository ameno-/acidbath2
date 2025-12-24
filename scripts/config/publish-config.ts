/**
 * Platform configurations for multi-channel publishing
 */

import { RateLimitConfig } from '../types/publisher.js';

/**
 * Platform API endpoint configurations
 */
export const API_ENDPOINTS = {
  twitter: {
    base: 'https://api.twitter.com/2',
    tweet: '/tweets',
    upload: 'https://upload.twitter.com/1.1/media/upload.json',
  },
  linkedin: {
    base: 'https://api.linkedin.com/v2',
    posts: '/ugcPosts',
    shares: '/shares',
  },
  devto: {
    base: 'https://dev.to/api',
    articles: '/articles',
  },
  hashnode: {
    base: 'https://gql.hashnode.com',
  },
  medium: {
    base: 'https://api.medium.com/v1',
    users: '/me',
    posts: '/users/{userId}/posts',
  },
  buttondown: {
    base: 'https://api.buttondown.email/v1',
    emails: '/emails',
  },
  substack: {
    base: 'https://api.substack.com/v1',
  },
  mailchimp: {
    base: 'https://{dc}.api.mailchimp.com/3.0',
    campaigns: '/campaigns',
  },
} as const;

/**
 * Platform rate limit configurations
 */
export const RATE_LIMITS: Record<string, RateLimitConfig> = {
  twitter: {
    maxRequests: 50,
    windowMs: 15 * 60 * 1000, // 15 minutes
    retryAfterMs: 60 * 1000, // 1 minute
  },
  linkedin: {
    maxRequests: 100,
    windowMs: 24 * 60 * 60 * 1000, // 24 hours
    retryAfterMs: 60 * 60 * 1000, // 1 hour
  },
  devto: {
    maxRequests: 30,
    windowMs: 30 * 1000, // 30 seconds
    retryAfterMs: 5 * 1000, // 5 seconds
  },
  hashnode: {
    maxRequests: 100,
    windowMs: 60 * 1000, // 1 minute (estimated)
    retryAfterMs: 10 * 1000, // 10 seconds
  },
  medium: {
    maxRequests: 60,
    windowMs: 60 * 60 * 1000, // 1 hour (recommended)
    retryAfterMs: 60 * 1000, // 1 minute
  },
  newsletter: {
    maxRequests: 10,
    windowMs: 60 * 60 * 1000, // 1 hour
    retryAfterMs: 5 * 60 * 1000, // 5 minutes
  },
};

/**
 * Platform-specific character/content limits
 */
export const PLATFORM_LIMITS = {
  twitter: {
    maxTweetLength: 280,
    maxThreadLength: 25,
    maxImageSize: 5 * 1024 * 1024, // 5MB
  },
  linkedin: {
    maxPostLength: 3000,
    maxArticleLength: 125000,
    maxImageSize: 10 * 1024 * 1024, // 10MB
  },
  devto: {
    maxTitleLength: 128,
    maxBodyLength: 1000000,
    maxTags: 4,
  },
  hashnode: {
    maxTitleLength: 250,
    maxBodyLength: 1000000,
    maxTags: 5,
  },
  medium: {
    maxTitleLength: 100,
    maxBodyLength: 100000,
    maxTags: 5,
  },
} as const;

/**
 * Authentication methods per platform
 */
export const AUTH_METHODS = {
  twitter: 'oauth1',
  linkedin: 'oauth2',
  devto: 'api_key',
  hashnode: 'api_key',
  medium: 'integration_token',
  buttondown: 'api_key',
  substack: 'api_key',
  mailchimp: 'api_key',
} as const;

/**
 * Default publishing order (optimized for engagement flow)
 */
export const DEFAULT_PUBLISH_ORDER = [
  'twitter',
  'linkedin',
  'devto',
  'hashnode',
  'medium',
  'newsletter',
] as const;

/**
 * Platforms that support canonical URLs
 */
export const CANONICAL_URL_SUPPORT = [
  'devto',
  'hashnode',
  'medium',
] as const;

/**
 * Platforms that support cover images
 */
export const COVER_IMAGE_SUPPORT = [
  'twitter',
  'linkedin',
  'devto',
  'hashnode',
  'medium',
] as const;

/**
 * Get environment variable key names for each platform
 */
export function getEnvKeys(platform: string): string[] {
  const envMap: Record<string, string[]> = {
    twitter: [
      'TWITTER_API_KEY',
      'TWITTER_API_SECRET',
      'TWITTER_ACCESS_TOKEN',
      'TWITTER_ACCESS_SECRET',
    ],
    linkedin: [
      'LINKEDIN_CLIENT_ID',
      'LINKEDIN_CLIENT_SECRET',
      'LINKEDIN_ACCESS_TOKEN',
    ],
    devto: ['DEVTO_API_KEY'],
    hashnode: ['HASHNODE_API_KEY'],
    medium: ['MEDIUM_INTEGRATION_TOKEN'],
    buttondown: ['BUTTONDOWN_API_KEY'],
    substack: ['SUBSTACK_API_KEY'],
    mailchimp: ['MAILCHIMP_API_KEY', 'MAILCHIMP_SERVER_PREFIX'],
  };

  return envMap[platform] || [];
}

/**
 * Validate that required environment variables are set for a platform
 */
export function validatePlatformEnv(platform: string): { valid: boolean; missing: string[] } {
  const required = getEnvKeys(platform);
  const missing = required.filter(key => !process.env[key]);

  return {
    valid: missing.length === 0,
    missing,
  };
}

/**
 * Get retry configuration for a platform
 */
export function getRetryConfig(platform: string) {
  return {
    maxRetries: 3,
    initialDelayMs: 1000,
    maxDelayMs: 30000,
    backoffMultiplier: 2,
  };
}
