# Banner Style Library

Simplified banner style templates optimized for Nano Banana image generation. Focus on **abstract beauty** over technical accuracy. Banners are 2560x1440 pixels (16:9 aspect ratio) and serve as blog post header images.

---

## CRITICAL: Nano Banana Limitations

⚠️ **READ BEFORE COMPOSING ANY PROMPT**

1. **NO complex diagrams** - Nano Banana fails at interconnected flowcharts, pipelines, and multi-component architectures
2. **MINIMAL text** - Spelling errors are common. Use 1-3 words max, or avoid text entirely
3. **DARK MODE ONLY** - All ACIDBATH graphics use dark backgrounds (black, navy, charcoal)
4. **ABSTRACT > LITERAL** - Evoke the concept, don't diagram it
5. **SINGLE FOCAL POINT** - One main subject, not multiple connected elements

---

## Style 1: Glass Object Technical

### Description
Single photorealistic glass/crystal object floating against dark background. Represents sophistication and technical elegance through material rendering, NOT through complexity.

### Best Use Cases
- Architecture posts, framework explanations, system design
- Agent systems, SDK architecture, platform design
- Posts emphasizing technical sophistication and elegant solutions

### When to Use
**Content Indicators**:
- Category: "AI Engineering", "System Design"
- Tags: `architecture`, `framework`, `SDK`, `system design`, `infrastructure`
- Title keywords: "architecture", "framework", "system", "platform"
- Tone: Advanced, architectural, sophisticated

**Scoring**: +3 for AI Engineering category, +2 per architecture tag (max +6)

### Nano Banana Prompt Template

```
A photorealistic [TECHNICAL_OBJECT] rendered in clear, polished transparent glass or crystal material. The object has elegant dimensional depth with rounded chamfers and smooth curved surfaces creating dramatic refraction effects. Simple, recognizable geometric form—[SIMPLE_SHAPE_DESCRIPTION].

The object floats slightly tilted against a deep black background with subtle gradient to dark charcoal. Dramatic rim lighting from behind creates glowing cyan and magenta edge highlights. Soft purple ambient light fills the shadows.

Sharp specular highlights on glass edges. Visible light refraction and caustics beneath the object. Shallow depth of field keeps the glass object in razor-sharp focus while background fades to darkness.

Aesthetic: Minimalist, luxurious, high-end product photography. Tech-noir atmosphere.

Technical specifications: 2560x1440 resolution, 16:9 aspect ratio optimized for blog header display.
```

### Key Guidelines
- **ONE object only** - no multiple connected pieces
- **Simple shapes** - cube, sphere, hexagon, chip—instantly recognizable
- **Dark background** - deep black or charcoal, never light
- **Neon rim lighting** - cyan, magenta, purple edge glow
- **NO text or labels**

### Placeholder Variables
- `[TECHNICAL_OBJECT]`: Single object (e.g., "processor chip", "crystal cube", "hexagonal node", "glass orb", "AI agent processing unit", "API gateway server")
- `[SIMPLE_SHAPE_DESCRIPTION]`: Basic geometry (e.g., "a hexagonal chip with beveled edges", "a perfect sphere with internal glow", "modular processor chip with connection pathways", "rectangular server chassis with front panel details")

### Example Filled Prompts
See `EXAMPLES.md` Examples 1-2 for complete filled prompts.

---

## Style 2: Simple Isometric Diagram

### Description
Isometric technical diagrams with **3-4 elements maximum**. Clean, readable layouts without text labels. The diagram structure is real, just simplified.

### Best Use Cases
- Workflow/process posts
- How-to guides, tutorials
- System overviews showing clear flow

### When to Use
**Content Indicators**:
- Category: "AI Development", "Tutorial"
- Tags: `workflow`, `automation`, `process`, `sub-agents`, `pipeline`
- Title keywords: "workflow", "build", "using", "how to", "process"
- Tone: Instructional, process-oriented

**Scoring**: +3 for AI Development category, +2 per workflow tag (max +6)

### Nano Banana Prompt Template

```
Clean isometric technical diagram showing [SIMPLE_SYSTEM] against a dark charcoal background.

The diagram contains exactly [NUMBER] elements arranged in isometric 3D space:
- [ELEMENT_1]: [simple shape description] in [COLOR_1]
- [ELEMENT_2]: [simple shape description] in [COLOR_2]
- [ELEMENT_3]: [simple shape description] in [COLOR_3]

Elements are connected by [CONNECTION_STYLE] (glowing lines, light trails, or energy streams). Flow direction is [DIRECTION].

Style: Clean vector illustration with consistent line weights. Each element is a simple geometric solid (cubes, cylinders, hexagonal prisms). Subtle glow on edges.

Lighting: Soft ambient with neon accent highlights on element edges. Dark background with subtle grid pattern.

Optional labels: Each element may have a single short word (1-3 words total in image). Use ALL CAPS, simple words like [LABEL_WORDS]. Labels float near or on elements.

Technical specifications: 2560x1440 resolution, 16:9 aspect ratio optimized for blog header display.
```

### Key Guidelines
- **3-4 elements MAXIMUM** - not 5, not 6, exactly 3-4
- **Simple shapes only** - cubes, cylinders, hexagons
- **1-3 words total** - one simple word per element, ALL CAPS
- **Dark background** - charcoal or dark navy with subtle grid
- **Glowing connections** - light trails instead of arrows
- **Clear flow direction** - left-to-right or top-to-bottom

### Placeholder Variables
- `[SIMPLE_SYSTEM]`: What diagram represents (e.g., "a three-stage data pipeline", "input-process-output flow", "multi-agent research workflow")
- `[NUMBER]`: Exactly 3 or 4
- `[ELEMENT_1/2/3]`: Simple shapes (cube, cylinder, hexagon)
- `[COLOR_1/2/3]`: Distinct neon colors (cyan, magenta, green)
- `[CONNECTION_STYLE]`: How elements connect (glowing lines, energy streams)
- `[DIRECTION]`: Flow direction (left-to-right, top-to-bottom)
- `[LABEL_WORDS]`: Optional 1-3 simple words (e.g., "INPUT, WORK, OUTPUT" or "DATA, AGENT, RESULT")

### Example Filled Prompts
See `EXAMPLES.md` Examples 3-4 for complete filled prompts.

---

## Style 3: Technical Blueprint

### Description
Blueprint-style schematic with **ONE main element** and supporting grid. Real technical drawing aesthetic, just simplified to what Nano Banana can render accurately.

### Best Use Cases
- Performance analysis, benchmarks
- Technical deep-dives
- Data-driven content with metrics

### When to Use
**Content Indicators**:
- Category: "Technical Analysis", "Deep Dive"
- Tags: `performance`, `optimization`, `benchmark`, `cost`, `token`, `efficiency`
- Title: Contains numbers, metrics, percentages
- Tone: Technical, data-driven, quantitative

**Scoring**: +3 for Technical Analysis category, +2 per performance tag (max +6), +2 for data indicators in title

### Nano Banana Prompt Template

```
Technical blueprint schematic showing [MAIN_ELEMENT] in the center. Classic blueprint aesthetic with [LINE_COLOR] lines on deep navy blue background.

The main element is a [ELEMENT_DESCRIPTION]—rendered in clean wireframe style with precise geometric construction. The element is centered and occupies about 50% of the frame.

Background: Deep navy blue (#0a1628) with subtle engineering grid pattern. Major grid lines visible, minor grid lines faint. Vignette darkening at edges.

The schematic has bright glowing edges with subtle bloom effect. A few [ACCENT_COLOR] highlight points mark key areas of the element.

Optional: [2-3 simple geometric callout lines] pointing to parts of the main element, but NO text on them.

Atmosphere: Technical, precise, engineering. Professional schematic quality.

NO text, numbers, measurements, or readable annotations. Visual elements only.

Technical specifications: 2560x1440 resolution, 16:9 aspect ratio optimized for blog header display.
```

### Key Guidelines
- **ONE main element** - don't try to show a complex system
- **Classic blueprint colors** - cyan/white lines on navy blue
- **Grid background** - subtle engineering grid adds authenticity
- **NO text** - callout lines can point, but no labels
- **Wireframe style** - clean geometric construction

### Placeholder Variables
- `[MAIN_ELEMENT]`: What the blueprint shows (e.g., "a context window diagram", "a processor cross-section", "a data flow gauge", "large codebase performance comparison", "context window allocation breakdown")
- `[ELEMENT_DESCRIPTION]`: Shape details (e.g., "rectangular container with internal divisions", "circular gauge with segments", "split-screen comparison with timeline bars", "horizontal bar divided into sections")
- `[LINE_COLOR]`: Main lines (cyan, white, light blue)
- `[ACCENT_COLOR]`: Highlight points (orange, green, bright cyan)

### Example Filled Prompts
See `EXAMPLES.md` Examples 5-6 for complete filled prompts.

---

## Style 4: Dramatic Announcement

### Description
Dramatic "breaking news" atmosphere without actual newspaper—moody lighting, urgency, bold visual impact. No text to avoid Nano Banana spelling errors.

### Best Use Cases
- Provocative opinion pieces
- Paradigm shift announcements
- Controversial takes, bold claims

### When to Use
**Content Indicators**:
- Category: "Opinion", "Commentary"
- Tags: `opinion`, `paradigm`, `controversial`, `future`, `prediction`
- Title keywords: "wrong", "dead", "obsolete", "endgame"
- Tone: Provocative, polarizing

**Scoring**: +3 for Opinion category, +2 per opinion tag (max +6), +2 for provocative keywords in title

### Nano Banana Prompt Template

```
Dramatic, moody photograph suggesting urgency and importance. [DRAMATIC_SUBJECT] captured in high-contrast lighting against deep black background.

The scene evokes "breaking news" atmosphere without any visible text. Strong chiaroscuro lighting—bright highlights against deep shadows. Single light source from [LIGHT_DIRECTION] creates dramatic modeling.

Subject: [SUBJECT_DESCRIPTION]. Rendered with photorealistic detail. The composition suggests something significant is happening or being revealed.

Color grading: Desaturated with [ACCENT_COLOR] tint. Dark, serious mood. Film noir aesthetic meets tech photography.

Background: Pure black or very dark charcoal. No distractions. All focus on the dramatic subject.

Atmosphere: Urgent, important, paradigm-shifting. The image itself makes a statement through visual impact, not through text.

NO text, headlines, or words visible anywhere in the image.

Technical specifications: 2560x1440 resolution, 16:9 aspect ratio optimized for blog header display.
```

### Key Guidelines
- **ABSOLUTELY NO TEXT** - this is critical for this style
- **Dramatic lighting** - high contrast, single source, film noir
- **Dark background** - black or near-black
- **Single subject** - one focal point
- **Mood over message** - the atmosphere carries the meaning

### Placeholder Variables
- `[DRAMATIC_SUBJECT]`: Main visual (e.g., "hands on keyboard in shadow", "glowing screen in darkness", "silhouette of figure against bright light", "engineer at terminal typing prompts", "terminal screen displaying natural language")
- `[SUBJECT_DESCRIPTION]`: Details of the subject
- `[LIGHT_DIRECTION]`: Where light comes from (upper-left, behind, etc.)
- `[ACCENT_COLOR]`: Color tint (cool blue, warm orange, neutral)

### Example Filled Prompts
See `EXAMPLES.md` Examples 7-8 for complete filled prompts.

---

## Style 5: Enhanced Glitch Corruption (Default/Fallback)

### Description
The signature ACIDBATH style. Digital glitch art with holographic effects and neon accents. Universal style that works for any content type. This is the default when other styles don't clearly fit.

### Best Use Cases
- Universal fallback for any post
- Technology, AI, digital topics
- When you want visual impact without specific conceptual ties
- When content type is unclear

### When to Use
**Content Indicators**:
- No clear category match
- Generic AI/tech topics
- Debugging, troubleshooting posts
- When other styles score low

**Scoring**: Baseline +1 (universal fallback)

### Nano Banana Prompt Template

```
Digital glitch art composition featuring [ABSTRACT_SUBJECT] with holographic corruption effects. Dark tech-noir aesthetic.

The image shows [SIMPLE_FOCAL_ELEMENT] with visible digital corruption: RGB channel separation creating cyan/magenta edge fringing, horizontal scanline artifacts, and subtle pixelation zones. Holographic shimmer on surfaces creates iridescent rainbow reflections.

Background: Deep black gradient with atmospheric depth fog. Subtle particle effects floating in space.

Lighting: [PRIMARY_COLOR] and [SECONDARY_COLOR] neon glow emanating from corrupted edges. Chromatic aberration at image borders. Subtle bloom on bright elements.

Color palette: [PRIMARY_COLOR] as main accent, [SECONDARY_COLOR] for contrast, holographic rainbow shimmer, deep black background.

Aesthetic: Cyberpunk, tech-noir, digital dystopia. Bold and visually striking.

NO text or readable words—pure visual abstraction with glitch effects.

Technical specifications: 2560x1440 resolution, 16:9 aspect ratio optimized for blog header display.
```

### Key Guidelines
- **NO text** - glitch text looks terrible
- **Simple subject** - one abstract focal point
- **Dark background** - pure black or near-black
- **Neon accents** - cyan, magenta, purple glow
- **Moderate corruption** - visible but not overwhelming
- **Always works** - this is the safe fallback style

### Placeholder Variables
- `[ABSTRACT_SUBJECT]`: What the image suggests (e.g., "digital consciousness", "data stream", "corrupted interface", "corrupted debugging interface", "glitching neural network")
- `[SIMPLE_FOCAL_ELEMENT]`: Main visual (e.g., "a glowing geometric shape", "abstract holographic sphere", "neon wireframe structure", "debugging interface panel", "error log display")
- `[PRIMARY_COLOR]`: Main neon (cyan, magenta, electric blue, purple)
- `[SECONDARY_COLOR]`: Contrast accent (purple, orange, green, magenta)

### Example Filled Prompts
See `EXAMPLES.md` Examples 9-10 for complete filled prompts.

---

## Quick Reference

### Style Selection Decision Tree

```
Is it an architecture/framework post? → Glass Object Technical
Is it a workflow/process post? → Simple Isometric Diagram
Does it have heavy metrics/benchmarks? → Technical Blueprint
Is it provocative/controversial? → Dramatic Announcement
Unclear or general tech content? → Enhanced Glitch Corruption
```

### Style Comparison Table

| Style | Complexity | Text Allowed | Best For | Color Scheme |
|-------|-----------|--------------|----------|--------------|
| Glass Object | Low (1 object) | NO | Architecture, frameworks | Cyan/magenta rim lighting |
| Isometric | Medium (3-4 elements) | 1-3 words | Workflows, processes | Multi-color neon elements |
| Blueprint | Low (1 element) | NO | Performance, benchmarks | Cyan on navy blue |
| Dramatic | Low (1 subject) | NO | Provocative opinions | High-contrast B&W or tinted |
| Glitch | Low (1 abstract) | NO | Universal fallback | Cyan/magenta/purple neon |

### ACIDBATH Color Palette

**Neon Accents** (on dark backgrounds):
- Cyan `#00ffff`
- Magenta `#ff00ff`
- Electric Blue `#0066ff`
- Purple `#9933ff`
- Acid Green `#39ff14`
- Orange `#ff6600` (for warnings)

**Backgrounds**:
- Pure Black `#000000`
- Charcoal `#1a1a1a`
- Deep Navy `#0a1628`

### Universal Prompt Checklist

Before generating banners:
- [ ] Dark background specified (black/navy/charcoal)
- [ ] Single focal subject (not multiple connected pieces unless isometric)
- [ ] Minimal or NO text
- [ ] Neon accent colors defined
- [ ] "2560x1440 resolution, 16:9 aspect ratio" included

### If Generation Fails

1. **Simplify** - Remove complexity, keep one focal element
2. **Remove text** - Any text will have errors
3. **Go abstract** - Don't try to literally depict concepts
4. **Use Glitch style** - It always works as fallback

---

## Troubleshooting Common Issues

### Issue: Generated banner doesn't match expectations
**Solutions**:
- Use `--preview-only` flag to review composed prompt before generation
- Try different style that may better suit content
- Manually edit prompt to adjust specific details
- Simplify the concept—less is more with Nano Banana

### Issue: Text is misspelled or unreadable
**Expected**: Nano Banana has spelling limitations
**Solutions**:
- Avoid text entirely (best practice)
- Use only 1-3 simple, short words in ALL CAPS
- Choose styles that don't require text (Glass Object, Blueprint, Glitch)

### Issue: Complex diagram came out as mess
**Expected**: Nano Banana cannot handle complex diagrams
**Solutions**:
- Use Isometric style with maximum 3-4 elements
- Or switch to Abstract Representation with single element
- Embrace abstract mood over technical accuracy

### Issue: Banner is too light/bright
**Root Cause**: Didn't specify dark background
**Solution**: Always include "deep black background" or "dark navy background" in prompt

---

## Version History

- **v2.1** (2025-12-24): Migrated to generalized design asset system as Banner asset type
- **v2.0** (2025-12-23): Simplified for Nano Banana limitations—dark mode only, no complex diagrams, minimal text
- **v1.0** (2025-12-23): Initial library
