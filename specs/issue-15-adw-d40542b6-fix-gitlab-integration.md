# Bug: GitLab integration is not working - 404 Not Found

## Metadata
issue_number: `15`
adw_id: `d40542b6`
issue_json: `{"number": "15", "title": "Gitlab integration is not", "body": "/bug\nThe Gitlab integration is failing to find and pickup changes in a gitlab issue. Review the implementation and verify that we can consume gitlab issues and trigger adws. The functionality should identical to github.\n\nGitlab issue: https://gitlab.com/ameno13/jerry/-/issues/1\n\nHere is the log output:\n\n```\nCreated new ADW ID and state: 7e4b818e\nUsing ADW ID: 7e4b818e\n\n=== ISOLATED PLAN PHASE ===\nRunning: uv run /Users/ameno/dev/tac/tac-8/adws/adw_plan_iso.py gitlab:1 7e4b818e\nADW Logger initialized - ID: 7e4b818e\nFound existing state from /Users/ameno/dev/tac/tac-8/agents/7e4b818e/adw_state.json\nFound existing ADW state for ID: 7e4b818e\nFound existing state from /Users/ameno/dev/tac/tac-8/agents/7e4b818e/adw_state.json\nADW Logger initialized - ID: 7e4b818e\nADW Plan Iso starting - ID: 7e4b818e, Issue ref: gitlab:1\n\n   ERROR\n\n  404 Not Found.\n\n\nError parsing GitLab issue data: Failed to fetch GitLab issue:\n   ERROR\n\n  404 Not Found.\n\n\nError resolving issue: Failed to fetch GitLab issue:\n   ERROR\n\n  404 Not Found.\n\n\nIsolated plan phase failed\n```"}`

## Bug Description
The GitLab integration fails to fetch issues with a 404 Not Found error when using the `gitlab:1` issue reference format. The bug occurs because the `GitLabIssueProvider` attempts to determine the project path by examining the current repository's git remote URL, but the current repository is hosted on GitHub (`https://github.com/ameno-/jerry.git`), not GitLab.

When the provider calls `_get_project_path()`, it extracts `ameno-/jerry` from the GitHub URL and then tries to fetch issue #1 from GitLab using this GitHub-style path, which results in a 404 error because the actual GitLab issue exists at `ameno13/jerry`.

The glab CLI works correctly when provided with the correct project path (`glab issue view 1 -R ameno13/jerry --output json` succeeds), confirming that:
1. glab CLI is properly installed and authenticated
2. The GitLab issue exists and is accessible
3. The problem is solely in the project path resolution logic

## Problem Statement
When using the `gitlab:ISSUE_NUMBER` format to reference a GitLab issue from a repository that is hosted on GitHub (or vice versa), the GitLab provider incorrectly uses the current repository's remote URL to determine the project path, resulting in failed API calls with 404 errors.

The core issue is that the `gitlab:` prefix indicates the issue source platform, but doesn't provide information about which GitLab project contains that issue. The current implementation assumes the issue belongs to the same project as the current working directory's git remote, which fails when the git remote is from a different platform or project.

## Solution Statement
Modify the GitLab issue resolution logic to support explicit project path specification when using the `gitlab:` prefix. The solution will:

1. **Extend the issue reference format** to support `gitlab:PROJECT_PATH:ISSUE_NUMBER` (e.g., `gitlab:ameno13/jerry:1`)
2. **Update `resolve_issue()` function** to parse the extended format and pass the project path to the provider
3. **Enhance `GitLabIssueProvider`** to accept and use an explicit project path when provided
4. **Provide clear error messages** when GitLab issue resolution fails due to mismatched platforms
5. **Update documentation** to explain the extended format and when it's needed

This approach maintains backward compatibility (simple `gitlab:123` still works for repos hosted on GitLab) while enabling cross-platform issue references.

## Steps to Reproduce
1. Clone a GitHub-hosted repository (e.g., `https://github.com/ameno-/jerry.git`)
2. Attempt to reference a GitLab issue using the format `gitlab:1`
3. Run `uv run adws/adw_plan_iso.py gitlab:1`
4. Observe the 404 Not Found error

**Expected behavior:** The system should either:
- Detect the mismatch and provide a helpful error message, OR
- Support an extended format that specifies the GitLab project path

**Actual behavior:** The system attempts to fetch the issue using the GitHub project path from the current repository's remote, resulting in a 404 error from GitLab.

## Root Cause Analysis
The root cause is in `/Users/ameno/dev/tac/tac-8/trees/d40542b6/adws/adw_modules/issue_providers.py` at line 513:

```python
if issue_ref.startswith("gitlab:"):
    provider = GitLabIssueProvider(repo_path)
    return provider.fetch_issue(issue_ref[7:])  # Remove "gitlab:" prefix
```

When `repo_path` is `None`, the `GitLabIssueProvider._get_project_path()` method (lines 122-130) calls:
```python
from .git_ops import get_repo_url
from .gitlab import extract_project_path

return extract_project_path(get_repo_url())
```

This extracts the project path from the **current repository's** git remote URL. If the current repository is on GitHub but the issue is on GitLab, this yields an incorrect project path.

**Example flow:**
1. Current git remote: `https://github.com/ameno-/jerry.git`
2. `extract_project_path()` returns: `ameno-/jerry`
3. glab CLI command: `glab issue view 1 -R ameno-/jerry`
4. GitLab API responds: 404 Not Found (no such project on GitLab)

The correct project path should be `ameno13/jerry` for the GitLab issue.

## Relevant Files
Files that need modification to fix this bug:

- **adws/adw_modules/issue_providers.py** (lines 511-513)
  - Update `resolve_issue()` to parse extended format `gitlab:PROJECT:ISSUE`
  - Pass extracted project path to `GitLabIssueProvider`
  - Add validation and error handling for malformed references

- **adws/adw_modules/issue_providers.py** (lines 108-136, `GitLabIssueProvider` class)
  - Ensure the provider correctly uses the explicit project path when provided
  - Add validation to detect platform mismatches
  - Improve error messages when project path is invalid

- **specs/gitlab-integration-guide.md**
  - Document the extended `gitlab:PROJECT:ISSUE` format
  - Explain when to use explicit project paths
  - Provide examples for cross-platform scenarios

### New Files
None required - this is a bug fix to existing implementation.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Add Support for Extended GitLab Issue Reference Format
- Modify `resolve_issue()` in `/Users/ameno/dev/tac/tac-8/trees/d40542b6/adws/adw_modules/issue_providers.py` around line 511
- Parse the `gitlab:` prefix to support both formats:
  - Simple format: `gitlab:123` (uses current repo's remote)
  - Extended format: `gitlab:ameno13/jerry:123` (explicit project path)
- Extract project path and issue number separately
- Pass the explicit project path to `GitLabIssueProvider` constructor

### 2. Enhance GitLabIssueProvider to Use Explicit Project Path
- Ensure `GitLabIssueProvider.__init__()` correctly stores the `project_path` parameter
- Verify `_get_project_path()` method returns the explicit path when provided
- Add validation to ensure the project path is in correct format (`namespace/project`)

### 3. Add Platform Mismatch Detection and Clear Error Messages
- When `gitlab:ISSUE` format is used (no explicit project), detect if current repo is not GitLab
- If mismatch detected, provide helpful error message:
  ```
  Error: Cannot resolve GitLab issue 'gitlab:1' - current repository is hosted on github.com.

  To reference a GitLab issue from a different project, use the extended format:
    gitlab:PROJECT_PATH:ISSUE_NUMBER

  Example:
    gitlab:ameno13/jerry:1
  ```
- Implement this check before calling glab CLI to fail fast

### 4. Update Documentation with Extended Format
- Update `/Users/ameno/dev/tac/tac-8/trees/d40542b6/specs/gitlab-integration-guide.md`
- Add section explaining the extended format
- Provide examples for cross-platform scenarios
- Document when explicit project paths are required

### 5. Add Unit Tests for Extended Format
- Create tests in `adws/adw_tests/test_gitlab_providers.py` (or relevant test file)
- Test parsing of `gitlab:PROJECT:ISSUE` format
- Test error handling for malformed references
- Test platform mismatch detection
- Mock glab CLI calls to avoid requiring real GitLab access

### 6. Verify Fix with Manual Testing
- Test simple format in GitLab repo: `gitlab:123`
- Test extended format in GitHub repo: `gitlab:ameno13/jerry:1`
- Test error messages with invalid formats
- Verify glab CLI is called with correct project path

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

```bash
# 1. Verify Python syntax is valid
uv run python -m py_compile adws/adw_modules/issue_providers.py

# 2. Test extended format parsing (manual verification)
uv run python -c "
from adws.adw_modules.issue_providers import resolve_issue
# Test extended format
try:
    issue = resolve_issue('gitlab:ameno13/jerry:1')
    print(f'✓ Extended format works: {issue.title}')
except Exception as e:
    print(f'✗ Extended format failed: {e}')

# Test simple format with platform detection
try:
    issue = resolve_issue('gitlab:1')
    print(f'✓ Simple format works: {issue.title}')
except Exception as e:
    print(f'Expected error with helpful message: {e}')
"

# 3. Verify glab CLI still works directly
glab issue view 1 -R ameno13/jerry --output json | jq -r '.title'

# 4. Test that GitHub issues still work (regression test)
# (Skip if no GitHub issues available)
# uv run python -c "from adws.adw_modules.issue_providers import resolve_issue; issue = resolve_issue('github:1'); print(f'GitHub still works: {issue.title}')"

# 5. Run unit tests (once created)
uv run python -m pytest adws/adw_tests/test_gitlab_providers.py -v -k gitlab

# 6. Verify error messages are helpful
uv run python -c "
from adws.adw_modules.issue_providers import resolve_issue
try:
    issue = resolve_issue('gitlab:999999')
except Exception as e:
    print(f'Error message: {e}')
    # Should mention platform mismatch or provide guidance
"
```

## Notes

### Key Insights
- The `gitlab:` prefix indicates the **source platform** but not the **specific project**
- When working in a multi-platform environment (GitHub repo referencing GitLab issues), explicit project paths are required
- The glab CLI requires the `-R` flag with the full project path (`namespace/project`)
- Current git remote URL is not always the correct source for issue resolution

### Alternative Solutions Considered
1. **Auto-detect from issue URL**: Parse full GitLab URLs (e.g., `https://gitlab.com/ameno13/jerry/-/issues/1`)
   - Pros: User-friendly, no new syntax to learn
   - Cons: Already solved by the URL format, doesn't address the `gitlab:` prefix issue

2. **Configuration file**: Store GitLab project mappings in `.gitlab-projects.yml`
   - Pros: Clean syntax, centralized configuration
   - Cons: Adds configuration complexity, doesn't work well for multi-project repositories

3. **Extended format (chosen solution)**: `gitlab:PROJECT:ISSUE`
   - Pros: Explicit, no ambiguity, no external configuration needed
   - Cons: Slightly more verbose, requires documentation

### Backward Compatibility
- The simple `gitlab:ISSUE` format must continue to work for repositories hosted on GitLab
- Only show platform mismatch error when simple format is used from a non-GitLab repository
- Extended format should work from any repository regardless of hosting platform

### Future Enhancements
- Consider supporting full GitLab URLs as issue references
- Add caching of project path to avoid repeated git remote lookups
- Support environment variable for default GitLab project path
- Add auto-completion for GitLab projects in shell integrations
