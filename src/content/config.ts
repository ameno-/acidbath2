import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    // Core fields
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('ACIDBATH'),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    banner: z.string().optional(),

    // SEO fields
    seoTitle: z.string().optional(),
    seoKeywords: z.array(z.string()).default([]),

    // AI optimization fields (for llms.txt and AI crawlers)
    tldr: z.string().optional(), // 2-3 sentence summary for AI quick answers
    keyTakeaways: z.array(z.string()).optional(), // 3-5 specific takeaways
    category: z.string().optional(), // Primary content category
    difficulty: z.enum(['Beginner', 'Intermediate', 'Advanced']).optional(),
    prerequisites: z.array(z.string()).optional(), // What readers should know first
    relatedPosts: z.array(z.string()).optional(), // Slugs of related posts
  }),
});

export const collections = { blog };
