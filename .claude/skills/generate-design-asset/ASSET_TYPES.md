# Design Asset Types

Comprehensive specifications for all supported asset types in the generalized design asset generation system. Each asset type serves a specific purpose in blog content and has unique dimensional, stylistic, and integration requirements.

---

## Asset Type 1: Banner

### Description
Blog post header images that provide the first visual impression and set the tone for the entire article.

### Use Cases
- Primary header image for all blog posts
- Hero visual for article landing
- Social media preview image (when cropped/resized)
- Email newsletter headers

### Dimensions
- **Standard**: 2560x1440 pixels
- **Aspect Ratio**: 16:9 (landscape)
- **File Size Target**: < 500KB (optimized for web)

### Output Path Pattern
```
/public/assets/posts/{slug}-banner.png
```

**Example**: `/public/assets/posts/prompts-are-the-new-code-banner.png`

### Integration Notes
**Astro/Markdown**:
```astro
---
banner: "/assets/posts/prompts-are-the-new-code-banner.png"
---
```

**Direct Markdown**:
```markdown
![Banner](/assets/posts/prompts-are-the-new-code-banner.png)
```

The post layout template automatically displays the banner from frontmatter metadata.

### Style Count
**5 Style Variants**:
1. Glass Object Technical
2. Simple Isometric Diagram
3. Technical Blueprint
4. Dramatic Announcement
5. Enhanced Glitch Corruption (universal fallback)

### Visual Examples Descriptions
- **Glass Object**: Transparent glass processor chip floating against dark background with cyan rim lighting
- **Isometric**: Three-stage workflow with glowing connections on dark grid
- **Blueprint**: Context window allocation diagram with cyan lines on navy, measurements visible
- **Dramatic**: Bold headline in sharp focus, dark blurred background, newspaper aesthetic
- **Glitch**: Abstract holographic corruption with magenta/cyan neon accents on black

---

## Asset Type 2: Callout

### Description
In-text visual highlights that draw attention to key insights, warnings, data points, or technical details within blog content. Smaller than banners but visually impactful for emphasizing critical information.

### Use Cases
- Highlighting key insights or takeaways
- Visual warning/caution indicators
- Showcasing important metrics or data within prose
- Drawing attention to technical gotchas
- Creating visual breaks in long text sections

### Dimensions
- **Standard Wide**: 1200x800 pixels (3:2 ratio)
- **Alternative**: 1600x900 pixels (16:9 ratio, cinematic)
- **Aspect Ratio**: 3:2 or 16:9 (landscape)
- **File Size Target**: < 300KB

### Output Path Pattern
```
/public/assets/posts/{slug}-callout-{identifier}.png
```

**Examples**:
- `/public/assets/posts/context-engineering-callout-insight-1.png`
- `/public/assets/posts/performance-guide-callout-warning-gotcha.png`
- `/public/assets/posts/benchmark-results-callout-data-95pct.png`

### Integration Notes
**Inline Markdown**:
```markdown
![Key Insight](/assets/posts/context-engineering-callout-insight-1.png)
```

**Enhanced Astro Callout Component** (future):
```astro
<Callout type="insight" image="/assets/posts/...-callout-insight-1.png">
Content here
</Callout>
```

Position callouts near the relevant text they emphasize.

### Style Count
**4 Style Variants**:
1. Insight Highlight (glowing card with key text)
2. Warning Alert (orange/red neon caution aesthetic)
3. Data Spotlight (metric/number with dramatic lighting)
4. Tech Detail (small technical object or abstract shape)

### Visual Examples Descriptions
- **Insight Highlight**: Glowing acid-green card with "KEY POINT" in neon, abstract background glow
- **Warning Alert**: Orange warning symbol with dramatic lighting, dark background, caution atmosphere
- **Data Spotlight**: Bold "95%" metric with cyan glow, dark dramatic background, minimal design
- **Tech Detail**: Small glass hexagon or abstract tech shape with rim lighting, suggests technical concept

---

## Asset Type 3: Divider

### Description
Section break graphics that create visual separation between major content sections, improving scannability and providing mental breaks for readers navigating long technical posts.

### Use Cases
- Separating major topic shifts in long articles
- Visual break before/after deep technical sections
- Marking transitions between conceptual and implementation content
- Creating rhythm in long-form posts
- Subtle branding reinforcement between sections

### Dimensions
- **Standard**: 2560x200 pixels (ultra-wide, thin strip)
- **Alternative**: 2560x300 pixels (slightly taller for more prominent breaks)
- **Aspect Ratio**: ~12.8:1 (ultra-wide horizontal)
- **File Size Target**: < 150KB

### Output Path Pattern
```
/public/assets/posts/{slug}-divider-{number}.png
```

**Examples**:
- `/public/assets/posts/long-form-article-divider-1.png`
- `/public/assets/posts/technical-guide-divider-section-2.png`

### Integration Notes
**Markdown** (simple insertion between sections):
```markdown
## Section 1 Content

Content here...

![Section Break](/assets/posts/long-form-article-divider-1.png)

## Section 2 Content

More content...
```

Use sparingly—1 divider per 3-4 major sections. Overuse reduces impact.

### Style Count
**3 Style Variants**:
1. Minimal Line (clean horizontal line with subtle neon glow)
2. Tech Pattern (geometric pattern strip: hexagons, circuits, nodes)
3. Glitch Break (horizontal glitch corruption effect)

### Visual Examples Descriptions
- **Minimal Line**: Thin cyan glowing line across dark background, clean and subtle
- **Tech Pattern**: Repeating hexagonal pattern in dim cyan, dark background, technical feel
- **Glitch Break**: Horizontal RGB separation effect with scanlines, tech-noir atmosphere

---

## Asset Type 4: Diagram

### Description
Simple 2-3 element technical representations for explaining concepts visually. Constrained by Nano Banana's limitations, these focus on abstract mood and simplified relationships rather than detailed technical accuracy.

### Use Cases
- Illustrating 2-element relationships (input → output)
- Showing 3-step processes (A → B → C)
- Abstract representation of systems/concepts
- Visual complement to complex explanations
- Creating memorable visual metaphors

### Dimensions
- **Standard**: 1920x1080 pixels (Full HD 16:9)
- **Alternative**: 2560x1440 pixels (2K 16:9, more detail)
- **Aspect Ratio**: 16:9 (landscape)
- **File Size Target**: < 400KB

### Output Path Pattern
```
/public/assets/posts/{slug}-diagram-{concept}.png
```

**Examples**:
- `/public/assets/posts/context-flow-diagram-input-output.png`
- `/public/assets/posts/agent-workflow-diagram-three-stage.png`

### Integration Notes
**Markdown**:
```markdown
The process works in three stages:

![Process Diagram](/assets/posts/agent-workflow-diagram-three-stage.png)

As shown above, each stage...
```

Position diagrams near the text explanation they support.

### Style Count
**3 Style Variants**:
1. Two-Element Flow (input → output with glowing connection)
2. Three-Element Process (A → B → C linear or triangular)
3. Abstract Representation (single element with atmospheric effects)

### Visual Examples Descriptions
- **Two-Element Flow**: Two glowing geometric shapes (cubes) connected by cyan energy stream, dark background
- **Three-Element Process**: Three hexagonal nodes arranged linearly with glowing connections, labels "INPUT", "PROCESS", "OUTPUT"
- **Abstract Representation**: Single holographic sphere with atmospheric glow suggesting a concept, no labels

### CRITICAL LIMITATIONS
⚠️ **Nano Banana Diagram Constraints**:
- **Maximum 2-3 elements** - Do not attempt 4+ element diagrams
- **Extremely limited text** - 1 word per element maximum, 3 words total
- **Simple geometric shapes only** - Cubes, spheres, hexagons, cylinders
- **Abstract over accurate** - Mood matters more than technical precision
- **No complex flowcharts** - Nano Banana will fail on intricate diagrams

---

## Asset Type 5: DataCard

### Description
Metric and statistic visualization cards for highlighting quantitative results, benchmarks, performance improvements, or key data points with dramatic visual impact.

### Use Cases
- Showcasing performance improvements (e.g., "36x faster")
- Highlighting cost savings or efficiency gains
- Presenting benchmark results visually
- Creating comparison cards (before vs after)
- Emphasizing key metrics in case studies

### Dimensions
- **Square**: 1200x1200 pixels (1:1 ratio)
- **Portrait**: 1200x1600 pixels (3:4 ratio, more vertical)
- **Aspect Ratio**: 1:1 (square) or 3:4 (portrait)
- **File Size Target**: < 350KB

### Output Path Pattern
```
/public/assets/posts/{slug}-datacard-{metric-identifier}.png
```

**Examples**:
- `/public/assets/posts/performance-analysis-datacard-36x-faster.png`
- `/public/assets/posts/cost-savings-datacard-comparison.png`
- `/public/assets/posts/optimization-datacard-95pct-improvement.png`

### Integration Notes
**Inline Markdown**:
```markdown
![Performance Improvement](/assets/posts/performance-analysis-datacard-36x-faster.png)
```

**Sidebar/Highlight** (future component):
```astro
<MetricCard image="/assets/posts/...-datacard-36x-faster.png" />
```

Can be used inline, in sidebars, or grouped for multi-metric presentations.

### Style Count
**3 Style Variants**:
1. Metric Hero (large number/percentage with dramatic lighting)
2. Comparison Card (two metrics side-by-side with visual contrast)
3. Progress Indicator (visual representation of improvement/change)

### Visual Examples Descriptions
- **Metric Hero**: Bold "36x" in giant neon text with dramatic spotlight, dark background, minimal design
- **Comparison Card**: Split-screen showing "3 hours" (orange) vs "5 minutes" (green), visual contrast
- **Progress Indicator**: Abstract bar or fill showing progression from 0% to 95%, glowing completion effect

---

## Decision Criteria for Choosing Asset Types

### When to Use Each Asset Type

| Scenario | Recommended Asset Type | Why |
|----------|------------------------|-----|
| Starting a new blog post | **Banner** | Every post needs a header visual |
| Emphasizing a key insight mid-post | **Callout** | Draws attention without breaking flow |
| Separating major topic transitions | **Divider** | Creates visual break, improves scannability |
| Explaining a simple 2-3 element concept | **Diagram** | Visual representation aids understanding |
| Highlighting quantitative results | **DataCard** | Numbers demand visual emphasis |
| Warning about edge case or gotcha | **Callout** (Warning Alert style) | Visual warning more impactful than text |
| Showing before/after comparison | **DataCard** (Comparison Card style) | Side-by-side visual comparison |
| Long article (5000+ words) | **Banner** + **Divider**(s) | Structure long content |
| Technical deep-dive with metrics | **Banner** + **DataCard**(s) | Combine header + metric highlights |
| Tutorial with steps | **Banner** + **Diagram**(s) | Visual process flow complements instructions |

### Asset Type Combinations for Comprehensive Posts

**Performance Analysis Post**:
- 1 Banner (blueprint style with metrics theme)
- 2-3 DataCards (key performance improvements)
- 1 Diagram (before/after workflow comparison)
- 1-2 Dividers (separating analysis sections)

**Architecture Explanation Post**:
- 1 Banner (glass object or isometric style)
- 1-2 Diagrams (simplified system representations)
- 1-2 Callouts (key architectural insights)
- 1-2 Dividers (section breaks)

**Provocative Opinion Post**:
- 1 Banner (dramatic style with bold headline)
- 2-3 Callouts (emphasizing controversial points)
- 0-1 Dividers (minimal, focus on flow)

**Tutorial/How-To Post**:
- 1 Banner (isometric or simple style)
- 2-4 Diagrams (step-by-step process flows)
- 1-2 Callouts (warnings or key tips)
- 0-1 DataCards (if showing measurable results)

---

## Asset Type Comparison Table

| Attribute | Banner | Callout | Divider | Diagram | DataCard |
|-----------|--------|---------|---------|---------|----------|
| **Width** | 2560px | 1200-1600px | 2560px | 1920-2560px | 1200px |
| **Height** | 1440px | 800-900px | 200-300px | 1080-1440px | 1200-1600px |
| **Aspect Ratio** | 16:9 | 3:2 or 16:9 | ~12:1 | 16:9 | 1:1 or 3:4 |
| **Placement** | Header | Inline | Between sections | Inline | Inline/Sidebar |
| **Text Allowed** | 1-3 words | 1-2 words | 0 words | 1-3 words | Numbers + 1-2 words |
| **Complexity** | Medium-High | Low-Medium | Low | Low (2-3 elements max) | Low-Medium |
| **Generation Time** | 45-60 sec | 30-45 sec | 20-30 sec | 30-45 sec | 30-45 sec |
| **Use Frequency** | 1 per post | 0-5 per post | 0-3 per post | 0-4 per post | 0-3 per post |
| **Style Variants** | 5 | 4 | 3 | 3 | 3 |

---

## Best Practices by Asset Type

### Banner Best Practices
- Always generate a banner for every post
- Choose style based on content category (see CONTENT_ASSET_MAP.md)
- Avoid text in banners when possible (Nano Banana spelling risk)
- Use dramatic lighting and dark backgrounds for ACIDBATH brand consistency
- Test banner visibility at different viewport sizes

### Callout Best Practices
- Use sparingly (2-5 per post maximum)
- Position near related text, not randomly
- Choose style based on content tone (insight vs warning vs data)
- Keep text to 1-2 words maximum
- Don't overuse—too many callouts reduce impact

### Divider Best Practices
- Use only for major topic shifts (not minor sub-sections)
- Spacing: 1 divider per 3-4 major sections minimum
- Choose minimal style for subtle breaks, tech pattern for prominent breaks
- Avoid using dividers in short posts (< 2000 words)
- Match divider color accent to section theme

### Diagram Best Practices
- **Simplicity is critical**: 2-3 elements maximum, never more
- Use abstract shapes, not literal representations
- One word per element only
- Complement diagrams with text explanations (don't rely on diagram alone)
- Test if concept can be explained with simpler visual before using

### DataCard Best Practices
- Reserve for important metrics only (not every number)
- Use comparison cards for before/after contexts
- Match color to metric meaning (green = improvement, orange = warning, cyan = neutral)
- Bold, large numbers work better than small detailed charts
- Group multiple datacards when presenting related metrics

---

## File Naming Conventions

### Banner
```
{slug}-banner.png
```

### Callout
```
{slug}-callout-{identifier}.png
```
**Identifier examples**: `insight-1`, `warning-gotcha`, `data-95pct`, `tech-detail`

### Divider
```
{slug}-divider-{number}.png
```
**Number**: Sequential (1, 2, 3...) based on order in post

### Diagram
```
{slug}-diagram-{concept}.png
```
**Concept examples**: `input-output`, `three-stage`, `workflow`, `abstract-flow`

### DataCard
```
{slug}-datacard-{metric-identifier}.png
```
**Metric identifier examples**: `36x-faster`, `comparison`, `95pct-improvement`, `cost-savings`

---

## Version History

- **v1.0** (2025-12-24): Initial asset type specifications with 5 types, comprehensive documentation, use cases, and best practices

