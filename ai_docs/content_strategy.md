# ACIDBATH: SEO Keywords & Content Production Pipeline

## Part 1: Underutilized Keywords for SEO Dominance

The AI blogging space is crowded with generic terms, but there are significant gaps in **practitioner-level technical content**. Your positioning—Claude Code expertise, agentic workflows, sub-agent architecture—puts you at the intersection of emerging terminology with low competition.

---

### Tier 1: High-Opportunity Emerging Keywords

These are terms with growing search momentum but limited quality content. First-mover advantage is significant.

| Keyword/Phrase | Competition | Search Trend | Why It's Underutilized |
|----------------|-------------|--------------|------------------------|
| **context engineering** | Very Low | 📈 Exploding | Karpathy coined it recently; LangChain just published on it; academic papers emerging (ACE framework). Almost no practitioner content exists. |
| **context window optimization** | Low | 📈 Growing | Everyone talks about context limits; almost no one explains how to actually optimize. Your existing post is perfectly positioned. |
| **context collapse** | Very Low | 📈 New | Technical term from recent ACE research paper. Zero blog coverage. |
| **CLAUDE.md best practices** | Very Low | 📈 Growing | Claude Code specific; no comprehensive guides exist outside Anthropic's own docs. |
| **agentic prompt patterns** | Low | 📈 Growing | Andrew Ng's "agentic workflows" created demand; practical implementation guides are scarce. |
| **sub-agent orchestration** | Very Low | Steady | Your existing content is among the only practitioner coverage. Own this niche. |
| **MCP server tutorial** | Low-Medium | 📈 Exploding | MCP adopted by OpenAI, Google, Microsoft in 2025. Demand is outpacing content. |
| **Claude Code commands** | Low | 📈 Growing | Specific how-to content for Claude Code power users. |

---

### Tier 2: Technical Problem-Solution Keywords

These target senior engineers actively searching for solutions. High intent, moderate competition.

| Keyword/Phrase | Competition | Content Angle |
|----------------|-------------|---------------|
| **LLM cost optimization production** | Medium | Real cost breakdowns, model routing, semantic caching ROI |
| **AI agent failure patterns** | Low | Post-mortems, common mistakes, reliability engineering |
| **token efficiency strategies** | Low | Practical techniques beyond "use shorter prompts" |
| **agentic workflow implementation** | Medium | Code-first guides with working examples |
| **Claude vs GPT for code generation** | Medium | Honest comparison from practitioner POV |
| **multi-agent architecture patterns** | Low-Medium | Supervisor vs peer, error propagation, coordination |
| **LLM observability production** | Medium | Tracing, debugging, monitoring agent systems |
| **prompt injection defense** | Medium | Security-focused content for production systems |
| **RAG vs long context tradeoffs** | Medium | Cost analysis, when to use which approach |
| **AI agent testing strategies** | Low | Non-deterministic system testing, eval frameworks |

---

### Tier 3: Claude Code Specific Keywords

You have unique expertise here. These are low competition with growing search volume.

| Keyword/Phrase | Competition | Content Idea |
|----------------|-------------|--------------|
| **Claude Code workflow** | Low | Your existing dual-agent system (ameno + qai) |
| **Claude Code MCP setup** | Very Low | Configuration guides, troubleshooting |
| **Claude Code sub-agents** | Very Low | Practical patterns (your existing expertise) |
| **Claude Code hooks** | Very Low | Automation and CI/CD integration |
| **Claude Code GitHub Actions** | Very Low | Automated PR workflows |
| **Claude Code plan mode** | Low | Best practices for complex tasks |
| **Claude Code dangerously-skip-permissions** | Very Low | When and how to use safely |
| **CLAUDE.md examples** | Very Low | Template library, real configurations |
| **Claude Code context management** | Very Low | Progressive disclosure, file-based context |

---

### Tier 4: Long-Tail Problem Queries

These are specific questions senior engineers ask. Lower volume but very high intent.

```
"how to reduce claude api costs"
"claude code keeps asking for permission"
"mcp server not connecting claude desktop"
"agent keeps running out of context"
"claude code vs cursor agent mode"
"sub-agent not returning results"
"how to test ai agents"
"llm cost per token comparison 2025"
"when to use rag vs long context"
"claude code with puppeteer screenshots"
"agent workflow diagram patterns"
"claude haiku vs sonnet when to use"
```

---

### Keyword Implementation Strategy

**Title Formulas That Work for Technical Content:**

1. **Problem-Solution**: "Reducing LLM Costs: How We Cut API Spend 60%"
2. **Pattern-Based**: "3 Sub-Agent Patterns That Actually Work in Production"
3. **Comparison**: "Claude Code vs Cursor: A Senior Engineer's Honest Take"
4. **How-To Specific**: "Context Engineering: The Missing Guide for AI Engineers"
5. **Numbered + Year**: "5 MCP Server Patterns Every AI Engineer Should Know (2025)"

**On-Page SEO for Technical Posts:**

- Include primary keyword in first 100 words naturally
- Use `TechArticle` schema with `proficiencyLevel: Expert`
- Code blocks with semantic `<pre><code>` tags (Google parses these)
- Include version numbers where relevant (signals freshness)
- Meta descriptions with specifics: "Learn the 3 architecture patterns for production agentic AI. Includes latency benchmarks, error handling, and cost analysis from 50K+ runs."

**Words to Avoid (trigger engineer skepticism):**
- "game-changer", "revolutionary", "unlock", "ultimate guide"
- "in today's fast-paced world", "cutting-edge"

**Words That Build Trust:**
- Specific version numbers
- "Here's what we learned"
- Measurable outcomes ("reduced latency by 40%")
- References to source code
- Honest limitations ("This doesn't work when...")

---

## Part 2: Content Production Pipeline

The goal is to **write once, distribute everywhere** with a systematic process. Each blog post becomes the seed for 5-7 derivative pieces across platforms.

---

### The ACIDBATH Content Factory

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CORE BLOG POST                               │
│                     (2,000-2,500 words)                             │
│                                                                     │
│  Structure:                                                         │
│  ├── Hook/Problem Statement (100 words)                             │
│  ├── Key Insight/Thesis (200 words)                                 │
│  ├── Technical Deep-Dive with Code (1,200-1,500 words)              │
│  ├── Practical Example/Case Study (400 words)                       │
│  └── Takeaways + What's Next (200 words)                            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │ Twitter │          │LinkedIn │          │Substack │
   │  Thread │          │  Post   │          │Newsletter
   └────┬────┘          └────┬────┘          └────┬────┘
        │                    │                    │
        ▼                    ▼                    ▼
   5-8 tweets           800-1200 words      1,000-1,500 words
   with hook            professional        personal angle
                        + code snippet      + link to full post
```

---

### Extraction Templates by Platform

#### Twitter/X Thread Template

**Purpose**: Drive awareness, build following, link to full post

**Structure**:
```
Tweet 1 (Hook): 
  - Contrarian take or surprising insight
  - No link, pure hook
  - Example: "Your context window is bleeding. Here's what most AI engineers get wrong about token management:"

Tweets 2-5 (Core Points):
  - One key insight per tweet
  - Can include code snippets (screenshot or text)
  - Example: "1/ Progressive disclosure saves 90% of context consumption. Instead of dumping everything upfront, inject context only when the agent needs it."

Tweet 6-7 (Proof/Example):
  - Concrete result or code example
  - Example: "We went from 180K tokens to 20K on average. Same results, 80% cost reduction. Here's the pattern:"

Final Tweet (CTA):
  - Link to full post
  - Example: "Full implementation guide with working code: [link]"
```

**Extraction Prompts for Claude**:
```markdown
Given this blog post, extract a Twitter thread:

1. Create a hook tweet (controversial or surprising angle, no link, max 280 chars)
2. Extract 4-5 key insights as individual tweets (each standalone value)
3. Include one code snippet or concrete example tweet
4. End with CTA linking to full post

Rules:
- No hashtags (engineers hate them)
- No emojis except sparingly
- Each tweet must stand alone
- Be opinionated, not hedging
```

---

#### LinkedIn Post Template

**Purpose**: Professional credibility, reach CTOs/senior engineers

**Structure**:
```
Opening Hook (1-2 sentences):
  - Personal experience or observation
  - Pattern: "I've reviewed 50+ agent implementations. 80% fail for the same reason."

Context/Setup (2-3 sentences):
  - Why this matters to their role
  - Pattern: "Engineering leaders are asking: why do our AI agents fail in production?"

Core Insight (3-5 sentences):
  - The main thesis, expanded
  - Include one specific technique or pattern

Code Block or Technical Snippet:
  - Short, readable example
  - 10-15 lines max

Proof Point (2-3 sentences):
  - Concrete result
  - Pattern: "After implementing this pattern, we reduced context consumption by 90%."

CTA (1-2 sentences):
  - Link to full post
  - Pattern: "I wrote a full implementation guide with working code: [link]"
  - OR: "Agree? Disagree? I'd love to hear what patterns have worked for you."
```

**Extraction Prompts for Claude**:
```markdown
Given this blog post, create a LinkedIn post (800-1200 words):

1. Start with a hook based on personal experience or observation
2. Frame the problem for engineering leaders
3. Distill the key insight (don't give everything away)
4. Include one short code snippet or technical example
5. End with a result/proof point and link to full post

Rules:
- Write in first person
- Be opinionated and direct
- Use short paragraphs (1-3 sentences)
- No bullet points unless listing 3+ items
- Professional but not stiff
```

---

#### Substack Newsletter Template

**Purpose**: Build owned audience, deeper relationship, drive traffic

**Structure**:
```
Personal Opening (2-3 sentences):
  - What prompted this post
  - Pattern: "I spent last week debugging an agent that kept running out of context. It led me to a realization..."

Story/Context (1-2 paragraphs):
  - Narrative framing
  - Why you care about this topic

The Big Idea (1-2 paragraphs):
  - Core thesis from the blog post
  - Slightly different angle than Twitter/LinkedIn

Key Technique (1 paragraph + optional code):
  - One actionable takeaway
  - Not the full implementation—tease the depth

What I'm Reading/Thinking (optional):
  - 2-3 links to related content
  - Commentary on industry trends

CTA:
  - Link to full post
  - Pattern: "If you want the full implementation with code, I wrote it up here: [link]"
```

**Extraction Prompts for Claude**:
```markdown
Given this blog post, create a newsletter edition (1,000-1,500 words):

1. Start with personal context—what prompted this exploration
2. Tell a brief story that frames the problem
3. Share the core insight in your own voice
4. Include one actionable technique (not everything)
5. Optional: add 2-3 related links you're reading
6. End with link to full post

Rules:
- First person, conversational
- More personal than LinkedIn
- Don't reproduce the full post—create complementary content
- Include your opinions and reactions
```

---

### The Systematic Workflow

**Phase 1: Pre-Writing (30 min)**
```
1. Choose topic based on keyword research
2. Outline structure with target keyword in H1
3. Note key code examples to include
4. Identify the "contrarian angle" for Twitter hook
5. Note personal story/context for newsletter
```

**Phase 2: Core Post Writing (2-3 hours)**
```
1. Write blog post following structure
2. Ensure code examples are complete and runnable
3. Include specific metrics/results where possible
4. End with clear takeaways
```

**Phase 3: Derivative Extraction (45 min)**
```
Using Claude or Claude Code:

1. Generate Twitter thread draft
   - Review hook for punch
   - Ensure each tweet has standalone value
   
2. Generate LinkedIn post draft
   - Adjust for professional tone
   - Add personal experience framing
   
3. Generate newsletter draft
   - Add personal story context
   - Include "what I'm reading" section
```

**Phase 4: Review & Polish (30 min)**
```
1. Review all derivatives for consistency
2. Ensure each piece has unique value (not just copy-paste)
3. Schedule posts:
   - Blog: Publish immediately
   - Twitter: Same day or next morning (8-10am EST Wed for HN)
   - LinkedIn: Same day, afternoon
   - Newsletter: Weekly batch (e.g., every Sunday)
```

---

### Claude Code Command for Content Extraction

Create a `.claude/commands/content-extract.md`:

```markdown
# Content Extraction Command

Extract derivative content from a blog post for multi-platform distribution.

## Input
- Blog post file path

## Output
Generate three files in `/content/derivatives/`:

1. `{slug}-twitter.md` - Twitter thread (8-12 tweets)
2. `{slug}-linkedin.md` - LinkedIn post (800-1200 words)  
3. `{slug}-newsletter.md` - Newsletter edition (1000-1500 words)

## Guidelines

### Twitter
- Hook tweet: contrarian or surprising, no link
- 4-6 insight tweets: one point each, standalone value
- 1-2 code/example tweets: concrete demonstration
- CTA tweet: link to full post
- No hashtags, minimal emojis

### LinkedIn
- Personal opening: what prompted this
- Problem framing for engineering leaders
- Core insight (not everything)
- Short code snippet (10-15 lines max)
- Result/proof point
- Link to full post
- First person, professional but opinionated

### Newsletter
- Personal story opening
- Narrative context
- One key actionable technique
- "What I'm reading" section (can leave placeholder)
- Link to full post
- Conversational, more personal than LinkedIn
```

---

### Content Calendar Structure

**Weekly Rhythm:**
```
Monday: Draft core blog post
Tuesday: Finish and publish blog post
         Extract Twitter thread, schedule for Wednesday AM
Wednesday: Post to LinkedIn
           Submit to HN (8-10am EST)
Thursday: Engage in comments across platforms
Friday: Draft newsletter edition
Saturday: (Buffer/rest)
Sunday: Send newsletter
```

**Monthly Content Mix:**
```
Week 1: Deep technical tutorial (keyword-targeted)
Week 2: Opinion/POV piece (builds authority)
Week 3: News analysis/rapid commentary (timely reach)
Week 4: Case study / "What Actually Worked" (differentiator)
```

---

### Tracking & Iteration

**Metrics to Track:**

| Platform | Primary Metric | Secondary |
|----------|---------------|-----------|
| Blog | Organic search traffic | Time on page |
| Twitter | Impressions + profile clicks | Thread engagement |
| LinkedIn | Post views + comments | Profile views |
| Newsletter | Open rate + CTR | Reply rate |
| HN | Points + front page | Comment quality |

**Monthly Review:**
```
1. Which topics drove the most traffic?
2. Which Twitter hooks got best engagement?
3. What LinkedIn framing worked?
4. Newsletter open rates by topic?
5. Any HN front page hits?

→ Double down on what works
→ Retire what doesn't
→ Test new angles on winning topics
```

---

## Quick Reference: Keywords to Target in Next 10 Posts

| Post # | Primary Keyword | Secondary Keywords | Content Type |
|--------|-----------------|-------------------|--------------|
| 1 | context engineering | context window, progressive disclosure | Tutorial |
| 2 | Claude Code workflow | CLAUDE.md, sub-agents | How-to |
| 3 | MCP server tutorial | model context protocol, tool calling | Tutorial |
| 4 | AI agent failure patterns | reliability, production, debugging | POV/Analysis |
| 5 | LLM cost optimization | token efficiency, model routing | Case Study |
| 6 | sub-agent orchestration | multi-agent, coordination patterns | Deep Dive |
| 7 | Claude Code MCP setup | configuration, troubleshooting | How-to |
| 8 | agentic prompt patterns | ReAct, workflow sections | Tutorial |
| 9 | context collapse | brevity bias, ACE framework | Analysis |
| 10 | Claude Code vs Cursor | comparison, honest take | Opinion |

---

## Implementation Checklist

**Week 1:**
- [ ] Set up content derivatives folder structure
- [ ] Create Claude Code extraction command
- [ ] Set up Substack newsletter
- [ ] Configure HN submission tracking

**Week 2:**
- [ ] Publish first keyword-targeted post
- [ ] Execute full derivative extraction workflow
- [ ] Post to all platforms
- [ ] Submit to HN

**Ongoing:**
- [ ] Weekly: Execute content calendar
- [ ] Monthly: Review metrics, adjust strategy
- [ ] Quarterly: Keyword research refresh
