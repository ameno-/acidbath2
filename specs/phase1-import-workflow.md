# Phase 1: Import Workflow Specification

## Overview

Create Jerry's **self-improvement mechanism** - a workflow that can import other workflows from sibling directories. This is the meta-artifact that enables Jerry to bootstrap itself.

## Components to Create

### 1. `/import_workflow.md` - Slash Command

**Location**: `/Users/ameno/dev/tac/tac-8/jerry/.claude/commands/import_workflow.md`

**Arguments**:
- `$1`: Source file path (required) - absolute path to file in sibling directory
- `$2`: Adaptation mode (optional, default: "copy")
  - `copy` - Verbatim copy, only update imports
  - `adapt` - Generalize, remove app-specific code
  - `merge` - Combine with existing file if present
- `$3`: Target path (optional) - defaults to equivalent path in jerry

**Behavior**:
1. Read source file
2. Apply adaptation based on mode:
   - `copy`: Update relative imports only
   - `adapt`: Remove app-specific code, generalize patterns
   - `merge`: Intelligently combine with existing file
3. Write to target path
4. Run validation import test
5. Report success/failure

### 2. `adw_import_workflow.py` - ADW Script

**Location**: `/Users/ameno/dev/tac/tac-8/jerry/adws/adw_import_workflow.py`

**CLI Arguments**:
```bash
./adws/adw_import_workflow.py <source_path> [--mode copy|adapt|merge] [--target <path>] [--phase <name>]
```

**Features**:
- Uses `execute_template()` to call `/import_workflow` slash command
- Retry logic: 3 attempts with exponential backoff (1s, 3s, 5s)
- State tracking via `ADWState` for resume capability
- Validation: Python import test after each file
- Error classification: retryable vs blocking
- Phase report generation

**Workflow Steps**:
1. Parse CLI arguments
2. Create/load ADWState
3. Execute `/import_workflow` with retry logic
4. Validate import with Python test
5. Update state with result
6. Generate phase report if `--phase` provided

## Implementation Details

### Retry Logic

```python
retry_delays = [1, 3, 5]  # seconds
max_retries = 3

for attempt in range(max_retries + 1):
    response = execute_template(request)
    if response.success:
        break
    if attempt < max_retries:
        time.sleep(retry_delays[attempt])
```

### Validation

After import, run:
```bash
uv run python3 -c "from adws.adw_modules.MODULE import *; print('OK')"
```

### State Schema

```json
{
  "adw_id": "abc12345",
  "phase": "import",
  "imports": [
    {
      "source": "/path/to/source.py",
      "target": "/path/to/target.py",
      "mode": "adapt",
      "status": "success|failed|pending",
      "attempts": 1,
      "validation": "passed|failed"
    }
  ],
  "metadata": {
    "phase_name": "meta_foundation"
  }
}
```

### Error Handling

- **Retryable Errors**: Claude Code timeouts, execution errors
- **Blocking Errors**: Source file not found, syntax errors after import
- **Report Context**: File path, line number, error type

## Acceptance Criteria

1. `/import_workflow.md` accepts source path and mode
2. `adw_import_workflow.py` executes with retry logic
3. Validation runs after each import
4. State persists to `agents/{adw_id}/adw_state.json`
5. Failed imports don't block subsequent imports
6. Phase report generated with results

## Usage Examples

```bash
# Copy a module verbatim
./adws/adw_import_workflow.py /Users/ameno/dev/tac/tac-8/tac8_app5__nlq_to_sql_aea/adws/adw_modules/workflow_ops.py --mode copy

# Adapt a module (generalize)
./adws/adw_import_workflow.py /path/to/sibling/module.py --mode adapt

# Import with phase reporting
./adws/adw_import_workflow.py /path/to/file.py --phase meta_orchestration
```
