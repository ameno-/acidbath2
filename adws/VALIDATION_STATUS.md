# ADW Validation Status

Last updated: 2025-12-05 16:31:49

This file tracks the validation status of all ADW scripts in Jerry. Each ADW is validated through 4 levels:
- **Deps**: Do all required slash command dependencies exist? (Level 0)
- **Import**: Can the module be imported without errors? (Level 1)
- **CLI**: Does `--help` work correctly? (Level 2)
- **Dry-Run**: Does `--dry-run` complete without side effects? (Level 3)

| ADW | Deps | Import | CLI | Dry-Run | Status |
|-----|------|--------|-----|---------|--------|
| adw_prompt | SKIP | PASS | PASS | N/A | Ready |
| adw_slash_command | SKIP | PASS | PASS | N/A | Ready |
| adw_chore_implement | SKIP | PASS | PASS | N/A | Ready |
| adw_import_workflow | SKIP | PASS | PASS | N/A | Ready |
| workflow_ops | PASS | PASS | SKIP | SKIP | Ready |
| worktree_ops | SKIP | PASS | PASS | PASS | Ready |
| adw_plan_iso | PASS | PASS | SKIP | PASS | Ready |
| adw_build_iso | PASS | PASS | SKIP | PASS | Ready |
| adw_plan_build_iso | SKIP | PASS | SKIP | PASS | Ready |
| adw_patch_iso | PASS | PASS | SKIP | PASS | Ready |
| adw_ship_iso | PASS | PASS | PASS | PASS | Ready |
| adw_rebase_iso | SKIP | PASS | PASS | PASS | Ready |
| trigger_github | SKIP | SKIP | SKIP | SKIP | Ready |

## Validation Levels

### Level 0: Dependencies Test
Validates that all slash command dependencies declared in the manifest exist in `.claude/commands/`.

```bash
# Check if all declared slash_command_dependencies exist
for cmd in $(yq '.slash_command_dependencies[]' adws/manifests/ADW_NAME.yaml); do
  test -f .claude/commands/${cmd}.md || echo "Missing: $cmd"
done
```

### Level 1: Import Test
Tests that the Python module can be imported without syntax errors or missing dependencies.

```bash
python3 -c "from adws.adw_NAME import main; print('OK')"
```

### Level 2: CLI Test
Tests that the script's CLI is properly configured and responds to `--help`.

```bash
uv run adws/adw_NAME.py --help
```

### Level 3: Dry-Run Test
For ADWs with major effects (creates worktrees, makes commits), tests that `--dry-run` works.

```bash
uv run adws/adw_NAME.py --dry-run [test_args]
```

## Status Meanings

- **Ready**: All enabled validation levels passed
- **Needs Fix**: One or more validation levels failed
- **N/A**: Level not applicable (e.g., no dry-run for utility scripts)
- **SKIP**: Level skipped per manifest configuration
| r2_uploader | PASS | SKIP | SKIP | Ready |
| adw_review_iso | PASS | PASS | SKIP | Ready |
