# Mark Step In Progress

Claim a step before starting work. Updates step status from PENDING or BLOCKED to IN_PROGRESS.

## Variables
spec_file: $1
step_id: $2
adw_id: $3

## Instructions

1. Read the spec file at `$1`
2. Find Step `$2` in the spec
3. Update the step status marker:
   - From `[ ]` (pending) to `[🟡, $3]` (in progress)
   - From `[⏰]` (blocked) to `[🟡, $3]` (in progress)
4. Save the updated spec file

## Status Markers

| Marker | Status | Meaning |
|--------|--------|---------|
| `[ ]` | PENDING | Ready to run |
| `[⏰]` | BLOCKED | Waiting on dependencies |
| `[🟡, adw_id]` | IN_PROGRESS | Agent working |
| `[✅ commit, adw_id]` | COMPLETED | Success |
| `[❌, adw_id]` | FAILED | Error |

## Report

- Confirm step `$2` was marked in progress with ADW ID `$3`
- Report any issues (step not found, already in progress, etc.)
