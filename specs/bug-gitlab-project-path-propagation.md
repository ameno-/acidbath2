# Bug: GitLab project_path not propagated through provider abstraction

## Metadata
issue_type: `bug`
related_issue: `21`

## Bug Description

When using the extended GitLab format (`gitlab:ameno13/jerry:1`) to reference issues from a different project than the current repository, the `project_path` is correctly parsed during issue resolution but not propagated when `get_provider_for_issue()` creates a new provider instance. This causes comment posting to fail with 404 errors because the provider attempts to use the git remote detection (which finds GitHub as origin) instead of the explicit project path.

The issue manifests when:
1. Current repository has GitHub as origin remote
2. GitLab issue is referenced using extended format: `gitlab:PROJECT_PATH:ISSUE_NUMBER`
3. Issue is resolved correctly with the explicit project path
4. But when `get_provider_for_issue(issue)` is called, it creates a new `GitLabIssueProvider(None)`
5. The new provider uses git remote detection which finds GitHub, not the GitLab project

## Root Cause Analysis

The abstraction layer was missing a key piece of context propagation:

1. **resolve_issue()** correctly parses `gitlab:ameno13/jerry:1` and creates `GitLabIssueProvider(project_path="ameno13/jerry")`
2. The issue is fetched successfully
3. But the `project_path` was not stored in the `Issue` object
4. When `get_provider_for_issue(issue)` is called later, it creates a new provider without the project path
5. The new provider's `_get_project_path()` falls back to git remote detection, which returns the wrong URL (GitHub origin)

## Solution

Implemented a multi-part fix:

1. **Added `repo_path` field to Issue model** (`data_types.py`)
   - Stores the repository/project path (e.g., `owner/repo` for GitHub, `namespace/project` for GitLab)

2. **Updated `gitlab.fetch_issue()` to store project_path** (`gitlab.py`)
   - Sets `repo_path=project_path` when creating Issue object

3. **Updated `make_issue_comment()` to accept explicit project_path** (`gitlab.py`)
   - New optional parameter: `project_path: Optional[str] = None`
   - Only falls back to git remote detection if not provided

4. **Updated `mark_issue_in_progress()` to accept explicit project_path** (`gitlab.py`)
   - Same pattern as `make_issue_comment()`

5. **Updated `GitLabIssueProvider` to pass project_path** (`issue_providers.py`)
   - `update_status()` and `add_comment()` now call `make_issue_comment(..., project_path=self._get_project_path())`

6. **Updated `get_provider_for_issue()` to use `issue.repo_path`** (`issue_providers.py`)
   - Uses `issue.repo_path` if no explicit `repo_path` is passed

## Files Modified

- **adws/adw_modules/data_types.py**
  - Added `repo_path: Optional[str] = None` field to Issue model

- **adws/adw_modules/gitlab.py**
  - Updated `fetch_issue()` to set `repo_path=project_path`
  - Updated `make_issue_comment()` signature to accept optional `project_path`
  - Updated `mark_issue_in_progress()` signature to accept optional `project_path`

- **adws/adw_modules/issue_providers.py**
  - Updated `GitLabIssueProvider.update_status()` to pass `project_path`
  - Updated `GitLabIssueProvider.add_comment()` to pass `project_path`
  - Updated `get_provider_for_issue()` to use `issue.repo_path` when available

## Validation

```bash
# Verify GitLab comment posting works
glab issue note 1 -R ameno13/jerry --message "Test comment from CLI"
# Expected: Success, returns comment URL

# Run workflow with GitLab issue
uv run adws/adw_plan_iso.py "gitlab:ameno13/jerry:1"
# Expected: All comments posted to GitLab issue successfully
```

## Testing Results

- GitLab issue #1 in `ameno13/jerry` received all workflow comments
- No 404 errors during comment posting
- Workflow completed successfully with full observability

## Backward Compatibility

All changes are backward compatible:
- New `repo_path` field has default value `None`
- Functions accept optional `project_path` parameter with fallback to git remote detection
- Existing GitHub workflows continue to work unchanged
- Existing GitLab workflows with simple format (`gitlab:123`) continue to work when git remote is GitLab
