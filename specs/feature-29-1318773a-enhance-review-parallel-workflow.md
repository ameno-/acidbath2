# Feature: Enhance Review Workflow with Parallel Processing and Automated PR/MR Review

## Metadata
adw_id: `1318773a`
prompt: `After writing lots of code, merging PRs and ensuring they're kept up to date is a chore. We must enhance the /review workflow with the capability to start multiple review processes in parallel. We must enhance the /review workflow with the capability to review all open branches in PRs and MRs and attach a review. We must enhance the /review workflow with the capability to upload a simple screenshot for non-ui types of changes. screenshot the diff, or draw an abstract interpretive picture of the changes and upload that to a bucket. We must have some evidence of a successful run. We also must improve the review workflow to always pull and merge latest changes from main.`

## Feature Description
This feature transforms the review workflow from a single-branch serial process into a parallel, multi-branch orchestrator that can review all open PRs/MRs simultaneously. It adds automated screenshot generation for non-UI changes (diff visualizations or abstract representations), ensures all branches are synced with the latest main branch changes before review, and posts comprehensive review results to each PR/MR. The enhancement enables teams to scale code review operations across multiple feature branches efficiently while maintaining visibility through visual evidence and detailed review summaries.

## User Story
As a developer managing multiple feature branches
I want to review all open PRs/MRs in parallel with automated screenshot evidence
So that I can quickly identify which branches are ready to merge, which need fixes, and ensure all branches are current with main without manually reviewing each one sequentially

## Problem Statement
The current review workflow (`adw_review_iso.py`) operates on a single branch at a time and requires manual invocation for each branch. As teams scale and work on multiple features simultaneously, this creates several pain points:

1. **Serial Processing Bottleneck**: Reviewing 5 open PRs requires 5 sequential review operations, wasting time when reviews could run in parallel
2. **Stale Branch Risk**: Branches may diverge from main significantly before review, causing merge conflicts and integration issues
3. **Limited Visual Evidence**: Reviews of non-UI changes (backend APIs, data models, infrastructure) lack visual artifacts, making it harder to communicate what changed
4. **Manual Discovery**: Developers must manually identify which PRs/MRs need review and invoke the workflow for each one
5. **No Centralized Status**: No single view of review status across all open branches

## Solution Statement
We will create a new parallel review orchestrator (`adw_review_all_iso.py`) that:
- Discovers all open PRs/MRs across both GitHub and GitLab platforms
- Syncs each branch with latest main before review to catch integration issues early
- Launches multiple review processes in parallel (configurable concurrency limit)
- Generates visual evidence for all changes, including non-UI changes via diff screenshots or abstract visual representations
- Posts comprehensive review results with screenshots to each PR/MR
- Produces a consolidated report showing review status across all branches

The solution leverages existing infrastructure (worktree isolation, R2 uploads, code review providers) while adding orchestration, main branch syncing, and enhanced screenshot generation capabilities.

## Relevant Files

### Existing Files to Modify
- `adws/adw_review_iso.py:1-552` - Current single-branch review workflow. We'll extract reusable functions and enhance screenshot logic to handle non-UI changes
- `adws/adw_modules/code_review_providers.py:1-828` - Add methods to list all open PRs/MRs for both GitHub and GitLab providers
- `adws/adw_modules/git_ops.py:1-150` - Add functions for syncing branches with main (fetch + merge/rebase)
- `adws/adw_modules/r2_uploader.py:1-127` - Already supports screenshot uploads, no changes needed
- `.claude/commands/review.md:1-87` - Enhance review template to support diff visualization screenshots for non-UI changes

### New Files
- `adws/adw_review_all_iso.py` - New parallel review orchestrator that discovers and reviews all open PRs/MRs
- `adws/adw_modules/diff_visualizer.py` - Generate visual representations of code diffs for non-UI changes
- `.claude/commands/sync_branch.md` - Template for syncing a branch with latest main changes
- `specs/feature-29-1318773a-enhance-review-parallel-workflow.md` - This specification document

## Implementation Plan

### Phase 1: Foundation - Branch Discovery and Syncing
Establish the infrastructure for discovering open PRs/MRs and syncing branches with main before review.

**Why First**: Parallel execution depends on having a reliable list of branches to review, and branches must be current with main to provide accurate review results.

**Deliverables**:
- Enhanced code review providers with list_open_reviews() method
- Git operations for branch syncing (fetch + merge/rebase from main)
- Sync branch command template
- Unit tests for discovery and syncing

### Phase 2: Core Implementation - Parallel Review Orchestrator
Build the main orchestrator that coordinates parallel review execution across multiple branches.

**Why Second**: Depends on Phase 1's discovery/syncing capabilities. This is the core feature that enables parallel processing.

**Deliverables**:
- `adw_review_all_iso.py` orchestrator with parallel execution
- Configuration for concurrency limits (default: 3 concurrent reviews)
- State management for tracking review progress across branches
- Error handling and retry logic for failed reviews

### Phase 3: Integration - Enhanced Screenshot Generation
Add visual evidence generation for all types of changes, including non-UI changes.

**Why Third**: Builds on existing review infrastructure but adds new capability. Can be developed in parallel with Phase 2 if needed.

**Deliverables**:
- Diff visualizer module for generating code diff images
- Abstract visualization option for complex changes
- Enhanced review template with diff screenshot capability
- Integration with existing R2 upload infrastructure

## Step by Step Tasks

### 1. Enhance Code Review Providers with List Capability
- Read `/Users/ameno/dev/tac/tac-8/trees/1318773a/adws/adw_modules/code_review_providers.py` to understand current provider structure
- Add `list_open_reviews()` method to `CodeReviewProvider` protocol
- Implement `list_open_reviews()` in `GitHubCodeReviewProvider` using `gh pr list` command
- Implement `list_open_reviews()` in `GitLabCodeReviewProvider` using `glab mr list` command
- Return list of `CodeReview` objects with branch names, titles, URLs, and statuses
- Add unit tests for the new list functionality

### 2. Add Branch Syncing Operations to Git Ops
- Read `/Users/ameno/dev/tac/tac-8/trees/1318773a/adws/adw_modules/git_ops.py` to understand current git operations
- Add `fetch_latest_main(cwd)` function to fetch latest main from origin
- Add `sync_branch_with_main(branch_name, strategy, cwd)` function supporting merge and rebase strategies
- Add `check_merge_conflicts(cwd)` function to detect conflicts after sync
- Add `get_commits_behind_main(branch_name, cwd)` to show how far behind a branch is
- Handle edge cases: no remote, already synced, conflict resolution needed
- Add comprehensive error handling and logging

### 3. Create Sync Branch Command Template
- Create `/Users/ameno/dev/tac/tac-8/trees/1318773a/.claude/commands/sync_branch.md`
- Template should accept branch name and sync strategy (merge/rebase) as arguments
- Include instructions for fetching latest main, syncing branch, and handling conflicts
- Add conflict detection and reporting in structured format
- Follow existing command template patterns from `/feature` and `/review`
- Include validation commands to verify sync succeeded

### 4. Build Diff Visualizer Module
- Create `/Users/ameno/dev/tac/tac-8/trees/1318773a/adws/adw_modules/diff_visualizer.py`
- Implement `generate_diff_screenshot(branch_name, output_path, cwd)` function
- Use `git diff origin/main..HEAD` to get changes
- Generate side-by-side diff visualization using pygments for syntax highlighting
- Create image using PIL/Pillow with proper formatting (line numbers, colors, word wrap)
- Implement `generate_abstract_visualization(branch_name, output_path, cwd)` as alternative
- Abstract visualization shows: files changed, lines added/removed, change categories
- Support both PNG and JPEG output formats
- Add dependency: `uv add pillow pygments` for image generation

### 5. Enhance Review Template for Diff Screenshots
- Read `/Users/ameno/dev/tac/tac-8/trees/1318773a/.claude/commands/review.md` to understand current review flow
- Add section for detecting if changes are UI-based or non-UI (backend, config, data models)
- For non-UI changes, add instruction to generate diff screenshot using diff_visualizer
- Include option to generate abstract visualization if diff is too large (>500 lines)
- Update screenshot capture instructions to include diff screenshots in the `screenshots` array
- Ensure diff screenshots are copied to `review_image_dir` with clear naming: `00_diff_overview.png`
- Update Output Structure documentation to clarify diff screenshots are included

### 6. Extract Reusable Functions from Current Review Workflow
- Read `/Users/ameno/dev/tac/tac-8/trees/1318773a/adws/adw_review_iso.py` completely
- Extract `run_review()` as a standalone function that can be called by orchestrator
- Extract `upload_review_screenshots()` as a utility function
- Extract `build_review_summary()` for formatting review results
- Extract `resolve_blocker_issues()` for handling review fixes
- Create new file `/Users/ameno/dev/tac/tac-8/trees/1318773a/adws/adw_modules/review_ops.py` with extracted functions
- Update `adw_review_iso.py` to import from `review_ops.py`
- Add comprehensive docstrings and type hints to all extracted functions

### 7. Create Parallel Review Orchestrator Script
- Create `/Users/ameno/dev/tac/tac-8/trees/1318773a/adws/adw_review_all_iso.py`
- Add script dependencies: `python-dotenv`, `pydantic`, `boto3>=1.26.0`, `click` for CLI
- Implement `discover_open_reviews()` function using code review providers
- Implement `sync_branch_if_needed(code_review, logger)` to sync each branch with main
- Implement `review_single_branch(code_review, adw_id, logger)` wrapper
- Implement `run_parallel_reviews(reviews, max_concurrent, adw_id, logger)` using asyncio or concurrent.futures
- Add CLI arguments: `--max-concurrent` (default: 3), `--platform` (github/gitlab/all), `--skip-sync`, `--skip-resolution`
- Add state tracking for overall orchestrator progress

### 8. Implement Parallel Execution Logic
- Use `concurrent.futures.ThreadPoolExecutor` for parallel review execution
- Create separate worktrees for each branch being reviewed (leverage existing worktree_ops)
- Assign unique ports for each worktree to avoid conflicts
- Implement progress tracking and logging for all parallel reviews
- Add timeout handling (default: 30 minutes per review)
- Implement graceful shutdown on interrupt (SIGINT) - wait for current reviews to finish
- Collect results from all reviews and aggregate into consolidated report

### 9. Add Consolidated Reporting
- Create consolidated review report showing status of all branches
- Report format: JSON with summary statistics (total, passed, failed, blocker issues)
- Include per-branch details: branch name, PR/MR URL, review status, issue count, screenshot URLs
- Save consolidated report to `agents/{adw_id}/consolidated_review_report.json`
- Generate markdown summary for posting to a "Review Dashboard" issue or PR
- Add option to post consolidated report to a designated GitHub/GitLab issue

### 10. Add Error Handling and Recovery
- Implement per-branch error isolation - one failing review doesn't stop others
- Add retry logic for transient failures (network issues, rate limits)
- Track failed reviews and generate summary of failures
- Add `--retry-failed` flag to re-run only previously failed reviews
- Store failed review state for retry operations
- Add comprehensive logging at debug, info, warning, and error levels

### 11. Update Documentation and Examples
- Update main `README.md` to document the new `adw_review_all_iso.py` workflow
- Add usage examples showing parallel review with different flags
- Document the new diff visualization capability
- Add section on branch syncing strategy (merge vs rebase)
- Update ADW-LIST table with new workflow entry
- Create example output showing consolidated review report format

### 12. Add Integration Tests
- Create test suite for parallel review orchestrator
- Mock GitHub/GitLab APIs for discovering open PRs/MRs
- Test parallel execution with multiple mock reviews
- Test branch syncing with mock git operations
- Test error handling when reviews fail
- Test consolidated report generation
- Verify screenshot generation for UI and non-UI changes

### 13. Create Validation Script
- Create `/Users/ameno/dev/tac/tac-8/trees/1318773a/adws/adw_tests/test_parallel_review.py`
- Test discovery of open PRs/MRs on test repository
- Test branch syncing on test branches
- Test diff visualization generation
- Test parallel execution with 2-3 test branches
- Test consolidated report generation
- Add to CI/CD pipeline for automated testing

## Testing Strategy

### Unit Tests
- **Code Review Provider Tests**: Test `list_open_reviews()` for GitHub and GitLab with mock API responses
- **Git Ops Tests**: Test branch syncing, conflict detection, commits-behind-main calculation
- **Diff Visualizer Tests**: Test diff screenshot generation with sample diffs of varying sizes
- **Review Ops Tests**: Test extracted review functions work independently
- **Parallel Execution Tests**: Test ThreadPoolExecutor coordination with mock review tasks

### Integration Tests
- **End-to-End Parallel Review**: Create 3 test branches, run parallel review, verify all complete
- **Branch Syncing Integration**: Test syncing test branch with main, verify changes applied
- **Screenshot Upload Integration**: Test diff screenshot generation and R2 upload
- **Cross-Platform Testing**: Test with both GitHub and GitLab repositories
- **Error Recovery**: Test retry logic when one review fails

### Edge Cases
- **No Open PRs/MRs**: Orchestrator should exit gracefully with informative message
- **All Branches Current**: Syncing should detect and skip already-synced branches
- **Merge Conflicts**: Branch sync should detect conflicts and report them without failing entire orchestration
- **Large Diffs**: Diff visualizer should generate abstract view for diffs >500 lines
- **Port Exhaustion**: Handle case where no available ports for worktrees (graceful degradation)
- **Concurrent Worktree Limit**: Handle case where too many branches exist for parallel processing
- **API Rate Limits**: Handle GitHub/GitLab API rate limits gracefully with backoff
- **Partial Failures**: Verify consolidated report accurately reflects mix of successful and failed reviews

## Acceptance Criteria

### Core Functionality
- [ ] `adw_review_all_iso.py` successfully discovers all open PRs/MRs on both GitHub and GitLab
- [ ] Orchestrator syncs all discovered branches with latest main before review
- [ ] Reviews execute in parallel with configurable concurrency (default 3)
- [ ] Each review produces screenshots with visual evidence (UI or diff visualizations)
- [ ] All screenshots upload to R2 and URLs are included in PR/MR comments
- [ ] Consolidated report generated showing status of all reviews
- [ ] Individual PR/MR comments posted with review results and screenshot links

### Branch Syncing
- [ ] Branches successfully sync with main using merge strategy
- [ ] Branches successfully sync with main using rebase strategy (when specified)
- [ ] Merge conflicts detected and reported without failing entire workflow
- [ ] Branches already current with main are skipped (no unnecessary syncing)
- [ ] Sync operation logs clear before/after commit information

### Screenshot Generation
- [ ] UI changes produce interactive screenshots via Playwright (existing capability)
- [ ] Non-UI changes produce diff visualization screenshots showing code changes
- [ ] Large diffs (>500 lines) produce abstract visualizations instead of full diff
- [ ] All screenshots have descriptive filenames and are numbered sequentially
- [ ] Diff screenshots have syntax highlighting and proper formatting

### Error Handling
- [ ] Single review failure doesn't stop other parallel reviews
- [ ] Failed reviews included in consolidated report with error details
- [ ] Retry logic successfully re-runs failed reviews with `--retry-failed` flag
- [ ] API rate limits handled gracefully with exponential backoff
- [ ] Worktree creation failures handled without crashing orchestrator

### Skip If Already Reviewed
- [x] Review skips execution if branch HEAD matches `last_reviewed_commit_sha` in state
- [x] Skip message posted to issue/PR when skipping duplicate review
- [x] `last_reviewed_commit_sha` saved to state after successful review completion
- [x] New commits trigger full review (SHA mismatch)
- [x] Missing `last_reviewed_commit_sha` treated as "not reviewed" (runs normally)

### Performance
- [ ] 3 parallel reviews complete in approximately the time of 1 sequential review (allowing for overhead)
- [ ] Memory usage stays reasonable with multiple worktrees (< 2GB per worktree)
- [ ] Diff visualization generation completes in < 30 seconds for typical diffs
- [ ] Screenshot upload to R2 completes in < 10 seconds per image

### Documentation
- [ ] README includes section on parallel review workflow with usage examples
- [ ] All CLI flags documented with descriptions and defaults
- [ ] Branch syncing strategies documented (merge vs rebase, when to use each)
- [ ] Troubleshooting guide for common issues (port conflicts, rate limits, conflicts)

## Validation Commands

Execute these commands to validate the feature is complete:

```bash
# Validate Python syntax for all new and modified files
uv run python -m py_compile adws/adw_review_all_iso.py
uv run python -m py_compile adws/adw_modules/diff_visualizer.py
uv run python -m py_compile adws/adw_modules/review_ops.py

# Run unit tests
uv run pytest adws/adw_tests/test_parallel_review.py -v

# Test branch syncing on a test branch
cd /Users/ameno/dev/tac/tac-8/trees/1318773a
git checkout -b test-sync-branch
echo "test" > test_sync.txt
git add test_sync.txt
git commit -m "test: add sync test file"
git checkout main
git pull origin main
git checkout test-sync-branch
# Now test syncing
uv run python adws/adw_review_all_iso.py --max-concurrent 1 --dry-run

# Test diff visualization on a test branch with changes
git checkout -b test-diff-viz
echo "# Test changes" >> README.md
git add README.md
git commit -m "test: diff visualization"
uv run python -c "from adws.adw_modules.diff_visualizer import generate_diff_screenshot; generate_diff_screenshot('test-diff-viz', '/tmp/test_diff.png', '.')"
ls -lh /tmp/test_diff.png  # Verify image created

# Test parallel review orchestrator discovery (dry-run)
uv run python adws/adw_review_all_iso.py --platform github --dry-run
uv run python adws/adw_review_all_iso.py --platform gitlab --dry-run

# Test actual parallel review (requires open PRs/MRs)
uv run python adws/adw_review_all_iso.py --max-concurrent 2 --skip-resolution

# Verify consolidated report generated
cat agents/*/consolidated_review_report.json | jq '.'

# Test retry logic
uv run python adws/adw_review_all_iso.py --retry-failed

# Cleanup test branches
git branch -D test-sync-branch test-diff-viz
```

## Notes

### Design Decisions

**Parallel Execution Approach**: Using `concurrent.futures.ThreadPoolExecutor` instead of `asyncio` because most operations (git commands, subprocess calls) are synchronous. ThreadPoolExecutor provides simpler error handling and easier debugging.

**Diff Visualization Strategy**: Using Pygments for syntax highlighting and Pillow for image generation provides a pure-Python solution without external dependencies like browser automation. For diffs >500 lines, abstract visualization prevents image size issues and improves readability.

**Branch Syncing Strategy**: Default to merge strategy (safer, preserves history) but support rebase via flag for teams that prefer linear history. Always fetch latest main before syncing to ensure accuracy.

**Concurrency Limit**: Default to 3 concurrent reviews as a balance between parallelism and resource usage. Each review requires a worktree (disk space) and port allocation (network resources). Higher concurrency (5-7) possible on machines with more resources.

**Screenshot Requirements**: All reviews must produce screenshots to provide visual evidence. For non-UI changes, diff screenshots serve as "proof of work" and help communicate what changed to reviewers.

**Skip If Already Reviewed**: The review workflow stores `last_reviewed_commit_sha` in ADW state after successful completion. On subsequent runs, it compares the current HEAD commit against this stored SHA and skips if they match. This prevents duplicate comments, wasted compute, and redundant screenshot uploads when re-running reviews on unchanged branches. The check is fail-open: if the SHA is missing or git commands fail, the review runs normally.

### Dependencies to Add

```bash
# Add image generation dependencies
uv add pillow pygments

# Existing dependencies already in place:
# - python-dotenv (for environment variables)
# - pydantic (for data validation)
# - boto3 (for R2 uploads)
# - click (for CLI)
```

### Future Enhancements

**Webhook Integration**: Add webhook endpoint to automatically trigger parallel review when new PRs/MRs are opened or when main branch updates.

**Review Approval Automation**: Automatically approve PRs/MRs that pass review with zero blocker issues (with appropriate safeguards).

**Slack/Discord Notifications**: Post consolidated review report to team chat channels for visibility.

**Review Metrics Dashboard**: Track review cycle time, common issues, and approval rates over time.

**Smart Concurrency**: Dynamically adjust concurrency based on available system resources (CPU, memory, ports).

**Incremental Reviews**: ✅ IMPLEMENTED - Reviews now skip if branch HEAD matches `last_reviewed_commit_sha` in state, avoiding duplicate reviews on unchanged branches.

### Configuration Options

The orchestrator supports the following environment variables:

- `REVIEW_MAX_CONCURRENT`: Override default concurrency (default: 3)
- `REVIEW_SYNC_STRATEGY`: Default sync strategy: "merge" or "rebase" (default: merge)
- `REVIEW_SKIP_SYNC`: Skip branch syncing entirely (default: false)
- `REVIEW_SKIP_RESOLUTION`: Skip blocker issue resolution (default: false)
- `REVIEW_TIMEOUT_MINUTES`: Timeout per review in minutes (default: 30)
- `REVIEW_DASHBOARD_ISSUE`: GitHub/GitLab issue number to post consolidated report

### Platform Support

This feature fully supports both GitHub and GitLab:

- **GitHub**: Uses `gh` CLI for PR discovery, branch operations
- **GitLab**: Uses `glab` CLI for MR discovery, branch operations
- **Cross-Platform**: Can discover and review PRs from GitHub and MRs from GitLab in single run with `--platform all`

The unified `CodeReviewProvider` abstraction ensures consistent behavior across platforms while respecting platform-specific conventions (PR vs MR terminology, approval workflows, etc.).
