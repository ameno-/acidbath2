---
description: Claude-assisted Jerry bootstrap - export and install Jerry into a target project
allowed-tools: Read, Bash, Write, Edit, Glob, Grep
---

# Jerry Bootstrap Assistant

You are helping the user install Jerry into a target project: **$ARGUMENTS**

## Important Documentation

Before starting, read the comprehensive bootstrap guide:
- `/docs/BOOTSTRAP.md` - Full specification with parallel phases, state tracking, and validation

## First: Check for Existing Import State

1. Parse the target path from $ARGUMENTS
2. Check if `<target>/.jerry/import_state.json` exists
3. If exists, read it and offer to:
   - **Resume** from the last incomplete phase
   - **Restart** from the beginning
4. If not exists, start a fresh import

## 5-Phase Parallel Import Process

Execute these phases, tracking state in `import_state.json`:

### Phase 1: PREREQS (run checks in parallel)

Check all prerequisites concurrently:
```bash
python3 --version  # Must be 3.11+
uv --version       # Must be installed
git --version      # Must be 2.0+
claude --version   # Must be installed
```

**State update**: Mark each check as completed/failed in `phases.prereqs.checks`

If any required check fails, stop and provide installation instructions.

### Phase 2: SETUP (run in parallel)

Execute concurrently:
1. **Export Jerry**: `./adws/jerry_export.py --output /tmp/jerry-export`
2. **Verify/create target**: Check target directory exists, create if needed

**State update**: Mark in `phases.setup.tasks`

### Phase 3: INSTALL (pipeline + parallel)

1. First, extract the archive:
   ```bash
   ./jerry_bootstrap.sh --source /tmp/jerry-export/jerry-export-*.tar.gz --target <target> --skip-validation
   ```

2. Then in parallel:
   - Verify Python dependencies installed
   - Verify directories created: `agents/`, `trees/`, `specs/`, `ai_docs/`
   - Verify templates copied from `.jerry/templates/`

**State update**: Mark in `phases.install.tasks`

### Phase 4: CONFIGURE (sequential - requires user input)

This phase may pause for user input:

1. Check if `.env` exists in target
2. If not, copy from template:
   ```bash
   cp .jerry/templates/env.template .env
   ```
3. Check if `ANTHROPIC_API_KEY` is set:
   ```bash
   grep -q "ANTHROPIC_API_KEY=" .env && grep "ANTHROPIC_API_KEY=" .env | grep -v "your-"
   ```
4. If not set, inform user they need to:
   - Edit `.env` and add their `ANTHROPIC_API_KEY`
   - Tell user to run `/bootstrap <target> --resume` after configuring

**State update**: Mark `phases.configure.status` and add `notes` if paused

### Phase 5: VALIDATE (tiered parallelism)

Run validation in order, with L1+L2 in parallel:

1. Run Level 1 and Level 2 in parallel:
   ```bash
   ./adws/jerry_validate.py --level 1
   ./adws/jerry_validate.py --level 2
   ```

2. If both pass, run Level 3:
   ```bash
   ./adws/jerry_validate.py --level 3
   ```

3. If L3 passes, run Level 4 (REQUIRED - ~5 minutes):
   ```bash
   ./adws/jerry_validate.py --level 4
   ```

4. Run smoke test:
   ```bash
   ./adws/adw_prompt.py "echo 'Jerry bootstrap complete!'"
   ```

**State update**: Mark each level in `phases.validate`

## State File Management

After each phase/step, update the import state file:

```bash
# Location
<target>/.jerry/import_state.json
```

Create/update with structure:
```json
{
  "import_id": "<8-char-random-id>",
  "started_at": "<ISO-timestamp>",
  "source_repo": "<path-to-jerry-source>",
  "target_repo": "<target-path>",
  "current_phase": "<phase-name>",
  "phases": {
    "prereqs": { "status": "...", "checks": {...} },
    "setup": { "status": "...", "tasks": {...} },
    "install": { "status": "...", "tasks": {...} },
    "configure": { "status": "...", "notes": "..." },
    "validate": { "status": "...", "levels": {...} }
  },
  "last_updated": "<ISO-timestamp>"
}
```

## Error Handling

If any step fails:
1. Mark the step as `"status": "failed"` with error details
2. Save the state file
3. Explain what went wrong
4. Suggest fixes based on the error type:
   - **Prerequisites**: Provide installation commands
   - **Export**: Check Jerry source repo is valid
   - **Install**: Check permissions, disk space
   - **Configure**: Remind user about API keys
   - **Validate**: Check validation report for details

## Resume Handling

When `--resume` is specified or state file exists:
1. Read the state file
2. Find the first phase with status not "completed"
3. Start from that phase
4. Skip all completed phases/steps

## Completion Message

When all phases complete successfully:

```
Jerry Bootstrap Complete!

Target: <target-path>
Duration: <elapsed-time>

Next steps:
1. cd <target-path>
2. source .env
3. ./adws/adw_slash_command.py /prime
4. Start building with: ./adws/adw_plan_iso.py "Your feature"

Documentation: docs/BOOTSTRAP.md
```

## Requirements

- **Level 4 validation is REQUIRED** - do not skip
- **State must be saved** after every phase
- **Parallel execution** should be used where possible for efficiency
