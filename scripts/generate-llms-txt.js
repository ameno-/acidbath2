/**
 * Generate llms.txt and llms-full.txt for AI crawler optimization
 *
 * Run: node scripts/generate-llms-txt.js
 */
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.join(__dirname, '..');
const BLOG_DIR = path.join(ROOT_DIR, 'src/content/blog');
const OUTPUT_DIR = path.join(ROOT_DIR, 'public');

/**
 * Parse frontmatter from markdown file
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { data: {}, content };

  const frontmatterLines = match[1].split('\n');
  const data = {};

  let currentKey = null;
  let currentArray = null;

  for (const line of frontmatterLines) {
    // Check for array item
    if (line.match(/^\s+-\s+/)) {
      const value = line.replace(/^\s+-\s+/, '').replace(/^["']|["']$/g, '');
      if (currentArray) {
        currentArray.push(value);
      }
      continue;
    }

    // Check for key-value pair
    const kvMatch = line.match(/^(\w+):\s*(.*)$/);
    if (kvMatch) {
      currentKey = kvMatch[1];
      let value = kvMatch[2].trim();

      // Check if it's an array start
      if (value === '' || value === '[]') {
        currentArray = [];
        data[currentKey] = currentArray;
      } else if (value.startsWith('[') && value.endsWith(']')) {
        // Inline array
        data[currentKey] = value
          .slice(1, -1)
          .split(',')
          .map(v => v.trim().replace(/^["']|["']$/g, ''))
          .filter(v => v);
        currentArray = null;
      } else {
        // Regular value
        data[currentKey] = value.replace(/^["']|["']$/g, '');
        currentArray = null;
      }
    }
  }

  return { data, content: match[2] };
}

/**
 * Get all blog posts
 */
async function getAllPosts() {
  const files = await fs.readdir(BLOG_DIR);
  const posts = await Promise.all(
    files
      .filter(f => f.endsWith('.md') || f.endsWith('.mdx'))
      .map(async (file) => {
        const filePath = path.join(BLOG_DIR, file);
        const fileContent = await fs.readFile(filePath, 'utf-8');
        const { data, content } = parseFrontmatter(fileContent);

        return {
          ...data,
          slug: file.replace(/\.mdx?$/, ''),
          body: content
        };
      })
  );

  // Filter out drafts and sort by date
  return posts
    .filter(p => p.draft !== 'true' && p.draft !== true)
    .sort((a, b) => new Date(b.pubDate || 0) - new Date(a.pubDate || 0));
}

/**
 * Strip markdown for plain text
 */
function stripMarkdown(content) {
  return content
    .replace(/```[\s\S]*?```/g, '[code block]') // Replace code blocks
    .replace(/`([^`]+)`/g, '$1') // Remove inline code markers
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Replace links with text
    .replace(/^#{1,6}\s+/gm, '') // Remove heading markers
    .replace(/[*_~]/g, '') // Remove emphasis markers
    .replace(/^\s*[-*+]\s+/gm, '• ') // Normalize list markers
    .replace(/^\s*\d+\.\s+/gm, '• ') // Normalize numbered lists
    .replace(/^>\s+/gm, '') // Remove blockquote markers
    .replace(/\n{3,}/g, '\n\n') // Normalize multiple newlines
    .trim();
}

/**
 * Group posts by category
 */
function groupByCategory(posts) {
  return posts.reduce((acc, post) => {
    const cat = post.category || 'Uncategorized';
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(post);
    return acc;
  }, {});
}

/**
 * Generate llms.txt (summary version)
 */
function generateSummary(posts) {
  const grouped = groupByCategory(posts);

  const recentPosts = posts.slice(0, 5)
    .map(p => `- [${p.title}](/blog/${p.slug}): ${p.description}`)
    .join('\n');

  const topicSections = Object.entries(grouped)
    .map(([category, categoryPosts]) => {
      const postList = categoryPosts
        .map(p => `- [${p.title}](/blog/${p.slug}): ${p.description}`)
        .join('\n');
      return `### ${category}\n\n${postList}`;
    })
    .join('\n\n');

  return `# ACIDBATH

> Production AI engineering patterns for senior engineers and technical leaders.
> Code-first, practitioner-focused content on agentic AI, context engineering,
> and LLM cost optimization.

## What This Site Covers

ACIDBATH provides deep technical content on building production AI systems:

- **Agentic AI Patterns**: Sub-agent architecture, workflow prompts, orchestration
- **Context Engineering**: Token optimization, progressive disclosure, semantic search
- **Claude Code**: Best practices, commands, custom agents, MCP integration
- **Production AI Economics**: Cost analysis, model routing, real-world benchmarks

## Recent Posts

${recentPosts}

## Topics

${topicSections}

## About

ACIDBATH is the critical, code-first voice that senior technical leaders trust.
We focus on what actually works in production, including honest coverage of
failures and limitations. No hype, no hand-waving—just working code and
real numbers.

## Contact

- Website: https://blog.amenoacids.com
- Email: contact@amenoacids.com

---

*For full post content, see [/llms-full.txt](/llms-full.txt)*
`;
}

/**
 * Generate llms-full.txt (complete content)
 */
function generateFull(posts) {
  const postSections = posts.map(post => {
    const plainContent = stripMarkdown(post.body);

    const tldrSection = post.tldr
      ? `### TL;DR\n\n${post.tldr}`
      : '';

    const takeawaysSection = post.keyTakeaways && post.keyTakeaways.length > 0
      ? `### Key Takeaways\n\n${post.keyTakeaways.map((t, i) => `${i + 1}. ${t}`).join('\n')}`
      : '';

    return `
---

## ${post.title}

*Published: ${post.pubDate}*
*Category: ${post.category || 'Uncategorized'}*
*Difficulty: ${post.difficulty || 'Intermediate'}*
*URL: /blog/${post.slug}*

${tldrSection}

${takeawaysSection}

### Content

${plainContent}
`;
  }).join('\n');

  return `# ACIDBATH - Complete Content

> This file contains the full text of all ACIDBATH blog posts,
> formatted for AI consumption.
> Last updated: ${new Date().toISOString()}

${postSections}

---

*End of content. For navigation, see [/llms.txt](/llms.txt)*
`;
}

/**
 * Main function
 */
async function main() {
  try {
    const posts = await getAllPosts();

    console.log(`Found ${posts.length} published posts`);

    // Generate llms.txt
    const llmsTxt = generateSummary(posts);
    await fs.writeFile(path.join(OUTPUT_DIR, 'llms.txt'), llmsTxt);
    console.log('✅ Generated public/llms.txt');

    // Generate llms-full.txt
    const llmsFullTxt = generateFull(posts);
    await fs.writeFile(path.join(OUTPUT_DIR, 'llms-full.txt'), llmsFullTxt);
    console.log('✅ Generated public/llms-full.txt');

    console.log('Done!');
  } catch (error) {
    console.error('Error generating llms.txt files:', error);
    process.exit(1);
  }
}

main();
