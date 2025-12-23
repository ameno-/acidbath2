---
name: ameno-voice
description: Apply Ameno's distinctive voice style to content. Use when writing blog posts, tutorials, or technical content. Strategically deploys personality (analogies, humor, conversational tone) for exploratory/educational sections while maintaining directness for technical details.
---

# Ameno Voice Style Skill

Apply the Ameno voice to technical content. **ACIDBATH is the star. Ameno voice is the flavor.**

## Quick Reference

### Voice Checklist

Before publishing, verify:

- [ ] Introduction leads with **facts and results**, not personality hook
- [ ] Each concept has an **analogy** using construction/engineering metaphor
- [ ] Code blocks are **direct** - no narrative inside
- [ ] Numbers and benchmarks are **specific and verifiable**
- [ ] Failure sections have **conversational honesty**
- [ ] Takeaways use **signature phrases** ("Not bad for...", "Here's the move:")
- [ ] Emoji usage is **strategic** (max 3-4 per section)
- [ ] Profanity is **emphasis** (sparingly), not filler

### When to Deploy Personality

| Content Type | Voice |
|--------------|-------|
| Concept explanation | **Ameno** - analogies, "so what?" |
| Failure modes | **Ameno** - honest, conversational |
| Takeaways | **Ameno** - memorable, brief |
| Introduction | **Direct** - facts, results |
| Code examples | **Direct** - clean, minimal |
| Benchmarks | **Direct** - specific, no fluff |
| Gotchas | **Direct** - bullet points |

### Signature Phrases

Transition INTO personality:
- "Here's where things get a little weird."
- "Think of it like this:"
- "So what does that mean?"
- "To put that into perspective..."

Close with personality:
- "Not bad for [X]."
- "Here's the move:"
- "Pretty damn useful."

### Structural Pattern

```
Definition → "So what?" → Analogy → Code → Plain English → Takeaway
```

---

## Supporting Files

For detailed guidance, read these files:

- **[ai_docs/ameno-voice-style.md](../../ai_docs/ameno-voice-style.md)** - Full voice DNA, vocabulary, anti-patterns
- **[METAPHOR_FRAMEWORKS.md](./METAPHOR_FRAMEWORKS.md)** - Construction/engineering metaphor library
- **[EXAMPLES.md](./EXAMPLES.md)** - Before/after transformations

---

## Example Flow

```
[INTRO - direct] "Context consumption averages 180K tokens per session.
That's $0.40 per conversation before you even start."

[PROBLEM - direct] "Default MCP setups dump everything upfront.
No progressive loading."

[EXPLANATION - Ameno] "Think of it like leaving every light on in your
house before checking which rooms you need."

[SOLUTION - direct] "Progressive disclosure injects context only when
the agent needs it."

[CODE - direct] <code block>

[RESULT - direct] "20K tokens average. 89% reduction."

[FLAVOR - Ameno] "Not bad for 20 lines of Python."
```

---

## Anti-Patterns

Avoid these mistakes:

1. **Starting with personality** - Lead with technical value
2. **Forced humor** - If it doesn't land naturally, cut it
3. **Emoji spam** - Treat like exclamation points: rare
4. **Personality in code** - Let code be code
5. **Excessive hedging** - Be direct, not "might/could/perhaps"
