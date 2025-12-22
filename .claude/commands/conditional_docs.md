# Conditional Documentation Guide

This prompt helps you determine what documentation you should read based on the specific changes you need to make in the codebase. Review the conditions below and read the relevant documentation before proceeding with your task.

## Instructions
- Review the task you've been asked to perform
- Check each documentation path in the Conditional Documentation section
- For each path, evaluate if any of the listed conditions apply to your task
  - IMPORTANT: Only read the documentation if any one of the conditions match your task
- IMPORTANT: You don't want to excessively read documentation. Only read the documentation if it's relevant to your task.

## Conditional Documentation

- README.md
  - Conditions:
    - When first understanding the project structure
    - When you need to understand the overall agentic layer architecture
    - When you want to learn about the 12 Leverage Points of Agentic Coding

- adws/README.md
  - Conditions:
    - When operating on anything under `adws/`
    - When creating or modifying AI Developer Workflows
    - When you need to understand ADW patterns and conventions
    - When working with workflow orchestration

- ai_docs/claude_code_sdk.md
  - Conditions:
    - When working with Claude Code SDK integration
    - When implementing agent.py or agent_sdk.py functionality
    - When troubleshooting Claude Code CLI execution

- ai_docs/uv-single-file-scripts.md
  - Conditions:
    - When creating new ADW scripts with inline dependencies
    - When troubleshooting uv script execution

- .claude/commands/classify_adw.md
  - Conditions:
    - When adding or removing new `adws/adw_*.py` files
    - When updating the AVAILABLE_ADW_WORKFLOWS list

- .claude/commands/classify_issue.md
  - Conditions:
    - When working with issue classification logic
    - When modifying how issues are routed to workflows

- adws/adw_modules/validation.py
  - Conditions:
    - When working with ADW validation or manifests
    - When adding new validation levels or checks

- adws/VALIDATION_STATUS.md
  - Conditions:
    - When checking current validation status of ADWs
    - When troubleshooting ADW import or execution failures

## App-Layer Documentation (Per-Deployment)

When this codebase is deployed with an application layer, additional conditional documentation may be added here. The structure follows:

```
- path/to/app/doc.md
  - Conditions:
    - When working with [specific feature]
    - When troubleshooting [specific behavior]
```

Add app-specific documentation conditions as needed for your deployment.
