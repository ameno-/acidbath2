# Code Repository Integration Guide

## Overview

ACIDBATH blog maintains a companion repository (`acidbath-code`) that hosts complete, runnable code examples extracted from blog posts. This guide explains how the integration works and how to use it.

## Architecture

```
acidbath2/                      acidbath-code/
├── src/content/blog/           ├── agentic-patterns/
│   ├── agent-architecture.md   │   ├── agent-architecture/
│   └── ...                     │   └── context-engineering/
├── adws/                       ├── production-patterns/
│   ├── adw_extract_code_blocks.py  │   ├── directory-watchers/
│   └── adw_transform_code_refs.py  │   └── document-generation-skills/
└── .claude/commands/           ├── workflow-tools/
    ├── extract-code.md         │   ├── single-file-scripts/
    └── sync-code-blocks.md     │   └── workflow-prompts/
                                └── manifest.json
```

## Why Separate Code Repository?

1. **Improved Readability**: Long code blocks (>30 lines) disrupt reading flow
2. **Maintainability**: Code examples can be tested and updated independently
3. **POC Rule Compliance**: All code remains accessible via one click
4. **Validation**: CI/CD can validate code syntax and functionality

## Quick Start

### Extract Code from a New Post
```bash
# Extract complete examples to acidbath-code
uv run ./adws/adw_extract_code_blocks.py --post your-new-post.md

# Transform post to use references
uv run ./adws/adw_transform_code_refs.py --post your-new-post.md
```

### Extract All Code
```bash
uv run ./adws/adw_extract_code_blocks.py --all
uv run ./adws/adw_transform_code_refs.py --all
```

### Using Slash Commands
```
/extract-code agent-architecture.md
/sync-code-blocks agent-architecture.md
```

## Code Block Categorization

| Category | Line Count | Action |
|----------|-----------|--------|
| Snippet | ≤20 lines | Keep inline |
| Medium Example | 21-39 lines | Consider extraction |
| Complete Example | ≥40 lines | Extract to repository |
| Diagram | Any (mermaid/diff) | Keep inline |

## Repository Structure

Categories are at the root level, organized by source post:

```
acidbath-code/
├── agentic-patterns/
│   ├── agent-architecture/
│   │   ├── poc-simplest-custom/
│   │   │   ├── README.md
│   │   │   └── poc_simplest_custom.py
│   │   └── poc-agent-custom/
│   │       ├── README.md
│   │       └── poc_agent_custom.py
│   └── context-engineering/
│       └── when-you-need/
│           ├── README.md
│           └── when_you_need.py
├── production-patterns/
│   ├── directory-watchers/
│   └── document-generation-skills/
├── workflow-tools/
│   ├── single-file-scripts/
│   └── workflow-prompts/
└── manifest.json
```

### Category Mapping

- **agentic-patterns**: Posts about AI agents, Claude, context engineering
- **production-patterns**: Posts about real-world implementation patterns
- **workflow-tools**: Posts about automation, scripts, utilities

## Reference Format

When code is extracted, blog posts are updated with this format:

```markdown
\`\`\`python
# First 15 lines showing the key concept
def main():
    """Core implementation."""
    pass
\`\`\`

> ** Complete Example:** [Example Name](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/...)
> Complete implementation from the 'Section Name' section.
> **Language:** python | **Lines:** 87
```

## Manifest Schema

The `manifest.json` file maps blog posts to extracted examples:

```json
{
  "version": "1.0",
  "generated": "2025-12-23T...",
  "posts": {
    "agent-architecture": {
      "title": "Agent Architecture: From Custom Agents to Effective Delegation",
      "path": "src/content/blog/agent-architecture.md",
      "extracted_examples": [
        {
          "name": "poc-agent-custom",
          "category": "agentic-patterns",
          "path": "agentic-patterns/agent-architecture/poc-agent-custom",
          "language": "python",
          "lines": 132,
          "section": "## POC: Building a Custom Agent"
        }
      ]
    }
  },
  "statistics": {
    "total_posts": 6,
    "total_examples_extracted": 14,
    "by_category": {...},
    "by_language": {...}
  }
}
```

## Workflow Integration

### New Post Workflow
1. Write blog post with code examples
2. Run `/extract-code {post}.md`
3. Run `/sync-code-blocks {post}.md`
4. Review and commit both repositories

### Review Workflow
During code review, check:
- Inline code blocks are ≤30 lines
- Code references link to valid paths
- Complete examples have been extracted
- Manifest is up-to-date

### AI Audit Workflow
The audit checks:
- POC Rule compliance (all code accessible)
- Code reference link validity
- Inline code size compliance

## Validation

### Validate Extracted Code
```python
from adws.adw_modules.code_validator import validate_directory
from pathlib import Path

results = validate_directory(Path("~/dev/acidbath-code"))
for path, result in results.items():
    if not result.valid:
        print(f"FAIL: {path} - {result.message}")
```

### Validate Code References
```bash
# Check that all links in blog posts are valid
uv run ./adws/adw_transform_code_refs.py --all --dry-run
```

## Common Tasks

### Add Code to Existing Post
1. Add code block to blog post
2. Run extraction and transformation
3. Commit changes to both repos

### Update Existing Example
1. Edit code in acidbath-code repository
2. Update README if needed
3. Blog post references remain valid

### Remove Example
1. Delete from acidbath-code
2. Remove from manifest
3. Update blog post (inline the code or remove)

## Troubleshooting

### "No matching example found"
The extraction and transformation run independently. Run extraction first:
```bash
uv run ./adws/adw_extract_code_blocks.py --all
```

### "Manifest not found"
Clone acidbath-code:
```bash
git clone https://github.com/ameno-/acidbath-code.git ~/dev/acidbath-code
```

### Code Validation Failures
Check specific file:
```python
from adws.adw_modules.code_validator import validate_file
from pathlib import Path

result = validate_file(Path("path/to/file.py"))
print(result.details if not result.valid else "Valid!")
```

## Related Resources

- **Extraction Script**: `adws/adw_extract_code_blocks.py`
- **Transform Script**: `adws/adw_transform_code_refs.py`
- **Validation Module**: `adws/adw_modules/code_validator.py`
- **Extraction Module**: `adws/adw_modules/code_extraction.py`
- **Organization Schema**: `specs/code-block-organization-schema.md`
- **Reference Format**: `specs/code-reference-format-spec.md`
- **Skill Documentation**: `.claude/skills/code-block-manager/SKILL.md`
