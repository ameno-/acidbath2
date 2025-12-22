---
allowed-tools: Bash, Read, Write, Task
description: Generate execution metaplan from a feature tracking document
---

# Generate Metaplan

Generate a structured execution metaplan for a multi-phase feature.

## Arguments

$ARGUMENTS should be a path to a feature tracking document (e.g., `specs/FEATURE_NAME.md`)

## Workflow Position

```
1. adw_plan_iso.py (per phase) → Individual specs
2. /metaplan                   → Aggregated metaplan  ← THIS COMMAND
3. feature-orchestrator agent  → Execution
```

## Execution

```bash
uv run ./adws/adw_metaplan_iso.py $ARGUMENTS
```

## What Gets Generated

A `*_METAPLAN.md` file containing:
- Phases table with ADW IDs, worktrees, branches
- Execution order with dependency graph
- Build commands per phase
- Test checklists per phase
- Review criteria per phase
- Commit message templates
- Final validation commands
- Status tracking table

## Next Steps

After generating the metaplan:
1. Review the generated metaplan
2. Execute with: `Use feature-orchestrator agent with [metaplan-path]`
