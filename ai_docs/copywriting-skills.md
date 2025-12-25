# Copywriting Skills Framework

Overview of ACIDBATH's copywriting skills system - three specialized skills for different persuasion and editing goals, all using the suggest_edits pattern for editorial control.

## Overview

The copywriting skills framework provides three distinct voices for strategic content enhancement:

1. **Mad Men Copywriter** - Conversion-focused, aggressive sales copy
2. **Master Copywriter** - Persuasion-focused, credibility-driven copy
3. **Ameno Voice** - Simplification-focused, technical-friendly personality

All skills use the **suggest_edits pattern** - they suggest changes with clear rationale, never auto-apply. You maintain full editorial control.

## Skills Comparison

| Skill | Focus | When to Use | Tone | Primary Technique | Typical Edits |
|-------|-------|-------------|------|-------------------|---------------|
| **Mad Men** | Conversion | Sales pages, CTAs, ads | Aggressive, urgent | Pain → Solution → Action | 5-8 |
| **Master** | Persuasion | Thought leadership, brand building | Authoritative, trustworthy | Credibility → Trust → Decision | 6-10 |
| **Ameno** | Simplification | Technical blog posts | Technical-friendly, honest | Direct → Clarity → Memorable | 4-7 |

## Decision Tree: Which Skill Should I Use?

```
START: What's your primary goal?

├─ Immediate conversion (signup, purchase, click)
│  └─ Use **Mad Men Copywriter** (/mad-men-edit)
│     └─ Focus: Drive action NOW through urgency and pain-focus
│
├─ Build trust and authority (long-term persuasion)
│  └─ Use **Master Copywriter** (/master-copy-edit)
│     └─ Focus: Establish credibility before asking for commitment
│
└─ Simplify technical concepts (educational content)
   └─ Use **Ameno Voice** (/ameno-finalize)
      └─ Focus: Make complex ideas accessible without dumbing down
```

### Content Type Guide

| Content Type | Recommended Skill | Rationale |
|--------------|------------------|-----------|
| Landing page | Mad Men | Maximum conversion focus |
| Product launch email | Mad Men | Drive immediate action |
| CEO blog post | Master | Build thought leadership |
| Technical whitepaper | Master | Establish expertise |
| Technical blog post | Ameno | Simplify while educating |
| Sales page | Mad Men | Convert visitors to buyers |
| About page | Master | Build trust and credibility |
| Case study | Master | Persuade through proof |
| How-to guide | Ameno | Teach with clarity |
| CTA copy | Mad Men | Maximize click-through |

## Integration with ACIDBATH Workflows

### Standalone Usage

Copywriting skills are **not** integrated into core workflows like `/new-post`. They're invoked explicitly when needed:

```
1. Create Draft → /new-post (direct voice, no personality)
   ↓
2. Review for Accuracy → Manual review
   ↓
3. [OPTIONAL] Run Copywriting Skill
   ├─ /mad-men-edit for conversion
   ├─ /master-copy-edit for persuasion
   └─ /ameno-finalize for simplification
   ↓
4. Review Suggestions → Evaluate rationale
   ↓
5. Selectively Apply Edits → User chooses which edits to use
   ↓
6. Final Review → Ensure consistency
   ↓
7. Publish
```

### Why Standalone?

Deliberately keeping copywriting skills as standalone commands rather than auto-applying:
- **Prevents coupling** - Skills can evolve independently
- **Preserves control** - User decides which suggestions fit
- **Allows combination** - Can run multiple skills, compare suggestions
- **Strategic use** - Apply where needed, not everywhere

## How suggest_edits Preserves Editorial Control

### Traditional Auto-Apply (Old Pattern)
```
[Content] → [Skill applies changes] → [Modified content]
❌ Problem: Loss of control, potential overwrites, unclear changes
```

### Suggest_Edits Pattern (New Pattern)
```
[Content] → [Skill suggests changes] → [User reviews] → [User applies selectively]
✅ Benefit: Full visibility, editorial control, understand WHY each edit
```

### Suggestion Format

Every suggestion includes:
- **Section name** - What part of content is being edited
- **Type** - Section classification (introduction, cta, concept-explanation, etc.)
- **Rationale** - WHY this edit improves content (specific principle/framework)
- **Before** - Exact original content
- **After** - Suggested replacement
- **Checklist** - Apply as-is | Modify | Skip

This transparency allows informed decision-making.

## Skill Details

### Mad Men Copywriter

**Voice DNA**: Write copy that fucking sells.

**Core Principles**:
- Hook in 2 seconds (pain-first, attention grab)
- Value by word 50 (front-load benefits)
- Eliminate weak sentences (every word earns its place)
- Drive action (benefit-driven CTAs)

**Frameworks**: AIDA, PAS, 4Ps, Before-After-Bridge

**Example Transformation**:
```
❌ Before: "Introducing our new analytics platform"
✅ After: "Stop making $1M decisions with gut feelings"
```

**Use for**: Sales pages, CTAs, ads, product launches

**Files**:
- `.claude/skills/mad-men-copywriter/SKILL.md` - Full documentation
- `.claude/skills/mad-men-copywriter/VOICE_DNA.md` - Voice characteristics
- `.claude/skills/mad-men-copywriter/FRAMEWORKS.md` - Copywriting frameworks
- `.claude/skills/mad-men-copywriter/EXAMPLES.md` - Before/after transformations

### Master Copywriter

**Voice DNA**: Persuade through credibility, trust, and authority.

**Core Principles**:
- Establish authority first (credentials, research, expertise)
- Use social proof strategically (testimonials, adoption stats)
- Tell stories (narrative illustrates benefits)
- Build credibility (specificity, evidence, proof access)

**Frameworks**: Cialdini's 6 Principles, StoryBrand, Hero's Journey

**Example Transformation**:
```
❌ Before: "Our security is world-class"
✅ After: "Our security team includes three former NSA cryptographers. They've spent 50,000 hours hardening this system. Here's their white paper..."
```

**Use for**: Thought leadership, brand building, high-trust sales, authority establishment

**Files**:
- `.claude/skills/master-copywriter/SKILL.md` - Full documentation
- `.claude/skills/master-copywriter/VOICE_DNA.md` - Voice characteristics
- `.claude/skills/master-copywriter/FRAMEWORKS.md` - Persuasion frameworks
- `.claude/skills/master-copywriter/EXAMPLES.md` - Before/after transformations

### Ameno Voice

**Voice DNA**: Simplification - making difficult concepts accessible without dumbing down.

**Core Principles**:
- Simplify without metaphor abuse
- Add conversational honesty to failure modes
- Make takeaways memorable
- Preserve direct introductions and code

**Anti-Patterns**: Forced metaphors, catchphrase abuse, personality in intros

**Example Transformation**:
```
❌ Before: "This represents a significant computational overhead"
✅ After: "That's 20% of your context gone. For tools you might not even use."
```

**Use for**: Technical blog posts, concept explanations, educational content

**Files**:
- `.claude/skills/ameno-voice/SKILL.md` - Full documentation
- `ai_docs/ameno-voice-style.md` - Full voice DNA
- `.claude/skills/ameno-voice/EXAMPLES.md` - Before/after transformations

## Commands

### /mad-men-edit {file_path}
Generate conversion-focused edit suggestions.

**Usage**: `/mad-men-edit content/landing-page.md`

**Output**: 5-8 suggestions focusing on hooks, CTAs, value props

### /master-copy-edit {file_path}
Generate persuasion-focused edit suggestions.

**Usage**: `/master-copy-edit content/thought-leadership.md`

**Output**: 6-10 suggestions focusing on authority, social proof, storytelling

### /ameno-finalize {file_path}
Generate simplification-focused edit suggestions.

**Usage**: `/ameno-finalize src/content/blog/technical-post.md`

**Output**: 4-7 suggestions focusing on concept clarity, failure honesty, memorable takeaways

## Best Practices

### For Skill Users

1. **Run after drafting** - Create content first, enhance second
2. **Review rationale** - Understand WHY each edit improves content
3. **Apply selectively** - Not all suggestions will fit your intent
4. **Modify suggestions** - Adapt to your voice and brand
5. **Re-read after applying** - Ensure consistency and flow
6. **Verify technical accuracy** - If code/configs touched, test them

### For Multiple Skills

You can run multiple skills on the same content:

```bash
/mad-men-edit article.md        # Conversion perspective
/master-copy-edit article.md    # Persuasion perspective
/ameno-finalize article.md      # Simplification perspective
```

Each provides different suggestions based on their focus. Choose what fits your goal.

### Combining Suggestions

Strategic combinations:
- **Ameno + Mad Men**: Simplify concepts, then add conversion CTAs
- **Master + Mad Men**: Build authority, then drive action
- **Ameno + Master**: Simplify for clarity, add credibility signals

## Framework Philosophy

### Why Three Skills?

Different content goals require different persuasion approaches:

- **Immediate conversion** (Mad Men) - Urgency, pain, action
- **Long-term persuasion** (Master) - Credibility, trust, authority
- **Clarity through simplification** (Ameno) - Accessibility, honesty, memorability

No single voice fits all contexts. Having three distinct skills allows strategic application.

### Why Suggest_Edits Pattern?

Auto-applying personality risks:
- Overwriting user voice
- Introducing errors in technical content
- Applying inappropriate tone to formal sections
- Loss of editorial control

Suggest_edits gives users:
- Full visibility into proposed changes
- Control over which edits to accept
- Understanding of WHY each edit improves content
- Ability to modify suggestions before applying

This preserves editorial integrity while enabling expert copywriting enhancement.

## Related Documentation

- **[ai_docs/suggest-edits-framework.md](./suggest-edits-framework.md)** - Core framework documentation
- **[README.md](../README.md)** - Project overview with skills section
- **[ai_docs/ameno-voice-style.md](./ameno-voice-style.md)** - Ameno voice full DNA

## Summary

The copywriting skills framework provides three specialized voices for strategic content enhancement:

- **Mad Men** drives immediate conversion through aggressive, pain-focused copy
- **Master** builds long-term persuasion through credibility and authority
- **Ameno** simplifies technical concepts through clarity and conversational honesty

All use suggest_edits pattern for editorial control. Run them after drafting, review suggestions, apply selectively, and maintain your voice while benefiting from expert copywriting principles.
