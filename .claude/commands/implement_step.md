# Implement Single Step

Focus ONLY on implementing this specific step. Do not work on other steps.

## Variables
step_id: $1
step_title: $2
step_description: $3

## Instructions

### 1. Understand the Step
- This is Step **$1: $2**
- Read the step description carefully
- Identify the specific files to modify
- Understand the expected outcome

### 2. Research Before Implementation
- Read all relevant files BEFORE making changes
- Understand existing patterns in the codebase
- Do not guess - verify by reading code

### 3. Implement the Step
Execute the following task:

```
$3
```

### 4. Validate Changes
After implementation:
- Ensure all modified files compile: `uv run python -m py_compile <file>`
- Verify imports work if new code was added
- Run any step-specific validation mentioned in the description

### 5. Do NOT Commit
The orchestrator handles commits. Just implement and validate.

## Report

Provide a brief summary:
- **Step**: $1 - $2
- **Files Modified**: List each file with 1-line description of change
- **Validation**: Pass/Fail with details
- **Notes**: Any issues encountered or decisions made
