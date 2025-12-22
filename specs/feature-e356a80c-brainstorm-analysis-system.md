# Feature: Brainstorm Analysis System with Manifest Tracking

## Metadata
adw_id: `e356a80c`
prompt: `{"number": "brainstorm-analysis-system", "title": "Local Issue brainstorm-analysis-system", "body": "# Issue: Brainstorm Analysis System with Manifest Tracking..."}`

## Feature Description
Create a persistent, manifest-driven content analysis system for the brainstorm directory that supports versioned re-analysis with per-pattern diffs, configurable output location, and ACIDBATH-aligned pattern presets. This system transforms the ephemeral `agents/{adw_id}/` analysis workflow into a permanent knowledge base with full version history, diff tracking, and blog post integration capabilities.

The system enables content creators to analyze content (YouTube videos, GitHub repos, PDFs, articles) with custom pattern presets, re-analyze when content updates, generate detailed diffs showing what changed, and link analyses to blog posts for content pipeline workflows.

## User Story
As a content creator and researcher
I want to analyze diverse content sources (YouTube, GitHub, articles) and store analyses persistently with version tracking
So that I can build a searchable knowledge base, re-analyze content when it changes, generate blog posts from analyses, and track the evolution of insights over time.

## Problem Statement
The current `adw_analyze_iso.py` workflow outputs to ephemeral `agents/{adw_id}/` directories which:
- Disappear when agents are cleaned up
- Cannot track analyses across multiple content sources
- Don't support re-analysis with diff generation
- Cannot link analyses to blog posts
- Lack a persistent manifest of all analyzed content
- Don't support custom pattern presets for specific use cases (blogging, POC extraction, technical content)

This makes it impossible to build a knowledge base from analyzed content or maintain a content-to-blog workflow.

## Solution Statement
Implement a brainstorm directory system (`~/dev/brainstorm` by default) with:

1. **Persistent Storage**: Each analysis stored in kebab-case slug subdirectories with all versions retained forever
2. **Manifest Tracking**: Root `manifest.json` tracking all analyses with metadata, source info, and version history
3. **Versioned Re-Analysis**: Auto-detect existing analyses by URL, create new version (v1→v2→v3), generate per-pattern diffs
4. **ACIDBATH Preset**: Custom pattern preset optimized for blog post generation (POCs, metrics, failure modes, agent opportunities)
5. **GitHub Content Support**: Extract and analyze GitHub files, notebooks (.ipynb), and directory trees
6. **Blog Integration**: Track blog post status and link analyses to published posts

The solution uses existing `pattern_executor.py` and `content_extractors.py` infrastructure, extending them with new content types (GitHub), custom patterns, and persistent storage.

## Relevant Files

### Core Analysis Infrastructure (Existing)
- **adws/adw_analyze_iso.py** - Main analysis workflow (will be extended with `--brainstorm` flag)
  - Currently outputs to `agents/{adw_id}/analyze`
  - Needs brainstorm mode to output to persistent directory
  - Needs re-analysis detection by URL matching

- **adws/adw_modules/pattern_executor.py** - Pattern execution engine
  - Already supports parallel pattern execution
  - Needs preset system for pattern bundling

- **adws/adw_modules/content_extractors.py** - Content extraction router
  - Currently supports YouTube, URL, PDF, text
  - Needs GitHub extractor integration

- **adws/adw_modules/data_types.py** - Type definitions
  - Needs ContentType.GITHUB enum value
  - Needs manifest data types (BrainstormManifest, AnalysisEntry, VersionInfo)

- **adws/adw_modules/report_generator.py** - Report generation
  - Already generates summaries and HTML dashboards
  - Will be used for per-version reports

### New Files

#### Core Brainstorm Modules
- **adws/adw_modules/brainstorm_ops.py** - Brainstorm operations module
  - Manifest CRUD operations (create, read, update manifest.json)
  - Slug generation from titles (kebab-case, collision handling)
  - Directory structure creation (slug dirs, version dirs, symlinks)
  - Analysis detection (find existing by URL)
  - Version management (get next version, update latest symlink)
  - Blog post linking (update manifest with blog status)

- **adws/adw_modules/github_ops.py** - GitHub content extraction
  - URL type detection (blob vs tree)
  - File extraction (raw content download)
  - Notebook parsing (.ipynb → readable markdown)
  - Directory aggregation (README + key files)
  - Content object generation (return ContentObject)

- **adws/adw_modules/diff_ops.py** - Diff generation module
  - Per-pattern diff generation (compare v1 vs v2 for each pattern)
  - Unified diff format with context
  - DIFF_FROM_vN.md summary generation
  - Change detection and categorization (major/minor/no change)

#### CLI Tools
- **adws/adw_brainstorm.py** - Brainstorm management CLI
  - `list` - List all analyses with metadata
  - `status <slug>` - Show status for specific analysis
  - `link <slug> <blog-path>` - Link analysis to blog post
  - `versions <slug>` - Show version history
  - `diff <slug> <v1> <v2>` - Show diff between versions

#### Patterns
- **.jerry/patterns/blogging/extract_numbers_and_metrics/system.md** - Extract numerical data
- **.jerry/patterns/blogging/extract_failure_modes/system.md** - Extract failure patterns
- **.jerry/patterns/blogging/generate_acidbath_outline/system.md** - Generate blog outline

#### Presets
- **.jerry/presets/acidbath.yaml** - ACIDBATH pattern preset configuration
  - Core: extract_poc, extract_agent_opportunities, extract_technical_content
  - Custom: extract_numbers_and_metrics, extract_failure_modes, generate_acidbath_outline
  - Supporting: extract_patterns, extract_ideas, extract_wisdom

#### Schema
- **~/.local/share/brainstorm/.schema/manifest.schema.json** - JSON schema for manifest validation

### Modified Files
- **.claude/commands/analyze.md** - Update documentation with `--brainstorm` flag examples

## Implementation Plan

### Phase 1: Foundation
Set up the brainstorm directory structure, manifest system, and core data types. This provides the foundation for all subsequent phases.

### Phase 2: Core Implementation
Implement GitHub content extraction, pattern creation, and brainstorm operations. This enables the core analysis workflow.

### Phase 3: Integration
Integrate brainstorm mode into the existing analysis workflow and create CLI tools. This makes the system fully functional and user-facing.

## Step by Step Tasks

### Group A: Data Types and Schema [parallel: false, model: sonnet]
Foundation work - define all data structures and schemas before implementation.

#### Step A.1: Define Brainstorm Data Types
- Add `ContentType.GITHUB = "github"` to data_types.py ContentType enum
- Create `BrainstormManifest` model with version, last_updated, total_analyses, analyses dict
- Create `AnalysisEntry` model with slug, title, source info, versions list, tags, blog_status
- Create `VersionInfo` model with version, date, preset, patterns_run, model, adw_id, diff_from, changes_summary
- Create `SourceInfo` model with type, url, original_title fields
- Add type hints for all models using Pydantic BaseModel

#### Step A.2: Create Manifest JSON Schema
- Create directory: `mkdir -p ~/.local/share/brainstorm/.schema`
- Write `manifest.schema.json` with JSON Schema Draft 7 format
- Define schema for manifest root (version, last_updated, total_analyses, analyses)
- Define schema for analysis entry (slug, title, source, versions, tags, blog_status)
- Define schema for version info (version, date, preset, patterns_run, model, adw_id)
- Add validation constraints (required fields, enum values, date formats)

### Group B: Pattern System [parallel: false, depends: A, model: sonnet]
Create custom blogging patterns and preset configuration. These patterns are specific to the ACIDBATH use case.

#### Step B.1: Create extract_numbers_and_metrics Pattern
- Create directory: `.jerry/patterns/blogging/extract_numbers_and_metrics/`
- Write `system.md` with pattern prompt
- Pattern extracts: numerical claims, metrics, percentages, statistics, benchmarks
- Output format: markdown list with context for each number
- Test pattern with sample technical content

#### Step B.2: Create extract_failure_modes Pattern
- Create directory: `.jerry/patterns/blogging/extract_failure_modes/`
- Write `system.md` with pattern prompt
- Pattern extracts: failure scenarios, edge cases, known issues, anti-patterns, gotchas
- Output format: markdown list with description and impact
- Test pattern with sample technical content

#### Step B.3: Create generate_acidbath_outline Pattern
- Create directory: `.jerry/patterns/blogging/generate_acidbath_outline/`
- Write `system.md` with pattern prompt
- Pattern generates: blog post outline optimized for ACIDBATH structure
- Includes sections: POCs, metrics, failure modes, agent opportunities, key insights
- Output format: hierarchical markdown outline with section descriptions
- Test pattern with sample analyzed content

#### Step B.4: Create ACIDBATH Preset Configuration
- Create `.jerry/presets/` directory if not exists
- Write `acidbath.yaml` preset configuration
- Define preset metadata (name, description, use_case)
- List always_run patterns: extract_poc, extract_agent_opportunities, extract_technical_content
- List custom patterns: extract_numbers_and_metrics, extract_failure_modes, generate_acidbath_outline
- List supporting patterns: extract_patterns, extract_ideas, extract_wisdom
- Add model configuration (default: haiku)

### Group C: Core Operations [parallel: true, depends: B, model: auto]
Implement the core operational modules. These can be built in parallel as they have minimal dependencies.

#### Step C.1: Implement brainstorm_ops.py
- Create `adws/adw_modules/brainstorm_ops.py`
- Implement `get_brainstorm_dir()` - read BRAINSTORM_DIR env or default to ~/dev/brainstorm
- Implement `generate_slug(title: str) -> str` - convert title to kebab-case, handle collisions with -2, -3 suffix
- Implement `init_brainstorm_dir()` - create directory structure (mkdir brainstorm, .schema/, manifest.json if not exists)
- Implement `load_manifest() -> BrainstormManifest` - read and parse manifest.json with error handling
- Implement `save_manifest(manifest: BrainstormManifest)` - write manifest.json with atomic write (temp file + rename)
- Implement `find_analysis_by_url(url: str) -> Optional[str]` - search manifest for matching source URL, return slug
- Implement `create_analysis_entry(slug, title, source_info) -> AnalysisEntry` - initialize new analysis entry
- Implement `add_version(slug, version_info) -> None` - append version to analysis entry, update latest_version
- Implement `create_version_dir(slug, version) -> Path` - create version directory, update "latest" symlink
- Add comprehensive error handling and logging

#### Step C.2: Implement github_ops.py
- Create `adws/adw_modules/github_ops.py`
- Implement `detect_github_url_type(url: str) -> Literal["blob", "tree", "unknown"]` - parse URL structure
- Implement `extract_github_file(url: str) -> ContentObject` - download raw file content from GitHub
- Implement `parse_notebook_to_markdown(ipynb_content: str) -> str` - convert .ipynb JSON to readable markdown with code cells and outputs
- Implement `extract_github_tree(url: str) -> ContentObject` - aggregate README + key files (*.py, *.md, *.ts, *.tsx)
- Implement `get_raw_github_url(url: str) -> str` - convert blob/tree URLs to raw.githubusercontent.com URLs
- Return ContentObject with type=GITHUB, text, url, title, metadata
- Handle rate limiting and authentication (use GITHUB_TOKEN env if available)
- Add comprehensive error handling for 404s, API errors

#### Step C.3: Implement diff_ops.py
- Create `adws/adw_modules/diff_ops.py`
- Implement `generate_pattern_diff(pattern_name, old_output, new_output) -> str` - create unified diff with context
- Implement `generate_diff_summary(slug, old_version, new_version) -> str` - create DIFF_FROM_vN.md summary
- Load pattern outputs from both version directories
- Compare each pattern (extract_wisdom v1 vs v2, etc.)
- Categorize changes: major (>50% changed), minor (10-50%), no change (<10%)
- Generate summary markdown with: version comparison, patterns changed, pattern-by-pattern diffs
- Write DIFF_FROM_vN.md to new version directory
- Return summary text for manifest

### Group D: Integration [parallel: false, depends: C, model: opus]
Integrate all components into the existing workflow. Requires heavy reasoning for proper integration.

#### Step D.1: Extend content_extractors.py for GitHub
- Modify `content_extractors.py` to import github_ops
- Update `detect_content_type()` to check for github.com URLs before generic URL detection
- Add `ContentType.GITHUB` case to `extract_content()` router
- Route to `github_ops.extract_github_content()` (which handles blob vs tree internally)
- Update `CONTENT_EXTRACTORS` registry to include GitHub extractor
- Add tests for GitHub URL detection

#### Step D.2: Extend pattern_executor.py for Presets
- Modify `pattern_executor.py` to support preset loading
- Implement `load_preset(preset_name: str) -> Dict[str, List[str]]` - read .jerry/presets/{name}.yaml
- Parse YAML with always_run, custom, supporting pattern lists
- Implement `get_patterns_for_preset(preset_name: str) -> List[str]` - flatten preset to pattern list
- Update `get_patterns_for_content_type()` to check for preset parameter
- Add preset validation (ensure all patterns exist)

#### Step D.3: Add Brainstorm Mode to adw_analyze_iso.py
- Add `--brainstorm` flag to adw_analyze_iso.py CLI
- Add `--preset` option (default: None, example: acidbath)
- Add `--slug` option for custom slug (default: auto-generate from title)
- When `--brainstorm` flag is set:
  - Call `init_brainstorm_dir()` to ensure directory exists
  - Extract content and get title from content_obj.title or content_obj.metadata
  - Check if URL already analyzed: `existing_slug = find_analysis_by_url(url)`
  - If exists: load existing entry, get next version (v2, v3, etc.), create version dir, generate diff from previous version
  - If new: generate slug, create analysis entry, set version to v1
  - Execute patterns (use preset if specified)
  - Save outputs to `{slug}/v{N}/patterns/`
  - Generate ANALYSIS_SUMMARY.md and metadata.json in version dir
  - Update manifest with new version info
  - Save manifest atomically
  - Update "latest" symlink
- Preserve existing behavior when `--brainstorm` not set

#### Step D.4: Create adw_brainstorm.py CLI Tool
- Create `adws/adw_brainstorm.py` with Click CLI
- Implement `list` command - load manifest, print table of analyses (slug, title, versions, latest_date, blog_status)
- Implement `status <slug>` command - show full details for one analysis (all versions, source, patterns, blog link)
- Implement `link <slug> <blog-path>` command - update manifest with blog_status=published and blog_post path
- Implement `versions <slug>` command - list all versions with dates and patterns
- Implement `diff <slug> <v1> <v2>` command - show diff between two versions (call diff_ops)
- Add rich formatting for tables (use rich library)
- Add JSON output option for programmatic access

#### Step D.5: Update analyze Command Documentation
- Modify `.claude/commands/analyze.md`
- Add `--brainstorm` flag documentation
- Add examples of brainstorm usage
- Add examples of preset usage with --preset acidbath
- Add examples of custom slugs with --slug
- Add examples of re-analysis workflow
- Document output directory structure for brainstorm mode
- Add link to adw_brainstorm.py CLI tool

### Group E: Testing and Validation [parallel: false, depends: D, model: sonnet]
Comprehensive end-to-end testing to ensure the feature works correctly.

#### Step E.1: Test YouTube Analysis to Brainstorm
- Run: `uv run adw_analyze_iso.py "https://youtube.com/watch?v=test" --preset acidbath --brainstorm`
- Verify brainstorm directory created with correct structure
- Verify manifest.json created with proper format
- Verify slug directory created with v1/ subdirectory
- Verify all ACIDBATH patterns executed (check patterns/ directory)
- Verify ANALYSIS_SUMMARY.md generated
- Verify "latest" symlink points to v1/
- Verify metadata.json contains all execution info
- Check manifest entry has correct source type (youtube), patterns_run list, timestamp

#### Step E.2: Test GitHub Notebook Analysis
- Create test GitHub notebook URL (e.g., public .ipynb file)
- Run: `uv run adw_analyze_iso.py "<github-notebook-url>" --brainstorm`
- Verify ContentType.GITHUB detected correctly
- Verify notebook parsed to readable markdown (code cells visible)
- Verify analysis created in brainstorm directory
- Check source.ipynb saved in slug directory
- Verify patterns executed successfully on parsed content
- Check manifest entry has source type "github"

#### Step E.3: Test Re-Analysis with Diff Generation
- Run same YouTube URL from E.1 again: `uv run adw_analyze_iso.py "<same-url>" --brainstorm`
- Verify existing analysis detected (slug reused)
- Verify v2/ directory created
- Verify DIFF_FROM_v1.md generated in v2/ directory
- Verify diff shows per-pattern changes
- Verify "latest" symlink updated to v2/
- Verify manifest updated with v2 entry
- Check diff summary in manifest (changes_summary field)
- Manually inspect diff for accuracy

#### Step E.4: Test CLI Tools
- Run: `uv run adws/adw_brainstorm.py list` - verify all analyses listed
- Run: `uv run adws/adw_brainstorm.py status <slug>` - verify full details shown
- Run: `uv run adws/adw_brainstorm.py versions <slug>` - verify version history
- Run: `uv run adws/adw_brainstorm.py link <slug> /path/to/blog.md` - verify manifest updated
- Check manifest.json directly for blog_status and blog_post fields
- Run: `uv run adws/adw_brainstorm.py diff <slug> v1 v2` - verify diff displayed

#### Step E.5: Test Preset System
- Run: `uv run adw_analyze_iso.py "<url>" --preset acidbath --brainstorm`
- Verify all ACIDBATH patterns executed (check patterns/ directory has all expected files)
- Verify custom patterns executed (extract_numbers_and_metrics, extract_failure_modes, generate_acidbath_outline)
- Check metadata.json has preset field set to "acidbath"
- Check patterns_run list matches acidbath.yaml configuration
- Manually review pattern outputs for quality

#### Step E.6: Test Manifest Integrity
- Run multiple analyses to create several entries
- Manually inspect manifest.json structure
- Validate manifest against schema: Use JSON schema validator
- Test concurrent writes (run two analyses simultaneously) - verify no data loss
- Test manifest recovery (corrupt manifest, ensure error handling)
- Verify atomic writes work (check for .tmp files)

## Testing Strategy

### Unit Tests
- `test_brainstorm_ops.py` - Test slug generation, manifest CRUD, version management
- `test_github_ops.py` - Test URL detection, file extraction, notebook parsing
- `test_diff_ops.py` - Test diff generation, change categorization
- `test_preset_loading.py` - Test YAML preset parsing

### Integration Tests
- Test full workflow: YouTube → brainstorm → re-analyze → diff
- Test GitHub workflow: notebook → brainstorm → analyze
- Test preset workflow: URL → ACIDBATH preset → verify all patterns
- Test CLI workflow: analyze → list → status → link

### Edge Cases
- Empty pattern outputs (diff generation with no content)
- Duplicate slugs (collision handling with -2, -3 suffix)
- Missing manifest.json (auto-creation on first run)
- Invalid GitHub URLs (404 errors, private repos)
- Corrupt .ipynb files (JSON parse errors)
- Very long titles (slug truncation)
- Special characters in titles (slug sanitization)
- Concurrent manifest writes (atomic write protection)
- Large content files (memory and performance)
- Missing patterns in preset (validation and error handling)

## Acceptance Criteria

1. ✅ Running `/analyze <youtube-url> --preset acidbath --brainstorm` creates versioned analysis in brainstorm dir
   - Directory structure: `~/dev/brainstorm/{slug}/v1/patterns/`
   - All ACIDBATH patterns executed
   - manifest.json updated with new entry
   - "latest" symlink created

2. ✅ Re-running same URL creates v2 with per-pattern diffs
   - Existing analysis detected by URL
   - v2/ directory created
   - DIFF_FROM_v1.md generated
   - Diffs show changes for each pattern
   - manifest.json updated with v2 entry

3. ✅ Manifest tracks all analyses with full metadata
   - manifest.json contains all analyses
   - Each entry has: slug, title, source, versions, tags, blog_status
   - Each version has: version, date, preset, patterns_run, model, adw_id
   - Valid JSON schema

4. ✅ GitHub notebook URLs are parsed and analyzed
   - ContentType.GITHUB detected
   - .ipynb converted to readable markdown
   - Analysis stored in brainstorm directory
   - source.ipynb saved

5. ✅ Custom ACIDBATH patterns extract POCs, numbers, and failure modes
   - extract_poc pattern works
   - extract_numbers_and_metrics pattern works
   - extract_failure_modes pattern works
   - generate_acidbath_outline pattern works
   - extract_agent_opportunities pattern works

6. ✅ `BRAINSTORM_DIR` env var controls output location
   - Default: ~/dev/brainstorm
   - Reads from environment variable
   - Creates directory if not exists

7. ✅ CLI tools work correctly
   - `adw_brainstorm.py list` shows all analyses
   - `adw_brainstorm.py status <slug>` shows details
   - `adw_brainstorm.py link <slug> <path>` updates manifest
   - `adw_brainstorm.py versions <slug>` shows history
   - `adw_brainstorm.py diff <slug> v1 v2` shows diffs

## Validation Commands

Execute these commands to validate the feature is complete:

```bash
# Verify Python syntax
uv run python -m py_compile adws/adw_modules/brainstorm_ops.py
uv run python -m py_compile adws/adw_modules/github_ops.py
uv run python -m py_compile adws/adw_modules/diff_ops.py
uv run python -m py_compile adws/adw_brainstorm.py

# Verify pattern files exist
ls .jerry/patterns/blogging/extract_numbers_and_metrics/system.md
ls .jerry/patterns/blogging/extract_failure_modes/system.md
ls .jerry/patterns/blogging/generate_acidbath_outline/system.md

# Verify preset file exists
ls .jerry/presets/acidbath.yaml

# Test YouTube analysis to brainstorm
uv run adws/adw_analyze_iso.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --preset acidbath --brainstorm --adw-id test-yt-001

# Verify directory structure created
ls ~/dev/brainstorm/manifest.json
ls ~/dev/brainstorm/*/v1/patterns/

# Test re-analysis
uv run adws/adw_analyze_iso.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --preset acidbath --brainstorm --adw-id test-yt-002

# Verify v2 created
ls ~/dev/brainstorm/*/v2/DIFF_FROM_v1.md

# Test CLI tools
uv run adws/adw_brainstorm.py list
uv run adws/adw_brainstorm.py status <slug-from-previous-command>

# Validate manifest schema
python -c "import json; json.load(open('$HOME/dev/brainstorm/manifest.json'))"
```

## Notes

### Design Decisions

1. **Persistent Storage Over Ephemeral**: Unlike `agents/{adw_id}/`, brainstorm directory is permanent. No cleanup, ever. This enables long-term knowledge base building.

2. **URL-Based Deduplication**: Re-analysis detection uses source URL matching. This means same content at different URLs creates separate entries. This is intentional - different URLs = different content items in the knowledge base.

3. **Kebab-Case Slugs**: Slugs are human-readable kebab-case (e.g., "how-to-build-agents") not UUIDs. Makes file system navigation easier. Collision handling with numeric suffixes (-2, -3) ensures uniqueness.

4. **Per-Pattern Diffs**: Diff generation happens at pattern level, not content level. This shows exactly which insights changed between versions, not just raw text changes.

5. **ACIDBATH Focus**: Preset optimized for blog post generation (Analysis, Code, Insights, Data, Blog, Agent opportunities, Testing, How-to). Other presets can be added later.

6. **Symlink for Latest**: The "latest" symlink provides a stable reference point for CI/CD or other automation that always wants the most recent analysis.

7. **Atomic Manifest Writes**: Manifest updates use temp file + rename to prevent corruption from crashes or concurrent writes.

8. **GitHub as First-Class Content**: GitHub repos/notebooks treated as primary content type, not just "URL". Enables special handling (notebook parsing, directory aggregation).

### Future Enhancements

1. **Tags System**: Add tagging UI/CLI for categorizing analyses (planned but not MVP)
2. **Search**: Full-text search across all analyses (requires additional indexing)
3. **Export**: Export to Obsidian/Notion/Markdown wiki (needs format converters)
4. **Web UI**: Interactive dashboard for browsing brainstorm (HTML + JavaScript)
5. **Smart Diffs**: Semantic diffing that understands markdown structure (not just line-by-line)
6. **Multi-Preset Analysis**: Run multiple presets on same content (e.g., ACIDBATH + technical)
7. **Automatic Re-Analysis**: Cron job to re-analyze all YouTube videos weekly
8. **Content Change Detection**: Check if YouTube video updated, trigger re-analysis automatically

### Dependencies

- **Existing**: pattern_executor.py, content_extractors.py, data_types.py, agent_sdk.py
- **New Python Packages**:
  - `PyYAML` for preset loading (add with `uv add pyyaml`)
  - `nbformat` for .ipynb parsing (add with `uv add nbformat`)
  - `rich` for CLI tables (add with `uv add rich`)
- **External Tools**:
  - GitHub API (optional GITHUB_TOKEN for higher rate limits)
  - No Fabric CLI dependency (uses bundled patterns)

### Performance Considerations

- **Parallel Pattern Execution**: Already supported by pattern_executor.py (default 4 workers)
- **Large Content**: Content files saved to disk, not kept in memory
- **Manifest Size**: JSON manifest can grow large (1000+ analyses = ~1-2MB). Acceptable for local disk.
- **Diff Generation**: Can be slow for large pattern outputs. Consider caching or lazy generation.

### Security Considerations

- **Path Traversal**: Slug generation must sanitize input to prevent path traversal attacks
- **GitHub Token**: If GITHUB_TOKEN used, store in env var, never commit to git
- **Manifest Validation**: Validate manifest JSON against schema on load to prevent injection
- **Atomic Writes**: Temp file + rename prevents partial writes from crashes
