#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
#   "pyyaml>=6.0.0",
# ]
# ///
"""
Jerry Simple Update System - Version-based framework updates.

This script provides a minimal, maintainable update system for Jerry installations.
It uses version tracking from .jerry/manifest.json and rsync for safe file updates.

Usage:
    # Update from default source (GitHub or manifest update_url)
    ./adws/jerry_update.py

    # Update from specific GitHub repository
    ./adws/jerry_update.py --source https://github.com/ameno-/tac

    # Update from local tarball
    ./adws/jerry_update.py --source /path/to/jerry-update.tar.gz

    # Update from local directory
    ./adws/jerry_update.py --source /path/to/jerry-source

    # Dry-run to see what would change
    ./adws/jerry_update.py --dry-run

    # Force downgrade to older version
    ./adws/jerry_update.py --source /path/to/older-version --force

Examples:
    # Check for updates without applying
    ./adws/jerry_update.py --dry-run

    # Update and see what changed
    ./adws/jerry_update.py

    # Update from development directory
    ./adws/jerry_update.py --source ~/dev/jerry-main
"""

import json
import sys
import subprocess
import tempfile
import tarfile
import shutil
from pathlib import Path
from typing import Optional, Tuple, List

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def get_local_version(jerry_root: Path) -> str:
    """
    Get the local Jerry version from manifest.json.

    Args:
        jerry_root: Path to Jerry installation root

    Returns:
        Version string (e.g., "0.1.0") or "0.0.0" if not found

    Notes:
        - Returns "0.0.0" for unversioned installations (migration baseline)
        - Returns "0.0.0" if manifest doesn't exist
        - Returns "0.0.0" if manifest exists but has no version field
        - Handles JSON parsing errors gracefully
    """
    manifest_path = jerry_root / ".jerry" / "manifest.json"

    # No manifest file
    if not manifest_path.exists():
        return "0.0.0"

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Get version field, default to "0.0.0" if missing
        return manifest.get("version", "0.0.0")

    except (json.JSONDecodeError, OSError) as e:
        console.print(f"[yellow]Warning: Could not read manifest: {e}[/yellow]")
        console.print("[yellow]Treating as unversioned installation (0.0.0)[/yellow]")
        return "0.0.0"


def compare_versions(local: str, remote: str) -> int:
    """
    Compare two semantic version strings.

    Args:
        local: Local version string (e.g., "0.1.0")
        remote: Remote version string (e.g., "0.2.0")

    Returns:
        -1 if local < remote (update available)
         0 if local == remote (up to date)
         1 if local > remote (downgrade would occur)

    Raises:
        ValueError: If either version string is not valid semver format

    Examples:
        >>> compare_versions("0.1.0", "0.2.0")
        -1
        >>> compare_versions("1.0.0", "1.0.0")
        0
        >>> compare_versions("2.0.0", "1.9.9")
        1
        >>> compare_versions("0.0.0", "0.1.0")
        -1
    """
    def parse_version(version: str) -> Tuple[int, int, int]:
        """Parse semver string into (major, minor, patch) tuple."""
        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid semver format: '{version}'. Expected 'X.Y.Z'")

        try:
            major = int(parts[0])
            minor = int(parts[1])
            patch = int(parts[2])
            return (major, minor, patch)
        except ValueError:
            raise ValueError(f"Invalid semver format: '{version}'. Parts must be integers")

    try:
        local_parts = parse_version(local)
        remote_parts = parse_version(remote)
    except ValueError as e:
        raise ValueError(f"Version comparison failed: {e}")

    # Compare tuples (Python does lexicographic comparison)
    if local_parts < remote_parts:
        return -1
    elif local_parts == remote_parts:
        return 0
    else:
        return 1


def resolve_update_source(source: Optional[str], jerry_root: Path) -> Tuple[str, Path]:
    """
    Resolve the update source to a local directory path and extract version.

    Args:
        source: Update source - can be:
                - None (use manifest update_url or default GitHub)
                - URL (GitHub repository - future implementation)
                - Path to tarball (.tar.gz)
                - Path to directory
        jerry_root: Path to current Jerry installation root

    Returns:
        Tuple of (version, source_path)
        - version: Version string from source manifest
        - source_path: Path to directory containing update files

    Raises:
        ValueError: If source is invalid or cannot be resolved
        FileNotFoundError: If source path doesn't exist
        RuntimeError: If extraction or download fails

    Notes:
        - GitHub URL support is planned for future implementation
        - Temporary directories are created for tarball extraction
        - Caller is responsible for cleanup of temporary directories
    """
    # Determine the source to use
    if source is None:
        # Try to get update_url from manifest
        manifest_path = jerry_root / ".jerry" / "manifest.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                source = manifest.get("update_url")
            except (json.JSONDecodeError, OSError):
                pass

        if source is None:
            raise ValueError(
                "No update source specified and no update_url in manifest. "
                "Please provide --source argument."
            )

    source_str = str(source)

    # Case 1: URL (GitHub) - Future implementation
    if source_str.startswith("http://") or source_str.startswith("https://"):
        raise ValueError(
            "GitHub URL updates not yet implemented. "
            "Please use local tarball or directory path."
        )

    # Case 2: Tarball path
    source_path = Path(source_str).expanduser().resolve()
    if source_path.is_file() and source_path.suffix == ".gz" and ".tar" in source_path.name:
        console.print(f"[cyan]Extracting tarball: {source_path}[/cyan]")

        # Create temporary directory for extraction
        temp_dir = Path(tempfile.mkdtemp(prefix="jerry_update_"))

        try:
            with tarfile.open(source_path, 'r:gz') as tar:
                # Security: Check for path traversal
                for member in tar.getmembers():
                    if member.name.startswith('/') or '..' in member.name:
                        raise ValueError(
                            f"Tarball contains unsafe path: {member.name}"
                        )
                tar.extractall(temp_dir)

            # Find the extracted Jerry root (should have .jerry/manifest.json)
            extracted_roots = list(temp_dir.glob("*/.jerry/manifest.json"))
            if not extracted_roots:
                # Maybe it's at the temp_dir root itself
                if (temp_dir / ".jerry" / "manifest.json").exists():
                    extracted_root = temp_dir
                else:
                    raise ValueError(
                        "Tarball does not contain a valid Jerry installation "
                        "(.jerry/manifest.json not found)"
                    )
            else:
                extracted_root = extracted_roots[0].parent.parent

            # Read version from extracted manifest
            version = get_local_version(extracted_root)
            console.print(f"[green]Extracted version: {version}[/green]")

            return (version, extracted_root)

        except (tarfile.TarError, OSError) as e:
            # Cleanup on failure
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to extract tarball: {e}")

    # Case 3: Directory path
    elif source_path.is_dir():
        console.print(f"[cyan]Using directory source: {source_path}[/cyan]")

        # Validate it's a Jerry installation
        if not (source_path / ".jerry" / "manifest.json").exists():
            raise ValueError(
                f"Source directory is not a valid Jerry installation: {source_path}\n"
                "Missing .jerry/manifest.json"
            )

        # Read version from source manifest
        version = get_local_version(source_path)
        console.print(f"[green]Source version: {version}[/green]")

        return (version, source_path)

    else:
        raise FileNotFoundError(
            f"Update source not found or invalid: {source_path}\n"
            "Source must be a directory or .tar.gz file"
        )


def sync_core_files(source: Path, target: Path, dry_run: bool = False) -> List[str]:
    """
    Synchronize core Jerry files from source to target using rsync.

    Args:
        source: Source directory containing Jerry update files
        target: Target directory (current Jerry installation)
        dry_run: If True, show what would change without applying

    Returns:
        List of file paths that were changed (or would be changed in dry-run)

    Raises:
        RuntimeError: If rsync command fails
        FileNotFoundError: If rsync is not available

    Notes:
        - Updates core directories: adws/, .claude/, .jerry/
        - Preserves user directories: agents/, trees/, specs/
        - Preserves environment files: .env, .ports.env
        - Uses rsync -av for archive mode with verbose output
    """
    # Check if rsync is available
    try:
        subprocess.run(
            ["rsync", "--version"],
            capture_output=True,
            check=True
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "rsync command not found. Please install rsync:\n"
            "  macOS: rsync is pre-installed\n"
            "  Linux: sudo apt-get install rsync"
        )

    # Build rsync command
    rsync_cmd = ["rsync", "-av"]

    if dry_run:
        rsync_cmd.append("--dry-run")

    # Include only core directories
    rsync_cmd.extend([
        "--include=adws/***",
        "--include=.claude/***",
        "--include=.jerry/***",
    ])

    # Exclude user directories and files
    rsync_cmd.extend([
        "--exclude=agents/",
        "--exclude=trees/",
        "--exclude=specs/",
        "--exclude=.env",
        "--exclude=.ports.env",
        "--exclude=*",  # Exclude everything else not explicitly included
    ])

    # Source and target paths (trailing slash important for rsync)
    rsync_cmd.append(f"{source}/")
    rsync_cmd.append(f"{target}/")

    # Run rsync
    try:
        result = subprocess.run(
            rsync_cmd,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"rsync failed with exit code {e.returncode}:\n"
            f"stdout: {e.stdout}\n"
            f"stderr: {e.stderr}"
        )

    # Parse rsync output to extract changed files
    changed_files = []
    for line in result.stdout.splitlines():
        # Skip rsync status lines
        if line.startswith("sending incremental file list"):
            continue
        if line.startswith("sent ") or line.startswith("total size"):
            continue
        if not line.strip():
            continue
        if line.endswith("/"):
            # Directory entry, skip
            continue

        # This is a file that was changed
        changed_files.append(line.strip())

    return changed_files


def update_manifest_version(jerry_root: Path, version: str) -> None:
    """
    Update the version field in the Jerry manifest.

    Args:
        jerry_root: Path to Jerry installation root
        version: New version string to set

    Raises:
        FileNotFoundError: If manifest doesn't exist
        RuntimeError: If manifest update fails

    Notes:
        - Preserves all other manifest fields
        - Maintains JSON formatting (indent=2)
        - Validates JSON structure before writing
    """
    manifest_path = jerry_root / ".jerry" / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifest not found: {manifest_path}\n"
            "Cannot update version in missing manifest"
        )

    try:
        # Read existing manifest
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Update version field
        manifest["version"] = version

        # Write back with proper formatting
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
            f.write('\n')  # Add trailing newline

        console.print(f"[green]Updated manifest version to: {version}[/green]")

    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError(f"Failed to update manifest: {e}")


@click.command()
@click.option(
    '--source',
    type=str,
    default=None,
    help='Update source: GitHub URL, tarball path, or directory path. '
         'If not specified, uses update_url from manifest.'
)
@click.option(
    '--dry-run',
    is_flag=True,
    default=False,
    help='Show what would change without applying updates'
)
@click.option(
    '--force',
    is_flag=True,
    default=False,
    help='Allow downgrade to older version'
)
def update(source: Optional[str], dry_run: bool, force: bool) -> None:
    """
    Update Jerry framework to a new version.

    This command safely updates core Jerry files while preserving user
    customizations (agents, trees, specs, .env files).

    Examples:

        \b
        # Update from default source
        ./adws/jerry_update.py

        \b
        # Dry-run to preview changes
        ./adws/jerry_update.py --dry-run

        \b
        # Update from local directory
        ./adws/jerry_update.py --source /path/to/jerry-dev

        \b
        # Update from tarball
        ./adws/jerry_update.py --source jerry-0.2.0.tar.gz

        \b
        # Force downgrade
        ./adws/jerry_update.py --source older-version/ --force
    """
    jerry_root = Path.cwd()

    # Display header
    console.print(Panel(
        "[bold cyan]Jerry Update System[/bold cyan]\n"
        "Safe, version-based framework updates",
        expand=False
    ))

    try:
        # Step 1: Get local version
        local_version = get_local_version(jerry_root)
        console.print(f"\n[cyan]Current version:[/cyan] {local_version}")

        # Step 2: Resolve update source and get remote version
        console.print(f"\n[cyan]Resolving update source...[/cyan]")
        remote_version, source_path = resolve_update_source(source, jerry_root)
        console.print(f"[cyan]Update version:[/cyan] {remote_version}")

        # Step 3: Compare versions
        version_cmp = compare_versions(local_version, remote_version)

        if version_cmp == 0:
            console.print(f"\n[green]✓ Already up to date (version {local_version})[/green]")
            return

        if version_cmp > 0:
            # Local is newer than remote
            if not force:
                console.print(
                    f"\n[yellow]⚠ Downgrade detected:[/yellow]\n"
                    f"  Current: {local_version}\n"
                    f"  Update:  {remote_version}\n\n"
                    f"[yellow]Use --force to allow downgrade[/yellow]"
                )
                sys.exit(1)
            else:
                console.print(
                    f"\n[yellow]⚠ Downgrading (--force enabled):[/yellow]\n"
                    f"  {local_version} → {remote_version}"
                )
        else:
            # Update available
            console.print(
                f"\n[green]✓ Update available:[/green]\n"
                f"  {local_version} → {remote_version}"
            )

        # Step 4: Sync files
        mode_str = "[yellow](DRY RUN)[/yellow]" if dry_run else ""
        console.print(f"\n[cyan]Syncing core files... {mode_str}[/cyan]")

        changed_files = sync_core_files(source_path, jerry_root, dry_run)

        if not changed_files:
            console.print("[green]✓ No file changes needed[/green]")
        else:
            console.print(f"\n[cyan]Changed files ({len(changed_files)}):[/cyan]")
            for file_path in changed_files[:20]:  # Show first 20
                console.print(f"  • {file_path}")
            if len(changed_files) > 20:
                console.print(f"  ... and {len(changed_files) - 20} more")

        # Step 5: Update manifest version (skip in dry-run)
        if not dry_run:
            console.print(f"\n[cyan]Updating manifest...[/cyan]")
            update_manifest_version(jerry_root, remote_version)

        # Step 6: Success summary
        console.print("\n" + "=" * 50)
        if dry_run:
            console.print("[yellow]DRY RUN COMPLETE[/yellow]")
            console.print(f"Would update: {local_version} → {remote_version}")
            console.print(f"Files affected: {len(changed_files)}")
        else:
            console.print("[green]✓ UPDATE COMPLETE[/green]")
            console.print(f"Updated: {local_version} → {remote_version}")
            console.print(f"Files changed: {len(changed_files)}")

            # Point to CHANGELOG
            changelog_path = jerry_root / "CHANGELOG.md"
            if changelog_path.exists():
                console.print(
                    f"\n[cyan]→ See CHANGELOG.md for breaking changes and new features[/cyan]"
                )

        console.print("=" * 50 + "\n")

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        console.print(f"\n[red]✗ Update failed:[/red] {e}\n")
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Update cancelled by user[/yellow]\n")
        sys.exit(130)

    finally:
        # Cleanup temporary directories if needed
        # (source_path from tarball extraction would need cleanup)
        # This is simplified - proper cleanup would track temp dirs
        pass


if __name__ == "__main__":
    update()
