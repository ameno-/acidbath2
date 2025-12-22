# Feature: YouTube Analyzer Migration - Port to Jerry as Specialized Workflow

## Metadata
adw_id: `b636eeb6`
prompt: `{"number": "youtube-migration", "title": "YouTube Analyzer Migration - Port to Jerry as Specialized Workflow", "body": "## Summary\n\nMigrate the existing YouTube analysis workflow from user-level Claude Code agents to Jerry's project structure. Update agents to use the bundled pattern executor instead of Fabric CLI.\n\n## Parent Issue\n\nThis is Phase 5 of `issue-jerry-patterns-content-analysis.md`\n\n## Dependencies\n\n- Requires: `issue-generic-analysis-adw.md` (Phase 4) completed\n\n## Source Files (User-Level)\n\nCurrent location: `~/.claude/agents/youtube/`\n\n| Agent | Purpose | Model |\n|-------|---------|-------|\n| metadata-extractor.md | Extract video metadata + transcript | haiku |\n| core-analyzer-haiku.md | Run 8 core patterns (fast) | haiku |\n| core-analyzer-sonnet.md | Run 8 core patterns (deep) | sonnet |\n| conditional-analyzer.md | Run content-type patterns | sonnet |\n| report-aggregator.md | Generate reports | haiku |\n| audio-summarizer.md | Generate TTS summary | haiku |\n| html-generator.md | Generate HTML dashboard | - |\n\nOrchestrators: `~/.claude/agents/youtube-orchestrator.md`, `youtube-analyzer-haiku.md`, `youtube-analyzer-sonnet.md`\n\nCommands: `~/.claude/commands/yt_*.md` (6 commands)\n\n## Deliverables\n\n### 1. Migrate Agents to Jerry\n\nMove and update agents to `.claude/agents/youtube/`:\n\n```\n.claude/agents/youtube/\n├── metadata-extractor.md      # Updated: paths to Jerry structure\n├── core-analyzer.md           # MERGED: haiku + sonnet into single with mode\n├── conditional-analyzer.md    # Updated: use pattern_executor\n├── report-aggregator.md       # Updated: paths\n├── audio-summarizer.md        # Updated: optional TTS dependency\n├── html-generator.md          # Moved from parent dir\n└── orchestrator.md            # MERGED: single orchestrator with mode\n```\n\n### 2. Key Updates to Agents\n\n**All Agents:**\n- Update hardcoded paths to use `$JERRY_ROOT` or relative paths\n- Update Fabric CLI calls to use `pattern_executor.execute_pattern()`\n- Update output paths to `agents/{adw_id}/youtube/{video_id}/`\n\n**core-analyzer.md (merged):**\n```markdown\n# Input includes mode: quick|full\n# quick → haiku model, core patterns only\n# full → sonnet model, all patterns\n```\n\n**conditional-analyzer.md:**\n```python\n# Before (Fabric CLI)\ncat transcript.txt | fabric --pattern extract_technical_content > patterns/extract_technical_content.md\n\n# After (pattern_executor)\nfrom adw_modules.pattern_executor import execute_pattern\nresult = execute_pattern(\"extract_technical_content\", transcript_text)\nPath(\"patterns/extract_technical_content.md\").write_text(result.output)\n```\n\n### 3. Create YouTube ADW (`adw_youtube_iso.py`)\n\nSpecialized wrapper around `adw_analyze_iso.py`:\n\n```python\n#!/usr/bin/env -S uv run\n\"\"\"\nADW YouTube Iso - YouTube-specific analysis workflow\n\nUsage:\n  uv run adw_youtube_iso.py <youtube-url> [options]\n\nOptions:\n  --mode       quick|full (default: full)\n  --output-dir Output directory\n  --no-audio   Skip audio summary generation\n  --no-html    Skip HTML dashboard generation\n\"\"\"\n```\n\nFeatures:\n- YouTube-specific pattern selection\n- Content type classification (technical/educational/general)\n- Conditional pattern execution based on content type\n- HTML dashboard generation\n- Audio summary generation (optional)\n\n### 4. Migrate Commands\n\nMove and update commands to `.claude/commands/`:\n\n| Command | File | Description |\n|---------|------|-------------|\n| /yt_analyze | yt_analyze.md | Main YouTube analysis |\n| /yt_quick | yt_quick.md | Quick analysis (haiku) |\n| /yt_full | yt_full.md | Full analysis (sonnet) |\n| /yt_metadata | yt_metadata.md | Metadata extraction only |\n\nRemove (consolidate):\n- `/yt_core` → merged into `/yt_analyze --quick`\n- `/yt_status` → use standard ADW state\n- `/yt_help` → use `/help youtube`\n\n### 5. Update Output Structure\n\n```\nagents/{adw_id}/youtube/{video_id}/\n├── metadata.json              # Video metadata\n├── transcript.txt             # Full transcript\n├── content-type.txt           # Classification\n├── patterns/                  # Pattern outputs\n│   ├── extract_wisdom.md\n│   ├── youtube_summary.md\n│   └── ...\n├── ANALYSIS_SUMMARY.md        # Executive summary\n├── aggregated-report.md       # Full report\n├── README.md                  # Navigation\n├── index.html                 # Interactive dashboard\n├── audio-summary.txt          # Summary text\n└── audio-summary.mp3          # TTS audio (optional)\n```\n\n### 6. TTS Integration (Optional)\n\nAudio summary depends on TTS utilities. Make it gracefully optional:\n\n```python\ndef generate_audio_summary(summary_text: str, output_path: str) -> bool:\n    \"\"\"Generate audio summary if TTS is available.\"\"\"\n    tts_utils = [\n        (\"elevenlabs\", os.getenv(\"ELEVENLABS_API_KEY\")),\n        (\"openai\", os.getenv(\"OPENAI_API_KEY\")),\n        (\"say\", shutil.which(\"say\")),  # macOS built-in\n    ]\n\n    for name, available in tts_utils:\n        if available:\n            return run_tts(name, summary_text, output_path)\n\n    logger.warning(\"No TTS available, skipping audio summary\")\n    return False\n```\n\n## Acceptance Criteria\n\n- [ ] All YouTube agents migrated to `.claude/agents/youtube/`\n- [ ] Agents updated to use `pattern_executor` instead of Fabric CLI\n- [ ] `adw_youtube_iso.py` created and functional\n- [ ] Commands migrated to `.claude/commands/`\n- [ ] Output structure matches specification\n- [ ] Quick mode completes in <90 seconds\n- [ ] Full mode completes in <180 seconds\n- [ ] Audio summary is optional (no failure if TTS unavailable)\n- [ ] HTML dashboard generated correctly\n- [ ] No hardcoded user paths remain\n\n## Migration Testing\n\nTest with known video:\n```bash\n# Quick analysis\n./adws/adw_youtube_iso.py \"https://youtube.com/watch?v=OIKTsVjTVJE\" --mode quick\n\n# Full analysis\n./adws/adw_youtube_iso.py \"https://youtube.com/watch?v=OIKTsVjTVJE\" --mode full\n```\n\nCompare outputs with original implementation.\n\n## Files to Create/Modify\n\n**Create:**\n- `.claude/agents/youtube/` (directory)\n- `.claude/agents/youtube/metadata-extractor.md`\n- `.claude/agents/youtube/core-analyzer.md`\n- `.claude/agents/youtube/conditional-analyzer.md`\n- `.claude/agents/youtube/report-aggregator.md`\n- `.claude/agents/youtube/audio-summarizer.md`\n- `.claude/agents/youtube/html-generator.md`\n- `.claude/agents/youtube/orchestrator.md`\n- `adws/adw_youtube_iso.py`\n- `.claude/commands/yt_analyze.md`\n- `.claude/commands/yt_quick.md`\n- `.claude/commands/yt_full.md`\n- `.claude/commands/yt_metadata.md`\n\n**Modify:**\n- None (all new files, old ones stay at user level)"}`

## Feature Description

This feature migrates the existing YouTube video analysis workflow from the user-level Claude Code configuration (`~/.claude/agents/youtube/`) to Jerry's project structure. The migration transforms a user-specific tool into a reusable, project-integrated workflow that:

1. **Eliminates hardcoded paths** - Replaces user-specific paths with project-relative paths and environment variables
2. **Adopts Jerry patterns** - Uses Jerry's agent orchestration, state management, and output structure
3. **Modernizes pattern execution** - Replaces direct Fabric CLI calls with a programmatic pattern executor module
4. **Provides isolated workflows** - Creates dedicated ADW script (`adw_youtube_iso.py`) following Jerry's isolation principles
5. **Maintains backward compatibility** - Preserves user-level agents while building project-integrated versions

The YouTube analyzer is a comprehensive multi-agent system that downloads video metadata, extracts transcripts, classifies content type, runs multiple Fabric patterns for analysis, aggregates results, generates interactive HTML dashboards, and produces optional audio summaries.

## User Story

As a developer using Jerry for content analysis
I want to analyze YouTube videos using Jerry's integrated workflow system
So that I can leverage reusable patterns, worktree isolation, and structured outputs without maintaining user-level agent configurations

## Problem Statement

The current YouTube analysis workflow exists exclusively in the user-level Claude Code configuration (`~/.claude/agents/youtube/`), creating several limitations:

1. **Not portable** - Other projects/users cannot leverage the workflow without manual file copying
2. **Hardcoded paths** - All agents use absolute paths like `/Users/ameno/dev/umbra-dev/technical-research/output/`
3. **Fabric CLI dependency** - Agents shell out to `fabric --pattern` commands instead of using programmatic execution
4. **No worktree isolation** - Operates on main working directory, not Jerry's isolated worktrees
5. **Manual orchestration** - Requires manual command invocation instead of integrated ADW workflows
6. **No state tracking** - Doesn't integrate with Jerry's state management and observability

The workflow is valuable (7 specialized agents, content classification, multi-pattern analysis, HTML output, TTS integration) but needs to be Jerry-native to realize its full potential as a reusable, composable component.

## Solution Statement

Port the YouTube analysis workflow to Jerry's project structure using these strategies:

1. **Agent migration** - Move agents from `~/.claude/agents/youtube/` to project `.claude/agents/youtube/` with path updates
2. **Pattern executor module** - Create `adw_modules/pattern_executor.py` to replace Fabric CLI with programmatic pattern execution
3. **Dedicated ADW script** - Implement `adws/adw_youtube_iso.py` following Jerry's isolation and state management patterns
4. **Slash command integration** - Migrate YouTube commands to project `.claude/commands/` with updated paths
5. **Consolidation** - Merge redundant agents (separate haiku/sonnet versions) into mode-aware single agents
6. **Output standardization** - Align output structure with Jerry's `agents/{adw_id}/` convention
7. **Graceful degradation** - Make optional features (TTS, HTML) fail gracefully if dependencies unavailable

The result is a fully-integrated, project-portable YouTube analysis workflow that maintains all existing capabilities while adopting Jerry's architectural benefits.

## Relevant Files

### Existing Jerry Infrastructure

**ADW Scripts (reference patterns):**
- `adws/adw_plan_iso.py` - Example of isolated workflow with state management (lines 50-150 show worktree creation, state tracking)
- `adws/adw_build_iso.py` - Example of agent orchestration in isolation (lines 200-250 show agent execution)
- `adws/adw_review_iso.py` - Example of specialized analysis workflow (similar pattern for YouTube)

**Modules to reference:**
- `adws/adw_modules/agent.py` - Core agent execution functions (`prompt_claude_code_with_retry`)
- `adws/adw_modules/workflow_ops.py` - Workflow utilities (state management, path handling)
- `adws/adw_modules/worktree_ops.py` - Worktree isolation operations
- `adws/adw_modules/state.py` - ADW state tracking (`ADWState` class)
- `adws/adw_modules/utils.py` - Utility functions for paths, IDs, etc.

**Commands to reference:**
- `.claude/commands/plan.md` - Shows slash command structure with frontmatter
- `.claude/commands/implement.md` - Shows agent instruction pattern
- `.claude/commands/feature.md` - Shows step-by-step task format (reference for new format)

### User-Level YouTube Agents (Source)

**Location:** `~/.claude/agents/youtube/`

**Agents to migrate:**
- `metadata-extractor.md` - Downloads video metadata and transcript using yt-dlp, classifies content type (78 lines)
- `core-analyzer-haiku.md` - Runs 8 core Fabric patterns in fast mode (65 lines)
- `core-analyzer-sonnet.md` - Runs 8 core Fabric patterns with deep analysis (89 lines)
- `conditional-analyzer.md` - Runs specialized patterns based on content type classification (72 lines)
- `report-aggregator.md` - Combines all pattern outputs into unified report (110 lines)
- `audio-summarizer.md` - Generates ultra-concise TTS audio summary (68 lines)

**Orchestrator agents:**
- `~/.claude/agents/youtube-orchestrator.md` - Coordinates agent execution flow
- `~/.claude/agents/youtube-analyzer-haiku.md` - Fast mode orchestration
- `~/.claude/agents/youtube-analyzer-sonnet.md` - Deep analysis orchestration

**Slash commands:**
- `~/.claude/commands/yt_quick.md` - Quick analysis command
- `~/.claude/commands/yt_full.md` - Full analysis command
- `~/.claude/commands/yt_metadata.md` - Metadata-only extraction
- `~/.claude/commands/yt_core.md` - Core patterns only
- `~/.claude/commands/yt_status.md` - Status checking
- `~/.claude/commands/yt_help.md` - Help documentation

### New Files

**Pattern Executor Module:**
- `adws/adw_modules/pattern_executor.py` - Programmatic Fabric pattern execution (replaces CLI calls)

**YouTube ADW Script:**
- `adws/adw_youtube_iso.py` - Main workflow script for isolated YouTube analysis

**Migrated Agents (Project-level):**
- `.claude/agents/youtube/metadata-extractor.md`
- `.claude/agents/youtube/core-analyzer.md` (merged haiku + sonnet)
- `.claude/agents/youtube/conditional-analyzer.md`
- `.claude/agents/youtube/report-aggregator.md`
- `.claude/agents/youtube/audio-summarizer.md`
- `.claude/agents/youtube/html-generator.md`
- `.claude/agents/youtube/orchestrator.md` (merged all orchestrators)

**Migrated Commands:**
- `.claude/commands/yt_analyze.md` (consolidated entry point)
- `.claude/commands/yt_quick.md`
- `.claude/commands/yt_full.md`
- `.claude/commands/yt_metadata.md`

## Implementation Plan

### Phase 1: Foundation - Pattern Executor and Infrastructure

Create the foundational module that replaces Fabric CLI calls with programmatic pattern execution. This must be completed before migrating agents since they all depend on it.

### Phase 2: Agent Migration

Migrate specialized agents from user-level to project-level, updating paths and pattern execution. Consolidate redundant agents (separate haiku/sonnet versions) into mode-aware single agents.

### Phase 3: ADW and Command Integration

Create the main YouTube analysis ADW script and migrate slash commands, ensuring full integration with Jerry's workflow orchestration and state management.

## Step by Step Tasks

IMPORTANT: Execute every step in order, respecting group dependencies.

### Group A: Foundation [parallel: false, model: sonnet]

Sequential foundation work that all other groups depend on.

#### Step A.1: Create Pattern Executor Module

- Create `adws/adw_modules/pattern_executor.py` with the following structure:
  - `PatternExecutionResult` dataclass (pattern_name, success, output, error)
  - `execute_pattern(pattern_name: str, input_text: str, working_dir: Optional[str] = None) -> PatternExecutionResult` function
  - Use `subprocess.run()` to call `fabric --pattern {pattern_name}` with stdin pipe
  - Handle errors gracefully (missing fabric, invalid pattern, execution failures)
  - Add retry logic (3 attempts with exponential backoff)
  - Add logging using Python logging module
- Validate: `uv run python -m py_compile adws/adw_modules/pattern_executor.py`
- Validate: `uv run python -c "from adws.adw_modules.pattern_executor import execute_pattern; print('OK')"`

#### Step A.2: Create Output Directory Structure Helper

- Add `create_youtube_output_dir(adw_id: str, video_id: str) -> str` function to `adws/adw_modules/utils.py`
- Function creates: `agents/{adw_id}/youtube/{video_id}/` and subdirectories: `patterns/`, `audio/`
- Returns absolute path to created directory
- Validate: `uv run python -c "from adws.adw_modules.utils import create_youtube_output_dir; print('OK')"`

#### Step A.3: Create YouTube ADW Script Skeleton

- Create `adws/adw_youtube_iso.py` with CLI argument parsing (click library):
  - Required: `youtube_url` (positional)
  - Optional: `--mode` (quick|full, default: full)
  - Optional: `--output-dir` (override default output location)
  - Optional: `--no-audio` (skip audio summary)
  - Optional: `--no-html` (skip HTML dashboard)
  - Optional: `--adw-id` (custom ADW ID, default: auto-generated)
- Add docstring with usage examples
- Implement help text
- Add script header: `#!/usr/bin/env -S uv run`
- Add PEP 723 inline metadata for dependencies: `click`, `rich`
- Validate: `uv run adws/adw_youtube_iso.py --help`

### Group B: Agent Migration [parallel: true, depends: A, model: sonnet]

Independent agents that can be migrated in parallel after foundation is complete.

#### Step B.1: Migrate Metadata Extractor Agent

- Create directory: `.claude/agents/youtube/`
- Copy `~/.claude/agents/youtube/metadata-extractor.md` to `.claude/agents/youtube/metadata-extractor.md`
- Update hardcoded paths:
  - Replace `/Users/ameno/dev/umbra-dev/technical-research/output/youtube-analysis/` with `agents/{adw_id}/youtube/`
  - Use `$WORKING_DIR` variable for all paths
- Update frontmatter: ensure `tools: Bash, Read, Write` and `model: haiku`
- Update workflow steps to accept `adw_id` and `video_id` as inputs
- Test with dry-run validation (no actual execution)

#### Step B.2: Migrate and Merge Core Analyzer Agents

- Copy `~/.claude/agents/youtube/core-analyzer-sonnet.md` to `.claude/agents/youtube/core-analyzer.md`
- Add mode support in frontmatter and instructions:
  - Accept `mode` parameter: `quick` (haiku, 8 core patterns) or `full` (sonnet, 8 core patterns with deeper analysis)
  - Update model directive based on mode
- Update pattern execution:
  - Replace `cat transcript.txt | fabric --pattern X > patterns/X.md`
  - With: `execute_pattern("X", transcript_text)` and save to file
- Update all 8 core patterns:
  - `extract_wisdom`
  - `create_summary`
  - `extract_insights`
  - `extract_recommendations`
  - `rate_content`
  - `extract_article_wisdom`
  - `analyze_answers`
  - `create_micro_summary`
- Update paths to use `$WORKING_DIR`
- Validate pattern names match Fabric's available patterns

#### Step B.3: Migrate Conditional Analyzer Agent

- Copy `~/.claude/agents/youtube/conditional-analyzer.md` to `.claude/agents/youtube/conditional-analyzer.md`
- Update pattern execution from Fabric CLI to `pattern_executor`:
  - Technical content: `extract_technical_content`, `extract_poc`, `extract_sponsors`, `summarize_rpg`
  - Educational content: `extract_questions`, `create_quiz`, `create_reading_plan`, `explain_code`
  - General content: `extract_sponsors`, `create_keynote`, `create_markmap_visualization`
- Read `content-type.txt` to determine which patterns to run
- Update paths to use `$WORKING_DIR`
- Add error handling for missing content-type file (default to "general")

#### Step B.4: Migrate Report Aggregator Agent

- Copy `~/.claude/agents/youtube/report-aggregator.md` to `.claude/agents/youtube/report-aggregator.md`
- Update file reading paths to use `$WORKING_DIR/patterns/*.md`
- Update aggregation logic:
  - Read all pattern outputs from `patterns/` directory
  - Combine into structured markdown report
  - Generate ANALYSIS_SUMMARY.md (executive summary)
  - Generate aggregated-report.md (full detailed report)
  - Generate README.md (navigation/table of contents)
- Update paths for output files
- Validate markdown generation

#### Step B.5: Migrate Audio Summarizer Agent

- Copy `~/.claude/agents/youtube/audio-summarizer.md` to `.claude/agents/youtube/audio-summarizer.md`
- Update TTS integration to be gracefully optional:
  - Check for ElevenLabs API key: `os.getenv("ELEVENLABS_API_KEY")`
  - Fallback to OpenAI TTS: `os.getenv("OPENAI_API_KEY")`
  - Fallback to macOS `say` command if available
  - Log warning and skip if no TTS available (don't fail)
- Update paths to use `$WORKING_DIR/audio/`
- Generate ultra-concise summary (2-3 sentences max)
- Save summary text to `audio-summary.txt`
- Generate audio to `audio-summary.mp3` if TTS available
- Validate graceful degradation when TTS unavailable

#### Step B.6: Migrate HTML Generator Agent

- Find HTML generator agent (check `~/.claude/agents/` parent directory)
- Copy to `.claude/agents/youtube/html-generator.md`
- Update to generate single-page interactive HTML dashboard:
  - Table of contents with anchor links
  - Searchable content (JavaScript filter)
  - Collapsible sections per pattern
  - Download button for full report
  - Responsive design (mobile-friendly)
- Update paths to read from `$WORKING_DIR/patterns/` and output to `$WORKING_DIR/index.html`
- Validate HTML generation (syntax check)

### Group C: Orchestrator and ADW Implementation [parallel: false, depends: B, model: sonnet]

Sequential integration work that ties all agents together.

#### Step C.1: Create Orchestrator Agent

- Create `.claude/agents/youtube/orchestrator.md`
- Merge logic from user-level orchestrators:
  - `~/.claude/agents/youtube-orchestrator.md`
  - `~/.claude/agents/youtube-analyzer-haiku.md`
  - `~/.claude/agents/youtube-analyzer-sonnet.md`
- Add mode support (quick|full) that determines:
  - Model selection (haiku for quick, sonnet for full)
  - Pattern depth (basic vs comprehensive analysis)
- Implement execution flow:
  1. Run metadata-extractor
  2. Run core-analyzer with mode
  3. Run conditional-analyzer based on content type
  4. Run report-aggregator
  5. Run audio-summarizer (optional)
  6. Run html-generator (optional)
- Add error handling and retry logic for each phase
- Track state using Jerry's state management
- Validate orchestration logic (no actual execution)

#### Step C.2: Implement YouTube ADW Main Logic

- Complete `adws/adw_youtube_iso.py` implementation:
  - Generate ADW ID if not provided: `utils.generate_adw_id()`
  - Parse and validate YouTube URL, extract video ID
  - Create output directory structure using helper from A.2
  - Initialize ADW state: `ADWState(adw_id)`
  - Execute orchestrator agent with Task tool, passing:
    - `adw_id`
    - `video_id`
    - `mode` (quick|full)
    - `working_dir` path
    - `skip_audio` flag
    - `skip_html` flag
  - Wait for orchestrator completion
  - Load final state and display summary
  - Return exit code based on success/failure
- Add comprehensive logging using Jerry's logger pattern
- Validate: `uv run python -m py_compile adws/adw_youtube_iso.py`

#### Step C.3: Add State Management Integration

- Update orchestrator agent to track state:
  - Update state after each agent execution
  - Record: phase name, agent name, success status, output paths
  - Use `ADWState.update()` method
  - Save state to `agents/{adw_id}/adw_state.json`
- Add resume capability (detect partial completion, skip completed phases)
- Validate state tracking (inspect generated state file structure)

### Group D: Command Migration and Testing [parallel: false, depends: C, model: sonnet]

Final integration of slash commands and comprehensive testing.

#### Step D.1: Migrate Primary Slash Commands

- Create `.claude/commands/yt_analyze.md`:
  - Consolidated entry point for YouTube analysis
  - Accept YouTube URL as `$ARGUMENTS`
  - Support mode flags: `--quick` or `--full`
  - Invoke `adws/adw_youtube_iso.py` with appropriate arguments
  - Follow Jerry slash command format with frontmatter
- Create `.claude/commands/yt_quick.md`:
  - Wrapper for quick mode: invokes `yt_analyze` with `--quick`
  - Optimized for speed (haiku model, core patterns only)
  - Target: <90 seconds execution time
- Create `.claude/commands/yt_full.md`:
  - Wrapper for full mode: invokes `yt_analyze` with `--full`
  - Comprehensive analysis (sonnet model, all patterns)
  - Target: <180 seconds execution time
- Create `.claude/commands/yt_metadata.md`:
  - Metadata extraction only (no pattern analysis)
  - Invokes metadata-extractor agent directly
  - Useful for previewing content before full analysis
- Validate: Check markdown syntax, frontmatter format

#### Step D.2: Document YouTube Workflow in README

- Add YouTube analysis section to project README.md:
  - Overview of workflow capabilities
  - Usage examples for `adw_youtube_iso.py`
  - Slash command reference (`/yt_quick`, `/yt_full`, `/yt_metadata`)
  - Output structure documentation
  - Configuration options (TTS, HTML generation)
- Add to Jerry's workflow table in README
- Validate: Ensure documentation is clear and comprehensive

#### Step D.3: Validation Testing with Test Video

- Test quick mode:
  - Run: `uv run adws/adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode quick`
  - Verify output structure matches spec
  - Verify all core patterns executed
  - Verify execution time <90 seconds
  - Inspect `agents/{adw_id}/adw_state.json` for state tracking
- Test full mode:
  - Run: `uv run adws/adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode full`
  - Verify all patterns executed (core + conditional)
  - Verify HTML dashboard generated
  - Verify execution time <180 seconds
  - Inspect all output files
- Test metadata-only mode:
  - Run with: `--no-audio --no-html` and verify graceful handling
- Test error handling:
  - Invalid YouTube URL (verify error message)
  - Missing video (verify graceful failure)
  - Network failure (verify retry logic)
- Document test results in validation log

## Testing Strategy

### Unit Tests

**Pattern Executor:**
- Test `execute_pattern()` with valid pattern name
- Test with invalid pattern name (should return error in result, not raise exception)
- Test with network failure (should retry 3 times)
- Test with empty input (should handle gracefully)

**Output Directory Helper:**
- Test `create_youtube_output_dir()` creates all subdirectories
- Test with existing directory (should not fail)
- Test with invalid adw_id (should sanitize)

**YouTube ADW Script:**
- Test CLI argument parsing (all valid combinations)
- Test YouTube URL parsing (full URL, short URL, video ID only)
- Test video ID extraction (various URL formats)

### Integration Tests

**Agent Execution Flow:**
1. Metadata extractor → verify metadata.json, transcript.txt, content-type.txt created
2. Core analyzer → verify 8 pattern outputs in patterns/ directory
3. Conditional analyzer → verify content-type-specific patterns run
4. Report aggregator → verify ANALYSIS_SUMMARY.md, aggregated-report.md, README.md
5. Audio summarizer → verify audio-summary.txt, optional audio-summary.mp3
6. HTML generator → verify index.html with correct structure

**State Management:**
- State file created at workflow start
- State updated after each agent phase
- State persisted correctly for resume capability
- State final summary accurate

**Performance:**
- Quick mode completes in <90 seconds
- Full mode completes in <180 seconds
- Parallel pattern execution (if applicable)

### Edge Cases

**URL Variations:**
- Full YouTube URL: `https://youtube.com/watch?v=VIDEO_ID`
- Short URL: `https://youtu.be/VIDEO_ID`
- Video ID only: `VIDEO_ID`
- URL with timestamp: `https://youtube.com/watch?v=VIDEO_ID&t=123s`
- URL with playlist: `https://youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID`

**Missing Dependencies:**
- No TTS API keys → should skip audio, log warning, continue
- No `yt-dlp` installed → should fail with clear error message
- No `fabric` installed → should fail with clear error message
- No internet connection → should retry, then fail gracefully

**Invalid Input:**
- Invalid YouTube URL → clear error message
- Private/deleted video → graceful failure with explanation
- Video without transcript → attempt manual subs, document if unavailable
- Empty video (no content) → handle gracefully

**Partial Failures:**
- Metadata succeeds, pattern execution fails → state reflects partial success
- Core patterns succeed, conditional patterns fail → continue to aggregation
- HTML generation fails → workflow still succeeds, log warning

**Path Edge Cases:**
- Very long video IDs → sanitize for filesystem
- Special characters in video titles → sanitize for filenames
- Working directory with spaces → handle with proper quoting

## Acceptance Criteria

**Migration Completeness:**
- [ ] All 6 agents migrated to `.claude/agents/youtube/`
- [ ] All agents use `pattern_executor` instead of Fabric CLI
- [ ] All hardcoded user paths removed
- [ ] All agents updated to use `$WORKING_DIR` variable
- [ ] Orchestrator consolidates haiku/sonnet variants with mode support

**ADW Implementation:**
- [ ] `adw_youtube_iso.py` created with full CLI support
- [ ] State management integrated using `ADWState`
- [ ] Output structure matches specification
- [ ] Pattern executor module implemented and tested

**Command Migration:**
- [ ] 4 primary slash commands migrated to `.claude/commands/`
- [ ] Commands removed: `/yt_core`, `/yt_status`, `/yt_help` (consolidated)
- [ ] All commands follow Jerry's frontmatter format
- [ ] Commands properly invoke `adw_youtube_iso.py`

**Performance:**
- [ ] Quick mode completes in <90 seconds (target: 60-75s)
- [ ] Full mode completes in <180 seconds (target: 120-150s)
- [ ] Metadata extraction completes in <15 seconds

**Robustness:**
- [ ] Audio summary gracefully optional (no failure if TTS unavailable)
- [ ] HTML generation gracefully optional (no failure if disabled)
- [ ] All error cases handled with clear messages
- [ ] Retry logic works for transient failures

**Quality:**
- [ ] HTML dashboard generated correctly with navigation
- [ ] All pattern outputs formatted as markdown
- [ ] Aggregated report includes all executed patterns
- [ ] README navigation includes all sections

**Documentation:**
- [ ] README updated with YouTube workflow section
- [ ] Usage examples documented
- [ ] Slash commands documented
- [ ] Configuration options documented

## Validation Commands

Execute these commands to validate the feature is complete:

**1. Module Compilation:**
```bash
# Validate pattern executor
uv run python -m py_compile adws/adw_modules/pattern_executor.py

# Validate YouTube ADW
uv run python -m py_compile adws/adw_youtube_iso.py
```

**2. Import Tests:**
```bash
# Test pattern executor import
uv run python -c "from adws.adw_modules.pattern_executor import execute_pattern; print('Pattern executor: OK')"

# Test utils import
uv run python -c "from adws.adw_modules.utils import create_youtube_output_dir; print('Utils: OK')"
```

**3. CLI Validation:**
```bash
# Test help output
uv run adws/adw_youtube_iso.py --help

# Verify exit code for invalid input
uv run adws/adw_youtube_iso.py "invalid-url" || echo "Expected failure: OK"
```

**4. Quick Mode End-to-End Test:**
```bash
# Run quick analysis on test video
time uv run adws/adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode quick

# Verify output structure
ADW_DIR=$(ls -td agents/*/ | head -1)
test -f "${ADW_DIR}youtube/OIKTsVjTVJE/metadata.json" && echo "Metadata: OK"
test -f "${ADW_DIR}youtube/OIKTsVjTVJE/transcript.txt" && echo "Transcript: OK"
test -f "${ADW_DIR}youtube/OIKTsVjTVJE/content-type.txt" && echo "Content-type: OK"
test -d "${ADW_DIR}youtube/OIKTsVjTVJE/patterns" && echo "Patterns dir: OK"
test -f "${ADW_DIR}youtube/OIKTsVjTVJE/ANALYSIS_SUMMARY.md" && echo "Summary: OK"
test -f "${ADW_DIR}adw_state.json" && echo "State: OK"

# Verify execution time <90 seconds (check time output above)
```

**5. Full Mode End-to-End Test:**
```bash
# Run full analysis
time uv run adws/adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode full

# Verify additional outputs
ADW_DIR=$(ls -td agents/*/ | head -1)
test -f "${ADW_DIR}youtube/OIKTsVjTVJE/index.html" && echo "HTML dashboard: OK"
test -f "${ADW_DIR}youtube/OIKTsVjTVJE/aggregated-report.md" && echo "Full report: OK"
test -f "${ADW_DIR}youtube/OIKTsVjTVJE/README.md" && echo "README: OK"

# Verify execution time <180 seconds (check time output above)
```

**6. Pattern Count Validation:**
```bash
# Quick mode should have 8 core patterns
ADW_DIR=$(ls -td agents/*/ | head -1)
PATTERN_COUNT=$(ls -1 "${ADW_DIR}youtube/OIKTsVjTVJE/patterns/" | wc -l | tr -d ' ')
test "$PATTERN_COUNT" -ge 8 && echo "Core patterns: OK ($PATTERN_COUNT files)"

# Full mode should have 8+ patterns (core + conditional)
# Count will vary based on content type
```

**7. State Management Validation:**
```bash
# Verify state file structure
ADW_DIR=$(ls -td agents/*/ | head -1)
uv run python -c "
import json
with open('${ADW_DIR}adw_state.json') as f:
    state = json.load(f)
    assert 'adw_id' in state, 'Missing adw_id'
    assert 'phases' in state or 'agents' in state, 'Missing execution tracking'
    print('State structure: OK')
"
```

**8. Graceful Degradation Tests:**
```bash
# Test without TTS (should not fail)
unset ELEVENLABS_API_KEY
unset OPENAI_API_KEY
uv run adws/adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode quick --no-audio
echo "No-audio mode: OK"

# Test without HTML
uv run adws/adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode quick --no-html
echo "No-HTML mode: OK"
```

**9. Slash Command Validation:**
```bash
# Verify slash commands exist
test -f .claude/commands/yt_analyze.md && echo "yt_analyze command: OK"
test -f .claude/commands/yt_quick.md && echo "yt_quick command: OK"
test -f .claude/commands/yt_full.md && echo "yt_full command: OK"
test -f .claude/commands/yt_metadata.md && echo "yt_metadata command: OK"

# Verify old commands removed or deprecated
test ! -f .claude/commands/yt_core.md && echo "yt_core removed: OK"
test ! -f .claude/commands/yt_status.md && echo "yt_status removed: OK"
test ! -f .claude/commands/yt_help.md && echo "yt_help removed: OK"
```

**10. Agent File Validation:**
```bash
# Verify all agents migrated
test -f .claude/agents/youtube/metadata-extractor.md && echo "metadata-extractor: OK"
test -f .claude/agents/youtube/core-analyzer.md && echo "core-analyzer: OK"
test -f .claude/agents/youtube/conditional-analyzer.md && echo "conditional-analyzer: OK"
test -f .claude/agents/youtube/report-aggregator.md && echo "report-aggregator: OK"
test -f .claude/agents/youtube/audio-summarizer.md && echo "audio-summarizer: OK"
test -f .claude/agents/youtube/html-generator.md && echo "html-generator: OK"
test -f .claude/agents/youtube/orchestrator.md && echo "orchestrator: OK"

# Verify no hardcoded paths remain
! grep -r "/Users/ameno" .claude/agents/youtube/ && echo "No hardcoded paths: OK"
```

**11. Documentation Validation:**
```bash
# Verify README updated
grep -q "YouTube" README.md && echo "README updated: OK"
grep -q "adw_youtube_iso" README.md && echo "ADW documented: OK"
```

**12. Complete System Test:**
```bash
# Full integration test with all features
uv run adws/adw_youtube_iso.py \
  "https://youtube.com/watch?v=OIKTsVjTVJE" \
  --mode full \
  --adw-id test-youtube-migration

# Verify comprehensive output
ADW_DIR="agents/test-youtube-migration"
test -f "${ADW_DIR}/youtube/OIKTsVjTVJE/metadata.json" || exit 1
test -f "${ADW_DIR}/youtube/OIKTsVjTVJE/transcript.txt" || exit 1
test -f "${ADW_DIR}/youtube/OIKTsVjTVJE/content-type.txt" || exit 1
test -d "${ADW_DIR}/youtube/OIKTsVjTVJE/patterns" || exit 1
test -f "${ADW_DIR}/youtube/OIKTsVjTVJE/ANALYSIS_SUMMARY.md" || exit 1
test -f "${ADW_DIR}/youtube/OIKTsVjTVJE/aggregated-report.md" || exit 1
test -f "${ADW_DIR}/youtube/OIKTsVjTVJE/README.md" || exit 1
test -f "${ADW_DIR}/youtube/OIKTsVjTVJE/index.html" || exit 1
test -f "${ADW_DIR}/adw_state.json" || exit 1

echo "Complete system test: PASSED"
```

## Notes

### Dependencies

**Python packages needed (add via `uv add`):**
- `click` - CLI framework (already in Jerry)
- `rich` - Terminal formatting (already in Jerry)
- Standard library: `subprocess`, `json`, `pathlib`, `logging`, `os`, `re`

**External tools required:**
- `yt-dlp` - YouTube video/metadata downloader (user must install: `brew install yt-dlp` or `pip install yt-dlp`)
- `fabric` - Pattern execution framework (user must install: `go install github.com/danielmiessler/fabric@latest`)

**Optional dependencies:**
- ElevenLabs API key for TTS (environment variable: `ELEVENLABS_API_KEY`)
- OpenAI API key for TTS fallback (environment variable: `OPENAI_API_KEY`)
- macOS `say` command (built-in on macOS for local TTS)

### Migration Strategy

**Backward Compatibility:**
- User-level agents remain untouched at `~/.claude/agents/youtube/`
- Users can continue using original workflow if desired
- Project-level version is independent, not a replacement

**Future Enhancements (Out of Scope):**
- Playlist analysis (analyze all videos in a playlist)
- Comparative analysis (compare multiple videos)
- Trend analysis (analyze channel over time)
- Video recommendations (suggest related content)
- Pattern customization (user-defined analysis patterns)
- Export formats (PDF, Word, JSON API)

### Pattern Executor Design Notes

The `pattern_executor` module is intentionally thin - it's a wrapper around Fabric CLI, not a reimplementation. This maintains compatibility with Fabric's evolving patterns while providing:
- Programmatic invocation (no shell interpolation vulnerabilities)
- Consistent error handling
- Retry logic for transient failures
- Structured result objects
- Logging integration

If Fabric adds a Python API in the future, we can update the executor internally without changing agent code.

### Performance Considerations

**Quick Mode Target: <90 seconds**
- Metadata extraction: ~10-15s (yt-dlp download)
- Core patterns (8x, parallel): ~40-50s
- Report aggregation: ~5-10s
- State management overhead: ~2-5s
- Total: 60-80s (buffer for slower networks)

**Full Mode Target: <180 seconds**
- Metadata extraction: ~10-15s
- Core patterns (8x): ~40-50s
- Conditional patterns (3-6x): ~30-40s
- Report aggregation: ~10-15s
- HTML generation: ~5-10s
- Audio summary (optional): ~10-20s
- Total: 105-150s (buffer for slower networks)

**Optimization Opportunities:**
- Parallel pattern execution (multiple fabric processes)
- Pattern result caching (skip re-running on resume)
- Incremental transcript download (stream processing)
- Pre-compiled pattern templates

### Output Size Estimates

Typical output directory for a 20-minute technical video:
- `metadata.json`: ~5-10 KB
- `transcript.txt`: ~15-30 KB
- `patterns/*.md`: 8-15 files, ~50-150 KB total
- `ANALYSIS_SUMMARY.md`: ~5-10 KB
- `aggregated-report.md`: ~100-200 KB
- `index.html`: ~150-300 KB (includes embedded CSS/JS)
- `audio-summary.mp3`: ~50-100 KB (if generated)
- Total: ~400-800 KB per video

For 100 videos: ~40-80 MB (manageable for git with LFS)

### Error Recovery

**Transient Failures (Retry):**
- Network timeouts during yt-dlp download
- Fabric pattern execution failures (busy process)
- File I/O temporary locks

**Permanent Failures (Fail Fast):**
- Invalid YouTube URL format
- Private/deleted video
- Missing required dependencies (yt-dlp, fabric)
- Disk space exhausted

**Partial Success (Continue):**
- Some patterns fail, others succeed → continue to aggregation
- TTS unavailable → skip audio, continue to HTML
- HTML generation fails → workflow succeeds, log warning

### Security Considerations

**Input Validation:**
- Sanitize video IDs for filesystem (remove special chars)
- Validate URL format before passing to yt-dlp
- Limit transcript size (prevent DoS from extremely long videos)

**Shell Command Safety:**
- Use `subprocess.run()` with list arguments (not shell=True)
- No string interpolation in shell commands
- Validate all paths are within working directory

**API Key Protection:**
- Never log API keys
- Read from environment variables only
- No API keys in state files or outputs

### Future Compatibility

**Fabric Pattern Evolution:**
- Pattern names may change → maintain mapping table
- New patterns added → easy to extend conditional analyzer
- Pattern output format changes → update parser in aggregator

**YouTube API Changes:**
- yt-dlp handles API changes → minimal impact
- Transcript format changes → may need parser updates
- Metadata schema changes → validate JSON structure

**Jerry Framework Evolution:**
- State management schema → use optional fields for new features
- ADW interface changes → isolate in workflow_ops
- Agent execution changes → isolate in orchestrator
