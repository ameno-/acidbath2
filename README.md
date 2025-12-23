# ACIDBATH

**Technical AI Engineering Blog + Agentic Workflow Framework**

ACIDBATH is a practitioner-focused technical blog for senior engineers building with AI agents, Claude Code, and LLMs. Built on Astro with the Jerry agentic workflow framework powering content production and automation.

---

## Table of Contents

- [What is ACIDBATH?](#what-is-acidbath)
- [Editorial Philosophy](#editorial-philosophy)
- [Content Strategy](#content-strategy)
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

## Project Structure

```
acidbath2/
├── src/                          # Astro blog source
│   ├── content/blog/             # Published posts (markdown)
│   ├── components/               # Astro components
│   ├── layouts/                  # Page layouts
│   ├── pages/                    # Routes
│   └── styles/                   # Global CSS (Tailwind v4)
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

### Companion Code Repository

Complete code examples from blog posts are hosted in a dedicated repository:

**Repository:** [github.com/ameno-/acidbath-code](https://github.com/ameno-/acidbath-code)

```
acidbath-code/
├── examples/
│   ├── agentic-patterns/         # AI agent and context engineering examples
│   ├── production-patterns/      # Real-world implementation patterns
│   └── workflow-tools/           # Automation and utility scripts
└── manifest.json                 # Maps blog posts to code locations
```

**Commands:**
- `/extract-code {post}.md` - Extract complete examples to acidbath-code
- `/sync-code-blocks` - Transform blog posts to use code references

**Documentation:** See `ai_docs/code-repository-integration.md` for the complete integration guide.

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

### Project Skills

| Skill | Description |
|-------|-------------|
| `/prime` | Load codebase context for new sessions |
| `/plan` | Generate implementation plan |
| `/implement` | Execute implementation spec |
| `/commit` | Generate git commit |
| `/pull_request` | Create PR with summary |
| `/review` | Review code changes |
| `/new-post` | Create AI-optimized blog post |
| `/ai-audit` | Audit post against ACIDBATH tenets |
| `/extract-content` | Generate Twitter/LinkedIn/Newsletter from post |
| `/analyze` | Run fabric patterns on content |

### Content Commands

```bash
# Create new blog post
/new-post "Context Engineering Deep Dive"

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
