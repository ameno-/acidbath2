---
name: ameno-voice
description: Suggest edits to add Ameno voice personality to concept explanations, failure modes, and takeaways while preserving direct introductions, code, and benchmarks. Uses suggest_edits pattern - suggests changes, never auto-applies.
allowed-tools: Read
---

# Ameno Voice Style Skill

**Suggestion-based skill** for adding Ameno voice to drafted content.

## Workflow Position

```
/new-post → Write draft (ACIDBATH default) → [OPTIONAL] /ameno-finalize → Review suggestions → Apply selectively → Publish
```

Creation happens in ACIDBATH's direct voice. This skill **suggests edits** during review phase. You decide which suggestions to apply.

**Pattern**: Uses suggest_edits framework - outputs edit suggestions with rationale, never modifies files.

## Core Purpose

The Ameno voice exists for **simplification** - making difficult concepts accessible without dumbing them down. It's not about catchphrases or forced metaphors. It's about clarity with character.

## Quick Reference

### Voice Checklist

Before publishing, verify:

- [ ] Introduction leads with **facts and results**, not personality
- [ ] Complex concepts are **simplified**, not decorated with metaphors
- [ ] Code blocks are **direct** - no narrative inside
- [ ] Numbers and benchmarks are **specific and verifiable**
- [ ] Failure sections have **conversational honesty** ("This is where it bites you")
- [ ] Takeaways add **style without fluff**
- [ ] Metaphors are used **only when they genuinely clarify** (rare)

### When to Deploy Personality

| Content Type | Voice | Notes |
|--------------|-------|-------|
| Concept explanation | **Ameno** - simplify, clarify | NOT with forced metaphors |
| Failure modes | **Ameno** - honest, direct | "This is where both patterns bite you" |
| Takeaways | **Ameno** - memorable summary | Style, not catchphrases |
| Introduction | **Direct** - facts, results | No personality hooks |
| Code examples | **Direct** - clean | Let code speak |
| Benchmarks | **Direct** - specific | No fluff |
| Configuration | **Direct** - step-by-step | No narrative |

---

## Metaphor Guidance

**Default: Don't use metaphors.**

Metaphors are helpful only when:
1. The concept is genuinely complex (not just unfamiliar)
2. The metaphor actually simplifies (doesn't add cognitive load)
3. You've developed it deliberately (not reached for one on the fly)

**Bad**: "Think of your context window like a cargo train with numbered cars" (adds complexity to a simple concept)

**Good**: Directly explaining what happens: "MCP servers load all tool descriptions upfront. Four servers at 10K tokens each = 40K tokens gone before you start."

When metaphors ARE needed for complex concepts, develop them collaboratively and deploy them consistently across related posts. See METAPHOR_FRAMEWORKS.md for the library.

---

## Where Conversational Phrases Help

Certain phrases earn their place because they signal common patterns:

- **"This is where [X] bites you"** - Signals a failure mode readers will likely hit
- **"Here's what actually happens"** - Cuts through abstraction to reality
- **"The numbers tell the story"** - Transitions to evidence

These aren't catchphrases to deploy everywhere. They're natural transitions for specific contexts.

---

## Example Flow

```
[INTRO - direct] "Context consumption averages 180K tokens per session.
That's $0.40 per conversation before you even start."

[PROBLEM - direct] "Default MCP setups load all tool descriptions upfront.
Four servers at 10K tokens each = 40K tokens consumed before any work."

[SIMPLIFICATION - Ameno] "That's 20% of your context gone. For tools you
might not even use."

[SOLUTION - direct] "Progressive disclosure loads tools only when needed."

[CODE - direct] <code block>

[RESULT - direct] "20K tokens average. 94% reduction."

[TAKEAWAY - Ameno] "The optimization is invisible. Your agent just works
faster and costs less."
```

Notice: No forced metaphor. The simplification ("That's 20% of your context gone") adds clarity without adding cognitive load.

---

## Anti-Patterns

1. **Forced metaphors** - If the concept is already clear, metaphors add noise
2. **Catchphrase deployment** - This isn't Power Rangers; earn each phrase
3. **Personality in introductions** - Lead with value, not hooks
4. **Decorating simple concepts** - "Context window" doesn't need a train analogy
5. **Excessive transitions** - "Here's where things get weird" loses impact when overused

---

## Suggest_Edits Implementation

### Process

When invoked with `/ameno-finalize {file}`:

1. **Read content** using Read tool
2. **Classify sections** by type (introduction, concept-explanation, failure-mode, takeaway, code, benchmark)
3. **Identify edit candidates** (concept explanations, failure modes, takeaways that could benefit from simplification)
4. **Generate suggestions** with before/after and rationale
5. **Output in suggest_edits format** (NO file modification)

### Section Focus

| Section Type | Action | Transformation |
|--------------|--------|----------------|
| `introduction` | **PRESERVE** | Keep direct, factual |
| `concept-explanation` | **EDIT** | Simplify without metaphor abuse |
| `failure-mode` | **EDIT** | Add conversational honesty |
| `takeaway` | **EDIT** | Add memorable style |
| `code` | **PRESERVE** | Never inject personality |
| `benchmark` | **PRESERVE** | Keep factual |

### Output Format

Standard suggest_edits format:

```markdown
# Edit Suggestions for {Post Title}

Generated by: Ameno Voice
Date: {YYYY-MM-DD}

## Summary

**Total Suggestions**: {N}
**Editable Sections**: {N}
**Preserved Sections**: {N}

**Focus Areas**:
- Simplifying concept explanations
- Adding conversational honesty to failure modes
- Making takeaways memorable

---

## Suggested Edit {N}: {Section Name}

**Type**: {concept-explanation|failure-mode|takeaway}
**Rationale**: {Why this simplification improves clarity}

### Before
```
{exact original content}
```

### After
```
{Ameno voice transformation}
```

### Apply This Edit?
- [ ] Yes, apply as-is
- [ ] Apply with modifications
- [ ] Skip this edit
```

### Rationale Requirements

Every Ameno suggestion must explain:
- **What clarity principle** is applied (simplification, directness, honesty)
- **How it improves understanding** (removes abstraction, adds relatability)
- **Why personality fits here** (vs sections that should stay direct)

**Example rationale**: "Simplifies abstract concept ('context consumption') to concrete impact ('20% of your context gone'). Adds relatability through direct comparison without introducing metaphor. Fits concept-explanation type where clarity improves understanding."

### Suggestion Limits

- **Typical range**: 4-7 suggestions per post
- **Priority**: Concept explanations > Failure modes > Takeaways
- **Quality over quantity**: Only suggest where personality genuinely improves clarity

---

## Supporting Files

- **[ai_docs/ameno-voice-style.md](../../ai_docs/ameno-voice-style.md)** - Full voice DNA, vocabulary
- **[ai_docs/suggest-edits-framework.md](../../ai_docs/suggest-edits-framework.md)** - Core suggest_edits framework
- **[METAPHOR_FRAMEWORKS.md](./METAPHOR_FRAMEWORKS.md)** - For genuinely complex concepts (use sparingly)
- **[EXAMPLES.md](./EXAMPLES.md)** - Before/after transformations in suggest_edits format
