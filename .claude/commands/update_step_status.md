# Update Step Status

Report step completion (success or failure). Updates step from IN_PROGRESS to COMPLETED or FAILED.

## Variables
spec_file: $1
step_id: $2
status: $3
result: $4

## Instructions

1. Read the spec file at `$1`
2. Find Step `$2` in the spec
3. Update the step status marker based on `$3`:
   - If `$3` is "success": `[🟡, adw_id]` → `[✅ $4, adw_id]` where $4 is commit hash
   - If `$3` is "failed": `[🟡, adw_id]` → `[❌, adw_id] // Failed: $4` where $4 is error message
4. Save the updated spec file

## Status Markers

| Marker | Status | Meaning |
|--------|--------|---------|
| `[🟡, adw_id]` | IN_PROGRESS | Agent working |
| `[✅ commit, adw_id]` | COMPLETED | Success with commit hash |
| `[❌, adw_id] // Failed: msg` | FAILED | Error with message |

## Report

- Confirm step `$2` status updated to `$3`
- Include result details (`$4`)
