#!/usr/bin/env -S uv run
# /// script
# dependencies = ["click", "rich", "pydantic"]
# ///

"""
ADW Transform Code Refs - Transform blog posts to use code repository references

Usage:
  uv run adw_transform_code_refs.py [options]

Options:
  --post, -p       Transform specific post (e.g., 'agent-architecture.md')
  --all            Transform all blog posts
  --dry-run        Show changes without writing
  --threshold      Line threshold for replacement (default: 30)
  --preview        Show before/after preview
  --backup         Create backup files before transforming

Examples:
  ./adw_transform_code_refs.py --all --dry-run
  ./adw_transform_code_refs.py --post agent-architecture.md --preview
  ./adw_transform_code_refs.py --all --threshold 25
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Constants
ACIDBATH_CODE_LOCAL = Path.home() / "dev" / "acidbath-code"
BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"
# Root-level categories, no examples/ prefix
GITHUB_BASE_URL = "https://github.com/ameno-/acidbath-code/tree/main"


@dataclass
class CodeBlockMatch:
    """Represents a code block found in markdown."""
    start: int
    end: int
    language: str
    code: str
    line_count: int
    context: str
    line_number: int


@dataclass
class Replacement:
    """Represents a code block replacement."""
    original: str
    replacement: str
    language: str
    line_count: int
    example_path: Optional[str]
    reason: str


def load_manifest() -> Dict[str, Any]:
    """Load the manifest from acidbath-code repository."""
    manifest_path = ACIDBATH_CODE_LOCAL / "manifest.json"

    if not manifest_path.exists():
        console.print("[yellow]Warning: manifest.json not found in acidbath-code[/yellow]")
        return {"posts": {}}

    return json.loads(manifest_path.read_text())


def find_code_blocks(content: str) -> List[CodeBlockMatch]:
    """Find all code blocks in markdown content."""
    blocks = []
    pattern = r'```(\w*)\n(.*?)```'
    lines = content.split('\n')

    for match in re.finditer(pattern, content, re.DOTALL):
        language = match.group(1) or 'unknown'
        code = match.group(2)
        line_count = len(code.strip().split('\n'))

        start_pos = match.start()
        line_num = content[:start_pos].count('\n') + 1

        # Extract context (previous heading)
        context = ""
        for i in range(line_num - 1, max(0, line_num - 50), -1):
            if i < len(lines) and lines[i].startswith('#'):
                context = lines[i].strip()
                break

        blocks.append(CodeBlockMatch(
            start=match.start(),
            end=match.end(),
            language=language,
            code=code,
            line_count=line_count,
            context=context,
            line_number=line_num,
        ))

    return blocks


def find_matching_example(
    block: CodeBlockMatch,
    post_slug: str,
    manifest: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Find a matching example in the manifest for a code block."""
    post_data = manifest.get("posts", {}).get(post_slug)

    if not post_data:
        return None

    # Try to match by context and language
    for example in post_data.get("extracted_examples", []):
        # Match by similar context
        example_section = example.get("section", "").lower()
        block_context = block.context.lower()

        # Check if contexts overlap
        if example_section and block_context:
            # Extract key words for comparison
            example_words = set(example_section.lstrip('#').strip().split())
            context_words = set(block_context.lstrip('#').strip().split())

            if example_words & context_words:  # Intersection
                if example.get("language") == block.language:
                    return example

    return None


def generate_callout(
    example: Dict[str, Any],
    block: CodeBlockMatch,
    keep_snippet: bool = True
) -> str:
    """Generate a callout box for a code example."""
    path = example["path"]
    name = example["name"].replace("-", " ").title()
    language = example["language"]
    lines = example["lines"]

    url = f"{GITHUB_BASE_URL}/{path}"

    # Determine callout type based on content
    if lines >= 50 or language in ["yaml", "json"]:
        icon = ""
        label = "Complete Example"
    else:
        icon = ""
        label = "See Full Implementation"

    callout_lines = [
        f"> **{icon} {label}:** [{name}]({url})",
        ">",
    ]

    # Add description
    section = example.get("section", "").lstrip("#").strip()
    if section:
        callout_lines.append(f"> Complete implementation from the '{section}' section.")
    else:
        callout_lines.append(f"> Complete {language} implementation with {lines} lines.")

    callout_lines.extend([
        ">",
        f"> **Language:** {language} | **Lines:** {lines}",
    ])

    return "\n".join(callout_lines)


def generate_hybrid_replacement(
    block: CodeBlockMatch,
    example: Dict[str, Any],
    max_snippet_lines: int = 15
) -> str:
    """Generate a hybrid replacement with snippet + callout."""
    code_lines = block.code.strip().split('\n')

    # Extract a meaningful snippet (first function/class or opening lines)
    snippet_lines = []
    in_def = False

    for i, line in enumerate(code_lines[:max_snippet_lines]):
        snippet_lines.append(line)

        # Stop at first complete function/class if we have enough
        if in_def and not line.strip() and i > 5:
            break
        if line.strip().startswith(('def ', 'class ', 'async def ')):
            in_def = True

    # If snippet is still too long, just take first few lines
    if len(snippet_lines) > max_snippet_lines:
        snippet_lines = snippet_lines[:max_snippet_lines - 1]
        snippet_lines.append("# ... continued in full example")

    snippet = '\n'.join(snippet_lines)

    # Build replacement
    result_lines = [
        f"```{block.language}",
        snippet,
        "```",
        "",
        generate_callout(example, block, keep_snippet=True),
    ]

    return '\n'.join(result_lines)


def transform_post(
    post_path: Path,
    manifest: Dict[str, Any],
    threshold: int = 30,
    dry_run: bool = False,
    backup: bool = False,
) -> List[Replacement]:
    """Transform a blog post to use code repository references."""
    content = post_path.read_text()
    post_slug = post_path.stem

    replacements = []
    blocks = find_code_blocks(content)

    # Sort blocks by position (reverse to preserve positions during replacement)
    blocks_sorted = sorted(blocks, key=lambda b: b.start, reverse=True)

    new_content = content

    for block in blocks_sorted:
        # Skip small blocks
        if block.line_count <= threshold:
            continue

        # Skip diagrams
        if block.language in ['mermaid', 'diff']:
            continue

        # Find matching example
        example = find_matching_example(block, post_slug, manifest)

        if example:
            # Generate replacement
            original = content[block.start:block.end]
            replacement = generate_hybrid_replacement(block, example)

            replacements.append(Replacement(
                original=original,
                replacement=replacement,
                language=block.language,
                line_count=block.line_count,
                example_path=example["path"],
                reason="Matched to extracted example",
            ))

            # Apply replacement
            new_content = new_content[:block.start] + replacement + new_content[block.end:]
        else:
            # No match found - mark for manual review
            replacements.append(Replacement(
                original=content[block.start:block.end][:100] + "...",
                replacement="",
                language=block.language,
                line_count=block.line_count,
                example_path=None,
                reason="No matching example found - needs manual extraction",
            ))

    # Write transformed content
    if not dry_run and replacements:
        # Filter to only applied replacements
        applied = [r for r in replacements if r.example_path]

        if applied:
            if backup:
                backup_path = post_path.with_suffix('.md.bak')
                backup_path.write_text(content)

            post_path.write_text(new_content)

    return replacements


def preview_replacement(replacement: Replacement) -> None:
    """Show a preview of a replacement."""
    console.print(Panel(
        replacement.original[:200] + ("..." if len(replacement.original) > 200 else ""),
        title="[red]Original[/red]",
        border_style="red",
    ))

    if replacement.replacement:
        console.print(Panel(
            replacement.replacement[:300] + ("..." if len(replacement.replacement) > 300 else ""),
            title="[green]Replacement[/green]",
            border_style="green",
        ))
    else:
        console.print(f"[yellow]No replacement: {replacement.reason}[/yellow]")


@click.command()
@click.option(
    "--post", "-p",
    default=None,
    help="Transform specific post",
)
@click.option(
    "--all", "process_all",
    is_flag=True,
    help="Transform all blog posts",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show changes without writing",
)
@click.option(
    "--threshold",
    default=30,
    help="Line threshold for replacement (default: 30)",
)
@click.option(
    "--preview",
    is_flag=True,
    help="Show before/after preview",
)
@click.option(
    "--backup",
    is_flag=True,
    help="Create backup files",
)
def main(
    post: Optional[str],
    process_all: bool,
    dry_run: bool,
    threshold: int,
    preview: bool,
    backup: bool,
):
    """Transform blog posts to use code repository references."""

    if not post and not process_all:
        console.print("[red]Error: Specify --post or --all[/red]")
        sys.exit(1)

    # Load manifest
    manifest = load_manifest()

    if not manifest.get("posts"):
        console.print("[red]Error: No posts in manifest. Run extraction first.[/red]")
        sys.exit(1)

    # Get posts to process
    if post:
        posts = [BLOG_DIR / post] if (BLOG_DIR / post).exists() else []
        if not posts:
            posts = [p for p in BLOG_DIR.glob("*.md") if p.stem == post.replace(".md", "")]
    else:
        posts = sorted(BLOG_DIR.glob("*.md"))

    if not posts:
        console.print("[red]No blog posts found[/red]")
        sys.exit(1)

    console.print(f"\n[bold]Blog Post Transformation[/bold]")
    console.print(f"Posts to process: {len(posts)}")
    console.print(f"Threshold: {threshold} lines")
    console.print(f"Dry run: {dry_run}\n")

    all_replacements = []

    for post_path in posts:
        console.print(f"[cyan]Processing: {post_path.name}[/cyan]")

        replacements = transform_post(
            post_path,
            manifest,
            threshold=threshold,
            dry_run=dry_run,
            backup=backup,
        )

        if replacements:
            applied = [r for r in replacements if r.example_path]
            pending = [r for r in replacements if not r.example_path]

            console.print(f"  Applied: {len(applied)}, Pending manual: {len(pending)}")

            if preview:
                for r in applied[:2]:  # Show first 2 previews
                    preview_replacement(r)
        else:
            console.print("  [dim]No replacements needed[/dim]")

        all_replacements.extend(replacements)

    # Summary
    console.print("\n[bold]Summary[/bold]")

    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Count", justify="right")

    applied = [r for r in all_replacements if r.example_path]
    pending = [r for r in all_replacements if not r.example_path]

    table.add_row("Total code blocks processed", str(len(all_replacements)))
    table.add_row("Replaced with references", str(len(applied)))
    table.add_row("Need manual extraction", str(len(pending)))

    console.print(table)

    if dry_run:
        console.print("\n[yellow]This was a dry run. No files were modified.[/yellow]")
    elif applied:
        console.print("\n[green]Blog posts updated with code references![/green]")

    if pending:
        console.print("\n[yellow]Some code blocks need manual extraction:[/yellow]")
        for r in pending[:5]:
            console.print(f"  - {r.language} ({r.line_count} lines): {r.reason}")


if __name__ == "__main__":
    main()
