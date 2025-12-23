# Banner Generation Quick Start Guide

Get started generating high-quality blog post banners in 60 seconds.

---

## Installation Check

Ensure Nano Banana MCP is installed and running:
```bash
claude mcp list
```

Look for `nano-banana` in the output. If missing, install the Nano Banana MCP server first.

---

## Basic Usage (3 Steps)

### Step 1: Invoke the Skill
```bash
/generate_post_banner --slug your-post-slug
```

### Step 2: Review Recommendations
The skill will analyze your post and recommend 3 styles:
- **Primary**: Best match based on content
- **Alternative 1**: Second-best option
- **Alternative 2**: Fallback/wildcard

### Step 3: Confirm and Generate
- Press **ENTER** to use recommended style
- Type **2** or **3** to select alternative
- Type style name to override

Banner saved to: `/public/assets/posts/[slug]-banner.png`

---

## Common Workflows

### Generate for Existing Post
```bash
/generate_post_banner --slug prompts-are-the-new-code
```
**What happens**:
1. Loads post metadata
2. Analyzes category, tags, tone
3. Recommends: Newspaper Front Page (provocative opinion piece)
4. You confirm
5. Generates newspaper-style banner

**Time**: 60-90 seconds

---

### Quick Glitch Banner (Legacy Style)
```bash
/generate_post_banner "My Post Title" --slug my-post --style glitch --auto
```
**What happens**:
1. Skips analysis and recommendations
2. Uses enhanced glitch style directly
3. Generates automatically without prompts

**Time**: 30-45 seconds (fastest)

---

### Preview Prompt Before Generating
```bash
/generate_post_banner --slug 55k-files-5-minutes --preview-only
```
**What happens**:
1. Analyzes post metadata
2. Recommends: Technical Blueprint
3. Shows composed Nano Banana prompt
4. You can review, edit, or proceed

**Use case**: Learning advanced prompting, debugging, quality control

---

### Force Specific Style
```bash
/generate_post_banner "API Architecture Guide" --style glass_object
```
**What happens**:
1. Skips recommendations
2. Uses Glass Object Technical style directly
3. Prompts for confirmation before generating

**Use case**: You already know which style you want

---

## Available Styles

| Style | Best For | Example Use Cases |
|-------|----------|-------------------|
| **glass_object** | Architecture, frameworks, systems | "The Agent Endgame", API design posts |
| **isometric** | Workflows, processes, tutorials | "Sub-Agents Wrong", automation guides |
| **blueprint** | Performance, benchmarks, metrics | "55k Files", "Context Window Bleeding" |
| **newspaper** | Provocative opinions, paradigm shifts | "Prompts Are New Code", "Chat UI Dead" |
| **glitch** | Universal, any content type | Fallback, quick generation |

---

## Command Flags Cheat Sheet

| Flag | Purpose | Example |
|------|---------|---------|
| `--slug [slug]` | Load post metadata | `--slug context-engineering` |
| `--style [name]` | Force specific style | `--style glass_object` |
| `--auto` | Auto-select primary | `--auto` |
| `--preview-only` | Show prompt, don't generate | `--preview-only` |
| `--metadata [path]` | Custom metadata path | `--metadata /path/to/file.json` |

**Combine flags**: `--slug my-post --style glitch --auto` (fast glitch generation)

---

## Expected Generation Times

| Style | Complexity | Time |
|-------|-----------|------|
| Enhanced Glitch | Low | 30-45 seconds |
| Isometric Diagram | Medium | 45-60 seconds |
| Technical Blueprint | Medium | 45-60 seconds |
| Glass Object Technical | High | 60-90 seconds |
| Newspaper Front Page | High | 60-90 seconds |

*Photorealistic styles (glass, newspaper) take longer due to complex rendering*

---

## Troubleshooting Common Issues

### "Nano Banana MCP not available"
**Problem**: MCP server not running
**Solution**:
1. Check installation: `claude mcp list`
2. Install if missing
3. Restart Claude Code

---

### "Invalid style name"
**Problem**: Typo in `--style` flag
**Solution**: Use one of: `glass_object`, `isometric`, `blueprint`, `newspaper`, `glitch`

---

### "Permission denied"
**Problem**: Can't write to output directory
**Solution**:
```bash
# Create directory if missing
mkdir -p /Users/ameno/dev/acidbath2/public/assets/posts/

# Check permissions
ls -ld /Users/ameno/dev/acidbath2/public/assets/posts/
```

---

### Style doesn't match content
**Problem**: Recommendation feels wrong
**Solution**: Override with `--style [name]` to use style you prefer

---

### Generation takes too long
**Problem**: Timeout or very slow generation
**Solution**:
- Photorealistic styles (glass, newspaper) are slower—this is normal
- Try simpler style: `--style glitch` or `--style isometric`
- Check MCP server status

---

### Prompt too generic
**Problem**: Banner doesn't capture post specifics
**Solution**:
1. Add more tags to post metadata
2. Include detailed description
3. Use `--preview-only` to review and manually edit prompt

---

## Migration from Old Command

### Old Way (v1.0)
```bash
/generate_post_banner "Context Engineering" --slug context-engineering
```
**Generated**: Simple glitch art only

### New Way (v2.0) - Recommended
```bash
/generate_post_banner --slug context-engineering
```
**Generates**: Content-aware style (e.g., blueprint for technical posts)

### New Way - Legacy Compatible
```bash
/generate_post_banner --slug context-engineering --style glitch --auto
```
**Generates**: Enhanced glitch (similar to old, but improved quality)

---

## Example: First Banner Generation

Let's generate a banner for a post about agent architecture:

### 1. Invoke Skill
```bash
/generate_post_banner --slug agent-endgame
```

### 2. Review Recommendations
```
📋 BANNER STYLE RECOMMENDATIONS for "The Agent Endgame"

Recommended Styles:

1. Glass Object Technical (Score: 10) ⭐ RECOMMENDED
   → Best for: Architecture, custom agent systems
   → Visual: Transparent glass processor with light refraction

2. Isometric Technical Diagram (Score: 4)
   → Best for: Agent workflow visualization

3. Enhanced Glitch Corruption (Score: 1)
   → Universal fallback

Press ENTER to use recommended style (1)
```

### 3. Confirm
Press **ENTER**

### 4. Generation
```
🎨 Generating banner...
Style: Glass Object Technical
⏳ Calling Nano Banana MCP... (60s)
```

### 5. Success
```
✅ BANNER GENERATED SUCCESSFULLY
File: /public/assets/posts/agent-endgame-banner.png
Size: 2.4 MB
```

**Total time**: ~90 seconds

---

## Next Steps After Quick Start

1. **Explore Other Styles**: Try different styles to see visual variety
   ```bash
   /generate_post_banner "Test Post" --style newspaper
   /generate_post_banner "Test Post" --style blueprint
   ```

2. **Read Style Library**: Review `.claude/skills/generate-post-banner/STYLE_LIBRARY.md` to understand when each style works best

3. **Check Examples**: See `.claude/skills/generate-post-banner/EXAMPLES.md` for filled prompt examples

4. **Understand Mapping**: Read `.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md` to see how content analysis works

5. **Batch Generation**: Generate banners for all existing posts using `--auto` flag

---

## Pro Tips

### Tip 1: Rich Metadata = Better Recommendations
Add detailed tags and tone information to post metadata for more accurate style recommendations.

**Example metadata.json**:
```json
{
  "title": "Context Engineering Deep-Dive",
  "category": "Technical Analysis",
  "tags": ["performance", "optimization", "context window", "token usage"],
  "formatting": {
    "tone": "direct, technical",
    "hasDiagrams": true
  }
}
```
→ This will trigger **Technical Blueprint** recommendation with high confidence

---

### Tip 2: Use Preview Mode for Learning
```bash
/generate_post_banner --slug your-post --preview-only
```
Review composed prompts to learn advanced Nano Banana techniques. You can copy and modify these prompts for other projects.

---

### Tip 3: Combine Flags for Speed
```bash
/generate_post_banner --slug post-slug --style glitch --auto
```
Fastest generation: skips analysis, recommendations, and confirmation.

---

### Tip 4: Override When Needed
The AI recommendation is good, but not perfect. Trust your judgment:
```bash
# AI recommends blueprint, but you want dramatic newspaper style
/generate_post_banner --slug your-post --style newspaper
```

---

### Tip 5: Regenerate Until Satisfied
If first generation doesn't meet expectations:
1. Type "regenerate" at success prompt
2. Try different style
3. Or edit prompt manually in preview mode

Generation is fast enough that trying 2-3 variations is practical.

---

## Getting Help

- **Skill Documentation**: `.claude/skills/generate-post-banner/SKILL.md` (comprehensive workflow)
- **Style Templates**: `.claude/skills/generate-post-banner/STYLE_LIBRARY.md` (prompt patterns)
- **Mapping Logic**: `.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md` (decision rules)
- **Examples**: `.claude/skills/generate-post-banner/EXAMPLES.md` (concrete cases)

---

## Version

- **Quick Start v1.0** (2025-12-23): Initial guide for banner generation skill v1.0
