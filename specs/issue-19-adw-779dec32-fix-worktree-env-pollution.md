# Bug: Isolate worktree env better

## Metadata
issue_number: `19`
adw_id: `779dec32`
issue_json: `{"number": "19", "title": "Isolate worktree env better", "body": "There is a bug during worktree dev where certain files use hardcoded worktree paths. This can subseqyently cause issues during dev when bootstrapping workflows. Investigate this issue and develop a workaround to ensure isolated envs without polluting main context. A viable solution is to reset or delete these files before starting new workflows\n\n[.mcp.json](https://github.com/ameno-/jerry/pull/17/files#diff-d5d3368a61f8d02e085f7a4cb666ee471cf5383690a04b64c839c6ae2080ceb9)\n[.ports.env](https://github.com/ameno-/jerry/pull/17/files#diff-e2fe5c6b2c4c6428e95e3c4fe07f257c09ab6bda517ab831e4f0e5999591ae8b)\n[playwright-mcp-config.json](https://github.com/ameno-/jerry/pull/17/files#diff-8d7a667c2aa5248d34bd00033488936850b18d73f8f1c367ebf07ae330de2297)"}`

## Bug Description
During worktree development workflows, three configuration files (`.mcp.json`, `.ports.env`, and `playwright-mcp-config.json`) are created with hardcoded absolute paths pointing to specific worktree directories. When these files are accidentally committed or persist in the main repository, they cause issues for subsequent workflow executions because:

1. The paths point to old/non-existent worktree directories (e.g., `/Users/ameno/dev/tac/tac-8/trees/d40542b6/`)
2. New worktrees cannot use the correct paths for their isolated environments
3. Port allocations become stale and cause conflicts
4. The main repository context gets polluted with worktree-specific configuration

**Evidence from current state:**
- Root `.mcp.json` has hardcoded path: `/Users/ameno/dev/tac/tac-8/trees/d40542b6/playwright-mcp-config.json`
- Root `playwright-mcp-config.json` has hardcoded path: `/Users/ameno/dev/tac/tac-8/trees/d40542b6/videos`
- Worktree `.mcp.json` has hardcoded path: `/Users/ameno/dev/tac/tac-8/trees/779dec32/playwright-mcp-config.json`
- Current worktree is `779dec32` but main repo files reference `d40542b6`

## Problem Statement
Worktree-specific configuration files with hardcoded absolute paths are being created in both the main repository and worktrees, causing:
1. Bootstrap failures when old paths don't exist
2. Loss of worktree isolation due to stale configuration
3. Main repository pollution with worktree-specific settings
4. Git tracking of files that should be ephemeral and worktree-local

## Solution Statement
Implement a cleanup mechanism that resets/deletes these worktree-specific files before creating new worktrees, ensuring:
1. Main repository stays clean of worktree-specific paths
2. Each worktree starts with a fresh configuration slate
3. Files are properly gitignored to prevent accidental commits
4. Workflows automatically clean up stale configurations before bootstrapping

## Steps to Reproduce
1. Run an ADW workflow that creates a worktree (e.g., `./adws/adw_plan_iso.py github:123`)
2. The workflow creates `.mcp.json`, `.ports.env`, and `playwright-mcp-config.json` with hardcoded paths to that worktree
3. Files may get committed or persist in main repo
4. Run a new ADW workflow in a different worktree
5. New workflow tries to use old paths from previous worktree
6. Bootstrap fails or uses incorrect configuration

## Root Cause Analysis

**Primary Cause:**
The `install_worktree.md` slash command copies configuration files from the parent repository and updates them with absolute paths for the current worktree. These files are then created in both:
- The worktree directory (correct)
- The main repository directory (incorrect - pollution)

**Contributing Factors:**
1. **File copying without isolation**: `install_worktree.md` (lines 42-50) copies `.mcp.json` and `playwright-mcp-config.json` from parent repo and updates paths, but this happens in a context where files may be written to main repo
2. **Missing .gitignore entries**: The three files are not explicitly listed in `.gitignore`:
   - `.mcp.json` is not ignored
   - `playwright-mcp-config.json` is not ignored
   - `.ports.env` IS ignored (line 4) ✓
3. **No pre-workflow cleanup**: ADW workflows (`adw_plan_iso.py`, `adw_patch_iso.py`) don't clean up stale configuration before creating new worktrees
4. **Path mutation in `worktree_ops.py`**: `setup_worktree_environment()` (line 152-172) creates `.ports.env` but doesn't handle MCP config files

**File Creation Flow:**
```
adw_plan_iso.py (line 300)
  ↓
setup_worktree_environment(worktree_path, ...)
  ↓
Creates .ports.env in worktree (correct)

Separately, agent executes /install_worktree command
  ↓
Copies and updates .mcp.json + playwright-mcp-config.json
  ↓
Files created in both main repo AND worktree (bug)
```

## Relevant Files
Use these files to fix the bug:

- **`/Users/ameno/dev/tac/tac-8/trees/779dec32/.gitignore`** (line 4) - Already has `.ports.env` ignored, need to add `.mcp.json` and `playwright-mcp-config.json`

- **`/Users/ameno/dev/tac/tac-8/trees/779dec32/adws/adw_modules/worktree_ops.py`** (lines 152-172) - `setup_worktree_environment()` function that sets up worktree files; needs cleanup logic

- **`/Users/ameno/dev/tac/tac-8/trees/779dec32/adws/adw_plan_iso.py`** (line 300) - Calls `setup_worktree_environment()` during worktree creation; should call cleanup before

- **`/Users/ameno/dev/tac/tac-8/trees/779dec32/adws/adw_patch_iso.py`** (line 445) - Also calls `setup_worktree_environment()`; should call cleanup before

- **`/Users/ameno/dev/tac/tac-8/trees/779dec32/.claude/commands/install_worktree.md`** (lines 42-50) - Documents the process of copying and updating MCP config files; should emphasize worktree-only creation

- **`/Users/ameno/dev/tac/tac-8/trees/779dec32/.mcp.json`** (current worktree) - Example of file with hardcoded path that should be worktree-local only

- **`/Users/ameno/dev/tac/tac-8/.mcp.json`** (main repo) - Should not exist or should be a template without hardcoded paths

- **`/Users/ameno/dev/tac/tac-8/trees/779dec32/playwright-mcp-config.json`** (current worktree) - Example of file with hardcoded path

- **`/Users/ameno/dev/tac/tac-8/playwright-mcp-config.json`** (main repo) - Should not exist or should be a template

### New Files
None - this is a cleanup and prevention fix

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update .gitignore to prevent future commits
- Add `.mcp.json` to `.gitignore` to prevent it from being tracked
- Add `playwright-mcp-config.json` to `.gitignore` to prevent it from being tracked
- Add `worktree.config` to `.gitignore` (also contains worktree-specific paths)
- Verify `.ports.env` is already present (line 4)

### 2. Create cleanup utility function in worktree_ops.py
- Add new function `cleanup_worktree_config_files(project_root: str, logger: logging.Logger) -> None`
- Function should delete these files from project root if they exist:
  - `.mcp.json`
  - `playwright-mcp-config.json`
  - `.ports.env`
  - `worktree.config`
- Log each deletion for observability
- Handle file not found gracefully (not an error condition)

### 3. Integrate cleanup into adw_plan_iso.py
- Import the new cleanup function
- Call `cleanup_worktree_config_files(project_root, logger)` BEFORE calling `setup_worktree_environment()`
- This ensures main repo is clean before creating worktree config
- Add log message: "Cleaning up stale worktree config files from main repo"

### 4. Integrate cleanup into adw_patch_iso.py
- Import the new cleanup function
- Call `cleanup_worktree_config_files(project_root, logger)` BEFORE calling `setup_worktree_environment()`
- This ensures main repo is clean before creating worktree config
- Add log message: "Cleaning up stale worktree config files from main repo"

### 5. Delete stale files from main repository
- Run cleanup manually to remove existing pollution:
  ```bash
  cd /Users/ameno/dev/tac/tac-8
  rm -f .mcp.json playwright-mcp-config.json .ports.env worktree.config
  ```
- Verify files are deleted
- Confirm worktree files remain intact

### 6. Add documentation comment to install_worktree.md
- Update the "Copy and configure MCP files" section (lines 42-50)
- Add explicit note that these files should ONLY be created in the worktree directory
- Add warning about not creating these in the parent repository
- Document that cleanup happens automatically before worktree setup

### 7. Test the fix with a new workflow
- Create a test worktree using `./adws/adw_plan_iso.py prompt:"test isolation"`
- Verify cleanup function runs and logs deletions
- Verify new worktree has correct config files with paths for that worktree
- Verify main repo does NOT have `.mcp.json` or `playwright-mcp-config.json`
- Check git status to confirm no unexpected files are tracked

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

```bash
# 1. Verify .gitignore has the new entries
grep -E "\.mcp\.json|playwright-mcp-config\.json|worktree\.config" .gitignore

# 2. Verify cleanup function exists
grep -A 10 "def cleanup_worktree_config_files" adws/adw_modules/worktree_ops.py

# 3. Verify cleanup is called in adw_plan_iso.py
grep -B 2 -A 2 "cleanup_worktree_config_files" adws/adw_plan_iso.py

# 4. Verify cleanup is called in adw_patch_iso.py
grep -B 2 -A 2 "cleanup_worktree_config_files" adws/adw_patch_iso.py

# 5. Verify main repo is clean (these should return "not found")
ls -la /Users/ameno/dev/tac/tac-8/.mcp.json 2>&1
ls -la /Users/ameno/dev/tac/tac-8/playwright-mcp-config.json 2>&1

# 6. Run a test workflow and verify isolation
./adws/adw_plan_iso.py prompt:"test worktree isolation" --dry-run

# 7. After test workflow, verify main repo stays clean
cd /Users/ameno/dev/tac/tac-8
git status | grep -E "\.mcp\.json|playwright-mcp-config\.json|worktree\.config"
# Should return nothing (no tracked changes for these files)

# 8. Verify worktree files exist with correct paths
WORKTREE_PATH=$(ls -td trees/* | head -1)
grep "$WORKTREE_PATH" "$WORKTREE_PATH/.mcp.json"
grep "$WORKTREE_PATH" "$WORKTREE_PATH/playwright-mcp-config.json"

# 9. Run existing ADW workflows to check for regressions
./adws/adw_plan_iso.py prompt:"regression test" --dry-run
```

## Notes

**Design Decision: Cleanup vs Template Approach**
We chose cleanup over a pure template approach because:
1. Templates would require maintaining separate template files (`.mcp.template.json`, etc.)
2. Cleanup is simpler and more maintainable
3. The install_worktree command already handles path updates dynamically
4. Cleanup ensures main repo never gets polluted, even if workflows change

**Prevention Layers:**
1. `.gitignore` - Prevents accidental commits (defense in depth)
2. Cleanup function - Removes stale files before worktree creation (primary fix)
3. Documentation - Warns future developers about the isolation requirement (education)

**Impact on Existing Worktrees:**
- Existing worktrees are unaffected
- Their config files remain valid with their own paths
- Only the main repository and future worktrees benefit from cleanup

**Why .ports.env wasn't causing visible issues:**
- It's already in `.gitignore` (line 4), so never gets committed
- But we still clean it up for consistency and safety
