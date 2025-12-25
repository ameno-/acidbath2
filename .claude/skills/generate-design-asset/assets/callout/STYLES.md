# Callout Style Library

Style templates for callout assets—in-text visual highlights that emphasize key insights, warnings, data points, or technical details within blog content. Callouts are smaller than banners (1200x800 or 1600x900 pixels) and require **even stricter text limitations** due to smaller size.

---

## CRITICAL: Callout-Specific Nano Banana Constraints

⚠️ **STRICTER THAN BANNERS**

1. **TEXT LIMIT: 1-2 words MAXIMUM** - Smaller size amplifies spelling errors
2. **EVEN SIMPLER compositions** - Less space means less complexity
3. **DARK MODE MANDATORY** - All callouts use dark backgrounds
4. **SINGLE FOCAL POINT** - One visual element only
5. **HIGH CONTRAST** - Must be readable when embedded in blog text

### Recommended Dimensions
- **Standard Wide**: 1200x800 pixels (3:2 ratio)
- **Cinematic**: 1600x900 pixels (16:9 ratio)

---

## Style 1: Insight Highlight

### Description
Glowing card-style visual with key insight text or abstract representation. Emphasizes "aha moment" or important takeaway with dramatic neon glow and atmospheric effects.

### Best Use Cases
- Key insights or breakthrough realizations
- Important takeaways mid-article
- "This is the critical point" emphasis
- Success stories or achievements

### When to Use
**Content Indicators**:
- Text contains: "key insight", "takeaway", "important", "breakthrough", "discovery"
- Positive/success tone
- Mid-article emphasis needed
- Highlighting paradigm-shifting concept

**Scoring**: +3 for key insight context, +2 for positive tone, +1 for mid-article placement

### Nano Banana Prompt Template

```
A glowing card or panel floating in dark space, representing a key insight. The card has a simple geometric shape (rectangle with rounded corners or hexagon) and glows with [GLOW_COLOR] neon edges.

Center of card: [INSIGHT_VISUAL]—either abstract glow, simple icon shape, or 1-2 word text in bold sans-serif.

Background: Deep black (#000000) with subtle atmospheric glow radiating from the card. Depth fog creates layering effect.

Lighting: Bright [GLOW_COLOR] rim lighting around card edges. Soft bloom effect. Subtle particle shimmer floating around the card suggesting importance or energy.

Card surface: Dark [CARD_TONE] (charcoal, dark navy) with [GLOW_COLOR] highlights. Minimal, clean design.

Optional text (use sparingly): [INSIGHT_TEXT] in ALL CAPS, 1-2 words maximum, bold geometric sans-serif font. Position: centered or offset.

Aesthetic: Clean, modern, tech-inspired. "Lightbulb moment" visual without literal lightbulb.

Technical specifications: [DIMENSIONS] (1200x800 or 1600x900), landscape aspect ratio, optimized for inline blog use.
```

### Key Guidelines
- **1-2 words maximum** if using text
- **Simple card shape** - rectangle, hexagon, or rounded panel
- **Bright glow** - acid-green, cyan, or magenta
- **Dark background** - pure black for maximum contrast
- **Abstract over literal** - suggest insight, don't explain it

### Placeholder Variables
- `[GLOW_COLOR]`: Main neon accent (acid-green `#39ff14`, cyan, magenta)
- `[INSIGHT_VISUAL]`: What's on the card ("abstract glowing shape", "simple star icon", bold text "KEY POINT")
- `[CARD_TONE]`: Card surface color (charcoal, dark navy, deep gray)
- `[INSIGHT_TEXT]`: Optional 1-2 words ("KEY POINT", "BREAKTHROUGH", "AHA", "CRITICAL")
- `[DIMENSIONS]`: 1200x800 or 1600x900 based on preference

### Example Contexts
- "The key insight: agents should research, not implement"
- "This breakthrough reduced costs by 95%"
- "Critical understanding: context is everything"

---

## Style 2: Warning Alert

### Description
Orange/red neon warning graphic with caution aesthetic. Creates visual urgency for gotchas, edge cases, or common mistakes that readers must avoid.

### Best Use Cases
- Warning about gotchas or edge cases
- Common mistakes to avoid
- Performance pitfalls
- Security concerns
- "Don't do this" cautions

### When to Use
**Content Indicators**:
- Text contains: "warning", "gotcha", "edge case", "avoid", "mistake", "problem"
- Caution/warning tone
- Before risky or error-prone section
- Highlighting failure modes

**Scoring**: +3 for warning context, +2 for caution tone, +1 for pre-risky-section placement

### Nano Banana Prompt Template

```
A warning alert visual with strong orange and red neon accents on dark background. The composition suggests caution and urgency without literal warning symbols.

Central element: [WARNING_VISUAL]—simple geometric shape or abstract form glowing with intense orange (#ff6600) and red (#ff0000) neon. The form suggests alert/danger through color and glow intensity.

Background: Deep black with subtle red/orange atmospheric haze creating tension. Vignette darkening at edges focuses attention on warning element.

Lighting: Harsh orange/red rim lighting with strong bloom effect. Glitch scanlines or distortion effects add urgency. Chromatic aberration with red/orange fringing.

Optional text (use sparingly): [WARNING_TEXT] in ALL CAPS, 1-2 words maximum. "CAUTION", "WARNING", "GOTCHA", or "AVOID". Bold sans-serif, orange glow.

Visual cues: Sharp edges, angular shapes, high contrast. The image should feel urgent and attention-grabbing.

Aesthetic: Dangerous, urgent, "pay attention now" energy. Tech warning interface without literal UI elements.

Technical specifications: [DIMENSIONS] (1200x800 or 1600x900), landscape aspect ratio, optimized for inline blog use.
```

### Key Guidelines
- **Orange/red color scheme** - warning colors
- **High contrast** - must grab attention
- **Angular shapes** - sharp, urgent feel
- **Strong glow** - intense bloom effect
- **1-2 words max** if using text

### Placeholder Variables
- `[WARNING_VISUAL]`: Central warning element ("angular geometric shape with red glow", "abstract hazard form", "glowing exclamation composition")
- `[WARNING_TEXT]`: Optional 1-2 words ("WARNING", "CAUTION", "GOTCHA", "AVOID", "DANGER")
- `[DIMENSIONS]`: 1200x800 or 1600x900

### Example Contexts
- "Gotcha: This approach causes N+1 queries"
- "Warning: Improper configuration breaks production"
- "Avoid this common mistake that wastes tokens"

---

## Style 3: Data Spotlight

### Description
Metric/number visualization with dramatic lighting. Highlights quantitative results, percentages, or key measurements with bold visual emphasis.

### Best Use Cases
- Showcasing specific metrics inline
- Performance improvements
- Cost savings or efficiency gains
- Percentages or multipliers
- "The number says it all" moments

### When to Use
**Content Indicators**:
- Text contains specific metric, number, percentage
- Quantitative tone
- After benchmark or test results
- Emphasizing data-driven conclusion

**Scoring**: +3 for metric presence, +2 for quantitative tone, +1 for post-benchmark placement

### Nano Banana Prompt Template

```
A bold, dramatic number or metric visualization on dark background. The number/metric is the hero of the composition with theatrical lighting.

Central element: [METRIC_VALUE] rendered large and prominent. The number can be displayed as glowing text or represented through abstract visual metaphor (progress bar, gauge, or geometric representation).

Number rendering (if using text): Bold sans-serif font, huge size occupying 60-70% of frame. [NUMBER_COLOR] neon glow with strong bloom. Numbers are clearer than words for Nano Banana.

Background: Pure black (#000000) or deep charcoal with dramatic spotlight effect. Single light source creates high contrast.

Lighting: Dramatic key light from [LIGHT_DIRECTION] creating rim lighting on number. Strong [NUMBER_COLOR] glow. Volumetric light rays optional for extra drama.

Optional context text: [METRIC_CONTEXT] in smaller text (1 word, e.g., "FASTER", "SAVED", "IMPROVED"). Position: below or beside main metric.

Aesthetic: Bold, confident, data-driven. "The numbers don't lie" visual impact.

Technical specifications: [DIMENSIONS] (1200x800 or 1600x900), landscape aspect ratio, optimized for inline blog use.
```

### Key Guidelines
- **Numbers preferred over words** - Nano Banana handles digits better
- **Large and bold** - metric is the star
- **Dramatic lighting** - theatrical spotlight
- **Success color coding** - green for improvements, cyan for neutral, orange for warnings
- **Minimal supporting text** - 1 word maximum for context

### Placeholder Variables
- `[METRIC_VALUE]`: The number ("95%", "36x", "10K", "$4.2K", "2.5s")
- `[NUMBER_COLOR]`: Success green (#4caf50), cyan (#00ffff), or orange (#ff6600) based on context
- `[LIGHT_DIRECTION]`: Spotlight direction (upper-left, behind, upper-right)
- `[METRIC_CONTEXT]`: Optional 1-word context ("FASTER", "SAVED", "REDUCED", "IMPROVED")
- `[DIMENSIONS]`: 1200x800 or 1600x900

### Example Contexts
- "Performance improved by 95%"
- "36x faster than previous approach"
- "Saved $4,200 in monthly costs"

---

## Style 4: Tech Detail

### Description
Small technical object or abstract shape representing a specific concept or system component. Minimal, focused, sophisticated visual for explaining technical details.

### Best Use Cases
- Explaining specific technical concept
- Representing system component
- Visualizing abstract idea
- Complementing code examples
- "Here's what this looks like" moments

### When to Use
**Content Indicators**:
- Text explains technical concept or system component
- Technical jargon present
- Architectural or implementation details
- Need visual metaphor for abstract concept

**Scoring**: +3 for technical concept, +2 for technical tone, +1 for component explanation

### Nano Banana Prompt Template

```
A single technical object or abstract geometric shape floating against dark background, representing [CONCEPT_NAME].

The object: [OBJECT_DESCRIPTION]—simple, clean geometric form. Can be glass/crystal material (sophistication), holographic (futuristic), or solid with neon edges (modern tech).

Object characteristics:
- Simple recognizable shape (cube, hexagon, chip, orb, cylinder)
- [MATERIAL_STYLE] rendering (glass, holographic, matte with glow)
- [ACCENT_COLOR] highlights or edge lighting
- Minimal detail—suggestion over accuracy

Background: Deep black or dark charcoal (#1a1a1a). Minimal atmospheric effects to keep focus on object.

Lighting: Clean rim lighting emphasizing object form. Subtle [ACCENT_COLOR] glow. Professional product photography aesthetic.

NO text or labels—the object itself communicates the concept through form and material.

Aesthetic: Technical, clean, sophisticated. "This is the thing" clarity without complexity.

Technical specifications: [DIMENSIONS] (1200x800 or 1600x900), landscape aspect ratio, optimized for inline blog use.
```

### Key Guidelines
- **ONE simple object** - no complex assemblies
- **NO text** - pure visual representation
- **Clean and minimal** - avoid clutter
- **Material sophistication** - glass, holographic, or glowing matte
- **Abstract metaphor** - represent, don't diagram

### Placeholder Variables
- `[CONCEPT_NAME]`: What it represents ("context window", "API endpoint", "data node", "agent processor")
- `[OBJECT_DESCRIPTION]`: Shape details ("hexagonal chip with beveled edges", "glass cube with internal glow", "holographic sphere with surface shimmer")
- `[MATERIAL_STYLE]`: Rendering approach ("transparent glass", "holographic", "matte black with cyan edges")
- `[ACCENT_COLOR]`: Edge/glow color (cyan, magenta, acid-green, purple)
- `[DIMENSIONS]`: 1200x800 or 1600x900

### Example Contexts
- "A context window allocates memory like this"
- "API endpoints function as gateways"
- "Agents process information through modules"

---

## Quick Reference

### Style Selection Decision Tree

```
Emphasizing key insight or takeaway? → Insight Highlight
Warning about gotcha or mistake? → Warning Alert
Showcasing specific metric or number? → Data Spotlight
Explaining technical concept or component? → Tech Detail
```

### Style Comparison Table

| Style | Primary Color | Text Allowed | Mood | Best For |
|-------|--------------|--------------|------|----------|
| Insight Highlight | Acid-green/Cyan | 1-2 words | Positive, enlightening | Breakthroughs, key points |
| Warning Alert | Orange/Red | 1-2 words | Urgent, cautious | Gotchas, mistakes to avoid |
| Data Spotlight | Green/Cyan/Orange | Numbers + 1 word | Confident, data-driven | Metrics, performance data |
| Tech Detail | Cyan/Magenta/Purple | NO text | Clean, sophisticated | Concepts, components |

### Callout Color Coding

**By Purpose**:
- **Insight/Success**: Acid-green (#39ff14), Cyan (#00ffff)
- **Warning/Caution**: Orange (#ff6600), Red (#ff0000)
- **Data/Neutral**: Cyan (#00ffff), Purple (#9933ff)
- **Technical**: Cyan (#00ffff), Magenta (#ff00ff)

### Dimension Recommendations

**Standard Wide (1200x800)**: Default for most callouts, good balance
**Cinematic (1600x900)**: When more horizontal space needed, dramatic feel

### Text Guidelines for Callouts

**ABSOLUTE MAXIMUM**: 2 words
**RECOMMENDED**: 1 word or NO text
**SAFE WORDS**: Short, simple, common (all caps)
- Numbers: Always safer than words
- Examples: "WARNING", "KEY", "95%", "10x", "FASTER"

### Universal Callout Checklist

Before generating callouts:
- [ ] Dark background (black or charcoal)
- [ ] Single focal element (one object, card, or number)
- [ ] 0-2 words maximum for text
- [ ] Appropriate color for purpose (green=insight, orange=warning, cyan=data)
- [ ] Dimensions specified (1200x800 or 1600x900)

---

## Integration Guidelines

### Placement Best Practices
- **Position near related text** - Don't insert callouts randomly
- **Use sparingly** - 2-5 callouts per post maximum
- **Vary styles** - Don't use same style repeatedly
- **Space appropriately** - Give callouts breathing room

### Markdown Integration

```markdown
## Section with Key Insight

Important concept explained here...

![Key Insight](/assets/posts/post-slug-callout-insight-1.png)

Concept continues after visual emphasis...
```

### Callout Naming Convention

```
{slug}-callout-{identifier}.png
```

**Identifier examples**:
- `insight-1`, `insight-breakthrough`
- `warning-gotcha`, `warning-n-plus-1`
- `data-95pct`, `data-performance`
- `tech-detail`, `tech-context-window`

---

## Common Failure Modes

### Issue: Text is unreadable or misspelled
**Expected**: Smaller callout size makes spelling errors worse
**Solution**: Use NO text, or numbers only, or absolute simplest 1-word labels

### Issue: Callout too complex
**Root Cause**: Tried to fit too much information
**Solution**: One concept per callout; make multiple callouts if needed

### Issue: Low contrast, hard to see when embedded
**Root Cause**: Background too bright or colors too muted
**Solution**: Always use pure black background, bright neon accents

### Issue: Callout doesn't match blog aesthetic
**Root Cause**: Used light colors or wrong color scheme
**Solution**: Follow ACIDBATH palette—dark backgrounds, neon accents only

---

## Troubleshooting

### Callout doesn't emphasize the right thing
- Simplify visual to single focal point
- Use color coding (green=good, orange=warning)
- Try different style variant

### Generated callout looks like banner
- Check dimensions—callouts are smaller (1200x800 not 2560x1440)
- Simplify composition even further
- Use tighter framing, less negative space

### Text completely illegible
- **Remove all text** - this is the safest approach
- If must have text: use numbers instead of words
- Keep to 1 simple word maximum

---

## Version History

- **v1.0** (2025-12-24): Initial callout style library with 4 variants optimized for Nano Banana constraints and ACIDBATH brand
