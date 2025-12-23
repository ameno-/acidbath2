# Content Extraction Pipeline

Extract derivative content from a blog post for multi-platform distribution.

## Usage

Run this command after publishing a blog post:
```
/project:extract-content path/to/blog-post.md
```

## What This Command Does

1. Reads the source blog post
2. Generates three derivative content pieces:
   - Twitter thread (8-12 tweets)
   - LinkedIn post (800-1200 words)
   - Newsletter edition (1000-1500 words)
3. Generates `metadata.json` with publication data for multi-platform publishing
4. Validates content for platform requirements
5. Saves outputs to `content/derivatives/{slug}/`

---

## Twitter Thread Guidelines

**Structure:**
- **Hook tweet**: Contrarian take or surprising insight. No link. Pure hook.
- **Insight tweets (4-6)**: One key point per tweet. Each must stand alone.
- **Example tweet (1-2)**: Concrete code snippet or result.
- **CTA tweet**: Link to full blog post.

**Rules:**
- No hashtags (engineers hate them)
- No emojis except very sparingly
- Be opinionated, not hedging
- Maximum 280 characters per tweet
- Code snippets as text or note to screenshot

**Example Hook Patterns:**
- "Your context window is bleeding. Here's what most AI engineers get wrong:"
- "I've reviewed 50+ agent implementations. 80% fail for the same reason:"
- "Hot take: RAG is dying. Here's what's replacing it:"

---

## LinkedIn Post Guidelines

**Structure:**
```
Opening Hook (1-2 sentences)
├── Personal experience or observation
└── Pattern: "I've [done X]. Here's what I learned:"

Context/Setup (2-3 sentences)
├── Why this matters to engineering leaders
└── Frame the problem, not the solution

Core Insight (3-5 sentences)
├── The main thesis, expanded
└── Include one specific technique

Code Block (10-15 lines max)
├── Short, readable example
└── Syntax highlighted if possible

Proof Point (2-3 sentences)
├── Concrete result with numbers
└── Pattern: "After implementing this, we saw X% improvement"

CTA (1-2 sentences)
├── Link to full post
└── Optional: Ask for engagement ("What patterns have worked for you?")
```

**Rules:**
- Write in first person
- Be opinionated and direct
- Short paragraphs (1-3 sentences)
- No bullet points unless listing 3+ items
- Professional but not stiff
- 800-1200 words total

---

## Newsletter Edition Guidelines

**Structure:**
```
Personal Opening (2-3 sentences)
├── What prompted this post
└── Pattern: "I spent last week [doing X]. It led me to..."

Story/Context (1-2 paragraphs)
├── Narrative framing
└── Why you care about this topic

The Big Idea (1-2 paragraphs)
├── Core thesis from blog post
└── Slightly different angle than Twitter/LinkedIn

Key Technique (1 paragraph + optional code)
├── One actionable takeaway
└── Tease the depth, don't give everything

What I'm Reading/Thinking (optional)
├── 2-3 related links with commentary
└── Industry trends you're following

CTA
├── Link to full post
└── Pattern: "Full implementation with code: [link]"
```

**Rules:**
- First person, conversational
- More personal than LinkedIn
- Don't reproduce the full post—create complementary content
- Include your opinions and reactions
- 1000-1500 words total

---

## Output Format

For each derivative, create a separate markdown file:

```
content/derivatives/{slug}/
├── twitter-thread.md
├── linkedin-post.md
├── newsletter-edition.md
├── metadata.json          # Publishing metadata
└── publish-ready.json     # Marker file indicating content is ready to publish
```

Each markdown file should include:
1. Platform-specific metadata (character counts, etc.)
2. The formatted content
3. Any notes for manual review

The `metadata.json` file should include:
```json
{
  "slug": "post-slug",
  "title": "Post Title",
  "description": "SEO meta description (150-160 chars)",
  "tags": ["tag1", "tag2", "tag3"],
  "publishedDate": "2025-01-15",
  "canonicalUrl": "https://acidbath.pages.dev/blog/post-slug",
  "coverImage": "/images/cover.png",
  "author": "Ameno",
  "wordCount": 2500,
  "readingTime": 10,
  "platforms": {
    "twitter": {
      "content": "twitter-thread.md",
      "characterCount": 1500,
      "tweetCount": 10,
      "valid": true
    },
    "linkedin": {
      "content": "linkedin-post.md",
      "characterCount": 1000,
      "valid": true
    },
    "devto": {
      "title": "Post Title",
      "tags": ["ai", "engineering"],
      "valid": true
    },
    "hashnode": {
      "title": "Post Title",
      "tags": ["ai", "engineering"],
      "valid": true
    },
    "medium": {
      "title": "Post Title",
      "tags": ["ai", "engineering"],
      "valid": true
    },
    "newsletter": {
      "content": "newsletter-edition.md",
      "characterCount": 1200,
      "valid": true
    }
  }
}
```

The `publish-ready.json` marker file indicates all content is extracted and validated:
```json
{
  "ready": true,
  "extractedAt": "2025-01-15T10:00:00Z",
  "platforms": ["twitter", "linkedin", "devto", "hashnode", "medium", "newsletter"]
}
```

---

## Example Extraction

**Source Post**: "Your Context Window Is Bleeding"

**Twitter Hook**:
> Your context window is bleeding.
> 
> I see it in every agent codebase I review: engineers dump everything into context, wonder why costs explode, then blame the model.
> 
> Here's the fix:

**LinkedIn Opening**:
> Last week I audited an agent system burning $3,000/day on API costs.
> 
> The culprit? Context bloat. They were stuffing 180K tokens into every request when they needed 20K.
> 
> This is the #1 mistake I see engineering teams make with AI agents...

**Newsletter Opening**:
> I've been thinking about context windows a lot lately.
> 
> It started when a friend asked me to review their agent architecture. Costs had ballooned from $200/day to $3,000/day in three weeks. Same functionality, same users.
> 
> The problem wasn't the model. It was how they were feeding it...

---

## Post-Extraction Checklist

- [ ] Review hook for punch (would YOU stop scrolling?)
- [ ] Verify each tweet stands alone
- [ ] Check LinkedIn doesn't give away everything
- [ ] Ensure newsletter has personal story angle
- [ ] Add specific links where noted
- [ ] Validate metadata.json contains all required fields
- [ ] Verify character counts are within platform limits
- [ ] Check tags are appropriate for each platform (max 4-5 tags)
- [ ] Ensure canonical URLs point to published blog post
- [ ] Confirm publish-ready.json marker file is created
- [ ] Schedule according to content calendar:
  - Twitter: Day of publish or next morning (Wed 8-10am EST for HN day)
  - LinkedIn: Same day, afternoon
  - Newsletter: Weekly Sunday batch

## Integration with Multi-Channel Publishing

After content extraction completes successfully:

1. The `/publish-all` skill can automatically detect and publish the content
2. Or manually trigger: `/publish-all {slug} --mode staged` for review before publishing
3. Or use npm scripts: `npm run publish:all -- --post {slug} --dry-run`

The metadata.json file provides all necessary data for automated publishing to:
- Twitter (thread from twitter-thread.md)
- LinkedIn (post from linkedin-post.md)
- dev.to (blog post content with frontmatter)
- Hashnode (blog post content with SEO metadata)
- Medium (blog post content with canonical URL)
- Newsletter (edition from newsletter-edition.md)
