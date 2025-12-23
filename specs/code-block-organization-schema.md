# Code Block Organization Schema

## Overview

This document defines the organizational structure for the acidbath-code repository, which hosts all complete code examples extracted from ACIDBATH blog posts.

## Category Taxonomy

Code examples are organized into four primary categories:

### 1. `agentic-patterns/`
Code examples demonstrating AI agent patterns, workflows, and architectures.

**Examples:**
- Agent orchestration systems
- Multi-agent coordination
- Agent communication protocols
- Prompt engineering patterns
- Context management strategies

**Source Posts:**
- agent-architecture.md
- claude-skills-deep-dive.md
- context-engineering.md

### 2. `production-patterns/`
Production-ready code patterns for real-world applications.

**Examples:**
- Error handling and resilience
- Monitoring and observability
- Configuration management
- Deployment patterns
- Performance optimization

**Source Posts:**
- directory-watchers.md
- document-generation-skills.md

### 3. `workflow-tools/`
Utility scripts, automation tools, and workflow helpers.

**Examples:**
- CLI tools
- Automation scripts
- File processing utilities
- Data transformation tools
- Build and deployment scripts

**Source Posts:**
- single-file-scripts.md
- workflow-prompts.md

### 4. `configurations/`
Configuration files, schemas, and templates.

**Examples:**
- YAML configurations
- JSON schemas
- Environment templates
- CI/CD configurations
- Docker/container configs

**Source Posts:**
- All posts (configuration snippets)

## Directory Structure

```
acidbath-code/
├── README.md                          # Repository overview and index
├── .github/
│   └── workflows/
│       └── validate-code.yml          # CI validation workflow
├── scripts/
│   └── validate-all.py                # Local validation script
├── examples/
│   ├── agentic-patterns/
│   │   ├── agent-architecture/
│   │   │   ├── multi-agent-orchestrator/
│   │   │   │   ├── README.md          # Example context and usage
│   │   │   │   ├── orchestrator.py    # Main implementation
│   │   │   │   ├── agents.py          # Agent definitions
│   │   │   │   └── config.yaml        # Configuration
│   │   │   └── agent-communication/
│   │   │       ├── README.md
│   │   │       └── message_bus.py
│   │   ├── claude-skills-deep-dive/
│   │   │   └── skill-template/
│   │   │       ├── README.md
│   │   │       └── skill.md
│   │   └── context-engineering/
│   │       └── context-manager/
│   │           ├── README.md
│   │           └── context_manager.py
│   ├── production-patterns/
│   │   ├── directory-watchers/
│   │   │   ├── file-system-watcher/
│   │   │   │   ├── README.md
│   │   │   │   ├── watcher.py
│   │   │   │   └── handlers.py
│   │   │   └── event-processor/
│   │   │       ├── README.md
│   │   │       └── processor.py
│   │   └── document-generation-skills/
│   │       └── pdf-generator/
│   │           ├── README.md
│   │           └── generator.py
│   ├── workflow-tools/
│   │   ├── single-file-scripts/
│   │   │   ├── git-workflow-automation/
│   │   │   │   ├── README.md
│   │   │   │   └── git_workflow.py
│   │   │   └── code-analyzer/
│   │   │       ├── README.md
│   │   │       └── analyze.py
│   │   └── workflow-prompts/
│   │       └── prompt-templates/
│   │           ├── README.md
│   │           └── templates.md
│   └── configurations/
│       └── ci-cd-configs/
│           ├── README.md
│           └── github-actions.yml
└── manifest.json                      # Mapping of blog posts to examples
```

## Naming Conventions

### Directory Names
- Use lowercase with hyphens: `multi-agent-orchestrator`
- Be descriptive but concise: `file-system-watcher` not `fsw`
- Match blog post slug when possible: `agent-architecture/`

### File Names
- Use snake_case for Python: `orchestrator.py`, `message_bus.py`
- Use kebab-case for configs: `github-actions.yml`, `docker-compose.yml`
- Use descriptive names: `watcher.py` not `w.py`

### Example Names
- Reflect the purpose: `multi-agent-orchestrator` not `example1`
- Be specific: `file-system-watcher` not `watcher`
- Match code focus: `context-manager` not `context-code`

## README Template

Each code example MUST include a README.md with the following structure:

```markdown
# {Example Name}

## Source

**Blog Post:** [{Post Title}](https://acidbath.sh/blog/{post-slug})
**Section:** {Section/Heading in Post}
**Date Extracted:** {YYYY-MM-DD}

## Description

{1-2 paragraph description of what this code does and why it's useful}

## Context

{Explanation of where this fits in the blog post discussion}

## Usage

### Prerequisites

- Python 3.11+
- Dependencies: {list dependencies}

### Installation

\`\`\`bash
# Installation steps
\`\`\`

### Running the Example

\`\`\`bash
# How to run
\`\`\`

## Files

- `{filename}` - {description}
- `{filename}` - {description}

## Key Concepts

- **Concept 1:** {explanation}
- **Concept 2:** {explanation}

## Modifications

To adapt this code for your use case:

1. {modification step 1}
2. {modification step 2}

## Related Examples

- [{Related Example}](../path/to/example)

## Notes

{Any important notes, limitations, or caveats}
```

## Manifest Schema

The `manifest.json` file maps blog posts to their extracted code examples:

```json
{
  "version": "1.0",
  "generated": "2025-12-23T10:00:00Z",
  "posts": {
    "agent-architecture.md": {
      "title": "Building Multi-Agent Architectures",
      "path": "src/content/blog/agent-architecture.md",
      "total_blocks": 26,
      "extracted_examples": [
        {
          "name": "multi-agent-orchestrator",
          "category": "agentic-patterns",
          "path": "examples/agentic-patterns/agent-architecture/multi-agent-orchestrator",
          "language": "python",
          "lines": 87,
          "section": "## Implementing the Orchestrator",
          "description": "Complete multi-agent orchestration system with task distribution"
        }
      ]
    }
  },
  "statistics": {
    "total_posts": 7,
    "total_examples_extracted": 14,
    "by_category": {
      "agentic-patterns": 6,
      "production-patterns": 5,
      "workflow-tools": 2,
      "configurations": 1
    },
    "by_language": {
      "python": 10,
      "typescript": 2,
      "bash": 1,
      "yaml": 1
    }
  }
}
```

## Code Categorization Rules

### Complete Example (Extract)
- **Criteria:**
  - ≥40 lines of code
  - Self-contained, runnable code
  - Demonstrates a complete concept
  - Requires multiple files or complex setup

- **Action:** Extract to acidbath-code repository

### Medium Example (Context-Dependent)
- **Criteria:**
  - 21-39 lines of code
  - May or may not be self-contained
  - Could be educational or functional

- **Action:** Evaluate context:
  - Extract if: Core to post thesis, reusable, complex
  - Keep inline if: Illustrative only, simple, one-off

### Snippet (Keep Inline)
- **Criteria:**
  - ≤20 lines of code
  - Illustrates a single concept
  - Not meant to be run standalone

- **Action:** Keep in blog post for readability

### Diagram (Special Handling)
- **Criteria:**
  - Mermaid diagrams
  - ASCII art
  - Diff visualizations

- **Action:** Keep in blog post (not extracted)

### Configuration (Extract if Reusable)
- **Criteria:**
  - JSON, YAML, TOML, ENV files
  - Complete configuration examples

- **Action:**
  - Extract if: Template, reusable, complex
  - Keep inline if: Simple, one-off, illustrative

## Validation Requirements

### Python Code
```bash
# Syntax validation
python -m py_compile {file}

# Optional: Linting (if dependencies available)
pylint {file}
```

### Bash Scripts
```bash
# Shellcheck validation
shellcheck {file}
```

### JSON/YAML
```python
# Schema validation
import json
import yaml

# Validate JSON
with open('config.json') as f:
    json.load(f)

# Validate YAML
with open('config.yaml') as f:
    yaml.safe_load(f)
```

### Links
```python
# Verify GitHub links resolve
import requests

response = requests.head(url)
assert response.status_code == 200
```

## Migration Strategy

### Phase 1: High-Value Extraction
Extract from top 4 posts with most complete examples:
1. directory-watchers.md (4 complete examples)
2. document-generation-skills.md (4 complete examples)
3. agent-architecture.md (3 complete examples)
4. context-engineering.md (1 complete example)

### Phase 2: Medium Examples Evaluation
Review 15 medium examples (21-39 lines) and extract if:
- Core to post's main argument
- Highly reusable
- Complex enough to benefit from isolation

### Phase 3: Remaining Posts
Process remaining posts:
- single-file-scripts.md
- workflow-prompts.md
- claude-skills-deep-dive.md

## Repository Health Checks

### Required for Each Example
- ✅ README.md with complete metadata
- ✅ Source code passes syntax validation
- ✅ Referenced in manifest.json
- ✅ Category is correct
- ✅ Files are properly named

### Repository-Wide
- ✅ All examples have unique names
- ✅ manifest.json is valid JSON
- ✅ CI validation workflow passes
- ✅ All blog post links resolve
- ✅ No orphaned examples (not in manifest)

## Future Enhancements

1. **Versioning:** Track code example versions as blog posts evolve
2. **Testing:** Add automated tests for extracted code
3. **Interactive:** Embed Replit/CodeSandbox for browser execution
4. **Search:** Build search index for code examples
5. **Analytics:** Track which examples are most accessed
6. **Bidirectional Sync:** Update blog when code repository changes
7. **Multi-Language:** Extend to Go, Rust, TypeScript, etc.

## Notes

- **Threshold Rationale:** 20-line inline threshold balances context with readability
- **Structure Rationale:** Category → Post → Example organization maintains clear lineage
- **Validation Rationale:** Syntax-only validation avoids security and dependency issues
- **Sync Strategy:** Manual via commands initially; can automate later if needed
