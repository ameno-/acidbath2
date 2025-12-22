# Chore: Manage Completed Issues

## Metadata
adw_id: `b4f53ff6`
prompt: `Make sure the local issues directory issues are up to date. If issues are completed, mmove it to new done dir.`

## Chore Description

This chore organizes the local issues directory by moving completed issues (those with status `resolved` or `closed`) into a dedicated `done/` subdirectory. This keeps the main `issues/` directory focused on active work while preserving completed issue history for reference.

The local issues directory (`issues/`) currently contains issue files tracking ADW workflow validation fixes. Several issues have been resolved and should be archived to maintain directory clarity.

## Relevant Files

### Existing Files
- **`issues/README.md`** - Documents the local issues system and file format. Will need updates to document the `done/` subdirectory.
- **`issues/issue-fix-adw_build_iso.md`** - Status: `resolved` - needs to be moved to `done/`
- **`issues/issue-fix-adw_plan_iso.md`** - Status: `resolved` - needs to be moved to `done/`
- **`issues/issue-fix-workflow_ops.md`** - Status: `resolved` - needs to be moved to `done/`
- **`issues/issue-fix-adw_patch_iso.md`** - Status: `in_progress` - remains in active directory
- **`issues/issue-fix-adw_plan_build_iso.md`** - Status: `in_progress` - remains in active directory
- **`issues/issue-fix-adw_ship_iso.md`** - Status: `in_progress` - remains in active directory
- **`issues/issue-fix-trigger_github.md`** - Status: `in_progress` - remains in active directory
- **`adws/adw_modules/issue_providers.py`** - May need updates if file paths are hardcoded (check LocalIssueProvider implementation)

### New Files
- **`issues/done/README.md`** - Documentation explaining the done directory and its purpose

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Verify Current Issue Status
- Read all issue files in `issues/` directory to confirm their current status
- Identify which issues have `status: resolved` or `status: closed`
- Confirm the list matches: `issue-fix-adw_build_iso.md`, `issue-fix-adw_plan_iso.md`, `issue-fix-workflow_ops.md`

### 2. Check Issue Provider Implementation
- Read `adws/adw_modules/issue_providers.py` focusing on the `LocalIssueProvider` class
- Verify how it resolves issue paths (whether it looks in subdirectories or only root `issues/`)
- Determine if any code changes are needed to support `issues/done/` subdirectory

### 3. Create Done Directory Structure
- Create `issues/done/` directory
- Create `issues/done/README.md` documenting the purpose and structure of the done directory

### 4. Move Completed Issues
- Move `issues/issue-fix-adw_build_iso.md` to `issues/done/`
- Move `issues/issue-fix-adw_plan_iso.md` to `issues/done/`
- Move `issues/issue-fix-workflow_ops.md` to `issues/done/`

### 5. Update Main Issues README
- Edit `issues/README.md` to document the new `done/` subdirectory
- Add section explaining when issues are moved to `done/`
- Update file structure documentation if present

### 6. Validate Changes
- Verify all 3 resolved issues are now in `issues/done/`
- Verify 4 in-progress issues remain in `issues/`
- Verify both README files are updated with clear documentation
- Test that LocalIssueProvider can still resolve issues if needed

## Validation Commands
Execute these commands to validate the chore is complete:

- `ls -la issues/` - Should show only 4 in-progress issue files (plus README.md and done/ directory)
- `ls -la issues/done/` - Should show 3 resolved issue files (plus README.md)
- `grep -l "status: resolved" issues/issue-*.md` - Should return no results (all resolved issues moved)
- `grep -l "status: resolved" issues/done/issue-*.md` - Should show all 3 moved files
- `grep -l "status: in_progress" issues/issue-*.md` - Should show the 4 remaining active issues
- `cat issues/README.md | grep -A 5 "done/"` - Should show documentation about the done directory

## Notes

- The move operation should preserve all file metadata and git history
- If `LocalIssueProvider` needs updates to support subdirectories, those changes should be minimal and backward-compatible
- Consider whether the provider should automatically search `done/` when resolving issue references
- The `done/` directory structure could be expanded in the future (e.g., by date, by workflow type) but keep it simple for now
