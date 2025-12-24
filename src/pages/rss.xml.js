import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);

  // Sort by date descending
  const sortedPosts = posts.sort((a, b) =>
    new Date(b.data.pubDate).getTime() - new Date(a.data.pubDate).getTime()
  );

  return rss({
    title: 'ACIDBATH',
    description: 'Production AI patterns for senior engineers. Code-first deep dives on AI agents, context engineering, and production LLM patterns.',
    site: context.site,
    items: sortedPosts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.slug}/`,
      categories: post.data.tags,
      // Include full content for platforms that support it
      content: post.data.tldr || post.data.description,
    })),
    customData: `<language>en-us</language>`,
  });
}
