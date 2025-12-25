# Divider Style Library

Style templates for divider assets—section break graphics that create visual separation between major content sections. Dividers are ultra-wide and thin (2560x200 or 2560x300 pixels) with **NO TEXT** as they serve purely decorative/structural purposes.

---

## CRITICAL: Divider-Specific Nano Banana Constraints

⚠️ **ULTRA-WIDE HORIZONTAL FORMAT**

1. **NO TEXT EVER** - Dividers are purely visual separators
2. **HORIZONTAL COMPOSITION** - Ultra-wide (2560px) and thin (200-300px)
3. **DARK MODE MANDATORY** - All dividers use dark backgrounds
4. **SIMPLE PATTERNS** - Repeating or flowing horizontal elements
5. **SUBTLE TO PROMINENT** - Range from minimal lines to bold patterns based on context

### Recommended Dimensions
- **Standard**: 2560x200 pixels (~12.8:1 ultra-wide)
- **Prominent**: 2560x300 pixels (for more visible breaks)

---

## Style 1: Minimal Line

### Description
Clean horizontal line with subtle neon glow. The most understated divider style—creates visual break without calling attention to itself. Perfect for maintaining flow while providing structure.

### Best Use Cases
- Subtle section breaks in long posts
- Professional, minimalist content
- When you want separation without disruption
- Technical posts emphasizing content over decoration

### When to Use
**Content Indicators**:
- Professional, technical tone
- Subtle topic transitions (related sections)
- Minimalist post aesthetic
- Clean, focused content

**Scoring**: Default +2, +2 for professional tone, +1 for subtle transitions

### Nano Banana Prompt Template

```
A minimalist horizontal divider line spanning the full width of the image. Ultra-wide format, very thin height.

The line: Single horizontal [LINE_COLOR] glowing line running left to right across center of frame. Line thickness: 2-4 pixels with soft glow/bloom extending upward and downward creating subtle atmosphere.

Background: Pure black (#000000) or deep charcoal (#1a1a1a). Gradient from darker at edges to slightly lighter at center (vignette reverse).

Lighting: Subtle [LINE_COLOR] glow emanating from the line. Soft bloom effect above and below. No harsh highlights—everything is smooth and minimal.

Line variations: Line can have very subtle wave or curve (gentle arc), but overall horizontal. Can fade slightly at very ends for elegance.

Aesthetic: Clean, professional, unobtrusive. "Less is more" philosophy. The line should separate sections without screaming for attention.

NO text, symbols, or decorative elements besides the line and its glow.

Technical specifications: 2560x200 pixels, ultra-wide aspect ratio (~12.8:1), optimized for section breaks.
```

### Key Guidelines
- **ONE line only** - no multiple lines or patterns
- **Subtle glow** - soft bloom, not harsh
- **Dark background** - pure black or charcoal
- **Minimal decoration** - the line is enough
- **NO text** - ever

### Placeholder Variables
- `[LINE_COLOR]`: Cyan (#00ffff), white (#ffffff), light cyan, or subtle color matching section theme
- Line can have subtle curve or be perfectly straight

### Example Contexts
- Between major sections in technical analysis
- Separating introduction from main content
- Before/after code examples in tutorial

---

## Style 2: Tech Pattern

### Description
Geometric pattern strip running horizontally—hexagons, circuits, nodes, or tech-inspired repeating elements. More prominent than minimal line, adds technical atmosphere while maintaining function as divider.

### Best Use Cases
- Technical deep-dives and architecture posts
- Prominently marking major topic shifts
- Reinforcing tech-noir brand aesthetic
- Posts with multiple distinct sections

### When to Use
**Content Indicators**:
- Deeply technical content
- Architecture or system design posts
- Major topic shifts between sections
- Posts emphasizing technical sophistication

**Scoring**: +2 for technical tone, +2 for architecture tags, +1 for major topic shifts

### Nano Banana Prompt Template

```
A horizontal strip of geometric technical patterns spanning full width. Ultra-wide format, moderate height.

The pattern: Repeating [PATTERN_TYPE] arranged horizontally across the strip. Pattern elements are simple geometric shapes (hexagons, circuit nodes, connected dots, geometric tiles) in [PRIMARY_COLOR] with subtle glow.

Pattern characteristics:
- Repeating or flowing pattern (not chaotic)
- Simple geometric elements only
- Consistent spacing and rhythm
- [PRIMARY_COLOR] glow on dark background
- Optional: Very subtle connection lines between elements

Background: Deep charcoal (#1a1a1a) or dark navy (#0a1628). Pattern sits in center band of frame.

Lighting: Soft [PRIMARY_COLOR] glow from pattern elements. Subtle bloom. Background darker at top and bottom edges (vignette) keeping focus on center pattern strip.

Aesthetic: Technical, systematic, architectural. Suggests infrastructure or underlying system. Pattern should feel organized and intentional, not random.

NO text, labels, or readable symbols. Pure geometric pattern.

Technical specifications: 2560x300 pixels (taller for pattern visibility), ultra-wide aspect ratio, optimized for section breaks.
```

### Key Guidelines
- **Repeating pattern** - systematic, not random
- **Simple geometric shapes** - hexagons, circuits, nodes, dots
- **Horizontal flow** - left-to-right rhythm
- **Dark background** - charcoal or navy
- **Moderate glow** - visible but not overwhelming
- **NO text** - geometric shapes only

### Placeholder Variables
- `[PATTERN_TYPE]`: "hexagonal tiles", "connected circuit nodes", "geometric grid cells", "dot matrix", "linked hexagons"
- `[PRIMARY_COLOR]`: Cyan (#00ffff), dim cyan, dark blue, purple based on section theme

### Example Contexts
- Transitioning from theory to implementation section
- Between major architectural components explanation
- Separating different system layers in deep-dive

---

## Style 3: Glitch Break

### Description
Horizontal glitch corruption effect—RGB separation, scanlines, digital disruption. Most prominent divider style. Creates strong visual break with edgy, digital aesthetic. Use sparingly for maximum impact.

### Best Use Cases
- Paradigm shifts in content
- Provocative or disruptive posts
- Major tonal shifts (e.g., problem → solution)
- Posts embracing glitch/cyberpunk aesthetic

### When to Use
**Content Indicators**:
- Disruptive, provocative tone
- Paradigm shift content
- Major conceptual transition
- Posts challenging status quo
- Edgy, modern aesthetic preference

**Scoring**: +2 for disruptive tone, +2 for paradigm shift, +1 for conceptual transitions

### Nano Banana Prompt Template

```
A horizontal glitch corruption effect strip spanning full width. Digital disruption aesthetic with RGB channel separation and scanline artifacts.

The glitch effect:
- Horizontal band of digital corruption running left-to-right
- RGB channel separation: cyan and magenta fringing offset horizontally
- Scanlines creating horizontal tear/displacement effect
- [GLITCH_INTENSITY] corruption level (moderate for readability, heavy for maximum impact)
- Color palette: Cyan (#00ffff) and magenta (#ff00ff) dominant with possible purple

Background: Deep black (#000000). Glitch effect concentrated in center horizontal band.

Corruption characteristics:
- Horizontal displacement (lines offset left/right randomly)
- RGB separation (red/green/blue channels misaligned)
- Scanline artifacts (horizontal lines of varying intensity)
- Subtle pixelation or mosaic zones
- Chromatic aberration

Aesthetic: Digital dystopia, cyberpunk disruption, "system breaking" feel. The corruption should suggest transition or shift—old section corrupting as new section begins.

NO text—corruption effects only.

Technical specifications: 2560x200 pixels, ultra-wide aspect ratio, optimized for dramatic section breaks.
```

### Key Guidelines
- **Horizontal corruption** - disruption flows left-to-right
- **Cyan/magenta dominant** - RGB separation colors
- **Moderate to heavy** - enough to be visible, not overwhelming
- **Dark background** - pure black
- **Scanline focus** - horizontal displacement primary effect
- **NO text** - glitch corruption only

### Placeholder Variables
- `[GLITCH_INTENSITY]`: "moderate" (still readable context) or "heavy" (maximum disruption)
- Corruption level adjustable based on how dramatic the section break should be

### Example Contexts
- Transitioning from "old approach" to "new approach"
- Paradigm shift moment in opinion piece
- Before revealing controversial take
- Between problem and solution sections

---

## Quick Reference

### Style Selection Decision Tree

```
Subtle transition between related sections? → Minimal Line
Major topic shift in technical content? → Tech Pattern
Paradigm shift or dramatic transition? → Glitch Break
Default/unsure? → Minimal Line (safest)
```

### Style Comparison Table

| Style | Prominence | Aesthetic | Best For | Color Scheme |
|-------|-----------|-----------|----------|--------------|
| Minimal Line | Low (subtle) | Professional, clean | Related section breaks | Single color glow |
| Tech Pattern | Medium (visible) | Technical, systematic | Major topic shifts | Geometric patterns |
| Glitch Break | High (dramatic) | Disruptive, cyberpunk | Paradigm shifts | Cyan/magenta glitch |

### Divider Usage Guidelines

**Frequency**:
- **Minimal Line**: Can use 3-5 per post (subtle, doesn't overwhelm)
- **Tech Pattern**: 1-3 per post (more prominent, use strategically)
- **Glitch Break**: 1-2 per post maximum (high impact, loses effect if overused)

**Spacing**:
- Minimum 3-4 paragraphs between dividers
- Use between major sections (H2 headings), not subsections
- Don't use dividers in short posts (< 2000 words)

### Color Matching by Section Theme

**Technical sections**: Cyan (#00ffff)
**Creative sections**: Magenta (#ff00ff), Purple (#9933ff)
**Warning sections**: Orange (#ff6600)
**Success sections**: Green (#4caf50), Acid-green (#39ff14)
**Neutral**: White (#ffffff), Light cyan

### Dimension Selection

**Standard (2560x200)**: Default for most dividers, subtle height
**Prominent (2560x300)**: When using Tech Pattern or Glitch Break for more visibility

### Universal Divider Checklist

Before generating dividers:
- [ ] Dark background (black or charcoal)
- [ ] Horizontal composition (left-to-right flow)
- [ ] NO text or labels
- [ ] Ultra-wide dimensions (2560px width)
- [ ] Thin height (200-300px)

---

## Integration Guidelines

### Placement Best Practices

```markdown
## Section 1 Content

Long content here...

![Section Break](/assets/posts/post-slug-divider-1.png)

## Section 2 Content

More content here...
```

**Spacing Rules**:
- Add blank line before divider image
- Add blank line after divider image
- Don't place dividers back-to-back
- Use between H2 sections, not H3 subsections

### Divider Naming Convention

```
{slug}-divider-{number}.png
```

**Sequential numbering**:
- `long-form-article-divider-1.png`
- `long-form-article-divider-2.png`
- `long-form-article-divider-3.png`

Or descriptive:
- `technical-guide-divider-section-2.png`
- `opinion-piece-divider-paradigm-shift.png`

---

## Common Failure Modes

### Issue: Divider not wide enough
**Root Cause**: Wrong dimensions specified
**Solution**: Always use 2560px width (match blog content width)

### Issue: Divider too tall, breaks flow
**Root Cause**: Used 400-500px height instead of 200-300px
**Solution**: Keep height 200-300px maximum—dividers should be thin

### Issue: Divider has text
**Expected**: This should never happen for dividers
**Solution**: Remove all text from prompts—dividers are decoration only

### Issue: Pattern too complex or chaotic
**Root Cause**: Tried too intricate pattern
**Solution**: Use simple repeating geometric shapes—hexagons, dots, simple circuits

---

## Troubleshooting

### Divider too subtle, almost invisible
- Switch from Minimal Line to Tech Pattern
- Increase glow intensity in prompt
- Use brighter color (cyan instead of dim blue)

### Divider too loud, distracts from content
- Switch from Glitch Break to Minimal Line
- Reduce glow intensity
- Use more subtle color (dim cyan, gray)

### Pattern looks messy or random
- Simplify pattern to basic geometric shapes
- Emphasize "repeating" and "systematic" in prompt
- Reduce number of pattern elements

### Glitch effect illegible or ugly
- Reduce glitch intensity from "heavy" to "moderate"
- Ensure horizontal-only disruption (not vertical chaos)
- Keep dark background for contrast

---

## Version History

- **v1.0** (2025-12-24): Initial divider style library with 3 variants optimized for ultra-wide format and ACIDBATH brand
