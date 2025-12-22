# Bug Fix: GitLabCodeReviewProvider Parameter Mismatch

## Issue Summary

**Error**: `TypeError: GitLabCodeReviewProvider.__init__() got an unexpected keyword argument 'repo_path'`

**Severity**: Critical - blocks all GitLab issue workflows

**ADWs Affected**: test1208a export/bootstrap verification

## Root Cause

The `GitLabCodeReviewProvider` class constructor expects `project_path` parameter, but `adw_plan_iso.py` and `adw_build_iso.py` were incorrectly passing `repo_path`.

### Class Definition (code_review_providers.py:395)
```python
class GitLabCodeReviewProvider:
    def __init__(self, project_path: Optional[str] = None, logger: Optional[logging.Logger] = None):
        self._project_path = project_path
        self._logger = logger or logging.getLogger(__name__)
```

### Incorrect Usage (before fix)
```python
# adw_plan_iso.py:486
gitlab_provider = GitLabCodeReviewProvider(repo_path=issue.repo_path, logger=logger)

# adw_build_iso.py:353
gitlab_provider = GitLabCodeReviewProvider(repo_path=issue.repo_path, logger=logger)
```

### Correct Usage (after fix)
```python
# adw_plan_iso.py:486
gitlab_provider = GitLabCodeReviewProvider(project_path=issue.repo_path, logger=logger)

# adw_build_iso.py:353
gitlab_provider = GitLabCodeReviewProvider(project_path=issue.repo_path, logger=logger)
```

## Files Changed

| File | Line | Change |
|------|------|--------|
| `adws/adw_plan_iso.py` | 486 | `repo_path=` → `project_path=` |
| `adws/adw_build_iso.py` | 353 | `repo_path=` → `project_path=` |

## Why This Happened

The factory function `get_code_review_provider()` at line 824 correctly uses:
```python
return GitLabCodeReviewProvider(project_path=repo_path, logger=logger)
```

However, when GitLab support was added to the isolated ADWs, the direct instantiation incorrectly used `repo_path` (GitHub's parameter name) instead of `project_path` (GitLab's parameter name).

## Behavioral Lesson

**CRITICAL**: Previous agent made a mistake by copying fixes directly to jerry-next (the bootstrapped instance) without tracking changes in the source repository (tac-8). This caused:

1. Changes lost on subsequent re-exports
2. No audit trail of what was fixed
3. Source repository remained broken

**Correct Workflow**:
1. Fix in source (tac-8) first
2. Commit and track changes with PR
3. Re-export to target repositories
4. Validate the export

## Testing

1. Run `adw_plan_iso.py` with GitLab source:
   ```bash
   ./adws/adw_plan_iso.py gitlab:test-issue
   ```

2. Run `adw_build_iso.py` with GitLab source:
   ```bash
   ./adws/adw_build_iso.py specs/test-spec.md
   ```

3. Verify no TypeError occurs during GitLabCodeReviewProvider instantiation

## Related

- **GitHub PR**: https://github.com/ameno-/jerry/pull/35
- **ADW IDs**: test1208a
- **GitLab Mirror**: jerry-next commit 4b27a06

## Resolution

- Fixed in commit `82fa67c` on main
- Re-exported Jerry and bootstrapped jerry-next
- Validated with `jerry_validate.py --level 2`
