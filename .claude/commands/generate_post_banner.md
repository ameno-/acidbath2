---
allowed-tools: mcp__nano-banana__generate_image, Bash, Write
description: Generate a glitch-style banner image for a blog post
---

# Generate Post Banner

Generate a banner image for the ACIDBATH blog post: $ARGUMENTS

## Style Guidelines

Use the ACIDBATH glitch art style:
- Dark background with digital corruption artifacts
- Neon green glowing text with RGB color splitting
- Scan lines, broken pixels, data corruption aesthetic
- Wide banner format suitable for blog post headers

## Prompt Template

Generate the banner using this prompt pattern:

```
3D text "[POST_TITLE]" in glitch art digital corruption style. Letters fragmenting and pixelating with data corruption artifacts. RGB color splitting, scan lines, broken pixels. Digital decay aesthetic like a corrupted file. Neon green glitch fragments on dark background. Wide banner format. No other text except the title.
```

## Output

1. Generate the image using nano-banana MCP
2. Save to `/Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png`
3. Report the file path for use in the post's frontmatter

## Usage

```
/generate_post_banner "Context Engineering" --slug context-engineering
```
