# Feature: Multi-Channel Publish - Maximum Reach Edition

## Metadata
adw_id: `508241d0`
prompt: `Maximum Reach Edition - Automated publishing from blog posts to social media, newsletters, and developer communities. Plan and implement the work in parallel. Create one PR for all the changes. Add the ability to publish content to multiple channels after each new post is published.`

## Feature Description
Implement an automated multi-channel publishing system that takes published blog posts from ACIDBATH and distributes them across multiple platforms: Twitter/X, LinkedIn, dev.to, Hashnode, Medium, and email newsletters. The system will extract platform-specific content from the source blog post, format it appropriately for each channel, and either auto-publish or stage content for manual review before publishing.

This feature transforms ACIDBATH from a single-channel blog into a multi-platform content distribution engine, maximizing reach and SEO impact for each piece of technical content.

## User Story
As a content creator publishing technical AI engineering content
I want to automatically distribute my blog posts to multiple platforms
So that I can maximize reach and engagement without manual reformatting and cross-posting

## Problem Statement
Currently, ACIDBATH has:
- Blog posts published only on the main site (Cloudflare Pages)
- Manual `/extract-content` command that generates Twitter/LinkedIn/Newsletter derivatives but doesn't publish them
- No automated distribution to developer communities (dev.to, Hashnode, Medium)
- No integration with social media APIs for auto-posting
- No newsletter distribution system

This results in:
- Limited reach for high-quality technical content
- Time-consuming manual cross-posting
- Inconsistent presence across platforms
- Missed SEO opportunities from syndication

## Solution Statement
Build a comprehensive multi-channel publishing system with:

1. **Content Extraction & Formatting**: Leverage and enhance the existing `/extract-content` command to generate platform-specific versions of blog posts
2. **Publishing Integrations**: Create API integrations for Twitter, LinkedIn, dev.to, Hashnode, Medium
3. **Newsletter System**: Integrate with email providers (Substack, Buttondown, or Mailchimp)
4. **Publishing Workflow**: Create both automated and staged publishing workflows
5. **Claude Code Skill**: Implement a `/publish-all` skill that orchestrates the entire process
6. **TypeScript Orchestrator**: Build a `publish-all.ts` script for reliable execution
7. **Python Community Publisher**: Create `publish-dev-communities.py` for dev platform publishing

## Relevant Files

### Existing Files to Modify
- **`/Users/ameno/dev/acidbath2/trees/508241d0/.claude/commands/extract-content.md`** - Existing content extraction command; will be enhanced to output JSON metadata for publishing
- **`/Users/ameno/dev/acidbath2/trees/508241d0/README.md`** - Update with new publishing workflow documentation
- **`/Users/ameno/dev/acidbath2/trees/508241d0/package.json`** - Add new dependencies for API integrations (Twitter API, LinkedIn API, dev.to API)
- **`/Users/ameno/dev/acidbath2/trees/508241d0/.env.sample`** - Add API keys and configuration for all publishing platforms

### New Files

#### Publishing Scripts
- **`scripts/publish-all.ts`** - Main orchestrator for multi-channel publishing
- **`scripts/publish-dev-communities.py`** - Python script for publishing to dev.to, Hashnode, Medium
- **`scripts/publishers/twitter.ts`** - Twitter/X API integration
- **`scripts/publishers/linkedin.ts`** - LinkedIn API integration
- **`scripts/publishers/devto.ts`** - dev.to API integration
- **`scripts/publishers/hashnode.ts`** - Hashnode API integration
- **`scripts/publishers/medium.ts`** - Medium API integration
- **`scripts/publishers/newsletter.ts`** - Newsletter provider integration

#### Skills & Commands
- **`.claude/skills/publish-all/SKILL.md`** - Claude Code skill for orchestrating multi-channel publishing
- **`.claude/skills/publish-all/README.md`** - Documentation for the publish skill

#### Configuration & Types
- **`scripts/config/publish-config.ts`** - Publishing configuration and platform settings
- **`scripts/types/publisher.ts`** - TypeScript types for publisher interfaces
- **`scripts/utils/content-formatter.ts`** - Utilities for formatting content per platform

#### Output Directories
- **`content/derivatives/{slug}/publish-log.json`** - Tracking published posts and their URLs across platforms
- **`content/derivatives/{slug}/staged/`** - Staged content awaiting manual publish approval

## Implementation Plan

### Phase 1: Foundation
Set up the core infrastructure for multi-channel publishing:
- Create TypeScript types and interfaces for publisher contracts
- Set up configuration management for API keys and platform settings
- Enhance content extraction to output structured JSON with metadata
- Create base publisher class with common functionality

### Phase 2: Core Implementation
Build individual platform publishers and orchestration:
- Implement Twitter/X publisher with thread support
- Implement LinkedIn publisher with article formatting
- Implement dev.to publisher with frontmatter support
- Implement Hashnode publisher with GraphQL API
- Implement Medium publisher with story formatting
- Build main orchestrator script (`publish-all.ts`)
- Build Python community publisher (`publish-dev-communities.py`)

### Phase 3: Integration
Integrate with existing ACIDBATH workflows:
- Create `/publish-all` Claude Code skill
- Update `/extract-content` to generate publish-ready metadata
- Add npm scripts for publishing workflows
- Create GitHub Actions workflow for automated publishing on merge to main
- Update documentation with publishing guide

## Step by Step Tasks

### Group A: Foundation [parallel: false, model: sonnet]
Sequential setup work establishing core infrastructure.

#### Step A.1: Create TypeScript Publishing Infrastructure
- Create `scripts/types/publisher.ts` with interfaces: `Publisher`, `PublishResult`, `PublishConfig`, `PlatformContent`
- Create `scripts/config/publish-config.ts` with platform configurations (API endpoints, auth methods, rate limits)
- Create `scripts/utils/content-formatter.ts` with helper functions for markdown transformation per platform
- Add TypeScript dependencies to `package.json`: `@types/node`, ensure TypeScript is configured

#### Step A.2: Set Up Environment Configuration
- Update `.env.sample` with all required API keys and configuration:
  - `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET`
  - `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, `LINKEDIN_ACCESS_TOKEN`
  - `DEVTO_API_KEY`
  - `HASHNODE_API_KEY`
  - `MEDIUM_INTEGRATION_TOKEN`
  - `NEWSLETTER_PROVIDER` (substack/buttondown/mailchimp)
  - `NEWSLETTER_API_KEY`
  - `PUBLISH_MODE` (auto/staged)
- Create `.env.local` template for local development

#### Step A.3: Enhance Content Extraction Command
- Modify `.claude/commands/extract-content.md` to:
  - Generate `metadata.json` with publication data (title, description, tags, canonical URL)
  - Output structured JSON for each platform with character counts and validation
  - Include SEO metadata (keywords, meta description)
- Create validation logic for extracted content (character limits, required fields)

#### Step A.4: Create Base Publisher Class
- Create `scripts/publishers/base-publisher.ts` with:
  - Abstract `Publisher` class implementing common functionality
  - Rate limiting logic (respect platform limits)
  - Error handling and retry logic
  - Logging and publish tracking
  - Dry-run mode for testing

### Group B: Platform Publishers [parallel: true, depends: A, model: auto]
Independent publisher implementations that can be built concurrently.

#### Step B.1: Implement Twitter/X Publisher
- Create `scripts/publishers/twitter.ts`:
  - Thread creation from extracted content
  - Image upload support for code snippets
  - Character limit validation (280 chars/tweet)
  - Rate limiting (300 tweets per 3 hours)
  - Reply chain construction
- Test with staging account

#### Step B.2: Implement LinkedIn Publisher
- Create `scripts/publishers/linkedin.ts`:
  - Article/post publishing
  - Support for both personal and organization pages
  - Rich media support (images, code blocks)
  - Hashtag management
  - Rate limiting compliance
- Test with personal account

#### Step B.3: Implement dev.to Publisher
- Create `scripts/publishers/devto.ts`:
  - Article creation with frontmatter (tags, canonical_url, published status)
  - Markdown formatting (dev.to flavor)
  - Cover image upload
  - Series support for multi-part posts
  - Canonical URL setting to blog post
- Test with dev.to API sandbox

#### Step B.4: Implement Hashnode Publisher
- Create `scripts/publishers/hashnode.ts`:
  - GraphQL API integration
  - Article publishing to publication
  - Tag management
  - Cover image handling
  - Canonical URL configuration
  - SEO metadata support
- Test with personal Hashnode blog

#### Step B.5: Implement Medium Publisher
- Create `scripts/publishers/medium.ts`:
  - Story creation API
  - Markdown to Medium format conversion
  - Tag support (max 5 tags)
  - Canonical URL reference
  - License selection
  - Publication status (draft/public)
- Test with Medium integration token

#### Step B.6: Implement Newsletter Publisher
- Create `scripts/publishers/newsletter.ts`:
  - Support multiple providers (Substack, Buttondown, Mailchimp)
  - Email template formatting
  - Subscriber list management
  - Scheduled sending
  - Campaign tracking
- Test with newsletter provider API

### Group C: Orchestration [parallel: false, depends: B, model: sonnet]
Sequential orchestration work that requires all publishers to be complete.

#### Step C.1: Build TypeScript Orchestrator
- Create `scripts/publish-all.ts`:
  - Load blog post and extracted derivatives
  - Validate all content meets platform requirements
  - Execute publishers in optimal order (Twitter → LinkedIn → Communities → Newsletter)
  - Handle partial failures gracefully
  - Generate publish report with all URLs
  - Support dry-run mode
  - Support staged vs auto mode
  - CLI interface with arguments: `--post <slug>`, `--platforms <csv>`, `--dry-run`, `--staged`

#### Step C.2: Build Python Community Publisher
- Create `scripts/publish-dev-communities.py`:
  - Unified interface for dev.to, Hashnode, Medium
  - Concurrent publishing to all platforms
  - Response handling and URL collection
  - Error reporting
  - Logging to publish-log.json
  - CLI interface compatible with TypeScript orchestrator

#### Step C.3: Create Publishing Workflows
- Add npm scripts to `package.json`:
  - `"publish:all": "uv run tsx scripts/publish-all.ts"`
  - `"publish:twitter": "uv run tsx scripts/publish-all.ts --platforms twitter"`
  - `"publish:linkedin": "uv run tsx scripts/publish-all.ts --platforms linkedin"`
  - `"publish:communities": "uv run python scripts/publish-dev-communities.py"`
  - `"publish:dry-run": "uv run tsx scripts/publish-all.ts --dry-run"`
- Test each npm script independently

### Group D: Claude Code Integration [parallel: false, depends: C, model: sonnet]
Integration with Claude Code workflow and skills.

#### Step D.1: Create Publish-All Skill
- Create `.claude/skills/publish-all/SKILL.md`:
  - Skill definition with command interface
  - Parameters: post slug, platform selection, mode (auto/staged/dry-run)
  - Integration with existing `/extract-content` command
  - Workflow: extract → validate → publish → report
  - Error handling and rollback instructions
- Create `.claude/skills/publish-all/README.md` with usage examples

#### Step D.2: Update Extract-Content Command
- Modify `.claude/commands/extract-content.md`:
  - Add option to auto-trigger publishing after extraction
  - Generate `publish-ready.json` marker file
  - Validate extracted content meets platform requirements
  - Output summary of what will be published

#### Step D.3: Create GitHub Actions Workflow
- Create `.github/workflows/publish-on-merge.yml`:
  - Trigger on merge to main
  - Detect new blog posts in `src/content/blog/`
  - Run `/extract-content` on new posts
  - Run `/publish-all --staged` for manual approval
  - Post comment on PR with staged content URLs
- Test workflow with feature branch

### Group E: Documentation & Validation [parallel: true, depends: D, model: auto]
Independent documentation and testing tasks.

#### Step E.1: Update Project Documentation
- Update `README.md`:
  - Add "Multi-Channel Publishing" section
  - Document `/publish-all` skill usage
  - Document manual publishing workflow
  - Document API key setup instructions
  - Add publishing workflow diagram
- Update roadmap to mark publishing feature as complete

#### Step E.2: Create Publishing Guide
- Create `ai_docs/publishing-guide.md`:
  - Step-by-step guide for publishing a new post
  - API key acquisition instructions for each platform
  - Troubleshooting common issues
  - Rate limiting and best practices
  - Platform-specific formatting guidelines

#### Step E.3: Create Integration Tests
- Create `tests/publishing.spec.ts`:
  - Test content extraction with mock blog post
  - Test each publisher in dry-run mode
  - Test orchestrator with staged mode
  - Test error handling (invalid API keys, rate limits)
  - Test partial failure scenarios
- Run tests: `npm run test`

## Testing Strategy

### Unit Tests
- **Content Formatter**: Test markdown transformations for each platform (Twitter thread splitting, LinkedIn formatting, Medium conversion)
- **Publisher Classes**: Test API request construction, rate limiting, error handling
- **Orchestrator**: Test execution order, partial failure handling, dry-run mode
- **Config Validation**: Test API key validation, platform configuration

### Integration Tests
- **End-to-End Dry Run**: Run full publishing workflow in dry-run mode with sample blog post
- **Single Platform Publish**: Test publishing to each platform individually with staging accounts
- **Multi-Platform Publish**: Test orchestrated publishing to all platforms
- **Error Recovery**: Test behavior with invalid API keys, rate limits, network failures

### Edge Cases
- **Very Long Posts**: Test with 5,000+ word blog post to ensure platform character limits are respected
- **Code-Heavy Posts**: Test with posts containing extensive code blocks (Medium, dev.to formatting)
- **Special Characters**: Test with posts containing emojis, unicode, markdown edge cases
- **Rate Limiting**: Test behavior when approaching/exceeding platform rate limits
- **Partial Failures**: Test when some platforms succeed and others fail
- **Network Failures**: Test retry logic and timeout handling
- **Missing API Keys**: Test graceful degradation when some platforms are not configured
- **Already Published**: Test behavior when attempting to republish to same platform

## Acceptance Criteria

1. **Content Extraction**:
   - [ ] `/extract-content` command generates platform-specific content for all 6 channels
   - [ ] Generated content respects character limits for each platform
   - [ ] Metadata includes canonical URLs, tags, descriptions

2. **Publishing Functionality**:
   - [ ] Can publish to Twitter with proper thread formatting
   - [ ] Can publish to LinkedIn with rich formatting
   - [ ] Can publish to dev.to with canonical URL
   - [ ] Can publish to Hashnode with SEO metadata
   - [ ] Can publish to Medium with canonical reference
   - [ ] Can send newsletter to configured provider

3. **Orchestration**:
   - [ ] `publish-all.ts` successfully publishes to all configured platforms
   - [ ] Dry-run mode works without making API calls
   - [ ] Staged mode creates content for manual review
   - [ ] Auto mode publishes immediately
   - [ ] Generates publish report with all URLs

4. **Error Handling**:
   - [ ] Gracefully handles missing API keys
   - [ ] Respects rate limits for all platforms
   - [ ] Continues publishing to other platforms if one fails
   - [ ] Logs all errors with actionable messages

5. **Claude Code Integration**:
   - [ ] `/publish-all` skill executes successfully
   - [ ] Can specify individual platforms or "all"
   - [ ] Can choose auto/staged/dry-run mode
   - [ ] Reports success/failure with URLs

6. **Documentation**:
   - [ ] README includes publishing workflow
   - [ ] API key setup is documented
   - [ ] Troubleshooting guide exists
   - [ ] Usage examples are clear

## Validation Commands

Execute these commands to validate the feature is complete:

### Compilation & Type Safety
```bash
uv run tsc --noEmit scripts/publish-all.ts
uv run python -m py_compile scripts/publish-dev-communities.py
```

### Unit Tests
```bash
npm run test:publishing
```

### Integration Tests (Dry Run)
```bash
# Test extraction
/extract-content src/content/blog/workflow-prompts.md

# Test dry-run publishing
npm run publish:dry-run -- --post workflow-prompts

# Test individual platforms
npm run publish:twitter -- --post workflow-prompts --dry-run
npm run publish:linkedin -- --post workflow-prompts --dry-run
```

### Staged Publishing Test
```bash
# Create staged content
npm run publish:all -- --post workflow-prompts --staged

# Verify staged files exist
ls -la content/derivatives/workflow-prompts/staged/
```

### Full Integration Test (Staging Accounts)
```bash
# Set up staging API keys in .env.local
# Run full publish to staging accounts
npm run publish:all -- --post workflow-prompts --platforms twitter,linkedin
```

### Skill Validation
```bash
# Test Claude Code skill
/publish-all workflow-prompts --mode dry-run
/publish-all workflow-prompts --platforms twitter,linkedin --mode staged
```

### GitHub Actions Validation
```bash
# Trigger workflow manually
gh workflow run publish-on-merge.yml

# Check workflow status
gh run list --workflow=publish-on-merge.yml
```

## Notes

### API Requirements
- **Twitter/X**: Requires Elevated access for Twitter API v2 (not Free tier)
- **LinkedIn**: Requires LinkedIn Marketing Developer Platform access
- **dev.to**: Free API key from https://dev.to/settings/extensions
- **Hashnode**: Free API key from Hashnode dashboard
- **Medium**: Integration token from https://medium.com/me/settings/security
- **Newsletter**: Depends on provider (Substack, Buttondown, Mailchimp)

### Dependencies to Add
Use `uv add` for Python dependencies:
```bash
uv add tweepy  # Twitter API v2
uv add requests  # HTTP client for APIs
uv add python-dotenv  # Environment management
```

Use npm for TypeScript dependencies:
```bash
npm install twitter-api-v2 linkedin-api-client --save
npm install tsx @types/node --save-dev
```

### Future Enhancements (Out of Scope for v1)
- Analytics dashboard showing engagement across platforms
- Scheduling system for optimal posting times
- A/B testing different hooks/titles per platform
- Automatic image generation for social media cards
- YouTube video publishing integration
- Reddit/HackerNews automated submission
- RSS feed syndication to aggregators

### Platform Rate Limits Reference
- **Twitter**: 300 tweets per 3 hours, 50 requests per 15 minutes
- **LinkedIn**: 100 API calls per day per user
- **dev.to**: 30 requests per 30 seconds
- **Hashnode**: No documented limits (GraphQL)
- **Medium**: No documented limits, recommended <1 post/hour
- **Newsletter**: Provider-specific (e.g., Substack: no API rate limits documented)

### Canonical URL Strategy
All syndicated content should include canonical URL pointing back to ACIDBATH blog to:
- Preserve SEO authority
- Avoid duplicate content penalties
- Drive traffic back to owned property

### Publishing Order Rationale
1. **Twitter** (first): Real-time platform, drives immediate engagement
2. **LinkedIn** (second): Professional network, benefits from Twitter momentum
3. **Communities** (parallel): dev.to, Hashnode, Medium can run concurrently
4. **Newsletter** (last): Sends after all other channels are live with URLs

### Error Handling Philosophy
- Fail gracefully: If one platform fails, continue with others
- Log everything: Maintain detailed logs for debugging
- Retry intelligently: Retry transient failures, not auth failures
- Alert on critical issues: Failed publish should notify via configured channel
