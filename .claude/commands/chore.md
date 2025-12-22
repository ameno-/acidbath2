# Chore Planning

Create a plan to complete the chore using the specified markdown `Plan Format`. Research the codebase and create a thorough plan.

## Variables
adw_id: $1
prompt: $2

## Instructions

- If the adw_id or prompt is not provided, stop and ask the user to provide them.
- Create a plan to complete the chore described in the `prompt`
- The plan should be simple, thorough, and precise
- Create the plan in the `specs/` directory with filename: `chore-{adw_id}-{descriptive-name}.md`
  - Replace `{descriptive-name}` with a short, descriptive name based on the chore (e.g., "update-readme", "add-logging", "refactor-agent")
- Research the codebase starting with `README.md`
- Replace every <placeholder> in the `Plan Format` with the requested value

## Codebase Structure

- `README.md` - Project overview and instructions (start here)
- `adws/` - AI Developer Workflow scripts and modules
- `.claude/commands/` - Claude command templates
- `specs/` - Specification and plan documents
- `agents/` - Output directory for agent results
- `trees/` - Worktree directory for isolated development

## Plan Format

```md
# Chore: <chore name>

## Metadata
adw_id: `{adw_id}`
prompt: `{prompt}`

## Chore Description
<describe the chore in detail based on the prompt>

## Relevant Files
Use these files to complete the chore:

<list files relevant to the chore with bullet points explaining why. Include new files to be created under an h3 'New Files' section if needed>

## Step by Step Tasks
IMPORTANT: Execute every step in order, respecting group dependencies.

Steps are organized into groups. Groups execute in dependency order.
Steps within a group can be parallel (independent) or sequential (ordered).

### Format:
- `### Group X: Title [parallel: bool, depends: Y, model: strategy]`
- `#### Step X.N: Step Title`

### Options:
- `parallel: true` - Steps in this group can run concurrently
- `parallel: false` - Steps must run sequentially (default)
- `depends: A, B` - This group waits for groups A and B to complete
- `model: auto|sonnet|opus` - Model selection for this group (default: auto)

<organize tasks into groups. For simple chores, a single Group A may suffice.>

### Group A: Implementation [parallel: false, model: sonnet]

#### Step A.1: <First Task Name>
- <specific action>
- <specific action>

#### Step A.2: <Second Task Name>
- <specific action>
- <specific action>

### Group B: Validation [parallel: false, depends: A, model: sonnet]

#### Step B.1: Validate Changes
- Run validation commands
- Verify expected behavior

## Validation Commands
Execute these commands to validate the chore is complete:

<list specific commands to validate the work. Be precise about what to run>
- Example: `uv run python -m py_compile adws/*.py` - Test to ensure the code compiles

## Notes
<optional additional context or considerations>
```

## Chore
Use the chore description from the `prompt` variable.

## Report

Return the path to the plan file created.