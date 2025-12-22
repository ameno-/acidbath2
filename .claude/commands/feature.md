# Feature Planning

Create a plan to implement the feature using the specified markdown `Plan Format`. Research the codebase and create a thorough plan.

## Variables
adw_id: $1
prompt: $2

## Instructions

- If the adw_id or prompt is not provided, stop and ask the user to provide them.
- Create a plan to implement the feature described in the `prompt`
- The plan should be comprehensive, well-designed, and follow existing patterns
- Create the plan in the `specs/` directory with filename: `feature-{adw_id}-{descriptive-name}.md`
  - Replace `{descriptive-name}` with a short, descriptive name based on the feature (e.g., "add-agent-logging", "implement-retry-logic", "create-workflow-api")
- Research the codebase starting with `README.md`
- Replace every <placeholder> in the `Plan Format` with the requested value
- Use your reasoning model: THINK HARD about the feature requirements, design, and implementation approach
- Follow existing patterns and conventions in the codebase
- Design for extensibility and maintainability

## Codebase Structure

- `README.md` - Project overview and instructions (start here)
- `adws/` - AI Developer Workflow scripts and modules
- `.claude/commands/` - Claude command templates
- `specs/` - Specification and plan documents
- `agents/` - Output directory for agent results
- `trees/` - Worktree directory for isolated development

## Plan Format

```md
# Feature: <feature name>

## Metadata
adw_id: `{adw_id}`
prompt: `{prompt}`

## Feature Description
<describe the feature in detail, including its purpose and value to users>

## User Story
As a <type of user>
I want to <action/goal>
So that <benefit/value>

## Problem Statement
<clearly define the specific problem or opportunity this feature addresses>

## Solution Statement
<describe the proposed solution approach and how it solves the problem>

## Relevant Files
Use these files to implement the feature:

<list files relevant to the feature with bullet points explaining why. Include new files to be created under an h3 'New Files' section if needed>

## Implementation Plan
### Phase 1: Foundation
<describe the foundational work needed before implementing the main feature>

### Phase 2: Core Implementation
<describe the main implementation work for the feature>

### Phase 3: Integration
<describe how the feature will integrate with existing functionality>

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

<organize tasks into groups. Group A is typically foundation/setup. Later groups depend on earlier ones. Mark independent work as parallel.>

### Group A: Foundation [parallel: false, model: sonnet]
Sequential setup work that other groups depend on.

#### Step A.1: <First Task Name>
- <specific action>
- <specific action>

#### Step A.2: <Second Task Name>
- <specific action>
- <specific action>

### Group B: Core Implementation [parallel: true, depends: A, model: auto]
Independent features that can be built in parallel after foundation.

#### Step B.1: <Parallel Task 1>
- <specific action>

#### Step B.2: <Parallel Task 2>
- <specific action>

### Group C: Integration [parallel: false, depends: B, model: opus]
Sequential integration work that requires heavy reasoning.

#### Step C.1: <Integration Task>
- <specific action>

<continue with additional groups as needed>

## Testing Strategy
### Unit Tests
<describe unit tests needed for the feature>

### Edge Cases
<list edge cases that need to be tested>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the feature to be considered complete>

## Validation Commands
Execute these commands to validate the feature is complete:

<list specific commands to validate the work. Be precise about what to run>
- Example: `uv run python -m py_compile adws/*.py` - Test to ensure the code compiles


## Notes
<optional additional context, future considerations, or dependencies. If new libraries are needed, specify using `uv add`>
```

## Feature
Use the feature description from the `prompt` variable.

## Report

Return the path to the plan file created.