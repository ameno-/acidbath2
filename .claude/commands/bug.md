# Bug Planning

Create a plan to resolve the `Bug` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create a thorough plan.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- IMPORTANT: You're writing a plan to resolve a bug. The plan should be thorough so we fix the root cause and prevent regressions.
- IMPORTANT: The `Bug` describes the bug to resolve but we're creating a plan, not implementing the fix yet.
- Create the plan in `specs/` directory with filename: `issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
  - Replace `{descriptive-name}` with a short name based on the bug (e.g., "fix-login-error", "resolve-timeout")
- Research the codebase to understand the bug, reproduce it, and create a fix plan.
- Replace every <placeholder> in the `Plan Format` with the requested value.
- Use your reasoning model: THINK HARD about the bug, its root cause, and the steps to fix it properly.
- IMPORTANT: Be surgical with your bug fix, solve the bug at hand and don't fall off track.
- IMPORTANT: We want the minimal number of changes that will fix and address the bug.
- Start your research by reading `README.md`.

## Codebase Structure

- `README.md` - Project overview (start here)
- `adws/` - AI Developer Workflow scripts and modules
- `adws/adw_modules/` - Core modules (agent, worktree_ops, issue_providers, etc.)
- `.claude/commands/` - Slash command templates
- `specs/` - Specification and plan documents

## Plan Format

```md
# Bug: <bug name>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`
issue_json: `{issue_json}`

## Bug Description
<describe the bug in detail, including symptoms and expected vs actual behavior>

## Problem Statement
<clearly define the specific problem that needs to be solved>

## Solution Statement
<describe the proposed solution approach to fix the bug>

## Steps to Reproduce
<list exact steps to reproduce the bug>

## Root Cause Analysis
<analyze and explain the root cause of the bug>

## Relevant Files
Use these files to fix the bug:

<list files relevant to the bug with bullet points explaining why>

### New Files
<list any new files that need to be created>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. <First Task>
- <specific action>
- <specific action>

### 2. <Second Task>
- <specific action>
- <specific action>

<continue as needed>

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

<list commands to validate the fix>

## Notes
<optional additional context>
```

## Bug
Extract the bug details from the `issue_json` variable (parse the JSON and use the title and body fields).

## Report

- IMPORTANT: Return exclusively the path to the plan file created and nothing else.
