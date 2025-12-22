---
allowed-tools: Bash, Task
argument-hint: [input-source] [--quick|--full|--patterns pattern1,pattern2]
description: Analyze any content using bundled fabric patterns
---

# Analyze Content

Run pattern-based analysis on any input type (YouTube videos, web URLs, GitHub content, PDFs, text files, or stdin).

## Input
**INPUT_SOURCE**: $ARGUMENTS

## Execution
Invoke `adw_analyze_iso.py` with the provided input source and any additional arguments.

The analysis workflow will:
1. Auto-detect content type from input (including GitHub notebooks/files)
2. Extract content using appropriate extractor
3. Execute selected fabric patterns (core, specialized, or custom)
4. Generate comprehensive reports and summaries
5. Create output directory with all results

## Examples

```bash
# Analyze YouTube video
/analyze "https://youtube.com/watch?v=abc123"

# Quick analysis (minimal patterns)
/analyze "https://blog.com/article" --quick

# Full analysis (all patterns)
/analyze "https://example.com/post" --full

# Specific patterns
/analyze ./document.pdf --patterns extract_wisdom,extract_insights

# Use different model
/analyze "https://youtube.com/watch?v=abc" --model sonnet

# Analyze from stdin
cat article.txt | /analyze - --patterns extract_wisdom

# Analyze GitHub notebook
/analyze "https://github.com/owner/repo/blob/main/notebook.ipynb"

# Brainstorm mode - persistent analysis with versioning
/analyze "https://youtube.com/watch?v=abc" --brainstorm

# Use ACIDBATH preset for blog post generation
/analyze "https://github.com/owner/repo/blob/main/code.py" --preset acidbath --brainstorm

# Custom slug for brainstorm analysis
/analyze "https://blog.com/article" --brainstorm --slug my-analysis-name
```

## Output

Analysis results are saved to `agents/{adw_id}/analyze/` (default) or brainstorm directory:

**Standard mode:**
- `content.txt` - Extracted content
- `patterns/` - Individual pattern outputs
- `ANALYSIS_SUMMARY.md` - Executive summary
- `report.md` - Full aggregated report
- `metadata.json` - Execution metadata
- `index.html` - Interactive dashboard

**Brainstorm mode** (`--brainstorm`):
- Saves to `$BRAINSTORM_DIR/{slug}/v{N}/` (default: `~/dev/brainstorm`)
- Creates `manifest.json` tracking all analyses
- Supports versioned re-analysis with diff generation
- Auto-detects re-analysis by URL

## Options

**Pattern Selection:**
- `--quick` - Use minimal core pattern set for speed
- `--full` - Use all applicable patterns (core + specialized + conditional)
- `--patterns` - Comma-separated list of specific patterns
- `--preset` - Use pattern preset (e.g., `acidbath` for blog generation)

**Execution:**
- `--model` - Model to use (haiku/sonnet, default: haiku)
- `--parallel` - Max concurrent pattern executions (default: 4)
- `--dry-run` - Show execution plan without running
- `--content-type` - Force content type (youtube/url/pdf/text/github)
- `--output-dir` - Custom output directory

**Brainstorm Mode:**
- `--brainstorm` - Save to persistent brainstorm directory with versioning
- `--slug` - Custom slug for analysis (auto-generated from title if not provided)

## Presets

**acidbath** - Optimized for technical blog post generation:
- Always runs: `extract_poc`, `extract_agent_opportunities`, `extract_technical_content`
- Custom: `extract_numbers_and_metrics`, `extract_failure_modes`, `generate_acidbath_outline`
- Supporting: `extract_wisdom`, `extract_insights`, `extract_recommendations`

## Brainstorm CLI

Manage brainstorm analyses with `adw_brainstorm.py`:

```bash
uv run adws/adw_brainstorm.py list              # List all analyses
uv run adws/adw_brainstorm.py status <slug>     # Show analysis details
uv run adws/adw_brainstorm.py versions <slug>   # Show version history
uv run adws/adw_brainstorm.py link <slug> <path> # Link to blog post
uv run adws/adw_brainstorm.py diff <slug> v1 v2 # Show diff between versions
```

Use the Bash tool to execute the adw_analyze_iso.py script with the provided arguments.
