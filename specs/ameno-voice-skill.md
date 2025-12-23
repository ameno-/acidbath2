# Ameno Voice Style Skill

## Overview

A **review-phase** voice/style system for ACIDBATH blog content. Ameno voice is applied during editing and finalization, not creation. The system adds personality to specific sections (concept explanations, failure modes, takeaways) while preserving directness where it matters.

---

## Workflow Position

```
/new-post → Draft in ACIDBATH voice → /ameno-finalize → Publish
```

| Phase | Voice | Tools |
|-------|-------|-------|
| **Creation** | ACIDBATH (direct, technical) | `/new-post`, manual writing |
| **Audit** | Structural (SEO, fields) | `/ai-audit` |
| **Finalize** | Ameno (selective application) | `/ameno-finalize` |
| **Publish** | - | Deploy |

---

## Core Philosophy

**ACIDBATH is the star. Ameno voice is the flavor.**

Lead with technical value. Don't hook on personality - hook on facts and results. The Ameno voice adds character and style to explanations, not entertainment for its own sake.

---

## Voice DNA

| Trait | Description |
|-------|-------------|
| **Conversational Directness** | Contractions, second-person, informal transitions |
| **Analogy-First Teaching** | Every concept anchored to real-world example |
| **Strategic Profanity** | "pretty damn good", "son of a bitch", "WTF" for emphasis |
| **Pop Culture Integration** | Memes, song references, movie quotes |
| **Humble Self-Awareness** | Work-in-progress notes, admitting uncertainty |
| **Extended Metaphor Architecture** | Learning journey mapped to construction/engineering concepts |
| **Strategic Emoji** | Punctuation not decoration - limited, purposeful use |

---

## Strategic Deployment Model

| Content Type | Voice Treatment |
|--------------|-----------------|
| **Introduction** | Direct, fact-based - lead with the technical problem and result |
| **Concept explanation** | Ameno flavor - analogies, "so what?", make it click |
| **Why this matters** | Directness first - the case speaks for itself |
| **Code examples** | Direct - let the code speak, minimal decoration |
| **Benchmarks/numbers** | Direct - specific, verifiable, no fluff |
| **Failure modes** | Ameno flavor - conversational honesty, "here's where things break" |
| **Production gotchas** | Direct - bullet points, actionable warnings |
| **Takeaways** | Brief Ameno flavor - "the move" summary style |

---

## Files to Create

### 1. `ai_docs/ameno-voice-style.md`

Core reference document (~2000 words) containing:

1. **Voice DNA** - Personality traits table
2. **Strategic Deployment Guide**
   - When to inject personality (concept explanations, failure stories, takeaways)
   - When to stay direct (code, benchmarks, gotchas, introductions)
   - Transition patterns between modes within same content
3. **Structural Patterns** - How to organize explanations
4. **Analogy Guidelines** - How to create anchoring analogies
5. **Humor Rules** - When/how to deploy
6. **Vocabulary** - Phrases to use, phrases to avoid
7. **Emoji Protocol** - Strategic usage
8. **Anti-patterns** - What NOT to do

### 2. `.claude/skills/ameno-voice/SKILL.md`

Skill definition with YAML frontmatter:

```yaml
---
name: ameno-voice
description: Apply Ameno's distinctive voice style to content. Use when writing blog posts, tutorials, or technical content. Strategically deploys personality (analogies, humor, conversational tone) for exploratory/educational sections while maintaining directness for technical details.
allowed-tools: Read, Write, Edit
---
```

Contents:
1. Quick reference voice checklist
2. Strategic deployment triggers
3. Links to supporting files

### 3. `.claude/skills/ameno-voice/METAPHOR_FRAMEWORKS.md`

Library of construction/engineering-oriented metaphors:

1. **Building a Bridge** - Foundations, load bearing, structural integrity, stress testing
2. **Train System** - Tracks (pipelines), stations (endpoints), cargo (data), switches (conditionals)
3. **Building a House** - Foundation, framing, plumbing/electrical (dependencies), finishing
4. **Factory Assembly Line** - Components, stations, quality control, throughput
5. **Power Grid** - Sources, transformers, distribution, load balancing
6. **Plumbing System** - Pipes (streams), valves (gates), pressure (load), drainage (cleanup)

Each framework includes:
- Phase names mapped to technical concepts
- Sample explanatory sentences
- When to use (which technical concepts fit best)

### 4. `.claude/skills/ameno-voice/EXAMPLES.md`

Concrete before/after transformations showing:
1. Explaining arrays (generic → Ameno style)
2. Error handling (dry → engaging)
3. API concepts (technical → relatable)
4. Context engineering (technical → accessible)

---

## Signature Phrases

Use these transitional phrases when shifting to Ameno voice:

- "Here's where things get a little weird"
- "To put that into perspective..."
- "So what does that mean?"
- "Think of it like this:"
- "pretty dumb, right?"
- "Not bad for [X]."
- "Here's the move:"

---

## Example Flow

```
[INTRO - direct] "Context consumption averages 180K tokens per session. That's $0.40 per conversation before you even start."
[PROBLEM - direct] "Default MCP setups dump everything upfront. No progressive loading."
[EXPLANATION - Ameno] "Think of it like leaving every light on in your house before checking which rooms you need."
[SOLUTION - direct] "Progressive disclosure injects context only when the agent needs it."
[CODE - direct] <code block>
[RESULT - direct] "20K tokens average. 89% reduction."
[FLAVOR - Ameno] "Not bad for 20 lines of Python."
```

---

## Integration Points

- `/ameno-finalize` - Primary invocation for review-phase voice application
- Reference in `ai_docs/ameno-voice-style.md` for context loading
- Runs **after** `/ai-audit` structural checks

---

## Validation Criteria

- [ ] `/ameno-finalize` command applies voice to appropriate sections only
- [ ] Direct sections (intro, code, benchmarks) remain unchanged
- [ ] Concept explanations gain clarity without forced metaphors
- [ ] Failure modes have conversational honesty
- [ ] Voice checklist is actionable and concise
