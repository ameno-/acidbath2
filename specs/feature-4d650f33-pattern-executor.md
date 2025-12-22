# Feature: Pattern Executor Module - Execute Bundled Patterns via Claude SDK

## Metadata
adw_id: `4d650f33`
prompt: `{"number": "pattern-executor", "title": "Pattern Executor Module - Execute Bundled Patterns via Claude SDK", "body": "## Summary\n\nCreate the pattern execution module that runs bundled Fabric patterns using the Claude Code SDK. This replaces the runtime Fabric CLI dependency with self-contained pattern execution.\n\n## Parent Issue\n\nThis is Phase 2 of `issue-jerry-patterns-content-analysis.md`\n\n## Dependencies\n\n- Requires: `issue-pattern-infrastructure.md` (Phase 1) completed\n\n## Deliverables\n\n### 1. Pattern Executor Module (`adw_modules/pattern_executor.py`)\n\nCore functions:\n\n```python\n@dataclass\nclass PatternResult:\n    pattern: str\n    success: bool\n    output: str\n    execution_time: float\n    error: Optional[str] = None\n\ndef get_pattern_prompt(pattern_name: str) -> str:\n    \"\"\"Load pattern system prompt from bundled patterns.\"\"\"\n\ndef execute_pattern(\n    pattern_name: str,\n    input_text: str,\n    model: str = \"haiku\"\n) -> PatternResult:\n    \"\"\"Execute a single pattern against input text via Claude SDK.\"\"\"\n\ndef execute_patterns_parallel(\n    patterns: list[str],\n    input_text: str,\n    model: str = \"haiku\",\n    max_workers: int = 4,\n) -> dict[str, PatternResult]:\n    \"\"\"Execute multiple patterns in parallel.\"\"\"\n\ndef list_available_patterns() -> dict:\n    \"\"\"List all bundled patterns with metadata.\"\"\"\n\ndef get_patterns_for_content_type(content_type: str) -> list[str]:\n    \"\"\"Get recommended patterns for a content type.\"\"\"\n\ndef validate_pattern_exists(pattern_name: str) -> bool:\n    \"\"\"Check if a pattern is available in the bundle.\"\"\"\n```\n\n### 2. Claude SDK Integration\n\nUse `agent_sdk.simple_query()` for pattern execution:\n\n```python\nfrom .agent_sdk import simple_query\n\ndef execute_pattern(pattern_name: str, input_text: str, model: str = \"haiku\") -> PatternResult:\n    system_prompt = get_pattern_prompt(pattern_name)\n    full_prompt = f\"{system_prompt}\\n\\n# INPUT\\n\\n{input_text}\"\n    output = simple_query(full_prompt, model=model)\n    return PatternResult(pattern=pattern_name, success=True, output=output, ...)\n```\n\n### 3. Parallel Execution\n\nUse ThreadPoolExecutor for concurrent pattern execution:\n- Default 4 workers (configurable)\n- Track execution time per pattern\n- Aggregate results in dict\n- Handle individual failures gracefully\n\n### 4. Pattern Discovery Functions\n\n```python\ndef get_patterns_by_category(category: str) -> list[str]:\n    \"\"\"Get all patterns in a category.\"\"\"\n\ndef search_patterns(query: str) -> list[str]:\n    \"\"\"Search patterns by name or description.\"\"\"\n\ndef get_pattern_info(pattern_name: str) -> dict:\n    \"\"\"Get full metadata for a pattern.\"\"\"\n```\n\n## Acceptance Criteria\n\n- [ ] `pattern_executor.py` module created in `adw_modules/`\n- [ ] `execute_pattern()` successfully runs bundled patterns\n- [ ] `execute_patterns_parallel()` runs multiple patterns concurrently\n- [ ] `list_available_patterns()` returns manifest data\n- [ ] Error handling for missing/invalid patterns\n- [ ] Execution time tracking works correctly\n- [ ] Unit tests for core functions\n\n## Technical Notes\n\n- All pattern execution uses Claude Code SDK (no external dependencies)\n- Patterns are loaded from `.jerry/patterns/{category}/{name}/system.md`\n- Model selection: \"haiku\" for speed, \"sonnet\" for depth\n- Parallel execution respects rate limits\n\n## Test Cases\n\n```python\n# Test single pattern execution\nresult = execute_pattern(\"extract_wisdom\", \"Sample text content\")\nassert result.success\nassert len(result.output) > 0\n\n# Test parallel execution\nresults = execute_patterns_parallel(\n    [\"extract_wisdom\", \"extract_insights\", \"rate_content\"],\n    \"Sample text content\"\n)\nassert len(results) == 3\nassert all(r.success for r in results.values())\n\n# Test pattern listing\npatterns = list_available_patterns()\nassert \"extract_wisdom\" in patterns[\"patterns\"]\n```\n\n## Files to Create/Modify\n\n**Create:**\n- `adws/adw_modules/pattern_executor.py`\n\n**Modify:**\n- `adws/adw_modules/__init__.py` (export new module)"}`

## Feature Description

Create a Python module that executes bundled Fabric patterns using the Claude Code SDK. This module replaces the runtime dependency on the Fabric CLI tool with self-contained pattern execution. The module provides both synchronous and parallel pattern execution, pattern discovery, and comprehensive error handling. This is Phase 2 of the Jerry Patterns Content Analysis feature.

The Pattern Executor Module enables Jerry to run content analysis patterns (like `extract_wisdom`, `extract_insights`, `rate_content`) against input text without requiring external CLI dependencies. It leverages the existing `agent_sdk.py` module for Claude API communication and provides a clean, type-safe interface for pattern operations.

## User Story

As a Jerry workflow developer
I want to execute Fabric patterns programmatically via the Claude SDK
So that I can analyze content without runtime CLI dependencies and integrate pattern execution into automated workflows

## Problem Statement

Currently, Jerry relies on the external Fabric CLI tool for content analysis patterns. This creates several issues:
1. **Runtime Dependency**: Requires Fabric CLI to be installed and configured on the system
2. **Limited Integration**: CLI-based execution is harder to integrate into Python workflows
3. **No Type Safety**: CLI outputs are unstructured strings requiring manual parsing
4. **Limited Error Handling**: CLI failures are opaque and difficult to debug
5. **No Parallel Execution**: Running multiple patterns requires sequential CLI calls

The goal is to replace CLI-based pattern execution with a self-contained Python module that bundles patterns and executes them via the Claude SDK.

## Solution Statement

Implement a `pattern_executor.py` module that:
1. **Loads Patterns**: Read pattern system prompts from `.jerry/patterns/{category}/{name}/system.md`
2. **Executes via SDK**: Use the existing `agent_sdk.simple_query()` for Claude API calls
3. **Parallel Execution**: Support concurrent pattern execution using ThreadPoolExecutor
4. **Pattern Discovery**: Provide functions to list, search, and filter available patterns
5. **Type-Safe Results**: Return structured `PatternResult` objects with execution metadata
6. **Error Resilience**: Handle missing patterns, API failures, and timeout scenarios gracefully

The module integrates seamlessly with Jerry's existing infrastructure:
- Uses `adw_modules/agent_sdk.py` for Claude API communication
- Follows Jerry's Pydantic-based typing conventions from `data_types.py`
- Supports model selection (haiku for speed, sonnet for depth)
- Provides comprehensive logging via Jerry's `utils.py` logger

## Relevant Files

### Existing Files to Reference

- **`adws/adw_modules/agent_sdk.py`** - Claude SDK wrapper providing `simple_query()` function for pattern execution. This is the foundation for making Claude API calls.

- **`adws/adw_modules/data_types.py`** - Pydantic models and data structures. We'll follow the existing patterns for creating `PatternResult` and related types.

- **`adws/adw_modules/__init__.py`** - Module exports. We'll add the new pattern executor exports here.

- **`adws/adw_modules/utils.py`** - Core utilities including `setup_logger()` and `get_project_root()`. Used for logging and path resolution.

- **`.jerry/manifest.json`** - Jerry framework manifest. May need updating to include pattern-related metadata if Phase 1 created pattern infrastructure.

### New Files

- **`adws/adw_modules/pattern_executor.py`** - Main pattern executor module with all core functionality

## Implementation Plan

### Phase 1: Foundation
Set up the basic pattern executor infrastructure including data types, file system operations for pattern loading, and pattern manifest parsing. This phase establishes the foundation without Claude SDK integration.

### Phase 2: Core Implementation
Implement the core pattern execution functions using the Claude SDK. Add synchronous single-pattern execution, then extend to parallel multi-pattern execution. Include comprehensive error handling and execution time tracking.

### Phase 3: Integration
Integrate the pattern executor with Jerry's module system, add logging, write tests, and update documentation. Ensure the module works seamlessly with existing Jerry infrastructure.

## Step by Step Tasks

### Group A: Foundation [parallel: false, model: sonnet]
Sequential foundational work establishing data structures and pattern loading infrastructure.

#### Step A.1: Create Pattern Data Types
- Create `adws/adw_modules/pattern_executor.py` with initial imports
- Define `PatternResult` dataclass with fields: pattern, success, output, execution_time, error
- Define `PatternMetadata` dataclass for pattern info: name, category, description, tags
- Define `PatternManifest` dataclass for manifest parsing
- Import necessary dependencies: dataclasses, pathlib, typing, asyncio, concurrent.futures

#### Step A.2: Implement Pattern File System Operations
- Create `_get_patterns_directory()` helper to resolve `.jerry/patterns/` path using `get_project_root()`
- Implement `get_pattern_prompt(pattern_name: str) -> str` to load pattern system.md files
- Add path validation to handle missing pattern directories gracefully
- Support pattern paths in format: `.jerry/patterns/{category}/{name}/system.md`

#### Step A.3: Implement Pattern Discovery Functions
- Implement `validate_pattern_exists(pattern_name: str) -> bool` to check pattern availability
- Implement `list_available_patterns() -> dict` to scan `.jerry/patterns/` and return manifest-like structure
- Implement `get_pattern_info(pattern_name: str) -> dict` to return metadata for a specific pattern
- Add error handling for filesystem access issues

### Group B: Core Pattern Execution [parallel: false, depends: A, model: sonnet]
Sequential implementation of pattern execution capabilities, building from single to parallel execution.

#### Step B.1: Implement Single Pattern Execution
- Import `simple_query` from `agent_sdk.py`
- Implement `execute_pattern(pattern_name: str, input_text: str, model: str = "haiku") -> PatternResult`
- Load pattern prompt using `get_pattern_prompt()`
- Construct full prompt: `"{system_prompt}\n\n# INPUT\n\n{input_text}"`
- Execute using `await simple_query(full_prompt, model=model)`
- Track execution time using `time.perf_counter()`
- Handle errors and return `PatternResult` with appropriate success/error fields
- Add async wrapper function since `simple_query` is async

#### Step B.2: Implement Synchronous Wrapper
- Create `execute_pattern_sync()` as synchronous wrapper around async `execute_pattern()`
- Use `asyncio.run()` to execute async function from sync context
- Add proper event loop handling for different Python versions
- This allows both sync and async usage patterns

#### Step B.3: Implement Parallel Pattern Execution
- Implement `execute_patterns_parallel(patterns: list[str], input_text: str, model: str = "haiku", max_workers: int = 4) -> dict[str, PatternResult]`
- Use `ThreadPoolExecutor` with configurable max_workers
- Execute patterns concurrently using thread pool
- Aggregate results into dictionary keyed by pattern name
- Handle individual pattern failures gracefully (partial success)
- Track overall execution time
- Add async version using `asyncio.gather()` for better concurrency

### Group C: Advanced Discovery and Filtering [parallel: false, depends: B, model: auto]
Additional pattern discovery features that build on core functionality.

#### Step C.1: Implement Pattern Filtering Functions
- Implement `get_patterns_by_category(category: str) -> list[str]` to filter patterns by category
- Implement `search_patterns(query: str) -> list[str]` to search patterns by name or description
- Implement `get_patterns_for_content_type(content_type: str) -> list[str]` to get recommended patterns
- Add fuzzy matching support for search functionality

#### Step C.2: Add Pattern Caching
- Implement in-memory cache for loaded pattern prompts to avoid repeated file reads
- Use simple dict cache with pattern_name as key
- Add cache invalidation mechanism
- Add optional `use_cache: bool` parameter to pattern loading functions

### Group D: Integration and Testing [parallel: false, depends: C, model: sonnet]
Integration with Jerry's module system, comprehensive testing, and documentation.

#### Step D.1: Update Module Exports
- Modify `adws/adw_modules/__init__.py` to export pattern executor components
- Add imports for: `PatternResult`, `execute_pattern`, `execute_patterns_parallel`, `list_available_patterns`
- Add to `__all__` list for public API exposure
- Ensure backward compatibility with existing imports

#### Step D.2: Add Logging and Observability
- Add logging using `setup_logger()` from `utils.py`
- Log pattern execution start/completion with timing
- Log pattern loading operations
- Log errors with full stack traces
- Add debug-level logging for cache operations

#### Step D.3: Create Unit Tests
- Create test file `adws/adw_modules/test_pattern_executor.py`
- Test `execute_pattern()` with mock pattern
- Test `execute_patterns_parallel()` with multiple patterns
- Test `list_available_patterns()` returns expected structure
- Test error handling for missing patterns
- Test timeout and failure scenarios
- Use pytest with async support (`pytest-asyncio`)

#### Step D.4: Update Documentation
- Add docstrings to all public functions following Google/NumPy style
- Include usage examples in module docstring
- Document model selection guidelines (haiku vs sonnet)
- Add inline comments for complex logic
- Update README.md or create pattern executor documentation in ai_docs/

## Testing Strategy

### Unit Tests

**Pattern Loading Tests:**
- Test `get_pattern_prompt()` with valid pattern name
- Test `get_pattern_prompt()` with invalid pattern name (should raise FileNotFoundError)
- Test pattern path resolution from project root

**Pattern Execution Tests:**
- Test `execute_pattern()` returns successful `PatternResult` with output
- Test `execute_pattern()` handles Claude API errors gracefully
- Test execution time tracking is accurate (within tolerance)
- Mock `simple_query()` to avoid API calls in tests

**Parallel Execution Tests:**
- Test `execute_patterns_parallel()` runs 3+ patterns concurrently
- Test partial failure scenario (1 pattern fails, others succeed)
- Test max_workers configuration affects concurrency
- Verify results dictionary contains all requested patterns

**Pattern Discovery Tests:**
- Test `list_available_patterns()` returns dict with expected keys
- Test `validate_pattern_exists()` returns True for existing patterns
- Test `validate_pattern_exists()` returns False for non-existent patterns
- Test `get_pattern_info()` returns metadata dict

**Model Selection Tests:**
- Test model parameter is passed correctly to `simple_query()`
- Test default model is "haiku"
- Test "sonnet" and "opus" models work correctly

### Integration Tests

**End-to-End Pattern Execution:**
- Test actual pattern execution against real `.jerry/patterns/` (if available)
- Test with sample input text from test fixtures
- Validate output format matches expected structure

**Cache Tests:**
- Test pattern prompt caching reduces file reads
- Test cache invalidation works correctly
- Test concurrent cache access (thread safety)

### Edge Cases

1. **Missing Pattern Directory**: Test behavior when `.jerry/patterns/` doesn't exist
2. **Empty Pattern File**: Test when `system.md` exists but is empty
3. **Invalid Pattern Name**: Test special characters, path traversal attempts
4. **Large Input Text**: Test with >100KB input to verify no truncation issues
5. **Timeout Scenarios**: Test behavior when Claude API is slow/unresponsive
6. **Concurrent Access**: Test parallel execution with shared resources
7. **Model Fallback**: Test graceful degradation if requested model unavailable
8. **Unicode Handling**: Test patterns with non-ASCII characters in prompts/input

## Acceptance Criteria

- [ ] `adws/adw_modules/pattern_executor.py` module created with all required functions
- [ ] `execute_pattern()` successfully executes a single pattern and returns `PatternResult`
- [ ] `execute_patterns_parallel()` executes multiple patterns concurrently with max_workers configuration
- [ ] `list_available_patterns()` returns dictionary with pattern metadata from `.jerry/patterns/`
- [ ] `validate_pattern_exists()` correctly identifies existing and missing patterns
- [ ] Error handling gracefully manages missing patterns, API failures, and timeouts
- [ ] Execution time tracking captures accurate timing for each pattern execution
- [ ] Pattern prompts are loaded from `.jerry/patterns/{category}/{name}/system.md`
- [ ] Both synchronous and asynchronous APIs are available
- [ ] Module is exported in `adws/adw_modules/__init__.py`
- [ ] Comprehensive logging added for debugging and observability
- [ ] Unit tests cover core functionality with >80% code coverage
- [ ] Documentation includes docstrings, usage examples, and inline comments
- [ ] Integration with existing Jerry infrastructure (agent_sdk, utils, data_types) works seamlessly
- [ ] Parallel execution handles partial failures without crashing

## Validation Commands

Execute these commands to validate the feature is complete:

```bash
# Test Python syntax and imports
uv run python -m py_compile adws/adw_modules/pattern_executor.py

# Verify module exports
uv run python -c "from adw_modules.pattern_executor import PatternResult, execute_pattern, execute_patterns_parallel, list_available_patterns; print('Exports OK')"

# Run unit tests
uv run pytest adws/adw_modules/test_pattern_executor.py -v

# Test pattern discovery (requires .jerry/patterns/ to exist)
uv run python -c "from adw_modules.pattern_executor import list_available_patterns; import json; print(json.dumps(list_available_patterns(), indent=2))"

# Test single pattern execution (requires actual pattern)
# uv run python -c "from adw_modules.pattern_executor import execute_pattern_sync; result = execute_pattern_sync('extract_wisdom', 'Test input'); print(f'Success: {result.success}, Time: {result.execution_time:.2f}s')"

# Verify type checking
uv run mypy adws/adw_modules/pattern_executor.py --ignore-missing-imports

# Check code formatting
uv run ruff check adws/adw_modules/pattern_executor.py
```

## Notes

### Dependencies
This feature requires Phase 1 (Pattern Infrastructure) to be completed first. Phase 1 should provide:
- `.jerry/patterns/` directory structure
- Pattern manifest or metadata system
- Sample patterns for testing (e.g., `extract_wisdom`, `extract_insights`)

If Phase 1 is not yet complete, we can proceed with the pattern executor implementation but testing will be limited until actual patterns are bundled.

### Model Selection Guidelines
- **haiku**: Fast, cost-effective for simple extraction patterns (recommended default)
- **sonnet**: Higher quality for complex analysis patterns
- **opus**: Maximum quality for critical analysis (use sparingly due to cost)

### Future Enhancements (Out of Scope)
- Pattern versioning and updates
- Pattern result caching (beyond prompt caching)
- Custom pattern creation API
- Pattern execution streaming (real-time output)
- Rate limiting and quota management
- Pattern execution metrics/telemetry

### Library Dependencies
May need to add to project dependencies (via `uv add`):
- `pytest-asyncio` - For async unit testing
- `mypy` - For type checking (if not already present)
- `ruff` - For code formatting/linting (if not already present)

These should be added as dev dependencies if not already in the project.

### Pattern Directory Structure Assumption
Based on the requirements, we assume patterns are organized as:
```
.jerry/patterns/
├── analysis/
│   ├── extract_wisdom/
│   │   └── system.md
│   ├── extract_insights/
│   │   └── system.md
├── rating/
│   ├── rate_content/
│   │   └── system.md
└── manifest.json (optional)
```

If the actual structure differs, the implementation will need adjustment.
