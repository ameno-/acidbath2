# Code Reference Format Specification

## Overview

This document defines the format for referencing code examples from the acidbath-code repository within ACIDBATH blog posts. The goal is to maintain readability while preserving the "POC Rule" (all code must be accessible and runnable).

## Decision Thresholds

### Inline Code Blocks (≤20 lines)
**Keep in blog post** - Essential for readability and context

**Criteria:**
- ≤20 lines of code
- Illustrates a single, focused concept
- Provides necessary context for the surrounding discussion
- Not meant to be run as a complete program

**Example Use Cases:**
- Function signatures with minimal implementation
- Configuration snippets showing specific options
- Short illustrative examples
- Code that explains a concept in the flow of text

**Format:** Standard markdown code block (no changes)

```python
def example_function():
    """This stays inline - short and illustrative."""
    return "context for the reader"
```

### External Code References (>20 lines)
**Extract to acidbath-code repository** - Improves readability without losing completeness

**Criteria:**
- >20 lines of code
- Self-contained, runnable example
- Complete implementation of a concept
- Reusable across multiple contexts

**Example Use Cases:**
- Complete class implementations
- Full workflow scripts
- Multi-function modules
- Production-ready examples

**Format:** Callout box with repository link (see templates below)

## Code Reference Formats

### Format 1: Complete Example Callout

Use for fully extracted code examples (40+ lines):

```markdown
> **📦 Complete Example:** [Multi-Agent Orchestrator](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/agent-architecture/multi-agent-orchestrator)
>
> This example demonstrates a complete multi-agent orchestration system with task distribution, agent coordination, and result aggregation.
>
> **Files:** `orchestrator.py`, `agents.py`, `config.yaml`
> **Lines:** 87
> **Language:** Python
```

**Rendered:**

> **📦 Complete Example:** [Multi-Agent Orchestrator](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/agent-architecture/multi-agent-orchestrator)
>
> This example demonstrates a complete multi-agent orchestration system with task distribution, agent coordination, and result aggregation.
>
> **Files:** `orchestrator.py`, `agents.py`, `config.yaml`
> **Lines:** 87
> **Language:** Python

### Format 2: See Full Implementation

Use when showing a snippet but full implementation is available:

```markdown
Here's the core function:

\`\`\`python
def process_task(task):
    """Core task processing logic."""
    result = execute(task)
    return result
\`\`\`

> **🔗 See Full Implementation:** [Task Processor](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/task-processor)
> The complete implementation includes error handling, retry logic, and monitoring integration.
```

**Rendered:**

Here's the core function:

```python
def process_task(task):
    """Core task processing logic."""
    result = execute(task)
    return result
```

> **🔗 See Full Implementation:** [Task Processor](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/task-processor)
> The complete implementation includes error handling, retry logic, and monitoring integration.

### Format 3: Runnable Example

Use when emphasizing that code is ready to run:

```markdown
> **▶️ Runnable Example:** [File System Watcher](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/file-system-watcher)
>
> A production-ready file system watcher with event handling and debouncing. Clone and run:
>
> \`\`\`bash
> git clone https://github.com/ameno-/acidbath-code.git
> cd acidbath-code/production-patterns/directory-watchers/file-system-watcher
> python watcher.py
> \`\`\`
```

**Rendered:**

> **▶️ Runnable Example:** [File System Watcher](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/file-system-watcher)
>
> A production-ready file system watcher with event handling and debouncing. Clone and run:
>
> ```bash
> git clone https://github.com/ameno-/acidbath-code.git
> cd acidbath-code/production-patterns/directory-watchers/file-system-watcher
> python watcher.py
> ```

### Format 4: Multiple Files

Use when code example spans multiple files:

```markdown
> **📁 Multi-File Example:** [Agent Communication System](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/agent-architecture/agent-communication)
>
> Complete agent communication implementation:
>
> - `message_bus.py` - Central message routing
> - `agents.py` - Agent implementations
> - `protocols.py` - Communication protocols
> - `config.yaml` - System configuration
>
> See the README for setup and usage instructions.
```

**Rendered:**

> **📁 Multi-File Example:** [Agent Communication System](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/agent-architecture/agent-communication)
>
> Complete agent communication implementation:
>
> - `message_bus.py` - Central message routing
> - `agents.py` - Agent implementations
> - `protocols.py` - Communication protocols
> - `config.yaml` - System configuration
>
> See the README for setup and usage instructions.

## URL Structure

### GitHub Repository URL Format

Categories are at the root level (not under `examples/`):

```
https://github.com/ameno-/acidbath-code/tree/main/{category}/{post-slug}/{example-name}
```

**Components:**
- `{category}`: One of `agentic-patterns`, `production-patterns`, `workflow-tools`
- `{post-slug}`: Blog post slug (e.g., `agent-architecture`, `directory-watchers`)
- `{example-name}`: Descriptive name for the example (e.g., `multi-agent-orchestrator`)

**Examples:**
```
https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/agent-architecture/multi-agent-orchestrator

https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/file-system-watcher

https://github.com/ameno-/acidbath-code/tree/main/workflow-tools/single-file-scripts/git-workflow-automation
```

### Direct File Links

For linking to specific files:

```
https://github.com/ameno-/acidbath-code/blob/main/{category}/{post-slug}/{example-name}/{filename}
```

**Example:**
```
https://github.com/ameno-/acidbath-code/blob/main/agentic-patterns/agent-architecture/multi-agent-orchestrator/orchestrator.py
```

## Hybrid Approach: Snippet + Reference

For maximum clarity, show a key snippet inline and reference the full code:

```markdown
The orchestrator's core routing logic:

\`\`\`python
def route_task(self, task: Task) -> Agent:
    """Route task to appropriate agent."""
    for agent in self.agents:
        if agent.can_handle(task):
            return agent
    raise NoAgentAvailable(task)
\`\`\`

> **📦 Complete Example:** [Multi-Agent Orchestrator](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/agent-architecture/multi-agent-orchestrator)
> The full implementation includes agent registration, task queuing, result aggregation, and error handling.
```

**Benefits:**
- Readers see the key concept immediately
- Complete code is one click away
- Post remains readable
- POC rule is maintained

## Before/After Examples

### Example 1: Long Python Class

**BEFORE (in blog post):**

```markdown
Here's the complete file system watcher implementation:

\`\`\`python
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcher(FileSystemEventHandler):
    def __init__(self, path: str, callback):
        self.path = Path(path)
        self.callback = callback
        self.observer = Observer()

    def on_modified(self, event):
        if not event.is_directory:
            self.callback(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.callback(event.src_path)

    def start(self):
        self.observer.schedule(self, str(self.path), recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

def process_file(filepath):
    """Process the modified file."""
    print(f"Processing {filepath}")
    # ... more processing logic ...

if __name__ == "__main__":
    watcher = FileWatcher("/path/to/watch", process_file)
    watcher.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()
\`\`\`
```

**AFTER (in blog post):**

```markdown
Here's how to set up a file system watcher:

\`\`\`python
watcher = FileWatcher("/path/to/watch", process_file)
watcher.start()
\`\`\`

> **▶️ Runnable Example:** [File System Watcher](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/file-system-watcher)
>
> A production-ready file system watcher with event handling, debouncing, and error recovery.
>
> **Files:** `watcher.py`, `handlers.py`
> **Lines:** 67
> **Language:** Python
```

**Impact:**
- **Before:** 45 lines of code in blog post
- **After:** 3 lines of code + reference callout
- **Readability:** Significantly improved
- **Completeness:** Still accessible via link

### Example 2: Configuration File

**BEFORE (in blog post):**

```markdown
Here's the complete GitHub Actions workflow:

\`\`\`yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        run: ./deploy.sh
\`\`\`
```

**AFTER (in blog post):**

```markdown
The workflow triggers on pushes to `main` and `develop`:

\`\`\`yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
\`\`\`

> **📦 Complete Example:** [CI/CD Workflow](https://github.com/ameno-/acidbath-code/tree/main/workflow-tools/ci-cd-workflow)
> Full GitHub Actions configuration with testing, deployment, and environment management.

```

**Impact:**
- **Before:** 30+ lines of YAML
- **After:** 6 lines showing the key concept
- **Readability:** Much cleaner
- **Completeness:** Full config available

### Example 3: Multi-File Example

**BEFORE (in blog post):**

Three separate large code blocks showing `orchestrator.py`, `agents.py`, and `config.yaml` (~150 lines total)

**AFTER (in blog post):**

```markdown
The orchestrator delegates tasks to specialized agents:

\`\`\`python
def delegate_task(self, task: Task) -> Result:
    agent = self.route_task(task)
    return agent.execute(task)
\`\`\`

> **📁 Multi-File Example:** [Multi-Agent Orchestrator](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/agent-architecture/multi-agent-orchestrator)
>
> Complete implementation with:
>
> - `orchestrator.py` - Task routing and coordination
> - `agents.py` - Specialized agent implementations
> - `config.yaml` - System configuration
> - `README.md` - Setup and usage guide
>
> Clone and run to see multi-agent coordination in action.
```

**Impact:**
- **Before:** 150+ lines across 3 code blocks
- **After:** 5-line snippet + structured reference
- **Readability:** Dramatic improvement
- **Completeness:** All code accessible with context

## Selection Guidelines

### When to Use Each Format

| Format | Use Case | Icon | Line Count |
|--------|----------|------|------------|
| **Complete Example** | Fully extracted code, comprehensive implementation | 📦 | 40+ |
| **See Full Implementation** | Snippet shown, full version available | 🔗 | 30+ |
| **Runnable Example** | Emphasis on ready-to-run code | ▶️ | 40+ |
| **Multi-File Example** | Multiple files, complex structure | 📁 | 50+ |

### Icon Usage

- **📦** - Complete, packaged example
- **🔗** - Link to full implementation
- **▶️** - Runnable, executable code
- **📁** - Multi-file, structured example

## Validation

### Before Transformation
- [ ] Code block is >20 lines
- [ ] Code is complete and runnable (not just a snippet)
- [ ] Code has been extracted to acidbath-code repository
- [ ] Example has a complete README
- [ ] GitHub URL is verified to work

### After Transformation
- [ ] Essential context is preserved (show key snippet if needed)
- [ ] Reference callout is clear and informative
- [ ] GitHub link resolves correctly
- [ ] POC rule is maintained (code is accessible)
- [ ] Post readability is improved

## POC Rule Compliance

**The POC Rule:** All code in blog posts must be working, copy-paste code that readers can use immediately.

**Compliance Strategy:**
1. **Inline Snippets:** Already copy-paste ready
2. **Extracted Examples:** One-click access to complete, runnable code
3. **Hybrid Approach:** Show key snippet + link to full implementation
4. **Runnable Callouts:** Include clone-and-run instructions

**Validation:**
- Every code reference must link to working code
- Every example in acidbath-code must have usage instructions
- No broken links allowed (validated in CI)
- All referenced code must pass syntax validation

## Notes

- **Consistency:** Use the same format for similar code types across posts
- **Context:** Always provide enough context for readers to understand the reference
- **Accessibility:** One-click access to full code is mandatory
- **Readability:** Improved post flow is the primary goal
- **Completeness:** Never sacrifice completeness for brevity
