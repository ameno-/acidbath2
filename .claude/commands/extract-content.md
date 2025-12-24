# Content Extraction Pipeline

Extract derivative content from a blog post for Typefully social publishing.

## Usage

Run this command after publishing a blog post:
```
/project:extract-content path/to/blog-post.md
```

## What This Command Does

1. Reads the source blog post
2. Generates platform-specific content for Typefully:
   - X/Twitter thread (8-12 tweets, 280 chars each)
   - LinkedIn post (up to 3000 chars)
   - Bluesky post (300 chars)
   - Threads post (500 chars)
   - Mastodon post (500 chars)
3. Creates `typefully-content.json` for API publishing
4. Validates content for platform character limits
5. Saves outputs to `content/derivatives/{slug}/`

**Note**: Developer communities (dev.to, Hashnode) and newsletter (Buttondown) are handled automatically via RSS import. See `ai_docs/rss-setup-guide.md`.

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
- Maximum 3000 characters
- Professional but not stiff

---

## Bluesky Post Guidelines

**Character Limit:** 300 characters

**Structure:**
- Single impactful statement or insight
- Include link to full post
- Use clear, direct language

**Rules:**
- No hashtags needed
- Can include @mentions
- Links count toward character limit
- Keep it punchy—less is more

**Example:**
> Context window optimization isn't about cramming more in—it's about ruthless prioritization.
>
> Full deep-dive: blog.amenoacids.com/context-engineering

---

## Threads Post Guidelines

**Character Limit:** 500 characters

**Structure:**
- Hook + single key insight
- Optional: include one code snippet reference
- CTA with link

**Rules:**
- More casual than LinkedIn
- Visual/code references work well
- Can be more opinionated
- Link to full post

**Example:**
> Every agent codebase I review has the same problem: context bloat.
>
> Engineers dump everything into the prompt, wonder why costs explode, then blame the model.
>
> The fix is progressive disclosure. Full breakdown → blog.amenoacids.com/context-engineering

---

## Mastodon Post Guidelines

**Character Limit:** 500 characters (default, varies by instance)

**Structure:**
- Clear technical insight
- Link to full post
- Optional content warning for long threads

**Rules:**
- No engagement bait
- Technical content appreciated
- Can use CamelCaseHashtags if relevant
- Be genuine, not promotional

**Example:**
> New blog post on context engineering for AI agents.
>
> Key insight: Progressive disclosure beats RAG for most agent use cases. Cut our context by 90% while improving accuracy.
>
> Technical deep-dive: blog.amenoacids.com/context-engineering
>
> #AI #LLM #Engineering

---

## Output Format

Generate these files in `content/derivatives/{slug}/`:

```
content/derivatives/{slug}/
├── twitter-thread.md      # X/Twitter thread content
├── linkedin-post.md       # LinkedIn post content
├── bluesky-post.md        # Bluesky post content
├── threads-post.md        # Threads post content
├── mastodon-post.md       # Mastodon post content
├── typefully-content.json # Typefully API-ready payload
└── metadata.json          # Post metadata
```

### typefully-content.json

This file is ready to send directly to the Typefully API:

```json
{
  "draft_title": "Post Title",
  "tags": ["blog"],
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [
        {"text": "First tweet (hook)"},
        {"text": "Second tweet (insight 1)"},
        {"text": "Third tweet (insight 2)"},
        {"text": "Final tweet with link to blog.amenoacids.com/slug"}
      ]
    },
    "linkedin": {
      "enabled": true,
      "posts": [{"text": "LinkedIn post content (up to 3000 chars)"}]
    },
    "bluesky": {
      "enabled": true,
      "posts": [{"text": "Bluesky post (300 chars max)"}]
    },
    "threads": {
      "enabled": true,
      "posts": [{"text": "Threads post (500 chars max)"}]
    },
    "mastodon": {
      "enabled": true,
      "posts": [{"text": "Mastodon post (500 chars max)"}]
    }
  }
}
```

### metadata.json

```json
{
  "slug": "post-slug",
  "title": "Post Title",
  "description": "SEO meta description",
  "canonicalUrl": "https://blog.amenoacids.com/blog/post-slug",
  "publishedDate": "2025-01-15",
  "extractedAt": "2025-01-15T10:00:00Z",
  "platforms": {
    "x": { "tweetCount": 8, "valid": true },
    "linkedin": { "characterCount": 1200, "valid": true },
    "bluesky": { "characterCount": 280, "valid": true },
    "threads": { "characterCount": 450, "valid": true },
    "mastodon": { "characterCount": 480, "valid": true }
  }
}
```

---

## Example Extraction

**Source Post**: "Your Context Window Is Bleeding"

**Twitter Hook:**
> Your context window is bleeding.
>
> I see it in every agent codebase I review: engineers dump everything into context, wonder why costs explode, then blame the model.
>
> Here's the fix:

**LinkedIn Opening:**
> Last week I audited an agent system burning $3,000/day on API costs.
>
> The culprit? Context bloat. They were stuffing 180K tokens into every request when they needed 20K.
>
> This is the #1 mistake I see engineering teams make with AI agents...

**Bluesky:**
> Context engineering > prompt engineering. Most agents fail because they stuff everything into context instead of prioritizing.
>
> New post on fixing this: blog.amenoacids.com/context-engineering

---

## Post-Extraction Checklist

- [ ] Review hook for punch (would YOU stop scrolling?)
- [ ] Verify each tweet stands alone
- [ ] Check LinkedIn doesn't give away everything
- [ ] Verify all posts include link to blog
- [ ] Validate character counts are within limits
- [ ] Ensure typefully-content.json is valid JSON

---

## Publishing Workflow

After content extraction:

### 1. Review Generated Content
```bash
# Check the generated files
cat content/derivatives/{slug}/typefully-content.json | jq '.platforms.x.posts'
```

### 2. Create Typefully Draft
```bash
# Create draft for review (doesn't publish)
uv run python -c "
import json
from adws.adw_modules.typefully_ops import TypefullyClient, TypefullyConfig

with open('content/derivatives/{slug}/typefully-content.json') as f:
    content = json.load(f)

config = TypefullyConfig.from_env()
client = TypefullyClient(config)

result = client.create_draft(
    platforms=content['platforms'],
    draft_title=content['draft_title'],
    tags=content.get('tags', []),
    publish_at=None  # Save as draft
)

print(f'Draft created: {result.private_url}')
"
```

### 3. Review in Typefully UI
- Go to the draft URL
- Preview on each platform
- Make any final edits
- Publish or schedule

### 4. RSS Handles the Rest
- dev.to will auto-import within 24 hours
- Hashnode: trigger manual RSS import
- Buttondown: included in next digest

---

## Platform Character Limits Reference

| Platform | Limit | Notes |
|----------|-------|-------|
| X/Twitter | 280/tweet | Thread up to 25 tweets |
| LinkedIn | 3000 | Single post |
| Bluesky | 300 | Links count toward limit |
| Threads | 500 | Single post |
| Mastodon | 500 | Default, varies by instance |
