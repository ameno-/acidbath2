#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
#   "pyyaml>=6.0.0",
# ]
# ///
"""
Jerry Export Script

Exports Jerry framework to a distributable package with manifest and checksums.

Usage:
    ./adws/jerry_export.py --output /tmp/jerry-export --format tar.gz
    ./adws/jerry_export.py --output /tmp/jerry-export --format zip --include-examples
"""

import os
import sys
import json
import hashlib
import tarfile
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA256 checksum for a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def collect_core_files(base_path: Path, include_examples: bool = False) -> Dict[str, List[Path]]:
    """
    Collect Jerry's core files based on manifest.

    Returns:
        Dictionary with categories (core, templates, docs) and their file lists
    """
    files = {
        "core": [],
        "templates": [],
        "docs": [],
        "examples": []
    }

    # Core directories to include
    core_dirs = ["adws", ".claude", "specs"]

    # Collect core files
    for dir_name in core_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    # Skip Python cache, test files, and backup files
                    if any(part.startswith(("__pycache__", ".pytest_cache", "test_", ".pyc")) for part in file_path.parts):
                        continue
                    if file_path.suffix in [".pyc", ".pyo"]:
                        continue
                    if "backup" in str(file_path).lower():
                        continue
                    # Skip local settings (contains machine-specific paths and MCP configs)
                    if file_path.name == "settings.local.json":
                        continue

                    files["core"].append(file_path)

    # Collect .jerry manifest and templates
    jerry_dir = base_path / ".jerry"
    if jerry_dir.exists():
        for file_path in jerry_dir.rglob("*"):
            if file_path.is_file():
                if "template" in file_path.parts:
                    files["templates"].append(file_path)
                else:
                    files["core"].append(file_path)

    # Collect docs
    docs_files = ["README.md", "LICENSE", ".gitignore"]
    for doc_file in docs_files:
        doc_path = base_path / doc_file
        if doc_path.exists():
            files["docs"].append(doc_path)

    # Collect docs/ directory if it exists
    docs_dir = base_path / "docs"
    if docs_dir.exists():
        for file_path in docs_dir.rglob("*"):
            if file_path.is_file():
                files["docs"].append(file_path)

    # Collect examples if requested
    if include_examples:
        examples_dir = base_path / "examples"
        if examples_dir.exists():
            for file_path in examples_dir.rglob("*"):
                if file_path.is_file():
                    files["examples"].append(file_path)

    return files


def generate_manifest(base_path: Path, collected_files: Dict[str, List[Path]]) -> Dict[str, Any]:
    """
    Generate export manifest with checksums for all files.
    """
    # Load existing manifest
    manifest_path = base_path / ".jerry" / "manifest.json"
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # Add export metadata
    manifest["export"] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hostname": os.uname().nodename if hasattr(os, "uname") else "unknown",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }

    # Calculate checksums for all files
    checksums = {}
    all_files = []
    for category, file_list in collected_files.items():
        all_files.extend(file_list)

    for file_path in all_files:
        rel_path = str(file_path.relative_to(base_path))
        checksums[rel_path] = calculate_sha256(file_path)

    manifest["integrity"]["checksums"] = checksums

    # Add file counts
    manifest["export"]["file_counts"] = {
        category: len(files) for category, files in collected_files.items()
    }

    return manifest


def create_tarball(output_path: Path, base_path: Path, collected_files: Dict[str, List[Path]], manifest: Dict[str, Any]) -> Path:
    """Create a tarball export package."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_name = f"jerry-export-{manifest['version']}-{timestamp}.tar.gz"
    archive_path = output_path / archive_name

    with tarfile.open(archive_path, "w:gz") as tar:
        # Add all collected files
        for category, file_list in collected_files.items():
            for file_path in file_list:
                arcname = str(file_path.relative_to(base_path))
                tar.add(file_path, arcname=arcname)

        # Add updated manifest
        manifest_path = base_path / ".jerry" / "manifest.json"
        manifest_temp = output_path / "manifest.json.tmp"
        with open(manifest_temp, "w") as f:
            json.dump(manifest, f, indent=2)
        tar.add(manifest_temp, arcname=".jerry/manifest.json")
        manifest_temp.unlink()

    return archive_path


def create_zip(output_path: Path, base_path: Path, collected_files: Dict[str, List[Path]], manifest: Dict[str, Any]) -> Path:
    """Create a zip export package."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_name = f"jerry-export-{manifest['version']}-{timestamp}.zip"
    archive_path = output_path / archive_name

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add all collected files
        for category, file_list in collected_files.items():
            for file_path in file_list:
                arcname = str(file_path.relative_to(base_path))
                zipf.write(file_path, arcname=arcname)

        # Add updated manifest
        manifest_path = base_path / ".jerry" / "manifest.json"
        manifest_temp = output_path / "manifest.json.tmp"
        with open(manifest_temp, "w") as f:
            json.dump(manifest, f, indent=2)
        zipf.write(manifest_temp, arcname=".jerry/manifest.json")
        manifest_temp.unlink()

    return archive_path


def validate_export(archive_path: Path, format_type: str) -> bool:
    """Validate the created export package."""
    try:
        if format_type == "tar.gz":
            with tarfile.open(archive_path, "r:gz") as tar:
                # Check if manifest exists
                manifest_found = any(".jerry/manifest.json" in member.name for member in tar.getmembers())
                # Check if we have some ADW files
                adw_files = sum(1 for member in tar.getmembers() if "adws/" in member.name)
                return manifest_found and adw_files > 0
        elif format_type == "zip":
            with zipfile.ZipFile(archive_path, "r") as zipf:
                # Check if manifest exists
                manifest_found = any(".jerry/manifest.json" in name for name in zipf.namelist())
                # Check if we have some ADW files
                adw_files = sum(1 for name in zipf.namelist() if "adws/" in name)
                return manifest_found and adw_files > 0
        return False
    except Exception as e:
        console.print(f"[red]Validation error: {e}[/red]")
        return False


def generate_export_report(
    archive_path: Path,
    collected_files: Dict[str, List[Path]],
    manifest: Dict[str, Any],
    output_path: Path
) -> Path:
    """Generate a detailed export report."""
    report_path = output_path / f"export-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"

    with open(report_path, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("Jerry Export Report\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Export Date: {manifest['export']['timestamp']}\n")
        f.write(f"Jerry Version: {manifest['version']}\n")
        f.write(f"Python Version: {manifest['export']['python_version']}\n")
        f.write(f"Archive: {archive_path.name}\n")
        f.write(f"Archive Size: {archive_path.stat().st_size / (1024*1024):.2f} MB\n\n")

        f.write("File Counts:\n")
        f.write("-" * 80 + "\n")
        for category, files in collected_files.items():
            f.write(f"  {category.capitalize()}: {len(files)} files\n")

        f.write(f"\nTotal Files: {sum(len(files) for files in collected_files.values())}\n\n")

        f.write("Core Directories:\n")
        f.write("-" * 80 + "\n")
        for dir_name in manifest["core_directories"]:
            f.write(f"  - {dir_name}\n")

        f.write("\nSystem Requirements:\n")
        f.write("-" * 80 + "\n")
        for req, version in manifest["system_requirements"].items():
            f.write(f"  {req}: {version}\n")

        f.write("\nPython Dependencies:\n")
        f.write("-" * 80 + "\n")
        for dep in manifest["python_dependencies"]:
            f.write(f"  - {dep}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("Export completed successfully!\n")
        f.write("=" * 80 + "\n")

    return report_path


@click.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("/tmp/jerry-export"),
    help="Output directory for export package",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["tar.gz", "zip"]),
    default="tar.gz",
    help="Export format (tar.gz or zip)",
)
@click.option(
    "--include-examples",
    is_flag=True,
    help="Include example workflows in export",
)
def main(output: Path, format: str, include_examples: bool):
    """Export Jerry framework to a distributable package."""
    console.print(Panel.fit("🚀 Jerry Export", style="bold blue"))

    # Determine base path (project root)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent

    # Verify we're in a Jerry installation
    manifest_path = base_path / ".jerry" / "manifest.json"
    if not manifest_path.exists():
        console.print("[red]Error: .jerry/manifest.json not found. Are you in a Jerry installation?[/red]")
        sys.exit(1)

    # Create output directory
    output.mkdir(parents=True, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Collect files
        task = progress.add_task("Collecting Jerry core files...", total=None)
        collected_files = collect_core_files(base_path, include_examples)
        progress.update(task, completed=True)

        # Generate manifest
        task = progress.add_task("Generating manifest with checksums...", total=None)
        manifest = generate_manifest(base_path, collected_files)
        progress.update(task, completed=True)

        # Create package
        task = progress.add_task(f"Creating {format} package...", total=None)
        if format == "tar.gz":
            archive_path = create_tarball(output, base_path, collected_files, manifest)
        else:
            archive_path = create_zip(output, base_path, collected_files, manifest)
        progress.update(task, completed=True)

        # Validate
        task = progress.add_task("Validating export package...", total=None)
        is_valid = validate_export(archive_path, format)
        progress.update(task, completed=True)

    if not is_valid:
        console.print("[red]✗ Export validation failed![/red]")
        sys.exit(1)

    # Generate report
    report_path = generate_export_report(archive_path, collected_files, manifest, output)

    # Display success summary
    console.print("\n[green]✓ Export completed successfully![/green]\n")

    table = Table(title="Export Summary", show_header=True, header_style="bold cyan")
    table.add_column("Category", style="dim")
    table.add_column("Value")

    table.add_row("Jerry Version", manifest["version"])
    table.add_row("Archive Format", format)
    table.add_row("Archive Path", str(archive_path))
    table.add_row("Archive Size", f"{archive_path.stat().st_size / (1024*1024):.2f} MB")
    table.add_row("Total Files", str(sum(len(files) for files in collected_files.values())))
    table.add_row("Report", str(report_path))

    console.print(table)

    console.print("\n[yellow]Next steps:[/yellow]")
    console.print(f"  1. Bootstrap Jerry: ./jerry_bootstrap.sh --source {archive_path} --target <target-dir>")
    console.print(f"  2. Review report: cat {report_path}")


if __name__ == "__main__":
    main()
