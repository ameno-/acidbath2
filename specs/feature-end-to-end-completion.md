# Plan: End-to-End Task Completion with Parallel Execution

## Meta: Self-Implementation Strategy

**This plan uses the new system to implement itself (dogfooding)**

Once Step 1-2 are complete (data types + spec format), we commit to `specs/` and use the NEW parallel group format to implement remaining steps. This allows:
1. Validating the new format works
2. Resuming work if interrupted (plan persisted in specs/)
3. Testing parallel execution as we build it

**Persistence**: After each major step, commit changes. The spec file at `specs/feature-end-to-end-completion.md` becomes the source of truth.

## Execution Order (Dogfooding Phases)

### Phase 0: Bootstrap (Manual Implementation)
Steps 1-3 must be implemented manually because the system doesn't exist yet:
- **Step 1**: Data types → validates with `py_compile` → commit
- **Step 2**: Spec format → validates visually → commit
- **Step 3**: Plan executor (PlanParser only) → validates with import → commit

**Checkpoint**: After Phase 0, we can parse specs with the new format.

### Phase 1: Self-Implementation Begins
Copy this plan to `specs/feature-end-to-end-completion.md` using new format:
```bash
# Convert remaining steps to new format with parallel groups
cp ~/.claude/plans/glittery-wibbling-rocket.md specs/feature-end-to-end-completion.md
# Edit to add Group annotations
```

Then use the NEW PlanParser to parse and track progress.

### Phase 2: Parallel Build (Steps 4-5 can be parallel)
```
### Group B: Slash Commands [parallel: true, depends: A, model: sonnet]
#### Step B.1: Create /implement_step
#### Step B.2: Create /mark_step_in_progress
#### Step B.3: Create /update_step_status
#### Step B.4: Rewrite /implement
```

### Phase 3: Integration (Sequential)
```
### Group C: Integration [parallel: false, depends: B, model: opus]
#### Step C.1: Complete plan_executor.py (StepExecutor, Orchestrator)
#### Step C.2: Add workflow_ops function
#### Step C.3: Update adw_build_iso.py
```

### Phase 4: Validation (Use new system to validate itself)
```
### Group D: Validation [parallel: false, depends: C, model: sonnet]
#### Step D.1: Run all validation commands
#### Step D.2: Run integration tests
#### Step D.3: Final commit
```

---

## Quick Reference

| File | Action | Purpose |
|------|--------|---------|
| `adws/adw_modules/data_types.py` | Modify | Add `ModelStrategy`, `StepStatus`, `StepGroup`, `ExecutionPlan` types |
| `adws/adw_modules/plan_executor.py` | **Create** | Multi-phase orchestrator with step tracking (based on legacy patterns) |
| `adws/adw_modules/workflow_ops.py` | Modify | Add `implement_plan_with_tracking()` function |
| `adws/adw_build_iso.py` | Modify | Use new orchestrator, pass model_strategy |
| `.claude/commands/implement.md` | Rewrite | Step-by-step execution with Task tool support |
| `.claude/commands/implement_step.md` | **Create** | Single-step execution command |
| `.claude/commands/mark_step_in_progress.md` | **Create** | Claim step before work (from legacy pattern) |
| `.claude/commands/update_step_status.md` | **Create** | Report step success/failure (from legacy pattern) |
| `.claude/commands/feature.md` | Modify | Add parallel group + dependency annotations |
| `.claude/commands/chore.md` | Modify | Same format changes as feature.md |

**Key Patterns Combined**:
1. **Phase-based orchestration** (tac8_app3) - separate agents per phase
2. **Task status state machine** (tac8_app2) - `[] → [⏰] → [🟡] → [✅]/[❌]`
3. **Dependency blocking** - blocked steps wait for ALL preceding steps to succeed

---

## Problem Statement

PR #44 exemplifies a critical issue: multi-step plans (26 steps, 3 phases) only get Phase 1 implemented. Root causes:

1. **Minimal `/implement` command** - Just 12 lines saying "read plan, think hard, implement"
2. **No step tracking** - No checkpoints, validation, or completion tracking
3. **Model always Sonnet** - Even for complex 26-step plans
4. **No parallelism support** - Sequential-only execution
5. **No context window awareness** - No mechanism to handle large tasks

## Proven Patterns: Legacy Multi-Agent Workflows

### Pattern 1: Phase-Based Orchestration
**Reference:** `legacy/tac8_app3__out_loop_multi_agent_task_board/adws/adw_plan_implement_update_task.py`

- **Separate agents per phase**: `planner-{name}`, `builder-{name}`, `updater-{name}`
- **Phase gating**: Implementation only runs if planning succeeded AND plan_path extracted
- **State tracking**: `workflow_success`, `plan_path`, `commit_hash`, `error_message`
- **Per-phase summaries**: Each phase saves JSON summary for observability
- **Always-run cleanup**: Update task runs regardless to report final status

### Pattern 2: Task Status State Machine
**Reference:** `legacy/tac8_app2__multi_agent_todone/.claude/commands/`

This system has a sophisticated task status progression:

```
[] → [⏰] → [🟡, <adw_id>] → [✅ <commit>, <adw_id>] or [❌, <adw_id>]
```

| Status | Meaning | Transition |
|--------|---------|------------|
| `[]` | Not started, ready | → `[🟡]` via `/mark_in_progress` |
| `[⏰]` | Blocked by dependencies | → `[🟡]` only if ALL above tasks are `[✅]` |
| `[🟡, <adw_id>]` | In progress | → `[✅]` or `[❌]` via `/update_task` |
| `[✅ <commit>, <adw_id>]` | Success with commit hash | Terminal |
| `[❌, <adw_id>] // Failed: <msg>` | Failed with error | Terminal |

**Key Commands:**
- `/process_tasks` - Analyze tasks, return eligible ones respecting dependencies
- `/mark_in_progress` - Claim task before starting work
- `/update_task` - Report success/failure after completion

**Critical Insight: Dependency Blocking**
```markdown
## Git Worktree feature-auth
[✅ abc123, adw_001] Task 1
[🟡, adw_002] Task 2         # In progress
[] Task 3 {api, auth}         # Eligible - not blocked
[⏰] Task 4                   # NOT eligible - Task 2 is not [✅]
```

Blocked tasks (`[⏰]`) can ONLY run when ALL preceding tasks are successful.

**Why previous approaches still failed**: Even with phase separation, the `/implement` agent receives the whole plan and may only complete part of it within its context window.

## Solution Overview

Combine the **legacy phase-based pattern** with **step-level orchestration**:

1. **Phase-based orchestration** (from legacy) - separate agents per major phase
2. **Step-level tracking** (new) - within implementation, track/checkpoint each step
3. **Structured spec format** with parallel groups and dependencies
4. **Configurable model selection** per-ADW/phase
5. **Context window awareness** with step decomposition when needed

---

## Files to Modify

### Core Type Definitions
- `/Users/ameno/dev/tac/tac-8/adws/adw_modules/data_types.py`
  - Add: `ModelStrategy`, `StepStatus`, `StepDefinition`, `StepGroup`, `ExecutionPlan`
  - Update: `AgentPromptRequest`, `AgentTemplateRequest` with `model_strategy`
  - Update: `ADWStateData` with `execution_plan`, `model_strategy`

### Workflow Operations
- `/Users/ameno/dev/tac/tac-8/adws/adw_modules/workflow_ops.py`
  - Add: `implement_plan_with_tracking()` function (keep existing `implement_plan()`)

### Build Workflow
- `/Users/ameno/dev/tac/tac-8/adws/adw_build_iso.py`
  - Update: Use `implement_plan_with_tracking()` by default
  - Add: Model strategy support from state

### Slash Commands
- `/Users/ameno/dev/tac/tac-8/.claude/commands/implement.md`
  - Rewrite: Add step tracking, context awareness, Task tool usage
- `/Users/ameno/dev/tac/tac-8/.claude/commands/feature.md`
  - Update: Add parallel group annotations format
- `/Users/ameno/dev/tac/tac-8/.claude/commands/chore.md`
  - Update: Same format changes as feature.md

## New Files to Create

- `/Users/ameno/dev/tac/tac-8/adws/adw_modules/plan_executor.py`
  - `PlanParser` - Parse spec into structured groups/steps
  - `StepExecutor` - Execute individual steps with model selection
  - `MultiPhaseOrchestrator` - Coordinate parallel/sequential execution (from legacy pattern)

- `/Users/ameno/dev/tac/tac-8/.claude/commands/implement_step.md`
  - Single-step execution command

- `/Users/ameno/dev/tac/tac-8/.claude/commands/mark_step_in_progress.md` (from legacy tac8_app2)
  - Claim step before starting work
  - Updates step status: `PENDING` or `BLOCKED` → `IN_PROGRESS`
  - Records agent ID that claimed the step

- `/Users/ameno/dev/tac/tac-8/.claude/commands/update_step_status.md` (from legacy tac8_app2)
  - Report step completion (success or failure)
  - Updates step status: `IN_PROGRESS` → `COMPLETED` or `FAILED`
  - Records commit hash (success) or error message (failure)

---

## Implementation Steps

### Step 1: Add Data Types (Following Legacy Status Pattern)
**File:** `/Users/ameno/dev/tac/tac-8/adws/adw_modules/data_types.py`

```python
# Model selection strategy
ModelStrategy = Literal["auto", "sonnet", "opus", "heavy-for-build"]

# Step status matching legacy pattern: [] → [⏰] → [🟡] → [✅]/[❌]
class StepStatus(str, Enum):
    PENDING = "pending"           # [] - ready to run
    BLOCKED = "blocked"           # [⏰] - waiting on dependencies
    IN_PROGRESS = "in_progress"   # [🟡, adw_id] - agent working
    COMPLETED = "completed"       # [✅ commit, adw_id] - success
    FAILED = "failed"             # [❌, adw_id] - error
    SKIPPED = "skipped"           # Skipped due to upstream failure

class StepDefinition(BaseModel):
    step_id: str  # e.g., "A.1"
    group_id: str
    title: str
    description: str
    status: StepStatus = StepStatus.PENDING
    adw_id: Optional[str] = None           # Agent ID that claimed this step
    commit_hash: Optional[str] = None      # Commit if successful
    result_summary: Optional[str] = None
    error_message: Optional[str] = None

class StepGroup(BaseModel):
    group_id: str
    title: str
    parallel: bool = False
    depends_on: List[str] = Field(default_factory=list)
    model_strategy: ModelStrategy = "auto"
    steps: List[StepDefinition] = Field(default_factory=list)

class ExecutionPlan(BaseModel):
    plan_file: str
    groups: List[StepGroup] = Field(default_factory=list)
    current_group: Optional[str] = None
    current_step: Optional[str] = None

# Update ADWStateData - add execution tracking
class ADWStateData(BaseModel):
    # ... existing fields ...
    execution_plan: Optional[Dict[str, Any]] = None  # Step progress
    model_strategy: Optional[ModelStrategy] = "auto"
    phases_completed: List[str] = Field(default_factory=list)
```

### Step 2: Update Spec Format
**File:** `feature.md` and `chore.md`

New step format with parallel groups:

```markdown
## Step by Step Tasks

### Group A: Foundation [parallel: false, model: sonnet]
Sequential foundation work.

#### Step A.1: Setup base types
- Create data models
- Add validation

#### Step A.2: Create utilities
- Add helper functions

### Group B: Core Features [parallel: true, depends: A, model: auto]
Independent features that can run in parallel.

#### Step B.1: Implement feature X
- Implementation details

#### Step B.2: Implement feature Y
- Implementation details

### Group C: Integration [parallel: false, depends: B, model: opus]
Sequential integration requiring heavy model.

#### Step C.1: Wire components together
- Integration work
```

### Step 3: Create Plan Executor Module
**File:** `plan_executor.py` (NEW)

Key classes:
- `PlanParser.parse(spec_content) -> ExecutionPlan`
- `StepExecutor.execute_step(step, group, state) -> (bool, str)`
- `PlanOrchestrator.execute_plan(spec_path, state) -> ExecutionPlan`

Features:
- Parse `[parallel: true, depends: A, model: opus]` annotations
- Execute groups in dependency order
- Parallel execution via `ThreadPoolExecutor` (pattern from `adw_review_all_iso.py`)
- Checkpoint progress in state for resume
- Model selection based on strategy

### Step 4: Create /implement_step Command
**File:** `implement_step.md` (NEW)

```markdown
---
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
description: Implement a single step from a plan
---

# Implement Step: $1 - $2

Focus ONLY on this specific step. Do not work on other steps.

## Task
$3

## Instructions
1. Read relevant code first
2. Implement the step's requirements
3. Validate changes compile: `uv run python -m py_compile <files>`
4. Do NOT commit (orchestrator handles this)

## Report
- Files modified
- Key changes
- Validation results
```

### Step 5: Rewrite /implement Command
**File:** `implement.md`

```markdown
---
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
description: Execute implementation plan with step tracking
---

# Implement Plan with Step Tracking

## Plan File
$ARGUMENTS

## Instructions

### 1. Parse the Plan
Identify step groups, dependencies, and parallel hints.

### 2. Execute Groups in Dependency Order
For each group:
1. Verify dependencies complete
2. Execute steps (parallel or sequential based on annotation)
3. Validate before proceeding

### 3. Step Execution Protocol
For each step:
1. Report: "Starting Step X.Y: <title>"
2. Execute ALL bullet points
3. Validate changes
4. Report: "Completed Step X.Y" or "Failed Step X.Y: <reason>"

### 4. Context Management
If a step is too large for single context:
- Use Task tool to spawn focused sub-agents
- Each sub-agent handles one aspect
- Aggregate results

### 5. Handle Failures
- Retry failed step ONCE with more focus
- If retry fails, continue with non-dependent steps
- Report all failures at end

## Report
- Steps completed vs total
- Failed steps with reasons
- `git diff --stat`
```

### Step 6: Create Multi-Phase Orchestrator (Following Legacy Pattern)
**File:** `/Users/ameno/dev/tac/tac-8/adws/adw_modules/plan_executor.py` (NEW)

Based on `legacy/tac8_app3__out_loop_multi_agent_task_board/adws/adw_plan_implement_update_task.py`:

```python
class MultiPhaseOrchestrator:
    """Orchestrates multi-phase workflow execution with separate agents per phase.

    Pattern from legacy adw_plan_implement_update_task.py:
    - Separate agent per phase for context isolation
    - Phase gating (only proceed if previous phase succeeded)
    - State tracking between phases
    - Per-phase summaries for observability
    """

    def __init__(self, adw_id: str, working_dir: str, logger: logging.Logger):
        self.adw_id = adw_id
        self.working_dir = working_dir
        self.logger = logger
        self.state = ADWState.load(adw_id, logger) or ADWState(adw_id)

    def execute_workflow(self, task: str, model_strategy: ModelStrategy = "auto") -> WorkflowResult:
        """Execute full plan-implement workflow with step tracking."""
        workflow_success = True
        plan_path = None
        error_message = None

        # Phase 1: Planning (separate agent)
        planner_name = f"planner-{self.adw_id[:6]}"
        plan_response = self._execute_phase(
            phase_name="planning",
            agent_name=planner_name,
            slash_command="/plan",
            args=[self.adw_id, task],
            model=self._select_model("planning", model_strategy)
        )

        if not plan_response.success:
            workflow_success = False
            error_message = "Planning phase failed"
        else:
            plan_path = self._extract_plan_path(plan_response.output)

        # Phase 2: Implementation with step tracking (multiple agents)
        if workflow_success and plan_path:
            implement_result = self._execute_implementation_phase(
                plan_path=plan_path,
                model_strategy=model_strategy
            )
            if not implement_result.success:
                workflow_success = False
                error_message = implement_result.error_message

        return WorkflowResult(
            success=workflow_success,
            plan_path=plan_path,
            error_message=error_message,
            phases_completed=self.state.get("phases_completed", [])
        )

    def _execute_implementation_phase(self, plan_path: str, model_strategy: ModelStrategy):
        """Execute implementation with step-level tracking.

        For complex plans: Parse into groups, execute per-group agents.
        For simple plans: Single implement agent.
        """
        # Parse plan to check complexity
        plan = self._parse_plan(plan_path)

        if len(plan.groups) > 1 or any(g.parallel for g in plan.groups):
            # Complex plan: use group-level orchestration
            return self._execute_grouped_implementation(plan, model_strategy)
        else:
            # Simple plan: single implement agent
            return self._execute_simple_implementation(plan_path, model_strategy)

    def _execute_grouped_implementation(self, plan: ExecutionPlan, model_strategy: ModelStrategy):
        """Execute plan group by group with dependency ordering."""
        completed_groups = set()

        for group in self._get_execution_order(plan.groups):
            # Check dependencies
            if not all(dep in completed_groups for dep in group.depends_on):
                continue

            model = self._select_model(f"build-{group.group_id}", model_strategy, group.model_strategy)

            if group.parallel and len(group.steps) > 1:
                # Parallel execution within group
                result = self._execute_parallel_steps(group, model)
            else:
                # Sequential execution
                result = self._execute_sequential_steps(group, model)

            if result.success:
                completed_groups.add(group.group_id)
            else:
                return result  # Stop on failure

        return ImplementResult(success=True)
```

### Step 7: Add workflow_ops Function
**File:** `/Users/ameno/dev/tac/tac-8/adws/adw_modules/workflow_ops.py`

```python
def implement_plan_with_tracking(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
    max_concurrent: int = 3,
    model_strategy: ModelStrategy = "auto",
) -> AgentPromptResponse:
    """Implement plan with step tracking and parallel execution.

    Uses the MultiPhaseOrchestrator pattern from legacy implementation.
    """
    from .plan_executor import MultiPhaseOrchestrator

    orchestrator = MultiPhaseOrchestrator(adw_id, working_dir, logger)
    result = orchestrator.execute_implementation_phase(
        plan_path=plan_file,
        model_strategy=model_strategy
    )

    return AgentPromptResponse(
        output=result.summary,
        success=result.success,
        retry_code=RetryCode.NONE
    )
```

### Step 8: Update adw_build_iso.py
**File:** `/Users/ameno/dev/tac/tac-8/adws/adw_build_iso.py` (around line 220)

```python
# Get model strategy from state
model_strategy = state.get("model_strategy", "auto")

# Use new implementation by default
implement_response = implement_plan_with_tracking(
    plan_file=plan_file,
    adw_id=adw_id,
    logger=logger,
    working_dir=worktree_path,
    max_concurrent=3,
    model_strategy=model_strategy,
)
```

---

## Backward Compatibility

1. **Existing specs** without group annotations → treated as single sequential group
2. **`implement_plan()`** remains unchanged for direct calls
3. **State files** extended with optional new fields

## Context Window Strategy

Per user requirement:
- Estimate step tokens before execution
- If step exceeds ~70% of context limit (~126K tokens), use focused prompt
- Agent can spawn sub-agents via Task tool for truly independent sub-work
- Each agent/sub-agent must complete its portion within single context

## Model Selection Logic

```python
def select_model(step, group, state):
    strategy = group.model_strategy
    if strategy == "opus": return "opus"
    if strategy == "sonnet": return "sonnet"
    if strategy == "heavy-for-build":
        if "implement" in step.title.lower(): return "opus"
        return "sonnet"
    # "auto": estimate complexity
    if estimated_tokens > 50000: return "opus"
    return "sonnet"
```

---

## Validation & Testing Strategy

### Per-Step Validation Commands

Each step MUST pass validation before proceeding:

**Step 1 (Data Types):**
```bash
# Verify Python compiles
uv run python -m py_compile adws/adw_modules/data_types.py

# Verify imports work
uv run python -c "from adws.adw_modules.data_types import StepStatus, StepGroup, ExecutionPlan, ModelStrategy; print('OK')"
```

**Step 2 (Spec Format):**
```bash
# Verify markdown is valid
cat .claude/commands/feature.md | head -100
# Visual inspection of Group/Step format
```

**Step 3 (Plan Executor):**
```bash
# Verify module compiles
uv run python -m py_compile adws/adw_modules/plan_executor.py

# Test parser
uv run python -c "
from adws.adw_modules.plan_executor import PlanParser
parser = PlanParser()
# Parse a sample spec
print('Parser OK')
"
```

**Step 4-5 (Slash Commands):**
```bash
# Verify markdown syntax
cat .claude/commands/implement_step.md
cat .claude/commands/implement.md
```

**Step 6-7 (Orchestrator + workflow_ops):**
```bash
# Verify integration
uv run python -c "
from adws.adw_modules.workflow_ops import implement_plan_with_tracking
print('workflow_ops OK')
"
```

**Step 8 (adw_build_iso):**
```bash
# Verify script runs help
uv run adws/adw_build_iso.py --help
```

### Integration Test: Self-Implementation

**Test 1: Parse This Plan**
```bash
# After Step 3 is complete, use the new parser on this plan
uv run python -c "
from adws.adw_modules.plan_executor import PlanParser
parser = PlanParser()
with open('specs/feature-end-to-end-completion.md') as f:
    plan = parser.parse(f.read(), 'specs/feature-end-to-end-completion.md')
print(f'Groups: {len(plan.groups)}')
for g in plan.groups:
    print(f'  {g.group_id}: {len(g.steps)} steps, parallel={g.parallel}')
"
```

**Test 2: Simple Sequential Execution**
```bash
# Create minimal test spec
cat > /tmp/test_spec.md << 'EOF'
# Test Plan

## Step by Step Tasks

### Group A: Test [parallel: false, model: sonnet]

#### Step A.1: Create test file
- Create /tmp/test_step_1.txt with content "Step 1 complete"

#### Step A.2: Verify test file
- Read /tmp/test_step_1.txt
- Verify content is correct
EOF

# Run with new orchestrator
uv run adws/adw_build_iso.py --plan-file /tmp/test_spec.md --adw-id test-001
```

**Test 3: Parallel Execution**
```bash
# Test spec with parallel group
cat > /tmp/test_parallel.md << 'EOF'
# Test Parallel Plan

## Step by Step Tasks

### Group A: Setup [parallel: false, model: sonnet]

#### Step A.1: Create base directory
- Create /tmp/parallel_test/

### Group B: Parallel Work [parallel: true, depends: A, model: sonnet]

#### Step B.1: Create file 1
- Create /tmp/parallel_test/file1.txt

#### Step B.2: Create file 2
- Create /tmp/parallel_test/file2.txt

#### Step B.3: Create file 3
- Create /tmp/parallel_test/file3.txt

### Group C: Verify [parallel: false, depends: B, model: sonnet]

#### Step C.1: Check all files exist
- ls /tmp/parallel_test/
- Verify 3 files exist
EOF

# Run and verify parallel execution in logs
uv run adws/adw_build_iso.py --plan-file /tmp/test_parallel.md --adw-id test-parallel
```

**Test 4: Resume Capability**
```bash
# Start execution, interrupt mid-way, then resume
uv run adws/adw_build_iso.py --plan-file specs/feature-end-to-end-completion.md --adw-id resume-test &
PID=$!
sleep 10
kill $PID

# Check state
cat agents/resume-test/adw_state.json

# Resume
uv run adws/adw_build_iso.py --resume resume-test
```

### Git Workflow: Feature Branch + PR

**CRITICAL**: All work on feature branch, periodic pushes to PR for visibility.

```bash
# 1. Create feature branch (before any implementation)
git checkout -b feat-end-to-end-completion
git push -u origin feat-end-to-end-completion

# 2. Create draft PR immediately for visibility
gh pr create --draft --title "feat: end-to-end task completion with parallel execution" \
  --body "Implements #<issue> - multi-step plan completion with parallel groups"
```

### Commit Strategy

After each successful step validation, commit AND push:
```bash
git add -A
git commit -m "feat: implement step N of end-to-end completion - <step name>"
git push  # Push after every commit for persistence
```

**Critical commits to make:**
1. After Step 1: Data types added → push
2. After Step 2: Spec format updated → push
3. After Step 3: Plan executor created → push
4. After Step 6: Full orchestrator working → push
5. After all tests pass: Final validation → push, mark PR ready

**Push frequency**: After EVERY commit. This ensures:
- Work is persisted if context is lost
- PR shows incremental progress
- Can resume from any commit if interrupted

### Spec Persistence

Copy this plan to specs/ FIRST (before implementation):
```bash
cp ~/.claude/plans/glittery-wibbling-rocket.md specs/feature-end-to-end-completion.md
git add specs/feature-end-to-end-completion.md
git commit -m "specs: add end-to-end completion feature specification"
git push
```

This becomes the source of truth for resuming work.
