# Create AI-Optimized Blog Post

Create a new blog post with complete frontmatter for both SEO and AI crawler optimization.

## Usage

```
Create a new blog post titled "Context Engineering Patterns for Production"
in the category "Context Engineering" with difficulty "Advanced"
```

## Process

1. Generate URL-friendly slug from title
2. Create file at `src/content/blog/{slug}.mdx`
3. Add complete frontmatter with AI optimization fields
4. Create section scaffolding
5. Remind to regenerate llms.txt after publishing

## Frontmatter Template

Every new post MUST include these fields:

```yaml
---
# Basic metadata
title: "Post Title"
slug: "post-slug"
date: "2025-12-22"
updated: "2025-12-22"
draft: true
author: "Your Name"

# SEO (required)
description: "" # One sentence, <160 chars, used by Google

# AI Optimization (required for llms.txt)
tldr: "" # 2-3 sentences. This is what AI will cite for quick answers.
keyTakeaways:
  - "" # Specific, actionable takeaway 1
  - "" # Specific, actionable takeaway 2  
  - "" # Specific, actionable takeaway 3

# Categorization
category: "Context Engineering" # Primary category
tags: ["context-engineering", "llm", "optimization"]
difficulty: "Advanced" # Beginner | Intermediate | Advanced

# Reading experience
readingTime: 12 # Minutes - calculate after writing
prerequisites:
  - "Basic LLM API experience"
  - "Python knowledge"

# Internal linking
relatedPosts:
  - "workflow-prompts"
  - "context-engineering"

# Structured data (for JSON-LD)
proficiencyLevel: "Expert" # Matches difficulty for schema.org
dependencies: "Claude API, Python 3.10+" # Technical requirements
---
```

## Post Section Template

```markdown
## TL;DR

[Expand the tldr from frontmatter. This section is critical for AI citation.
Be specific: include the key insight and one concrete number or result.]

## The Problem

[Clear problem statement. Frame what pain point this solves.
Senior engineers appreciate direct problem framing without fluff.]

## The Solution

[High-level approach. What pattern or technique solves this?
Include a brief conceptual explanation before diving into code.]

## Implementation

[Detailed walkthrough with complete, runnable code.
Use multiple code blocks for different files or stages.]

```python
# context_manager.py
# Include complete, working code - not snippets

def main():
    """
    Production-ready implementation.
    """
    pass
```

## Benchmarks / Results

[Concrete numbers. Token counts, cost savings, latency improvements.
"We reduced context consumption from 180K to 20K tokens" is better than
"We significantly reduced context consumption."]

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Tokens | 180K   | 20K   | 89% ↓       |
| Cost   | $2.40  | $0.27 | 89% ↓       |
| Latency| 4.2s   | 1.1s  | 74% ↓       |

## Common Pitfalls

[What can go wrong? What mistakes did you make while learning this?
This section builds trust and helps readers avoid your mistakes.]

## What's Next

[Connection to related content or future posts.
"In the next post, we'll explore..." or "For more on X, see [Related Post]"]
```

## Checklist Before Publishing

Before setting `draft: false`:

### Content Quality
- [ ] Title is specific and benefit-focused
- [ ] Description is exactly one sentence, <160 chars
- [ ] TL;DR is 2-3 sentences with a specific insight
- [ ] 3-5 key takeaways, each specific and actionable
- [ ] Code examples are complete and runnable
- [ ] Benchmarks include real numbers

### AI Optimization
- [ ] `tldr` field is filled (required for llms.txt)
- [ ] `keyTakeaways` has 3+ items
- [ ] `category` is set (for grouping in llms.txt)
- [ ] `difficulty` is set
- [ ] `proficiencyLevel` matches difficulty

### SEO
- [ ] Primary keyword in title
- [ ] Primary keyword in first 100 words
- [ ] Heading hierarchy is correct (H2 → H3, no skips)
- [ ] Internal links to related posts

### Technical
- [ ] `readingTime` is calculated
- [ ] `relatedPosts` references valid slugs
- [ ] All code blocks have language specified
- [ ] Images have alt text

## Post-Publish Steps

After setting `draft: false` and deploying:

1. **Regenerate llms.txt**:
   ```bash
   node scripts/generate-llms-txt.js
   ```

2. **Verify structured data**:
   - Check https://blog.amenoacids.com/blog/{slug}
   - Validate JSON-LD with Google's Rich Results Test

3. **Create derivative content**:
   - Run `/project:extract-content` to generate Twitter/LinkedIn/newsletter versions

4. **Submit to HN** (if appropriate):
   - Best time: Wednesday 8-10am EST
   - Use factual title, no marketing speak

## Example: Complete Frontmatter

```yaml
---
title: "Context Engineering: From Token Optimization to Large Codebase Mastery"
slug: "context-engineering"
date: "2025-12-14"
updated: "2025-12-14"
draft: false
author: "Your Name"

description: "Progressive disclosure and semantic search patterns for managing LLM context windows efficiently."

tldr: "Context engineering is about providing the right information at the right time. Progressive disclosure reduces token consumption by 90% compared to naive approaches. File-based context is more reliable than in-memory for complex agent workflows."

keyTakeaways:
  - "Progressive disclosure reduces context consumption by 90%"
  - "File-based context survives agent restarts and enables debugging"
  - "Semantic search beats keyword matching for large codebases"
  - "Context injection should happen at decision points, not upfront"
  - "Measure tokens per successful task, not just total tokens"

category: "Context Engineering"
tags: ["context-engineering", "llm", "optimization", "claude-code", "tokens"]
difficulty: "Advanced"

readingTime: 15
prerequisites:
  - "Experience with LLM APIs (Claude or GPT)"
  - "Familiarity with agentic coding workflows"
  - "Python knowledge"

relatedPosts:
  - "workflow-prompts"
  - "document-generation-skills"

proficiencyLevel: "Expert"
dependencies: "Claude API, Python 3.10+, semantic search library"
---
```

## Notes

- The `tldr` field is the most important for AI citation. Make it specific.
- `keyTakeaways` should be things someone could act on immediately.
- Avoid vague takeaways like "Context matters" - prefer "Reduce context by 90% with progressive disclosure"
- The structured data (`proficiencyLevel`, `dependencies`) helps Google's TechArticle schema.
