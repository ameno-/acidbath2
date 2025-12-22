#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pydantic",
#   "python-dotenv",
#   "click",
#   "rich",
#   "pyyaml",
# ]
# ///
"""
Import workflow from sibling directories into Jerry's agentic layer.

This is Jerry's SELF-IMPROVEMENT MECHANISM - the meta-artifact that enables
Jerry to bootstrap itself by importing more workflows.

Usage:
    # Copy a module verbatim
    ./adws/adw_import_workflow.py /path/to/source.py

    # Adapt a module (generalize, remove app-specific code)
    ./adws/adw_import_workflow.py /path/to/source.py --mode adapt

    # Import with 3-level validation (import → CLI → dry-run)
    ./adws/adw_import_workflow.py /path/to/source.py --validation-level all

    # Generate manifest template for an ADW
    ./adws/adw_import_workflow.py /path/to/source.py --generate-manifest

    # Import with auto-documentation updates
    ./adws/adw_import_workflow.py /path/to/source.py --update-docs

    # Import with phase reporting
    ./adws/adw_import_workflow.py /path/to/source.py --phase meta_orchestration

Features:
    - 3-level validation: import test → CLI test → dry-run test
    - YAML manifests define test criteria per ADW
    - Auto-update README and VALIDATION_STATUS.md
    - Retry logic: 3 attempts with exponential backoff
    - State tracking via ADWState for resume capability
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule

# Add the adws directory to the path for proper package imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.agent import (
    AgentTemplateRequest,
    AgentPromptResponse,
    execute_template,
    generate_short_id,
)
from adws.adw_modules.data_types import RetryCode
from adws.adw_modules.state import ADWState
from adws.adw_modules.utils import make_adw_id, setup_logger, get_project_root
from adws.adw_modules.validation import (
    ManifestSchema,
    ValidationReport,
    load_manifest,
    find_manifest_for_adw,
    run_validation,
    generate_manifest_template,
    get_manifests_dir,
)

# Output file name constants
OUTPUT_JSONL = "cc_raw_output.jsonl"
OUTPUT_JSON = "cc_raw_output.json"
FINAL_OBJECT_JSON = "cc_final_object.json"
SUMMARY_JSON = "custom_summary_output.json"

# Retry configuration
RETRY_DELAYS = [1, 3, 5]  # seconds
MAX_RETRIES = 3


def derive_target_path(source_path: str) -> str:
    """Derive target path from source path.

    Maps sibling directory paths to Jerry's equivalent paths.

    Examples:
        /path/to/tac8_app5/adws/module.py -> /jerry/adws/module.py
        /path/to/app2/.claude/commands/cmd.md -> /jerry/.claude/commands/cmd.md
    """
    project_root = get_project_root()
    source = Path(source_path)

    # Find the relative path after the app directory
    parts = source.parts

    # Look for common directory markers
    markers = ["adws", ".claude", "specs", "scripts"]

    for i, part in enumerate(parts):
        if part in markers:
            # Found marker, reconstruct path from here
            relative = Path(*parts[i:])
            return str(Path(project_root) / relative)

    # Fallback: use filename only in project root
    return str(Path(project_root) / source.name)


def validate_python_import(target_path: str, console: Console) -> bool:
    """Validate that a Python module can be imported.

    Returns True if validation passes, False otherwise.
    """
    if not target_path.endswith(".py"):
        return True  # Skip validation for non-Python files

    project_root = get_project_root()
    target = Path(target_path)

    # Determine module path
    try:
        relative = target.relative_to(project_root)
    except ValueError:
        console.print("[yellow]Cannot determine relative path, skipping validation[/yellow]")
        return True

    # Convert path to module notation
    # e.g., adws/adw_modules/workflow_ops.py -> adws.adw_modules.workflow_ops
    if str(relative).startswith("adws/adw_modules/"):
        module_name = str(relative).replace("/", ".").replace(".py", "")
        # For adw_modules, we need to use relative import syntax
        module_file = relative.name.replace(".py", "")
        import_cmd = f"from adws.adw_modules.{module_file} import *"
    else:
        # Generic import attempt
        import_cmd = f"exec(open('{target_path}').read())"

    # Run validation
    cmd = [
        "python3", "-c",
        f"import sys; sys.path.insert(0, '{project_root}'); {import_cmd}; print('OK')"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=project_root,
        )

        if result.returncode == 0:
            console.print("[green]Validation passed[/green]")
            return True
        else:
            console.print(f"[red]Validation failed: {result.stderr[:200]}[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Validation error: {e}[/red]")
        return False


def execute_import_with_retry(
    request: AgentTemplateRequest,
    console: Console,
) -> AgentPromptResponse:
    """Execute the import workflow with retry logic.

    Implements exponential backoff: 1s, 3s, 5s delays between retries.
    """
    last_response = None

    for attempt in range(MAX_RETRIES + 1):
        if attempt > 0:
            delay = RETRY_DELAYS[attempt - 1]
            console.print(f"[yellow]Retry {attempt}/{MAX_RETRIES} after {delay}s delay...[/yellow]")
            time.sleep(delay)

        with console.status(f"[bold yellow]Executing import (attempt {attempt + 1})...[/bold yellow]"):
            response = execute_template(request)

        last_response = response

        if response.success:
            return response

        # Check if error is retryable
        if response.retry_code in [
            RetryCode.CLAUDE_CODE_ERROR,
            RetryCode.TIMEOUT_ERROR,
            RetryCode.EXECUTION_ERROR,
            RetryCode.ERROR_DURING_EXECUTION,
        ]:
            if attempt < MAX_RETRIES:
                console.print(f"[yellow]Retryable error: {response.retry_code}[/yellow]")
                continue

        # Non-retryable error or max retries reached
        break

    return last_response


def run_enhanced_validation(
    target_path: str,
    validation_level: str,
    console: Console,
) -> ValidationReport:
    """Run enhanced 3-level validation on imported ADW.

    Args:
        target_path: Path to the imported ADW
        validation_level: "1", "2", "3", or "all"
        console: Rich console for output

    Returns:
        ValidationReport with results
    """
    # Determine max level
    max_level = 3 if validation_level == "all" else int(validation_level)

    console.print(f"[cyan]Running validation (max level: {max_level})...[/cyan]")

    # Try to find manifest for the target
    manifest = None
    manifest_path = find_manifest_for_adw(target_path)
    if manifest_path:
        try:
            manifest = load_manifest(manifest_path)
            console.print(f"[dim]Using manifest: {manifest_path}[/dim]")
        except Exception as e:
            console.print(f"[yellow]Could not load manifest: {e}[/yellow]")

    # Run validation
    report = run_validation(target_path, manifest, max_level=max_level)

    # Display results
    for result in report.results:
        status = "[green]PASS[/green]" if result.passed else ("[yellow]SKIP[/yellow]" if result.skipped else "[red]FAIL[/red]")
        console.print(f"  Level {result.level} ({result.name}): {status} ({result.duration_ms}ms)")
        if not result.passed and not result.skipped and result.message:
            console.print(f"    [dim]{result.message[:100]}[/dim]")

    overall = "[green]PASSED[/green]" if report.overall_passed else "[red]FAILED[/red]"
    console.print(f"  Overall: {overall}")

    return report


def update_validation_status(
    adw_name: str,
    report: ValidationReport,
    console: Console,
) -> None:
    """Update the VALIDATION_STATUS.md file with results.

    Args:
        adw_name: Name of the ADW
        report: Validation report
        console: Rich console for output
    """
    project_root = get_project_root()
    status_path = Path(project_root) / "adws" / "VALIDATION_STATUS.md"

    # Read existing content or create new
    if status_path.exists():
        with open(status_path, "r") as f:
            content = f.read()
    else:
        content = """# ADW Validation Status

Last updated: TIMESTAMP

| ADW | Import | CLI | Dry-Run | Status |
|-----|--------|-----|---------|--------|
"""

    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = content.replace("Last updated: TIMESTAMP", f"Last updated: {timestamp}")
    if "Last updated:" in content and timestamp not in content:
        # Update existing timestamp
        import re
        content = re.sub(r"Last updated: [\d\-: ]+", f"Last updated: {timestamp}", content)

    # Build status row
    import_status = "N/A"
    cli_status = "N/A"
    dry_run_status = "N/A"

    for result in report.results:
        status = "PASS" if result.passed else ("SKIP" if result.skipped else "FAIL")
        if result.name == "import":
            import_status = status
        elif result.name == "cli":
            cli_status = status
        elif result.name == "dry_run":
            dry_run_status = status

    overall_status = "Ready" if report.overall_passed else "Needs Fix"
    new_row = f"| {adw_name} | {import_status} | {cli_status} | {dry_run_status} | {overall_status} |"

    # Check if ADW already exists in table
    if f"| {adw_name} |" in content:
        # Update existing row
        import re
        pattern = rf"\| {re.escape(adw_name)} \|[^\n]+\|"
        content = re.sub(pattern, new_row, content)
    else:
        # Add new row before the last line (or at the end)
        if content.rstrip().endswith("|"):
            content = content.rstrip() + "\n" + new_row + "\n"
        else:
            content = content + new_row + "\n"

    with open(status_path, "w") as f:
        f.write(content)

    console.print(f"[cyan]Updated: {status_path}[/cyan]")


def update_readme_with_adw(
    adw_name: str,
    manifest: Optional[ManifestSchema],
    validation_status: str,
    console: Console,
) -> None:
    """Update adws/README.md with imported ADW info.

    Args:
        adw_name: Name of the ADW
        manifest: Optional manifest with metadata
        validation_status: "Ready", "Needs Fix", etc.
        console: Rich console for output
    """
    project_root = get_project_root()
    readme_path = Path(project_root) / "adws" / "README.md"

    if not readme_path.exists():
        console.print("[yellow]adws/README.md not found, skipping update[/yellow]")
        return

    with open(readme_path, "r") as f:
        content = f.read()

    # Look for auto-update markers
    start_marker = "<!-- ADW-LIST-START -->"
    end_marker = "<!-- ADW-LIST-END -->"

    if start_marker not in content:
        console.print("[yellow]No ADW-LIST markers found in README, skipping update[/yellow]")
        return

    # Build ADW entry
    category = manifest.category if manifest else "utility"
    description = manifest.description if manifest else f"AI Developer Workflow: {adw_name}"

    new_entry = f"| {adw_name} | {category} | {description} | {validation_status} |"

    # Extract existing table
    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)

    if end_idx <= start_idx:
        console.print("[yellow]Invalid marker positions in README[/yellow]")
        return

    table_content = content[start_idx:end_idx]

    # Check if ADW already in table
    if f"| {adw_name} |" in table_content:
        # Update existing entry
        import re
        pattern = rf"\| {re.escape(adw_name)} \|[^\n]+\|"
        table_content = re.sub(pattern, new_entry, table_content)
    else:
        # Add new entry
        # Ensure table header exists
        if "| ADW |" not in table_content:
            table_content = "\n| ADW | Category | Description | Validation |\n|-----|----------|-------------|------------|\n"
        table_content = table_content.rstrip() + "\n" + new_entry + "\n"

    # Rebuild content
    new_content = content[:start_idx] + table_content + content[end_idx:]

    with open(readme_path, "w") as f:
        f.write(new_content)

    console.print(f"[cyan]Updated: {readme_path}[/cyan]")


def save_phase_report(
    adw_id: str,
    phase_name: str,
    imports: List[Dict[str, Any]],
    console: Console,
) -> str:
    """Generate and save a phase report.

    Returns the path to the report file.
    """
    project_root = get_project_root()
    report_dir = Path(project_root) / "ai_docs" / "genesis"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"phase1_{phase_name}_report.md"

    # Count successes and failures
    successes = sum(1 for i in imports if i.get("status") == "success")
    failures = sum(1 for i in imports if i.get("status") == "failed")

    # Generate report content
    content = f"""# Phase 1: {phase_name.replace('_', ' ').title()} Report

**Date**: {datetime.now().strftime('%Y-%m-%d')}
**ADW ID**: {adw_id}
**Status**: {'COMPLETED' if failures == 0 else 'PARTIAL'}

## Summary

- **Total Imports**: {len(imports)}
- **Successful**: {successes}
- **Failed**: {failures}

## Import Details

| Source | Target | Mode | Status | Validation |
|--------|--------|------|--------|------------|
"""

    for imp in imports:
        source = Path(imp.get("source", "")).name
        target = Path(imp.get("target", "")).name
        mode = imp.get("mode", "copy")
        status = imp.get("status", "unknown")
        validation = imp.get("validation", "skipped")
        status_icon = "OK" if status == "success" else "FAIL"
        validation_icon = "OK" if validation == "passed" else "SKIP" if validation == "skipped" else "FAIL"

        content += f"| {source} | {target} | {mode} | {status_icon} | {validation_icon} |\n"

    content += """
## Validation Commands

```bash
cd /Users/ameno/dev/tac/tac-8/jerry
uv run python3 -c "from adws.adw_modules import *; print('All modules imported successfully!')"
```

## Next Steps

- Use `adw_import_workflow.py` to import additional modules
- Run validation to ensure all imports work correctly
- Proceed to Phase 2 after validation passes

---

**Phase 1 Complete** - Import workflow is operational.
"""

    with open(report_path, "w") as f:
        f.write(content)

    console.print(f"[cyan]Phase report saved to: {report_path}[/cyan]")
    return str(report_path)


@click.command()
@click.argument("source_path", required=True)
@click.option(
    "--mode",
    type=click.Choice(["copy", "adapt", "merge"]),
    default="copy",
    help="Adaptation mode: copy (verbatim), adapt (generalize), merge (combine with existing)",
)
@click.option(
    "--target",
    "target_path",
    type=str,
    default=None,
    help="Target path in Jerry (defaults to equivalent path)",
)
@click.option(
    "--phase",
    "phase_name",
    type=str,
    default=None,
    help="Phase name for report generation",
)
@click.option(
    "--adw-id",
    type=str,
    default=None,
    help="ADW ID to use (generates new one if not provided)",
)
@click.option(
    "--model",
    type=click.Choice(["sonnet", "opus"]),
    default="sonnet",
    help="Claude model to use",
)
@click.option(
    "--skip-validation",
    is_flag=True,
    help="Skip all validation (legacy option)",
)
@click.option(
    "--validation-level",
    type=click.Choice(["1", "2", "3", "all"]),
    default="all",
    help="Validation level: 1=import, 2=cli, 3=dry-run, all=all levels",
)
@click.option(
    "--generate-manifest",
    is_flag=True,
    help="Generate manifest template for the source ADW",
)
@click.option(
    "--update-docs/--no-update-docs",
    default=True,
    help="Auto-update README and VALIDATION_STATUS.md (default: True)",
)
def main(
    source_path: str,
    mode: str,
    target_path: Optional[str],
    phase_name: Optional[str],
    adw_id: Optional[str],
    model: str,
    skip_validation: bool,
    validation_level: str,
    generate_manifest: bool,
    update_docs: bool,
):
    """Import a workflow from a sibling directory into Jerry."""
    console = Console()

    # Generate or use provided ADW ID
    if not adw_id:
        adw_id = make_adw_id()

    # Derive target path if not provided
    if not target_path:
        target_path = derive_target_path(source_path)

    project_root = get_project_root()

    # Set up logger
    logger = setup_logger(adw_id, "import_workflow")

    # Handle --generate-manifest option
    if generate_manifest:
        console.print(Rule("[bold yellow]Generating Manifest Template[/bold yellow]"))
        manifest_content = generate_manifest_template(source_path)
        adw_name = Path(source_path).stem
        manifest_path = get_manifests_dir() / f"{adw_name}.test.yaml"
        get_manifests_dir().mkdir(parents=True, exist_ok=True)

        with open(manifest_path, "w") as f:
            f.write(manifest_content)

        console.print(f"[green]Generated manifest: {manifest_path}[/green]")
        console.print()
        console.print(manifest_content)
        sys.exit(0)

    # Display workflow configuration
    console.print(
        Panel(
            f"[bold blue]ADW Import Workflow[/bold blue]\n\n"
            f"[cyan]ADW ID:[/cyan] {adw_id}\n"
            f"[cyan]Source:[/cyan] {source_path}\n"
            f"[cyan]Target:[/cyan] {target_path}\n"
            f"[cyan]Mode:[/cyan] {mode}\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]Validation:[/cyan] {'skip' if skip_validation else f'level {validation_level}'}\n"
            f"[cyan]Update Docs:[/cyan] {update_docs}",
            title="[bold blue]Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # Validate source file exists
    if not os.path.exists(source_path):
        console.print(
            Panel(
                f"[bold red]Source file not found: {source_path}[/bold red]",
                title="[bold red]Error[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    # Load or create state
    state = ADWState.load(adw_id, logger) or ADWState(adw_id)

    # Track imports in state metadata
    imports = state.get("imports", [])
    if not isinstance(imports, list):
        imports = []

    # Create import request
    console.print(Rule("[bold yellow]Executing Import[/bold yellow]"))
    console.print()

    # Build args for the slash command
    args = [source_path, mode]
    if target_path:
        args.append(target_path)

    request = AgentTemplateRequest(
        agent_name="importer",
        slash_command="/import_workflow",
        args=args,
        adw_id=adw_id,
        model=model,
        working_dir=project_root,
    )

    # Execute with retry
    response = execute_import_with_retry(request, console)

    # Process result
    import_record = {
        "source": source_path,
        "target": target_path,
        "mode": mode,
        "status": "success" if response.success else "failed",
        "validation": "skipped",
        "attempts": 1,
        "timestamp": datetime.now().isoformat(),
    }

    # Variables for validation results
    validation_report = None
    manifest = None

    if response.success:
        console.print(
            Panel(
                response.output,
                title="[bold green]Import Success[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

        # Run enhanced validation
        if not skip_validation:
            console.print()
            console.print(Rule("[bold yellow]Running Validation[/bold yellow]"))
            validation_report = run_enhanced_validation(target_path, validation_level, console)
            import_record["validation"] = "passed" if validation_report.overall_passed else "failed"
            import_record["validation_details"] = {
                "highest_level": validation_report.highest_level_passed,
                "results": [
                    {"level": r.level, "name": r.name, "passed": r.passed}
                    for r in validation_report.results
                ],
            }

            # Try to load manifest for doc updates
            manifest_path = find_manifest_for_adw(target_path)
            if manifest_path:
                try:
                    manifest = load_manifest(manifest_path)
                except Exception:
                    pass

        # Update documentation
        if update_docs and validation_report:
            console.print()
            console.print(Rule("[bold yellow]Updating Documentation[/bold yellow]"))
            adw_name = Path(target_path).stem
            validation_status = "Ready" if validation_report.overall_passed else "Needs Fix"

            # Update VALIDATION_STATUS.md
            update_validation_status(adw_name, validation_report, console)

            # Update README with ADW info
            update_readme_with_adw(adw_name, manifest, validation_status, console)

    else:
        console.print(
            Panel(
                response.output,
                title="[bold red]Import Failed[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
        )
        import_record["error"] = response.output[:500]

    # Update state
    imports.append(import_record)
    state.update(metadata={"imports": imports})
    if phase_name:
        state.update(metadata={"phase_name": phase_name})
    state.save("import_workflow")

    # Save summary
    output_dir = Path(project_root) / "agents" / adw_id / "importer"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / SUMMARY_JSON
    with open(summary_path, "w") as f:
        json.dump(
            {
                "workflow": "import_workflow",
                "adw_id": adw_id,
                "source": source_path,
                "target": target_path,
                "mode": mode,
                "model": model,
                "success": response.success,
                "validation": import_record.get("validation", "skipped"),
                "session_id": response.session_id,
                "retry_code": str(response.retry_code),
            },
            f,
            indent=2,
        )

    # Generate phase report if requested
    if phase_name:
        console.print()
        save_phase_report(adw_id, phase_name, imports, console)

    # Show output files
    console.print()
    files_table = Table(show_header=True, box=None)
    files_table.add_column("File Type", style="bold cyan")
    files_table.add_column("Path", style="dim")

    files_table.add_row("State", str(state.get_state_path()))
    files_table.add_row("Summary", str(summary_path))
    files_table.add_row("Log", str(output_dir / "execution.log"))

    console.print(
        Panel(
            files_table,
            title="[bold blue]Output Files[/bold blue]",
            border_style="blue",
        )
    )

    # Exit with appropriate code
    validation_passed = import_record.get("validation") != "failed"
    if response.success and validation_passed:
        console.print("\n[bold green]Import completed successfully![/bold green]")
        if validation_report:
            console.print(f"[dim]Validation: level {validation_report.highest_level_passed} passed[/dim]")
        sys.exit(0)
    else:
        if not response.success:
            console.print("\n[bold red]Import failed[/bold red]")
        else:
            console.print("\n[bold yellow]Import succeeded but validation failed[/bold yellow]")
            if validation_report:
                console.print(f"[dim]Check validation report for details[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()
