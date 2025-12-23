---
allowed-tools: Skill
description: Generate high-quality banner images for blog posts (invokes generate-post-banner skill)
---

# Generate Post Banner

Generate a banner image for the ACIDBATH blog post: $ARGUMENTS

## ⚠️ Note: Enhanced Skill Available

This command now invokes the **generate-post-banner** skill, which provides:
- **5 distinct banner styles** (glass, isometric, blueprint, newspaper, glitch)
- **Content-aware recommendations** based on post metadata
- **Advanced Nano Banana prompting** for higher quality images
- **Interactive style selection** with preview options

For the legacy glitch-only behavior, use `--style glitch --auto`.

---

## Quick Start

### Basic Usage (Recommended)
```
/generate_post_banner --slug post-slug
```
Loads post metadata, recommends styles, generates banner interactively.

### Specific Style
```
/generate_post_banner "Post Title" --style glass_object
```
Skip recommendations, use specified style directly.

### Auto Mode (No Prompts)
```
/generate_post_banner --slug post-slug --auto
```
Uses primary recommendation automatically without interaction.

### Legacy Glitch Style
```
/generate_post_banner "Post Title" --style glitch --auto
```
Replicates old command behavior with enhanced glitch style.

---

## Available Styles

1. **glass_object** - Glass Object Technical
   - Best for: Architecture, frameworks, system design
   - Photorealistic glass rendering of technical objects

2. **isometric** - Isometric Technical Diagram
   - Best for: Workflows, processes, tutorials
   - Hand-drawn isometric system views

3. **blueprint** - Technical Blueprint
   - Best for: Performance analysis, benchmarks, metrics
   - Engineering schematic with technical annotations

4. **newspaper** - Newspaper Front Page
   - Best for: Provocative opinions, paradigm shifts
   - Close-up newspaper with bold headline

5. **glitch** - Enhanced Glitch Corruption (Default Legacy)
   - Best for: Universal, any content type
   - Upgraded version of original glitch art style

---

## Command-Line Flags

- `--slug [slug]`: Load metadata from blog/posts/[slug]/metadata.json
- `--metadata [path]`: Load metadata from custom path
- `--style [name]`: Use specific style (skip recommendations)
- `--auto`: Use primary recommendation automatically
- `--preview-only`: Show prompt without generating

---

## Migration Guide

### Old Command Behavior
```bash
/generate_post_banner "Context Engineering" --slug context-engineering
```
Generated simple glitch art banner automatically.

### New Behavior (Default)
```bash
/generate_post_banner --slug context-engineering
```
1. Analyzes post metadata
2. Recommends appropriate style (e.g., blueprint for technical deep-dive)
3. Presents 3 options interactively
4. Generates selected style

### Replicate Old Behavior
```bash
/generate_post_banner --slug context-engineering --style glitch --auto
```
Generates enhanced glitch banner automatically (backward compatible).

---

## Output

Banner saved to: `/Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png`

Public URL: `/assets/posts/[slug]-banner.png`

Resolution: 2560x1440 (16:9 aspect ratio)

---

## Examples

### Example 1: Generate for Existing Post
```
/generate_post_banner --slug prompts-are-the-new-code
```
→ Recommends: Newspaper Front Page (provocative opinion)

### Example 2: Quick Glitch Banner
```
/generate_post_banner "My New Post" --slug my-new-post --style glitch --auto
```
→ Generates enhanced glitch banner immediately

### Example 3: Preview Before Generating
```
/generate_post_banner --slug 55k-files-5-minutes --preview-only
```
→ Shows composed Nano Banana prompt, allows review before generation

---

## Troubleshooting

**"Invalid style name"**
→ Use one of: glass_object, isometric, blueprint, newspaper, glitch

**"Nano Banana MCP not available"**
→ Verify MCP server installed and running: `claude mcp list`

**"Permission denied"**
→ Check output directory exists and is writable

**"Style doesn't match content"**
→ Override with `--style [name]` or edit metadata to improve recommendations

---

## References

- Full skill documentation: `.claude/skills/generate-post-banner/SKILL.md`
- Style templates: `.claude/skills/generate-post-banner/STYLE_LIBRARY.md`
- Mapping rules: `.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md`
- Examples: `.claude/skills/generate-post-banner/EXAMPLES.md`

---

## Version History

- **v2.0** (2025-12-23): Migrated to invoke generate-post-banner skill, maintains backward compatibility with `--style glitch --auto`
- **v1.0** (Original): Simple glitch art generation only
