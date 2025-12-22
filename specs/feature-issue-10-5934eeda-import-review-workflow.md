# Feature: Import Review Workflow from Legacy Application

## Metadata
adw_id: `5934eeda`
prompt: `{"number": "10", "title": "Import review workflow", "body": "\nadw_plan_build_iso\nadw_import_workflow\n\nImport this workflow from. a legacy app. Make sure it passes validation and documentation is updated after implementation\n\npath: \"legacy/tac8_app5__nlq_to_sql_aea/adws/adw_review_iso.py\"\nmode: merge\n"}`

## Feature Description
Import the `adw_review_iso.py` workflow from the legacy application (`legacy/tac8_app5__nlq_to_sql_aea/adws/`) into Jerry's agentic layer. This workflow provides automated code review capabilities with screenshot capture, issue detection, and automated resolution. The import will use merge mode to intelligently adapt the legacy code to Jerry's patterns while preserving core functionality. After import, the workflow must pass validation tests and documentation must be updated.

## User Story
As a Jerry developer
I want to import the review workflow from the legacy application
So that Jerry can automatically review implementations against specifications, capture screenshots, detect issues, and optionally auto-resolve blocker issues

## Problem Statement
Jerry currently lacks an automated review workflow that can:
- Review implementations against specifications in isolated worktrees
- Capture screenshots of critical functionality for documentation
- Detect and classify issues (blocker, tech_debt, skippable)
- Automatically create and implement patches for blocker issues
- Upload screenshots to R2 storage for GitHub PR comments
- Retry reviews after resolving blockers

The legacy application has a mature `adw_review_iso.py` that provides all these capabilities, but it needs to be adapted to Jerry's architecture.

## Solution Statement
Use Jerry's `adw_import_workflow.py` utility to import the review workflow with merge mode adaptation. The import will:
1. Copy the core review logic from legacy app
2. Adapt code to match Jerry's existing patterns (state management, git ops, workflow ops)
3. Ensure all dependencies are available in Jerry's module structure
4. Generate or update validation manifests
5. Run 3-level validation (import → CLI → dry-run)
6. Update Jerry's README and VALIDATION_STATUS.md

The imported workflow will integrate seamlessly with existing isolated workflows (`adw_plan_iso`, `adw_build_iso`) and composite workflows (`adw_plan_build_iso`).

## Relevant Files

**Legacy Source:**
- `legacy/tac8_app5__nlq_to_sql_aea/adws/adw_review_iso.py` - Source workflow to import (535 lines, contains main review orchestration)

**Target Location:**
- `adws/adw_review_iso.py` - Target location for imported workflow

**Dependencies to Verify:**
- `adws/adw_modules/state.py` - ADW state management (used by review workflow)
- `adws/adw_modules/git_ops.py` - Git operations (commit, push)
- `adws/adw_modules/github.py` - GitHub integration (fetch_issue, make_issue_comment, get_repo_url)
- `adws/adw_modules/workflow_ops.py` - Workflow operations (create_commit, format_issue_message, implement_plan, find_spec_file)
- `adws/adw_modules/utils.py` - Utilities (setup_logger, parse_json, check_env_vars)
- `adws/adw_modules/data_types.py` - Data types (AgentTemplateRequest, ReviewResult, ReviewIssue, AgentPromptResponse)
- `adws/adw_modules/agent.py` - Agent execution (execute_template)
- `adws/adw_modules/worktree_ops.py` - Worktree operations (validate_worktree)

**New Module Needed:**
- `adws/adw_modules/r2_uploader.py` - R2 storage uploader for screenshots (imported from legacy if doesn't exist)

**Slash Command Needed:**
- `.claude/commands/review.md` - Review command template (needs to be created or imported)

**Documentation:**
- `README.md` - Update ADW-LIST section with adw_review_iso entry
- `adws/VALIDATION_STATUS.md` - Update with validation results
- `adws/README.md` - Update ADW list (if exists)

**Validation:**
- `adws/adw_tests/manifests/adw_review_iso.test.yaml` - Validation manifest (create if needed)

## Implementation Plan

### Phase 1: Pre-Import Verification
Verify Jerry's module structure is ready to support the review workflow dependencies. Check for missing modules that need to be imported first.

### Phase 2: Core Import Execution
Use `adw_import_workflow.py` to import the review workflow with merge mode, which will intelligently adapt the code to Jerry's patterns.

### Phase 3: Dependency Resolution
Import or create any missing dependencies identified during validation (R2 uploader, review command template).

### Phase 4: Validation and Documentation
Run 3-level validation and update all documentation to reflect the new workflow.

## Step by Step Tasks

### 1. Verify Pre-Import Dependencies
- Check if `adws/adw_modules/r2_uploader.py` exists in Jerry
- Check if `.claude/commands/review.md` exists in Jerry
- Check if legacy app has these dependencies: `legacy/tac8_app5__nlq_to_sql_aea/adws/adw_modules/r2_uploader.py`
- Check if legacy app has review command: `legacy/tac8_app5__nlq_to_sql_aea/.claude/commands/review.md`
- Document missing dependencies for Phase 3

### 2. Import R2 Uploader Module (if needed)
- If R2 uploader doesn't exist in Jerry, import it first using `adw_import_workflow.py`
- Use copy mode since it's a utility module
- Example: `uv run adws/adw_import_workflow.py legacy/tac8_app5__nlq_to_sql_aea/adws/adw_modules/r2_uploader.py --mode copy --validation-level all`
- Verify import validation passes

### 3. Import Review Command Template (if needed)
- If review command doesn't exist in Jerry, import it from legacy
- Use copy mode for command templates
- Example: `uv run adws/adw_import_workflow.py legacy/tac8_app5__nlq_to_sql_aea/.claude/commands/review.md --mode copy --validation-level 1`
- Verify the command template is valid

### 4. Execute Main Review Workflow Import
- Run import workflow using merge mode for intelligent adaptation
- Command: `uv run adws/adw_import_workflow.py legacy/tac8_app5__nlq_to_sql_aea/adws/adw_review_iso.py --mode merge --validation-level all --update-docs`
- The merge mode will:
  - Analyze the legacy code structure
  - Map legacy imports to Jerry's module structure
  - Adapt function calls to match Jerry's APIs
  - Preserve core review logic and workflow orchestration
  - Maintain data types and agent patterns

### 5. Review Import Output
- Check `agents/{adw_id}/importer/cc_final_object.json` for import results
- Check `agents/{adw_id}/importer/custom_summary_output.json` for high-level summary
- Review the imported file at `adws/adw_review_iso.py`
- Verify all imports are correctly mapped to Jerry's modules
- Check for any manual fixes needed

### 6. Generate or Update Validation Manifest
- If manifest doesn't exist, generate template: `uv run adws/adw_import_workflow.py adws/adw_review_iso.py --generate-manifest`
- Update manifest at `adws/adw_tests/manifests/adw_review_iso.test.yaml` with:
  - Correct CLI arguments for dry-run test
  - Required environment variables
  - Expected success criteria
- Reference existing manifests in `adws/adw_tests/manifests/` for examples

### 7. Run Level 1 Validation (Import Test)
- Command: `uv run python3 -c "from adws.adw_review_iso import *; print('Import successful')"`
- Verify no import errors
- Fix any missing imports or module issues

### 8. Run Level 2 Validation (CLI Test)
- Command: `uv run adws/adw_review_iso.py --help` or `uv run adws/adw_review_iso.py`
- Verify CLI loads without errors
- Check that click/argparse is properly configured

### 9. Run Level 3 Validation (Dry-Run Test)
- Use the manifest's dry_run configuration
- Execute with minimal test data
- Verify workflow can initialize state, validate worktree, and execute review logic
- Check output files are created in `agents/{adw_id}/reviewer/`

### 10. Update README.md ADW List
- Verify `README.md` has ADW-LIST-START and ADW-LIST-END markers
- Add entry: `| adw_review_iso | composite | AI Developer Workflow for agentic review in isolated worktrees | Ready |`
- Update entry if import workflow already added it

### 11. Update VALIDATION_STATUS.md
- Verify `adws/VALIDATION_STATUS.md` exists and is updated
- Check that adw_review_iso entry shows validation results
- Format: `| adw_review_iso | PASS | PASS | PASS | Ready |`

### 12. Update workflow_ops.py AVAILABLE_ADW_WORKFLOWS
- Add "adw_review_iso" to the AVAILABLE_ADW_WORKFLOWS list in `adws/adw_modules/workflow_ops.py`
- This enables runtime validation and webhook triggers

### 13. Test Integration with Existing Workflows
- Create a test issue or use existing issue
- Run plan workflow: `uv run adws/adw_plan_iso.py github:test_issue test_adw_id`
- Run build workflow: `uv run adws/adw_build_iso.py test_issue test_adw_id`
- Run review workflow: `uv run adws/adw_review_iso.py test_issue test_adw_id`
- Verify state is correctly passed between workflows
- Verify worktree isolation works correctly

### 14. Test Review Features End-to-End
- Verify spec file detection from worktree
- Verify review agent execution with `/review` command
- Verify screenshot capture (if enabled)
- Verify issue classification (blocker, tech_debt, skippable)
- Verify blocker resolution loop (if not skipped)
- Verify R2 screenshot upload
- Verify GitHub comment formatting
- Verify commit creation and push

### 15. Create Composite Workflow Variant (Optional)
- Consider creating `adw_plan_build_review_iso.py` composite workflow
- This would chain: plan → build → review in one command
- Update README with composite workflow entry

## Testing Strategy

### Unit Tests
- **Import Validation**: Verify `from adws.adw_review_iso import main` succeeds
- **CLI Validation**: Verify `uv run adws/adw_review_iso.py --help` works
- **Dry-Run Validation**: Verify workflow can execute with minimal test data
- **Module Dependencies**: Verify all imports resolve correctly

### Integration Tests
- **State Management**: Verify workflow loads state from plan/build phases
- **Worktree Operations**: Verify workflow operates in isolated worktree
- **GitHub Integration**: Verify comments are posted correctly
- **Screenshot Upload**: Verify R2 uploader works with test image
- **Git Operations**: Verify commits are created and pushed

### Edge Cases
- **Missing Spec File**: Workflow should error gracefully if spec file not found
- **No Worktree**: Workflow should error if no worktree exists (requires plan first)
- **No Screenshots**: Workflow should work without screenshots
- **Skip Resolution**: `--skip-resolution` flag should prevent blocker patching
- **Max Retry Attempts**: Workflow should stop after MAX_REVIEW_RETRY_ATTEMPTS

## Acceptance Criteria

1. **Import Success**: `adw_import_workflow.py` completes successfully with merge mode
2. **Level 1 Validation**: Python import test passes without errors
3. **Level 2 Validation**: CLI loads and displays usage correctly
4. **Level 3 Validation**: Dry-run test executes review logic successfully
5. **Documentation Updated**: README and VALIDATION_STATUS.md reflect new workflow
6. **Integration Works**: Review workflow integrates with plan and build workflows
7. **Screenshots Work**: Screenshot capture and R2 upload function correctly
8. **Issue Detection Works**: Review correctly identifies and classifies issues
9. **Blocker Resolution Works**: Auto-patching resolves blockers and re-reviews
10. **State Persistence**: Workflow state is correctly saved and loaded

## Validation Commands

Execute these commands to validate the feature is complete:

### 1. Verify Import Success
```bash
# Check import output
cat agents/5934eeda/importer/custom_summary_output.json | jq '.success'

# Verify file exists
ls -lh adws/adw_review_iso.py
```

### 2. Run 3-Level Validation
```bash
# Level 1: Import test
uv run python3 -c "from adws.adw_review_iso import main; print('Level 1 PASS')"

# Level 2: CLI test
uv run adws/adw_review_iso.py --help

# Level 3: Dry-run test (requires manifest configuration)
uv run python3 -m pytest adws/adw_tests/test_agents.py::test_adw_review_iso -v
```

### 3. Verify Documentation Updates
```bash
# Check README has the workflow listed
grep "adw_review_iso" README.md

# Check validation status
cat adws/VALIDATION_STATUS.md | grep "adw_review_iso"

# Check workflow is in available list
grep "adw_review_iso" adws/adw_modules/workflow_ops.py
```

### 4. Integration Test with Full Workflow
```bash
# Create test worktree and run plan → build → review
TEST_ADW_ID=$(uuidgen | cut -d'-' -f1)
uv run adws/adw_plan_iso.py github:10 $TEST_ADW_ID
uv run adws/adw_build_iso.py 10 $TEST_ADW_ID
uv run adws/adw_review_iso.py 10 $TEST_ADW_ID

# Verify review output exists
ls -lh agents/$TEST_ADW_ID/reviewer/
cat agents/$TEST_ADW_ID/reviewer/custom_summary_output.json
```

### 5. Verify Dependencies
```bash
# Check R2 uploader module
uv run python3 -c "from adws.adw_modules.r2_uploader import R2Uploader; print('R2Uploader available')"

# Check review command template
cat .claude/commands/review.md
```

## Notes

### Legacy Code Analysis
The legacy `adw_review_iso.py` contains:
- **533 lines** of Python code with comprehensive review orchestration
- **Review workflow loop** with retry logic (max 3 attempts)
- **Screenshot management** with R2 upload integration
- **Issue classification** (blocker, tech_debt, skippable)
- **Automated patching** for blocker issues
- **State-aware execution** requiring prior plan/build phases
- **Worktree isolation** support throughout

### Key Features to Preserve During Import
1. **Review retry logic**: MAX_REVIEW_RETRY_ATTEMPTS = 3
2. **Screenshot URL generation**: R2 upload and GitHub markdown formatting
3. **Blocker auto-resolution**: Creates patch plans and implements them
4. **State validation**: Validates worktree exists before running
5. **GitHub integration**: Formatted comments with issue classification

### Import Mode Justification
**Merge mode** is chosen because:
- The workflow has significant complexity (533 lines)
- It needs adaptation to Jerry's module structure
- It references multiple Jerry modules that may have different APIs
- Some functions may need to be generalized or simplified
- The agent can intelligently map legacy patterns to Jerry patterns

**Copy mode** would be inappropriate because:
- Direct copy would likely have import errors
- Module paths differ between legacy and Jerry
- Some functions may have different signatures

### Future Enhancements
- **Review configuration file**: YAML config for review criteria
- **Custom review agents**: Allow different review agents per project
- **Review templates**: Pre-defined review checklists
- **Review metrics**: Track review success rates and issue types
- **Parallel review**: Review multiple specs concurrently

### Dependencies Required
If not present in Jerry, these need to be imported first:
- `adws/adw_modules/r2_uploader.py` - For screenshot cloud storage
- `.claude/commands/review.md` - Review slash command template

### Environment Variables Required
The review workflow requires:
- `GITHUB_TOKEN` - For GitHub API access
- R2 storage credentials (via r2_uploader.py):
  - `R2_ACCOUNT_ID`
  - `R2_ACCESS_KEY_ID`
  - `R2_SECRET_ACCESS_KEY`
  - `R2_BUCKET_NAME`

### Validation Manifest Structure
Create `adws/adw_tests/manifests/adw_review_iso.test.yaml`:
```yaml
name: adw_review_iso
category: composite
description: Review implementation against spec in isolated worktree
requires_state: true
requires_worktree: true

tests:
  level_1:
    type: import
    module: adws.adw_review_iso

  level_2:
    type: cli
    command: uv run adws/adw_review_iso.py
    expect_help: true

  level_3:
    type: dry_run
    setup:
      - create test state with worktree
      - create mock spec file
    command: uv run adws/adw_review_iso.py 999 test_adw_id --skip-resolution
    expect_files:
      - agents/test_adw_id/reviewer/cc_final_object.json
```
