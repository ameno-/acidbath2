# Implement Plan with Step Tracking

Execute an implementation plan step-by-step with progress tracking.

## Plan File
$ARGUMENTS

## Instructions

### 1. Parse the Plan

Read the plan file and identify:
- **Groups**: Look for `### Group X: Title [options]` headers
- **Steps**: Look for `#### Step X.N: Title` within each group
- **Dependencies**: Note `depends:` in group options
- **Parallel hints**: Note `parallel: true` for concurrent steps
- **Model hints**: Note `model:` for heavy reasoning steps

If no group format found, treat as single sequential group.

### 2. Execute Groups in Dependency Order

For each group (respecting dependencies):

1. **Check Dependencies**: Ensure all groups in `depends:` are complete
2. **Report Group Start**: "Starting Group X: Title (N steps)"
3. **Execute Steps**:
   - If `parallel: false`: Execute sequentially
   - If `parallel: true`: Steps are independent (still execute one at a time unless using Task tool)
4. **Report Group Complete**: "Completed Group X: N/N steps succeeded"

### 3. Step Execution Protocol

For EACH step:

#### 3.1 Report Start
```
═══════════════════════════════════════
Starting Step X.N: <title>
═══════════════════════════════════════
```

#### 3.2 Read Before Writing
- ALWAYS read relevant files BEFORE modifying
- Understand existing patterns
- Do not guess - verify by reading

#### 3.3 Execute ALL Bullet Points
- Execute EVERY bullet point in the step
- Do not skip any items
- Do not stop early

#### 3.4 Validate
- Ensure code compiles: `uv run python -m py_compile <file>`
- Run step-specific validation if mentioned

#### 3.5 Report Completion
```
───────────────────────────────────────
Completed Step X.N: <title>
Files: <list modified files>
───────────────────────────────────────
```
OR if failed:
```
───────────────────────────────────────
FAILED Step X.N: <title>
Error: <what went wrong>
───────────────────────────────────────
```

### 4. Context Management

If a step is too large for comfortable execution:
- Break it into logical sub-tasks
- Use the Task tool with focused prompts for sub-tasks
- Aggregate results

### 5. Handle Failures

If a step fails:
1. Report the failure with details
2. Retry ONCE with more focused approach
3. If retry fails:
   - Mark step as failed
   - Continue with non-dependent steps
   - Report all failures at end

### 6. Do NOT Commit

The orchestrator handles commits. Focus on implementation and validation.

## Report

After ALL steps are attempted:

```
════════════════════════════════════════════
IMPLEMENTATION SUMMARY
════════════════════════════════════════════

Groups Completed: X/Y
Steps Completed: N/M

Successful Steps:
- A.1: <title>
- A.2: <title>
- B.1: <title>

Failed Steps:
- C.1: <title> - <reason>

Files Changed:
<output of git diff --stat>
════════════════════════════════════════════
```
