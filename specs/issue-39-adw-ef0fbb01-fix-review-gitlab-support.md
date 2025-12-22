# Bug: adw_review_iso.py GitLab Support - Hardcoded GitHub Provider

## Metadata
issue_number: `39`
adw_id: `ef0fbb01`
issue_json: `{"number": "39", "title": "Hardcoded issue provider", "body": "Let's review and fix all workflows to ensure compatibility with various issue providers.\n\n---\ntitle: \"adw_review_iso.py does not support GitLab - hardcoded to GitHub\"\nstatus: open\nlabels:\n  - bug\n  - gitlab\n  - adw\ncreated_at: 2024-12-09T00:00:00\nupdated_at: 2024-12-09T00:00:00\nagent_updates: []\n---\n\n## Summary\n\n`adw_review_iso.py` fails to detect GitLab issues because it directly imports from `github.py` instead of using the platform-agnostic `issue_providers` module.\n\n## Reproduction\n\n```bash\n# In a GitLab-hosted repository\nuv run adws/adw_review_iso.py 2 3f9d30d1 --skip-resolution\n```\n\n**Expected:** Issue #2 is fetched from GitLab and review workflow proceeds.\n\n**Actual:** Fails to detect the GitLab issue because the workflow uses `gh` CLI (GitHub CLI) instead of `glab` CLI.\n\n## Root Cause\n\n`adw_review_iso.py` (lines 40-45) directly imports GitHub-specific functions:\n\n```python\nfrom adws.adw_modules.github import (\n    fetch_issue,\n    make_issue_comment,\n    get_repo_url,\n    extract_repo_path,\n)\n```\n\nThis bypasses the platform detection logic in `issue_providers.py` that other workflows use.\n\n## Comparison with Working Workflows\n\n`adw_plan_iso.py` and `adw_build_iso.py` correctly support both platforms by:\n\n1. Using `resolve_issue()` from `issue_providers.py` to auto-detect platform from git remote\n2. Using `get_provider_for_issue()` for posting comments\n3. Conditionally handling GitHub PRs vs GitLab MRs in the finalization step\n\nExample from `adw_plan_iso.py`:\n```python\nfrom adws.adw_modules.issue_providers import resolve_issue, get_provider_for_issue\nfrom adws.adw_modules.code_review_providers import GitLabCodeReviewProvider\n\n# Auto-detect platform and fetch issue\nissue = resolve_issue(issue_number)\n\n# Use appropriate provider for comments\nprovider = get_provider_for_issue(issue)\nprovider.add_comment(issue, \"Starting planning phase...\")\n\n# Handle GitLab MRs\nif issue.source == IssueSource.GITLAB:\n    gitlab_provider = GitLabCodeReviewProvider(project_path=issue.repo_path, logger=logger)\n    # ... create/update MR\n```\n\n## Proposed Fix\n\n1. Replace `github.py` imports with platform-agnostic modules:\n   ```python\n   from adws.adw_modules.issue_providers import resolve_issue, get_provider_for_issue\n   from adws.adw_modules.git_ops import get_repo_url, extract_repo_path, detect_git_platform\n   from adws.adw_modules.gitlab import extract_project_path\n   from adws.adw_modules.code_review_providers import GitLabCodeReviewProvider\n   ```\n\n2. Use `resolve_issue()` instead of direct `fetch_issue()` call (line 497)\n\n3. Replace `make_issue_comment()` calls with provider-based approach:\n   ```python\n   provider = get_provider_for_issue(issue)\n   provider.add_comment(issue, message)\n   ```\n\n4. Add GitLab MR handling in the finalization step (similar to `adw_build_iso.py` lines 337-369)\n\n## Files to Modify\n\n- `/Users/ameno/dev/ask-anna-ai/adws/adw_review_iso.py`\n\n## Related Files (Reference Implementation)\n\n- `adws/adw_plan_iso.py` - Has working GitLab support\n- `adws/adw_build_iso.py` - Has working GitLab support\n- `adws/adw_modules/issue_providers.py` - Platform-agnostic issue resolution\n- `adws/adw_modules/gitlab.py` - GitLab-specific operations\n- `adws/adw_modules/notification_providers.py` - Platform-agnostic notifications\n\n## Environment\n\n- Repository: `git@gitlab.com:ameno13/ask-anna-ai.git`\n- Platform: GitLab\n- Jerry version: Current main branch\n"}`

## Bug Description
`adw_review_iso.py` is hardcoded to use GitHub-specific functions from `github.py` instead of using the platform-agnostic `issue_providers` module. This causes the workflow to fail when working with GitLab repositories because:
1. It directly imports `fetch_issue`, `make_issue_comment`, `get_repo_url`, and `extract_repo_path` from `github.py` (lines 40-45)
2. It attempts to use the `gh` CLI (GitHub CLI) instead of `glab` CLI (GitLab CLI)
3. It lacks GitLab MR handling in the finalization step

When executed in a GitLab repository, the workflow cannot fetch GitLab issues and cannot post comments to GitLab issues, making it completely non-functional for GitLab users.

## Problem Statement
The `adw_review_iso.py` workflow must be refactored to support both GitHub and GitLab platforms by using the existing platform-agnostic abstractions (`issue_providers.py` and `code_review_providers.py`) that are already successfully implemented in `adw_plan_iso.py` and `adw_build_iso.py`.

## Solution Statement
Replace GitHub-specific imports and function calls with platform-agnostic equivalents:
1. Use `resolve_issue()` for auto-detecting and fetching issues from any platform
2. Use `get_provider_for_issue()` to obtain the correct provider (GitHub or GitLab)
3. Replace all `make_issue_comment()` calls with `provider.add_comment()`
4. Add conditional GitLab MR handling in the finalization logic (similar to `adw_plan_iso.py`)

## Steps to Reproduce
1. Clone or work in a GitLab-hosted repository with issues (e.g., `git@gitlab.com:ameno13/ask-anna-ai.git`)
2. Ensure the repository has at least one GitLab issue (e.g., issue #2)
3. Run: `uv run adws/adw_review_iso.py 2 3f9d30d1 --skip-resolution`
4. **Expected:** Issue #2 is fetched from GitLab and review workflow proceeds normally
5. **Actual:** Workflow fails because it tries to use GitHub CLI (`gh`) instead of GitLab CLI (`glab`)

## Root Cause Analysis
The root cause is architectural inconsistency across ADW workflows:

**Working Workflows (`adw_plan_iso.py`, `adw_build_iso.py`):**
- Import from `issue_providers` module (lines 73-76 in `adw_plan_iso.py`)
- Use `resolve_issue()` to auto-detect platform from git remote
- Use `get_provider_for_issue()` to get platform-specific provider
- Handle both GitHub PRs and GitLab MRs conditionally

**Broken Workflow (`adw_review_iso.py`):**
- Directly imports from `github.py` module (lines 40-45)
- Uses `fetch_issue()` from `github.py` which only works with GitHub
- Uses `make_issue_comment()` which is GitHub-only
- Missing GitLab MR handling in finalization

The workflow was likely created before the platform abstraction layer was implemented and never updated to use the new abstractions.

## Relevant Files
Use these files to fix the bug:

- **`/Users/ameno/dev/tac/tac-8/trees/ef0fbb01/adws/adw_review_iso.py`** (lines 40-45, 223-229, 392-395, 420-423, 435-440, 449-460, 469-472, 490-496, 520-526, 541-543, 569-571, 580-581, 587-588, 595-596, 606-608) - Main file to fix, contains 15+ locations where GitHub-specific functions are called
- **`/Users/ameno/dev/tac/tac-8/trees/ef0fbb01/adws/adw_plan_iso.py`** (lines 73-78, 192-209, 230-241, 246-261, 477-524) - Reference implementation showing correct usage of platform-agnostic providers
- **`/Users/ameno/dev/tac/tac-8/trees/ef0fbb01/adws/adw_modules/issue_providers.py`** (lines 461-606, 608-636) - Contains `resolve_issue()` and `get_provider_for_issue()` functions
- **`/Users/ameno/dev/tac/tac-8/trees/ef0fbb01/adws/adw_modules/git_ops.py`** (lines 11-13, 38-60) - Contains platform detection and shared git operations
- **`/Users/ameno/dev/tac/tac-8/trees/ef0fbb01/adws/adw_modules/gitlab.py`** (lines 66-93, 95-130) - Contains GitLab-specific helper functions
- **`/Users/ameno/dev/tac/tac-8/trees/ef0fbb01/adws/adw_modules/code_review_providers.py`** - GitLab MR creation (reference for finalization step)
- **`/Users/ameno/dev/tac/tac-8/trees/ef0fbb01/adws/adw_modules/data_types.py`** - Contains `Issue`, `IssueSource`, and related types

### New Files
None. All required abstractions already exist.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update Import Statements (lines 40-45)
- Remove GitHub-specific imports: `fetch_issue`, `make_issue_comment`, `get_repo_url`, `extract_repo_path` from `adws.adw_modules.github`
- Add platform-agnostic imports: `resolve_issue`, `get_provider_for_issue` from `adws.adw_modules.issue_providers`
- Keep `get_repo_url` and `extract_repo_path` imports but change to import from `adws.adw_modules.git_ops` instead
- Add import for `detect_git_platform` from `adws.adw_modules.git_ops`
- Add import for `extract_project_path` from `adws.adw_modules.gitlab`
- Add import for `GitLabCodeReviewProvider` from `adws.adw_modules.code_review_providers`
- Add import for `IssueSource` from `adws.adw_modules.data_types`

### 2. Load Issue Using Platform-Agnostic Provider (lines 386-403)
- After loading state (line 388), resolve the issue using `resolve_issue(issue_number)` instead of using GitHub-specific `fetch_issue()`
- Store the resolved issue in a variable
- Get the provider using `get_provider_for_issue(issue)`
- Store provider for reuse throughout the workflow

### 3. Replace GitHub Comment Calls with Provider-Based Calls
- Line 392-395: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 420-423: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 435-440: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 449-460: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 469-472: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 490-496: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 520-526: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 541-543: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 569-571: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 580-581: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 587-588: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 595-596: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`
- Line 606-608: Replace `make_issue_comment()` with `provider.add_comment(issue, ...)`

### 4. Update resolve_blocker_issues Function (lines 206-255)
- Update function signature to accept `Issue` object and `IssueProvider` instead of just issue_number
- Replace `make_issue_comment(issue_number, ...)` call on line 223-229 with `provider.add_comment(issue, ...)`

### 5. Remove GitHub-Specific Issue Fetching (lines 546-556)
- Remove the try-except block that fetches issue using GitHub-specific `fetch_issue()` function
- The issue is already resolved in step 2, so this code is redundant
- Keep the repo URL and repo path extraction for backward compatibility if needed elsewhere

### 6. Add GitLab MR Support in Finalization (after line 592)
- After the existing `finalize_git_operations()` call, add conditional GitLab MR handling
- Check if `issue.source == IssueSource.GITLAB`
- If GitLab, instantiate `GitLabCodeReviewProvider` with `project_path=issue.repo_path`
- Check for existing MR using `gitlab_provider.check_exists()`
- If no MR exists, create one using `gitlab_provider.create()`
- Update state with `mr_url` and post comment to issue
- Use the implementation pattern from `adw_plan_iso.py` lines 477-524 as reference

### 7. Update Function Calls to Pass Issue and Provider
- Update all calls to `resolve_blocker_issues()` to pass the `issue` object and `provider` instead of just `issue_number`
- Ensure consistency across the entire file

### 8. Test with GitLab Repository
- Verify the workflow works in a GitLab repository
- Test issue resolution from GitLab
- Test comment posting to GitLab issues
- Test MR creation/update in GitLab

### 9. Test with GitHub Repository (Regression)
- Verify the workflow still works with GitHub repositories
- Test issue resolution from GitHub
- Test comment posting to GitHub issues
- Test PR creation/update in GitHub

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

```bash
# 1. Syntax validation
uv run python3 -m py_compile adws/adw_review_iso.py

# 2. Test with GitLab repository (primary use case)
# Requires: GitLab repository with issue #2, existing ADW state
cd /path/to/gitlab/repo
uv run adws/adw_review_iso.py 2 <adw-id> --skip-resolution

# 3. Test with GitHub repository (regression test)
# Requires: GitHub repository with issue, existing ADW state
cd /path/to/github/repo
uv run adws/adw_review_iso.py <issue-number> <adw-id> --skip-resolution

# 4. Verify imports are correct
grep -n "from adws.adw_modules.github import" adws/adw_review_iso.py
# Should return NO matches for fetch_issue, make_issue_comment

grep -n "from adws.adw_modules.issue_providers import" adws/adw_review_iso.py
# Should show resolve_issue, get_provider_for_issue

grep -n "from adws.adw_modules.git_ops import" adws/adw_review_iso.py
# Should show get_repo_url, extract_repo_path, detect_git_platform

# 5. Verify provider usage
grep -n "make_issue_comment" adws/adw_review_iso.py
# Should return NO matches

grep -n "provider.add_comment" adws/adw_review_iso.py
# Should return 13+ matches

# 6. Verify GitLab MR support added
grep -n "IssueSource.GITLAB" adws/adw_review_iso.py
# Should show conditional logic for GitLab MR handling

grep -n "GitLabCodeReviewProvider" adws/adw_review_iso.py
# Should show import and usage
```

## Notes
- This fix makes `adw_review_iso.py` consistent with `adw_plan_iso.py` and `adw_build_iso.py`
- The platform abstraction layer (`issue_providers.py`) already exists and is proven to work
- No new functionality needs to be created - only integration of existing abstractions
- The fix is surgical: only replace GitHub-specific calls with platform-agnostic equivalents
- Backward compatibility with GitHub is maintained through the abstraction layer
- After this fix, all three core isolated workflows (plan, build, review) will support both GitHub and GitLab
