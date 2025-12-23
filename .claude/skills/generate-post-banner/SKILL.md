---
name: generate-post-banner
description: Generate high-quality, content-aware blog post banner images using advanced Nano Banana prompting techniques with multiple style options
allowed-tools: mcp__nano-banana__generate_image, Bash, Write, Read, Grep, Glob
---

# Banner Generation Skill

Generate visually distinctive, high-quality banner images for ACIDBATH blog posts. This skill analyzes post content, recommends appropriate visual styles, composes advanced Nano Banana prompts, and generates professional banner images optimized for blog headers.

---

## Overview

This skill transforms banner generation from a simple command into a comprehensive creative workflow:

1. **Content Analysis**: Analyzes post metadata or title/description to understand content type and tone
2. **Style Recommendation**: Suggests 1-3 banner styles based on content mapping rules
3. **Interactive Selection**: Presents style options with descriptions for user confirmation
4. **Prompt Composition**: Fills selected style template with content-specific variables
5. **Generation**: Calls Nano Banana MCP to create the banner image
6. **Verification**: Confirms generation success and offers regeneration if needed
7. **Output**: Saves banner to appropriate location with proper naming

---

## Workflow Sections

### Section 1: Content Analysis

**Objective**: Extract key information from post to inform style selection and prompt composition.

**Inputs**:
- Post metadata file path (if available): `/path/to/post/metadata.json`
- OR post title + optional description/tags (manual input)

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

3. **Extract Placeholder Values**:
   Based on content analysis, identify values for common prompt placeholders:
   - Technical objects (e.g., "AI agent processor", "context window", "automation pipeline")
   - Metrics/measurements (e.g., "55,000 files", "36x faster", "20% reduction")
   - Headlines (for newspaper style)
   - System components (for isometric diagrams)
   - Color preferences based on topic (performance issues → red/orange, architecture → cyan/blue)

**Output**:
- Structured content summary with extracted metadata
- Identified content archetype
- Preliminary placeholder values for prompt templates

---

### Section 2: Style Recommendation

**Objective**: Apply content-to-style mapping rules to suggest appropriate banner styles.

**Process**:

1. **Load Mapping Rules**: Reference `CONTENT_STYLE_MAP.md` decision tree logic

2. **Score Each Style**:
   ```python
   scores = {
       "glass_object": 0,
       "isometric": 0,
       "blueprint": 0,
       "newspaper": 0,
       "glitch": 1  # Universal baseline
   }
   ```

3. **Apply Scoring Logic**:

   **Category Matching** (+3 points):
   - "AI Engineering" → Glass Object +3
   - "Technical Analysis" or "Deep Dive" → Technical Blueprint +3
   - "AI Development" → Isometric Diagram +3

   **Tag Matching** (+2 points each, max +6):
   - Architecture tags (`architecture`, `framework`, `SDK`, `system design`) → Glass Object +2
   - Workflow tags (`workflow`, `automation`, `process`, `sub-agents`) → Isometric +2
   - Performance tags (`performance`, `optimization`, `benchmark`, `cost`, `token`) → Blueprint +2
   - Opinion tags (`opinion`, `paradigm`, `controversial`, `future`) → Newspaper +2

   **Title Sentiment** (+1 to +2 points):
   - Provocative keywords ("wrong", "dead", "obsolete") → Newspaper +2
   - Data indicators (numbers, metrics) → Blueprint +2
   - System keywords → Glass Object +1
   - Process keywords → Isometric +1

   **Formatting Metadata** (+0.5 to +2 points):
   - `tone: "provocative"` → Newspaper +2
   - `tone: "technical"` → Blueprint/Glass +1 each
   - `hasDiagrams: true` → Isometric +1

4. **Rank Styles**:
   - Sort by score (highest to lowest)
   - Primary recommendation: Highest score
   - Alternative 1: Second highest
   - Alternative 2: Third highest or Enhanced Glitch (fallback)

**Output**:
- Primary style recommendation with score
- 2 alternative styles
- Brief rationale for each recommendation

---

### Section 3: Interactive Selection

**Objective**: Present style options to user and get confirmation or allow override.

**Process**:

1. **Present Recommendations**:
   ```
   📋 BANNER STYLE RECOMMENDATIONS for "[Post Title]"

   Based on content analysis:
   - Category: [category]
   - Content Type: [archetype]
   - Key Tags: [top 3-5 tags]

   Recommended Styles:

   1. [PRIMARY STYLE NAME] (Score: X) ⭐ RECOMMENDED
      → Best for: [use case]
      → Visual: [brief description]
      → Example: See EXAMPLES.md #[example number]

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

### Section 4: Prompt Composition

**Objective**: Fill selected style template with content-specific variables to create final Nano Banana prompt.

**Process**:

1. **Load Style Template**: Read appropriate section from `STYLE_LIBRARY.md` based on selected style

2. **Map Content to Placeholders**:

   **For Glass Object Technical**:
   - `[TECHNICAL_OBJECT]`: From content analysis (e.g., "AI agent processing unit", "context window allocator", "API gateway server")
   - `[OBJECT_DESCRIPTION]`: Structural details (e.g., "modular processor chip with connection pathways", "transparent server chassis with status LED array")
   - Color adjustments based on topic

   **For Isometric Technical Diagram**:
   - `[SYSTEM_DESCRIPTION]`: Main system being visualized (e.g., "multi-agent research workflow", "file-based automation pipeline")
   - `[KEY_COMPONENTS]`: Main elements (e.g., "parent agent, research sub-agents, context file")
   - `[FOREGROUND_LAYER]`: Primary elements description
   - `[MIDGROUND_LAYER]`: Supporting elements
   - `[BACKGROUND_LAYER]`: Context elements
   - `[COLOR_SCHEME]`: Based on content tone

   **For Technical Blueprint**:
   - `[TECHNICAL_SUBJECT]`: What the blueprint shows (e.g., "context window allocation", "performance comparison")
   - `[PRIMARY_ELEMENTS]`: Main schematic components
   - `[METRIC_1/2/3]`: Actual metrics from post (e.g., "55,000 files", "36x faster", "20% overhead")
   - `[COLOR_SCHEME]`: Technical colors (cyan/white or orange/yellow warnings)

   **For Newspaper Front Page**:
   - `[HEADLINE]`: Provocative headline derived from title (keep to 5-10 words max)
   - `[PHOTO_DESCRIPTION]`: Supporting image concept (e.g., "engineer frustrated at terminal", "server room with glowing lights")
   - `[PUBLICATION_NAME]`: "ACIDBATH TECHNICAL JOURNAL" or variant
   - `[NEWSPAPER_DATE]`: Post publish date
   - `[SUBHEADLINE]`: Supporting text from subtitle or description

   **For Enhanced Glitch Corruption**:
   - `[SUBJECT_DESCRIPTION]`: Abstract representation of topic (e.g., "corrupted debugging interface", "glitching neural network")
   - `[PRIMARY_COLOR]`: Neon accent color (cyan, magenta, purple) based on topic
   - `[CORRUPTION_LEVEL]`: "moderate" for clarity, "heavy" if appropriate
   - `[GLITCH_TYPE_1/2/3]`: Specific corruption effects

3. **Apply Smart Defaults**:
   - If placeholder value not clear from content: Use template-provided defaults
   - If color not specified: Use brand colors (cyan/blue for technical, orange for warnings, purple for creative)
   - If measurements unavailable: Use placeholder values like "X% improvement" or "N tokens"

4. **Validation Check**:
   - Ensure all `[PLACEHOLDER]` variables are filled
   - Verify no contradictory instructions (e.g., "shallow depth of field" + "everything in focus")
   - Confirm technical specifications included (2560x1440, 16:9 aspect ratio)
   - Check color choices complement each other

5. **Preview Mode** (if `--preview-only` flag):
   ```
   🎨 COMPOSED PROMPT PREVIEW

   Style: [Selected Style Name]
   Post: [Post Title]

   === Nano Banana Prompt ===
   [Full composed prompt with all placeholders filled]
   === End Prompt ===

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

### Section 5: Generation

**Objective**: Call Nano Banana MCP to generate the banner image.

**Process**:

1. **Prepare MCP Call**:
   ```
   Tool: mcp__nano-banana__generate_image
   Parameters:
   - prompt: [composed prompt from Section 4]
   - output_path: /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png
   ```

2. **Invoke Nano Banana MCP**:
   - Call `mcp__nano-banana__generate_image` with composed prompt
   - Include timeout handling (complex prompts may take longer)
   - Show generation progress if MCP provides status updates

3. **Handle MCP Errors**:
   - **MCP Unavailable**:
     ```
     ❌ ERROR: Nano Banana MCP server not available

     Please ensure MCP server is running:
     1. Check MCP configuration: claude mcp list
     2. Verify nano-banana server is installed and running
     3. Restart MCP server if needed

     Cannot proceed with banner generation without MCP access.
     ```

   - **Prompt Too Long**:
     ```
     ⚠️  WARNING: Prompt may exceed MCP length limits

     Attempting to simplify prompt by removing optional details...
     [Retry with simplified prompt]
     ```

   - **Generation Timeout**:
     ```
     ⏱️  TIMEOUT: Generation taking longer than expected

     Complex photorealistic prompts may require extended processing.
     Continuing to wait... (timeout: 300s)
     ```

   - **Other MCP Errors**:
     ```
     ❌ ERROR: Generation failed
     Reason: [MCP error message]

     Options:
     - Type "retry" to attempt generation again
     - Type "simplify" to use simpler prompt template
     - Type "back" to select different style
     ```

4. **Show Progress**:
   ```
   🎨 Generating banner...

   Style: [Selected Style]
   Post: [Post Title]
   Output: [file path]

   ⏳ Calling Nano Banana MCP... (this may take 30-60 seconds for complex prompts)
   ```

**Output**:
- Generated image file at specified path
- Or error message with recovery options

---

### Section 6: Verification

**Objective**: Confirm image generation success and offer regeneration if needed.

**Process**:

1. **Verify File Exists**:
   ```bash
   # Check if banner file was created
   ls -lh /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png
   ```

2. **Show Success**:
   ```
   ✅ BANNER GENERATED SUCCESSFULLY

   File: /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png
   Size: [file size]
   Style: [Selected Style]

   Banner is ready for use in blog post.

   Options:
   - Press ENTER to finish
   - Type "view" to see file path for manual review
   - Type "regenerate" to create new version with same style
   - Type "try-different" to select different style and regenerate
   ```

3. **If File Not Created**:
   ```
   ❌ VERIFICATION FAILED

   Banner file not found at expected location.
   Possible issues:
   - MCP generation failed silently
   - File permission issues
   - Incorrect output path

   Options:
   - Type "retry" to attempt generation again
   - Type "debug" to see detailed error log
   ```

4. **Regeneration Workflow** (if user requests):
   - **Same Style**: Jump back to Section 5 (Generation) with same prompt
   - **Different Style**: Jump back to Section 3 (Interactive Selection)
   - **Edit Prompt**: Allow manual prompt modification, then proceed to Section 5

**Output**:
- Confirmation of successful generation
- File path for banner image
- Or regeneration workflow if requested

---

### Section 7: Output

**Objective**: Finalize banner placement and provide usage information.

**Process**:

1. **Confirm Output Location**:
   ```
   📁 BANNER OUTPUT

   Location: /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png
   Public URL: /assets/posts/[slug]-banner.png

   To use in blog post:
   - Ensure post metadata references banner path
   - Banner optimized for 2560x1440 resolution
   - Aspect ratio: 16:9 for blog headers
   ```

2. **Update Post Metadata** (optional):
   If post metadata file exists, offer to add banner reference:
   ```json
   {
     ...
     "banner": {
       "path": "/assets/posts/[slug]-banner.png",
       "style": "[Selected Style Name]",
       "generatedDate": "[timestamp]"
     }
   }
   ```

3. **Summary Report**:
   ```
   📊 GENERATION SUMMARY

   Post: [Post Title]
   Style: [Selected Style Name]
   Rationale: [Why this style was recommended]

   Content Analysis:
   - Category: [category]
   - Archetype: [content type]
   - Key Tags: [tags]

   Prompt Details:
   - Template: [style name]
   - Key Placeholders: [main variables filled]
   - Prompt Length: [word count] words

   Output:
   - File: [path]
   - Size: [file size]
   - Resolution: 2560x1440

   ✅ Banner generation complete.
   ```

**Output**:
- Banner file saved at correct location
- Optional metadata update
- Complete summary report

---

## Command-Line Flags

Support for command-line arguments to streamline workflow:

### `--style [name]`
**Usage**: `/generate-post-banner "Post Title" --style glass_object`
**Behavior**: Skip style recommendation, use specified style directly
**Valid Values**: `glass_object`, `isometric`, `blueprint`, `newspaper`, `glitch`

### `--auto`
**Usage**: `/generate-post-banner --slug post-slug --auto`
**Behavior**: Use primary style recommendation automatically without interactive confirmation
**Use Case**: Batch processing, automation scripts

### `--preview-only`
**Usage**: `/generate-post-banner "Post Title" --preview-only`
**Behavior**: Show composed prompt without generating image
**Use Case**: Reviewing prompt quality, debugging, learning

### `--slug [slug]`
**Usage**: `/generate-post-banner --slug context-window-bleeding`
**Behavior**: Use slug to find and load post metadata automatically
**Requires**: Metadata file exists at `blog/posts/[slug]/metadata.json`

### `--metadata [path]`
**Usage**: `/generate-post-banner --metadata /path/to/metadata.json`
**Behavior**: Load metadata from specified file path
**Use Case**: Non-standard post locations

---

## Error Handling

### Missing Metadata
**Scenario**: No metadata file, only title provided
**Handling**:
1. Extract what information possible from title
2. Prompt user for additional context: "Is this a technical deep-dive, tutorial, opinion piece, or architecture post?"
3. Use Enhanced Glitch as safe fallback if still unclear
4. Proceed with limited placeholder filling

### Invalid Style Name
**Scenario**: `--style invalid_name` provided
**Handling**:
```
❌ ERROR: Invalid style name "invalid_name"

Valid styles:
- glass_object (Glass Object Technical)
- isometric (Isometric Technical Diagram)
- blueprint (Technical Blueprint)
- newspaper (Newspaper Front Page)
- glitch (Enhanced Glitch Corruption)

Please specify a valid style name or omit --style flag for recommendations.
```

### MCP Server Unavailable
**Scenario**: Nano Banana MCP not running or not configured
**Handling**:
```
❌ ERROR: Nano Banana MCP server not available

Banner generation requires the nano-banana MCP server.

Setup instructions:
1. Install nano-banana MCP server
2. Configure in Claude Code MCP settings
3. Verify with: claude mcp list

Cannot proceed without MCP access. Please install and configure nano-banana MCP server.
```

### File Permission Issues
**Scenario**: Cannot write to output directory
**Handling**:
```
❌ ERROR: Permission denied writing to output path

Path: /Users/ameno/dev/acidbath2/public/assets/posts/[slug]-banner.png

Possible solutions:
1. Check directory exists: mkdir -p /Users/ameno/dev/acidbath2/public/assets/posts/
2. Check write permissions: ls -ld /Users/ameno/dev/acidbath2/public/assets/posts/
3. Try alternative output path with --output flag

Please resolve permission issues and retry.
```

---

## Integration with Existing Command

This skill replaces the old `.claude/commands/generate_post_banner.md` command with enhanced capabilities. For backward compatibility, the old command file will be updated to invoke this skill.

**Migration Path**:
- Old command: Simple glitch generation
- New skill: Content-aware, multi-style, interactive workflow
- Transition: Old command points to skill with default behavior

---

## Usage Examples

### Example 1: Basic Usage with Metadata
```
/generate-post-banner --slug prompts-are-the-new-code
```
**Flow**:
1. Loads metadata from `blog/posts/01-prompts-are-the-new-code/metadata.json`
2. Analyzes content → Identifies provocative opinion piece
3. Recommends: Newspaper Front Page (primary), Glitch (alt 1), Glass Object (alt 2)
4. User confirms or selects alternative
5. Generates banner with newspaper style
6. Saves to `/public/assets/posts/prompts-are-the-new-code-banner.png`

### Example 2: Manual Input with Style Override
```
/generate-post-banner "API Gateway Architecture" --style glass_object
```
**Flow**:
1. No metadata, uses title only
2. Skips recommendation (style specified)
3. Loads glass_object template
4. Prompts for technical object description (or uses default "API gateway server")
5. Generates glass object banner
6. Prompts for slug to determine output filename

### Example 3: Preview Mode for Learning
```
/generate-post-banner "Context Engineering Deep-Dive" --preview-only
```
**Flow**:
1. Analyzes title → Technical deep-dive, performance-focused
2. Recommends: Technical Blueprint
3. Shows fully composed Nano Banana prompt
4. User can review, edit, or proceed to generation
5. If user proceeds, generates banner

### Example 4: Automated Batch Processing
```
/generate-post-banner --slug 55k-files-5-minutes --auto
```
**Flow**:
1. Loads metadata
2. Analyzes → Technical benchmark post
3. Auto-selects primary recommendation (Technical Blueprint)
4. Skips interactive confirmation
5. Generates banner automatically
6. Saves and reports success

---

## References

- **Style Templates**: See `STYLE_LIBRARY.md` for complete prompt templates
- **Mapping Rules**: See `CONTENT_STYLE_MAP.md` for decision tree logic
- **Examples**: See `EXAMPLES.md` for concrete filled prompts and visual descriptions

---

## Troubleshooting

### Issue: Style recommendation doesn't match content
**Solution**: Override with `--style [name]` flag or provide more detailed metadata/tags

### Issue: Generated image doesn't match expectations
**Solution**:
1. Use `--preview-only` to review composed prompt
2. Manually edit prompt to adjust details
3. Refer to `STYLE_LIBRARY.md` troubleshooting section
4. Try different style that may better suit content

### Issue: Prompt too generic
**Solution**:
1. Provide richer metadata with more tags
2. Add content description when invoking skill
3. Manually fill placeholders during interactive prompt

### Issue: Generation takes too long
**Solution**:
1. Complex photorealistic styles (glass, newspaper) take 45-60 seconds
2. Use simpler styles (isometric, glitch) for faster generation
3. Increase timeout if needed

---

## Version History

- **v1.0** (2025-12-23): Initial skill with 7-section workflow, content analysis, style recommendation, and Nano Banana integration
