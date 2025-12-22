# ACIDBATH Blog Review & Improvement Plan

## Executive Summary

Your current blog has strong content fundamentals—practical AI engineering posts targeting senior engineers. However, the layout and design need significant upgrades to match the authority of your content, and you're missing a major opportunity: **optimizing for AI crawlers** so that AI tools cite and learn from your work.

This document covers:
1. Current state review
2. Human UX improvements
3. AI optimization (the novel opportunity)
4. Implementation via Claude Code commands and skills

---

## Part 1: Current State Review

### What I Observed

**Homepage (blog.amenoacids.com):**
```
ACIDBATH
- Banner image
- Tagline: "The critical, code-first voice that senior technical leaders trust."
- Navigation: Home | Blog | About
- 3 posts listed with dates, titles, descriptions, tags
- Footer: © 2025 ACIDBATH · Built with Astro
```

**Current Posts:**
1. "AI Document Skills: Automated File Generation That Actually Ships" (Dec 16)
2. "Workflow Prompts: The Pattern That Makes AI Engineering Predictable" (Dec 14)  
3. "Context Engineering: From Token Optimization to Large Codebase Mastery" (Dec 14)

### Strengths

✅ **Strong positioning**: "The critical, code-first voice" is excellent  
✅ **Quality topic selection**: Context engineering, workflow prompts, document skills—all high-value keywords  
✅ **Technical credibility**: Practical, code-focused content  
✅ **Astro foundation**: Fast, modern framework  
✅ **Clean URL structure**: `/blog/{slug}` is SEO-friendly  
✅ **Tags present**: Good for categorization  

### Weaknesses

❌ **No AI optimization**: No llms.txt, no structured data for AI crawlers  
❌ **Minimal design system**: Generic blog layout, no distinctive visual identity  
❌ **No reading time or difficulty indicators**: Senior engineers want to know upfront  
❌ **No table of contents**: Long technical posts need navigation  
❌ **No code copy buttons**: Essential for code-heavy content  
❌ **No syntax highlighting customization**: Code blocks need better treatment  
❌ **No "Start Here" page**: New visitors need orientation  
❌ **No newsletter signup**: Missing owned audience opportunity  
❌ **No related posts**: Reduces session depth  
❌ **No author credibility section**: Who is writing this?  
❌ **No search functionality**: Technical blogs need search  
❌ **No RSS feed visibility**: Engineers love RSS  

---

## Part 2: Human UX Improvements

### 2.1 Post Layout Redesign

**Current**: Basic post with title, date, content, tags

**Recommended Structure**:

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Breadcrumb: Home > Blog > Category]                               │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ [Category Badge]  [Difficulty: Advanced]  [Reading Time: 12m] │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  # Post Title                                                       │
│  Published Dec 14, 2025 · Updated Dec 15, 2025                      │
│                                                                     │
│  ┌─────────────────┐ ┌──────────────────────────────────────────┐   │
│  │ TABLE OF        │ │                                          │   │
│  │ CONTENTS        │ │  ## TL;DR                                │   │
│  │                 │ │  Key insight in 2-3 sentences...         │   │
│  │ - TL;DR         │ │                                          │   │
│  │ - The Problem   │ │  ## The Problem                          │   │
│  │ - The Pattern   │ │  Content...                              │   │
│  │ - Implementation│ │                                          │   │
│  │ - Code Examples │ │  ```python                               │   │
│  │ - Benchmarks    │ │  # Code with copy button                 │   │
│  │ - What's Next   │ │  def example():                          │   │
│  │                 │ │      pass                    [📋 Copy]   │   │
│  │ [Sticky on      │ │  ```                                     │   │
│  │  scroll]        │ │                                          │   │
│  └─────────────────┘ └──────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 📧 Get more posts like this                                   │   │
│  │ [Email input] [Subscribe]                                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Related Posts                                                 │   │
│  │ ┌────────┐ ┌────────┐ ┌────────┐                              │   │
│  │ │ Post 1 │ │ Post 2 │ │ Post 3 │                              │   │
│  │ └────────┘ └────────┘ └────────┘                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Code Block Enhancements

Technical blogs live and die by code presentation. Implement:

```astro
<!-- Ideal code block component -->
<CodeBlock 
  language="python"
  title="context_manager.py"
  showLineNumbers={true}
  highlightLines={[3, 4, 5]}
  collapsible={true}
  defaultCollapsed={false}
>
  {code}
</CodeBlock>
```

**Features needed:**
- Copy button (top-right corner)
- Language indicator
- Optional filename/title
- Line numbers for reference
- Line highlighting for emphasis
- Collapsible for long blocks
- Diff highlighting for before/after
- Terminal output distinction (different styling)

**Font recommendation**: JetBrains Mono or Fira Code with ligatures

### 2.3 Typography & Reading Experience

**Current issues**: Generic fonts, likely default Astro styling

**Recommendations:**

```css
/* Body text */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
font-size: 18px;
line-height: 1.7;
max-width: 680px; /* Optimal reading width */

/* Headings */
font-family: 'Space Grotesk', sans-serif; /* Distinctive, technical feel */

/* Code */
font-family: 'JetBrains Mono', 'Fira Code', monospace;
font-size: 14px;
```

**Spacing:**
- Generous paragraph spacing (1.5em minimum)
- Clear heading hierarchy (H2: 32px, H3: 24px, H4: 20px)
- White space around code blocks (32px top/bottom)

### 2.4 Visual Identity System

**Brand Elements to Develop:**

1. **Color Palette** (suggestion based on "ACIDBATH" name):
   - Primary: Electric green (#00FF41) - the "acid" terminal green
   - Dark: Near-black (#0D0D0D) - deep background
   - Light: Off-white (#F5F5F5) - readable background
   - Accent: Amber (#FFB800) - warnings, highlights
   - Code bg: Charcoal (#1A1A2E) - code blocks

2. **Visual Motifs**:
   - Terminal/CLI aesthetic
   - Monospace typography accents
   - Subtle grid or circuit patterns
   - ASCII art elements (sparingly)

3. **Iconography**:
   - Custom icons for categories (agents, context, prompts, etc.)
   - Consistent icon style (line-based, not filled)

### 2.5 Homepage Improvements

**Current**: Basic post list

**Recommended Structure:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ACIDBATH                                                           │
│  Production AI Engineering for Senior Leaders                       │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 📚 Start Here: New to ACIDBATH?                                │ │
│  │ → The 3 posts that define our approach                         │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  Featured Post                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ [Hero card with excerpt, tags, reading time]                   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  Recent Posts                     Topics                            │
│  ┌───────────────────────┐       ┌────────────────────┐             │
│  │ Post cards (3-5)      │       │ • Context Engineering           │
│  │ - Title               │       │ • Agentic Patterns              │
│  │ - Date                │       │ • Claude Code                   │
│  │ - 1-line description  │       │ • Cost Optimization             │
│  │ - Read time           │       │ • Production Patterns           │
│  │ - Tags                │       │                    │             │
│  └───────────────────────┘       └────────────────────┘             │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 📧 Subscribe for production AI insights                        │ │
│  │ [Email] [Subscribe]                                            │ │
│  │ No spam. Unsubscribe anytime.                                  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  RSS • GitHub • Twitter/X • About                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.6 Essential New Pages

1. **Start Here** (`/start`): 
   - Who this blog is for
   - Core philosophy (the "Muad'Dib" vision)
   - 3-5 foundational posts to read first
   - How to get the most value

2. **Topics/Categories** (`/topics`):
   - Organized by theme, not just chronological
   - Visual categorization
   - "Learning paths" for topics with multiple posts

3. **About** (improve existing):
   - Your credibility (experience, projects)
   - Photo (builds trust)
   - Contact/social links
   - Speaking/consulting if applicable

---

## Part 3: AI Optimization (The Novel Opportunity)

This is the **differentiator**. While everyone optimizes for Google, few are optimizing for AI crawlers (ChatGPT, Claude, Perplexity). You can be early.

### 3.1 Implement llms.txt

Create `/llms.txt` in your site root:

```markdown
# ACIDBATH

> Production AI engineering patterns for senior engineers and technical leaders.
> Code-first, practitioner-focused content on agentic AI, context engineering,
> and LLM cost optimization.

## Core Content

- [Context Engineering Guide](/blog/context-engineering): Progressive disclosure and semantic search patterns for managing LLM context windows efficiently. Includes working code and benchmarks.

- [Workflow Prompts Pattern](/blog/workflow-prompts): The workflow section architecture that makes agentic prompts predictable. Template-based approach with ROI measurement.

- [AI Document Skills](/blog/document-generation-skills): Automated Excel, PowerPoint, and PDF generation using Claude. Production code with token analysis.

## Topics

### Context Engineering
Techniques for optimizing LLM context windows, progressive disclosure patterns, and cost-efficient context management.

### Agentic Patterns  
Sub-agent orchestration, workflow prompts, and production patterns for AI agents.

### Claude Code
Best practices, commands, and workflows for Claude Code development.

## About

ACIDBATH is written by [Your Name], a software engineer building production AI systems. Focus areas include multi-provider agent orchestration, context optimization, and AI engineering tooling.

## Contact

- Twitter: @yourhandle
- GitHub: @yourhandle
- Email: contact@amenoacids.com
```

### 3.2 Create llms-full.txt

For AI tools that want the complete content:

```markdown
# ACIDBATH - Complete Content

> This file contains the full text of all ACIDBATH blog posts,
> formatted for AI consumption.

---

## Context Engineering: From Token Optimization to Large Codebase Mastery

*Published: December 14, 2025*
*Category: Context Engineering*
*Difficulty: Advanced*

[Full post content in clean markdown, no HTML]

---

## Workflow Prompts: The Pattern That Makes AI Engineering Predictable

*Published: December 14, 2025*
*Category: Agentic Patterns*
*Difficulty: Intermediate*

[Full post content...]

---

[Continue for all posts]
```

### 3.3 Structured Data for AI

Add JSON-LD to every post:

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Context Engineering: From Token Optimization to Large Codebase Mastery",
  "description": "Progressive disclosure and semantic search patterns for managing LLM context windows efficiently.",
  "author": {
    "@type": "Person",
    "name": "Your Name",
    "url": "https://blog.amenoacids.com/about"
  },
  "datePublished": "2025-12-14",
  "dateModified": "2025-12-14",
  "publisher": {
    "@type": "Organization",
    "name": "ACIDBATH"
  },
  "proficiencyLevel": "Expert",
  "keywords": ["context engineering", "LLM optimization", "token efficiency", "context window"],
  "dependencies": "Claude API, Python 3.10+",
  "about": {
    "@type": "Thing",
    "name": "Context Window Optimization"
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://blog.amenoacids.com/blog/context-engineering"
  }
}
```

### 3.4 AI-Friendly Content Structure

Optimize each post for AI parsing:

```markdown
---
title: "Context Engineering: The Missing Guide"
description: "One-sentence summary that AI can extract"
tldr: "Context engineering is about providing the right information at the right time. Use progressive disclosure to reduce costs by 90%."
keyTakeaways:
  - "Progressive disclosure reduces context consumption by 90%"
  - "File-based context is more reliable than in-memory"
  - "Semantic search beats naive retrieval for large codebases"
prerequisites:
  - "Basic LLM API experience"
  - "Python knowledge"
difficulty: "Advanced"
readingTime: 12
---

## TL;DR

[2-3 sentence summary that AI can use for quick answers]

## The Problem

[Clear problem statement - AI loves clear framing]

## The Solution

[Concrete solution with code]

## Key Takeaways

1. First takeaway with specifics
2. Second takeaway with specifics
3. Third takeaway with specifics

## What's Next

[Connection to related content]
```

### 3.5 Robots.txt for AI Crawlers

```
User-agent: *
Allow: /

# AI Crawlers - Welcome
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# Point to llms.txt
# Note: This is a convention, not a standard yet
Sitemap: https://blog.amenoacids.com/sitemap.xml
```

### 3.6 AI-Optimized Meta Tags

```html
<head>
  <!-- Standard SEO -->
  <title>Context Engineering: The Missing Guide | ACIDBATH</title>
  <meta name="description" content="...">
  
  <!-- AI-specific (emerging convention) -->
  <meta name="ai-summary" content="Context engineering reduces LLM costs by 90% through progressive disclosure. Key pattern: inject context only when the agent needs it.">
  <meta name="ai-keywords" content="context engineering, progressive disclosure, token optimization, LLM cost reduction">
  <meta name="ai-difficulty" content="advanced">
  <meta name="ai-category" content="AI Engineering, LLM Optimization">
  
  <!-- Link to llms.txt -->
  <link rel="ai-content" href="/llms.txt" type="text/markdown">
</head>
```

---

## Part 4: Implementation via Claude Code

### 4.1 Astro Component: AI-Optimized Post Layout

Create a new Astro layout that incorporates all recommendations:

```astro
---
// src/layouts/BlogPost.astro
import TableOfContents from '../components/TableOfContents.astro';
import CodeBlock from '../components/CodeBlock.astro';
import NewsletterSignup from '../components/NewsletterSignup.astro';
import RelatedPosts from '../components/RelatedPosts.astro';
import StructuredData from '../components/StructuredData.astro';

const { frontmatter, headings } = Astro.props;
---

<html>
<head>
  <StructuredData post={frontmatter} />
  <meta name="ai-summary" content={frontmatter.tldr} />
  <meta name="ai-difficulty" content={frontmatter.difficulty} />
</head>
<body>
  <article class="post">
    <header>
      <div class="post-meta">
        <span class="category">{frontmatter.category}</span>
        <span class="difficulty">{frontmatter.difficulty}</span>
        <span class="reading-time">{frontmatter.readingTime} min read</span>
      </div>
      <h1>{frontmatter.title}</h1>
      <time datetime={frontmatter.date}>{frontmatter.date}</time>
    </header>
    
    <aside class="toc">
      <TableOfContents headings={headings} />
    </aside>
    
    <div class="content">
      {frontmatter.tldr && (
        <div class="tldr">
          <h2>TL;DR</h2>
          <p>{frontmatter.tldr}</p>
        </div>
      )}
      
      <slot />
      
      {frontmatter.keyTakeaways && (
        <div class="takeaways">
          <h2>Key Takeaways</h2>
          <ol>
            {frontmatter.keyTakeaways.map(t => <li>{t}</li>)}
          </ol>
        </div>
      )}
    </div>
    
    <NewsletterSignup />
    <RelatedPosts currentPost={frontmatter.slug} tags={frontmatter.tags} />
  </article>
</body>
</html>
```

### 4.2 Claude Code Skill: LLMs.txt Generator

Create this as a skill for your workflow:

**File: `.claude/skills/llms-txt-generator/SKILL.md`**

```markdown
# LLMs.txt Generator Skill

Generate and maintain llms.txt and llms-full.txt files for AI crawler optimization.

## When to Use

- After publishing new blog posts
- When updating existing content
- During site rebuilds

## Process

1. Scan all posts in `src/content/blog/`
2. Extract frontmatter and content
3. Generate structured llms.txt with summaries
4. Generate llms-full.txt with complete content
5. Output to `public/llms.txt` and `public/llms-full.txt`

## llms.txt Format

```markdown
# ACIDBATH

> [Site tagline from config]

## Core Content

[For each post, sorted by importance/recency:]
- [Post Title](/blog/slug): [Description from frontmatter]

## Topics

[Group posts by category/tag]

## About

[From about page or config]
```

## llms-full.txt Format

```markdown
# ACIDBATH - Complete Content

[For each post:]

---

## [Post Title]

*Published: [Date]*
*Category: [Category]*
*Difficulty: [Difficulty]*

### TL;DR
[tldr from frontmatter]

### Key Takeaways
[keyTakeaways from frontmatter]

### Content
[Full post content, cleaned of HTML]

---
```

## Implementation

Run this command to regenerate:
```bash
node scripts/generate-llms-txt.js
```
```

### 4.3 Claude Code Command: Post Creation Workflow

**File: `.claude/commands/new-post.md`**

```markdown
# Create New Blog Post

Create a new blog post with all required frontmatter and AI optimization fields.

## Usage

```
/project:new-post "Post Title" --category="Context Engineering" --difficulty="Advanced"
```

## Process

1. Generate slug from title
2. Create file at `src/content/blog/{slug}.mdx`
3. Add complete frontmatter template
4. Create placeholder sections
5. Update llms.txt

## Frontmatter Template

```yaml
---
title: "{title}"
description: "" # REQUIRED: One sentence for SEO and AI
tldr: "" # REQUIRED: 2-3 sentences for AI quick answers
keyTakeaways:
  - "" # REQUIRED: 3-5 specific takeaways
  - ""
  - ""
category: "{category}"
tags: []
difficulty: "{difficulty}" # Beginner | Intermediate | Advanced
readingTime: 0 # Will be calculated
date: "{date}"
updated: "{date}"
draft: true
author: "Your Name"
prerequisites:
  - "" # What readers should know first
relatedPosts: [] # Slugs of related posts
---
```

## Section Template

```markdown
## TL;DR

[Expand on the tldr - this is what AI will cite]

## The Problem

[Clear problem statement]

## The Solution

[Your approach]

## Implementation

[Code and details]

## Benchmarks / Results

[Concrete numbers]

## What's Next

[Connection to related content or future posts]
```

## Post-Creation Checklist

- [ ] Fill in description (one sentence)
- [ ] Write tldr (2-3 sentences)
- [ ] Add 3-5 key takeaways
- [ ] Set appropriate tags
- [ ] Calculate reading time
- [ ] Add prerequisites if advanced
- [ ] Link related posts
- [ ] Remove draft: true when ready
```

### 4.4 Claude Code Command: AI Optimization Audit

**File: `.claude/commands/audit-ai-optimization.md`**

```markdown
# Audit AI Optimization

Check all posts for AI optimization compliance.

## Usage

```
/project:audit-ai-optimization
```

## Checks

For each post, verify:

### Required Fields
- [ ] `description` exists and is < 160 chars
- [ ] `tldr` exists and is 2-3 sentences
- [ ] `keyTakeaways` has 3-5 items
- [ ] `difficulty` is set
- [ ] `category` is set
- [ ] `readingTime` is calculated

### Content Structure
- [ ] Has ## TL;DR section
- [ ] Has clear heading hierarchy (no skipped levels)
- [ ] Code blocks have language specified
- [ ] Has ## Key Takeaways section

### Structured Data
- [ ] JSON-LD is valid
- [ ] proficiencyLevel matches difficulty
- [ ] keywords match tags

## Output

Generate report:
```
AI Optimization Audit Report
============================

✅ 3 posts fully optimized
⚠️ 1 post missing tldr
❌ 1 post missing keyTakeaways

Details:
- context-engineering.mdx: ✅ All checks passed
- workflow-prompts.mdx: ⚠️ Missing prerequisites
- document-skills.mdx: ❌ Missing tldr, keyTakeaways
```
```

### 4.5 Build Script: Generate LLMs Files

**File: `scripts/generate-llms-txt.js`**

```javascript
// scripts/generate-llms-txt.js
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import strip from 'strip-markdown';

const BLOG_DIR = 'src/content/blog';
const OUTPUT_DIR = 'public';

async function generateLlmsTxt() {
  const posts = await getAllPosts();
  
  // Generate llms.txt (summary version)
  const llmsTxt = generateSummary(posts);
  await fs.writeFile(
    path.join(OUTPUT_DIR, 'llms.txt'), 
    llmsTxt
  );
  
  // Generate llms-full.txt (complete content)
  const llmsFullTxt = await generateFull(posts);
  await fs.writeFile(
    path.join(OUTPUT_DIR, 'llms-full.txt'), 
    llmsFullTxt
  );
  
  console.log('✅ Generated llms.txt and llms-full.txt');
}

async function getAllPosts() {
  const files = await fs.readdir(BLOG_DIR);
  const posts = await Promise.all(
    files
      .filter(f => f.endsWith('.mdx') || f.endsWith('.md'))
      .map(async (file) => {
        const content = await fs.readFile(
          path.join(BLOG_DIR, file), 
          'utf-8'
        );
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
  
  return `# ACIDBATH

> Production AI engineering patterns for senior engineers and technical leaders.
> Code-first, practitioner-focused content on agentic AI, context engineering,
> and LLM cost optimization.

## Recent Posts

${posts.slice(0, 5).map(p => 
  `- [${p.title}](/blog/${p.slug}): ${p.description}`
).join('\n')}

## Topics

${Object.entries(grouped).map(([category, categoryPosts]) => `
### ${category}

${categoryPosts.map(p => 
  `- [${p.title}](/blog/${p.slug}): ${p.description}`
).join('\n')}
`).join('\n')}

## About

ACIDBATH is written by [Your Name], focusing on production AI systems,
multi-provider agent orchestration, and AI engineering tooling.

## Contact

- Twitter: @yourhandle
- GitHub: @yourhandle
`;
}

async function generateFull(posts) {
  const sections = await Promise.all(
    posts.map(async (post) => {
      const plainContent = await stripMarkdown(post.body);
      
      return `
---

## ${post.title}

*Published: ${post.date}*
*Category: ${post.category || 'Uncategorized'}*
*Difficulty: ${post.difficulty || 'Intermediate'}*

### TL;DR

${post.tldr || post.description}

${post.keyTakeaways ? `### Key Takeaways

${post.keyTakeaways.map((t, i) => `${i + 1}. ${t}`).join('\n')}
` : ''}

### Content

${plainContent}
`;
    })
  );
  
  return `# ACIDBATH - Complete Content

> This file contains the full text of all ACIDBATH blog posts,
> formatted for AI consumption. Last updated: ${new Date().toISOString()}

${sections.join('\n')}
`;
}

async function stripMarkdown(content) {
  const result = await remark()
    .use(strip)
    .process(content);
  return String(result);
}

function groupByCategory(posts) {
  return posts.reduce((acc, post) => {
    const cat = post.category || 'Uncategorized';
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(post);
    return acc;
  }, {});
}

generateLlmsTxt();
```

### 4.6 Astro Integration: Auto-Generate on Build

**File: `astro.config.mjs` (addition)**

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  // ... existing config
  
  integrations: [
    // ... existing integrations
    {
      name: 'llms-txt-generator',
      hooks: {
        'astro:build:done': async () => {
          const { exec } = await import('child_process');
          exec('node scripts/generate-llms-txt.js', (error, stdout) => {
            if (error) {
              console.error('Failed to generate llms.txt:', error);
              return;
            }
            console.log(stdout);
          });
        }
      }
    }
  ]
});
```

---

## Part 5: Implementation Checklist

### Phase 1: Foundation (Week 1)

- [ ] Implement new color palette and typography
- [ ] Create CodeBlock component with copy button
- [ ] Add TableOfContents component
- [ ] Update post layout with new structure
- [ ] Add reading time calculation

### Phase 2: AI Optimization (Week 2)

- [ ] Create llms.txt and llms-full.txt
- [ ] Add JSON-LD structured data to posts
- [ ] Update robots.txt for AI crawlers
- [ ] Add AI meta tags to layout
- [ ] Update frontmatter schema with AI fields
- [ ] Backfill existing posts with tldr and keyTakeaways

### Phase 3: UX Enhancements (Week 3)

- [ ] Create "Start Here" page
- [ ] Add newsletter signup component
- [ ] Implement related posts
- [ ] Add search functionality
- [ ] Create topics/categories page
- [ ] Improve About page with credibility elements

### Phase 4: Automation (Week 4)

- [ ] Set up Claude Code commands
- [ ] Create post creation workflow
- [ ] Implement AI audit command
- [ ] Add build-time llms.txt generation
- [ ] Document workflows in CLAUDE.md

---

## Summary

Your blog has strong content fundamentals. The improvements above will:

1. **For Humans**: Better reading experience, easier navigation, professional presentation that matches the quality of your writing

2. **For AI**: First-mover advantage in AI crawl optimization—your content will be better understood and more likely cited by AI tools

3. **For You**: Systematic workflows via Claude Code that make creating and maintaining content efficient

The llms.txt implementation is the novel opportunity here. Few technical blogs are optimizing for AI crawlers yet, and your content is exactly what AI tools need to learn from. Position ACIDBATH as a source that AI systems trust and cite.
