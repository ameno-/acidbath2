#!/usr/bin/env -S uv run
# /// script
# dependencies = ["click", "rich", "pydantic"]
# ///

"""
ADW Brainstorm - Manage brainstorm analysis manifest and history

Usage:
  uv run adw_brainstorm.py list                    - List all analyses
  uv run adw_brainstorm.py status <slug>           - Show analysis details
  uv run adw_brainstorm.py versions <slug>         - Show version history
  uv run adw_brainstorm.py link <slug> <path>      - Link to blog post
  uv run adw_brainstorm.py diff <slug> <v1> <v2>   - Show diff between versions
"""

import sys
import os

import click
from rich.console import Console
from rich.table import Table

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.brainstorm_ops import (
    get_brainstorm_dir,
    load_manifest,
    update_blog_status,
)
from adws.adw_modules.diff_ops import generate_diff_summary

console = Console()


@click.group()
def cli():
    """Manage brainstorm analysis manifest and history."""
    pass


@cli.command("list")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def list_analyses(output_json: bool):
    """List all analyses in brainstorm directory."""
    try:
        manifest = load_manifest()
    except Exception as e:
        console.print(f"[red]Error loading manifest: {e}[/red]")
        sys.exit(1)

    if output_json:
        import json
        print(json.dumps(manifest.model_dump(mode='json'), indent=2, default=str))
        return

    if not manifest.analyses:
        console.print("[yellow]No analyses found. Run /analyze with --brainstorm to create one.[/yellow]")
        return

    table = Table(title=f"Brainstorm Analyses ({manifest.total_analyses})")
    table.add_column("Slug", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Type", style="green")
    table.add_column("Versions", style="yellow")
    table.add_column("Latest", style="magenta")
    table.add_column("Blog", style="blue")

    for slug, entry in manifest.analyses.items():
        table.add_row(
            slug,
            entry.title[:40] + "..." if len(entry.title) > 40 else entry.title,
            entry.source.type,
            str(len(entry.versions)),
            entry.latest_version or "-",
            entry.blog_status or "none"
        )

    console.print(table)
    console.print(f"\nBrainstorm directory: {get_brainstorm_dir()}")


@cli.command("status")
@click.argument("slug")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def show_status(slug: str, output_json: bool):
    """Show detailed status for a specific analysis."""
    try:
        manifest = load_manifest()
    except Exception as e:
        console.print(f"[red]Error loading manifest: {e}[/red]")
        sys.exit(1)

    if slug not in manifest.analyses:
        console.print(f"[red]Analysis '{slug}' not found[/red]")
        sys.exit(1)

    entry = manifest.analyses[slug]

    if output_json:
        import json
        print(json.dumps(entry.model_dump(mode='json'), indent=2, default=str))
        return

    console.print(f"\n[bold cyan]Analysis: {slug}[/bold cyan]\n")
    console.print(f"[bold]Title:[/bold] {entry.title}")
    console.print(f"[bold]Source Type:[/bold] {entry.source.type}")
    console.print(f"[bold]Source URL:[/bold] {entry.source.url}")
    console.print(f"[bold]Original Title:[/bold] {entry.source.original_title}")
    console.print(f"[bold]Latest Version:[/bold] {entry.latest_version}")
    console.print(f"[bold]Total Versions:[/bold] {len(entry.versions)}")
    console.print(f"[bold]Blog Status:[/bold] {entry.blog_status or 'none'}")
    if entry.blog_post:
        console.print(f"[bold]Blog Post:[/bold] {entry.blog_post}")
    if entry.tags:
        console.print(f"[bold]Tags:[/bold] {', '.join(entry.tags)}")

    console.print(f"\n[bold]Directory:[/bold] {get_brainstorm_dir() / slug}")


@cli.command("versions")
@click.argument("slug")
def show_versions(slug: str):
    """Show version history for an analysis."""
    try:
        manifest = load_manifest()
    except Exception as e:
        console.print(f"[red]Error loading manifest: {e}[/red]")
        sys.exit(1)

    if slug not in manifest.analyses:
        console.print(f"[red]Analysis '{slug}' not found[/red]")
        sys.exit(1)

    entry = manifest.analyses[slug]

    if not entry.versions:
        console.print("[yellow]No versions found[/yellow]")
        return

    table = Table(title=f"Versions for {slug}")
    table.add_column("Version", style="cyan")
    table.add_column("Date", style="white")
    table.add_column("Preset", style="green")
    table.add_column("Model", style="yellow")
    table.add_column("Patterns", style="magenta")
    table.add_column("Diff From", style="blue")

    for version in entry.versions:
        table.add_row(
            version.version,
            str(version.date)[:19] if version.date else "-",
            version.preset or "-",
            version.model or "-",
            str(len(version.patterns_run)) if version.patterns_run else "0",
            version.diff_from or "-"
        )

    console.print(table)

    if entry.versions:
        latest = entry.versions[-1]
        if latest.changes_summary:
            console.print(f"\n[bold]Latest changes:[/bold] {latest.changes_summary}")


@cli.command("link")
@click.argument("slug")
@click.argument("blog_path")
@click.option("--status", default="published", help="Blog status (draft/published/archived)")
def link_blog(slug: str, blog_path: str, status: str):
    """Link an analysis to a blog post."""
    try:
        manifest = load_manifest()
    except Exception as e:
        console.print(f"[red]Error loading manifest: {e}[/red]")
        sys.exit(1)

    if slug not in manifest.analyses:
        console.print(f"[red]Analysis '{slug}' not found[/red]")
        sys.exit(1)

    valid_statuses = ["draft", "published", "archived"]
    if status not in valid_statuses:
        console.print(f"[red]Invalid status. Must be one of: {', '.join(valid_statuses)}[/red]")
        sys.exit(1)

    try:
        update_blog_status(slug, status, blog_path)
        console.print(f"[green]Linked {slug} to {blog_path} (status: {status})[/green]")
    except Exception as e:
        console.print(f"[red]Error updating manifest: {e}[/red]")
        sys.exit(1)


@cli.command("diff")
@click.argument("slug")
@click.argument("old_version")
@click.argument("new_version")
def show_diff(slug: str, old_version: str, new_version: str):
    """Show diff between two versions of an analysis."""
    try:
        manifest = load_manifest()
    except Exception as e:
        console.print(f"[red]Error loading manifest: {e}[/red]")
        sys.exit(1)

    if slug not in manifest.analyses:
        console.print(f"[red]Analysis '{slug}' not found[/red]")
        sys.exit(1)

    try:
        full_diff, brief = generate_diff_summary(slug, old_version, new_version)
        console.print(full_diff)
        console.print(f"\n[bold]Summary:[/bold] {brief}")
    except ValueError as e:
        console.print(f"[red]Error generating diff: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
