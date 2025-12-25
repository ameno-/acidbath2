---
allowed-tools: Bash, Read, Write, Glob
description: Synchronize code blocks between blog posts and the acidbath-code repository
---

# Sync Code Blocks

Transform blog posts to use references to the acidbath-code repository, and ensure code blocks are synchronized.

## Input
$ARGUMENTS - Optional: specific post to sync, or empty for all posts

## Process

1. **Load Manifest**
   - Read `manifest.json` from acidbath-code repository
   - Verify extraction has been done (run `/extract-code` first if not)

2. **Transform Blog Posts**
   ```bash
   uv run ./adws/adw_transform_code_refs.py --all
   ```
   Or for specific post:
   ```bash
   uv run ./adws/adw_transform_code_refs.py --post "$ARGUMENTS"
   ```

3. **Verify Transformations**
   - Check that code references link to valid paths
   - Ensure inline snippets are preserved
   - Validate callout format

4. **Report Status**
   - Number of code blocks transformed
   - Any blocks needing manual attention
   - Links to updated files

## Options

- `--dry-run` - Preview changes without modifying files
- `--threshold N` - Line count threshold for replacement (default: 30)
- `--preview` - Show before/after comparison
- `--backup` - Create .bak files before modifying

## Examples

```
/sync-code-blocks
/sync-code-blocks agent-architecture.md
/sync-code-blocks --dry-run
```

## Transformation Rules

### Keep Inline (≤30 lines by default)
- Short snippets providing immediate context
- Illustrative examples within text flow
- Single-function demonstrations

### Replace with Reference (>30 lines)
- Complete implementations
- Multi-function examples
- Configuration files
- Full class definitions

### Reference Format

Long code blocks are replaced with a hybrid format:
1. **Short snippet** (first ~15 lines) showing the key concept
2. **Callout box** linking to full implementation

Example:
```markdown
> ** Complete Example:** [Multi-Agent Orchestrator](https://github.com/ameno-/acidbath-code/...)
> Complete implementation from the 'Building Multi-Agent Architectures' section.
> **Language:** python | **Lines:** 132
```

## Workflow

1. First run: `/extract-code all` to populate acidbath-code
2. Then run: `/sync-code-blocks` to transform blog posts
3. Review changes and commit

## Related Commands

- `/extract-code` - Extract code to repository
- `/review` - Review code block references
- `/ai-audit` - Audit code organization compliance
