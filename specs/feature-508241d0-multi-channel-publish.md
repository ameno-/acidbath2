# Feature: Multi-Channel Publish with Typefully + RSS

## Metadata
adw_id: `508241d0`
prompt: `Simplified multi-channel publishing using Typefully for social platforms and native RSS import for developer communities. Only 2 API keys required.`

## Feature Description
Implement a streamlined multi-channel publishing system that:
1. Uses **Typefully** for social platforms (X, LinkedIn, Bluesky, Threads, Mastodon)
2. Uses **native RSS import** for developer communities (dev.to, Hashnode)
3. Uses **RSS digest** for newsletter (Buttondown)

This approach reduces API key management from 8+ keys to just **2 keys** while maintaining full control over social media formatting and thread creation.

## Architecture

```
┌─────────────────┐
│   Blog Post     │
│   Published     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RSS Feed      │ ◄── Astro generates automatically at /rss.xml
└────────┬────────┘
         │
    ┌────┴────┬──────────────┐
    ▼         ▼              ▼
┌────────┐ ┌────────┐  ┌───────────┐
│ dev.to │ │Hashnode│  │ Buttondown│
│  RSS   │ │  RSS   │  │RSS Digest │
│ Import │ │ Import │  │  Feature  │
└────────┘ └────────┘  └───────────┘
  (auto)    (auto)       (auto)

┌─────────────────┐
│ /extract-content│ ◄── Generate platform-specific social content
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Typefully     │ ◄── Single API for 5 platforms
│ X/LI/BS/TH/MA   │     Custom threads, hooks, formatting
└─────────────────┘
  (2 API keys)
```

## Why This Approach

### Previous Architecture (8+ API Keys)
- `TYPEFULLY_API_KEY` + `TYPEFULLY_SOCIAL_SET_ID`
- `DEVTO_API_KEY`
- `HASHNODE_API_KEY` + `HASHNODE_PUBLICATION_ID`
- `MEDIUM_INTEGRATION_TOKEN`
- `NEWSLETTER_PROVIDER` + provider-specific keys

### New Architecture (2 API Keys)
- `TYPEFULLY_API_KEY`
- `TYPEFULLY_SOCIAL_SET_ID`

### What RSS Handles Automatically
| Platform | RSS Feature | Result |
|----------|-------------|--------|
| dev.to | RSS Import | Auto-creates drafts with canonical URL |
| Hashnode | RSS Import | Auto-imports posts to publication |
| Buttondown | RSS Digest | Auto-sends new posts to subscribers |

### What Typefully Handles
| Platform | Capability |
|----------|------------|
| X (Twitter) | Threads with hooks, scheduling |
| LinkedIn | Professional formatting |
| Bluesky | 300 char posts |
| Threads | 500 char posts |
| Mastodon | 500 char posts |

## Environment Variables

### Required (2 total)
```bash
# Typefully - handles all social platforms
TYPEFULLY_API_KEY=your_typefully_api_key
TYPEFULLY_SOCIAL_SET_ID=your_social_set_id
```

### Optional
```bash
# Publishing mode: staged (default), auto, dry-run
PUBLISH_MODE=staged

# Your blog's canonical URL base
CANONICAL_URL_BASE=https://blog.amenoacids.com
```

## Relevant Files

### Files to Delete
These custom publishers are replaced by RSS import:
- `scripts/publishers/devto.ts`
- `scripts/publishers/hashnode.ts`
- `scripts/publishers/medium.ts`
- `scripts/publishers/newsletter.ts`

### Files to Keep
- `scripts/publishers/base-publisher.ts` - Base class
- `scripts/publishers/typefully.ts` - Typefully integration
- `adws/adw_modules/typefully_ops.py` - Python Typefully client

### Files to Update
- `.env.sample` - Remove unnecessary API keys
- `.claude/commands/extract-content.md` - Simplify for Typefully-only output
- `ai_docs/publishing-test-plan.md` - Update for RSS + Typefully

### New Files
- `ai_docs/rss-setup-guide.md` - How to configure RSS import on each platform

## Implementation Plan

### Phase 1: Cleanup [model: sonnet]

#### Step 1.1: Delete Unnecessary Publishers
Delete files that are replaced by RSS import:
```bash
rm scripts/publishers/devto.ts
rm scripts/publishers/hashnode.ts
rm scripts/publishers/medium.ts
rm scripts/publishers/newsletter.ts
```

#### Step 1.2: Simplify Environment Configuration
Update `.env.sample` to only include:
- Typefully API keys
- Publishing mode
- Canonical URL base

Remove all dev.to, Hashnode, Medium, and newsletter provider variables.

### Phase 2: Documentation [model: sonnet]

#### Step 2.1: Create RSS Setup Guide
Create `ai_docs/rss-setup-guide.md` with:
- dev.to RSS import setup instructions
- Hashnode RSS import setup instructions
- Buttondown RSS digest setup instructions
- Verification steps for each platform

#### Step 2.2: Update Test Plan
Simplify `ai_docs/publishing-test-plan.md`:
- Remove API tests for deleted platforms
- Add RSS verification steps
- Focus on Typefully testing

#### Step 2.3: Update Extract-Content Command
Simplify `.claude/commands/extract-content.md`:
- Remove dev.to/Hashnode/Medium/Newsletter output formats
- Keep only Typefully social content generation
- Update output file structure

### Phase 3: Validation [model: sonnet]

#### Step 3.1: Verify RSS Feed
Confirm Astro RSS feed is working:
```bash
curl -s https://blog.amenoacids.com/rss.xml | head -50
```

#### Step 3.2: Test Typefully Integration
```bash
uv run python adws/adw_modules/typefully_ops.py --test
```

## Step by Step Tasks

### Group A: Cleanup [parallel: false, model: sonnet]

#### Step A.1: Delete Redundant Publisher Files
Delete these files from `/Users/ameno/dev/acidbath2/trees/508241d0/scripts/publishers/`:
- `devto.ts` - Replaced by dev.to RSS import
- `hashnode.ts` - Replaced by Hashnode RSS import
- `medium.ts` - Skip Medium or use manual import
- `newsletter.ts` - Replaced by Buttondown RSS digest

#### Step A.2: Update Environment Sample
Rewrite `/Users/ameno/dev/acidbath2/trees/508241d0/.env.sample` to only include:
- Jerry core configuration
- Typefully configuration (2 variables)
- Publishing mode configuration

Remove all individual platform API keys.

### Group B: Documentation [parallel: true, depends: A, model: sonnet]

#### Step B.1: Create RSS Setup Guide
Create `/Users/ameno/dev/acidbath2/trees/508241d0/ai_docs/rss-setup-guide.md`:
- One-time setup instructions for each RSS-based platform
- Screenshots or step descriptions
- Verification commands

#### Step B.2: Simplify Extract-Content Command
Update `/Users/ameno/dev/acidbath2/trees/508241d0/.claude/commands/extract-content.md`:
- Remove sections for dev.to, Hashnode, Medium, Newsletter
- Keep Twitter, LinkedIn, Bluesky, Threads, Mastodon guidelines
- Simplify output structure to only `typefully-content.json`

#### Step B.3: Update Test Plan
Rewrite `/Users/ameno/dev/acidbath2/trees/508241d0/ai_docs/publishing-test-plan.md`:
- Phase 1: Typefully API validation only
- Phase 2: RSS feed verification
- Phase 3: End-to-end social publishing test

### Group C: Validation [parallel: false, depends: B, model: sonnet]

#### Step C.1: Verify All Changes
- Confirm deleted files are gone
- Test Python module imports
- Verify .env.sample is correct

## Acceptance Criteria

1. **Simplified Environment**:
   - [ ] Only 2 API keys required (Typefully)
   - [ ] .env.sample has no dev.to/Hashnode/Medium/Newsletter keys
   - [ ] All deleted publisher files removed

2. **Documentation**:
   - [ ] RSS setup guide created with platform instructions
   - [ ] Test plan updated for new architecture
   - [ ] Extract-content command simplified

3. **Working Integration**:
   - [ ] Typefully Python module works
   - [ ] Typefully TypeScript publisher works
   - [ ] RSS feed accessible at blog URL

## RSS Platform Setup (One-Time)

### dev.to
1. Go to https://dev.to/settings/extensions
2. Scroll to "Publishing to DEV from RSS"
3. Add your RSS feed URL: `https://blog.amenoacids.com/rss.xml`
4. Posts will auto-import as drafts with canonical URL set

### Hashnode
1. Go to your Hashnode dashboard
2. Navigate to Import → RSS Feed
3. Add your RSS feed URL
4. Configure import settings (drafts recommended)

### Buttondown
1. Go to https://buttondown.email/settings
2. Navigate to RSS settings
3. Enable RSS digest
4. Add your RSS feed URL
5. Configure digest frequency (weekly recommended)

## Validation Commands

### Typefully API Test
```bash
# Test connection
curl -s -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  https://api.typefully.com/v2/me | jq '.name'

# Python module test
uv run python adws/adw_modules/typefully_ops.py --test
```

### RSS Feed Test
```bash
# Verify RSS feed exists and is valid
curl -s https://blog.amenoacids.com/rss.xml | xmllint --noout - && echo "✓ Valid RSS"

# Check latest post in feed
curl -s https://blog.amenoacids.com/rss.xml | grep -o '<title>[^<]*</title>' | head -5
```

## Notes

### Why Skip Medium?
- Medium's API is limited and rarely updated
- Import from URL works for occasional cross-posting
- Low ROI for maintaining custom integration

### Why Buttondown RSS Digest?
- Subscribers get automatic updates without API integration
- Can still send manual newsletters for special content
- Zero maintenance after initial setup

### Future Enhancements
- Add RSS validation to CI pipeline
- Create Typefully draft preview in CLI
- Add analytics tracking for cross-platform performance
