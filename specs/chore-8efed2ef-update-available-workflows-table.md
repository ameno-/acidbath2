# Chore: Update Available Workflows Section in Documentation

## Metadata
adw_id: `8efed2ef`
prompt: `ensure adws#available-workflows section in documentation is accurate based on most recent run results`

## Chore Description
Update the "Available Workflows" table in `/Users/ameno/dev/tac/tac-8/jerry/adws/README.md` to accurately reflect the current validation status of all ADW scripts based on the most recent validation results in `VALIDATION_STATUS.md`. The table currently shows outdated validation statuses (several workflows marked as "Needs Fix" are now "Ready").

## Relevant Files
Use these files to complete the chore:

- `/Users/ameno/dev/tac/tac-8/jerry/adws/README.md` - Main ADWs documentation with the "Available Workflows" table to be updated (lines 16-34)
- `/Users/ameno/dev/tac/tac-8/jerry/adws/VALIDATION_STATUS.md` - Source of truth for current validation results (last updated 2025-12-04)
- `/Users/ameno/dev/tac/tac-8/jerry/adws/manifests/*.yaml` - Manifest files containing ADW descriptions and categories

### New Files
None - only updating existing documentation.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Analyze Current vs Expected State
- Read the current "Available Workflows" table in `adws/README.md` (lines 18-34 in the ADW-LIST markers)
- Read the validation status from `adws/VALIDATION_STATUS.md` (lines 10-23)
- Identify discrepancies:
  - Missing workflows: `adw_sdk_prompt` (exists in codebase but not in table)
  - Incorrect statuses: All workflows currently showing "Needs Fix" are actually "Ready" per VALIDATION_STATUS.md
  - Missing workflows: `adw_slash_command` (exists but not in the table)

### 2. Gather ADW Metadata
- For `adw_sdk_prompt`: Check if manifest exists, else extract description from script docstring
- For `adw_slash_command`: Verify manifest exists (`adws/manifests/adw_slash_command.test.yaml` does NOT exist, need to get from script)
- For `adw_fix_validation`: Verify manifest description matches table entry
- Confirm categories for each ADW from manifests or infer from naming

### 3. Update the Available Workflows Table
- Replace the content between `<!-- ADW-LIST-START -->` and `<!-- ADW-LIST-END -->` markers
- Include ALL 13 ADW workflows in this order:
  1. **Utility workflows**: adw_prompt, adw_sdk_prompt, adw_slash_command, adw_import_workflow, adw_fix_validation, workflow_ops, worktree_ops, trigger_github
  2. **Planning workflows**: adw_plan_iso
  3. **Building workflows**: adw_build_iso
  4. **Composite workflows**: adw_chore_implement, adw_plan_build_iso, adw_patch_iso, adw_ship_iso
- Update validation status column based on VALIDATION_STATUS.md (all should be "Ready")
- Ensure descriptions are accurate and consistent with manifests

### 4. Verify Table Format
- Ensure markdown table syntax is correct
- Verify all 4 columns are present: ADW | Category | Description | Validation
- Ensure alignment is consistent
- Check that the comment markers `<!-- ADW-LIST-START -->` and `<!-- ADW-LIST-END -->` remain intact

### 5. Validate Documentation Accuracy
- Cross-reference each ADW entry with:
  - Script existence in `adws/*.py`
  - Manifest existence in `adws/manifests/*.yaml`
  - Validation results in `VALIDATION_STATUS.md`
- Ensure no ADW is missing from the table
- Verify descriptions are concise and informative

## Validation Commands
Execute these commands to validate the chore is complete:

- `grep -A 20 "Available Workflows" /Users/ameno/dev/tac/tac-8/jerry/adws/README.md` - Verify table is updated and formatted correctly
- `diff -u <(ls /Users/ameno/dev/tac/tac-8/jerry/adws/adw_*.py | xargs -n1 basename | sed 's/.py$//' | sort) <(grep -A 20 "ADW-LIST-START" /Users/ameno/dev/tac/tac-8/jerry/adws/README.md | grep "^|" | grep -v "^|--" | grep -v "^| ADW " | awk -F'|' '{print $2}' | tr -d ' ' | sort)` - Ensure all ADW scripts are represented in the table
- `cat /Users/ameno/dev/tac/tac-8/jerry/adws/VALIDATION_STATUS.md` - Confirm validation statuses match source of truth

## Notes
- The `VALIDATION_STATUS.md` file shows that ALL ADWs are now passing their validation tests (status: "Ready")
- The table previously showed several "Needs Fix" statuses that are now outdated
- `adw_sdk_prompt` exists as a Python script but is missing from the table entirely
- The table structure uses HTML comment markers for automated updates in future
- Two modules are listed: `workflow_ops` and `worktree_ops` - these are utility modules, not executable ADWs, but should remain in the table per current structure
- Validation statuses in VALIDATION_STATUS.md:
  - All workflows show "Ready" status
  - Some have SKIP levels which is expected (e.g., workflow_ops has CLI and Dry-Run skipped as it's a module)
  - This reflects successful validation runs as of 2025-12-04
