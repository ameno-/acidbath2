# Feature: ADW Rebase ISO - PR-First Merge Conflict Resolution

## Metadata
adw_id: `c2b8a2d0`
prompt: `{"number": "5", "title": "feat: Add adw_rebase_iso.py for merge conflict resolution", "body": "## Problem\nPR #2 (ADW a6edbc74) has merge conflicts that cannot be resolved by existing ADWs.\n\nCurrently available workflows:\n- `adw_plan_iso` - Planning only\n- `adw_build_iso` - Building only\n- `adw_patch_iso` - Quick patches\n- `adw_ship_iso` - Merge to main (fails on conflicts)\n\n**Gap**: No workflow to resolve merge conflicts when a feature branch diverges from main.\n\n## Proposed Solution\nCreate `adw_rebase_iso.py` with **PR-first interface**:\n\n### Usage\n```bash\n# PR number required, issue/adw-id optional\nuv run adws/adw_rebase_iso.py <pr-number> [adw-id] [--dry-run]\n\n# Examples\nuv run adws/adw_rebase_iso.py 2              # Just PR number\nuv run adws/adw_rebase_iso.py 2 a6edbc74     # With known ADW ID\nuv run adws/adw_rebase_iso.py 2 --dry-run    # Validate only\n```\n\n### Workflow\n1. Fetch PR details via `gh pr view <pr-number> --json ...`\n2. Extract branch name from PR\n3. Find ADW state by matching branch pattern (or use provided adw-id)\n4. Validate/create worktree for the branch\n5. Fetch latest origin/main\n6. Detect conflicts via dry-run rebase\n7. Attempt rebase onto origin/main\n8. Report conflict files if resolution fails (agent assistance)\n9. Commit and force-push if successful\n10. PR auto-updates (same branch)\n\n## Acceptance Criteria\n- [ ] `uv run adws/adw_rebase_iso.py <pr-number> --dry-run` validates inputs\n- [ ] Works with just PR number (derives branch, finds state)\n- [ ] Optionally accepts adw-id for direct state lookup\n- [ ] Posts progress to linked issue (if any)\n- [ ] Handles conflict detection gracefully\n- [ ] Creates manifest at `adws/manifests/adw_rebase_iso.yaml`\n\n## Reference\n- Triggered by: PR #2 conflict (ADW a6edbc74, Issue #1)\n- Pattern reference: `adw_ship_iso.py`, `adw_patch_iso.py`"}`

## Feature Description
The `adw_rebase_iso.py` workflow solves a critical gap in the ADW ecosystem: handling merge conflicts when a feature branch diverges from main. Currently, `adw_ship_iso.py` fails when merge conflicts exist, and there's no automated way to rebase feature branches onto the latest main. This workflow provides a PR-first interface that automatically discovers the related ADW state, validates the worktree environment, and attempts to rebase the branch onto origin/main within the isolated worktree. If conflicts occur, it provides detailed reporting for agent-assisted resolution.

## User Story
As a developer using ADW workflows
I want to rebase my feature branch onto the latest main when conflicts occur
So that I can resolve conflicts in isolation and keep my PR up-to-date with minimal manual intervention

## Problem Statement
When a feature branch is developed in an isolated worktree and diverges from main (due to other PRs merging), the `adw_ship_iso` workflow fails with merge conflicts. Currently, there's no ADW workflow to:
1. Detect that a PR has conflicts with main
2. Rebase the feature branch onto the latest main in the isolated worktree
3. Report conflict details for agent or manual resolution
4. Automatically push the rebased branch to update the PR

This forces developers to manually manage git operations outside the ADW isolation model, breaking the workflow and potentially causing port conflicts or state inconsistencies.

## Solution Statement
Create `adw_rebase_iso.py` with a PR-first interface that:
1. **Discovers context from PR**: Takes PR number as primary input, fetches PR details via `gh pr view`
2. **Locates ADW state**: Finds the associated ADW state by matching branch patterns or uses provided adw-id
3. **Validates isolation**: Ensures worktree exists and is properly configured
4. **Performs rebase**: Fetches latest origin/main and attempts rebase in the worktree
5. **Handles conflicts**: Detects conflicts and provides detailed reporting with file paths
6. **Auto-updates PR**: Force-pushes rebased branch to automatically update the PR
7. **Maintains observability**: Posts progress to linked issue and logs all operations

The workflow operates entirely within the isolated worktree, preserving the ADW isolation model and avoiding conflicts with the main repository or other ADWs.

## Relevant Files

### Existing Workflows (Reference Patterns)
- `adws/adw_ship_iso.py` - Manual merge workflow, demonstrates state validation and git operations in main repo
- `adws/adw_patch_iso.py` - Issue-driven workflow, demonstrates worktree operations and finalize_git_operations pattern

### Core Modules (Dependencies)
- `adws/adw_modules/state.py` - ADWState management for loading/saving workflow state
- `adws/adw_modules/git_ops.py` - Git operations including push_branch, get_current_branch, finalize_git_operations
- `adws/adw_modules/github.py` - GitHub operations including fetch_issue, make_issue_comment, get_repo_url
- `adws/adw_modules/worktree_ops.py` - Worktree validation and port management
- `adws/adw_modules/workflow_ops.py` - Workflow utilities including format_issue_message
- `adws/adw_modules/utils.py` - Logging and environment validation
- `adws/adw_modules/data_types.py` - Type definitions for ADWStateData

### New Files
- `adws/adw_rebase_iso.py` - Main rebase workflow script (new implementation)
- `adws/manifests/adw_rebase_iso.yaml` - Workflow manifest describing dependencies and validation

## Implementation Plan

### Phase 1: Foundation
Set up the rebase workflow structure following ADW patterns established in `adw_ship_iso.py` and `adw_patch_iso.py`. This includes:
- Creating the uv script shebang and dependencies
- Importing required modules (state, git_ops, github, worktree_ops, workflow_ops, utils, data_types)
- Setting up Click CLI with PR number as primary argument, optional adw-id, and --dry-run flag
- Establishing agent name constants for notifications (AGENT_REBASER)

### Phase 2: Core Implementation
Implement the PR-first resolution logic with state discovery:
1. **PR Resolution**: Fetch PR details using `gh pr view <pr-number> --json headRefName,number,title,state`
2. **State Discovery**: Find ADW state by either:
   - Using provided adw-id directly
   - Scanning `agents/*/adw_state.json` files to match branch_name with PR's headRefName
3. **Worktree Validation**: Use `validate_worktree()` to ensure isolated environment exists
4. **Rebase Operations**:
   - Fetch latest origin/main in the worktree
   - Detect current divergence with `git log --oneline origin/main..HEAD`
   - Attempt `git rebase origin/main` in the worktree
   - Capture conflict files if rebase fails
5. **Conflict Reporting**: Format detailed conflict report with file paths and rebase status
6. **Force Push**: If rebase succeeds, force-push to origin to update PR

### Phase 3: Integration
Integrate with existing ADW infrastructure:
- Post progress updates to linked issue (if issue_number exists in state)
- Update ADW state with rebase timestamp and status
- Append 'adw_rebase_iso' to state's all_adws list
- Create comprehensive manifest file for validation and documentation
- Follow dry-run pattern from `adw_ship_iso.py` for safe testing

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Workflow Script Foundation
- Create `adws/adw_rebase_iso.py` with uv shebang and dependencies header
- Add dependencies: `python-dotenv`, `pydantic`, `click`, `rich`
- Write comprehensive module docstring with usage examples
- Import all required modules (state, git_ops, github, worktree_ops, workflow_ops, utils, data_types)
- Define agent name constant: `AGENT_REBASER = "rebaser"`
- Set up Click command decorator with arguments: `pr_number` (required), `adw_id` (optional), `--dry-run` (flag)

### 2. Implement PR Resolution Function
- Create `fetch_pr_details(pr_number: str, logger: logging.Logger) -> Tuple[Dict[str, Any], Optional[str]]`
- Use `gh pr view <pr-number> --json headRefName,number,title,state,url` to fetch PR data
- Return tuple of (pr_data_dict, error_message)
- Handle errors: PR not found, gh CLI not installed, network issues
- Log PR details for observability

### 3. Implement State Discovery Function
- Create `find_adw_state_by_branch(branch_name: str, logger: logging.Logger) -> Optional[Tuple[str, ADWState]]`
- Scan `agents/*/adw_state.json` files in the project root
- Match branch_name field in state files with PR's headRefName
- Return tuple of (adw_id, loaded_state) if found, None otherwise
- Log discovery process for debugging

### 4. Implement Conflict Detection Function
- Create `detect_rebase_conflicts(worktree_path: str, logger: logging.Logger) -> Tuple[bool, List[str]]`
- Fetch latest origin/main: `git fetch origin main` (in worktree)
- Check for divergence: `git log --oneline origin/main..HEAD` (in worktree)
- Return tuple of (has_divergence, list_of_conflicting_commits)
- Include commit hashes and messages for context

### 5. Implement Rebase Operation Function
- Create `rebase_onto_main(worktree_path: str, logger: logging.Logger, dry_run: bool = False) -> Tuple[bool, Optional[str], List[str]]`
- If dry_run: log what would happen and return success
- Execute `git rebase origin/main` in the worktree
- Capture rebase output and any conflict markers
- If conflicts: parse conflict files from git status
- Return tuple of (success, error_message, conflict_files_list)
- Include detailed logging for each step

### 6. Implement Main Workflow Logic
- Load environment variables with `load_dotenv()`
- Handle --dry-run early exit with validation logging
- Fetch PR details using `fetch_pr_details()`
- Extract branch_name from PR data (headRefName field)
- Find ADW state: use provided adw_id or discover via `find_adw_state_by_branch()`
- Exit with error if no state found
- Validate state has required fields (worktree_path, branch_name)
- Set up logger with `setup_logger(adw_id, "adw_rebase_iso")`
- Validate environment with `check_env_vars()`

### 7. Implement Worktree Validation and Rebase
- Use `validate_worktree(adw_id, state)` to ensure worktree exists
- Exit with error if worktree validation fails
- Post initial status to issue: "🔄 Starting rebase workflow"
- Detect conflicts with `detect_rebase_conflicts()`
- Log divergence details (commits ahead/behind)
- Attempt rebase with `rebase_onto_main()`
- Handle three outcomes:
  - Success: continue to push
  - Conflicts: report files and exit with instructions
  - Error: report error and exit

### 8. Implement Conflict Reporting
- Create detailed conflict report format:
  - List of conflicting files with full paths
  - Rebase status and error message
  - Suggestion to resolve manually or use agent assistance
- Post conflict report to issue if applicable
- Log conflict details for debugging
- Exit with clear error message and non-zero status code

### 9. Implement Force Push and PR Update
- If rebase succeeds, force-push branch: `git push origin <branch> --force` (in worktree)
- Verify PR updates automatically (same branch, GitHub updates PR)
- Post success message to issue: "✅ Rebased onto main and force-pushed"
- Include PR URL in success message for easy access
- Update state with rebase timestamp

### 10. Implement State Updates and Finalization
- Append 'adw_rebase_iso' to state.all_adws list
- Save state with `state.save("adw_rebase_iso")`
- Post final state summary to issue if applicable
- Log completion message
- Use Rich console for colorized output

### 11. Create Workflow Manifest
- Create `adws/manifests/adw_rebase_iso.yaml` following the pattern from `adw_ship_iso.yaml`
- Define workflow metadata: name, description, category (composite)
- List effects: `creates_worktree: false`, `posts_github: true`, `modifies_git: true`, `pushes_remote: true`
- Document module dependencies (all adw_modules imports)
- List required env vars: ANTHROPIC_API_KEY (if using agents), GITHUB_TOKEN
- Define validation commands:
  - Import test: `python -c "import adws.adw_rebase_iso"`
  - CLI test: `--help` flag
  - Dry run: `2 --dry-run`
- Document arguments: pr_number (required), adw_id (optional), --dry-run (flag)
- List workflow dependencies: none (can run independently when conflicts detected)

### 12. Add Error Handling and Edge Cases
- Handle PR not found error with clear message
- Handle state not found error (no matching branch)
- Handle worktree missing error with recovery suggestion
- Handle git command failures with stderr output
- Handle network failures for GitHub operations
- Handle permission issues for git operations
- Add timeout handling for long-running operations
- Include retry logic for network operations

### 13. Add Logging and Observability
- Log all PR resolution steps
- Log state discovery process
- Log worktree validation checks
- Log each git operation with command and output
- Log conflict detection results
- Log rebase progress and outcome
- Use Rich console for user-facing output with colors
- Post progress updates to issue at key milestones

## Testing Strategy

### Unit Tests
- **PR Resolution**: Test `fetch_pr_details()` with valid/invalid PR numbers
- **State Discovery**: Test `find_adw_state_by_branch()` with existing/non-existing branches
- **Conflict Detection**: Test `detect_rebase_conflicts()` with clean/diverged branches
- **Rebase Operations**: Test `rebase_onto_main()` with various conflict scenarios
- **Dry Run**: Test all functions in dry-run mode to ensure no side effects

### Integration Tests
- **Full Workflow with Clean Rebase**: Test with a branch that rebases cleanly onto main
- **Full Workflow with Conflicts**: Test with a branch that has merge conflicts
- **PR-First Flow**: Test providing only PR number (auto-discovers state)
- **Direct State Flow**: Test providing both PR number and adw-id
- **Missing State**: Test with PR that has no associated ADW state
- **Invalid Worktree**: Test with state that has missing/corrupted worktree

### Edge Cases
- **PR from fork**: Handle PRs from forked repositories
- **Protected branch**: Handle force-push restrictions on protected branches
- **Already rebased**: Handle branch that's already up-to-date with main
- **Multiple states**: Handle multiple ADW states matching the same branch
- **Detached HEAD**: Handle worktree in detached HEAD state
- **Merge commits**: Handle branches with merge commits (not just rebases)
- **Empty PR**: Handle PR with no commits
- **Closed PR**: Handle attempting to rebase a closed/merged PR

## Acceptance Criteria
- [x] Script uses uv shebang with correct dependencies
- [x] Primary argument is PR number (required)
- [x] Optional adw-id argument for direct state lookup
- [x] --dry-run flag validates without executing operations
- [x] Fetches PR details via `gh pr view` command
- [x] Auto-discovers ADW state by matching branch name
- [x] Falls back to provided adw-id if state discovery fails
- [x] Validates worktree exists and is properly configured
- [x] Detects divergence from origin/main
- [x] Attempts rebase onto origin/main in worktree
- [x] Reports conflict files with full paths if rebase fails
- [x] Force-pushes rebased branch to update PR if rebase succeeds
- [x] Posts progress updates to linked issue (if available)
- [x] Updates ADW state with rebase status
- [x] Appends workflow ID to state.all_adws list
- [x] Creates comprehensive manifest file
- [x] Handles errors gracefully with clear messages
- [x] Uses Rich console for colorized output
- [x] Logs all operations for observability
- [x] Follows existing ADW patterns and conventions

## Validation Commands
Execute these commands to validate the feature is complete:

```bash
# 1. Test Python imports
uv run python -c "import sys; sys.path.insert(0, 'adws'); from adw_rebase_iso import *; print('✅ Imports successful')"

# 2. Test help text
uv run adws/adw_rebase_iso.py --help

# 3. Test dry-run mode (with actual PR #2)
uv run adws/adw_rebase_iso.py 2 --dry-run

# 4. Test with PR number only (auto-discovers state)
uv run adws/adw_rebase_iso.py 2

# 5. Test with PR number and explicit adw-id
uv run adws/adw_rebase_iso.py 2 a6edbc74

# 6. Verify manifest exists and is valid YAML
uv run python -c "import yaml; yaml.safe_load(open('adws/manifests/adw_rebase_iso.yaml')); print('✅ Manifest valid')"

# 7. Test state discovery function independently
uv run python -c "import sys; sys.path.insert(0, 'adws'); from adw_rebase_iso import find_adw_state_by_branch; from adws.adw_modules.utils import setup_logger; logger = setup_logger('test', 'test'); result = find_adw_state_by_branch('chore-issue-1-adw-a6edbc74-enhance-readme-showcase-power', logger); print(f'✅ Found state: {result[0] if result else None}')"

# 8. Verify gh CLI access to PR
gh pr view 2 --json headRefName,number,title,state

# 9. Check worktree exists for ADW a6edbc74
ls -la trees/a6edbc74/ 2>/dev/null || echo "Worktree not found (expected if not created yet)"

# 10. Compile check for Python syntax
uv run python -m py_compile adws/adw_rebase_iso.py
```

## Notes

### Dependencies
- All required dependencies are already in the project (no `uv add` needed)
- Uses existing `gh` CLI for GitHub operations
- Uses existing git for rebase operations

### Force Push Considerations
- Force-push is necessary after rebase to update PR
- Only force-pushes the feature branch (never main)
- Force-push happens in the isolated worktree, not main repo
- GitHub automatically updates the PR when branch is force-pushed

### State Discovery Logic
The workflow prioritizes two methods for finding the ADW state:
1. **Explicit adw-id**: If provided, use it directly (fastest, most reliable)
2. **Branch name matching**: Scan agents/*/adw_state.json to find state with matching branch_name

This approach allows flexibility: users can provide the adw-id if known, or let the workflow discover it automatically from the PR's branch name.

### Isolation Model
The rebase operations happen entirely within the isolated worktree at `trees/<adw_id>/`. This ensures:
- No impact on main repository or other ADWs
- Dedicated ports preserved (backend_port, frontend_port)
- Safe force-push without affecting other developers
- Clean rollback possible (just delete worktree)

### Conflict Resolution Strategy
When conflicts occur, the workflow:
1. Detects conflicts by checking git status for unmerged paths
2. Aborts the rebase to preserve worktree state
3. Reports conflict files to the user/issue
4. Exits with clear instructions for manual or agent-assisted resolution
5. Can be re-run after conflicts are resolved manually

### Future Enhancements
- **Agent-assisted conflict resolution**: Invoke conflict resolver agent when conflicts detected
- **Auto-retry with merge strategy**: Try rebase first, fallback to merge if conflicts
- **Conflict visualization**: Generate diff previews for conflicting sections
- **Batch rebase**: Support rebasing multiple PRs at once
- **Slack/Discord notifications**: Notify team when conflicts require attention
