/**
 * Utilities for formatting content for different publishing platforms
 */

import { PlatformContent } from '../types/publisher.js';
import { PLATFORM_LIMITS } from '../config/publish-config.js';

/**
 * Split long text into Twitter thread chunks
 */
export function splitIntoThreads(content: string, maxLength: number = 280): string[] {
  const threads: string[] = [];
  const paragraphs = content.split('\n\n');

  let currentThread = '';

  for (const paragraph of paragraphs) {
    const trimmed = paragraph.trim();
    if (!trimmed) continue;

    // If paragraph fits in current thread
    if ((currentThread + '\n\n' + trimmed).length <= maxLength) {
      currentThread = currentThread ? currentThread + '\n\n' + trimmed : trimmed;
    }
    // If paragraph is too long, split it
    else if (trimmed.length > maxLength) {
      if (currentThread) {
        threads.push(currentThread);
        currentThread = '';
      }

      // Split long paragraph into sentences
      const sentences = trimmed.split(/\. |\n/);
      for (const sentence of sentences) {
        const withPeriod = sentence.endsWith('.') ? sentence : sentence + '.';
        if ((currentThread + ' ' + withPeriod).length <= maxLength) {
          currentThread = currentThread ? currentThread + ' ' + withPeriod : withPeriod;
        } else {
          if (currentThread) threads.push(currentThread);
          currentThread = withPeriod;
        }
      }
    }
    // Start new thread
    else {
      if (currentThread) threads.push(currentThread);
      currentThread = trimmed;
    }
  }

  if (currentThread) threads.push(currentThread);

  return threads;
}

/**
 * Format content for LinkedIn (supports longer posts)
 */
export function formatForLinkedIn(content: string, title: string): string {
  const maxLength = PLATFORM_LIMITS.linkedin.maxPostLength;

  let formatted = `${title}\n\n${content}`;

  // Truncate if too long
  if (formatted.length > maxLength) {
    formatted = formatted.substring(0, maxLength - 50) + '... [Read more]';
  }

  return formatted;
}

/**
 * Convert markdown to dev.to flavor
 */
export function formatForDevTo(markdown: string): string {
  // dev.to supports standard markdown with some enhancements
  // Add liquid tags if needed, handle code blocks, etc.
  let formatted = markdown;

  // Ensure code blocks use proper fencing
  formatted = formatted.replace(/```(\w+)/g, '```$1');

  // Convert image paths to absolute URLs if needed
  // This would need the canonical URL context

  return formatted;
}

/**
 * Convert markdown for Hashnode
 */
export function formatForHashnode(markdown: string): string {
  // Hashnode uses standard markdown
  let formatted = markdown;

  // Ensure proper heading hierarchy
  // Hashnode uses H1 for title, so shift down all headings
  formatted = formatted.replace(/^### /gm, '#### ');
  formatted = formatted.replace(/^## /gm, '### ');
  formatted = formatted.replace(/^# /gm, '## ');

  return formatted;
}

/**
 * Convert markdown to Medium format
 */
export function formatForMedium(markdown: string): string {
  // Medium has its own format, but accepts markdown
  let formatted = markdown;

  // Medium prefers cleaner formatting
  // Remove excessive line breaks
  formatted = formatted.replace(/\n{3,}/g, '\n\n');

  // Ensure code blocks are properly formatted
  formatted = formatted.replace(/```(\w+)\n/g, '```$1\n');

  return formatted;
}

/**
 * Extract and validate hashtags from tags
 */
export function formatHashtags(tags: string[], platform: string): string[] {
  const formatted = tags.map(tag => {
    // Remove spaces and special characters
    const cleaned = tag.replace(/[^\w\s]/g, '').replace(/\s+/g, '');

    // Add # prefix for Twitter/LinkedIn
    if (platform === 'twitter' || platform === 'linkedin') {
      return `#${cleaned}`;
    }

    return cleaned;
  });

  // Respect platform tag limits
  const limits: Record<string, number> = {
    twitter: 5,
    linkedin: 10,
    devto: 4,
    hashnode: 5,
    medium: 5,
  };

  const limit = limits[platform] || 5;
  return formatted.slice(0, limit);
}

/**
 * Create excerpt from content
 */
export function createExcerpt(content: string, maxLength: number = 200): string {
  // Remove markdown formatting
  let plain = content
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/`[^`]+`/g, '') // Remove inline code
    .replace(/[#*_\[\]()]/g, '') // Remove markdown symbols
    .replace(/\n+/g, ' ') // Replace newlines with spaces
    .trim();

  if (plain.length <= maxLength) {
    return plain;
  }

  // Truncate at last complete sentence
  const truncated = plain.substring(0, maxLength);
  const lastPeriod = truncated.lastIndexOf('.');

  if (lastPeriod > maxLength * 0.7) {
    return truncated.substring(0, lastPeriod + 1);
  }

  return truncated + '...';
}

/**
 * Validate content meets platform requirements
 */
export function validateContent(content: PlatformContent): PlatformContent {
  const errors: string[] = [];
  const limits = PLATFORM_LIMITS[content.platform as keyof typeof PLATFORM_LIMITS];

  if (!limits) {
    errors.push(`Unknown platform: ${content.platform}`);
    return { ...content, valid: false, validationErrors: errors };
  }

  // Validate title length
  if ('maxTitleLength' in limits && content.title.length > limits.maxTitleLength) {
    errors.push(`Title too long: ${content.title.length} > ${limits.maxTitleLength}`);
  }

  // Validate content length
  if ('maxBodyLength' in limits && content.content.length > limits.maxBodyLength) {
    errors.push(`Content too long: ${content.content.length} > ${limits.maxBodyLength}`);
  }

  // Validate tags
  if ('maxTags' in limits && content.tags.length > limits.maxTags) {
    errors.push(`Too many tags: ${content.tags.length} > ${limits.maxTags}`);
  }

  // Validate required fields
  if (!content.title) errors.push('Title is required');
  if (!content.content) errors.push('Content is required');
  if (!content.canonicalUrl) errors.push('Canonical URL is required');

  return {
    ...content,
    valid: errors.length === 0,
    validationErrors: errors.length > 0 ? errors : undefined,
  };
}

/**
 * Strip code blocks from content (useful for social media)
 */
export function stripCodeBlocks(content: string): string {
  return content
    .replace(/```[\s\S]*?```/g, '[Code example - see blog post]')
    .replace(/`[^`]+`/g, '');
}

/**
 * Count characters excluding markdown formatting
 */
export function countPlainTextChars(markdown: string): number {
  const plain = markdown
    .replace(/```[\s\S]*?```/g, '[code]')
    .replace(/`[^`]+`/g, '')
    .replace(/[#*_\[\]()]/g, '')
    .replace(/\n+/g, ' ')
    .trim();

  return plain.length;
}

/**
 * Prepare content for a specific platform
 */
export function prepareContentForPlatform(
  originalContent: string,
  platform: string,
  metadata: {
    title: string;
    description: string;
    tags: string[];
    canonicalUrl: string;
    coverImage?: string;
  }
): PlatformContent {
  let formattedContent = originalContent;
  let title = metadata.title;

  switch (platform) {
    case 'twitter':
      // For Twitter, create a thread-friendly version
      formattedContent = stripCodeBlocks(originalContent);
      break;

    case 'linkedin':
      formattedContent = formatForLinkedIn(originalContent, title);
      break;

    case 'devto':
      formattedContent = formatForDevTo(originalContent);
      break;

    case 'hashnode':
      formattedContent = formatForHashnode(originalContent);
      break;

    case 'medium':
      formattedContent = formatForMedium(originalContent);
      break;
  }

  const platformContent: PlatformContent = {
    platform,
    title,
    content: formattedContent,
    excerpt: createExcerpt(originalContent),
    tags: formatHashtags(metadata.tags, platform),
    canonicalUrl: metadata.canonicalUrl,
    coverImage: metadata.coverImage,
    characterCount: countPlainTextChars(formattedContent),
    valid: true,
  };

  return validateContent(platformContent);
}
