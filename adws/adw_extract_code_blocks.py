#!/usr/bin/env -S uv run
# /// script
# dependencies = ["click", "pyyaml", "rich", "pydantic"]
# ///

"""
ADW Extract Code Blocks - Extract code from blog posts to acidbath-code repository

Usage:
  uv run adw_extract_code_blocks.py [options]

Options:
  --post, -p       Process specific post (e.g., 'agent-architecture.md')
  --all            Process all blog posts
  --dry-run        Show what would be extracted without writing
  --min-lines      Minimum lines for extraction (default: 40)
  --include-medium Include medium examples (21-39 lines)
  --output-dir     Override output directory
  --report         Generate extraction report only
  --no-commit      Don't commit changes to acidbath-code

Examples:
  ./adw_extract_code_blocks.py --all
  ./adw_extract_code_blocks.py --post agent-architecture.md
  ./adw_extract_code_blocks.py --all --dry-run
  ./adw_extract_code_blocks.py --report
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.code_extraction import (
    parse_code_blocks,
    categorize_code_block,
    determine_category_directory,
    generate_example_readme,
    extract_post_metadata,
    get_post_slug,
    CodeBlock,
)
from adws.adw_modules.code_validator import validate_code_block

console = Console()

# Constants
ACIDBATH_CODE_REPO = "https://github.com/ameno-/acidbath-code.git"
ACIDBATH_CODE_LOCAL = Path.home() / "dev" / "acidbath-code"
BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"


def ensure_acidbath_code_repo() -> Path:
    """Ensure acidbath-code repository is cloned locally."""
    if ACIDBATH_CODE_LOCAL.exists():
        # Pull latest changes
        console.print(f"[dim]Updating acidbath-code repository...[/dim]")
        subprocess.run(
            ["git", "pull", "--rebase"],
            cwd=ACIDBATH_CODE_LOCAL,
            capture_output=True,
        )
        return ACIDBATH_CODE_LOCAL

    # Clone the repository
    console.print(f"[yellow]Cloning acidbath-code repository...[/yellow]")
    ACIDBATH_CODE_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", ACIDBATH_CODE_REPO, str(ACIDBATH_CODE_LOCAL)],
        check=True,
    )
    return ACIDBATH_CODE_LOCAL


def get_blog_posts(blog_dir: Path, post_filter: Optional[str] = None) -> List[Path]:
    """Get list of blog posts to process."""
    posts = list(blog_dir.glob("*.md"))

    if post_filter:
        # Filter to specific post
        posts = [p for p in posts if p.name == post_filter or p.stem == post_filter]

    return sorted(posts)


def extract_examples_from_post(
    post_path: Path,
    min_lines: int = 40,
    include_medium: bool = False
) -> List[Dict[str, Any]]:
    """Extract code examples from a blog post."""
    content = post_path.read_text()
    post_slug = get_post_slug(str(post_path))
    metadata = extract_post_metadata(content)
    post_title = metadata.get("title", post_slug.replace("-", " ").title())

    # Parse all code blocks
    blocks = parse_code_blocks(content, str(post_path))

    examples = []
    example_counter = {}  # Track example numbers per category

    for block in blocks:
        category = categorize_code_block(block)

        # Skip diagrams and snippets
        if category == "diagram":
            continue
        if category == "snippet":
            continue
        if category == "medium_example" and not include_medium:
            continue
        if block.line_count < min_lines and not (include_medium and block.line_count >= 21):
            continue

        # Validate the code
        validation = validate_code_block(block.code, block.language)

        # Determine directory category
        dir_category = determine_category_directory(block, post_slug)

        # Generate example name
        base_name = generate_example_name(block, post_slug)

        # Handle duplicate names
        if base_name not in example_counter:
            example_counter[base_name] = 0
        example_counter[base_name] += 1

        if example_counter[base_name] > 1:
            example_name = f"{base_name}-{example_counter[base_name]}"
        else:
            example_name = base_name

        examples.append({
            "block": block,
            "category": dir_category,
            "post_slug": post_slug,
            "post_title": post_title,
            "example_name": example_name,
            "validation": validation,
        })

    return examples


def generate_example_name(block: CodeBlock, post_slug: str) -> str:
    """Generate a descriptive name for a code example."""
    # Extract key words from context
    context = block.context.lower()

    # Remove markdown heading markers
    context = context.lstrip("#").strip()

    # Try to extract meaningful words
    words = context.split()

    # Filter out common words
    stopwords = {"the", "a", "an", "is", "are", "for", "to", "in", "on", "with", "and", "or"}
    keywords = [w for w in words if w not in stopwords and len(w) > 2][:3]

    if keywords:
        name = "-".join(keywords)
    else:
        # Fallback to language + post
        name = f"{block.language}-example"

    # Clean up the name
    name = name.replace("_", "-").replace(" ", "-").lower()

    # Remove special characters
    name = "".join(c for c in name if c.isalnum() or c == "-")

    return name or "example"


def write_example_to_repo(
    example: Dict[str, Any],
    repo_path: Path,
    dry_run: bool = False
) -> Dict[str, Any]:
    """Write a code example to the acidbath-code repository."""
    block: CodeBlock = example["block"]
    category = example["category"]
    post_slug = example["post_slug"]
    example_name = example["example_name"]

    # Create directory path - categories at root level, not under examples/
    example_dir = repo_path / category / post_slug / example_name

    result = {
        "path": str(example_dir.relative_to(repo_path)),
        "files": [],
        "created": False,
    }

    if dry_run:
        result["dry_run"] = True
        return result

    # Create directory
    example_dir.mkdir(parents=True, exist_ok=True)
    result["created"] = True

    # Determine filename based on language
    filename = get_filename_for_language(block.language, example_name)

    # Write code file
    code_file = example_dir / filename
    code_file.write_text(block.code.strip() + "\n")
    result["files"].append(filename)

    # Generate and write README
    readme_content = generate_example_readme(
        example_name=example_name,
        post_title=example["post_title"],
        post_slug=post_slug,
        section_heading=block.context,
        description=f"Code example from the '{block.context}' section demonstrating {block.language} implementation.",
        blocks=[block],
    )

    readme_file = example_dir / "README.md"
    readme_file.write_text(readme_content)
    result["files"].append("README.md")

    return result


def get_filename_for_language(language: str, example_name: str) -> str:
    """Get appropriate filename for language."""
    extensions = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "bash": ".sh",
        "sh": ".sh",
        "yaml": ".yaml",
        "yml": ".yaml",
        "json": ".json",
        "html": ".html",
        "css": ".css",
        "markdown": ".md",
        "md": ".md",
    }

    ext = extensions.get(language.lower(), ".txt")

    # Use snake_case for Python, kebab-case for others
    if language.lower() == "python":
        base = example_name.replace("-", "_")
    else:
        base = example_name

    return base + ext


def update_manifest(
    repo_path: Path,
    examples: List[Dict[str, Any]],
    dry_run: bool = False
) -> Dict[str, Any]:
    """Update the manifest.json file."""
    manifest_path = repo_path / "manifest.json"

    # Load existing manifest or create new one
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    else:
        manifest = {
            "version": "1.0",
            "generated": None,
            "posts": {},
            "statistics": {
                "total_posts": 0,
                "total_examples_extracted": 0,
                "by_category": {},
                "by_language": {},
            },
        }

    # Update manifest with new examples
    for example in examples:
        block: CodeBlock = example["block"]
        post_slug = example["post_slug"]

        # Initialize post entry if needed
        if post_slug not in manifest["posts"]:
            manifest["posts"][post_slug] = {
                "title": example["post_title"],
                "path": f"src/content/blog/{post_slug}.md",
                "total_blocks": 0,
                "extracted_examples": [],
            }

        # Add example to post - path at root level, not under examples/
        manifest["posts"][post_slug]["extracted_examples"].append({
            "name": example["example_name"],
            "category": example["category"],
            "path": f"{example['category']}/{post_slug}/{example['example_name']}",
            "language": block.language,
            "lines": block.line_count,
            "section": block.context,
        })

    # Update statistics
    all_examples = []
    for post_data in manifest["posts"].values():
        all_examples.extend(post_data["extracted_examples"])

    manifest["statistics"]["total_posts"] = len(manifest["posts"])
    manifest["statistics"]["total_examples_extracted"] = len(all_examples)

    # Count by category and language
    by_category = {}
    by_language = {}
    for ex in all_examples:
        cat = ex["category"]
        lang = ex["language"]
        by_category[cat] = by_category.get(cat, 0) + 1
        by_language[lang] = by_language.get(lang, 0) + 1

    manifest["statistics"]["by_category"] = by_category
    manifest["statistics"]["by_language"] = by_language
    manifest["generated"] = datetime.now().isoformat()

    if not dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    return manifest


def commit_changes(repo_path: Path, message: str) -> bool:
    """Commit and push changes to acidbath-code repository."""
    try:
        # Add all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=repo_path,
            check=True,
        )

        # Check if there are changes to commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if not result.stdout.strip():
            console.print("[dim]No changes to commit[/dim]")
            return False

        # Commit changes
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_path,
            check=True,
        )

        # Push changes
        subprocess.run(
            ["git", "push"],
            cwd=repo_path,
            check=True,
        )

        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Git operation failed: {e}[/red]")
        return False


def generate_extraction_report(
    examples: List[Dict[str, Any]],
    output_path: Optional[Path] = None
) -> str:
    """Generate a report of what was/would be extracted."""
    report = []
    report.append("# Code Block Extraction Report\n\n")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Total Examples:** {len(examples)}\n\n")

    # Group by post
    by_post = {}
    for ex in examples:
        post = ex["post_slug"]
        if post not in by_post:
            by_post[post] = []
        by_post[post].append(ex)

    for post_slug, post_examples in sorted(by_post.items()):
        report.append(f"## {post_slug}\n\n")
        report.append(f"**Examples:** {len(post_examples)}\n\n")

        for ex in post_examples:
            block = ex["block"]
            report.append(f"### {ex['example_name']}\n\n")
            report.append(f"- **Category:** {ex['category']}\n")
            report.append(f"- **Language:** {block.language}\n")
            report.append(f"- **Lines:** {block.line_count}\n")
            report.append(f"- **Section:** {block.context}\n")
            report.append(f"- **Validation:** {'Valid' if ex['validation'].valid else ex['validation'].message}\n")
            report.append(f"- **Path:** `examples/{ex['category']}/{post_slug}/{ex['example_name']}`\n\n")

    report_content = "".join(report)

    if output_path:
        output_path.write_text(report_content)
        console.print(f"[green]Report saved to: {output_path}[/green]")

    return report_content


@click.command()
@click.option(
    "--post", "-p",
    default=None,
    help="Process specific post (e.g., 'agent-architecture.md')",
)
@click.option(
    "--all", "process_all",
    is_flag=True,
    help="Process all blog posts",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be extracted without writing",
)
@click.option(
    "--min-lines",
    default=40,
    help="Minimum lines for extraction (default: 40)",
)
@click.option(
    "--include-medium",
    is_flag=True,
    help="Include medium examples (21-39 lines)",
)
@click.option(
    "--output-dir", "-o",
    default=None,
    help="Override output directory",
)
@click.option(
    "--report",
    is_flag=True,
    help="Generate extraction report only",
)
@click.option(
    "--no-commit",
    is_flag=True,
    help="Don't commit changes to acidbath-code",
)
def main(
    post: Optional[str],
    process_all: bool,
    dry_run: bool,
    min_lines: int,
    include_medium: bool,
    output_dir: Optional[str],
    report: bool,
    no_commit: bool,
):
    """Extract code blocks from blog posts to acidbath-code repository."""

    # Determine which posts to process
    if not post and not process_all:
        console.print("[red]Error: Specify --post or --all[/red]")
        sys.exit(1)

    # Get blog posts
    posts = get_blog_posts(BLOG_DIR, post)

    if not posts:
        console.print("[red]No blog posts found[/red]")
        sys.exit(1)

    console.print(f"\n[bold]Code Block Extraction[/bold]")
    console.print(f"Posts to process: {len(posts)}")
    console.print(f"Min lines: {min_lines}")
    console.print(f"Include medium: {include_medium}")
    console.print(f"Dry run: {dry_run}\n")

    # Extract examples from all posts
    all_examples = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting code blocks...", total=len(posts))

        for post_path in posts:
            progress.update(task, description=f"Processing {post_path.name}...")
            examples = extract_examples_from_post(
                post_path,
                min_lines=min_lines,
                include_medium=include_medium,
            )
            all_examples.extend(examples)
            progress.advance(task)

    console.print(f"\n[green]Found {len(all_examples)} examples to extract[/green]\n")

    # Display summary table
    if all_examples:
        table = Table(title="Examples to Extract")
        table.add_column("Post", style="cyan")
        table.add_column("Example", style="green")
        table.add_column("Language", style="yellow")
        table.add_column("Lines", justify="right")
        table.add_column("Valid", justify="center")

        for ex in all_examples:
            block = ex["block"]
            valid_mark = "[green]" if ex["validation"].valid else "[red]"
            table.add_row(
                ex["post_slug"],
                ex["example_name"],
                block.language,
                str(block.line_count),
                valid_mark + "" if ex["validation"].valid else valid_mark + "",
            )

        console.print(table)
        console.print()

    # Report only mode
    if report:
        report_path = Path(__file__).parent.parent / "specs" / "code-block-extraction-report.md"
        generate_extraction_report(all_examples, report_path)
        return

    # Ensure acidbath-code repo is available
    if not dry_run:
        repo_path = ensure_acidbath_code_repo()
    else:
        repo_path = ACIDBATH_CODE_LOCAL

    if output_dir:
        repo_path = Path(output_dir)

    # Write examples to repository
    console.print(f"[bold]Writing to: {repo_path}[/bold]\n")

    written = []
    for ex in all_examples:
        result = write_example_to_repo(ex, repo_path, dry_run=dry_run)
        written.append(result)

        status = "[dim](dry run)[/dim]" if dry_run else "[green]created[/green]"
        console.print(f"  {status} {result['path']}")

    # Update manifest
    manifest = update_manifest(repo_path, all_examples, dry_run=dry_run)

    console.print(f"\n[bold]Manifest updated[/bold]")
    console.print(f"  Total posts: {manifest['statistics']['total_posts']}")
    console.print(f"  Total examples: {manifest['statistics']['total_examples_extracted']}")

    # Commit and push
    if not dry_run and not no_commit:
        console.print("\n[bold]Committing changes...[/bold]")

        post_names = list(set(ex["post_slug"] for ex in all_examples))
        message = f"feat: extract {len(all_examples)} code examples from {', '.join(post_names[:3])}"
        if len(post_names) > 3:
            message += f" (+{len(post_names) - 3} more)"

        if commit_changes(repo_path, message):
            console.print("[green]Changes committed and pushed successfully![/green]")
        else:
            console.print("[yellow]No changes were committed[/yellow]")

    # Final summary
    console.print("\n[bold green]Extraction complete![/bold green]")
    console.print(f"  Examples extracted: {len(all_examples)}")

    if dry_run:
        console.print("\n[yellow]This was a dry run. No files were written.[/yellow]")
        console.print("Run without --dry-run to actually extract code blocks.")


if __name__ == "__main__":
    main()
