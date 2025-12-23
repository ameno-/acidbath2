# Feature: Improve Banner Images for Blog Posts

## Metadata
adw_id: `88182869`
prompt: `We must improve our use Nano Banana and command the command to generate_post_banner. It isn't good enough and should include more dynamism and interest. Here is a repo with sample prompts that can extract immense quality from Nano banana: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/main/README_en.md

Some highlights:
```
A photorealistic, highly detailed image featuring [a 3D Polaroid camera] rendered in clear, highly polished transparent glass or crystal material. [The body has distinct thickness and dimensional depth, the iconic shape of a classic Polaroid camera—boxy body, front lens, top viewfinder, front shutter button, and bottom film slot—all presented in simplified yet extremely precise geometric structures, making it instantly recognizable without any patterns]. All edges are treated with rounded chamfers and smooth curved surfaces, creating elegant refraction effects under light. The camera is placed slightly tilted, as if floating above a clean, flawless, seamless pale beige or very light gray studio background.

Lighting is bright, clean professional studio light, focusing on highlighting the transparency, specular reflection and refraction characteristics of the glass material. Sharp and delicate highlights appear on the body chamfers, film slot edges and lens rings, highlighting the crystal texture and luxurious vision. Subtle refraction, light bending and local distortion effects are produced when light penetrates the interior of the glass body, especially obvious in the lens thickness variation area, inside the film slot and near the top viewfinder, greatly enhancing realism and visual impact. A soft, diffuse shadow falls below and slightly behind the camera, giving the picture a sense of groundedness without destroying the minimalist temperament.

The overall aesthetic style is minimalist, modern, and clean, presenting the visual effect of high-end product photography and concept art rendering. The focus of the picture is completely on the crystal clear material performance and classic geometric shape of the glass Polaroid camera. The image as a whole is high-key and shallow depth of field processing, keeping the Polaroid camera in absolute sharp focus, while the background is softly blurred, thereby maximizing the subject.
```

For content using metaphors or real-world objects, we can replace "this street" with a 757 Boeing
```
Draw a hand-drawn isometric diagram of this street
```

```
A 1080x1080 pixel close-up photo, hands holding a white newspaper, shot downwards. The background is extremely blurred and dark, making the newspaper stand out clearly. The newspaper occupies most of the picture, and its content is legible. The eye-catching headline is "[Headline]". In the center of the picture is a large black and white photo of [Photo Description]. The caption has many columns and is legible. Each shot maintains the same style, composition, lighting, characters, blur effect, layout and newspaper design, only changing the headline and photo.
```

Create a more dynamic, high-quality post banner generation workflow.`

## Feature Description

Transform the ACIDBATH blog post banner generation workflow to produce more dynamic, visually compelling, and technically sophisticated images. The current implementation uses a simple glitch art style with limited variation. This feature will leverage advanced Nano Banana prompting techniques to create multiple banner style options that match different content types, maintain brand consistency, and significantly improve visual impact.

The improved workflow will:
- Support multiple banner style templates (photorealistic glass, isometric diagrams, technical blueprints, newspaper front-page, corrupted data glitch)
- Intelligently recommend styles based on post content and metadata
- Use advanced prompting techniques for material rendering, lighting, composition, and depth
- Provide a library of reusable style patterns adapted from high-quality Nano Banana examples
- Maintain backward compatibility with existing banners while offering opt-in improvements

## User Story

As a **technical blog author**
I want to **generate visually distinctive, high-quality banner images that match my post's tone and content**
So that **my posts stand out visually, communicate technical concepts through imagery, and maintain a professional yet unique brand aesthetic**

## Problem Statement

The current `generate_post_banner` command produces generic glitch art banners with minimal variation. While the style is consistent, it:
- Lacks visual dynamism and fails to differentiate between technical deep-dives, opinion pieces, and tutorials
- Misses opportunities to use metaphors and technical imagery to reinforce content themes
- Uses basic prompts that don't leverage Nano Banana's advanced capabilities for photorealistic rendering, material effects, and composition
- Provides no style options or content-aware recommendations
- Has limited reusability across different blog post types

For a practitioner-focused technical blog competing for senior engineer attention, banner quality matters. Posts about agent architecture deserve different visual treatment than posts about cost optimization. The current one-size-fits-all approach undersells the content quality.

## Solution Statement

Create a modular, extensible banner generation system with:

1. **Style Template Library**: 5+ distinct banner styles (glass/crystal tech objects, isometric technical diagrams, blueprint/schematic, newspaper front-page, enhanced glitch corruption) each with reusable prompt patterns optimized for Nano Banana

2. **Content-Aware Recommendations**: Analyze post metadata (category, tags, title) to suggest appropriate banner styles. Technical deep-dives get isometric/blueprint treatment, opinion pieces get newspaper style, architecture posts get glass object rendering

3. **Advanced Prompt Engineering**: Implement Nano Banana best practices including:
   - Photorealistic material specifications (glass, crystal, metal, holographic)
   - Professional lighting setups (studio, HDR, dramatic)
   - Spatial composition control (depth-of-field, foreground/midground/background)
   - Geometric and textural precision
   - Technical accuracy in object rendering

4. **Interactive Style Selection**: Update command to support style flags (`--style glass`, `--style newspaper`, `--style auto`) with preview descriptions before generation

5. **Verification and Iteration**: Built-in quality checks and regeneration options if output doesn't match expectations

The solution transforms banner generation from a single-command afterthought into a creative workflow step that enhances content impact.

## Relevant Files

### Existing Files to Modify
- `.claude/commands/generate_post_banner.md` - Current banner generation command; needs complete rewrite to support style templates, content analysis, and advanced prompting
- `blog/posts/*/metadata.json` - Post metadata files; will inform style recommendations based on category, tags, and technical focus

### New Files to Create

#### New Files
- `.claude/skills/generate-post-banner/SKILL.md` - Migrate from command to full skill with verification workflow
- `.claude/skills/generate-post-banner/STYLE_LIBRARY.md` - Comprehensive library of banner style templates with Nano Banana prompt patterns
- `.claude/skills/generate-post-banner/EXAMPLES.md` - Reference examples showing each style with sample outputs and use cases
- `.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md` - Mapping rules for content types → recommended banner styles

## Implementation Plan

### Phase 1: Research and Style Template Design
Extract and adapt Nano Banana advanced prompting techniques into reusable banner style templates. Research existing post content to understand style-to-content mapping requirements.

### Phase 2: Core Skill Development
Build the banner generation skill with style library, content analysis, and interactive selection. Implement prompt composition system for mixing base styles with content-specific adaptations.

### Phase 3: Integration and Testing
Test each style template across different post types, verify Nano Banana MCP integration, create comprehensive examples, and document usage patterns for future banner generation.

## Step by Step Tasks

### Group A: Foundation and Research [parallel: false, model: sonnet]
Sequential research and design work to establish style library and requirements.

#### Step A.1: Research Nano Banana Prompting Techniques
- Fetch and analyze https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/main/README_en.md
- Extract key prompting patterns: photorealistic materials, lighting specifications, composition control, depth-of-field
- Identify reusable prompt components: material specifications, lighting setups, camera angles, post-processing effects
- Document specific techniques for glass/crystal rendering, isometric diagrams, newspaper layouts, blueprint styles

#### Step A.2: Analyze Existing Blog Content
- Review all post metadata files to understand content categories, tags, and topics
- Identify 3-5 distinct content archetypes (technical deep-dive, opinion/POV, tutorial/how-to, case study, architecture)
- Map archetypes to appropriate visual styles
- Extract common technical metaphors and objects from post titles/content

#### Step A.3: Design Style Template Library
- Create 5 distinct banner style templates:
  1. **Glass Object Technical** - Photorealistic glass/crystal rendering of technical objects (cameras, servers, circuits)
  2. **Isometric Technical Diagram** - Hand-drawn isometric views of systems, architectures, workflows
  3. **Technical Blueprint** - Engineering schematic/blueprint style with annotations and measurements
  4. **Newspaper Front Page** - Close-up newspaper with headline and technical photo
  5. **Enhanced Glitch Corruption** - Upgraded version of current style with better depth and effects
- For each style, define: prompt template, material specifications, lighting setup, composition rules, content fit
- Document placeholder variables in each template (e.g., [TECHNICAL_OBJECT], [HEADLINE], [CONCEPT])

### Group B: Style Library Implementation [parallel: false, depends: A, model: sonnet]
Build the style template library files with complete prompt patterns.

#### Step B.1: Create STYLE_LIBRARY.md
- Write comprehensive style library document
- For each of 5 styles, include:
  - Style name and description
  - Best use cases (content types, topics)
  - Complete Nano Banana prompt template with placeholders
  - Material/lighting/composition specifications
  - Technical notes on what makes this style work
- Include prompt composition guidance (how to mix base style with content-specific elements)
- Add troubleshooting section for common Nano Banana generation issues

#### Step B.2: Create CONTENT_STYLE_MAP.md
- Define mapping rules from post metadata → recommended styles
- Create decision tree: category + tags + title analysis → style recommendations
- Include examples: "context engineering" post → glass object style, "agent architecture" → isometric diagram
- Document override patterns (when to ignore recommendations)
- Add multi-style suggestions (primary + 2 alternatives)

#### Step B.3: Create EXAMPLES.md
- For each of the 5 styles, create 2-3 concrete examples
- Include: post title, recommended style, filled prompt template, rationale
- Add visual descriptions of expected output (since we can't include actual images yet)
- Create "style comparison" section showing how same post title would look in different styles

### Group C: Skill Implementation [parallel: false, depends: B, model: auto]
Build the actual banner generation skill with all workflow logic.

#### Step C.1: Create Main SKILL.md
- Write skill frontmatter: name, description, allowed tools (mcp__nano-banana__generate_image, Bash, Write, Read, Grep)
- Implement workflow sections:
  1. **Content Analysis**: Read post metadata or take post title/description as input
  2. **Style Recommendation**: Apply CONTENT_STYLE_MAP rules to suggest styles
  3. **Interactive Selection**: Present 1-3 style options with descriptions, get user confirmation or allow override
  4. **Prompt Composition**: Fill selected style template with content-specific variables
  5. **Generation**: Call Nano Banana MCP with composed prompt
  6. **Verification**: Check image was created, offer regeneration if needed
  7. **Output**: Save to `/Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png`
- Add command-line flag support: `--style [name]`, `--auto`, `--preview-only`
- Include error handling for MCP failures, missing metadata, invalid style names

#### Step C.2: Implement Content Analysis Logic
- Add prompt template for analyzing post content when metadata is unavailable
- Extract key concepts, technical objects, metaphors from post title/subtitle/summary
- Identify tone markers (opinion vs tutorial vs deep-dive)
- Generate placeholder values for style templates based on analysis

#### Step C.3: Implement Prompt Composition System
- Create utility for filling style template placeholders
- Add smart defaults for common placeholders
- Implement validation: ensure all placeholders are filled before generation
- Add preview mode that shows composed prompt without generating image

### Group D: Migration and Enhancement [parallel: true, depends: C, model: haiku]
Update existing command and create backward compatibility.

#### Step D.1: Update generate_post_banner Command
- Rewrite `.claude/commands/generate_post_banner.md` to invoke new skill
- Maintain backward compatibility: default to enhanced glitch style if no flags
- Add deprecation notice pointing to new skill
- Update usage examples

#### Step D.2: Create Quick Start Documentation
- Add section to main skill explaining basic usage
- Create "migration guide" for users of old command
- Document common workflows: auto-generate, style comparison, manual selection
- Add troubleshooting section

### Group E: Testing and Validation [parallel: false, depends: D, model: opus]
Comprehensive testing across all styles and content types.

#### Step E.1: Test Each Style Template
- Generate test banners for each of 5 styles using sample post titles
- Verify Nano Banana MCP accepts prompts without errors
- Review outputs for quality, consistency with style description
- Iterate on prompt templates if outputs don't match expectations

#### Step E.2: Test Content-Aware Recommendations
- Run style recommendation logic against 5-10 existing posts
- Verify recommendations match expected style for content type
- Test edge cases: posts with minimal metadata, multi-category posts
- Adjust CONTENT_STYLE_MAP rules based on results

#### Step E.3: End-to-End Workflow Testing
- Test full workflow: content analysis → recommendation → selection → generation → save
- Verify all command flags work correctly
- Test error handling: MCP unavailable, invalid style, missing metadata
- Confirm file paths are correct and images are saved properly

## Testing Strategy

### Unit Tests
- **Style Template Validation**: Each template has all required placeholders documented and can be filled with test data
- **Content Analysis**: Post metadata parsing correctly extracts category, tags, title, and generates accurate recommendations
- **Prompt Composition**: Template filling produces valid Nano Banana prompts with no unfilled placeholders
- **File Operations**: Images save to correct paths with proper naming conventions

### Integration Tests
- **Nano Banana MCP**: Each style template generates valid images through MCP without errors
- **Style Recommendations**: 10+ existing posts get appropriate style recommendations based on content type
- **End-to-End Workflow**: Complete generation workflow works from post input to saved banner image

### Edge Cases
- Post with minimal metadata (only title) → should fall back to title analysis
- Post with conflicting tags (technical + opinion) → should recommend primary + alternatives
- Nano Banana MCP timeout or error → should provide clear error message and retry option
- Very long post titles → should truncate or abbreviate appropriately in prompts
- Special characters in titles → should escape or sanitize for prompt templates
- Request for non-existent style → should list available styles and prompt for valid selection

## Acceptance Criteria

1. **Style Library Complete**: 5 distinct banner styles documented with complete Nano Banana prompt templates, material/lighting specs, and usage guidance
2. **Content-Aware Recommendations**: System analyzes post metadata/content and recommends appropriate style(s) based on category, tags, and tone
3. **Interactive Workflow**: User can review style recommendations, select from options, preview composed prompts, and generate banners
4. **Quality Improvement**: Generated banners demonstrate significantly higher visual quality, dynamism, and content relevance compared to current glitch-only approach
5. **Backward Compatibility**: Existing `generate_post_banner` command still works with default behavior
6. **Documentation Complete**: Skill includes usage examples, style library reference, content mapping rules, and troubleshooting guide
7. **Verification Workflow**: System confirms image generation success and offers regeneration if needed
8. **Reusability**: Style templates are modular and can be easily extended with new styles in the future

## Validation Commands

Execute these commands to validate the feature is complete:

```bash
# Verify skill file structure exists
ls -la /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/

# Verify all required skill files are present
test -f /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/SKILL.md && \
test -f /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/STYLE_LIBRARY.md && \
test -f /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md && \
test -f /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/EXAMPLES.md && \
echo "✓ All skill files present" || echo "✗ Missing skill files"

# Verify updated command exists
test -f /Users/ameno/dev/acidbath2/trees/88182869/.claude/commands/generate_post_banner.md && \
echo "✓ Command file updated" || echo "✗ Command file missing"

# Test style library has 5 styles documented
grep -c "^## Style [0-9]:" /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/STYLE_LIBRARY.md | \
grep -q "5" && echo "✓ 5 styles documented" || echo "✗ Incorrect style count"

# Verify content style mapping rules exist
grep -q "decision tree\|mapping rules" /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md && \
echo "✓ Style mapping rules present" || echo "✗ Missing style mapping"

# Test skill can be read and parsed (basic syntax check)
head -20 /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/SKILL.md | \
grep -q "^---" && echo "✓ Skill has valid frontmatter" || echo "✗ Invalid skill format"

# Verify examples exist for multiple styles
grep -c "^### Example [0-9]" /Users/ameno/dev/acidbath2/trees/88182869/.claude/skills/generate-post-banner/EXAMPLES.md | \
awk '$1 >= 5 {print "✓ Sufficient examples documented"; exit 0} {print "✗ Need more examples"; exit 1}'

# Manual test: Generate banner for existing post (requires human verification)
echo "Manual test required: Run skill to generate banner and verify image quality"
echo "Command: /generate-post-banner \"Context Engineering\" --slug context-engineering --preview-only"
```

## Notes

### Technical Considerations
- **MCP Integration**: Requires `mcp__nano-banana__generate_image` MCP server to be configured and available. Test MCP availability in skill initialization.
- **Prompt Length**: Nano Banana prompts can be lengthy (300-500 words for photorealistic styles). Ensure MCP accepts full prompts without truncation.
- **Image Dimensions**: Current banners are varying sizes. Standardize on 1920x1080 or 2560x1440 for blog headers, specify in all style templates.
- **Generation Time**: Complex photorealistic prompts may take longer to generate. Add timeout handling and progress indicators.

### Style Template Design Philosophy
- **Modularity**: Each style should be self-contained with clear placeholder variables
- **Adaptability**: Templates should work across different technical topics with minimal modification
- **Quality First**: Prioritize visual impact and technical accuracy over generation speed
- **Brand Consistency**: All styles should feel cohesive despite different aesthetics (professional, technical, high-quality)

### Future Extensions (Not in Scope)
- A/B testing framework to compare banner styles for engagement metrics
- Batch regeneration tool to upgrade all existing post banners with new styles
- Style "mixing" system to combine elements from multiple templates
- Custom style creation workflow for one-off banner needs
- Integration with post frontmatter to store style metadata for reproducibility

### Dependencies
- Nano Banana MCP server must be installed and configured
- Existing posts need metadata.json files for content-aware recommendations (most already have this)
- No new Python libraries required (skill operates through MCP and Claude Code tools)
