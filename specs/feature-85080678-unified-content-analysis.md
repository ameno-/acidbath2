# Feature: Generic Content Analysis ADW - Unified Analysis Workflow

## Metadata
adw_id: `85080678`
prompt: `{"number": "generic-analysis-adw", "title": "Generic Content Analysis ADW - Unified Analysis Workflow", "body": "## Summary\n\nCreate the main content analysis ADW that accepts any input type and runs appropriate patterns through the unified pipeline. This is the primary interface for pattern-based content analysis in Jerry.\n\n## Parent Issue\n\nThis is Phase 4 of `issue-jerry-patterns-content-analysis.md`\n\n## Dependencies\n\n- Requires: `issue-pattern-executor.md` (Phase 2) completed\n- Requires: `issue-content-extractors.md` (Phase 3) completed\n\n## Deliverables\n\n### 1. Main ADW Script (`adw_analyze_iso.py`)\n\n```python\n#!/usr/bin/env -S uv run\n\"\"\"\nADW Analyze Iso - Generic content analysis in isolated worktree\n\nUsage:\n  uv run adw_analyze_iso.py <input-source> [options]\n\nInput Sources:\n  https://youtube.com/watch?v=...  - YouTube video\n  https://example.com/article      - Web URL\n  /path/to/document.pdf            - PDF file\n  /path/to/notes.txt               - Text file\n  -                                - Read from stdin\n\nOptions:\n  --patterns, -p     Comma-separated pattern names (or 'all', 'core')\n  --content-type, -t Force content type (youtube/url/pdf/text)\n  --output-dir, -o   Output directory (default: agents/{adw_id}/analyze)\n  --model, -m        Model for execution (haiku/sonnet, default: haiku)\n  --parallel         Max parallel executions (default: 4)\n  --quick            Use minimal pattern set for speed\n  --full             Use all applicable patterns\n\nExamples:\n  ./adw_analyze_iso.py \"https://youtube.com/watch?v=abc123\"\n  ./adw_analyze_iso.py ./paper.pdf --patterns analyze_paper,extract_insights\n  ./adw_analyze_iso.py https://blog.com/post --model sonnet\n  cat article.txt | ./adw_analyze_iso.py - --patterns extract_wisdom\n\"\"\"\n```\n\n### 2. Workflow Steps\n\n1. **Parse input and detect content type**\n2. **Extract content** (via content_extractors)\n3. **Select patterns** (based on type, flags, or explicit list)\n4. **Execute patterns** (via pattern_executor, parallel)\n5. **Generate outputs** (patterns/, report.md, metadata.json)\n6. **Optionally generate HTML dashboard**\n\n### 3. Pattern Selection Logic\n\n```python\nCONTENT_PATTERN_MAP = {\n    \"youtube\": {\n        \"core\": [\"extract_wisdom\", \"extract_insights\", \"extract_recommendations\", \"rate_content\"],\n        \"specialized\": [\"youtube_summary\", \"extract_youtube_metadata\", \"get_wow_per_minute\"],\n        \"conditional\": {\n            \"technical\": [\"extract_technical_content\"],\n            \"educational\": [\"extract_educational_value\", \"create_knowledge_artifacts\"],\n        }\n    },\n    \"url\": {\n        \"core\": [\"extract_wisdom\", \"extract_insights\", \"extract_recommendations\"],\n        \"specialized\": [\"extract_references\", \"extract_article_wisdom\"],\n        \"conditional\": {}\n    },\n    \"pdf\": {\n        \"core\": [\"extract_wisdom\", \"extract_insights\", \"extract_recommendations\"],\n        \"specialized\": [\"analyze_paper\", \"extract_references\"],\n        \"conditional\": {}\n    },\n    \"text\": {\n        \"core\": [\"extract_wisdom\", \"extract_insights\", \"extract_recommendations\", \"rate_content\"],\n        \"specialized\": [],\n        \"conditional\": {}\n    }\n}\n```\n\n### 4. Output Structure\n\n```\nagents/{adw_id}/analyze/\n├── metadata.json          # Input metadata + execution info\n├── content.txt            # Extracted text content\n├── patterns/              # Individual pattern outputs\n│   ├── extract_wisdom.md\n│   ├── extract_insights.md\n│   └── ...\n├── ANALYSIS_SUMMARY.md    # Executive summary\n├── report.md              # Full aggregated report\n└── index.html             # Interactive dashboard (optional)\n```\n\n### 5. Slash Command (`/analyze`)\n\n```markdown\n---\nallowed-tools: Task\nargument-hint: [input-source] [--quick|--full]\ndescription: Analyze any content using bundled patterns\n---\n\n# Analyze Content\n\nRun pattern analysis on any input type.\n\n## Input\n**INPUT_SOURCE**: $ARGUMENTS\n\n## Execution\nInvoke adw_analyze_iso.py with the input source.\n```\n\n### 6. Integration with ADW State\n\n```python\nstate = ADWState(adw_id)\nstate.update(\n    content_type=content.type.value,\n    content_source=content.source,\n    patterns_executed=list(results.keys()),\n    execution_time=total_time,\n)\n```\n\n## Acceptance Criteria\n\n- [ ] `adw_analyze_iso.py` accepts all input types\n- [ ] Content type auto-detection works correctly\n- [ ] Pattern selection based on content type\n- [ ] Parallel pattern execution works\n- [ ] Output directory structure created correctly\n- [ ] ANALYSIS_SUMMARY.md generated\n- [ ] ADW state tracking works\n- [ ] `/analyze` slash command functional\n- [ ] Stdin input (`-`) works\n\n## Technical Notes\n\n- Uses worktree isolation like other `_iso` ADWs\n- Defaults to haiku model for speed\n- `--full` flag includes all applicable patterns\n- `--quick` flag uses minimal core patterns only\n\n## Test Cases\n\n```bash\n# YouTube analysis\n./adws/adw_analyze_iso.py \"https://youtube.com/watch?v=dQw4w9WgXcQ\"\n\n# URL analysis\n./adws/adw_analyze_iso.py \"https://example.com/article\" --quick\n\n# PDF analysis with specific patterns\n./adws/adw_analyze_iso.py ./research.pdf --patterns analyze_paper,extract_insights\n\n# Stdin\necho \"Content to analyze\" | ./adws/adw_analyze_iso.py -\n```\n\n## Files to Create/Modify\n\n**Create:**\n- `adws/adw_analyze_iso.py`\n- `.claude/commands/analyze.md`\n\n**Modify:**\n- None (standalone ADW)"}`

## Feature Description

This feature implements a unified content analysis workflow that accepts any input type (YouTube videos, web URLs, PDFs, text files, or stdin) and executes appropriate fabric patterns to extract insights, wisdom, recommendations, and other valuable information. It serves as the primary user-facing interface for pattern-based content analysis in Jerry, orchestrating content extraction, pattern selection, parallel execution, and comprehensive reporting.

The workflow leverages existing Jerry patterns including worktree isolation, ADW state management, and modular design principles to create a production-ready analysis pipeline that scales with compute.

## User Story

As a Jerry user
I want to analyze any type of content (videos, articles, documents) using AI patterns
So that I can extract actionable insights, wisdom, and recommendations without manually running multiple tools

## Problem Statement

Currently, analyzing different content types (YouTube videos, web articles, PDFs, text files) requires:
1. Manual content extraction using different tools (yt-dlp, web scrapers, PDF parsers)
2. Running individual fabric patterns one at a time
3. Manually aggregating and organizing outputs
4. No standardized workflow for content analysis tasks
5. No integration with Jerry's ADW infrastructure (worktree isolation, state tracking, observability)

This creates friction for users who want to quickly analyze content and extract value, forcing them to understand multiple tools and manually orchestrate workflows.

## Solution Statement

Create `adw_analyze_iso.py`, a unified ADW that:
1. **Auto-detects content type** from input (URL patterns, file extensions, explicit flags)
2. **Extracts content** using appropriate extractors (yt-dlp for YouTube, web fetch for URLs, PyPDF for PDFs)
3. **Selects relevant patterns** based on content type and user preferences (core, specialized, conditional)
4. **Executes patterns in parallel** using fabric CLI with configurable concurrency
5. **Aggregates results** into structured outputs (individual pattern files, summary report, metadata)
6. **Tracks execution** via ADW state for observability and debugging
7. **Provides slash command interface** (`/analyze`) for Claude Code integration

This follows Jerry's composable architecture pattern and leverages existing modules for state management, worktree operations, and agent execution.

## Relevant Files

### Existing Files to Reference

- **`adws/adw_plan_iso.py`** (lines 1-100+) - Reference implementation for `_iso` ADW pattern, worktree setup, state management, and agent execution flow
- **`adws/adw_modules/workflow_ops.py`** (lines 1-150+) - Shared ADW operations including agent execution, state helpers, and workflow utilities
- **`adws/adw_modules/state.py`** (lines 1-100+) - ADW state management for tracking workflow execution and metadata
- **`adws/adw_modules/worktree_ops.py`** - Worktree creation, port allocation, and environment setup (if worktree isolation is needed)
- **`adws/adw_modules/agent.py`** - Core agent execution functions for running Claude Code prompts
- **`adws/adw_modules/utils.py`** - Utility functions for logging, environment checks, and common operations
- **`adws/adw_modules/data_types.py`** - Shared data types and Pydantic models
- **`.claude/commands/feature.md`** (lines 1-140) - Template for slash command format and structure

### New Files to Create

#### Core Analysis Workflow
- **`adws/adw_analyze_iso.py`** - Main ADW script for content analysis orchestration

#### Content Type Detection
- **`adws/adw_modules/content_types.py`** - Content type detection and classification (YouTube, URL, PDF, text)

#### Content Extractors
- **`adws/adw_modules/content_extractors.py`** - Content extraction logic for different input types:
  - YouTube: yt-dlp transcript extraction
  - URLs: Web fetch and HTML-to-markdown conversion
  - PDFs: PyPDF text extraction
  - Text files: Direct file reading
  - Stdin: Stream reading

#### Pattern Execution
- **`adws/adw_modules/pattern_executor.py`** - Parallel pattern execution using fabric CLI:
  - Pattern selection based on content type
  - Parallel execution with configurable concurrency
  - Result collection and error handling

#### Report Generation
- **`adws/adw_modules/report_generator.py`** - Aggregate pattern outputs into comprehensive reports:
  - Executive summary (ANALYSIS_SUMMARY.md)
  - Full report combining all patterns (report.md)
  - Metadata tracking (metadata.json)
  - Optional HTML dashboard generation

#### Slash Command
- **`.claude/commands/analyze.md`** - Slash command template for `/analyze` command

## Implementation Plan

### Phase 1: Foundation
Establish the core data structures, content type detection, and extraction infrastructure before implementing the main workflow.

**Tasks:**
1. Create content type detection module with URL/file pattern matching
2. Implement content extractors for each input type (YouTube, URL, PDF, text, stdin)
3. Define pattern selection maps for each content type (core, specialized, conditional)
4. Set up output directory structure and metadata tracking

### Phase 2: Core Implementation
Build the main ADW script with pattern execution, state management, and CLI interface.

**Tasks:**
1. Implement `adw_analyze_iso.py` main script with CLI argument parsing
2. Create pattern executor module for parallel fabric CLI execution
3. Integrate with ADW state management for tracking
4. Add error handling and retry logic for transient failures
5. Implement logging and observability

### Phase 3: Integration
Connect the analysis workflow with Jerry's existing infrastructure and create user interfaces.

**Tasks:**
1. Create `/analyze` slash command template
2. Generate report aggregation and summary generation
3. Add optional HTML dashboard generation
4. Write validation tests and example usage
5. Update documentation and README

## Step by Step Tasks

### Group A: Foundation - Content Type Detection and Data Structures [parallel: false, model: sonnet]
Foundational data structures and content type detection must be established first.

#### Step A.1: Create Content Type Detection Module
- Create `adws/adw_modules/content_types.py`
- Define `ContentType` enum (YOUTUBE, URL, PDF, TEXT, STDIN)
- Implement `detect_content_type(input_source: str) -> ContentType` function
- Add URL pattern matching for YouTube (watch?v=, youtu.be/, shorts/)
- Add file extension detection (.pdf, .txt, .md)
- Add special case for stdin ("-")
- Include unit tests for detection logic

#### Step A.2: Define Pattern Selection Maps
- In `content_types.py`, define `CONTENT_PATTERN_MAP` dictionary
- Map each content type to core patterns (always run)
- Map to specialized patterns (content-specific)
- Map to conditional patterns (based on content classification)
- Document pattern selection logic

#### Step A.3: Create Output Data Structures
- Define `AnalysisMetadata` Pydantic model in `adws/adw_modules/data_types.py`
- Include fields: input_source, content_type, patterns_executed, execution_time, model_used
- Define `PatternResult` model for individual pattern outputs
- Define `AnalysisReport` model for aggregated results

### Group B: Content Extraction Infrastructure [parallel: true, depends: A, model: auto]
Content extractors can be implemented in parallel as they are independent.

#### Step B.1: Implement YouTube Extractor
- Create `adws/adw_modules/content_extractors.py`
- Implement `extract_youtube_content(url: str) -> tuple[str, dict]`
- Use yt-dlp to fetch transcript and metadata
- Return (transcript_text, metadata_dict)
- Handle errors (no transcript, private video, etc.)

#### Step B.2: Implement URL Extractor
- In `content_extractors.py`, implement `extract_url_content(url: str) -> tuple[str, dict]`
- Use requests/httpx to fetch HTML
- Convert HTML to markdown using html2text or similar
- Extract metadata (title, author, publish date if available)
- Return (markdown_text, metadata_dict)

#### Step B.3: Implement PDF Extractor
- In `content_extractors.py`, implement `extract_pdf_content(filepath: str) -> tuple[str, dict]`
- Use PyPDF2 or pypdf to extract text from all pages
- Extract metadata (title, author, page count)
- Return (full_text, metadata_dict)

#### Step B.4: Implement Text/Stdin Extractor
- In `content_extractors.py`, implement `extract_text_content(source: str) -> tuple[str, dict]`
- Handle file paths: read file contents
- Handle stdin ("-"): read from sys.stdin
- Return (text_content, minimal_metadata)

#### Step B.5: Create Unified Extractor Interface
- In `content_extractors.py`, implement `extract_content(input_source: str, content_type: ContentType) -> tuple[str, dict]`
- Route to appropriate extractor based on content_type
- Standardize return format across all extractors
- Add error handling and logging

### Group C: Pattern Execution Engine [parallel: false, depends: A, model: sonnet]
Pattern executor requires content type definitions but is independent of extractors.

#### Step C.1: Create Pattern Executor Module
- Create `adws/adw_modules/pattern_executor.py`
- Define `execute_pattern(pattern_name: str, content: str, model: str, output_dir: str) -> PatternResult`
- Use subprocess to call `fabric --pattern {pattern_name}` with content via stdin
- Capture stdout as pattern result
- Write result to `{output_dir}/patterns/{pattern_name}.md`
- Return PatternResult object with success status, output, execution time

#### Step C.2: Implement Parallel Pattern Execution
- In `pattern_executor.py`, implement `execute_patterns_parallel(patterns: list[str], content: str, model: str, output_dir: str, max_parallel: int) -> dict[str, PatternResult]`
- Use `concurrent.futures.ThreadPoolExecutor` for parallel execution
- Set max_workers to max_parallel parameter
- Collect all results into dictionary keyed by pattern name
- Handle individual pattern failures gracefully (don't fail entire batch)

#### Step C.3: Implement Pattern Selection Logic
- In `pattern_executor.py`, implement `select_patterns(content_type: ContentType, quick: bool, full: bool, explicit_patterns: list[str]) -> list[str]`
- If explicit_patterns provided, use those (validate they exist)
- If quick=True, return only core patterns for content_type
- If full=True, return core + specialized + all conditional patterns
- Default: return core + specialized patterns
- Use CONTENT_PATTERN_MAP from content_types module

### Group D: Report Generation [parallel: false, depends: B, C, model: auto]
Report generation requires both extraction and pattern execution to be complete.

#### Step D.1: Create Report Generator Module
- Create `adws/adw_modules/report_generator.py`
- Implement `generate_analysis_summary(pattern_results: dict[str, PatternResult], metadata: AnalysisMetadata) -> str`
- Create executive summary with key insights from each pattern
- Limit to 1-2 pages of high-value content
- Return markdown formatted summary

#### Step D.2: Implement Full Report Aggregation
- In `report_generator.py`, implement `generate_full_report(pattern_results: dict[str, PatternResult], metadata: AnalysisMetadata, content_preview: str) -> str`
- Combine all pattern outputs into single report
- Include table of contents with links to each section
- Add metadata section at top
- Include content preview (first 500 chars)
- Return full markdown report

#### Step D.3: Implement Metadata JSON Generation
- In `report_generator.py`, implement `generate_metadata_json(metadata: AnalysisMetadata, pattern_results: dict[str, PatternResult]) -> dict`
- Create comprehensive metadata including input details, execution stats, pattern list
- Include timestamps, durations, success/failure counts
- Return dictionary ready for JSON serialization

#### Step D.4: Optional HTML Dashboard Generator
- In `report_generator.py`, implement `generate_html_dashboard(report: str, metadata: dict, pattern_results: dict) -> str`
- Create interactive single-page HTML with embedded CSS/JS
- Include searchable table of contents
- Add collapsible sections for each pattern
- Include download buttons for individual reports
- Return HTML string

### Group E: Main ADW Script [parallel: false, depends: A, B, C, D, model: opus]
Main orchestration script requires all components to be complete.

#### Step E.1: Create Main Script Structure
- Create `adws/adw_analyze_iso.py`
- Add shebang: `#!/usr/bin/env -S uv run`
- Add inline script dependencies for uv
- Import necessary modules (click for CLI, all adw_modules)
- Define main CLI function with click decorators

#### Step E.2: Implement CLI Argument Parsing
- Add click arguments and options:
  - `input_source` (required, positional)
  - `--patterns, -p` (comma-separated list)
  - `--content-type, -t` (force content type)
  - `--output-dir, -o` (custom output location)
  - `--model, -m` (haiku/sonnet, default: haiku)
  - `--parallel` (max concurrent executions, default: 4)
  - `--quick` (minimal pattern set flag)
  - `--full` (all patterns flag)
  - `--dry-run` (show what would run without executing)
- Add validation logic for mutually exclusive flags (quick vs full)

#### Step E.3: Implement Content Type Detection and Extraction
- In main function, detect content type using `detect_content_type()`
- Allow override with `--content-type` flag
- Call `extract_content()` to get content text and metadata
- Handle extraction errors with helpful error messages
- Log extraction progress

#### Step E.4: Implement Pattern Selection and Execution
- Parse explicit patterns from `--patterns` flag if provided
- Otherwise, call `select_patterns()` based on content type and flags
- Display selected patterns to user before execution
- Call `execute_patterns_parallel()` with content and configuration
- Show progress indicators during execution
- Handle execution errors and partial failures

#### Step E.5: Implement Output Generation
- Create output directory structure: `agents/{adw_id}/analyze/`
- Write extracted content to `content.txt`
- Create `patterns/` subdirectory for individual outputs
- Generate and write `ANALYSIS_SUMMARY.md`
- Generate and write `report.md`
- Generate and write `metadata.json`
- Optionally generate `index.html` if requested

#### Step E.6: Implement ADW State Integration
- Generate or use provided adw_id
- Create ADWState instance
- Update state with content type, source, patterns executed
- Add execution time and success status
- Save state to disk
- Add state tracking to output directory

#### Step E.7: Add Error Handling and Logging
- Set up logger with appropriate verbosity
- Add try/catch blocks around major operations
- Provide helpful error messages for common failures
- Add retry logic for transient failures (network issues)
- Log all important events and decisions

#### Step E.8: Add Dry Run Mode
- When `--dry-run` flag is set, show:
  - Detected content type
  - Content extraction plan (which extractor)
  - Selected patterns list
  - Output directory structure
  - Estimated execution time
- Exit without executing

### Group F: Integration and User Interfaces [parallel: false, depends: E, model: auto]
Integration work requires the main script to be functional.

#### Step F.1: Create Slash Command Template
- Create `.claude/commands/analyze.md`
- Add frontmatter with allowed-tools (Bash, Task)
- Add argument-hint for user guidance
- Write command description
- Add template body that invokes `adw_analyze_iso.py` with `$ARGUMENTS`
- Include usage examples in comments

#### Step F.2: Add Validation Tests
- Create test script or add to existing test suite
- Test each content type (YouTube, URL, PDF, text, stdin)
- Test pattern selection logic (quick, full, explicit)
- Test error handling (invalid URLs, missing files)
- Test output structure validation
- Test ADW state tracking

#### Step F.3: Create Usage Examples
- Add example invocations to docstring in main script
- Create example input files for testing (sample.txt, sample.pdf)
- Document expected outputs for each example
- Add examples to slash command template

#### Step F.4: Update Documentation
- Add entry to README workflow table
- Document dependencies (yt-dlp, fabric, PyPDF, etc.)
- Add installation instructions if needed
- Document pattern selection logic
- Add troubleshooting section

## Testing Strategy

### Unit Tests

1. **Content Type Detection Tests**
   - Test YouTube URL patterns (watch?v=, youtu.be/, /shorts/)
   - Test file extension detection (.pdf, .txt, .md, .docx)
   - Test stdin detection ("-")
   - Test explicit content type override
   - Test edge cases (malformed URLs, missing extensions)

2. **Content Extraction Tests**
   - Test YouTube extraction with mock yt-dlp responses
   - Test URL extraction with mock HTTP responses
   - Test PDF extraction with sample PDF files
   - Test text file extraction
   - Test stdin extraction with simulated input
   - Test error handling for each extractor

3. **Pattern Selection Tests**
   - Test core pattern selection for each content type
   - Test quick mode (minimal patterns)
   - Test full mode (all patterns)
   - Test explicit pattern list
   - Test pattern validation (reject invalid patterns)

4. **Pattern Execution Tests**
   - Test single pattern execution
   - Test parallel execution with multiple patterns
   - Test error handling for failed patterns
   - Test output file creation
   - Test execution timeout handling

5. **Report Generation Tests**
   - Test summary generation from pattern results
   - Test full report aggregation
   - Test metadata JSON structure
   - Test HTML dashboard generation
   - Test empty/missing pattern handling

6. **ADW State Tests**
   - Test state creation and updates
   - Test state persistence to disk
   - Test state retrieval
   - Test metadata storage

### Integration Tests

1. **End-to-End YouTube Analysis**
   - Input: Real YouTube URL
   - Expected: Transcript extracted, patterns executed, reports generated
   - Validate: All output files present and non-empty

2. **End-to-End URL Analysis**
   - Input: Public web article URL
   - Expected: Article content extracted, patterns executed, reports generated
   - Validate: Output structure and content quality

3. **End-to-End PDF Analysis**
   - Input: Sample PDF document
   - Expected: Text extracted, patterns executed, reports generated
   - Validate: Text extraction quality and pattern results

4. **Stdin Pipeline Test**
   - Input: Text via stdin
   - Expected: Content processed, patterns executed
   - Validate: Pipeline compatibility

5. **Slash Command Integration**
   - Execute `/analyze` with sample inputs
   - Validate: Command routing and execution

### Edge Cases

1. **Invalid Inputs**
   - Non-existent file paths
   - Invalid URLs (404, connection errors)
   - Malformed YouTube URLs
   - Corrupted PDF files
   - Empty stdin
   - Binary files passed as text

2. **Pattern Failures**
   - Pattern execution timeout
   - Pattern returns error
   - Fabric CLI not installed
   - Invalid pattern name requested
   - Partial pattern failures (some succeed, some fail)

3. **Resource Constraints**
   - Very large content (100+ page PDFs)
   - Very long YouTube videos (3+ hours)
   - Network timeouts during extraction
   - Disk space constraints for outputs
   - Memory limits during parallel execution

4. **Concurrency Issues**
   - Max parallel executions respected
   - No race conditions in file writes
   - Proper cleanup on interruption (Ctrl+C)

5. **State Management Edge Cases**
   - Missing ADW ID
   - Corrupted state file
   - State directory permissions issues

## Acceptance Criteria

1. ✅ **Input Handling**
   - Accepts YouTube URLs (all variants: watch?v=, youtu.be/, /shorts/)
   - Accepts web URLs (http://, https://)
   - Accepts file paths (.pdf, .txt, .md, etc.)
   - Accepts stdin input ("-")
   - Provides clear error messages for invalid inputs

2. ✅ **Content Type Detection**
   - Correctly auto-detects content type from input
   - Respects `--content-type` override flag
   - Logs detected content type for user visibility

3. ✅ **Content Extraction**
   - Successfully extracts YouTube transcripts using yt-dlp
   - Successfully extracts web content and converts to markdown
   - Successfully extracts text from PDF files
   - Successfully reads text files and stdin
   - Handles extraction errors gracefully with helpful messages

4. ✅ **Pattern Selection**
   - Selects core patterns by default
   - `--quick` flag uses minimal pattern set
   - `--full` flag uses all applicable patterns
   - `--patterns` flag accepts explicit comma-separated list
   - Validates pattern names and rejects invalid ones

5. ✅ **Pattern Execution**
   - Executes patterns in parallel with configurable concurrency
   - Respects `--parallel` limit (default: 4)
   - Handles individual pattern failures without stopping execution
   - Writes each pattern result to separate file in `patterns/` directory
   - Shows progress during execution

6. ✅ **Output Structure**
   - Creates directory: `agents/{adw_id}/analyze/`
   - Generates `content.txt` with extracted content
   - Generates `patterns/` directory with individual pattern outputs
   - Generates `ANALYSIS_SUMMARY.md` with executive summary
   - Generates `report.md` with full aggregated report
   - Generates `metadata.json` with execution metadata
   - Optional: Generates `index.html` interactive dashboard

7. ✅ **ADW State Tracking**
   - Creates ADWState instance with unique adw_id
   - Updates state with content type, source, patterns executed
   - Saves state to `adw_state.json`
   - State is retrievable and valid JSON

8. ✅ **Slash Command Integration**
   - `/analyze` command exists in `.claude/commands/`
   - Command properly invokes `adw_analyze_iso.py`
   - Arguments are passed through correctly
   - Command provides usage hints

9. ✅ **CLI Interface**
   - Clear help text with `--help` flag
   - Proper argument validation
   - User-friendly error messages
   - Progress indicators during long operations
   - Dry-run mode (`--dry-run`) shows execution plan without running

10. ✅ **Error Handling**
    - Network errors during extraction handled gracefully
    - Missing dependencies (yt-dlp, fabric) reported clearly
    - File system errors (permissions, disk space) handled
    - Pattern execution errors don't crash entire workflow
    - Provides actionable error messages

11. ✅ **Performance**
    - Parallel execution reduces total time vs sequential
    - Respects concurrency limits to avoid resource exhaustion
    - Large content (100+ pages) processed successfully
    - Memory usage stays reasonable during execution

12. ✅ **Documentation**
    - Main script has comprehensive docstring with examples
    - Slash command has usage documentation
    - README updated with workflow entry
    - Dependencies documented

## Validation Commands

Execute these commands to validate the feature is complete:

### 1. Code Compilation
```bash
uv run python -m py_compile adws/adw_analyze_iso.py
uv run python -m py_compile adws/adw_modules/content_types.py
uv run python -m py_compile adws/adw_modules/content_extractors.py
uv run python -m py_compile adws/adw_modules/pattern_executor.py
uv run python -m py_compile adws/adw_modules/report_generator.py
```

### 2. Dependency Check
```bash
# Verify fabric is installed
which fabric

# Verify yt-dlp is installed
which yt-dlp

# Verify Python packages
uv run python -c "import pypdf; import requests; import concurrent.futures; print('All packages available')"
```

### 3. Help Text Validation
```bash
uv run adws/adw_analyze_iso.py --help
# Should display comprehensive help with all options
```

### 4. Dry Run Tests
```bash
# Test YouTube dry run
uv run adws/adw_analyze_iso.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --dry-run

# Test URL dry run
uv run adws/adw_analyze_iso.py "https://example.com" --dry-run --quick

# Test file dry run
echo "Test content" > /tmp/test.txt
uv run adws/adw_analyze_iso.py /tmp/test.txt --dry-run --full
```

### 5. End-to-End Execution Tests
```bash
# YouTube analysis
uv run adws/adw_analyze_iso.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --quick

# Verify output structure
test -f agents/*/analyze/content.txt
test -d agents/*/analyze/patterns/
test -f agents/*/analyze/ANALYSIS_SUMMARY.md
test -f agents/*/analyze/report.md
test -f agents/*/analyze/metadata.json
```

### 6. Pattern Selection Validation
```bash
# Test explicit patterns
uv run adws/adw_analyze_iso.py "https://example.com" --patterns extract_wisdom,extract_insights

# Test quick mode
uv run adws/adw_analyze_iso.py "https://example.com" --quick

# Test full mode
uv run adws/adw_analyze_iso.py "https://example.com" --full
```

### 7. Stdin Test
```bash
echo "Sample content for analysis" | uv run adws/adw_analyze_iso.py - --patterns extract_wisdom
```

### 8. Slash Command Test
```bash
# Verify slash command exists
test -f .claude/commands/analyze.md

# Test via Claude Code (manual validation)
# claude /analyze "https://youtube.com/watch?v=dQw4w9WgXcQ" --quick
```

### 9. State Validation
```bash
# Check state file exists and is valid JSON
test -f agents/*/adw_state.json
cat agents/*/adw_state.json | jq .
# Should output valid JSON with content_type, content_source, patterns_executed fields
```

### 10. Error Handling Tests
```bash
# Test invalid URL
uv run adws/adw_analyze_iso.py "https://invalid-url-that-does-not-exist.com" 2>&1 | grep -i error

# Test non-existent file
uv run adws/adw_analyze_iso.py "/path/that/does/not/exist.pdf" 2>&1 | grep -i error

# Test invalid pattern
uv run adws/adw_analyze_iso.py "https://example.com" --patterns invalid_pattern_name 2>&1 | grep -i error
```

## Notes

### Dependencies

This feature requires the following dependencies to be installed:

#### System Dependencies
```bash
# Fabric CLI (for pattern execution)
pipx install fabric

# yt-dlp (for YouTube content extraction)
brew install yt-dlp  # macOS
# or
pip install yt-dlp
```

#### Python Dependencies (add via uv)
```bash
# In pyproject.toml or uv add:
uv add click         # CLI framework
uv add pypdf         # PDF text extraction
uv add requests      # HTTP requests for URL fetching
uv add html2text     # HTML to Markdown conversion
uv add pydantic      # Data validation
uv add python-dotenv # Environment management
```

### Future Enhancements

1. **Content Type Expansion**
   - DOCX file support (python-docx)
   - Audio file support (whisper transcription)
   - Video file support (local video processing)
   - Image analysis (OCR + vision models)

2. **Pattern Intelligence**
   - Auto-detect content category (technical, educational, entertainment)
   - Conditionally select specialized patterns based on content analysis
   - Learn from user pattern preferences over time

3. **Enhanced Reporting**
   - Export to multiple formats (PDF, HTML, Markdown, JSON)
   - Interactive web dashboard with search and filtering
   - Email report delivery
   - Slack/Discord integration for notifications

4. **Performance Optimizations**
   - Cache extracted content to avoid re-fetching
   - Incremental pattern execution (only run new patterns)
   - Distributed execution across multiple machines
   - GPU acceleration for pattern processing

5. **Collaboration Features**
   - Share analysis results via URLs
   - Collaborative annotation of insights
   - Team pattern libraries
   - Analysis templates for common use cases

### Design Decisions

1. **Why worktree isolation?**
   - While this ADW doesn't modify code, worktree isolation provides a clean execution environment and allows parallel analysis runs without conflicts in output directories.

2. **Why default to haiku model?**
   - Most fabric patterns work well with haiku, providing fast execution at lower cost. Users can override with `--model sonnet` for complex analysis needs.

3. **Why parallel execution?**
   - Fabric patterns are independent and I/O-bound, making them ideal for parallel execution. This significantly reduces total analysis time for multi-pattern runs.

4. **Why fabric CLI instead of direct API calls?**
   - Fabric CLI provides mature pattern library, caching, and error handling. We leverage existing tooling rather than reimplementing pattern execution.

5. **Why support stdin?**
   - Enables Unix pipeline composition and integration with other tools (e.g., `curl | adw_analyze_iso.py -`), following the principle of composability.
