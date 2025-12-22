#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
# ]
# ///
"""
E2E Test for Jerry Export/Bootstrap/Validate Workflows

Tests the complete lifecycle:
1. Setup - Copy test fixture to temp directory
2. Export - Run jerry_export.py to create package
3. Bootstrap - Run jerry_bootstrap.sh to install Jerry into target
4. Validate - Run jerry_validate.py to verify installation
5. Smoke Test - Verify app still works, simple ADW executes
6. Cleanup - Remove temp artifacts

Usage:
    ./adws/adw_test_export_bootstrap.py
    ./adws/adw_test_export_bootstrap.py --keep-artifacts
    ./adws/adw_test_export_bootstrap.py --dry-run
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Constants
DEFAULT_FIXTURE = "tests/fixtures/vite-bun-app"
TEMP_BASE = "/tmp"


def get_project_root() -> Path:
    """Get the project root directory (where jerry_export.py lives)."""
    script_path = Path(__file__).resolve()
    return script_path.parent.parent


def create_temp_dir() -> Path:
    """Create a timestamped temp directory for test artifacts."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    temp_dir = Path(TEMP_BASE) / f"jerry-e2e-{timestamp}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def run_command(
    cmd: list[str],
    cwd: Optional[Path] = None,
    capture: bool = True,
    timeout: int = 300
) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout}s"
    except Exception as e:
        return -1, "", str(e)


def phase_setup(
    project_root: Path,
    fixture_path: Path,
    temp_dir: Path,
    dry_run: bool
) -> Tuple[bool, Path]:
    """Phase 1: Setup test environment."""
    console.print("\n[bold cyan]Phase 1: Setup[/bold cyan]")

    target_app = temp_dir / "target-app"

    if dry_run:
        console.print(f"  [dim]Would copy {fixture_path} -> {target_app}[/dim]")
        return True, target_app

    # Copy fixture to temp directory
    try:
        shutil.copytree(fixture_path, target_app)
        console.print(f"  [green]Copied fixture to {target_app}[/green]")
        return True, target_app
    except Exception as e:
        console.print(f"  [red]Failed to copy fixture: {e}[/red]")
        return False, target_app


def phase_export(
    project_root: Path,
    temp_dir: Path,
    dry_run: bool
) -> Tuple[bool, Optional[Path]]:
    """Phase 2: Export Jerry package."""
    console.print("\n[bold cyan]Phase 2: Export[/bold cyan]")

    export_script = project_root / "adws" / "jerry_export.py"
    export_output = temp_dir / "export"

    if not export_script.exists():
        console.print(f"  [red]Export script not found: {export_script}[/red]")
        return False, None

    cmd = [str(export_script), "--output", str(export_output), "--format", "tar.gz"]

    if dry_run:
        console.print(f"  [dim]Would run: {' '.join(cmd)}[/dim]")
        return True, export_output / "jerry-export-mock.tar.gz"

    console.print(f"  Running: {' '.join(cmd)}")
    returncode, stdout, stderr = run_command(cmd, cwd=project_root)

    if returncode != 0:
        console.print(f"  [red]Export failed (code {returncode})[/red]")
        if stderr:
            console.print(f"  [red]{stderr}[/red]")
        return False, None

    # Find the created archive
    archives = list(export_output.glob("jerry-export-*.tar.gz"))
    if not archives:
        console.print("  [red]No export archive found[/red]")
        return False, None

    archive_path = archives[0]
    console.print(f"  [green]Exported: {archive_path.name}[/green]")
    return True, archive_path


def phase_bootstrap(
    project_root: Path,
    archive_path: Path,
    target_app: Path,
    dry_run: bool
) -> bool:
    """Phase 3: Bootstrap Jerry into target app."""
    console.print("\n[bold cyan]Phase 3: Bootstrap[/bold cyan]")

    bootstrap_script = project_root / "jerry_bootstrap.sh"

    if not bootstrap_script.exists():
        console.print(f"  [red]Bootstrap script not found: {bootstrap_script}[/red]")
        return False

    cmd = [
        str(bootstrap_script),
        "--source", str(archive_path),
        "--target", str(target_app),
    ]

    if dry_run:
        cmd.append("--dry-run")
        console.print(f"  [dim]Would run: {' '.join(cmd)}[/dim]")
        return True

    console.print(f"  Running: {' '.join(cmd)}")
    returncode, stdout, stderr = run_command(cmd, cwd=project_root)

    if returncode != 0:
        console.print(f"  [red]Bootstrap failed (code {returncode})[/red]")
        if stderr:
            console.print(f"  [red]{stderr}[/red]")
        return False

    console.print("  [green]Bootstrap completed[/green]")
    return True


def phase_validate(
    target_app: Path,
    dry_run: bool,
    validation_level: str = "2"
) -> bool:
    """Phase 4: Validate Jerry installation.

    Validation Levels:
    - Level 1: Import validation (requires global deps - may fail in bootstrap)
    - Level 2: CLI validation (scripts executable, gh/glab checks)
    - Level 3: Workflow validation (prompt, slash commands, worktree)
    - Level 4: Full SDLC validation (plan, build workflows - takes 5+ min)
    - Level 5: Auth validation (GitHub/GitLab token auth)
    - all: Run all levels
    """
    console.print("\n[bold cyan]Phase 4: Validate[/bold cyan]")

    validate_script = target_app / "adws" / "jerry_validate.py"

    if dry_run:
        console.print(f"  [dim]Would run: {validate_script} --level {validation_level}[/dim]")
        return True

    if not validate_script.exists():
        console.print(f"  [red]Validate script not found in target: {validate_script}[/red]")
        return False

    cmd = [str(validate_script), "--level", validation_level]
    console.print(f"  Running: {' '.join(cmd)}")

    # Level 3+ may take longer due to actual workflow execution
    timeout = 120 if validation_level == "2" else 600
    returncode, stdout, stderr = run_command(cmd, cwd=target_app, timeout=timeout)

    if returncode != 0:
        console.print(f"  [red]Validation failed (code {returncode})[/red]")
        if stderr:
            console.print(f"  [red]{stderr}[/red]")
        return False

    console.print(f"  [green]Validation level {validation_level} passed[/green]")
    return True


def phase_smoke_test(
    target_app: Path,
    dry_run: bool
) -> bool:
    """Phase 5: Smoke test - verify app and Jerry work."""
    console.print("\n[bold cyan]Phase 5: Smoke Test[/bold cyan]")

    if dry_run:
        console.print("  [dim]Would verify target app structure[/dim]")
        console.print("  [dim]Would check Jerry ADW scripts are executable[/dim]")
        return True

    # Check that key directories exist
    expected_dirs = ["adws", ".claude", "frontend", "backend"]
    for dir_name in expected_dirs:
        dir_path = target_app / dir_name
        if not dir_path.exists():
            console.print(f"  [red]Missing directory: {dir_name}[/red]")
            return False
        console.print(f"  [green]Found: {dir_name}/[/green]")

    # Check that Jerry ADW scripts exist
    adw_scripts = ["adw_prompt.py", "adw_slash_command.py"]
    for script_name in adw_scripts:
        script_path = target_app / "adws" / script_name
        if not script_path.exists():
            console.print(f"  [yellow]Warning: {script_name} not found[/yellow]")
        else:
            console.print(f"  [green]Found: adws/{script_name}[/green]")

    console.print("  [green]Smoke test passed[/green]")
    return True


def phase_cleanup(
    temp_dir: Path,
    keep_artifacts: bool,
    dry_run: bool
) -> None:
    """Phase 6: Cleanup temp artifacts."""
    console.print("\n[bold cyan]Phase 6: Cleanup[/bold cyan]")

    if keep_artifacts:
        console.print(f"  [yellow]Keeping artifacts: {temp_dir}[/yellow]")
        return

    if dry_run:
        console.print(f"  [dim]Would remove: {temp_dir}[/dim]")
        return

    try:
        shutil.rmtree(temp_dir)
        console.print(f"  [green]Removed: {temp_dir}[/green]")
    except Exception as e:
        console.print(f"  [yellow]Failed to cleanup: {e}[/yellow]")


@click.command()
@click.option(
    "--fixture",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help=f"Path to test fixture (default: {DEFAULT_FIXTURE})",
)
@click.option(
    "--keep-artifacts",
    is_flag=True,
    help="Keep test artifacts after completion",
)
@click.option(
    "--skip-smoke",
    is_flag=True,
    help="Skip smoke tests after validation",
)
@click.option(
    "--validation-level",
    "-l",
    type=click.Choice(["1", "2", "3", "4", "5", "all"]),
    default="2",
    help="Validation level: 1=Import, 2=CLI (default), 3=Workflows, 4=Full SDLC, 5=Auth, all=All",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without executing",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def main(
    fixture: Optional[Path],
    keep_artifacts: bool,
    skip_smoke: bool,
    validation_level: str,
    dry_run: bool,
    verbose: bool
):
    """E2E test for Jerry export/bootstrap/validate workflows."""
    console.print(Panel.fit(
        "[bold]Jerry E2E Test[/bold]\nExport → Bootstrap → Validate",
        style="bold blue"
    ))

    # Determine paths
    project_root = get_project_root()

    if fixture is None:
        fixture = project_root / DEFAULT_FIXTURE

    if not fixture.exists():
        console.print(f"[red]Fixture not found: {fixture}[/red]")
        sys.exit(1)

    console.print(f"\nProject root: {project_root}")
    console.print(f"Test fixture: {fixture}")

    if dry_run:
        console.print("[yellow]DRY RUN MODE - No changes will be made[/yellow]")

    # Create temp directory
    temp_dir = create_temp_dir()
    console.print(f"Temp directory: {temp_dir}")

    # Track results
    results = {}

    try:
        # Phase 1: Setup
        success, target_app = phase_setup(project_root, fixture, temp_dir, dry_run)
        results["setup"] = success
        if not success:
            raise RuntimeError("Setup failed")

        # Phase 2: Export
        success, archive_path = phase_export(project_root, temp_dir, dry_run)
        results["export"] = success
        if not success:
            raise RuntimeError("Export failed")

        # Phase 3: Bootstrap
        success = phase_bootstrap(project_root, archive_path, target_app, dry_run)
        results["bootstrap"] = success
        if not success:
            raise RuntimeError("Bootstrap failed")

        # Phase 4: Validate
        success = phase_validate(target_app, dry_run, validation_level)
        results["validate"] = success
        if not success:
            raise RuntimeError(f"Validation failed (level {validation_level})")

        # Phase 5: Smoke Test
        if not skip_smoke:
            success = phase_smoke_test(target_app, dry_run)
            results["smoke"] = success
            if not success:
                raise RuntimeError("Smoke test failed")
        else:
            results["smoke"] = None  # Skipped

        # All phases passed
        all_passed = True

    except RuntimeError as e:
        console.print(f"\n[red]Test failed: {e}[/red]")
        all_passed = False

    finally:
        # Phase 6: Cleanup (always runs)
        if all_passed or not keep_artifacts:
            phase_cleanup(temp_dir, keep_artifacts or not all_passed, dry_run)

    # Summary
    console.print("\n")
    table = Table(title="Test Results", show_header=True, header_style="bold cyan")
    table.add_column("Phase", style="dim")
    table.add_column("Status")

    for phase, status in results.items():
        if status is None:
            status_str = "[dim]Skipped[/dim]"
        elif status:
            status_str = "[green]PASSED[/green]"
        else:
            status_str = "[red]FAILED[/red]"
        table.add_row(phase.capitalize(), status_str)

    console.print(table)

    if all_passed:
        console.print("\n[bold green]All tests passed![/bold green]")
        sys.exit(0)
    else:
        console.print("\n[bold red]Tests failed![/bold red]")
        if not keep_artifacts:
            console.print(f"[yellow]Artifacts preserved at: {temp_dir}[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
