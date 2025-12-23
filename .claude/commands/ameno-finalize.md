# Ameno Finalize

Review and finalize a blog post by applying Ameno voice where appropriate. ACIDBATH is the star - Ameno voice is the flavor applied during editing, not creation.

## Usage

```
/ameno-finalize src/content/blog/your-post.md
```

## Philosophy

**Creation**: Write in ACIDBATH's direct, technical voice.
**Finalization**: Apply Ameno voice to specific sections that benefit from personality.

The Ameno voice exists for **simplification** - making difficult concepts accessible without dumbing them down. It's not about catchphrases or forced metaphors.

---

## Process

### 1. Read the Post

Read the file at: $ARGUMENTS

### 2. Identify Section Types

Classify each section by type:

| Section Type | Voice Treatment |
|--------------|-----------------|
| Introduction | Keep **direct** - facts and results |
| Concept explanation | Consider **Ameno** - simplify, clarify |
| Code examples | Keep **direct** - let code speak |
| Benchmarks/numbers | Keep **direct** - specific, verifiable |
| Failure modes | Consider **Ameno** - conversational honesty |
| Configuration/steps | Keep **direct** - no narrative |
| Takeaways | Consider **Ameno** - memorable close |

### 3. Review Direct Sections

Verify these stay direct:
- [ ] Introduction leads with facts and results, not personality hooks
- [ ] Code blocks are clean, no narrative inside
- [ ] Numbers are specific and verifiable (not "significantly faster")
- [ ] Configuration steps are step-by-step

### 4. Apply Ameno Voice Where Appropriate

For concept explanations, failure modes, and takeaways:

**Simplification** (primary technique):
- Restate complex things in plain terms
- Add significance: "That means..." / "That's 20% of your context gone."
- NOT forced metaphors

**Conversational honesty** (for failure modes):
- "This is where it bites you"
- "Here's what actually happens"
- Direct about limitations

**Memorable closes** (for takeaways):
- Style without fluff
- "The optimization is invisible. Your agent just works faster."

### 5. Anti-Pattern Check

Flag if any of these appear:
- [ ] Forced metaphors where direct explanation works
- [ ] Catchphrases deployed excessively
- [ ] Personality in introductions before establishing value
- [ ] "Think of it like..." preceding unnecessary analogies
- [ ] Multiple "here's where things get weird" style phrases

---

## Reference Files

Load these for detailed guidance:
- `ai_docs/ameno-voice-style.md` - Full voice DNA
- `.claude/skills/ameno-voice/SKILL.md` - Quick reference
- `.claude/skills/ameno-voice/EXAMPLES.md` - Before/after transformations

---

## Output Format

Provide a summary:

```markdown
## Ameno Finalize Report

### Sections Reviewed
- **Keep Direct**: [list sections that should stay as-is]
- **Applied Ameno**: [list sections where voice was added/enhanced]

### Changes Made
[Describe specific edits, with before/after snippets for significant changes]

### Anti-Patterns Flagged
[List any issues found, or "None"]

### Final Check
- [ ] Introduction stays direct
- [ ] Code stays clean
- [ ] Numbers stay specific
- [ ] Ameno voice adds clarity, not decoration
```

---

## Example Transformation

**Before (generic technical):**
> "Context window consumption averages 180K tokens in typical sessions. This represents a significant computational overhead."

**After (Ameno finalize):**
> "Context consumption averages 180K tokens per session. That's $0.40 per conversation before you even start."

The intro is direct. The Ameno touch adds significance ("$0.40 before you start") without metaphor.
