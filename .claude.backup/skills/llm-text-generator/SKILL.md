# LLMs.txt Generator Skill

Generate and maintain `llms.txt` and `llms-full.txt` files for AI crawler optimization.

## Purpose

AI tools (ChatGPT, Claude, Perplexity) increasingly crawl websites to provide answers. This skill generates structured files that help AI systems understand your blog content, increasing the likelihood of being cited in AI responses.

## Files Generated

1. **`/llms.txt`** - Summary map for quick AI comprehension
2. **`/llms-full.txt`** - Complete content in clean markdown

## When to Use

- After publishing new blog posts
- When updating existing content
- During site rebuilds
- Run with: `node scripts/generate-llms-txt.js`

## llms.txt Format

```markdown
# ACIDBATH

> Production AI engineering patterns for senior engineers and technical leaders.
> Code-first, practitioner-focused content on agentic AI, context engineering,
> and LLM cost optimization.

## Recent Posts

- [Post Title](/blog/slug): One-sentence description from frontmatter

## Topics

### Context Engineering

- [Post Title](/blog/slug): Description

### Agentic Patterns

- [Post Title](/blog/slug): Description

## About

Brief author/site description.

## Contact

- Twitter: @handle
- GitHub: @handle
```

## llms-full.txt Format

```markdown
# ACIDBATH - Complete Content

> Full text of all posts for AI consumption.
> Last updated: [ISO date]

---

## Post Title

*Published: Date*
*Category: Category*
*Difficulty: Level*

### TL;DR

[tldr from frontmatter]

### Key Takeaways

1. First takeaway
2. Second takeaway
3. Third takeaway

### Content

[Full post content, stripped of HTML and complex formatting]

---

[Next post...]
```

## Implementation Script

Save as `scripts/generate-llms-txt.js`:

```javascript
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import strip from 'strip-markdown';

const BLOG_DIR = 'src/content/blog';
const OUTPUT_DIR = 'public';
const SITE_NAME = 'ACIDBATH';
const SITE_TAGLINE = 'Production AI engineering patterns for senior engineers and technical leaders.';

async function generateLlmsTxt() {
  console.log('🤖 Generating llms.txt files for AI crawlers...\n');
  
  const posts = await getAllPosts();
  console.log(`📚 Found ${posts.length} published posts\n`);
  
  // Generate llms.txt (summary version)
  const llmsTxt = generateSummary(posts);
  await fs.writeFile(path.join(OUTPUT_DIR, 'llms.txt'), llmsTxt);
  console.log('✅ Generated public/llms.txt');
  
  // Generate llms-full.txt (complete content)
  const llmsFullTxt = await generateFull(posts);
  await fs.writeFile(path.join(OUTPUT_DIR, 'llms-full.txt'), llmsFullTxt);
  console.log('✅ Generated public/llms-full.txt');
  
  // Stats
  const llmsSize = (Buffer.byteLength(llmsTxt, 'utf8') / 1024).toFixed(1);
  const fullSize = (Buffer.byteLength(llmsFullTxt, 'utf8') / 1024).toFixed(1);
  console.log(`\n📊 File sizes: llms.txt (${llmsSize}KB), llms-full.txt (${fullSize}KB)`);
}

async function getAllPosts() {
  const files = await fs.readdir(BLOG_DIR);
  const posts = await Promise.all(
    files
      .filter(f => f.endsWith('.mdx') || f.endsWith('.md'))
      .map(async (file) => {
        const content = await fs.readFile(path.join(BLOG_DIR, file), 'utf-8');
        const { data, content: body } = matter(content);
        return {
          ...data,
          slug: file.replace(/\.mdx?$/, ''),
          body
        };
      })
  );
  
  return posts
    .filter(p => !p.draft)
    .sort((a, b) => new Date(b.date) - new Date(a.date));
}

function generateSummary(posts) {
  const grouped = groupByCategory(posts);
  
  let output = `# ${SITE_NAME}

> ${SITE_TAGLINE}
> Code-first, practitioner-focused content on agentic AI, context engineering,
> and LLM cost optimization.

## Recent Posts

${posts.slice(0, 5).map(p => 
  `- [${p.title}](/blog/${p.slug}): ${p.description || 'No description'}`
).join('\n')}

## Topics
`;

  for (const [category, categoryPosts] of Object.entries(grouped)) {
    output += `
### ${category}

${categoryPosts.map(p => 
  `- [${p.title}](/blog/${p.slug}): ${p.description || 'No description'}`
).join('\n')}
`;
  }

  output += `
## About

ACIDBATH is written by a software engineer focused on production AI systems,
multi-provider agent orchestration, and AI engineering tooling. The blog
provides practical, code-first guidance for senior engineers and technical leaders.

## Contact

- Blog: https://blog.amenoacids.com
- GitHub: @yourhandle
- Twitter: @yourhandle
`;

  return output;
}

async function generateFull(posts) {
  const sections = await Promise.all(
    posts.map(async (post) => {
      const plainContent = await stripMarkdownContent(post.body);
      
      let section = `
---

## ${post.title}

*Published: ${formatDate(post.date)}*
*Category: ${post.category || 'Uncategorized'}*
*Difficulty: ${post.difficulty || 'Intermediate'}*

### TL;DR

${post.tldr || post.description || 'No summary available.'}
`;

      if (post.keyTakeaways && post.keyTakeaways.length > 0) {
        section += `
### Key Takeaways

${post.keyTakeaways.map((t, i) => `${i + 1}. ${t}`).join('\n')}
`;
      }

      section += `
### Content

${plainContent}
`;

      return section;
    })
  );
  
  return `# ${SITE_NAME} - Complete Content

> This file contains the full text of all ${SITE_NAME} blog posts,
> formatted for AI consumption.
> 
> Last updated: ${new Date().toISOString()}
> Total posts: ${posts.length}

${sections.join('\n')}
`;
}

async function stripMarkdownContent(content) {
  try {
    const result = await remark()
      .use(strip)
      .process(content);
    return String(result)
      .replace(/\n{3,}/g, '\n\n')  // Collapse multiple newlines
      .trim();
  } catch (e) {
    // Fallback: basic cleanup
    return content
      .replace(/```[\s\S]*?```/g, '[code block]')
      .replace(/`[^`]+`/g, (match) => match.slice(1, -1))
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/[#*_~]/g, '')
      .trim();
  }
}

function groupByCategory(posts) {
  return posts.reduce((acc, post) => {
    const cat = post.category || 'Uncategorized';
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(post);
    return acc;
  }, {});
}

function formatDate(date) {
  if (!date) return 'Unknown';
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// Run
generateLlmsTxt().catch(console.error);
```

## Required Dependencies

```bash
npm install gray-matter remark strip-markdown
```

## Astro Build Integration

Add to `astro.config.mjs`:

```javascript
{
  name: 'llms-txt-generator',
  hooks: {
    'astro:build:done': async () => {
      const { exec } = await import('child_process');
      const { promisify } = await import('util');
      const execAsync = promisify(exec);
      
      try {
        await execAsync('node scripts/generate-llms-txt.js');
      } catch (error) {
        console.error('Failed to generate llms.txt:', error);
      }
    }
  }
}
```

## Verification

After generation, verify files are accessible:
- https://blog.amenoacids.com/llms.txt
- https://blog.amenoacids.com/llms-full.txt

## AI Crawler Notes

Current AI crawlers that may use these files:
- GPTBot (OpenAI)
- ClaudeBot (Anthropic)
- PerplexityBot
- Google-Extended

The llms.txt standard is emerging but not yet universally adopted. Early implementation provides first-mover advantage as AI search grows.
