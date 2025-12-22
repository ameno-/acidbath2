# Import Workflow

Import a file from a sibling directory into Jerry's agentic layer, with optional adaptation.

## Variables
source_path: $1
mode: $2
target_path: $3

## Instructions

This command imports files from sibling directories (like `tac8_app5__nlq_to_sql_aea`) into Jerry's codebase. It is Jerry's **self-improvement mechanism**.

### Arguments

1. `source_path` (required): Absolute path to the source file
2. `mode` (optional, default: "copy"): Adaptation mode
   - `copy` - Verbatim copy, only update relative imports
   - `adapt` - Generalize, remove app-specific code
   - `merge` - Combine with existing file if present
3. `target_path` (optional): Target path in Jerry (defaults to equivalent path)

### Workflow Steps

1. **Validate Source**: Ensure the source file exists and is readable
2. **Determine Target**: Calculate target path if not provided
3. **Read Source Content**: Load the file content
4. **Apply Adaptation**: Transform based on mode:
   - `copy`: Minimal changes (fix imports only)
   - `adapt`: Remove app-specific code, generalize
   - `merge`: Intelligently combine if target exists
5. **Write Target**: Create/update the target file
6. **Validate Import**: Run Python import test

## Adaptation Rules

### Mode: copy
- Change absolute imports to relative imports where needed
- Keep all functionality intact
- Preserve docstrings and comments

### Mode: adapt
- Remove app-specific types and functions
- Generalize hardcoded values (issue types, endpoints, etc.)
- Remove app-specific environment variables
- Add extensibility hooks (metadata fields)
- Update docstrings to be deployment-agnostic

### Mode: merge
- Read existing target file if present
- Preserve unique functionality from both files
- Resolve import conflicts
- Prefer Jerry's existing implementation for overlapping code

## Target Path Calculation

If `target_path` is not provided, derive it from `source_path`:
- `/path/to/tac8_app5__nlq_to_sql_aea/adws/module.py` -> `/Users/ameno/dev/tac/tac-8/jerry/adws/module.py`
- `/path/to/app2/.claude/commands/cmd.md` -> `/Users/ameno/dev/tac/tac-8/jerry/.claude/commands/cmd.md`

## 3-Level Validation

After writing the target file, run validation levels:

### Level 1: Import Test (Always)
```bash
python3 -c "import sys; sys.path.insert(0, '.'); from adws.adw_MODULE import main; print('OK')"
```

### Level 2: CLI Test (Always)
```bash
uv run adws/adw_MODULE.py --help
```

### Level 3: Dry-Run Test (If ADW has major effects)
```bash
uv run adws/adw_MODULE.py --dry-run [test_args]
```

## Dry-Run Pattern for Major-Effect ADWs

When importing ADWs with major effects (creates worktrees, branches, commits), add a `--dry-run` flag:

```python
@click.option("--dry-run", is_flag=True, help="Validate without executing")
def main(issue_number: int, dry_run: bool = False):
    # Parse and validate inputs...
    if dry_run:
        console.print("[yellow]DRY RUN[/yellow] - Would create worktree, branch, etc.")
        return
    # Actual execution...
```

## Manifest Generation

For each imported ADW, generate a manifest at `adws/manifests/<name>.test.yaml`:

```yaml
name: adw_example
description: Example workflow
category: utility  # planning, building, testing, composite, utility
effects:
  creates_worktree: false
  posts_github: false
module_dependencies:
  - adw_modules.agent
env_vars:
  required: [ANTHROPIC_API_KEY]
validation:
  import_test: {enabled: true, timeout: 30}
  cli_test: {enabled: true, command: "--help"}
  dry_run: {enabled: false}
```

## Output Format

Return a JSON report:

```json
{
  "source": "<source_path>",
  "target": "<target_path>",
  "mode": "<mode>",
  "status": "success|failed",
  "validation": {
    "level_1": "passed|failed",
    "level_2": "passed|failed|skipped",
    "level_3": "passed|failed|skipped",
    "overall": "passed|failed"
  },
  "changes": ["<list of changes made>"],
  "error": "<error message if failed>"
}
```

## Task

Import the file from `$1` using mode `$2` (default: copy) to target `$3` (or derived path).

1. Read the source file
2. Apply the appropriate transformation based on mode
3. If mode is "adapt" and source has major effects, add `--dry-run` flag
4. Write to target location
5. Run 3-level validation
6. Return the JSON report
