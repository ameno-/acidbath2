# Feature: Comprehensive Unit Test Coverage for Jerry

## Metadata
adw_id: `1cc4d84c`
prompt: `{"number": "50", "title": "Unit tests", "body": "Add meaningful test coverage to every ADW, script, or executable in Jerry. Focus on testing key functionality and consider refactors and decomposition to improve consistency of key adw workflows and modules."}`

## Feature Description
This feature adds comprehensive unit test coverage to the Jerry framework, focusing on all AI Developer Workflows (ADWs), core modules, and executable scripts. The implementation will establish a robust testing infrastructure that ensures reliability, catches regressions early, and provides documentation through test cases. Testing will cover critical paths, edge cases, error handling, and integration points while considering refactors to improve testability and consistency.

## User Story
As a Jerry developer
I want comprehensive unit test coverage across all ADWs and modules
So that I can confidently modify code, catch bugs early, maintain consistent behavior, and ensure production reliability

## Problem Statement
Currently, Jerry has minimal test coverage with only three test files in `adws/adw_modules/`:
- `test_content_extractors.py` - Integration tests for content extraction
- `test_issue_providers_gitlab.py` - GitLab provider tests
- `test_pattern_executor.py` - Pattern executor tests

This lack of comprehensive testing creates several issues:
1. **Regression Risk**: Changes to core modules can break workflows without detection
2. **Refactoring Difficulty**: No safety net when restructuring code for better consistency
3. **Documentation Gap**: Tests serve as executable documentation of expected behavior
4. **Integration Uncertainty**: No validation that ADW compositions work correctly
5. **Error Handling Coverage**: Unknown edge cases and error paths
6. **Deployment Confidence**: No automated validation before production use

The codebase has:
- 21 ADW workflow scripts in `adws/`
- 29 module files in `adws/adw_modules/`
- Multiple triggers in `adws/adw_triggers/`
- Only 3 existing test files with limited coverage

## Solution Statement
Implement a comprehensive, pytest-based testing framework that covers:

1. **Core Module Testing**: Unit tests for all 29 modules in `adw_modules/` covering:
   - Agent execution (agent.py, agent_sdk.py)
   - Workflow operations (workflow_ops.py, worktree_ops.py)
   - Platform integrations (github.py, gitlab.py, issue_providers.py)
   - Content handling (content_extractors.py, pdf_ops.py, youtube_ops.py)
   - State management and utilities

2. **ADW Workflow Testing**: Functional tests for all 21 ADW scripts covering:
   - Input validation and argument parsing
   - Error handling and retry logic
   - Output structure and file generation
   - Integration between composed workflows

3. **Testing Infrastructure**:
   - Pytest configuration with fixtures and utilities
   - Mocking for external services (GitHub, GitLab, Claude API)
   - Test data factories and builders
   - CI/CD integration support

4. **Refactoring for Testability**:
   - Extract reusable validation logic
   - Standardize error handling patterns
   - Improve module boundaries and interfaces
   - Consistent output structures

This approach provides comprehensive coverage while improving code quality and consistency.

## Relevant Files

### Existing Test Files
- `adws/adw_modules/test_content_extractors.py` - Integration tests for content extraction (good example)
- `adws/adw_modules/test_issue_providers_gitlab.py` - GitLab provider tests
- `adws/adw_modules/test_pattern_executor.py` - Pattern executor tests
- `pyproject.toml` - Project dependencies and pytest configuration

### Core Modules to Test (adws/adw_modules/)
- `agent.py` - Core agent execution with subprocess management and retry logic
- `agent_sdk.py` - SDK-based agent execution
- `workflow_ops.py` - Shared workflow operations
- `worktree_ops.py` - Worktree isolation and port management
- `git_ops.py` - Git operations
- `state.py` - Workflow state management
- `validation.py` - Validation utilities
- `utils.py` - Common utilities
- `data_types.py` - Type definitions

### Platform Integration Modules to Test
- `issue_providers.py` - Multi-source issue tracking
- `github.py` - GitHub operations
- `gitlab.py` - GitLab operations
- `code_review_providers.py` - Code review abstractions
- `notification_providers.py` - Notification systems

### Content Processing Modules to Test
- `content_extractors.py` - Content extraction pipeline
- `pdf_ops.py` - PDF processing
- `youtube_ops.py` - YouTube operations
- `web_ops.py` - Web scraping
- `text_ops.py` - Text processing
- `pattern_executor.py` - Pattern execution
- `plan_executor.py` - Plan execution
- `diff_visualizer.py` - Diff visualization
- `report_generator.py` - Report generation

### ADW Scripts to Test (adws/)
- `adw_prompt.py` - Direct prompt execution
- `adw_sdk_prompt.py` - SDK-based prompt execution
- `adw_slash_command.py` - Slash command execution
- `adw_plan_iso.py` - Planning in isolation
- `adw_build_iso.py` - Building in isolation
- `adw_review_iso.py` - Review in isolation
- `adw_review_all_iso.py` - Parallel review orchestration
- `adw_ship_iso.py` - Shipping workflow
- `adw_plan_build_iso.py` - Composed planning + building
- `adw_patch_iso.py` - Patch workflow
- `adw_chore_implement.py` - Chore implementation
- `adw_import_workflow.py` - Workflow import
- `adw_fix_validation.py` - Self-healing validation

### Trigger Modules to Test
- `adws/adw_triggers/trigger_base.py` - Base trigger interface
- `adws/adw_triggers/trigger_github.py` - GitHub webhook trigger
- `adws/adw_triggers/trigger_manual.py` - Manual trigger

### New Files

#### Test Infrastructure
- `tests/__init__.py` - Test package initialization
- `tests/conftest.py` - Pytest configuration and shared fixtures
- `tests/fixtures/` - Test data and mock objects
- `tests/utils/test_helpers.py` - Test utilities and builders

#### Module Tests
- `tests/modules/test_agent.py` - Agent execution tests
- `tests/modules/test_agent_sdk.py` - SDK agent tests
- `tests/modules/test_workflow_ops.py` - Workflow operations tests
- `tests/modules/test_worktree_ops.py` - Worktree operations tests
- `tests/modules/test_git_ops.py` - Git operations tests
- `tests/modules/test_state.py` - State management tests
- `tests/modules/test_validation.py` - Validation tests
- `tests/modules/test_utils.py` - Utilities tests
- `tests/modules/test_data_types.py` - Data types tests
- `tests/modules/test_issue_providers.py` - Issue provider tests
- `tests/modules/test_github.py` - GitHub module tests
- `tests/modules/test_gitlab.py` - GitLab module tests
- `tests/modules/test_code_review_providers.py` - Code review tests
- `tests/modules/test_content_extractors.py` - Content extraction tests
- `tests/modules/test_pdf_ops.py` - PDF operations tests
- `tests/modules/test_youtube_ops.py` - YouTube operations tests
- `tests/modules/test_web_ops.py` - Web operations tests
- `tests/modules/test_pattern_executor.py` - Pattern executor tests
- `tests/modules/test_plan_executor.py` - Plan executor tests
- `tests/modules/test_diff_visualizer.py` - Diff visualizer tests
- `tests/modules/test_report_generator.py` - Report generator tests

#### ADW Workflow Tests
- `tests/adws/test_adw_prompt.py` - Prompt ADW tests
- `tests/adws/test_adw_sdk_prompt.py` - SDK prompt ADW tests
- `tests/adws/test_adw_slash_command.py` - Slash command ADW tests
- `tests/adws/test_adw_plan_iso.py` - Plan isolation ADW tests
- `tests/adws/test_adw_build_iso.py` - Build isolation ADW tests
- `tests/adws/test_adw_review_iso.py` - Review isolation ADW tests
- `tests/adws/test_adw_review_all_iso.py` - Parallel review tests
- `tests/adws/test_adw_ship_iso.py` - Ship workflow tests
- `tests/adws/test_adw_plan_build_iso.py` - Composed workflow tests
- `tests/adws/test_adw_patch_iso.py` - Patch workflow tests

#### Trigger Tests
- `tests/triggers/test_trigger_base.py` - Base trigger tests
- `tests/triggers/test_trigger_github.py` - GitHub trigger tests
- `tests/triggers/test_trigger_manual.py` - Manual trigger tests

#### Integration Tests
- `tests/integration/test_plan_build_flow.py` - End-to-end plan→build flow
- `tests/integration/test_worktree_isolation.py` - Worktree isolation validation
- `tests/integration/test_multi_source_issues.py` - Multi-source issue handling
- `tests/integration/test_retry_logic.py` - Retry logic integration

## Implementation Plan

### Phase 1: Foundation
Establish the testing infrastructure and patterns before implementing comprehensive tests. This includes:
- Setting up pytest configuration and shared fixtures
- Creating test utilities and mock builders
- Establishing testing patterns and conventions
- Implementing baseline tests for core modules

### Phase 2: Core Implementation
Systematically add tests for all modules and ADWs following established patterns:
- Module-by-module test coverage
- ADW workflow functional tests
- Trigger and integration tests
- Refactoring modules as needed for testability

### Phase 3: Integration
Ensure tests work together and validate end-to-end flows:
- Integration test suites
- CI/CD pipeline integration
- Test documentation and maintenance guides
- Coverage reporting and quality gates

## Step by Step Tasks

### Group A: Testing Infrastructure Setup [parallel: false, model: sonnet]
Foundation work that all other tests depend on. Must be completed sequentially.

#### Step A.1: Configure pytest and test structure
- Create `tests/__init__.py` package file
- Create `tests/conftest.py` with pytest configuration
- Add pytest fixtures for common test scenarios (temp directories, mock agents, etc.)
- Configure pytest.ini options in `pyproject.toml` (add markers, coverage, etc.)
- Create test directory structure: `tests/modules/`, `tests/adws/`, `tests/triggers/`, `tests/integration/`

#### Step A.2: Create test utilities and fixtures
- Create `tests/utils/test_helpers.py` with builder functions for test data
- Create `tests/fixtures/` directory with sample data files
- Add mock builders for AgentPromptRequest, AgentPromptResponse, Issue objects
- Create temporary file/directory fixtures
- Add assertion helpers for common validations

#### Step A.3: Add testing dependencies
- Review and update `pyproject.toml` dependencies
- Add `pytest-mock` for mocking support
- Add `pytest-cov` for coverage reporting
- Add `freezegun` for time-based testing
- Add `responses` or `requests-mock` for HTTP mocking
- Verify all dependencies with `uv lock`

#### Step A.4: Create baseline module test template
- Create `tests/modules/test_utils.py` as reference implementation
- Test all functions in `adws/adw_modules/utils.py`
- Include examples of: unit tests, mocking, fixtures, parametrized tests
- Document testing patterns and conventions
- Validate test can run: `uv run pytest tests/modules/test_utils.py -v`

### Group B: Core Module Tests [parallel: true, depends: A, model: auto]
Independent test files that can be developed in parallel after infrastructure is ready.

#### Step B.1: Test agent.py module
- Create `tests/modules/test_agent.py`
- Test `generate_short_id()` function
- Test `truncate_output()` with various inputs (text, JSONL, edge cases)
- Mock subprocess calls to test `prompt_claude_code()` function
- Test `prompt_claude_code_with_retry()` retry logic with failures
- Test `execute_template()` with slash commands
- Validate error handling and timeout scenarios

#### Step B.2: Test agent_sdk.py module
- Create `tests/modules/test_agent_sdk.py`
- Test SDK initialization and configuration
- Mock Claude SDK client and test agent execution
- Test async/await patterns
- Test error handling specific to SDK
- Validate type safety and message objects

#### Step B.3: Test data_types.py module
- Create `tests/modules/test_data_types.py`
- Test Pydantic model validation for all data types
- Test RetryCode enum values
- Test AgentPromptRequest, AgentPromptResponse construction
- Test AgentTemplateRequest validation
- Test ClaudeCodeResultMessage parsing
- Test ADWExtractionResult validation

#### Step B.4: Test validation.py module
- Create `tests/modules/test_validation.py`
- Test all validation functions
- Test input sanitization
- Test error message formatting
- Test validation edge cases (empty, None, invalid types)

#### Step B.5: Test state.py module
- Create `tests/modules/test_state.py`
- Test ADWState initialization
- Test phase tracking (update_phase, complete_phase)
- Test artifact management (add_artifact, get_artifact)
- Test state persistence (save/load from JSON)
- Test concurrent state updates

#### Step B.6: Test workflow_ops.py module
- Create `tests/modules/test_workflow_ops.py`
- Test `format_issue_message()` with various inputs
- Test `extract_adw_info()` with mocked classify_adw agent
- Test workflow command validation
- Test model_set extraction
- Mock agent calls to avoid external dependencies

#### Step B.7: Test git_ops.py module
- Create `tests/modules/test_git_ops.py`
- Use temporary git repositories for testing
- Test git status, branch, commit operations
- Test error handling for git failures
- Mock git commands where appropriate
- Validate git operation outputs

#### Step B.8: Test worktree_ops.py module
- Create `tests/modules/test_worktree_ops.py`
- Test worktree creation in temporary directories
- Test port allocation and management
- Test worktree cleanup
- Test error handling for failed worktree operations
- Validate isolation guarantees

### Group C: Platform Integration Module Tests [parallel: true, depends: A, model: auto]
Tests for platform integration modules that can be developed in parallel.

#### Step C.1: Test issue_providers.py module
- Create `tests/modules/test_issue_providers.py`
- Test IssueProvider interface
- Test provider registration
- Mock GitHub, Linear, Notion API calls
- Test issue fetching and normalization
- Test error handling for API failures
- Validate multi-source issue retrieval

#### Step C.2: Test github.py module
- Create `tests/modules/test_github.py`
- Mock GitHub API responses
- Test repository operations
- Test issue and PR operations
- Test authentication handling
- Test rate limiting and retries

#### Step C.3: Test gitlab.py module
- Create `tests/modules/test_gitlab.py`
- Mock GitLab API responses
- Test project operations
- Test issue and MR operations
- Test authentication handling
- Validate error handling

#### Step C.4: Test code_review_providers.py module
- Create `tests/modules/test_code_review_providers.py`
- Test CodeReviewProvider interface
- Mock PR/MR creation
- Test review comment posting
- Test provider switching
- Validate error handling

### Group D: Content Processing Module Tests [parallel: true, depends: A, model: auto]
Tests for content processing modules that can be developed in parallel.

#### Step D.1: Enhance test_content_extractors.py
- Move existing `adws/adw_modules/test_content_extractors.py` to `tests/modules/test_content_extractors.py`
- Add more edge cases and error scenarios
- Add tests for all ContentType variants
- Test content detection logic
- Add performance tests for large inputs

#### Step D.2: Test pdf_ops.py module
- Create `tests/modules/test_pdf_ops.py`
- Create sample PDF fixture files
- Test PDF text extraction
- Test error handling for corrupted PDFs
- Mock PDF libraries to avoid heavy dependencies
- Validate output formats

#### Step D.3: Test youtube_ops.py module
- Create `tests/modules/test_youtube_ops.py`
- Mock yt-dlp calls
- Test video ID extraction
- Test metadata fetching
- Test transcript extraction
- Test error handling for invalid videos

#### Step D.4: Test pattern_executor.py module
- Migrate `adws/adw_modules/test_pattern_executor.py` to `tests/modules/test_pattern_executor.py`
- Add more pattern execution tests
- Test pattern composition
- Test error handling
- Validate output formats

#### Step D.5: Test web_ops.py module
- Create `tests/modules/test_web_ops.py`
- Mock HTTP requests
- Test URL validation
- Test scraping logic
- Test timeout and retry handling
- Validate output formats

#### Step D.6: Test diff_visualizer.py module
- Create `tests/modules/test_diff_visualizer.py`
- Create sample diff fixtures
- Test syntax highlighting
- Test diff formatting
- Test screenshot generation for UI changes

#### Step D.7: Test report_generator.py module
- Create `tests/modules/test_report_generator.py`
- Test report creation from templates
- Test data aggregation
- Test output formatting (JSON, Markdown)
- Validate report structure

### Group E: ADW Workflow Tests - Core [parallel: true, depends: A, model: auto]
Tests for core ADW workflows that can be developed in parallel.

#### Step E.1: Test adw_prompt.py
- Create `tests/adws/test_adw_prompt.py`
- Test CLI argument parsing
- Mock agent execution
- Test output file generation
- Test working directory handling
- Test retry flag behavior
- Validate error handling

#### Step E.2: Test adw_sdk_prompt.py
- Create `tests/adws/test_adw_sdk_prompt.py`
- Test SDK initialization
- Mock SDK agent calls
- Test async execution
- Test error handling
- Validate output structures

#### Step E.3: Test adw_slash_command.py
- Create `tests/adws/test_adw_slash_command.py`
- Test slash command parsing
- Mock template loading
- Test argument substitution
- Test command execution
- Validate error handling

#### Step E.4: Test adw_import_workflow.py
- Create `tests/adws/test_adw_import_workflow.py`
- Test workflow discovery
- Test import validation
- Test file copying
- Test error handling for missing workflows

### Group F: ADW Workflow Tests - Isolation [parallel: true, depends: A, model: auto]
Tests for isolation-based ADW workflows.

#### Step F.1: Test adw_plan_iso.py
- Create `tests/adws/test_adw_plan_iso.py`
- Mock worktree creation
- Mock agent planning execution
- Test spec file generation
- Test output structure
- Validate cleanup on failure

#### Step F.2: Test adw_build_iso.py
- Create `tests/adws/test_adw_build_iso.py`
- Mock worktree operations
- Mock agent build execution
- Test commit creation
- Test output validation
- Validate cleanup behavior

#### Step F.3: Test adw_review_iso.py
- Create `tests/adws/test_adw_review_iso.py`
- Mock code review process
- Test screenshot generation
- Test blocker detection
- Test review report creation

#### Step F.4: Test adw_ship_iso.py
- Create `tests/adws/test_adw_ship_iso.py`
- Mock git operations
- Test merge logic
- Test PR creation
- Test push to remote
- Validate error handling

#### Step F.5: Test adw_review_all_iso.py
- Create `tests/adws/test_adw_review_all_iso.py`
- Test PR/MR discovery
- Test parallel execution
- Test concurrency limits
- Test report aggregation
- Validate error isolation

### Group G: ADW Workflow Tests - Composite [parallel: true, depends: E, F, model: auto]
Tests for composite workflows that depend on core workflow tests.

#### Step G.1: Test adw_plan_build_iso.py
- Create `tests/adws/test_adw_plan_build_iso.py`
- Mock both planning and building phases
- Test state transitions
- Test output chaining
- Test error propagation
- Validate cleanup on failures

#### Step G.2: Test adw_patch_iso.py
- Create `tests/adws/test_adw_patch_iso.py`
- Test multi-source issue handling
- Mock patch application
- Test worktree isolation
- Validate output structure

#### Step G.3: Test adw_chore_implement.py
- Create `tests/adws/test_adw_chore_implement.py`
- Test chore planning and implementation
- Mock agent execution
- Validate workflow composition

### Group H: Trigger and Integration Tests [parallel: false, depends: B, C, D, E, F, G, model: auto]
Sequential tests that validate integration points.

#### Step H.1: Test trigger modules
- Create `tests/triggers/test_trigger_base.py`
- Create `tests/triggers/test_trigger_github.py`
- Create `tests/triggers/test_trigger_manual.py`
- Mock webhook payloads
- Test event parsing
- Test workflow invocation
- Validate error handling

#### Step H.2: Create integration tests
- Create `tests/integration/test_plan_build_flow.py` - Test full plan→build→ship flow
- Create `tests/integration/test_worktree_isolation.py` - Validate isolation guarantees
- Create `tests/integration/test_multi_source_issues.py` - Test GitHub, Linear, Notion sources
- Create `tests/integration/test_retry_logic.py` - Test retry behavior across workflows

#### Step H.3: Migrate existing tests
- Move `adws/adw_modules/test_issue_providers_gitlab.py` to `tests/modules/test_issue_providers_gitlab.py`
- Update imports and paths
- Integrate with new test infrastructure
- Ensure compatibility with pytest fixtures

### Group I: Refactoring and Consistency [parallel: false, depends: H, model: sonnet]
Refactoring work informed by test coverage to improve consistency.

#### Step I.1: Identify refactoring opportunities
- Review test coverage reports
- Identify duplicated validation logic
- Document inconsistent patterns
- Create refactoring plan

#### Step I.2: Extract common validation logic
- Create `adws/adw_modules/validators.py` with shared validation functions
- Refactor ADWs to use common validators
- Update tests to validate new validators
- Ensure backward compatibility

#### Step I.3: Standardize error handling
- Create consistent error classes in `adws/adw_modules/errors.py`
- Update modules to use standard exceptions
- Add tests for error handling consistency
- Update documentation

#### Step I.4: Improve module boundaries
- Identify and fix circular dependencies
- Extract interfaces where appropriate
- Update tests to validate clean boundaries
- Document module responsibilities

### Group J: Documentation and CI/CD [parallel: false, depends: I, model: sonnet]
Final documentation and automation setup.

#### Step J.1: Document testing approach
- Create `docs/TESTING.md` with testing guide
- Document test structure and conventions
- Add examples for writing new tests
- Document mocking strategies

#### Step J.2: Setup coverage reporting
- Configure pytest-cov in `pyproject.toml`
- Add coverage thresholds (target: 80%+ for modules, 60%+ for ADWs)
- Create coverage report generation script
- Document coverage requirements

#### Step J.3: Create test runner CLI utility
Create `adws/run_tests.py` - a CLI utility for running tests with:

**CLI Interface:**
```bash
uv run adws/run_tests.py                    # Run all tests
uv run adws/run_tests.py -m agent -m git_ops # Run specific modules
uv run adws/run_tests.py --coverage --timing # With all features
uv run adws/run_tests.py list               # List available modules
uv run adws/run_tests.py stats              # Show stats only
```

**Options:**
- `--module, -m` - Run specific module(s), repeatable
- `--coverage` - Enable coverage reporting with module percentages
- `--timing` - Show slowest tests and timing breakdown
- `--verbose, -v` - Verbose output
- `--fail-fast, -x` - Stop on first failure
- `--parallel, -n` - Parallel workers (default: auto)

**Output Format (Plain Text for CI/PR reviews):**
```
================================================================================
TEST RUN: 2024-12-17 15:30:45
================================================================================

[  1/12] agent ........................... 37 tests   PASS    2.3s
[  2/12] content_extractors .............. 40 tests   PASS    1.8s
...

================================================================================
SUMMARY
================================================================================

Total Tests:    496
Passed:         496
Failed:         0
Duration:       28.5s

Status: ALL TESTS PASSED
```

**Implementation:**
- Use Click for CLI argument parsing
- Use Rich for progress display and tables
- Integrate pytest programmatically with custom result collector plugin
- Auto-discover test modules from `tests/modules/`
- Plain text formatters for coverage, timing, and failure details

#### Step J.4: Add CI/CD integration
- Create `.github/workflows/tests.yml` for GitHub Actions
- Configure test runs on PR and push
- Add coverage reporting to PRs
- Document CI/CD requirements

## Testing Strategy

### Unit Tests
Unit tests will focus on individual functions and classes in isolation:

- **Agent Module Tests**: Mock subprocess calls, test retry logic, validate output parsing
- **Workflow Operations Tests**: Test state transitions, artifact management, message formatting
- **Platform Integration Tests**: Mock API calls (GitHub, GitLab, Linear), test error handling
- **Content Processing Tests**: Test extraction, validation, transformation with fixtures
- **Data Type Tests**: Validate Pydantic models, test serialization/deserialization
- **Utility Tests**: Test helper functions, validators, formatters

**Mocking Strategy**:
- External APIs (GitHub, GitLab, Linear, Notion) mocked with `responses` or `requests-mock`
- Subprocess calls mocked with `pytest-mock` or `unittest.mock`
- File system operations use `tmp_path` fixtures
- Claude API calls mocked to avoid API usage during tests

### Integration Tests
Integration tests will validate end-to-end workflows:

- **Plan→Build Flow**: Test full workflow from issue to implementation
- **Worktree Isolation**: Validate parallel execution and isolation guarantees
- **Multi-Source Issues**: Test fetching from GitHub, Linear, Notion in sequence
- **Retry Logic**: Test retry behavior with transient failures

### Functional Tests
Functional tests for ADW scripts:

- **CLI Argument Parsing**: Test all command-line flags and arguments
- **Output Structure**: Validate JSONL, JSON, and summary outputs
- **Error Handling**: Test failure modes and error messages
- **Composition**: Test workflow chaining (plan→build→test→review)

### Edge Cases
Critical edge cases to test:

- **Empty Inputs**: Empty strings, None values, empty files
- **Invalid Data**: Malformed JSON, invalid URLs, corrupted files
- **API Failures**: Network errors, rate limiting, authentication failures
- **File System Issues**: Permission errors, disk full, missing directories
- **Concurrent Access**: Race conditions, file locking, port conflicts
- **Long Running Operations**: Timeouts, cancellation, cleanup
- **Unicode and Special Characters**: Internationalization, emojis, control characters
- **Large Inputs**: Memory usage, performance degradation
- **Retry Exhaustion**: All retries fail, backoff logic
- **Partial Failures**: Some operations succeed, others fail

## Acceptance Criteria

1. **Coverage Thresholds**:
   - ✅ Core modules (adw_modules/*.py) have ≥80% code coverage
   - ✅ ADW scripts (adws/adw_*.py) have ≥60% functional coverage
   - ✅ Critical paths (agent execution, worktree ops, state management) have 100% coverage

2. **Test Organization**:
   - ✅ All tests organized in `tests/` directory with clear structure
   - ✅ Test files mirror source structure (tests/modules/, tests/adws/, tests/triggers/)
   - ✅ Shared fixtures in `conftest.py`
   - ✅ Test utilities in `tests/utils/`

3. **Test Quality**:
   - ✅ Each module has dedicated test file
   - ✅ Tests are independent and can run in any order
   - ✅ External dependencies properly mocked
   - ✅ Test names clearly describe what is being tested
   - ✅ Assertions validate expected behavior, not implementation details

4. **CI/CD Integration**:
   - ✅ Tests run automatically on PR creation/update
   - ✅ Coverage reports generated and visible in PRs
   - ✅ Tests pass consistently without flakiness
   - ✅ Fast execution (full suite < 5 minutes)

5. **Documentation**:
   - ✅ Testing guide in `docs/TESTING.md`
   - ✅ Test conventions documented
   - ✅ Examples for common testing scenarios
   - ✅ README updated with test execution instructions

6. **Refactoring**:
   - ✅ Common validation logic extracted to shared validators
   - ✅ Consistent error handling across modules
   - ✅ Clear module boundaries without circular dependencies
   - ✅ All refactorings validated with passing tests

## Validation Commands

Execute these commands to validate the feature is complete:

1. **Run all tests with coverage**:
   ```bash
   uv run pytest tests/ --cov=adws/adw_modules --cov=adws --cov-report=term-missing --cov-report=html -v
   ```
   Expected: All tests pass, coverage ≥70% overall

2. **Run unit tests only**:
   ```bash
   uv run pytest tests/modules/ -v
   ```
   Expected: All module tests pass

3. **Run integration tests**:
   ```bash
   uv run pytest tests/integration/ -v
   ```
   Expected: All integration tests pass

4. **Run specific test file**:
   ```bash
   uv run pytest tests/modules/test_agent.py -v
   ```
   Expected: All agent tests pass

5. **Check test file structure**:
   ```bash
   find tests -name "test_*.py" | wc -l
   ```
   Expected: ≥30 test files (covering all modules and critical ADWs)

6. **Validate pytest configuration**:
   ```bash
   uv run pytest --collect-only tests/
   ```
   Expected: Tests discovered without errors

7. **Run tests with markers**:
   ```bash
   uv run pytest -m unit tests/
   ```
   Expected: Unit tests run successfully

8. **Verify code compiles**:
   ```bash
   uv run python -m py_compile adws/*.py adws/adw_modules/*.py
   ```
   Expected: No compilation errors

9. **Check coverage thresholds**:
   ```bash
   uv run pytest tests/ --cov=adws/adw_modules --cov-fail-under=70
   ```
   Expected: Coverage threshold met

10. **Validate test isolation**:
    ```bash
    uv run pytest tests/ --random-order
    ```
    Expected: All tests pass in random order (requires pytest-random-order)

## Notes

### Testing Dependencies
Add these dependencies using `uv add`:
- `pytest` - Already present
- `pytest-asyncio` - Already present
- `pytest-mock` - For mocking
- `pytest-cov` - For coverage reporting
- `requests-mock` - For HTTP mocking
- `freezegun` - For time-based testing
- `pytest-random-order` - For test isolation validation
- `pytest-xdist` - For parallel test execution

### Performance Considerations
- Mock external APIs to avoid network calls
- Use temporary directories with cleanup
- Parallelize tests where possible with pytest-xdist
- Target < 5 minute full test suite execution

### Future Enhancements
- Property-based testing with Hypothesis for edge cases
- Performance regression tests
- Mutation testing with mutpy to validate test quality
- Visual regression testing for diff visualizer
- Load testing for parallel review orchestration

### Refactoring Opportunities Identified
Based on initial code review, consider these refactors during testing implementation:
1. **Validation Logic**: Extract common validation patterns (URL validation, file path validation, JSON parsing)
2. **Error Handling**: Standardize exception types and error messages
3. **Output Formatting**: Consistent structure for JSONL, JSON, and summary outputs
4. **Retry Logic**: Extract retry decorator or utility function
5. **Worktree Operations**: Improve interface and error handling
6. **State Management**: Consider adding state validation and migration support

### Test Data Management
- Store sample files in `tests/fixtures/`
- Create builders for common test objects (Issue, AgentPromptRequest, etc.)
- Use factories for generating test data with sensible defaults
- Document fixture usage and maintenance

### Continuous Improvement
- Add tests when bugs are discovered
- Update tests when refactoring
- Monitor coverage trends
- Review and prune obsolete tests
- Keep test documentation current
