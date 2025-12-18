import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('ACIDBATH'),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    banner: z.string().optional(),
    seoTitle: z.string().optional(),
    seoKeywords: z.array(z.string()).default([]),
  }),
});

export const collections = { blog };
