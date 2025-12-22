/**
 * Calculate reading time for content
 * Average reading speed: 200-250 words per minute for technical content
 * We use 200 WPM for technical content (more careful reading)
 */
export function calculateReadingTime(content: string): number {
  // Strip markdown/HTML for accurate word count
  const plainText = content
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/`[^`]+`/g, '') // Remove inline code
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Replace links with text
    .replace(/[#*_~>\-|]/g, '') // Remove markdown symbols
    .replace(/<[^>]+>/g, '') // Remove HTML tags
    .replace(/\s+/g, ' ') // Normalize whitespace
    .trim();

  const wordCount = plainText.split(/\s+/).filter(word => word.length > 0).length;
  const wordsPerMinute = 200; // Technical content reading speed
  const minutes = Math.ceil(wordCount / wordsPerMinute);

  return Math.max(1, minutes); // Minimum 1 minute
}

/**
 * Format reading time for display
 */
export function formatReadingTime(minutes: number): string {
  return `${minutes} min read`;
}
