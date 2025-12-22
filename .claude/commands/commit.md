# Generate Git Commit

Based on the `Instructions` below, take the `Variables` follow the `Run` section to create a git commit with a properly formatted message. Then follow the `Report` section to report the results of your work.

## Variables

scope: $1
category: $2
description: $3

## Instructions

- Generate a concise commit message in the format: `<scope>: <category>: <commit message>`
- The `<scope>` should identify the component/module/area affected (e.g., "adws", "agents", "hooks")
- The `<category>` should be a standard type (e.g., "feat", "fix", "chore", "docs", "refactor", "test")
- The `<commit message>` should be:
  - Present tense (e.g., "add", "fix", "update", not "added", "fixed", "updated")
  - 50 characters or less
  - Descriptive of the actual changes made
  - No period at the end
- Examples:
  - `adws: feat: add workflow orchestration module`
  - `agents: fix: correct crypto analyzer API timeout`
  - `hooks: chore: update TTS utilities to v2`
  - `commands: docs: update import workflow documentation`
- If arguments are not provided, infer from git diff and recent context
- Don't include any 'Generated with...' or 'Authored by...' in the commit message. Focus purely on the changes made.

## Run

1. Run `git diff HEAD` to understand what changes have been made
2. Run `git add -A` to stage all changes
3. Run `git commit -m "<generated_commit_message>"` to create the commit

## Report

Return ONLY the commit message that was used (no other text)
