# ACIDBATH Charter

The critical, code-first voice that senior technical leaders trust.

---

## Core Philosophy

**The Acid Test**: Every piece of content must pass the test of skeptical rigor. We're the counter-weight to AI hype while remaining technically credible.

### What We Believe

1. **Production reality over marketing promise** - 80-90% of AI agent projects fail to leave pilot phase. We document what actually works, including what doesn't.

2. **Code-first, always** - No hand-waving. Complete, working code that readers can copy and run today.

3. **Respect the reader's intelligence** - Our audience is senior engineers who build production systems. We skip 101-level explanations and trust them to Google unfamiliar terms.

4. **Honest about costs and failures** - Token consumption, API costs, failure modes, and production gotchas are features of our content, not things we hide.

5. **Substance over style** - Technical terminology IS our keywords. Production experience IS our competitive advantage.

### What We Don't Do

- "Game-changer," "revolutionary," "unlock your potential"
- Generic prompt engineering tips
- RAG 101 explainers
- Intro-to-anything tutorials
- Content for beginners in disguise

---

## Key Components

### Content Pillars

| Pillar | Description | Target Keywords |
|--------|-------------|-----------------|
| **Agentic AI Patterns** | Sub-agent architecture, orchestration, workflow prompts | "agentic AI patterns," "multi-agent architecture," "ReAct prompting" |
| **Claude-Specific Deep Dives** | Claude Code, SDK patterns, model optimization | "Claude Code best practices," "Claude vs GPT for code generation" |
| **Production AI Economics** | Cost optimization, context management, real numbers | "LLM cost optimization," "context window optimization" |
| **Reliability & Failure** | What breaks, how to prevent it, honest post-mortems | "AI agent observability," "AI agent failure patterns" |

### Content Mix

- **60%** Educational deep-dives (sub-agent patterns, context optimization, cost analysis)
- **20%** Opinion/POV pieces with earned contrarian takes
- **15%** News analysis and rapid commentary on releases
- **5%** Personal/process stories (building in public)

### Format Requirements

- **Length**: 2,000-2,500 words for comprehensive technical content
- **Structure**: TL;DR → Context → Technical depth → Practical code → Key takeaways
- **Code**: Complete, runnable examples with realistic variable names
- **Diagrams**: Architecture diagrams for system design content (Mermaid, ASCII art)
- **Numbers**: Include benchmarks, token counts, costs when relevant

---

## Blog Post Tenets

Every ACIDBATH post must embody these principles:

### 1. The POC Rule
Every post includes a proof-of-concept the reader can implement today. Not "consider doing X" but "here's the exact code to do X."

### 2. The Numbers Test
Quantify claims. "Reduces context consumption" becomes "95% reduction in token usage." "Faster" becomes "36x improvement."

### 3. The Production Lens
Ask: "Would this work in a real codebase?" If the answer requires asterisks, address them explicitly.

### 4. The Senior Engineer Filter
Before publishing, ask: "Would a senior engineer at a serious company find this valuable?" If it's something they already know or could easily Google, cut it.

### 5. The Honest Failure Requirement
Include what doesn't work, edge cases that break, and scenarios where the approach is wrong. This builds trust.

### 6. The "Try It Now" Call
End with a specific, actionable next step. Not "think about your workflows" but "create this file and run this command."

### Writing Voice

- Direct, technical, confident
- First person when sharing experience ("I found that...")
- Specific version numbers and tool names
- Honest limitations stated plainly
- No hedging or over-qualification

---

## Content Strategy Execution

### Distribution Priority

1. **Hacker News** - Primary reach multiplier (post 8-10 AM EST Wednesdays)
2. **LinkedIn** - CTOs and technical leadership (personal account, not brand)
3. **Reddit** - r/LocalLLaMA, r/MachineLearning, r/programming
4. **Twitter/X** - Real-time thought leadership, rapid reactions to AI news
5. **Newsletter** - Owned audience for direct distribution

### SEO Approach

- Title formula: Problem-Solution or Architecture-Focus ("Reducing LLM Costs: How We Cut API Spend 60%")
- Meta descriptions with specific numbers
- TechArticle schema with `proficiencyLevel: Expert`
- Technical terminology as natural keywords
- First-mover advantage on new patterns/terms

### Competitive Positioning

We fill the gap others don't cover:
- AI cost engineering and economics
- Failure post-mortems (not just success stories)
- Small/mid-sized company AI implementation
- AI agent observability
- Long-term AI product maintenance

---

## Published Content Registry

Track all published posts here. Update as new content goes live.

### Foundation Posts (December 2025)

| # | Title | Key Topic | Primary Pattern | Word Count |
|---|-------|-----------|-----------------|------------|
| 01 | **Workflow Prompts: The Pattern That Makes AI Engineering Predictable** | Workflow sections, failure modes, ROI calculation | Input → Workflow → Output | ~2,150 |
| 02 | **Context Engineering: From Token Optimization to Large Codebase Mastery** | Progressive disclosure + semantic search | UV scripts + Serena MCP | ~3,400 |
| 03 | **Agent Architecture: From Custom Agents to Effective Delegation** | Custom agents + sub-agent delegation | System prompts + file-based context | ~3,400 |
| 04 | **Directory Watchers: File-Based AI Automation That Scales** | Drop zones, production deployment | Python watchdog + error handling | ~3,450 |
| 05 | **AI Document Skills: Automated File Generation That Actually Ships** | Skills API, document pipelines, Excel/PowerPoint/PDF | Data → Skills → Multi-format output | ~3,200 |

### Content Consolidation Notes

Posts consolidated December 2025 to improve depth and eliminate word count padding:
- Post 01: Expanded with failure modes and ROI calculation sections
- Post 02+06: Combined context optimization with large codebase tooling
- Post 03+05: Combined sub-agent delegation with custom agent patterns
- Post 04: Expanded with production deployment and failure mode sections

### Content Themes Established

From foundation posts, we've established expertise in:
- [x] Agentic prompt architecture (workflow patterns, failure modes)
- [x] Context engineering (progressive disclosure, semantic search)
- [x] Agent architecture (custom agents, sub-agent delegation)
- [x] File system automation (directory watchers, drop zones)
- [x] Production considerations (error handling, monitoring, scaling)
- [x] Document generation (Skills API, multi-format pipelines, Excel/PowerPoint/PDF)

### Upcoming Content Priorities

High-opportunity topics (from content strategy) not yet covered:
- [ ] Multi-agent coordination and error propagation
- [ ] Real economics of production LLM systems (comprehensive cost analysis)
- [ ] AI agent reliability and failure patterns (detailed post-mortems)
- [ ] Model routing economics (when to use Haiku vs Sonnet vs Opus)

---

## Quality Checklist

Before publishing any post, verify:

**Content Quality**
- [ ] Includes complete, runnable POC code
- [ ] Numbers are specific and verifiable
- [ ] Production considerations addressed
- [ ] Failure modes documented
- [ ] "Try It Now" section with specific action

**Technical Accuracy**
- [ ] Code tested and working
- [ ] Version numbers current
- [ ] Links verified
- [ ] Diagrams accurate to described architecture

**Voice & Style**
- [ ] No banned phrases ("game-changer," "revolutionary," etc.)
- [ ] Specific over vague throughout
- [ ] Senior engineer would find valuable
- [ ] Honest about limitations

**SEO & Distribution**
- [ ] Title follows Problem-Solution or Architecture-Focus format
- [ ] Meta description includes specific numbers
- [ ] Tags appropriate for content
- [ ] Distribution plan for HN, LinkedIn, Reddit

---

## Updating This Charter

This document evolves with the blog. Update when:

1. **New post published** - Add to Content Registry with key topic and pattern
2. **New content pillar identified** - Add to Key Components section
3. **Distribution strategy changes** - Update priority/approach
4. **Quality standards evolve** - Update checklist

The charter reflects what ACIDBATH is, not what we wish it to be. Keep it grounded in published work and proven strategy.

---

*"The biggest opportunity is practical depth at the senior engineer level. Most AI content is either too basic or too theoretical. ACIDBATH bridges this gap."*
