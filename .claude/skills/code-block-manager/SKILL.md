---
name: code-block-manager
description: Manage code block extraction, synchronization, and validation between ACIDBATH blog posts and the acidbath-code repository. Use when working with code examples in blog posts.
---

# Code Block Manager

Comprehensive skill for managing code examples across ACIDBATH blog posts and the acidbath-code repository.

## Overview

The ACIDBATH blog maintains a companion repository (`acidbath-code`) containing complete, runnable code examples extracted from blog posts. This skill helps manage the bidirectional synchronization between blog content and the code repository.

## Quick Reference

| Task | Command |
|------|---------|
| Extract code from posts | `uv run ./adws/adw_extract_code_blocks.py --all` |
| Transform posts with refs | `uv run ./adws/adw_transform_code_refs.py --all` |
| View manifest | `cat ~/dev/acidbath-code/manifest.json` |
| Validate code | `uv run ./adws/adw_modules/code_validator.py` |

## Code Organization Schema

### Repository Structure

Categories are at the root level (not under `examples/`):

```
acidbath-code/
├── agentic-patterns/           # AI agent patterns
│   ├── agent-architecture/
│   ├── context-engineering/
│   └── claude-skills-deep-dive/
├── production-patterns/        # Production-ready code
│   ├── directory-watchers/
│   └── document-generation-skills/
├── workflow-tools/             # Utility scripts
│   ├── single-file-scripts/
│   └── workflow-prompts/
├── scripts/
│   └── validate-all.py
└── manifest.json               # Blog-to-code mapping
```

### Category Assignment
- **agentic-patterns**: Posts about AI agents, Claude, context engineering
- **production-patterns**: Posts about real-world implementation
- **workflow-tools**: Posts about automation, scripts, utilities

## Extraction Workflow

### Step 1: Audit Code Blocks
```bash
uv run ./scripts/audit_code_blocks.py
```
Generates `specs/code-block-audit-report.md` with statistics.

### Step 2: Extract Complete Examples
```bash
uv run ./adws/adw_extract_code_blocks.py --all
```
Extracts code blocks ≥40 lines to acidbath-code.

### Step 3: Transform Blog Posts
```bash
uv run ./adws/adw_transform_code_refs.py --all
```
Replaces long code blocks with repository references.

## Categorization Rules

| Category | Line Count | Action |
|----------|-----------|--------|
| Complete Example | ≥40 lines | Extract to acidbath-code |
| Medium Example | 21-39 lines | Consider extraction |
| Snippet | ≤20 lines | Keep inline |
| Diagram | Any (mermaid/diff) | Keep inline |

## Reference Format

When a long code block is replaced, we use this format:

```markdown
\`\`\`python
# First 15 lines of code as preview
def main():
    # ...
\`\`\`

> ** Complete Example:** [Example Name](https://github.com/ameno-/acidbath-code/tree/main/agentic-patterns/...)
> Description of what this code does.
> **Language:** python | **Lines:** 87
```

## Validation

### Python Code
```python
from adws.adw_modules.code_validator import validate_python
result = validate_python(code)
print(f"Valid: {result.valid}, Message: {result.message}")
```

### All Languages
```python
from adws.adw_modules.code_validator import validate_code_block
result = validate_code_block(code, language)
```

### Directory Validation
```bash
# Validate all code in acidbath-code
python3 -c "
from pathlib import Path
from adws.adw_modules.code_validator import validate_directory, generate_validation_report

results = validate_directory(Path('~/dev/acidbath-code').expanduser())
print(generate_validation_report(results))
"
```

## Manifest Schema

The `manifest.json` maps blog posts to extracted examples:

```json
{
  "version": "1.0",
  "generated": "2025-12-23T10:00:00Z",
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
    "total_examples_extracted": 14
  }
}
```

## Integration Points

### With /new-post
After creating a new blog post:
1. Run `/extract-code {post-name}.md` to extract examples
2. Run `/sync-code-blocks {post-name}.md` to add references

### With /review
Code review should check:
- All code references link to valid paths
- No inline blocks exceed 30 lines
- Manifest is up-to-date

### With /ai-audit
Content audit should verify:
- POC rule maintained (all code accessible)
- Code examples have READMEs
- No broken links

## Common Tasks

### Add New Code Example
1. Write code block in blog post
2. Run extraction: `uv run ./adws/adw_extract_code_blocks.py --post {post}.md`
3. Transform post: `uv run ./adws/adw_transform_code_refs.py --post {post}.md`
4. Commit both repositories

### Update Existing Example
1. Edit code in acidbath-code repository
2. Update manifest if needed
3. Blog post references remain valid

### Remove Example
1. Delete from acidbath-code
2. Remove from manifest
3. Update blog post to inline the code or remove reference

## Troubleshooting

### "No matching example found"
The extraction and transformation work independently. Run extraction first:
```bash
uv run ./adws/adw_extract_code_blocks.py --all
```

### "Manifest not found"
Clone or pull the acidbath-code repository:
```bash
git clone https://github.com/ameno-/acidbath-code.git ~/dev/acidbath-code
```

### Validation Failures
Check specific file:
```python
from adws.adw_modules.code_validator import validate_file
result = validate_file(Path("path/to/file.py"))
print(result.details if not result.valid else "Valid!")
```

## Resources

- **Manifest**: `~/dev/acidbath-code/manifest.json`
- **Extraction Script**: `adws/adw_extract_code_blocks.py`
- **Transform Script**: `adws/adw_transform_code_refs.py`
- **Validation Module**: `adws/adw_modules/code_validator.py`
- **Extraction Module**: `adws/adw_modules/code_extraction.py`
- **Schema Spec**: `specs/code-block-organization-schema.md`
- **Reference Spec**: `specs/code-reference-format-spec.md`
