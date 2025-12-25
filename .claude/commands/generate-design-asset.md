---
allowed-tools: Skill
description: Generate design assets (banners, callouts, dividers, diagrams, datacards) for blog posts using content-aware style recommendations
---

# Generate Design Asset Command

Generate high-quality, content-aware design assets for ACIDBATH blog posts using the generalized design asset generation skill.

## Usage

```bash
/generate-design-asset [options] [content-description]
```

## Asset Types

This command generates 5 types of visual assets:

1. **Banner** - Blog post header images (2560x1440, 16:9)
2. **Callout** - In-text visual highlights (1200x800 or 1600x900)
3. **Divider** - Section break graphics (2560x200 or 2560x300, ultra-wide)
4. **Diagram** - Simple 2-3 element technical representations (1920x1080 or 2560x1440)
5. **DataCard** - Metric/statistic visualization cards (1200x1200 or 1200x1600, square/portrait)

## Quick Start Examples

### Generate Banner for New Post

```bash
# Using post metadata (recommended)
/generate-design-asset --asset-type banner --slug prompts-are-the-new-code

# Manual with title
/generate-design-asset --asset-type banner "The Agent Endgame"

# With specific style
/generate-design-asset --asset-type banner --style glass_object "API Gateway Architecture"
```

### Generate Callout for Key Insight

```bash
# Insight highlight
/generate-design-asset --asset-type callout "Custom agents scale"

# Warning callout
/generate-design-asset --asset-type callout --style warning_alert "N+1 query gotcha"

# Data callout
/generate-design-asset --asset-type callout --style data_spotlight "95% faster"
```

### Generate Section Divider

```bash
# Minimal divider
/generate-design-asset --asset-type divider

# Tech pattern divider for architecture post
/generate-design-asset --asset-type divider --style tech_pattern

# Glitch break for paradigm shift
/generate-design-asset --asset-type divider --style glitch_break
```

### Generate Simple Diagram

```bash
# Two-element flow
/generate-design-asset --asset-type diagram "Input to Output"

# Three-element process
/generate-design-asset --asset-type diagram --style three_element_process "Data pipeline"
```

### Generate Metric DataCard

```bash
# Performance metric
/generate-design-asset --asset-type datacard "36x faster"

# Cost savings
/generate-design-asset --asset-type datacard "Saved $4.2K"

# Comparison
/generate-design-asset --asset-type datacard --style comparison_card "Before vs After"
```

## Command-Line Flags

### Asset Type Selection

`--asset-type [type]`
- **Values**: `banner`, `callout`, `divider`, `diagram`, `datacard`
- **Usage**: Skip interactive asset type selection
- **Example**: `--asset-type callout`

### Style Override

`--style [style-name]`
- **Values**: Depends on asset type (see style libraries)
- **Usage**: Skip style recommendation, use specified style
- **Example**: `--style glass_object`

### Automation

`--auto`
- **Usage**: Auto-accept primary recommendation without interaction
- **Use Case**: Batch processing, scripts
- **Example**: `--slug post-slug --auto`

### Preview Mode

`--preview-only`
- **Usage**: Show composed prompt without generating image
- **Use Case**: Review prompt quality, debugging, learning
- **Example**: `--asset-type banner "Title" --preview-only`

### Metadata Loading

`--slug [post-slug]`
- **Usage**: Load post metadata from slug
- **Requires**: Metadata file at `blog/posts/[slug]/metadata.json`
- **Example**: `--slug context-window-bleeding`

`--metadata [path]`
- **Usage**: Load metadata from custom path
- **Example**: `--metadata /path/to/metadata.json`

## Available Styles by Asset Type

### Banner Styles
1. `glass_object` - Glass Object Technical (architecture, frameworks)
2. `isometric` - Simple Isometric Diagram (workflows, processes)
3. `blueprint` - Technical Blueprint (performance, benchmarks)
4. `dramatic` - Dramatic Announcement (provocative opinions)
5. `glitch` - Enhanced Glitch Corruption (universal fallback)

### Callout Styles
1. `insight_highlight` - Glowing card with key insight
2. `warning_alert` - Orange/red caution aesthetic
3. `data_spotlight` - Metric with dramatic lighting
4. `tech_detail` - Technical object/concept representation

### Divider Styles
1. `minimal_line` - Clean horizontal line with subtle glow
2. `tech_pattern` - Geometric pattern strip
3. `glitch_break` - Horizontal glitch corruption

### Diagram Styles
1. `two_element_flow` - Input→Output (2 elements)
2. `three_element_process` - A→B→C flow (3 elements)
3. `abstract_representation` - Single element metaphor

### DataCard Styles
1. `metric_hero` - Large number with dramatic lighting
2. `comparison_card` - Side-by-side before/after
3. `progress_indicator` - Visual progress/completion bar

## Workflow

When invoked, the skill:

1. **Selects Asset Type** - Based on flag or interactive menu
2. **Analyzes Content** - Extracts metadata, tags, tone from input
3. **Recommends Styles** - Applies content-to-style mapping rules
4. **Presents Options** - Shows 3 style recommendations
5. **Composes Prompt** - Fills style template with content variables
6. **Generates Asset** - Calls OpenRouter (Nano Banana) to create image
7. **Verifies Output** - Confirms file creation, offers regeneration
8. **Provides Integration** - Shows file path and usage markdown

## Output Paths

Assets are saved to:

```
/public/assets/posts/{slug}-{asset-type}-{identifier}.png
```

**Examples**:
- `/public/assets/posts/prompts-are-the-new-code-banner.png`
- `/public/assets/posts/context-engineering-callout-insight-1.png`
- `/public/assets/posts/long-article-divider-1.png`
- `/public/assets/posts/workflow-diagram-three-stage.png`
- `/public/assets/posts/performance-datacard-36x.png`

## Integration in Blog Posts

### Banner
```astro
---
banner: "/assets/posts/post-slug-banner.png"
---
```

### Callout/DataCard/Diagram (Inline)
```markdown
![Key Insight](/assets/posts/post-slug-callout-insight-1.png)
```

### Divider (Between Sections)
```markdown
## Section 1

Content...

![Section Break](/assets/posts/post-slug-divider-1.png)

## Section 2
```

## Best Practices

### Asset Usage Guidelines

**Banners**: 1 per post (required for all posts)
**Callouts**: 0-5 per post (use sparingly for emphasis)
**Dividers**: 0-3 per post (major section breaks only, posts >2000 words)
**Diagrams**: 0-4 per post (when visual aids comprehension)
**DataCards**: 0-3 per post (for important metrics only)

### When to Use Each Asset Type

| Scenario | Asset Type | Why |
|----------|-----------|-----|
| New blog post | Banner | Every post needs header |
| Key insight mid-article | Callout (insight) | Draw attention without breaking flow |
| Warning about gotcha | Callout (warning) | Visual urgency |
| Impressive metric | DataCard | Numbers demand visual emphasis |
| Simple 2-3 step process | Diagram | Visual aids understanding |
| Long post section break | Divider | Improve scannability |

### Content-Aware Recommendations

The skill analyzes your content and recommends appropriate:
- Asset types (based on content structure and needs)
- Styles within each asset type (based on category, tags, tone)

**Example**: For a post about "55,000 Files in 5 Minutes":
- **Banner**: Technical Blueprint (performance/metrics focus)
- **DataCard**: Metric Hero (showcasing "55,000" and "5 min")
- **Divider**: Tech Pattern (technical content structure)

## Troubleshooting

### Issue: Style recommendation doesn't match content
**Solution**: Override with `--style [name]` or provide more detailed metadata

### Issue: Generated asset doesn't match expectations
**Solutions**:
1. Use `--preview-only` to review prompt first
2. Try different style variant
3. Manually edit prompt before generation
4. Simplify concept (especially for diagrams)

### Issue: Text is misspelled or unreadable
**Expected**: Nano Banana has text limitations
**Solutions**:
- Avoid text entirely (best practice for most assets)
- Use numbers instead of words (safer for DataCards)
- Use only 1-3 simple words maximum
- Choose styles that minimize text dependency

### Issue: Diagram too complex
**Expected**: Nano Banana limited to 2-3 elements
**Solutions**:
- Use Abstract Representation style (single element metaphor)
- Break into multiple simple diagrams
- Use Callout (Tech Detail) instead for single concept

### Issue: Asset dimensions not suitable
**Solution**: Check ASSET_TYPES.md for specifications, some types support custom dimensions

## Requirements

- **OpenRouter API Key**: `OPENROUTER_API_KEY` environment variable must be set
- **adws/adw_modules/openrouter_image.py**: Image generation module (already implemented)

Setup:
```bash
export OPENROUTER_API_KEY="your-key-here"
```

Add to `~/.zshrc` for persistence.

## Advanced Usage

### Batch Generation

Generate multiple assets for comprehensive post:

```bash
# Generate banner
/generate-design-asset --slug post-slug --asset-type banner --auto

# Generate callout for key insight
/generate-design-asset --asset-type callout "Key insight text"

# Generate datacard for metric
/generate-design-asset --asset-type datacard "95% improvement"

# Generate dividers (2x)
/generate-design-asset --asset-type divider --style minimal_line
/generate-design-asset --asset-type divider --style tech_pattern
```

### Preview Before Generating

Always preview complex prompts:

```bash
/generate-design-asset --asset-type diagram "Complex system" --preview-only
# Review prompt, then:
/generate-design-asset --asset-type diagram "Complex system" --style abstract_representation
```

## Related Documentation

- **Skill Documentation**: `.claude/skills/generate-design-asset/SKILL.md`
- **Asset Type Specs**: `.claude/skills/generate-design-asset/ASSET_TYPES.md`
- **Mapping Rules**: `.claude/skills/generate-design-asset/CONTENT_ASSET_MAP.md`
- **Style Libraries**: `.claude/skills/generate-design-asset/assets/{type}/STYLES.md`
- **Examples**: `.claude/skills/generate-design-asset/assets/{type}/EXAMPLES.md`

## Backward Compatibility

For existing banner generation workflows, use:

```bash
/generate_post_banner [args]
```

This command now invokes the generalized skill with `--asset-type banner` for backward compatibility.

## Version History

- **v2.0** (2025-12-24): Generalized command supporting 5 asset types
- **v1.0** (2025-12-23): Initial banner-only command
