# Jerry Architecture

Jerry is an AI Developer Workflows (ADW) framework that separates the agentic layer from application code, enabling portable, scalable development automation.

## Core Philosophy

**Separation of Concerns**: Jerry maintains a clear boundary between:
- **Agentic Layer** (`adws/`, `.claude/`) - AI workflow orchestration
- **Application Layer** - Your actual codebase
- **Metadata Layer** (`.jerry/`) - Framework configuration and versioning

This separation makes Jerry:
- ✅ **Portable** - Deploy to any repository
- ✅ **Composable** - Build complex workflows from simple primitives
- ✅ **Observable** - Track and debug agent actions
- ✅ **Scalable** - Scale compute, not just effort

## Directory Structure

```
your-project/
├── adws/                      # AI Developer Workflows (core)
│   ├── adw_modules/          # Reusable workflow modules
│   │   ├── agent.py          # Agent execution engine
│   │   ├── state.py          # Workflow state management
│   │   ├── workflow_ops.py   # Workflow orchestration
│   │   ├── data_types.py     # Type definitions
│   │   ├── git_ops.py        # Git operations
│   │   └── worktree_ops.py   # Worktree management
│   ├── adw_prompt.py         # Direct prompt execution
│   ├── adw_slash_command.py  # Template-based execution
│   ├── adw_plan_iso.py       # Planning workflows
│   ├── adw_build_iso.py      # Build workflows
│   └── jerry_export.py       # Export Jerry
│   └── jerry_validate.py     # Validate installation
│
├── .claude/                   # Claude Code configuration
│   ├── commands/             # Slash command templates
│   │   ├── chore.md          # Chore planning
│   │   ├── feature.md        # Feature planning
│   │   └── implement.md      # Implementation
│   └── hooks/                # Event-driven automation
│
├── .jerry/                    # Jerry metadata
│   ├── manifest.json         # Version, dependencies, checksums
│   ├── templates/            # Configuration templates
│   └── README.md             # Manifest documentation
│
├── specs/                     # Implementation specifications
│   ├── feature-*.md          # Feature plans
│   ├── chore-*.md            # Chore plans
│   └── patch/*.md            # Patch specifications
│
├── agents/                    # Agent execution outputs
│   └── {adw_id}/             # Per-execution results
│       └── {agent_name}/     # Per-agent outputs
│
├── trees/                     # Worktree isolation
│   └── {worktree_id}/        # Isolated development environments
│
└── jerry_bootstrap.sh         # Bootstrap script

# Your application code lives alongside Jerry
├── src/                       # Your source code
├── tests/                     # Your tests
└── ...                        # Your other files
```

## Layer Separation

### Agentic Layer (Jerry)
**Purpose**: Orchestrate AI agents to perform development tasks

**Components**:
- ADW scripts - Executable workflows
- Slash commands - Templated prompts
- Agent modules - Execution engine
- State management - Track workflow progress

**Responsibilities**:
- Execute Claude Code prompts
- Orchestrate multi-agent workflows
- Manage worktree isolation
- Track and log agent actions

### Application Layer (Your Code)
**Purpose**: The actual software you're building

**Characteristics**:
- Independent of Jerry
- Can be any language/framework
- Modified by Jerry agents
- Tested by Jerry workflows

**Relationship with Jerry**:
- Jerry modifies application code
- Jerry doesn't depend on application code
- Application can exist without Jerry

### Metadata Layer (.jerry/)
**Purpose**: Jerry framework configuration and versioning

**Components**:
- `manifest.json` - Version, dependencies, integrity
- `templates/` - Configuration templates
- Documentation - Framework guides

**Usage**:
- Export/import operations
- Version compatibility checks
- Bootstrap configuration

## Core Concepts

### 1. AI Developer Workflows (ADWs)

ADWs are executable scripts that combine deterministic code with AI agents.

**Types**:
- **Utility ADWs** - Single-purpose tools (`adw_prompt.py`)
- **Planning ADWs** - Generate specifications (`adw_plan_iso.py`)
- **Building ADWs** - Implement specifications (`adw_build_iso.py`)
- **Composite ADWs** - Chain multiple workflows (`adw_plan_build_iso.py`)

**Execution Flow**:
```
User Input → ADW Script → Template Composition → Claude Code CLI → Agent Execution → Output Parsing → Results
```

### 2. Slash Commands

Templated prompts defined in `.claude/commands/*.md`.

**Structure**:
```markdown
# Command Title

## Variables
var1: $1
var2: $2

## Instructions
- Step 1
- Step 2

## Output
Expected output format
```

**Usage**:
```bash
./adws/adw_slash_command.py /chore "Add logging"
```

### 3. Worktree Isolation

Git worktrees provide isolated environments for parallel workflows.

**Benefits**:
- No conflicts between parallel executions
- Safe experimentation
- Port isolation for services
- Clean state per workflow

**Management**:
- `worktree_ops.py` - Create, cleanup, manage
- `trees/` directory - Isolated checkouts
- Automatic port allocation

### 4. Agent State Management

Track workflow progress and results.

**State Types**:
- `PLANNING` - Generating specifications
- `BUILDING` - Implementing code
- `TESTING` - Running validation
- `REVIEWING` - Code review
- `COMPLETED` - Workflow done
- `FAILED` - Workflow failed

**Storage**:
```json
{
  "adw_id": "abc123de",
  "state": "BUILDING",
  "start_time": "2025-01-06T14:30:00Z",
  "agents": ["planner", "implementor"],
  "outputs": ["agents/abc123de/"]
}
```

### 5. Export/Import/Bootstrap

Jerry's portability system.

**Export**:
- Collects core files
- Generates manifest with checksums
- Creates distributable package

**Bootstrap**:
- Validates prerequisites
- Extracts files
- Installs dependencies
- Configures environment

**Validation**:
- Level 1: Import checks
- Level 2: CLI checks
- Level 3: Dry-run workflow

## Design Principles

### 1. Composability

Build complex workflows from simple primitives.

**Example**:
```python
# Simple primitives
adw_prompt.py "generate plan"
adw_slash_command.py /implement spec.md

# Composed workflow
adw_plan_build_iso.py "new feature"
```

### 2. Observability

Every agent action is logged and traceable.

**Output Structure**:
```
agents/{adw_id}/
  ├── adw_state.json          # Workflow state
  ├── {agent_name}/
  │   ├── cc_raw_output.jsonl # Raw stream
  │   ├── cc_final_object.json # Parsed result
  │   └── custom_summary.json  # High-level summary
  └── workflow_summary.json    # Overall summary
```

### 3. Idempotency

Workflows can be safely re-run without side effects.

**Strategies**:
- Check existing state before creating
- Skip already-completed steps
- Clean up failed attempts before retry

### 4. Failure Handling

Graceful degradation and retry logic.

**Retry Codes**:
- `RETRY_API_ERROR` - Transient API failures
- `RETRY_TIMEOUT` - Operation timeout
- `RETRY_RATE_LIMIT` - Rate limiting
- `NO_RETRY` - Fatal errors

### 5. Extensibility

Easy to add new workflows and integrations.

**Extension Points**:
- New ADW scripts - Add new workflows
- New slash commands - Add new templates
- New hooks - Event-driven automation
- New integrations - External services

## Data Flow

### Prompt Execution Flow

```
1. User provides prompt/command
   ↓
2. ADW script receives input
   ↓
3. Template composition (if using slash command)
   ↓
4. Execute Claude Code CLI
   ↓
5. Parse JSONL output stream
   ↓
6. Extract result object
   ↓
7. Save multiple output formats
   ↓
8. Return to user
```

### Worktree Workflow Flow

```
1. Create isolated worktree
   ↓
2. Allocate unique port
   ↓
3. Execute workflow in isolation
   ↓
4. Commit changes to branch
   ↓
5. Merge back to main
   ↓
6. Clean up worktree
```

## Deployment Model

### Single Repository

Jerry lives alongside your application code in the same repository.

**Structure**:
```
your-repo/
├── adws/           # Jerry
├── .claude/        # Jerry
├── .jerry/         # Jerry
├── src/            # Your app
└── tests/          # Your tests
```

### Multiple Repositories

Use export/import to deploy Jerry across projects.

**Workflow**:
1. Maintain Jerry in central repository
2. Export Jerry to package
3. Bootstrap into project repositories
4. Customize per-project as needed

## Scaling Strategies

### Horizontal Scaling

Run multiple ADW workflows in parallel.

**Approaches**:
- Multiple worktrees (parallel feature development)
- Concurrent agent execution
- Distributed task queue

### Vertical Scaling

Scale individual workflow compute.

**Approaches**:
- Use Opus model for complex tasks
- Increase timeout for long-running tasks
- Multi-step workflows with checkpoints

### Organizational Scaling

Scale Jerry across teams and projects.

**Approaches**:
- Central Jerry maintenance team
- Per-project customizations
- Shared ADW library
- Internal package registry

## Future Architecture

Planned enhancements:

### Plugin System
- Third-party ADW registry
- Marketplace for workflows
- Version compatibility matrix

### Distributed Execution
- Remote agent execution
- Cloud-based workflows
- Multi-machine coordination

### Advanced Orchestration
- Workflow graphs
- Conditional execution
- Parallel composition

### Observability++
- Real-time workflow monitoring
- Performance metrics dashboard
- Cost tracking and optimization

---

For deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

For ADW documentation, see [adws/README.md](../adws/README.md)
