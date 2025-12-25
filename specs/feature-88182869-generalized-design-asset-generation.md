# Feature: Generalized Design Asset Generation System

## Metadata
adw_id: `88182869`
prompt: `We recently made made improvements for how we generate banner images using OpenRouter and NanoBanana. Now we need to expand on that and generate more types of content, not just banner images but images that we can use throughout our website. Review these images and create new nano banana prompts to generate similar styles using our banner image generation skill. Create a new skill that is more generalized that replaces the banner image but just allows us to reference certain prompts and inject them into skill to generate asset. Use the skills documentation to understand how to structure skills references and progressive disclosure. The idea is to have reference files with prompts for ways to generate all these specific styles, including the banner image styles that we've already been generating. This new skill will be used in the creation of blog posts to generate content and all kinds of assets. This new skill will also define certain types of assets that can be generated. We already know of banner images, we must also be able to generate callouts inside of text and other styles of assets for the blog. Feel free to create several for now, banner images are the ones I currently use but we will iterate on this.`

## Feature Description

Transform the specialized banner generation skill into a comprehensive, generalized design asset generation system that supports multiple asset types beyond just blog post banners. This system will use the same content-aware, style-library approach but extend it to generate various design assets needed throughout the ACIDBATH website: in-text callouts, section dividers, technical diagrams, data visualizations, and more.

The generalized system will:
- Support multiple asset types (banners, callouts, diagrams, dividers, icons)
- Maintain the existing banner generation capabilities while adding new asset types
- Use progressive disclosure with reference files for each asset type's style library
- Apply content-aware recommendations for all asset types
- Provide a unified interface for generating any visual asset needed for blog content
- Integrate seamlessly with blog post creation workflows

## User Story

As a **technical blog author creating ACIDBATH content**
I want to **generate various types of visual assets (not just banners) using intelligent style recommendations and advanced prompting**
So that **I can create visually cohesive, professional content with callouts, diagrams, and visual elements that enhance readability without needing external design tools**

## Problem Statement

The current `generate-post-banner` skill is powerful but narrowly focused on blog post header banners. When creating comprehensive technical blog posts, authors need various visual assets:
- **In-text callouts**: Visual highlights for key insights, warnings, or data points within blog content
- **Section dividers**: Visual breaks between major sections to improve scannability
- **Technical diagrams**: Simplified visual representations of concepts (without Nano Banana's text limitations)
- **Data cards**: Standalone visualization of metrics, benchmarks, or statistics
- **Decorative elements**: Icons, badges, or accent graphics that reinforce branding

Currently, authors either:
1. Manually create these assets using external tools (slow, inconsistent)
2. Use text-based Astro components (Callout, Collapse) which lack visual impact
3. Skip visual enhancements entirely (reduces engagement)

This creates friction in the content creation workflow and results in posts that rely heavily on text when strategic visuals could dramatically improve comprehension and retention.

## Solution Statement

Build a **generalized design asset generation skill** that:

1. **Asset Type Library**: Define 5+ asset types (Banner, Callout, Divider, Diagram, DataCard) each with:
   - Multiple style variants (matching banner system's approach)
   - Content-aware use case recommendations
   - Nano Banana-optimized prompt templates
   - Dimension/aspect ratio specifications appropriate to asset type

2. **Unified Skill Interface**: Single skill (`generate-design-asset`) that:
   - Takes asset type and content context as input
   - Recommends appropriate styles based on content and placement
   - Composes prompts from modular style libraries
   - Generates assets with consistent ACIDBATH brand aesthetic

3. **Progressive Disclosure Structure**: Organize like the banner skill but generalized:
   ```
   .claude/skills/generate-design-asset/
   ├── SKILL.md                    # Main workflow (unified for all asset types)
   ├── ASSET_TYPES.md              # Defines all supported asset types
   ├── assets/
   │   ├── banner/
   │   │   ├── STYLES.md           # Banner style library (migrated from banner skill)
   │   │   └── EXAMPLES.md
   │   ├── callout/
   │   │   ├── STYLES.md           # Callout style library
   │   │   └── EXAMPLES.md
   │   ├── divider/
   │   │   ├── STYLES.md           # Section divider styles
   │   │   └── EXAMPLES.md
   │   ├── diagram/
   │   │   ├── STYLES.md           # Simple diagram styles
   │   │   └── EXAMPLES.md
   │   └── datacard/
   │       ├── STYLES.md           # Data visualization styles
   │       └── EXAMPLES.md
   └── CONTENT_ASSET_MAP.md        # Maps content needs → asset type + style
   ```

4. **Content Integration Workflow**: Update blog post creation to suggest assets:
   - When creating posts with `/new-post`, skill suggests relevant assets
   - When adding callouts, offer to generate visual callout assets
   - When presenting metrics, offer to generate data cards

5. **Brand Consistency**: All asset types follow ACIDBATH aesthetic:
   - Dark mode backgrounds (black, charcoal, navy)
   - Neon accent colors (cyan, magenta, purple, acid-green)
   - Tech-noir atmosphere with sophisticated minimalism
   - Consistent with design system components

## Relevant Files

### Existing Files to Reference
- `.claude/skills/generate-post-banner/SKILL.md` - Current banner generation workflow; will serve as template for generalized skill
- `.claude/skills/generate-post-banner/STYLE_LIBRARY.md` - Banner styles to migrate into new asset type structure
- `.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md` - Content analysis logic to extend for all asset types
- `.claude/skills/generate-post-banner/EXAMPLES.md` - Banner examples to migrate
- `adws/adw_modules/openrouter_image.py` - Image generation module (already working with OpenRouter)
- `ai_docs/design-system.md` - Design system reference for brand consistency
- `ai_docs/anthropic_agent_skills.md` - Skills documentation for progressive disclosure patterns
- `README.md` - Project overview and existing banner skill usage patterns

### Existing Files to Modify
- `.claude/commands/generate_post_banner.md` - Update to point to new skill's banner asset type
- `.claude/commands/new-post.md` - Enhance to suggest asset generation during post creation

### New Files to Create

#### Core Skill Files
- `.claude/skills/generate-design-asset/SKILL.md` - Main skill with unified generation workflow
- `.claude/skills/generate-design-asset/ASSET_TYPES.md` - Comprehensive list of supported asset types with specs
- `.claude/skills/generate-design-asset/CONTENT_ASSET_MAP.md` - Decision tree for content → asset recommendations

#### Banner Asset Type (Migrated)
- `.claude/skills/generate-design-asset/assets/banner/STYLES.md` - Migrated banner styles
- `.claude/skills/generate-design-asset/assets/banner/EXAMPLES.md` - Migrated banner examples

#### Callout Asset Type (New)
- `.claude/skills/generate-design-asset/assets/callout/STYLES.md` - Callout visual styles (insight highlights, warnings, data callouts)
- `.claude/skills/generate-design-asset/assets/callout/EXAMPLES.md` - Callout examples for different use cases

#### Divider Asset Type (New)
- `.claude/skills/generate-design-asset/assets/divider/STYLES.md` - Section divider styles (minimal lines, tech patterns, glitch breaks)
- `.claude/skills/generate-design-asset/assets/divider/EXAMPLES.md` - Divider examples

#### Diagram Asset Type (New)
- `.claude/skills/generate-design-asset/assets/diagram/STYLES.md` - Simple diagram styles (2-3 element max, abstract representations)
- `.claude/skills/generate-design-asset/assets/diagram/EXAMPLES.md` - Diagram examples

#### DataCard Asset Type (New)
- `.claude/skills/generate-design-asset/assets/datacard/STYLES.md` - Data visualization styles (metric cards, stat displays)
- `.claude/skills/generate-design-asset/assets/datacard/EXAMPLES.md` - DataCard examples

#### Wrapper Command (New)
- `.claude/commands/generate-design-asset.md` - User-facing command that invokes the skill

## Implementation Plan

### Phase 1: Foundation and Asset Type Design
Research and design the asset type system. Define what asset types ACIDBATH needs, their specifications, and how they integrate with blog content.

### Phase 2: Core Skill Development
Build the generalized skill structure with unified workflow. Migrate existing banner functionality into the new asset type framework.

### Phase 3: New Asset Type Implementation
Create callout, divider, diagram, and datacard asset types with complete style libraries and examples.

### Phase 4: Integration and Testing
Integrate with blog post creation workflows, test all asset types, validate brand consistency across assets.

## Step by Step Tasks

IMPORTANT: Execute every step in order, respecting group dependencies.

Steps are organized into groups. Groups execute in dependency order.
Steps within a group can be parallel (independent) or sequential (ordered).

### Group A: Research and Asset Type Design [parallel: false, model: sonnet]
Sequential foundation work to understand requirements and design the asset type system.

#### Step A.1: Analyze Provided Design Images
- Review the 10 design images provided in the GitHub issue
- Categorize images by visual style (glass/crystal, abstract tech, neon accents, data-focused, glitch art)
- Identify recurring visual patterns: dark backgrounds, neon highlights, geometric shapes, material rendering
- Extract key Nano Banana prompting patterns from each image type
- Document which images would work as banners vs callouts vs other asset types
- Note any visual styles that align with existing banner styles vs need new templates

#### Step A.2: Define Asset Type Requirements
- Identify 5 core asset types needed for ACIDBATH blog content:
  1. **Banner**: Blog post headers (existing functionality)
  2. **Callout**: In-text visual highlights for insights, warnings, data
  3. **Divider**: Section break graphics
  4. **Diagram**: Simple 2-3 element technical representations
  5. **DataCard**: Metric/statistic visualization cards
- For each asset type, define:
  - Purpose and use cases
  - Recommended dimensions and aspect ratios
  - Placement context (header, inline, between sections)
  - Integration method (Astro component prop, markdown image, direct path)
  - Number of style variants needed (aim for 3-5 per asset type)

#### Step A.3: Design Asset Type Directory Structure
- Design the skill's progressive disclosure structure following `.claude/skills/generate-post-banner/` pattern
- Plan asset type subdirectories under `assets/` folder
- Define file naming conventions for consistency
- Document migration path for existing banner skill files
- Plan how asset type selection will work in the main SKILL.md workflow
- Design content-to-asset mapping logic (extends existing content-to-style mapping)

#### Step A.4: Audit Existing Banner Skill
- Review all files in `.claude/skills/generate-post-banner/`
- Identify components to migrate vs components to generalize
- Document workflow sections that apply to all asset types vs banner-specific
- Extract reusable prompt composition patterns
- Note OpenRouter integration specifics to maintain
- List any banner-specific logic that needs asset type parameterization

### Group B: Core Skill Structure [parallel: false, depends: A, model: sonnet]
Build the foundational skill structure and migrate banner functionality.

#### Step B.1: Create Main SKILL.md
- Write skill frontmatter with name `generate-design-asset` and comprehensive description
- Define allowed tools: `Bash, Write, Read, Grep, Glob` (OpenRouter via Python module)
- Document skill overview explaining generalized asset generation approach
- Create 7-section workflow structure (adapted from banner skill):
  1. **Asset Type Selection**: New section to choose Banner/Callout/Divider/Diagram/DataCard
  2. **Content Analysis**: Migrated from banner skill, adapted for all asset types
  3. **Style Recommendation**: Load appropriate asset type's STYLES.md, apply mapping rules
  4. **Interactive Selection**: Present style options, get user confirmation
  5. **Prompt Composition**: Fill style template with content variables
  6. **Generation**: Call OpenRouter via `adws/adw_modules/openrouter_image.py`
  7. **Verification**: Confirm asset created, offer regeneration
- Include Nano Banana guidelines (dark mode, minimal text, abstract over literal)
- Document command-line flags: `--asset-type`, `--style`, `--auto`, `--preview-only`, `--slug`, `--metadata`

#### Step B.2: Create ASSET_TYPES.md
- Define all 5 supported asset types with comprehensive specifications
- For each asset type, document:
  - **Name and description**: What it's for
  - **Use cases**: When to use this asset type
  - **Dimensions**: Standard sizes (e.g., Banner 2560x1440, Callout 1200x800, Divider 2560x200)
  - **Aspect ratio**: Recommended ratio for OpenRouter generation
  - **Output path pattern**: Where files are saved
  - **Integration notes**: How to use in blog posts
  - **Style count**: How many style variants exist
- Include visual examples descriptions
- Add decision criteria for choosing asset types
- Document asset type combinations for comprehensive posts

#### Step B.3: Create CONTENT_ASSET_MAP.md
- Extend banner's content-style mapping to content-asset mapping
- Define decision tree for content analysis → asset type recommendation
- Create scoring system for asset type selection:
  - Post sections with key insights → Callout asset
  - Posts with multiple major sections → Divider assets
  - Posts explaining systems/workflows → Diagram assets
  - Posts with benchmarks/metrics → DataCard assets
  - All posts → Banner asset (default)
- Document when to recommend multiple asset types for single post
- Include examples of content analysis leading to asset recommendations
- Add override patterns and manual selection guidance

### Group C: Banner Asset Migration [parallel: false, depends: B, model: sonnet]
Migrate existing banner skill into new asset type structure.

#### Step C.1: Migrate Banner Styles
- Create `.claude/skills/generate-design-asset/assets/banner/STYLES.md`
- Copy and adapt content from `.claude/skills/generate-post-banner/STYLE_LIBRARY.md`
- Ensure all 5 banner styles are included:
  1. Glass Object Technical
  2. Simple Isometric Diagram
  3. Technical Blueprint
  4. Newspaper Front Page
  5. Enhanced Glitch Corruption
- Verify all Nano Banana guidelines are preserved
- Update any file paths or references to work in new structure
- Add asset type context (dimensions, use cases specific to banners)

#### Step C.2: Migrate Banner Examples
- Create `.claude/skills/generate-design-asset/assets/banner/EXAMPLES.md`
- Copy examples from `.claude/skills/generate-post-banner/EXAMPLES.md`
- Enhance examples with asset type framing
- Ensure examples cover all 5 banner styles
- Add output path examples and integration notes

#### Step C.3: Migrate Banner Mapping Rules
- Extract banner-specific mapping logic from `.claude/skills/generate-post-banner/CONTENT_STYLE_MAP.md`
- Integrate into CONTENT_ASSET_MAP.md under "Banner Asset Type" section
- Preserve all category, tag, title, and formatting-based scoring
- Ensure backward compatibility with existing banner generation patterns

### Group D: Callout Asset Type [parallel: true, depends: C, model: auto]
Create callout asset type for in-text visual highlights.

#### Step D.1: Design Callout Styles
- Create `.claude/skills/generate-design-asset/assets/callout/STYLES.md`
- Design 4 callout style variants:
  1. **Insight Highlight**: Glowing card with key insight text overlay (1-2 words max)
  2. **Warning Alert**: Orange/red neon warning graphic with caution aesthetic
  3. **Data Spotlight**: Metric/number visualization with dramatic lighting
  4. **Tech Detail**: Small technical object or abstract shape representing concept
- For each style:
  - Write Nano Banana prompt template
  - Define placeholders for content injection
  - Specify dimensions (1200x800 or 1600x900 for inline use)
  - Document dark mode aesthetic requirements
  - Include guidelines on text limitations (even more strict for smaller callouts)
- Add usage notes: when each callout style is appropriate

#### Step D.2: Create Callout Examples
- Create `.claude/skills/generate-design-asset/assets/callout/EXAMPLES.md`
- Provide 2-3 examples for each of the 4 callout styles
- Examples should show:
  - Post context where callout would appear
  - Content being highlighted (insight, warning, metric)
  - Filled prompt template
  - Expected visual description
  - Integration markdown (how to embed in blog post)
- Include combination examples: post using multiple callout types

### Group E: Divider Asset Type [parallel: true, depends: C, model: auto]
Create divider asset type for section breaks.

#### Step E.1: Design Divider Styles
- Create `.claude/skills/generate-design-asset/assets/divider/STYLES.md`
- Design 3 divider style variants:
  1. **Minimal Line**: Clean horizontal line with subtle neon glow
  2. **Tech Pattern**: Geometric pattern strip (hexagons, circuits, nodes)
  3. **Glitch Break**: Horizontal glitch corruption effect
- For each style:
  - Write Nano Banana prompt template
  - Specify long horizontal dimensions (2560x200 or 2560x300)
  - Focus on horizontal composition with dark background
  - Define color variations based on section context
  - No text needed (pure visual separator)
- Add guidelines on divider spacing and usage frequency

#### Step E.2: Create Divider Examples
- Create `.claude/skills/generate-design-asset/assets/divider/EXAMPLES.md`
- Provide 2 examples for each of the 3 divider styles
- Show appropriate section contexts (major topic shifts, before/after deep technical sections)
- Include filled prompts and integration notes

### Group F: Diagram Asset Type [parallel: true, depends: C, model: auto]
Create diagram asset type for simple technical representations.

#### Step F.1: Design Diagram Styles
- Create `.claude/skills/generate-design-asset/assets/diagram/STYLES.md`
- Design 3 diagram style variants (all emphasizing simplicity due to Nano Banana limitations):
  1. **Two-Element Flow**: Input → Output with glowing connection
  2. **Three-Element Process**: A → B → C in linear or triangular arrangement
  3. **Abstract Representation**: Single element with atmospheric effects suggesting concept
- For each style:
  - Write Nano Banana prompt template with STRICT element limits (2-3 max)
  - Define simple geometric shapes only (cubes, spheres, hexagons)
  - Specify minimal text (1 word per element, 3 words total max)
  - Use glowing connections instead of arrows
  - Dimensions: 1920x1080 or 2560x1440 for clarity
- Include prominent warnings about Nano Banana's diagram limitations
- Emphasize abstract mood over technical accuracy

#### Step F.2: Create Diagram Examples
- Create `.claude/skills/generate-design-asset/assets/diagram/EXAMPLES.md`
- Provide 2-3 examples for each diagram style
- Show appropriate technical concepts that benefit from visual representation
- Include filled prompts with example element descriptions
- Add anti-patterns: what NOT to try (complex flowcharts, detailed architectures)

### Group G: DataCard Asset Type [parallel: true, depends: C, model: auto]
Create datacard asset type for metric visualization.

#### Step G.1: Design DataCard Styles
- Create `.claude/skills/generate-design-asset/assets/datacard/STYLES.md`
- Design 3 datacard style variants:
  1. **Metric Hero**: Large number/percentage with dramatic lighting on dark card
  2. **Comparison Card**: Two metrics side-by-side with visual contrast
  3. **Progress Indicator**: Visual representation of improvement/change (abstract bars, glowing fills)
- For each style:
  - Write Nano Banana prompt template
  - Define placeholders for metric values (numbers, percentages)
  - Specify square or portrait dimensions (1200x1200 or 1200x1600)
  - Focus on bold typography for numbers (even with spelling risk, numbers are clearer)
  - Use color to convey meaning (green=improvement, red=warning, cyan=neutral)
- Include guidelines on when datacards add value vs text callouts

#### Step G.2: Create DataCard Examples
- Create `.claude/skills/generate-design-asset/assets/datacard/EXAMPLES.md`
- Provide 2 examples for each of the 3 datacard styles
- Show metrics from existing or planned blog posts (performance improvements, cost savings, efficiency gains)
- Include filled prompts with actual metric values
- Document integration patterns (in-line, grouped, sidebar)

### Group H: Integration and Commands [parallel: false, depends: D, E, F, G, model: sonnet]
Update commands and integrate with blog workflow.

#### Step H.1: Create Wrapper Command
- Create `.claude/commands/generate-design-asset.md`
- Write user-facing documentation explaining the generalized skill
- Provide quick start examples for each asset type:
  - Banner generation (backward compatible)
  - Callout generation for blog post section
  - Divider generation between sections
  - Diagram generation for concept explanation
  - DataCard generation for metric highlight
- Document all command-line flags
- Include troubleshooting section
- Add references to skill documentation files

#### Step H.2: Update Banner Command
- Update `.claude/commands/generate_post_banner.md`
- Change to invoke new skill with `--asset-type banner` parameter
- Maintain all existing usage patterns for backward compatibility
- Add note about generalized skill and new asset types available
- Keep migration guide for users transitioning from old to new

#### Step H.3: Enhance New Post Command (Optional)
- Review `.claude/commands/new-post.md`
- Add optional section suggesting asset generation during post creation
- When creating post, after main content structure is created, suggest:
  - "Generate banner for this post? [Y/n]"
  - "This post has metrics. Generate datacards? [Y/n]"
  - "Generate callouts for key insights? [Y/n]"
- Keep suggestions non-intrusive and easily skippable
- Document integration pattern for future workflow enhancements

### Group I: Validation and Testing [parallel: false, depends: H, model: opus]
Comprehensive testing of all asset types and integration.

#### Step I.1: Test Each Asset Type
- For each of the 5 asset types (Banner, Callout, Divider, Diagram, DataCard):
  - Generate test asset using 2-3 different styles
  - Verify OpenRouter generation works correctly
  - Check output dimensions match specifications
  - Confirm files save to correct paths
  - Review visual output for brand consistency (dark mode, neon accents)
  - Validate Nano Banana limitations are respected (minimal text, simple composition)
- Document any style templates that need refinement
- Adjust prompts based on generation results

#### Step I.2: Test Content-to-Asset Recommendations
- Create test scenarios with different content types
- Verify CONTENT_ASSET_MAP decision tree produces appropriate recommendations
- Test edge cases:
  - Post with unclear category → should recommend safe defaults
  - Post suitable for multiple asset types → should suggest combination
  - Post with metrics → should recommend DataCard
  - Post with complex concepts → should recommend Diagram or Callout
- Adjust mapping rules based on recommendation quality

#### Step I.3: Test Integration Workflow
- Test end-to-end workflow from blog post creation through asset generation
- Verify command-line flags work correctly (`--asset-type`, `--style`, `--auto`, etc.)
- Test backward compatibility: old banner generation patterns still work
- Validate preview mode shows correct composed prompts
- Confirm error handling works (missing metadata, invalid asset type, API failures)
- Test regeneration workflow for all asset types

#### Step I.4: Validate Brand Consistency
- Review all generated test assets across asset types
- Verify dark mode aesthetic is consistent (no light backgrounds)
- Check neon accent colors align with ACIDBATH palette (cyan, magenta, purple, acid-green)
- Confirm tech-noir atmosphere is maintained
- Ensure all assets feel cohesive when used together in a blog post
- Document any style inconsistencies and update templates

## Testing Strategy

### Unit Tests
- **Asset Type Selection**: Workflow correctly identifies and loads appropriate asset type directory
- **Style Template Loading**: Each asset type's STYLES.md loads correctly and templates are parsable
- **Placeholder Filling**: Content variables correctly fill style template placeholders without errors
- **Dimension Validation**: Generated assets match specified dimensions for each asset type
- **Path Generation**: Output paths follow correct naming conventions and directory structure

### Integration Tests
- **OpenRouter Generation**: All style templates generate valid images via OpenRouter API
- **Content Analysis**: Post metadata correctly maps to asset type and style recommendations
- **Multi-Asset Generation**: Can generate multiple assets for single post (banner + callouts + dividers)
- **Command-Line Interface**: All flags (`--asset-type`, `--style`, `--auto`, `--preview-only`) work correctly
- **Backward Compatibility**: Existing banner generation workflows continue to function

### Edge Cases
- **Missing Metadata**: Asset generation works with minimal content (title only)
- **Invalid Asset Type**: Clear error message when unknown asset type specified
- **Invalid Style**: Error handling when non-existent style name provided
- **API Failures**: Graceful handling of OpenRouter rate limits or errors
- **Text Limitations**: Prompts with complex text are simplified or text is removed
- **Dimension Variations**: Non-standard dimensions can be specified if needed
- **File Conflicts**: Handles overwriting existing assets with user confirmation

## Acceptance Criteria

1. **Asset Type Library Complete**: 5 distinct asset types (Banner, Callout, Divider, Diagram, DataCard) fully documented with style libraries
2. **Progressive Disclosure Structure**: Skill organized with SKILL.md, ASSET_TYPES.md, CONTENT_ASSET_MAP.md, and asset-specific subdirectories following skills best practices
3. **Banner Migration Successful**: All existing banner functionality preserved and migrated into new asset type framework
4. **New Asset Types Functional**: Callout, Divider, Diagram, and DataCard asset types generate valid images with multiple style options
5. **Content-Aware Recommendations**: System analyzes content and recommends appropriate asset types and styles
6. **Brand Consistency**: All generated assets maintain ACIDBATH aesthetic (dark mode, neon accents, tech-noir atmosphere)
7. **Backward Compatibility**: Existing banner generation command and workflows continue to work
8. **Documentation Complete**: Comprehensive documentation for all asset types, styles, examples, and usage patterns
9. **Integration Ready**: Skill can be invoked from blog post creation workflows
10. **Quality Validation**: Generated assets meet Nano Banana best practices (minimal text, simple composition, dark backgrounds)

## Validation Commands

Execute these commands to validate the feature is complete:

```bash
# Verify core skill structure
test -f /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/SKILL.md && \
test -f /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/ASSET_TYPES.md && \
test -f /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/CONTENT_ASSET_MAP.md && \
echo "✓ Core skill files present" || echo "✗ Missing core skill files"

# Verify all 5 asset type directories exist
for asset in banner callout divider diagram datacard; do
  test -d /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/assets/$asset && \
  test -f /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/assets/$asset/STYLES.md && \
  test -f /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/assets/$asset/EXAMPLES.md && \
  echo "✓ Asset type '$asset' complete" || echo "✗ Asset type '$asset' missing files"
done

# Verify command files updated
test -f /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/commands/generate-design-asset.md && \
echo "✓ New command created" || echo "✗ New command missing"

test -f /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/commands/generate_post_banner.md && \
grep -q "generate-design-asset" /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/commands/generate_post_banner.md && \
echo "✓ Banner command updated to use new skill" || echo "✗ Banner command not updated"

# Count asset types defined in ASSET_TYPES.md
grep -c "^## Asset Type [0-9]:" /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/ASSET_TYPES.md | \
awk '$1 >= 5 {print "✓ All 5 asset types documented"; exit 0} {print "✗ Missing asset type documentation"; exit 1}'

# Verify each asset type has multiple styles
for asset in banner callout divider diagram datacard; do
  style_count=$(grep -c "^### Style [0-9]:" /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/assets/$asset/STYLES.md 2>/dev/null || echo 0)
  if [ "$style_count" -ge 3 ]; then
    echo "✓ Asset type '$asset' has $style_count styles"
  else
    echo "✗ Asset type '$asset' has insufficient styles ($style_count)"
  fi
done

# Verify skill frontmatter is valid
head -10 /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/SKILL.md | \
grep -q "^---" && \
grep -q "^name: generate-design-asset" /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/SKILL.md && \
echo "✓ Skill has valid frontmatter" || echo "✗ Invalid skill frontmatter"

# Verify examples exist for all asset types
for asset in banner callout divider diagram datacard; do
  example_count=$(grep -c "^### Example [0-9]" /Users/ameno/dev/acidbath2/trees/563e54cd/.claude/skills/generate-design-asset/assets/$asset/EXAMPLES.md 2>/dev/null || echo 0)
  if [ "$example_count" -ge 2 ]; then
    echo "✓ Asset type '$asset' has sufficient examples"
  else
    echo "✗ Asset type '$asset' needs more examples"
  fi
done

# Manual test: Generate one asset of each type
echo ""
echo "=== MANUAL TESTING REQUIRED ==="
echo "Run the following commands to generate test assets:"
echo ""
echo "1. Banner: /generate-design-asset --asset-type banner --style glass_object \"Test Post\" --preview-only"
echo "2. Callout: /generate-design-asset --asset-type callout --style insight_highlight \"Key Insight\" --preview-only"
echo "3. Divider: /generate-design-asset --asset-type divider --style tech_pattern --preview-only"
echo "4. Diagram: /generate-design-asset --asset-type diagram --style two_element_flow \"Process\" --preview-only"
echo "5. DataCard: /generate-design-asset --asset-type datacard --style metric_hero \"95% faster\" --preview-only"
echo ""
echo "Verify all prompts look correct, then remove --preview-only to generate actual assets"
```

## Notes

### Technical Considerations
- **OpenRouter Integration**: Continues to use existing `adws/adw_modules/openrouter_image.py` module; no changes needed to image generation infrastructure
- **Dimension Flexibility**: Each asset type has recommended dimensions but should support custom dimensions via optional flag
- **File Naming**: Standardize on pattern: `{slug}-{asset-type}-{identifier}.png` (e.g., `context-engineering-callout-insight-1.png`)
- **Asset Storage**: All assets save to `public/assets/posts/` for consistent public URL structure
- **Nano Banana Constraints**: More strict with callouts and diagrams than banners due to smaller sizes amplifying text issues

### Progressive Disclosure Benefits
- **Token Efficiency**: Only load asset type styles when that asset type is selected
- **Maintainability**: Each asset type can be updated independently
- **Extensibility**: New asset types can be added by creating new subdirectories without modifying core skill
- **Learning**: Users can explore individual asset type documentation without overwhelming main SKILL.md

### Design Philosophy
- **Asset Types Over One-Size-Fits-All**: Each asset type has unique requirements, constraints, and use cases
- **Content-Driven**: System recommends asset types based on content analysis, not just user request
- **Brand Consistency**: All assets feel like ACIDBATH through unified color palette and aesthetic principles
- **Simplicity Constraints**: Embrace Nano Banana limitations by designing for abstract beauty over technical accuracy
- **Workflow Integration**: Assets are created during blog post creation, not as afterthought

### Future Extensions (Not in Scope)
- **Icon Asset Type**: Small branded icons for inline use
- **Badge Asset Type**: Achievement/category badges for post metadata
- **Thumbnail Asset Type**: Social media preview thumbnails (different aspect ratios)
- **Animation Support**: If Nano Banana or OpenRouter adds animation capabilities
- **Style Mixing**: Combine elements from multiple styles into custom hybrid
- **Batch Generation**: Generate all recommended assets for a post in one command
- **A/B Testing**: Generate multiple variants of same asset for comparison
- **Asset Management**: Track which assets are used in which posts, enable regeneration

### Migration Notes
- **Banner Skill Deprecation**: `.claude/skills/generate-post-banner/` will eventually be marked deprecated and point to new skill
- **Existing Banners**: No need to regenerate existing banners; migration is for new content only
- **Learning Curve**: Users familiar with banner skill will find similar workflow in generalized skill
- **Documentation**: Update README.md to reference new skill as primary design asset generation tool

### Dependencies
- `adws/adw_modules/openrouter_image.py` - Already implemented and working
- OpenRouter API key must be configured (OPENROUTER_API_KEY environment variable)
- No new Python libraries required
- Skills system (built into Claude Code)
