# Ameno Voice Style Guide

## Workflow Position

**This style is applied during review and finalization, not creation.**

```
/new-post → Draft (ACIDBATH) → /ai-audit → /ameno-finalize → Publish
```

---

## Core Philosophy

**ACIDBATH is the star. Ameno voice is the flavor.**

The Ameno voice exists for **simplification** - making difficult concepts accessible without dumbing them down. It's not about catchphrases or forced metaphors. It's about clarity with character.

Lead with technical value. The Ameno voice adds character to explanations when it genuinely helps understanding, not as decoration.

---

## Voice DNA

| Trait | Description | Example |
|-------|-------------|---------|
| **Conversational Directness** | Contractions, second-person, informal tone | "You're probably wondering..." not "One might wonder..." |
| **Simplification** | Make complex things clear without metaphors | "That's 20% of your context gone before you start" |
| **Strategic Profanity** | Emphasis, not shock value | "pretty damn good", "WTF" |
| **Humble Self-Awareness** | Admitting uncertainty, honest about limits | "This might be wrong, but here's my take..." |
| **Honest Failure Modes** | Conversational about what breaks | "This is where it bites you" |

**Removed from DNA**: Forced analogies, catchphrase deployment, pop culture overload

---

## Strategic Deployment Guide

### When to Use Ameno Voice

| Context | Ameno Approach |
|---------|----------------|
| **Concept simplification** | Restate in plain terms, NOT with metaphors |
| **Failure modes** | Conversational honesty: "This is where both patterns bite you" |
| **Takeaways** | Add style to summary, make it stick |
| **Significance** | "That's 94% reduction" → "That's 94% reduction. For tools you might not even use." |

### When to Stay Direct (ACIDBATH)

| Context | Stay Direct |
|---------|-------------|
| **Introductions** | Lead with facts and results |
| **Code examples** | Let the code speak |
| **Benchmarks/numbers** | Specific, verifiable |
| **Configuration** | Step-by-step |
| **Gotchas** | Bullet points |

---

## Metaphor Restraint

**Default: Don't use metaphors.**

Metaphors are appropriate only when:
1. The concept is genuinely complex (not just unfamiliar)
2. The metaphor actually simplifies (doesn't add cognitive load)
3. You've developed it deliberately with the author (not reached for one on the fly)

### Bad Example

"Think of your context window like a cargo train with numbered cars..."

This adds complexity. "Context window" is already understandable. The train metaphor requires the reader to:
1. Map train cars to tokens
2. Understand the cargo analogy
3. Then map back to the actual concept

**More cognitive load, not less.**

### Good Example

"MCP servers load all tool descriptions upfront. Four servers at 10K tokens each = 40K tokens gone before you start. That's 20% of your context. For tools you might not even use."

Direct. Clear. The simplification ("For tools you might not even use") adds punch without metaphor.

### When Metaphors ARE Needed

For genuinely complex concepts (multi-step pipelines, distributed systems architecture, complex state machines), metaphors can help. But:

1. **Develop them collaboratively** with the author
2. **Deploy them consistently** across related posts
3. **Don't reach for them on the fly** - that's when they become forced

See METAPHOR_FRAMEWORKS.md for the library of developed metaphors.

---

## Structural Pattern

The default explanation structure:

```
Definition → Significance → Code → Result → Takeaway
```

Example:

1. **Definition** (direct): "Progressive disclosure loads context only when needed."
2. **Significance** (Ameno): "That's the difference between 40K tokens upfront and 2K when you actually need them."
3. **Code** (direct): `<code block>`
4. **Result** (direct): "94% reduction in context consumption."
5. **Takeaway** (Ameno): "The optimization is invisible. Your agent just works faster."

Notice: No forced metaphor. Simplification adds clarity.

---

## Where Conversational Phrases Help

These phrases earn their place because they signal **common patterns**, not because they're catchy:

| Phrase | When It Helps |
|--------|---------------|
| "This is where [X] bites you" | Failure modes that readers will actually hit |
| "Here's what actually happens" | Cutting through abstraction |
| "The numbers tell the story" | Transitioning to evidence |

**These are NOT catchphrases to deploy everywhere.** They're natural transitions for specific contexts. If you find yourself using "Here's where things get weird" in every section, stop.

---

## Humor and Profanity

### When Humor Works

- After complex explanation (release tension)
- In failure stories (self-deprecation)
- Wrapping up sections (memorable close)

### When Humor Fails

- In introductions (earn attention with value first)
- During step-by-step instructions (interrupts flow)
- More than once per section (dilutes impact)

### Profanity Protocol

Strategic profanity adds emphasis. Overuse removes impact.

**Appropriate**: "pretty damn good", "WTF is going on here?", "this is a pain in the ass"

**Inappropriate**: Every paragraph, code comments, headings

---

## Vocabulary

### Phrases to Avoid

| Avoid | Why |
|-------|-----|
| "Revolutionary" | Hype-speak |
| "Game-changer" | Overused |
| "Simply put" | Often precedes complexity |
| "Obviously" | Condescending |
| "It's easy" | Dismissive |
| "Just" | Minimizes complexity |
| "Think of it like..." | Often forces metaphors |

### Natural Transitions

| Context | Phrase |
|---------|--------|
| Failure modes | "This is where it bites you" |
| Evidence | "The numbers tell the story" |
| Reality check | "Here's what actually happens" |
| Significance | "That means..." |

---

## Anti-Patterns

### Voice Mistakes

1. **Forced metaphors** - If the concept is clear without one, don't add one
2. **Catchphrase deployment** - This isn't Power Rangers
3. **Personality in introductions** - Lead with value
4. **Decorating simple concepts** - "Context window" doesn't need an analogy
5. **Excessive transitions** - "Here's where things get weird" loses impact when overused
6. **Reaching for analogies** - If you're searching for one, you don't need one

### Structural Mistakes

1. **Metaphor-first** - Don't start explanations with analogies
2. **Personality in code** - Let code speak
3. **Fluff in takeaways** - Style yes, padding no

---

## Sample Application

### Before (Generic Technical)

"Context window consumption averages 180K tokens in typical sessions. This represents a significant computational overhead that impacts both latency and cost."

### After (Ameno Voice - WITHOUT Metaphor)

"Context consumption averages 180K tokens per session. That's $0.40 per conversation before you even start.

Default MCP setups load all tool descriptions upfront. Four servers at 10K tokens each = 40K tokens consumed. That's 20% of your context gone. For tools you might not even use.

Progressive disclosure fixes this. Load tools only when needed. Result: 2,500 tokens average. 94% reduction."

**What changed**: Simplified with significance ("$0.40 before you start", "For tools you might not even use"), not with metaphors.

---

## Integration with ACIDBATH

| ACIDBATH Tenet | Ameno Voice Application |
|----------------|------------------------|
| **POC Rule** | Code examples stay direct |
| **Numbers Test** | Numbers stay factual; Ameno adds significance |
| **Production Lens** | Gotchas stay bulleted; Ameno explains "why it hurts" |
| **Senior Engineer Filter** | Respect reader intelligence; simplify, don't decorate |
| **Honest Failure Requirement** | Failure sections get conversational honesty |
| **Try It Now** | Call to action stays direct |
