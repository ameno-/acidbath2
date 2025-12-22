#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml"]
# ///

"""
ADW Fix Validation - Self-healing workflow for broken ADWs

Usage:
  uv run adw_fix_validation.py [--dry-run] [--adw-name NAME]

Options:
  --dry-run       Validate without making changes
  --adw-name NAME Fix only the specified ADW

Workflow:
1. Parse VALIDATION_STATUS.md to identify broken ADWs
2. Create local issues for each broken ADW (if not exists)
3. Process issues by complexity (simplest first)
4. For each issue:
   a. Read the ADW's manifest for expected behavior
   b. Run the failing validation to capture error
   c. Use /patch command to fix the issue
   d. Re-run validation to verify fix
   e. Update local issue status
5. Report summary of fixes

Complexity ordering (from validation status):
1. Simplest: Single failure (e.g., just CLI or just dry-run)
2. Medium: Two failures
3. Complex: All three levels failing
"""

import sys
import os
import re
import json
import subprocess
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from adws.adw_modules.state import ADWState
from adws.adw_modules.utils import setup_logger, make_adw_id
from adws.adw_modules.data_types import IssueStatus
from adws.adw_modules.issue_providers import LocalIssueProvider
from adws.adw_modules.agent import execute_template
from adws.adw_modules.workflow_ops import create_and_implement_patch


@dataclass
class BrokenADW:
    """Represents a broken ADW from validation status."""

    name: str
    import_status: str
    cli_status: str
    dry_run_status: str

    @property
    def complexity(self) -> int:
        """Calculate complexity score (number of failures)."""
        failures = 0
        if self.import_status == "FAIL":
            failures += 1
        if self.cli_status == "FAIL":
            failures += 1
        if self.dry_run_status == "FAIL":
            failures += 1
        return failures

    @property
    def failure_levels(self) -> List[str]:
        """Return list of failing validation levels."""
        failures = []
        if self.import_status == "FAIL":
            failures.append("import")
        if self.cli_status == "FAIL":
            failures.append("cli")
        if self.dry_run_status == "FAIL":
            failures.append("dry_run")
        return failures


def get_project_root() -> str:
    """Get the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_validation_status(status_path: str) -> List[BrokenADW]:
    """Parse VALIDATION_STATUS.md and return broken ADWs sorted by complexity.

    Args:
        status_path: Path to VALIDATION_STATUS.md

    Returns:
        List of BrokenADW objects, sorted by complexity (simplest first)
    """
    with open(status_path, "r") as f:
        content = f.read()

    # Extract table rows with "Needs Fix" status
    # Format: | name | PASS/FAIL | PASS/FAIL/N/A/SKIP | PASS/FAIL/N/A/SKIP | Needs Fix |
    pattern = r"\| (\w+) \| (PASS|FAIL) \| (PASS|FAIL|N/A|SKIP) \| (PASS|FAIL|N/A|SKIP) \| Needs Fix \|"

    broken_adws = []
    for match in re.finditer(pattern, content):
        name, import_s, cli_s, dry_run_s = match.groups()

        broken_adws.append(
            BrokenADW(
                name=name,
                import_status=import_s,
                cli_status=cli_s,
                dry_run_status=dry_run_s,
            )
        )

    # Sort by complexity (simplest first, per user preference)
    return sorted(broken_adws, key=lambda x: x.complexity)


def get_script_path(adw_name: str, project_root: str) -> Optional[Path]:
    """Get the path to an ADW script.

    Args:
        adw_name: Name of the ADW (e.g., "adw_patch_iso", "workflow_ops")
        project_root: Project root directory

    Returns:
        Path to the script or None if not found
    """
    adws_dir = Path(project_root) / "adws"

    # Check different locations
    candidates = [
        adws_dir / f"{adw_name}.py",  # Direct ADW script
        adws_dir / f"adw_{adw_name}.py",  # With adw_ prefix
        adws_dir / "adw_modules" / f"{adw_name}.py",  # Module
        adws_dir / "adw_triggers" / f"{adw_name}.py",  # Trigger
        adws_dir / "adw_triggers" / f"trigger_{adw_name}.py",  # Trigger with prefix
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def run_validation_level(
    script_path: Path, level: str, logger: logging.Logger
) -> Tuple[bool, str]:
    """Run a single validation level and capture output.

    Args:
        script_path: Path to the script to validate
        level: Validation level ("import", "cli", "dry_run")
        logger: Logger instance

    Returns:
        Tuple of (passed, output)
    """
    try:
        if level == "import":
            # Test import
            module_path = str(script_path.relative_to(Path.cwd()))
            module_name = module_path.replace("/", ".").replace(".py", "")
            cmd = ["python3", "-c", f"import {module_name}; print('OK')"]
            timeout = 30

        elif level == "cli":
            # Test CLI --help
            cmd = ["uv", "run", str(script_path), "--help"]
            timeout = 30

        elif level == "dry_run":
            # Test dry-run with test args
            cmd = ["uv", "run", str(script_path), "--dry-run", "test"]
            timeout = 120

        else:
            return False, f"Unknown validation level: {level}"

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path.cwd(),
        )

        output = result.stdout + result.stderr
        passed = result.returncode == 0

        return passed, output[:2000]  # Truncate long output

    except subprocess.TimeoutExpired:
        return False, f"Timeout after {timeout}s"
    except Exception as e:
        return False, str(e)


def create_fix_issue(
    provider: LocalIssueProvider, broken: BrokenADW, error_output: str
) -> str:
    """Create a local issue for fixing a broken ADW.

    Args:
        provider: LocalIssueProvider instance
        broken: BrokenADW object
        error_output: Captured error output from validation

    Returns:
        Issue ID
    """
    failures = broken.failure_levels

    title = f"Fix validation for {broken.name}"
    body = f"""## Description

The `{broken.name}` ADW is failing validation tests.

## Failing Levels

{chr(10).join(f'- {level}' for level in failures)}

## Current Status

- Import: {broken.import_status}
- CLI: {broken.cli_status}
- Dry-run: {broken.dry_run_status}

## Error Output

```
{error_output[:1500]}
```

## Acceptance Criteria

{chr(10).join(f'- [ ] {level} test passes' for level in failures)}

## Notes

This issue was auto-generated by `adw_fix_validation.py`.
"""

    issue = provider.create_issue(
        title=title,
        body=body,
        issue_id=f"fix-{broken.name}",
        labels=["validation", "auto-generated"],
    )

    return issue.id


def update_acceptance_criteria(
    issue_path: str,
    validation_results: Dict[str, bool],
    logger: logging.Logger,
) -> bool:
    """Update acceptance criteria checkboxes in issue based on validation results.

    Args:
        issue_path: Path to the issue markdown file
        validation_results: Dict mapping level name to pass/fail (e.g., {"cli": True, "dry_run": False})
        logger: Logger instance

    Returns:
        True if all criteria now pass, False otherwise
    """
    from pathlib import Path

    path = Path(issue_path)
    if not path.exists():
        logger.warning(f"Issue file not found: {issue_path}")
        return False

    content = path.read_text()

    # Update each checkbox based on validation results
    all_passed = True
    for level, passed in validation_results.items():
        # Match both checked and unchecked variants
        old_unchecked = f"- [ ] {level} test passes"
        old_checked = f"- [x] {level} test passes"
        new_value = f"- [x] {level} test passes" if passed else f"- [ ] {level} test passes"

        if old_unchecked in content:
            content = content.replace(old_unchecked, new_value)
        elif old_checked in content:
            content = content.replace(old_checked, new_value)

        if not passed:
            all_passed = False

    path.write_text(content)
    logger.info(f"Updated acceptance criteria in {issue_path}")

    return all_passed


def fix_single_adw(
    broken: BrokenADW,
    adw_id: str,
    logger: logging.Logger,
    dry_run: bool = False,
) -> Tuple[bool, str, Dict[str, bool]]:
    """Attempt to fix a single broken ADW.

    Args:
        broken: BrokenADW object
        adw_id: ADW ID for this fix attempt
        logger: Logger instance
        dry_run: If True, don't actually make changes

    Returns:
        Tuple of (success, message, validation_results)
        - success: True if fix was successful (all validations pass)
        - message: Human-readable status message
        - validation_results: Dict mapping level name to pass/fail
    """
    project_root = get_project_root()
    validation_results: Dict[str, bool] = {}

    # Find the script
    script_path = get_script_path(broken.name, project_root)

    if not script_path:
        return False, f"Script not found for: {broken.name}", {}

    # Run validation to capture actual error
    logger.info(f"Running validation on {broken.name} to capture error...")

    failures_detail = []
    for level in broken.failure_levels:
        passed, output = run_validation_level(script_path, level, logger)
        validation_results[level] = passed
        if not passed:
            failures_detail.append(f"**{level}**: FAILED")
            failures_detail.append(f"```\n{output[:500]}\n```")

    if not failures_detail:
        return True, "All validations now pass", validation_results

    # Build patch request
    patch_request = f"""Fix validation failures in {broken.name}:

Script: {script_path}

Failures:
{chr(10).join(failures_detail)}

Requirements:
1. Fix the specific error shown above
2. Maintain backward compatibility
3. Ensure the validation test will pass after fix
4. Do not add unnecessary dependencies
"""

    if dry_run:
        logger.info(f"[DRY RUN] Would create patch for:\n{patch_request[:300]}...")
        # Return current validation results - don't claim success
        return False, "Dry run - no changes made", validation_results

    # Use patch workflow
    try:
        patch_file, implement_response = create_and_implement_patch(
            adw_id=adw_id,
            review_change_request=patch_request,
            logger=logger,
            agent_name_planner="validation_fixer",
            agent_name_implementor="validation_fixer",
        )

        if not patch_file:
            return False, "Failed to create patch plan", validation_results

        if not implement_response or not implement_response.success:
            error_msg = implement_response.output if implement_response else "No response"
            return False, f"Patch failed: {error_msg[:200]}", validation_results

    except Exception as e:
        return False, f"Exception during patch: {str(e)}", validation_results

    # Re-run validation to verify fix
    logger.info("Re-running validation to verify fix...")

    all_passed = True
    for level in broken.failure_levels:
        passed, output = run_validation_level(script_path, level, logger)
        validation_results[level] = passed
        if not passed:
            all_passed = False
            logger.warning(f"Level {level} still failing: {output[:100]}")

    if all_passed:
        return True, "Fix verified - all validations pass", validation_results
    else:
        return False, "Fix incomplete - some validations still failing", validation_results


def main():
    """Main entry point."""
    load_dotenv()

    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    target_adw = None

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--adw-name" and i + 1 < len(sys.argv):
            target_adw = sys.argv[i + 1]
        elif arg.startswith("--adw-name="):
            target_adw = arg.split("=")[1]
        elif not arg.startswith("-"):
            # Positional argument could be ADW name
            if target_adw is None:
                target_adw = arg

    # Generate ADW ID
    adw_id = make_adw_id()
    logger = setup_logger(adw_id, "adw_fix_validation")

    logger.info(f"ADW Fix Validation starting - ID: {adw_id}")
    if dry_run:
        logger.info("[DRY RUN MODE]")

    project_root = get_project_root()
    status_path = Path(project_root) / "adws" / "VALIDATION_STATUS.md"

    if not status_path.exists():
        logger.error(f"VALIDATION_STATUS.md not found at {status_path}")
        print(f"Error: VALIDATION_STATUS.md not found at {status_path}")
        sys.exit(1)

    # Parse broken ADWs
    broken_adws = parse_validation_status(str(status_path))

    if target_adw:
        broken_adws = [b for b in broken_adws if b.name == target_adw]
        if not broken_adws:
            logger.error(f"ADW '{target_adw}' not found in validation status or not broken")
            print(f"Error: ADW '{target_adw}' not found in validation status or not broken")
            sys.exit(1)

    logger.info(f"Found {len(broken_adws)} broken ADWs to fix")
    print(f"\nBroken ADWs ({len(broken_adws)} total):")
    for b in broken_adws:
        print(f"  - {b.name} (complexity: {b.complexity}, failures: {', '.join(b.failure_levels)})")

    if not broken_adws:
        logger.info("No broken ADWs found - all validations passing!")
        print("\nAll ADW validations passing!")
        return

    # Initialize local issue provider
    issue_provider = LocalIssueProvider(project_root)

    results = []
    for broken in broken_adws:
        print(f"\n{'='*60}")
        print(f"Processing: {broken.name} (complexity: {broken.complexity})")
        print(f"Failing: {', '.join(broken.failure_levels)}")
        logger.info(f"Processing: {broken.name}")

        # Capture initial error for issue
        script_path = get_script_path(broken.name, project_root)
        error_output = ""
        if script_path:
            for level in broken.failure_levels:
                passed, output = run_validation_level(script_path, level, logger)
                if not passed:
                    error_output += f"\n--- {level} ---\n{output}\n"

        # Create or fetch local issue
        issue_id = f"fix-{broken.name}"
        try:
            issue = issue_provider.fetch_issue(issue_id)
            logger.info(f"Found existing issue: {issue.local_path}")
        except FileNotFoundError:
            issue_id = create_fix_issue(issue_provider, broken, error_output)
            issue = issue_provider.fetch_issue(issue_id)
            logger.info(f"Created new issue: {issue.local_path}")
            print(f"Created issue: {issue.local_path}")

        # Update status to in_progress
        issue_provider.update_status(
            issue, IssueStatus.IN_PROGRESS, "Starting fix attempt", adw_id
        )

        # Attempt fix
        success, message, validation_results = fix_single_adw(broken, adw_id, logger, dry_run)

        # Update acceptance criteria checkboxes based on validation results
        if validation_results and issue.local_path:
            all_criteria_pass = update_acceptance_criteria(
                issue.local_path, validation_results, logger
            )
            # Only mark as resolved if ALL criteria pass (not just success from fix attempt)
            if all_criteria_pass:
                success = True
                message = "All acceptance criteria validated and passing"

        # Update issue status based on actual validation results
        if dry_run:
            # In dry-run mode, keep status as in_progress (work not actually done)
            new_status = IssueStatus.IN_PROGRESS
            issue_provider.update_status(issue, new_status, f"[DRY RUN] {message}", adw_id)
        else:
            new_status = IssueStatus.RESOLVED if success else IssueStatus.OPEN
            issue_provider.update_status(issue, new_status, message, adw_id)

        results.append((broken.name, success, message))

        status_icon = "✓" if success else "✗"
        if dry_run:
            status_icon = "○"  # Indicate dry-run (no action taken)
        print(f"Result: [{status_icon}] {message[:60]}...")
        logger.info(f"Result: {'SUCCESS' if success else 'FAILED'} - {message}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    success_count = sum(1 for _, s, _ in results if s)
    print(f"Fixed: {success_count}/{len(results)}")

    for name, success, message in results:
        status = "✓" if success else "✗"
        print(f"  [{status}] {name}: {message[:50]}...")

    logger.info(f"Completed: {success_count}/{len(results)} fixed")


if __name__ == "__main__":
    main()
