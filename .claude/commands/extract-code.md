---
allowed-tools: Bash, Read, Write, Glob
description: Extract code blocks from blog posts to the acidbath-code repository
---

# Extract Code Blocks

Extract complete code examples from blog posts and organize them in the acidbath-code repository.

## Input
$ARGUMENTS - Blog post path or "all" to process all posts

## Process

1. **Validate Input**
   - If no argument provided, prompt for post selection
   - Validate the post path exists in `src/content/blog/`

2. **Run Extraction Workflow**
   ```bash
   uv run ./adws/adw_extract_code_blocks.py --post "$ARGUMENTS"
   ```
   Or for all posts:
   ```bash
   uv run ./adws/adw_extract_code_blocks.py --all
   ```

3. **Report Results**
   - Show number of examples extracted
   - List paths in acidbath-code repository
   - Confirm commit and push status

## Options

- `--dry-run` - Preview what would be extracted without making changes
- `--min-lines N` - Set minimum line threshold (default: 40)
- `--include-medium` - Also extract examples with 21-39 lines
- `--no-commit` - Extract locally without committing to remote

## Examples

```
/extract-code agent-architecture.md
/extract-code all
/extract-code agent-architecture.md --dry-run
```

## What Gets Extracted

- **Complete Examples (≥40 lines)**: Full implementations extracted to acidbath-code
- **Medium Examples (21-39 lines)**: Optional, with `--include-medium` flag
- **Snippets (≤20 lines)**: Always kept inline in blog posts
- **Diagrams**: Never extracted (mermaid, diff blocks)

## Output Location

Extracted code is organized in acidbath-code repository:
```
acidbath-code/examples/{category}/{post-slug}/{example-name}/
├── README.md      # Context and usage instructions
└── {code-file}    # The actual code
```

## After Extraction

Consider running `/sync-code-blocks` to update blog posts with references to the extracted code.
