#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
#   "pyyaml>=6.0.0",
# ]
# ///
"""
Jerry Pattern Sync Tool

Syncs Fabric patterns from local Fabric installation to Jerry's pattern directory.
Supports incremental sync, category filtering, and dry-run mode.

Usage:
    ./adws/jerry_sync_patterns.py --list
    ./adws/jerry_sync_patterns.py
    ./adws/jerry_sync_patterns.py --category youtube
    ./adws/jerry_sync_patterns.py --pattern extract_wisdom
    ./adws/jerry_sync_patterns.py --dry-run
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()

# Constants
FABRIC_PATTERNS_DIR = Path.home() / ".config" / "fabric" / "patterns"
JERRY_ROOT = Path(__file__).parent.parent
JERRY_PATTERNS_DIR = JERRY_ROOT / ".jerry" / "patterns"
MANIFEST_PATH = JERRY_PATTERNS_DIR / "manifest.json"

# Pattern categories and their bundled patterns
BUNDLED_PATTERNS = {
    "core": [
        "extract_wisdom",
        "extract_insights",
        "extract_recommendations",
        "rate_content",
        "create_summary",
        "create_5_sentence_summary",
        "extract_references",
    ],
    "youtube": [
        "youtube_summary",
        "extract_youtube_metadata",
        "get_wow_per_minute",
        "extract_agent_opportunities",
    ],
    "technical": [
        "extract_technical_content",
        "review_code",
        "extract_poc",
        "analyze_terraform_plan",
        "analyze_logs",
    ],
    "educational": [
        "extract_educational_value",
        "create_knowledge_artifacts",
        "create_flash_cards",
    ],
    "research": [
        "analyze_paper",
        "analyze_claims",
        "analyze_threat_report",
        "analyze_patent",
        "extract_article_wisdom",
    ],
    "custom": [],
}


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--list", "list_patterns", is_flag=True, help="List available Fabric patterns")
@click.option("--category", help="Sync specific category (core, youtube, technical, educational, research)")
@click.option("--pattern", help="Sync specific pattern by name")
@click.option("--dry-run", is_flag=True, help="Preview changes without writing")
def cli(ctx, list_patterns, category, pattern, dry_run):
    """Jerry Pattern Sync Tool - Sync Fabric patterns to Jerry"""

    if list_patterns:
        list_fabric_patterns()
        ctx.exit(0)

    if ctx.invoked_subcommand is None:
        # Default action: sync patterns
        sync_patterns(category=category, pattern_name=pattern, dry_run=dry_run)


def list_fabric_patterns():
    """List all available Fabric patterns"""
    if not FABRIC_PATTERNS_DIR.exists():
        console.print(f"[red]Error: Fabric not found at {FABRIC_PATTERNS_DIR}[/red]")
        console.print("[yellow]Install Fabric from: https://github.com/danielmiessler/fabric[/yellow]")
        sys.exit(1)

    patterns = discover_fabric_patterns()

    table = Table(title=f"Available Fabric Patterns ({len(patterns)} total)")
    table.add_column("Pattern Name", style="cyan")
    table.add_column("Bundled", style="green")

    # Get list of all bundled pattern names
    bundled_names = []
    for category_patterns in BUNDLED_PATTERNS.values():
        bundled_names.extend(category_patterns)

    for pattern in sorted(patterns):
        is_bundled = "✓" if pattern in bundled_names else ""
        table.add_row(pattern, is_bundled)

    console.print(table)
    console.print(f"\n[dim]Bundled patterns: {len(bundled_names)}[/dim]")


def discover_fabric_patterns() -> List[str]:
    """Discover all patterns in Fabric installation"""
    if not FABRIC_PATTERNS_DIR.exists():
        return []

    patterns = []
    for item in FABRIC_PATTERNS_DIR.iterdir():
        if item.is_dir() and (item / "system.md").exists():
            patterns.append(item.name)

    return patterns


def sync_patterns(category: Optional[str] = None, pattern_name: Optional[str] = None, dry_run: bool = False):
    """Sync patterns from Fabric to Jerry"""

    # Validation
    if not FABRIC_PATTERNS_DIR.exists():
        console.print(f"[red]Error: Fabric not found at {FABRIC_PATTERNS_DIR}[/red]")
        console.print("[yellow]Install Fabric from: https://github.com/danielmiessler/fabric[/yellow]")
        sys.exit(1)

    if not JERRY_PATTERNS_DIR.exists():
        console.print(f"[red]Error: Jerry patterns directory not found at {JERRY_PATTERNS_DIR}[/red]")
        console.print("[yellow]Run this script from Jerry root directory[/yellow]")
        sys.exit(1)

    # Determine which patterns to sync
    patterns_to_sync = []

    if pattern_name:
        # Sync specific pattern
        found_category = None
        for cat, patterns in BUNDLED_PATTERNS.items():
            if pattern_name in patterns:
                found_category = cat
                break

        if not found_category:
            console.print(f"[red]Error: Pattern '{pattern_name}' not in bundled patterns[/red]")
            sys.exit(1)

        patterns_to_sync.append((found_category, pattern_name))

    elif category:
        # Sync specific category
        if category not in BUNDLED_PATTERNS:
            console.print(f"[red]Error: Unknown category '{category}'[/red]")
            console.print(f"[yellow]Valid categories: {', '.join(BUNDLED_PATTERNS.keys())}[/yellow]")
            sys.exit(1)

        for pattern in BUNDLED_PATTERNS[category]:
            patterns_to_sync.append((category, pattern))

    else:
        # Sync all bundled patterns
        for cat, patterns in BUNDLED_PATTERNS.items():
            for pattern in patterns:
                patterns_to_sync.append((cat, pattern))

    if dry_run:
        console.print("[yellow]DRY RUN MODE - No files will be written[/yellow]\n")

    # Sync patterns
    synced_count = 0
    skipped_count = 0
    error_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Syncing {len(patterns_to_sync)} patterns...", total=len(patterns_to_sync))

        for cat, pattern in patterns_to_sync:
            progress.update(task, description=f"Syncing {pattern}...")

            result = sync_pattern(pattern, cat, dry_run)

            if result["status"] == "synced":
                synced_count += 1
                console.print(f"[green]✓[/green] {pattern} ({cat})")
            elif result["status"] == "skipped":
                skipped_count += 1
                console.print(f"[dim]○[/dim] {pattern} ({cat}) - unchanged")
            else:
                error_count += 1
                console.print(f"[red]✗[/red] {pattern} ({cat}) - {result.get('error', 'unknown error')}")

            progress.advance(task)

    # Summary
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Synced: {synced_count}")
    console.print(f"  Skipped: {skipped_count}")
    console.print(f"  Errors: {error_count}")

    if not dry_run and synced_count > 0:
        console.print(f"\n[green]Successfully synced {synced_count} patterns![/green]")


def sync_pattern(pattern_name: str, category: str, dry_run: bool = False) -> Dict:
    """Sync a single pattern from Fabric to Jerry"""

    fabric_pattern_dir = FABRIC_PATTERNS_DIR / pattern_name
    jerry_pattern_dir = JERRY_PATTERNS_DIR / category / pattern_name

    # Check if pattern exists in Fabric
    if not fabric_pattern_dir.exists():
        return {"status": "error", "error": "Pattern not found in Fabric"}

    system_md_path = fabric_pattern_dir / "system.md"
    if not system_md_path.exists():
        return {"status": "error", "error": "system.md not found"}

    # Read files from Fabric
    system_md_content = system_md_path.read_text()

    user_md_content = None
    user_md_path = fabric_pattern_dir / "user.md"
    if user_md_path.exists():
        user_md_content = user_md_path.read_text()

    # Calculate checksum
    checksum_data = system_md_content
    if user_md_content:
        checksum_data += user_md_content
    checksum = hashlib.sha256(checksum_data.encode()).hexdigest()

    # Check if pattern already exists and is unchanged
    if jerry_pattern_dir.exists():
        meta_json_path = jerry_pattern_dir / "meta.json"
        if meta_json_path.exists():
            try:
                existing_meta = json.loads(meta_json_path.read_text())
                if existing_meta.get("checksum") == f"sha256:{checksum}":
                    return {"status": "skipped"}
            except:
                pass

    if dry_run:
        return {"status": "synced"}

    # Create pattern directory
    jerry_pattern_dir.mkdir(parents=True, exist_ok=True)

    # Write files
    (jerry_pattern_dir / "system.md").write_text(system_md_content)

    files_copied = ["system.md"]
    if user_md_content:
        (jerry_pattern_dir / "user.md").write_text(user_md_content)
        files_copied.append("user.md")

    # Generate metadata
    meta = {
        "name": pattern_name,
        "category": category,
        "description": f"{pattern_name.replace('_', ' ').title()} pattern",
        "fabric_source": str(fabric_pattern_dir),
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "files": files_copied,
        "checksum": f"sha256:{checksum}",
    }

    (jerry_pattern_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    # Update manifest
    update_manifest(pattern_name, category, meta)

    return {"status": "synced", "files": files_copied}


def update_manifest(pattern_name: str, category: str, meta: Dict):
    """Update the pattern manifest with new pattern metadata"""

    # Read current manifest
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text())
    else:
        # Initialize manifest if it doesn't exist
        manifest = {
            "version": "1.0.0",
            "last_synced": "",
            "fabric_version": "1.4.0",
            "source_patterns_count": len(discover_fabric_patterns()),
            "bundled_patterns_count": 0,
            "categories": {cat: {"count": 0, "patterns": []} for cat in BUNDLED_PATTERNS.keys()},
            "patterns": {},
        }

    # Add/update pattern entry
    manifest["patterns"][pattern_name] = meta

    # Update category
    if pattern_name not in manifest["categories"][category]["patterns"]:
        manifest["categories"][category]["patterns"].append(pattern_name)
    manifest["categories"][category]["count"] = len(manifest["categories"][category]["patterns"])

    # Update counts and timestamp
    manifest["bundled_patterns_count"] = len(manifest["patterns"])
    manifest["last_synced"] = datetime.now(timezone.utc).isoformat()
    manifest["source_patterns_count"] = len(discover_fabric_patterns())

    # Write manifest
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    cli()
