# ACIDBATH

**Technical AI Engineering Blog + Agentic Workflow Framework**

ACIDBATH is a practitioner-focused technical blog for senior engineers building with AI agents, Claude Code, and LLMs. Built on Astro with the Jerry agentic workflow framework powering content production and automation.

---

## Table of Contents

- [What is ACIDBATH?](#what-is-acidbath)
- [Editorial Philosophy](#editorial-philosophy)
- [Content Strategy](#content-strategy)
- [Design System](#design-system)
- [Project Structure](#project-structure)
- [Jerry Framework](#jerry-framework)
- [Available Workflows](#available-workflows)
- [Skills & Commands](#skills--commands)
- [Getting Started](#getting-started)
- [Development](#development)
- [Deployment](#deployment)

---

## What is ACIDBATH?

ACIDBATH targets a gap in AI content: **practitioner-level technical content** for engineers who actually build with AI, not just read about it.

**What we cover:**
- Claude Code workflows and sub-agent patterns
- Context engineering and token optimization
- Agentic prompt design and workflow prompts
- Production AI agent architecture
- MCP servers and tool integration
- Real cost analysis and failure modes

**What we don't do:**
- Hype-speak ("revolutionary", "game-changer", "the future")
- Unsubstantiated claims ("90% of developers...")
- Fear-mongering ("your job is obsolete")
- Tutorial content without working code

---

## Editorial Philosophy

### The ACIDBATH Tenets

Every post must pass these six checks:

| Tenet | Requirement |
|-------|-------------|
| **POC Rule** | Include working, copy-paste code that readers can run today |
| **Numbers Test** | Specific, verifiable metrics (not "significantly faster") |
| **Production Lens** | Document setup complexity, maintenance burden, edge cases |
| **Senior Engineer Filter** | Would a 10+ year engineer find this valuable? |
| **Honest Failure Requirement** | Explicit "What Doesn't Work" section |
| **Try It Now** | Clear action item at the end |

### Voice Guidelines

**Do:**
- Be direct and opinionated
- Use specific version numbers and dollar amounts
- Reference source code
- Say "Here's what we learned" and "This doesn't work when..."

**Don't:**
- Hedge with "might", "could potentially"
- Use superlatives without evidence
- Include emotional hooks or FOMO language
- Make claims without working examples

### Post Structure

Target: **2,000-2,500 words** per post

```
├── Hook/Problem Statement (100 words)
├── Key Insight/Thesis (200 words)
├── Technical Deep-Dive with Code (1,200-1,500 words)
├── Practical Example/Case Study (400 words)
└── Takeaways + What's Next (200 words)
```

---

## Content Strategy

### Target Keywords

| Tier | Keywords | Competition |
|------|----------|-------------|
| **High Opportunity** | context engineering, context window optimization, CLAUDE.md best practices | Very Low |
| **Problem-Solution** | AI agent failure patterns, token efficiency strategies, LLM cost optimization | Low-Medium |
| **Claude Code Specific** | Claude Code workflow, Claude Code MCP setup, Claude Code sub-agents | Very Low |

### Content Pipeline

```
Blog Post (2,000-2,500 words)
         │
         ├── Twitter Thread (5-8 tweets)
         ├── LinkedIn Post (800-1,200 words)
         └── Newsletter Edition (1,000-1,500 words)
```

Use `/extract-content` skill to generate derivatives from any published post.

---

## Design System

ACIDBATH uses a comprehensive design system featuring acid-green theming, fluid typography, and four key UI components that transform dense technical content into scannable, layered information.

### Core Components

| Component | Purpose | Variants/Features |
|-----------|---------|-------------------|
| **Callout** | Semantic content highlighting | 7 types: quote, info, warning, danger, success, insight, data |
| **Collapse** | Collapsible sections | 3 variants: default, compact, prominent |
| **CodeBlock** | Enhanced code display | Auto-collapse at 15+ lines, line numbers, copy button, syntax highlighting |
| **TableOfContents** | Navigation sidebar | Hierarchical H2/H3 grouping, scroll progress, active tracking |

### Typography

Fluid typography using `clamp()` scales responsively from mobile (320px) to desktop (1440px):

```css
--text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
--text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
--text-2xl: clamp(1.5rem, 1.3rem + 1vw, 2.25rem);
```

### Colors

**Acid-Green Accent**: `#39ff14` (12.3:1 contrast ratio, WCAG AAA)

**Semantic Colors**: Warning (orange), Info (blue), Success (green), Danger (red), Insight (acid-green), Data (purple)

### Component Usage

```astro
---
import Callout from '../../components/Callout.astro';
import Collapse from '../../components/Collapse.astro';
---

<Callout type="insight" title="Key Takeaway">
This design system reduced scrolling by 40% on 10,000-word posts.
</Callout>

<Collapse title="Advanced Details" variant="prominent">
Content here auto-collapses to reduce initial cognitive load.
</Collapse>
```

### Props Reference

**Callout Props**:
- `type`: `'quote' | 'info' | 'warning' | 'danger' | 'success' | 'insight' | 'data'` (required)
- `title`: string (optional, uses default if omitted)
- `author`: string (optional, quote variant only)

**Collapse Props**:
- `title`: string (required)
- `preview`: string (optional, shown when collapsed)
- `variant`: `'default' | 'compact' | 'prominent'` (default: 'default')
- `defaultOpen`: boolean (default: false)

**CodeBlock Props**:
- `language`: string (for syntax highlighting)
- `filename`: string (displayed in header)
- `showLineNumbers`: boolean (default: true)
- `maxPreviewLines`: number (default: 8)
- `defaultExpanded`: boolean (default: false)

**TableOfContents Props**:
- `headings`: Array<{depth, slug, text}> (required)
- `maxTopLevel`: number (default: 8, triggers "show more")

### Documentation

- **Full Reference**: `ai_docs/design-system.md`
- **Component Showcase**: `src/content/blog/design-system-showcase.md`
- **Implementation Details**: Each component file (`src/components/*.astro`)

---

## Project Structure

```
acidbath2/
├── src/                          # Astro blog source
│   ├── content/blog/             # Published posts (markdown)
│   ├── components/               # Astro components
│   │   ├── Callout.astro         # Semantic callout (7 variants)
│   │   ├── Collapse.astro        # Collapsible sections
│   │   ├── CodeBlock.astro       # Enhanced code display
│   │   └── TableOfContents.astro # Hierarchical navigation
│   ├── layouts/                  # Page layouts
│   ├── pages/                    # Routes
│   └── styles/                   # Global CSS (Tailwind v4 + Design tokens)
│
├── blog/                         # Content pipeline
│   ├── posts/                    # Source posts with metadata.json
│   │   └── {post-name}/
│   │       ├── post.md
│   │       ├── metadata.json
│   │       └── diagrams/         # Mermaid diagrams
│   ├── _meta/                    # Keywords, series config
│   └── archive/                  # Draft/archived content
│
├── adws/                         # AI Developer Workflows (Jerry)
│   ├── adw_modules/              # Core modules
│   │   ├── agent.py              # Claude Code execution
│   │   ├── workflow_ops.py       # Workflow orchestration
│   │   └── worktree_ops.py       # Git worktree management
│   └── adw_*.py                  # Individual workflows
│
├── .claude/
│   ├── commands/                 # Slash command templates
│   └── skills/                   # Skill definitions
│
├── ai_docs/                      # Context documents
│   ├── astro.md                  # Astro framework reference
│   ├── tailwind-v4-astro.md      # Tailwind v4 patterns
│   ├── content_strategy.md       # SEO and distribution
│   ├── design-system.md          # Design system reference
│   └── blog_audit.md             # Post quality audit
│
├── specs/                        # Implementation specifications
├── technical-research/           # YouTube analysis system
│   └── output/youtube-analysis/  # Analyzed video outputs
│
└── public/
    ├── assets/                   # Images, banners
    ├── llms.txt                  # LLM-readable site summary
    └── llms-full.txt             # Full content for LLMs
```

---

## Jerry Framework

Jerry is the agentic workflow layer powering ACIDBATH's automation. It transforms high-level intentions into executed changes through AI agent orchestration.

### Core Concepts

- **ADWs (AI Developer Workflows)**: Python scripts combining deterministic code with Claude Code agents
- **Slash Commands**: Templated prompts in `.claude/commands/*.md`
- **Worktree Isolation**: Each agent operates in a dedicated Git worktree
- **Observability**: Every execution produces structured outputs in `agents/`

### Architecture

```
┌─────────────────────────────────────┐
│     Agentic Layer (Jerry)           │
│  ┌─────────────────────────────┐    │
│  │  ADWs (Workflows)           │    │  ← Orchestration
│  └──────────┬──────────────────┘    │
│             │                        │
│  ┌──────────▼──────────────────┐    │
│  │  Slash Commands (Templates) │    │  ← Instructions
│  └──────────┬──────────────────┘    │
│             │                        │
│  ┌──────────▼──────────────────┐    │
│  │  Agents (Execution)         │    │  ← Execution
│  └──────────┬──────────────────┘    │
└─────────────┼───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│     Application Layer               │
│  ┌─────────────────────────────┐    │
│  │  ACIDBATH Blog (Astro)      │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

---

## Available Workflows

### Utility Workflows

| ADW | Description |
|-----|-------------|
| `adw_prompt` | Execute adhoc Claude Code prompts |
| `adw_sdk_prompt` | SDK-based prompts with type safety |
| `adw_slash_command` | Execute slash command templates |

### Planning & Building

| ADW | Description |
|-----|-------------|
| `adw_plan_iso` | Generate implementation specs in isolated worktrees |
| `adw_build_iso` | Implement plans and commit changes |
| `adw_plan_build_iso` | Chained planning + building |
| `adw_ship_iso` | Merge feature branch to main |

### Content Analysis

| ADW | Description |
|-----|-------------|
| `adw_analyze_iso` | Pattern-based analysis (YouTube, GitHub, PDFs) |
| `adw_brainstorm` | Versioned content analysis with diffs |

### Usage Examples

```bash
# Direct prompt
./adws/adw_prompt.py "Add dark mode toggle to header"

# Plan + Build from issue
./adws/adw_plan_build_iso.py "Add RSS feed to blog"

# Analyze YouTube video for blog content
./adws/adw_analyze_iso.py "https://youtube.com/watch?v=..." --preset acidbath --brainstorm
```

---

## Skills & Commands

### Copywriting Skills Framework

ACIDBATH includes three specialized copywriting skills using the **suggest_edits pattern** - they suggest changes with clear rationale, never auto-apply:

| Skill | Focus | When to Use | Command |
|-------|-------|-------------|---------|
| **Mad Men Copywriter** | Conversion | Sales pages, CTAs, ads, product launches | `/mad-men-edit {file}` |
| **Master Copywriter** | Persuasion | Thought leadership, brand building, high-trust sales | `/master-copy-edit {file}` |
| **Ameno Voice** | Simplification | Technical blog posts, concept explanations | `/ameno-finalize {file}` |

**Pattern**: All skills use suggest_edits framework - they **suggest** edits with rationale, you apply selectively. Original files never modified.

**Documentation**:
- [ai_docs/copywriting-skills.md](ai_docs/copywriting-skills.md) - Full comparison and decision tree
- [ai_docs/suggest-edits-framework.md](ai_docs/suggest-edits-framework.md) - Core framework docs
- [samples/copywriting-demos/](samples/copywriting-demos/) - Sample outputs for each skill

### Project Skills

| Skill | Description |
|-------|-------------|
| `/prime` | Load codebase context for new sessions |
| `/plan` | Generate implementation plan |
| `/implement` | Execute implementation spec |
| `/commit` | Generate git commit |
| `/pull_request` | Create PR with summary |
| `/review` | Review code changes |
| `/new-post` | Create AI-optimized blog post (ACIDBATH direct voice) |
| `/ai-audit` | Audit post against ACIDBATH tenets |
| `/extract-content` | Generate Twitter/LinkedIn/Newsletter from post |
| `/analyze` | Run fabric patterns on content |

### Content Commands

```bash
# Create new blog post (direct voice)
/new-post "Context Engineering Deep Dive"

# [OPTIONAL] Apply copywriting skill for suggestions
/mad-men-edit content/landing-page.md        # For conversion focus
/master-copy-edit content/thought-leadership.md  # For persuasion/authority
/ameno-finalize src/content/blog/technical-post.md  # For simplification

# Audit existing post
/ai-audit src/content/blog/workflow-prompts.md

# Extract derivatives
/extract-content src/content/blog/workflow-prompts.md
```

### Development Commands

```bash
# Generate implementation plan
/plan "Add search functionality to blog"

# Implement from spec
/implement specs/feature-search.md

# Commit with conventional format
/commit

# Open PR
/pull_request
```

---

## Getting Started

### Prerequisites

- Node.js 18+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Claude Code CLI](https://docs.anthropic.com/claude/docs/claude-code)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/ameno-/acidbath2.git
cd acidbath2

# Install dependencies
npm install

# Start development server
npm run dev
```

### Writing a New Post

1. Create post structure:
```bash
mkdir -p blog/posts/07-your-post-title/{diagrams,callouts}
```

2. Create `post.md` with frontmatter and content

3. Create `metadata.json` with SEO data

4. Build and preview:
```bash
npm run build
npm run preview
```

5. Or use the skill:
```bash
/new-post "Your Post Title"
```

---

## Development

### Local Development

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run Playwright tests
npm run test
```

### Content Pipeline

```bash
# Generate llms.txt from content
node scripts/generate-llms-txt.js

# Analyze YouTube video for research
./adws/adw_analyze_iso.py "https://youtube.com/watch?v=..." --preset acidbath
```

### Jerry Workflows

```bash
# Plan a feature
./adws/adw_plan_iso.py "Add tag filtering to blog"

# Build from spec
./adws/adw_build_iso.py specs/feature-tag-filtering.md

# Ship to main
./adws/adw_ship_iso.py feat/tag-filtering
```

---

## Deployment

ACIDBATH deploys to **Cloudflare Pages**.

### Manual Deploy

```bash
npm run build
npx wrangler pages deploy dist
```

### Automatic Deploy

Push to `main` triggers Cloudflare Pages build.

### Environment Variables

Set in Cloudflare Pages dashboard:
- `SITE_URL` - Production URL
- `ANTHROPIC_API_KEY` - For content generation (if using)

---

## Roadmap

### Near-term

- [ ] Search functionality (Pagefind or custom)
- [ ] RSS feed with full content
- [ ] Newsletter signup integration
- [ ] Reading time estimates

### Content Pipeline

- [ ] Automated Twitter thread scheduling
- [ ] LinkedIn post templates
- [ ] HN submission tracking

### Jerry Enhancements

- [ ] `adw_review_all_iso` for batch PR review
- [ ] Content freshness checking
- [ ] Automated link validation

---

## License

MIT

---

**ACIDBATH**: Technical content for engineers who build, not just read.
