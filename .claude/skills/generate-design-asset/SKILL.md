---
name: generate-design-asset
description: Generate high-quality, content-aware design assets (banners, callouts, dividers, diagrams, datacards) using advanced Nano Banana prompting with multiple style options for each asset type
allowed-tools: Bash, Write, Read, Grep, Glob
---

# Design Asset Generation Skill

Generate visually distinctive, high-quality design assets for ACIDBATH blog posts. This skill analyzes post content, recommends appropriate asset types and styles, composes advanced Nano Banana prompts, and generates professional images optimized for various placements throughout blog content.

---

## Overview

This skill transforms asset generation from simple commands into a comprehensive creative workflow:

1. **Asset Type Selection**: Choose the type of asset to generate (Banner, Callout, Divider, Diagram, DataCard)
2. **Content Analysis**: Analyzes post metadata or description to understand content type and context
3. **Style Recommendation**: Suggests 1-3 styles from the selected asset type's library
4. **Interactive Selection**: Presents style options with descriptions for user confirmation
5. **Prompt Composition**: Fills selected style template with content-specific variables
6. **Generation**: Calls OpenRouter (Nano Banana) to create the asset image
7. **Verification**: Confirms generation success and offers regeneration if needed
8. **Output**: Saves asset to appropriate location with proper naming

---

## Supported Asset Types

This skill supports 5 distinct asset types:

- **Banner**: Blog post header images (2560x1440, 16:9)
- **Callout**: In-text visual highlights for insights, warnings, data (1200x800 or 1600x900)
- **Divider**: Section break graphics (2560x200 or 2560x300, ultra-wide)
- **Diagram**: Simple 2-3 element technical representations (1920x1080 or 2560x1440)
- **DataCard**: Metric/statistic visualization cards (1200x1200 or 1200x1600, square/portrait)

See `ASSET_TYPES.md` for complete specifications of each asset type.

---

## Nano Banana Prompting Guidelines

**CRITICAL**: Follow these rules when composing prompts to avoid common Nano Banana failures.

### Rule 1: Simplicity Over Accuracy

Nano Banana struggles with complex interconnected diagrams. **Do NOT** create:
- Flowcharts with more than 3-4 connected elements
- Pipelines with multiple arrows and nodes
- Detailed system architectures with many components
- Isometric diagrams with intricate connections

**DO** create:
- Single focal objects with atmospheric effects
- Abstract representations of concepts
- Mood-driven visuals that evoke the topic
- Clean compositions with 1-2 primary elements

### Rule 2: Text Guidelines (1-3 Words Max)

Nano Banana makes spelling mistakes. When using text:

**Allowed**:
- 1-3 simple words maximum
- Common, short words (INPUT, OUTPUT, DATA, AGENT, etc.)
- ALL CAPS works best for readability
- Single word per element/shape

**Avoid**:
- Technical terminology (will be misspelled)
- Words longer than 8 characters
- Multiple words on same element
- Sentences or phrases

**Best practice**: Use text sparingly—one word labels on key elements only. For smaller assets (callouts, datacards), text should be even more limited.

### Rule 3: Abstract Over Literal

Don't try to literally depict technical concepts. **Instead**:
- Use visual metaphors (glass = sophistication, glitch = digital/tech)
- Focus on mood and atmosphere
- Let the image suggest rather than explain
- Prioritize aesthetic impact over technical accuracy

### Rule 4: Dark Mode Aesthetic

**ALL graphics must use dark backgrounds** to align with ACIDBATH brand:
- Deep blacks, dark grays, navy blues
- Neon accents against dark backgrounds
- High contrast focal elements
- Cyberpunk/tech-noir atmosphere

**Never use**:
- White or light backgrounds
- Pastel color schemes
- Bright, cheerful aesthetics

### Rule 5: ACIDBATH Brand Alignment

Visual identity guidelines:
- **Colors**: Cyan, magenta, purple, electric blue, acid-green as accents on dark backgrounds
- **Mood**: Technical, sophisticated, slightly edgy
- **Style**: Modern, minimal, high-contrast
- **Feel**: Professional but with personality

### Prompt Structure Template

```
[SUBJECT] - Simple, singular focal point
[MATERIAL/STYLE] - Glass, holographic, neon, glitch effects
[LIGHTING] - Dramatic, neon accents, rim lighting
[BACKGROUND] - Dark (black, deep navy, charcoal)
[ATMOSPHERE] - Subtle glow, particles, depth fog
[SPECS] - Dimensions based on asset type, aspect ratio
```

### Anti-Patterns to Avoid

❌ "A flowchart showing INPUT → PROCESS → OUTPUT with labeled boxes"
❌ "Technical diagram with annotations pointing to each component"
❌ "Isometric view of a system with multiple interconnected parts"
❌ "Complex data visualization with multiple axes and legends"

✅ "A glowing glass orb representing data transformation, floating against deep black"
✅ "Abstract holographic waves with cyan and magenta accents on dark background"
✅ "Single crystalline processor chip with dramatic rim lighting"
✅ "Bold number '95%' with dramatic neon glow on dark background"

---

## Workflow Sections

### Section 1: Asset Type Selection

**Objective**: Determine which type of asset to generate based on user input or content analysis.

**Inputs**:
- Command-line flag: `--asset-type [banner|callout|divider|diagram|datacard]`
- User manual selection (if no flag provided)
- Content context (post metadata, description, placement intent)

**Process**:

1. **If `--asset-type` flag provided**:
   - Validate asset type name (must be one of 5 supported types)
   - Load corresponding asset type specification from `ASSET_TYPES.md`
   - Skip interactive selection, proceed to content analysis

2. **If no flag provided**:
   Present asset type menu:
   ```
   📋 DESIGN ASSET TYPE SELECTION

   What type of asset do you want to generate?

   1. Banner - Blog post header image (2560x1440)
      → Use for: Post headers, main visual

   2. Callout - In-text visual highlight (1200x800)
      → Use for: Key insights, warnings, data points

   3. Divider - Section break graphic (2560x200)
      → Use for: Visual separation between major sections

   4. Diagram - Simple technical representation (1920x1080)
      → Use for: 2-3 element concept explanations

   5. DataCard - Metric visualization (1200x1200)
      → Use for: Statistics, benchmarks, improvements

   Enter number (1-5) or type asset name:
   ```

3. **Load Asset Type Specification**:
   - Read `ASSET_TYPES.md` for selected type
   - Extract dimensions, use cases, and integration notes
   - Determine default output path pattern

4. **Set Context for Subsequent Steps**:
   - Asset type name stored for later reference
   - Dimensions configured for generation
   - Style library path identified: `assets/{asset-type}/STYLES.md`

**Output**:
- Selected asset type (banner, callout, divider, diagram, or datacard)
- Asset type specifications loaded
- Ready to proceed to content analysis

---

### Section 2: Content Analysis

**Objective**: Extract key information from post to inform style selection and prompt composition.

**Inputs**:
- Post metadata file path (if available): `/path/to/post/metadata.json`
- OR post title + optional description/tags (manual input)
- Selected asset type from Section 1

**Process**:

1. **If metadata file provided**:
   ```bash
   # Read the metadata file
   cat /path/to/post/metadata.json
   ```
   Extract:
   - `category`: Content category (e.g., "AI Engineering", "Technical Analysis")
   - `tags`: Array of topic tags
   - `title`: Post title
   - `tone`: Writing tone (if available in `formatting` object)
   - `slug`: URL slug for file naming

2. **If manual input provided**:
   - Parse title for:
     - Provocative keywords ("wrong", "dead", "obsolete", "endgame")
     - Data indicators (numbers, metrics, percentages)
     - System keywords ("architecture", "framework", "agent")
     - Process keywords ("workflow", "build", "using")
   - Extract tags from description if provided
   - Identify content archetype:
     - Technical deep-dive (performance, optimization, benchmarks)
     - Provocative opinion (paradigm shifts, controversial claims)
     - How-to/tutorial (practical guides, implementations)
     - Architecture/framework (system design, infrastructure)

3. **Extract Placeholder Values** (based on asset type):

   **For Banners**:
   - Technical objects (e.g., "AI agent processor", "context window", "automation pipeline")
   - Metrics/measurements (e.g., "55,000 files", "36x faster", "20% reduction")
   - Headlines (for dramatic style)
   - System components (for isometric diagrams)
   - Color preferences based on topic

   **For Callouts**:
   - Key insight text (1-2 words max)
   - Warning/alert context
   - Metric value for data spotlight
   - Concept name for tech detail

   **For Dividers**:
   - Section transition theme
   - Color based on content tone (cyan for technical, magenta for creative, orange for warnings)

   **For Diagrams**:
   - Main concept (extremely simplified)
   - 2-3 element names (single words)
   - Flow direction

   **For DataCards**:
   - Metric value (number, percentage, time)
   - Comparison values (before/after, A vs B)
   - Improvement indicators (up/down, better/worse)

**Output**:
- Structured content summary with extracted metadata
- Identified content archetype
- Preliminary placeholder values for prompt templates
- Asset type context (how asset will be used in this post)

---

### Section 3: Style Recommendation

**Objective**: Apply content-to-style mapping rules to suggest appropriate styles from selected asset type's library.

**Process**:

1. **Load Asset Type's Style Library**:
   ```bash
   # Load styles for selected asset type
   cat .claude/skills/generate-design-asset/assets/{asset-type}/STYLES.md
   ```

2. **Load Mapping Rules**: Reference `CONTENT_ASSET_MAP.md` decision tree logic

3. **Score Each Style** (asset-type specific):
   ```python
   # Example for Banner asset type
   scores = {
       "glass_object": 0,
       "isometric": 0,
       "blueprint": 0,
       "dramatic": 0,
       "glitch": 1  # Universal baseline
   }

   # Example for Callout asset type
   scores = {
       "insight_highlight": 0,
       "warning_alert": 0,
       "data_spotlight": 0,
       "tech_detail": 1  # Universal baseline
   }
   ```

4. **Apply Scoring Logic**:

   **Category Matching** (+3 points):
   - Match content category to asset type style preferences
   - Example: "Technical Analysis" → Blueprint style (for banners), Data Spotlight (for callouts)

   **Tag Matching** (+2 points each, max +6):
   - Architecture tags → Certain styles per asset type
   - Workflow tags → Process-oriented styles
   - Performance tags → Data-focused styles
   - Opinion tags → Dramatic styles

   **Title Sentiment** (+1 to +2 points):
   - Provocative keywords → Dramatic styles
   - Data indicators → Data-focused styles
   - System keywords → Architectural styles
   - Process keywords → Flow-oriented styles

   **Formatting Metadata** (+0.5 to +2 points):
   - `tone: "provocative"` → Dramatic styles
   - `tone: "technical"` → Precision styles
   - `hasDiagrams: true` → Complement existing visuals

5. **Rank Styles**:
   - Sort by score (highest to lowest)
   - Primary recommendation: Highest score
   - Alternative 1: Second highest
   - Alternative 2: Third highest or universal fallback

**Output**:
- Primary style recommendation with score
- 2 alternative styles
- Brief rationale for each recommendation

---

### Section 4: Interactive Selection

**Objective**: Present style options to user and get confirmation or allow override.

**Process**:

1. **Present Recommendations**:
   ```
   📋 STYLE RECOMMENDATIONS for {Asset Type}: "[Post Title/Context]"

   Based on content analysis:
   - Category: [category]
   - Content Type: [archetype]
   - Key Tags: [top 3-5 tags]
   - Asset Use: [how asset will be used]

   Recommended Styles:

   1. [PRIMARY STYLE NAME] (Score: X) ⭐ RECOMMENDED
      → Best for: [use case]
      → Visual: [brief description]
      → Example: See assets/{asset-type}/EXAMPLES.md #[example number]

   2. [ALTERNATIVE 1 NAME] (Score: Y)
      → Best for: [use case]
      → Visual: [brief description]

   3. [ALTERNATIVE 2 NAME] (Score: Z)
      → Best for: [use case]
      → Visual: [brief description]

   Options:
   - Press ENTER to use recommended style (1)
   - Type 2 or 3 to select alternative
   - Type "preview" to see composed prompts before generating
   - Type style name to override with specific style
   ```

2. **Handle Command Flags** (if provided at skill invocation):
   - `--style [name]`: Skip recommendation, use specified style directly
   - `--auto`: Use primary recommendation automatically without prompt
   - `--preview-only`: Show composed prompt without generating image

3. **Get User Confirmation**:
   - If interactive: Wait for user input
   - If `--auto` flag: Proceed with primary recommendation
   - If `--style` flag: Validate style name, proceed with specified style

**Output**:
- Selected style name
- User confirmation received (or auto-proceed flag honored)

---

### Section 5: Prompt Composition

**Objective**: Fill selected style template with content-specific variables to create final Nano Banana prompt.

**Process**:

1. **Load Style Template**:
   Read appropriate section from `assets/{asset-type}/STYLES.md` based on selected style

2. **Map Content to Placeholders**:

   Placeholders vary by asset type and style. Examples:

   **Banner (Glass Object Style)**:
   - `[TECHNICAL_OBJECT]`: From content analysis (e.g., "AI agent processing unit")
   - `[SIMPLE_SHAPE_DESCRIPTION]`: Structural details (e.g., "hexagonal chip with beveled edges")
   - Color adjustments based on topic

   **Callout (Insight Highlight Style)**:
   - `[INSIGHT_TEXT]`: 1-2 word key point (e.g., "95% FASTER")
   - `[GLOW_COLOR]`: Based on content tone (cyan, magenta, acid-green)
   - `[BACKGROUND_TONE]`: Dark variant selection

   **Divider (Tech Pattern Style)**:
   - `[PATTERN_TYPE]`: Geometric pattern (hexagons, circuits, nodes)
   - `[ACCENT_COLOR]`: Section theme color
   - `[INTENSITY]`: Subtle or prominent based on context

   **Diagram (Two-Element Flow Style)**:
   - `[ELEMENT_1]`: First concept (single word)
   - `[ELEMENT_2]`: Second concept (single word)
   - `[CONNECTION_DESCRIPTION]`: How they connect (glowing line, energy stream)

   **DataCard (Metric Hero Style)**:
   - `[METRIC_VALUE]`: Number/percentage (e.g., "95%", "10x", "$4.2K")
   - `[METRIC_CONTEXT]`: Brief context (e.g., "FASTER", "SAVED", "IMPROVEMENT")
   - `[EMPHASIS_COLOR]`: Success green, warning orange, neutral cyan

3. **Apply Smart Defaults**:
   - If placeholder value not clear from content: Use template-provided defaults
   - If color not specified: Use brand colors (cyan/blue for technical, orange for warnings, purple for creative, acid-green for success)
   - If measurements unavailable: Use placeholder values like "X% improvement"

4. **Validation Check**:
   - Ensure all `[PLACEHOLDER]` variables are filled
   - Verify no contradictory instructions
   - Confirm dimensions match asset type specifications
   - Check color choices complement each other
   - Verify text limitations respected (more strict for smaller assets)

5. **Preview Mode** (if `--preview-only` flag):
   ```
   🎨 COMPOSED PROMPT PREVIEW

   Asset Type: [Asset Type Name]
   Style: [Selected Style Name]
   Context: [Post Title or Description]

   === Nano Banana Prompt ===
   [Full composed prompt with all placeholders filled]
   === End Prompt ===

   Dimensions: [width]x[height]
   Output Path: [file path]
   Estimated length: [word count] words

   Options:
   - Press ENTER to proceed with generation
   - Type "edit" to manually modify prompt
   - Type "back" to select different style
   ```

**Output**:
- Fully composed Nano Banana prompt with all placeholders filled
- Validation passed (or errors listed)
- Preview shown if requested

---

### Section 6: Generation

**Objective**: Generate the asset image using OpenRouter API with Nano Banana model.

**Process**:

1. **Prepare Generation Script**:

   Write a temporary Python script that uses the `openrouter_image` module:

   ```python
   # /tmp/generate_asset.py
   from adws.adw_modules.openrouter_image import generate_banner, AspectRatio

   prompt = """[composed prompt from Section 5]"""

   # Determine aspect ratio based on asset type
   aspect_ratio_map = {
       "banner": AspectRatio.LANDSCAPE,      # 16:9
       "callout": AspectRatio.LANDSCAPE,     # 4:3 or 16:9
       "divider": AspectRatio.ULTRAWIDE,     # Custom ultra-wide
       "diagram": AspectRatio.LANDSCAPE,     # 16:9
       "datacard": AspectRatio.SQUARE        # 1:1 or portrait
   }

   result = generate_banner(
       prompt=prompt,
       output_path="/Users/ameno/dev/acidbath2/public/assets/posts/[slug]-[asset-type]-[identifier].png",
       aspect_ratio=aspect_ratio_map["[asset-type]"]
   )

   if result.success:
       print(f"SUCCESS: {result.file_path}")
       if result.usage:
           print(f"Tokens used: {result.usage.get('total_tokens', 'N/A')}")
   else:
       print(f"FAILED: {result.error}")
   ```

2. **Execute Generation**:
   ```bash
   cd /Users/ameno/dev/acidbath2 && uv run python /tmp/generate_asset.py
   ```

   - Generation typically takes 30-60 seconds
   - OpenRouter handles rate limiting automatically
   - Output is saved directly to the specified path

3. **Handle Errors**:
   - **API Key Missing**:
     ```
     ❌ ERROR: OPENROUTER_API_KEY not set

     Please configure your OpenRouter API key:
     1. Get a key from https://openrouter.ai/keys
     2. Add to ~/.zshrc: export OPENROUTER_API_KEY="your-key"
     3. Run: source ~/.zshrc
     ```

   - **Rate Limit**:
     ```
     ⚠️  Rate limit hit. Waiting and retrying...
     ```
     The module handles rate limits automatically with retry logic.

   - **Generation Failed**:
     ```
     ❌ ERROR: Generation failed
     Reason: [error message]

     Options:
     - Type "retry" to attempt generation again
     - Type "simplify" to use simpler prompt template
     - Type "back" to select different style
     ```

4. **Show Progress**:
   ```
   🎨 Generating {asset type} via OpenRouter (Nano Banana)...

   Asset Type: [Asset Type]
   Style: [Selected Style]
   Context: [Post Title or Description]
   Output: [file path]

   ⏳ This may take 30-60 seconds for complex prompts...
   ```

**Output**:
- Generated image file at specified path
- Token usage statistics
- Or error message with recovery options

---

### Section 7: Verification

**Objective**: Confirm image generation success and offer regeneration if needed.

**Process**:

1. **Verify File Exists**:
   ```bash
   # Check if asset file was created
   ls -lh /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-[asset-type]-[identifier].png
   ```

2. **Show Success**:
   ```
   ✅ ASSET GENERATED SUCCESSFULLY

   Type: [Asset Type]
   Style: [Selected Style]
   File: /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-[asset-type]-[identifier].png
   Size: [file size]
   Dimensions: [width]x[height]

   Asset is ready for use in blog post.

   Options:
   - Press ENTER to finish
   - Type "view" to see file path for manual review
   - Type "regenerate" to create new version with same style
   - Type "try-different" to select different style and regenerate
   ```

3. **If File Not Created**:
   ```
   ❌ VERIFICATION FAILED

   Asset file not found at expected location.
   Possible issues:
   - Generation failed silently
   - File permission issues
   - Incorrect output path

   Options:
   - Type "retry" to attempt generation again
   - Type "debug" to see detailed error log
   ```

4. **Regeneration Workflow** (if user requests):
   - **Same Style**: Jump back to Section 6 (Generation) with same prompt
   - **Different Style**: Jump back to Section 4 (Interactive Selection)
   - **Edit Prompt**: Allow manual prompt modification, then proceed to Section 6

**Output**:
- Confirmation of successful generation
- File path for asset image
- Or regeneration workflow if requested

---

### Section 8: Output

**Objective**: Finalize asset placement and provide usage information.

**Process**:

1. **Confirm Output Location**:
   ```
   📁 ASSET OUTPUT

   Type: [Asset Type]
   Location: /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-[asset-type]-[identifier].png
   Public URL: /assets/posts/[slug]-[asset-type]-[identifier].png

   To use in blog post:
   - [Integration method based on asset type]
   - Dimensions: [width]x[height]
   - Aspect ratio: [ratio]
   ```

2. **Provide Integration Guidance** (asset-type specific):

   **Banner**:
   ```
   - Ensure post metadata references banner path
   - Banner optimized for 2560x1440 resolution
   - Aspect ratio: 16:9 for blog headers
   ```

   **Callout**:
   ```markdown
   - Use inline in markdown:
   ![Key Insight](/assets/posts/[slug]-callout-insight-1.png)

   - Or enhance Astro Callout component with image prop
   ```

   **Divider**:
   ```markdown
   - Insert between major sections:
   ![Section Break](/assets/posts/[slug]-divider-1.png)
   ```

   **Diagram**:
   ```markdown
   - Use to explain concepts:
   ![Concept Diagram](/assets/posts/[slug]-diagram-flow.png)
   ```

   **DataCard**:
   ```markdown
   - Highlight metrics inline or in sidebar:
   ![Performance Metric](/assets/posts/[slug]-datacard-perf-1.png)
   ```

3. **Summary Report**:
   ```
   📊 GENERATION SUMMARY

   Asset Type: [Asset Type Name]
   Style: [Selected Style Name]
   Context: [Post Title or Description]
   Rationale: [Why this style was recommended]

   Content Analysis:
   - Category: [category]
   - Archetype: [content type]
   - Key Tags: [tags]
   - Asset Purpose: [how asset enhances content]

   Prompt Details:
   - Template: [style name]
   - Key Placeholders: [main variables filled]
   - Prompt Length: [word count] words

   Output:
   - File: [path]
   - Size: [file size]
   - Dimensions: [width]x[height]

   ✅ Asset generation complete.
   ```

**Output**:
- Asset file saved at correct location
- Integration guidance provided
- Complete summary report

---

## Command-Line Flags

Support for command-line arguments to streamline workflow:

### `--asset-type [type]`
**Usage**: `/generate-design-asset --asset-type callout "Key Insight"`
**Behavior**: Skip asset type selection, use specified type directly
**Valid Values**: `banner`, `callout`, `divider`, `diagram`, `datacard`

### `--style [name]`
**Usage**: `/generate-design-asset --asset-type banner "Post Title" --style glass_object`
**Behavior**: Skip style recommendation, use specified style directly
**Valid Values**: Depends on asset type (see ASSET_TYPES.md)

### `--auto`
**Usage**: `/generate-design-asset --slug post-slug --asset-type banner --auto`
**Behavior**: Use primary asset type and style recommendation automatically without interactive confirmation
**Use Case**: Batch processing, automation scripts

### `--preview-only`
**Usage**: `/generate-design-asset --asset-type callout "Key Point" --preview-only`
**Behavior**: Show composed prompt without generating image
**Use Case**: Reviewing prompt quality, debugging, learning

### `--slug [slug]`
**Usage**: `/generate-design-asset --slug context-window-bleeding --asset-type banner`
**Behavior**: Use slug to find and load post metadata automatically
**Requires**: Metadata file exists at `blog/posts/[slug]/metadata.json`

### `--metadata [path]`
**Usage**: `/generate-design-asset --metadata /path/to/metadata.json --asset-type banner`
**Behavior**: Load metadata from specified file path
**Use Case**: Non-standard post locations

---

## Error Handling

### Missing Metadata
**Scenario**: No metadata file, only title/description provided
**Handling**:
1. Extract what information possible from title
2. Prompt user for additional context if needed
3. Use universal fallback styles if still unclear
4. Proceed with limited placeholder filling

### Invalid Asset Type
**Scenario**: `--asset-type invalid_name` provided
**Handling**:
```
❌ ERROR: Invalid asset type "invalid_name"

Valid asset types:
- banner (Blog post headers)
- callout (In-text visual highlights)
- divider (Section break graphics)
- diagram (Simple technical representations)
- datacard (Metric visualization cards)

Please specify a valid asset type or omit --asset-type flag for interactive selection.
```

### Invalid Style Name
**Scenario**: `--style invalid_name` provided for selected asset type
**Handling**:
```
❌ ERROR: Invalid style name "invalid_name" for asset type "[type]"

Valid styles for [asset type]:
[List of valid styles from assets/{asset-type}/STYLES.md]

Please specify a valid style name or omit --style flag for recommendations.
```

### OpenRouter API Key Missing
**Scenario**: OPENROUTER_API_KEY environment variable not set
**Handling**:
```
❌ ERROR: OPENROUTER_API_KEY not configured

Asset generation requires an OpenRouter API key.

Setup instructions:
1. Get an API key from https://openrouter.ai/keys
2. Add to ~/.zshrc: export OPENROUTER_API_KEY="your-key-here"
3. Reload shell: source ~/.zshrc

The skill uses OpenRouter's Nano Banana (Gemini 2.5 Flash Image) model.
```

### OpenRouter Rate Limit
**Scenario**: API rate limit exceeded
**Handling**:
```
⚠️  Rate limit exceeded. The module will automatically retry.

If persistent, check your OpenRouter usage at https://openrouter.ai/usage
```

### File Permission Issues
**Scenario**: Cannot write to output directory
**Handling**:
```
❌ ERROR: Permission denied writing to output path

Path: /Users/ameno/dev/acidbath2/public/assets/posts/[file]

Possible solutions:
1. Check directory exists: mkdir -p /Users/ameno/dev/acidbath2/public/assets/posts/
2. Check write permissions: ls -ld /Users/ameno/dev/acidbath2/public/assets/posts/
3. Try alternative output path with --output flag

Please resolve permission issues and retry.
```

---

## Integration with Existing Command

This skill extends the old `.claude/commands/generate_post_banner.md` command with generalized capabilities. For backward compatibility, the old command file will be updated to invoke this skill with `--asset-type banner`.

**Migration Path**:
- Old command: Simple banner-only generation
- New skill: Multi-asset-type, content-aware, interactive workflow
- Transition: Old command points to skill with banner asset type

---

## Usage Examples

### Example 1: Generate Banner with Metadata
```
/generate-design-asset --slug prompts-are-the-new-code --asset-type banner
```
**Flow**:
1. Loads metadata from `blog/posts/01-prompts-are-the-new-code/metadata.json`
2. Analyzes content → Identifies provocative opinion piece
3. Recommends: Dramatic style (if available) or Glitch
4. User confirms or selects alternative
5. Generates banner
6. Saves to `/public/assets/posts/prompts-are-the-new-code-banner.png`

### Example 2: Generate Callout for Key Insight
```
/generate-design-asset --asset-type callout "95% faster"
```
**Flow**:
1. Asset type: Callout
2. Analyzes content → Performance metric
3. Recommends: Data Spotlight style
4. User confirms
5. Generates callout with "95% FASTER" in dramatic neon
6. Prompts for slug to determine output filename

### Example 3: Generate Section Divider
```
/generate-design-asset --asset-type divider --style tech_pattern --auto
```
**Flow**:
1. Asset type: Divider
2. Style: tech_pattern (specified, skip recommendation)
3. Auto mode: Skip confirmation
4. Generates geometric pattern divider
5. Saves automatically

### Example 4: Generate Diagram with Preview
```
/generate-design-asset --asset-type diagram "Input to Output" --preview-only
```
**Flow**:
1. Asset type: Diagram
2. Analyzes → Two-element flow
3. Recommends: Two-Element Flow style
4. Shows composed prompt
5. User can review, edit, or proceed

### Example 5: Generate DataCard for Metric
```
/generate-design-asset --asset-type datacard "36x improvement" --style metric_hero
```
**Flow**:
1. Asset type: DataCard
2. Style: metric_hero (specified)
3. Composes prompt with "36x" as hero metric
4. Generates dramatic visualization
5. Saves square/portrait metric card

---

## References

- **Asset Type Specs**: See `ASSET_TYPES.md` for complete specifications
- **Style Templates**: See `assets/{asset-type}/STYLES.md` for prompt templates
- **Mapping Rules**: See `CONTENT_ASSET_MAP.md` for decision tree logic
- **Examples**: See `assets/{asset-type}/EXAMPLES.md` for concrete filled prompts

---

## Troubleshooting

### Issue: Style recommendation doesn't match content
**Solution**: Override with `--style [name]` flag or provide more detailed metadata/tags

### Issue: Generated image doesn't match expectations
**Solution**:
1. Use `--preview-only` to review composed prompt
2. Manually edit prompt to adjust details
3. Refer to asset type's STYLES.md troubleshooting section
4. Try different style that may better suit content

### Issue: Prompt too generic
**Solution**:
1. Provide richer metadata with more tags
2. Add content description when invoking skill
3. Manually fill placeholders during interactive prompt

### Issue: Generation takes too long
**Solution**:
1. Complex photorealistic styles take 45-60 seconds
2. Use simpler styles for faster generation
3. Increase timeout if needed

### Issue: Asset dimensions not suitable
**Solution**:
1. Check ASSET_TYPES.md for recommended dimensions
2. Some asset types support custom dimensions via optional flag
3. Consider different asset type if dimensions are critical

---

## Version History

- **v2.0** (2025-12-24): Generalized from banner-only to multi-asset-type system with 5 asset types
- **v1.1** (2025-12-23): Replaced MCP dependency with OpenRouter API integration
- **v1.0** (2025-12-23): Initial banner skill
