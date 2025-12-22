#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "click", "rich"]
# ///

"""
ADW Ship Iso - AI Developer Workflow for shipping (merging) to main

Usage:
  uv run adws/adw_ship_iso.py <issue-number> <adw-id> [--dry-run]

Workflow:
1. Load state and validate worktree exists
2. Validate ALL state fields are populated (not None)
3. Perform manual git merge in main repository:
   - Fetch latest from origin
   - Checkout main
   - Merge feature branch
   - Push to origin/main
4. Post success message to issue

This workflow REQUIRES that all previous workflows have been run and that
every field in ADWState has a value. This is our final approval step.

Note: Merge operations happen in the main repository root, not in the worktree,
to preserve the worktree's state.
"""

import sys
import os
import logging
import json
import subprocess
import click
from typing import Optional, Dict, Any, Tuple
from dotenv import load_dotenv
from rich.console import Console

try:
    from adw_modules.state import ADWState
    from adw_modules.github import (
        make_issue_comment,
        get_repo_url,
        extract_repo_path,
    )
    from adw_modules.workflow_ops import format_issue_message
    from adw_modules.utils import setup_logger, check_env_vars
    from adw_modules.worktree_ops import validate_worktree
    from adw_modules.data_types import ADWStateData
except ImportError:
    # Handle running from different contexts
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from adws.adw_modules.state import ADWState
    from adws.adw_modules.github import (
        make_issue_comment,
        get_repo_url,
        extract_repo_path,
    )
    from adws.adw_modules.workflow_ops import format_issue_message
    from adws.adw_modules.utils import setup_logger, check_env_vars
    from adws.adw_modules.worktree_ops import validate_worktree
    from adws.adw_modules.data_types import ADWStateData

console = Console()

# Agent name constant
AGENT_SHIPPER = "shipper"


def get_main_repo_root() -> str:
    """Get the main repository root directory (parent of adws)."""
    # This script is in adws/, so go up one level to get repo root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def manual_merge_to_main(
    branch_name: str, logger: logging.Logger, dry_run: bool = False
) -> Tuple[bool, Optional[str]]:
    """Manually merge a branch to main using git commands.

    This runs in the main repository root, not in a worktree.

    Args:
        branch_name: The feature branch to merge
        logger: Logger instance
        dry_run: If True, only validate without executing

    Returns:
        Tuple of (success, error_message)
    """
    repo_root = get_main_repo_root()
    logger.info(f"Performing manual merge in main repository: {repo_root}")

    if dry_run:
        logger.info("[DRY RUN] Would perform the following operations:")
        logger.info(f"  1. Fetch latest from origin")
        logger.info(f"  2. Checkout main branch")
        logger.info(f"  3. Pull latest main")
        logger.info(f"  4. Merge branch '{branch_name}' with --no-ff")
        logger.info(f"  5. Push to origin/main")
        logger.info(f"  6. Restore original branch")
        return True, None

    try:
        # Save current branch to restore later
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=repo_root
        )
        original_branch = result.stdout.strip()
        logger.debug(f"Original branch: {original_branch}")

        # Step 1: Fetch latest from origin
        logger.info("Fetching latest from origin...")
        result = subprocess.run(
            ["git", "fetch", "origin"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to fetch from origin: {result.stderr}"

        # Step 2: Checkout main
        logger.info("Checking out main branch...")
        result = subprocess.run(
            ["git", "checkout", "main"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to checkout main: {result.stderr}"

        # Step 3: Pull latest main
        logger.info("Pulling latest main...")
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            # Try to restore original branch
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
            return False, f"Failed to pull latest main: {result.stderr}"

        # Step 4: Merge the feature branch (no-ff to preserve all commits)
        logger.info(f"Merging branch {branch_name} (no-ff to preserve all commits)...")
        result = subprocess.run(
            ["git", "merge", branch_name, "--no-ff", "-m", f"Merge branch '{branch_name}' via ADW Ship workflow"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            # Try to restore original branch
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
            return False, f"Failed to merge {branch_name}: {result.stderr}"

        # Step 5: Push to origin/main
        logger.info("Pushing to origin/main...")
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            # Try to restore original branch
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
            return False, f"Failed to push to origin/main: {result.stderr}"

        # Step 6: Restore original branch
        logger.info(f"Restoring original branch: {original_branch}")
        subprocess.run(["git", "checkout", original_branch], cwd=repo_root)

        logger.info("✅ Successfully merged and pushed to main!")
        return True, None

    except Exception as e:
        logger.error(f"Unexpected error during merge: {e}")
        # Try to restore original branch
        try:
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
        except:
            pass
        return False, str(e)


def validate_state_completeness(state: ADWState, logger: logging.Logger) -> tuple[bool, list[str]]:
    """Validate that all fields in ADWState have values (not None).

    Returns:
        tuple of (is_valid, missing_fields)
    """
    # Get the expected fields from ADWStateData model
    expected_fields = {
        "adw_id",
        "issue_number",
        "branch_name",
        "plan_file",
        "issue_class",
        "worktree_path",
        "backend_port",
        "frontend_port",
    }

    missing_fields = []

    for field in expected_fields:
        value = state.get(field)
        if value is None:
            missing_fields.append(field)
            logger.warning(f"Missing required field: {field}")
        else:
            logger.debug(f"✓ {field}: {value}")

    return len(missing_fields) == 0, missing_fields


@click.command()
@click.argument("issue_number")
@click.argument("adw_id", required=False, default=None)
@click.option("--dry-run", is_flag=True, help="Validate without executing merge operations")
def main(issue_number: str, adw_id: Optional[str], dry_run: bool = False):
    """Main entry point for ADW Ship Iso workflow.

    Args:
        issue_number: GitHub issue number (or local issue reference)
        adw_id: ADW identifier (optional for --dry-run)
        dry_run: If True, validate without executing
    """
    # Load environment variables
    load_dotenv()

    # For dry-run mode, generate a test ADW ID if not provided
    if dry_run and not adw_id:
        import uuid
        adw_id = f"test-{uuid.uuid4().hex[:8]}"

    # Dry-run mode: exit early with minimal operations (no state/network calls)
    if dry_run:
        console.print("[yellow]DRY RUN MODE[/yellow] - Validation only")
        console.print("[DRY RUN] Would execute ship workflow:")
        console.print(f"  - Issue ref: {issue_number}")
        console.print(f"  - ADW ID: {adw_id}")
        console.print(f"  - Load and validate state completeness")
        console.print(f"  - Validate worktree exists")
        console.print(f"  - Merge feature branch to main")
        console.print(f"  - Push to origin/main")
        console.print(f"  - Post success message to issue")
        return

    # Require adw_id for non-dry-run mode
    if not adw_id:
        console.print("[red]Error: adw_id is required when not using --dry-run[/red]")
        console.print("Usage: uv run adws/adw_ship_iso.py <issue-number> <adw-id> [--dry-run]")
        sys.exit(1)

    # Try to load existing state
    temp_logger = setup_logger(adw_id, "adw_ship_iso")
    state = ADWState.load(adw_id, temp_logger)
    if not state:
        # No existing state found
        logger = setup_logger(adw_id, "adw_ship_iso")
        logger.error(f"No state found for ADW ID: {adw_id}")
        logger.error("Run the complete SDLC workflow before shipping")
        console.print(f"\n[red]Error: No state found for ADW ID: {adw_id}[/red]")
        console.print("Run the complete SDLC workflow before shipping")
        sys.exit(1)

    # Update issue number from state if available
    issue_number = state.get("issue_number", issue_number)

    # Track that this ADW workflow has run
    if not dry_run:
        state.append_adw_id("adw_ship_iso")

    # Set up logger with ADW ID
    logger = setup_logger(adw_id, "adw_ship_iso")
    logger.info(f"ADW Ship Iso starting - ID: {adw_id}, Issue: {issue_number}, Dry-run: {dry_run}")

    # Validate environment
    check_env_vars(logger)

    # Post initial status (skip in dry-run mode)
    if not dry_run:
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"🚢 Starting ship workflow\n"
                               f"📋 Validating state completeness...")
        )

    # Step 1: Validate state completeness
    logger.info("Validating state completeness...")
    is_valid, missing_fields = validate_state_completeness(state, logger)

    if not is_valid:
        error_msg = f"State validation failed. Missing fields: {', '.join(missing_fields)}"
        logger.error(error_msg)
        if not dry_run:
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, AGENT_SHIPPER, f"❌ {error_msg}\n\n"
                                   "Please ensure all workflows have been run:\n"
                                   "- adw_plan_iso.py (creates plan_file, branch_name, issue_class)\n"
                                   "- adw_build_iso.py (implements the plan)\n"
                                   "- adw_test_iso.py (runs tests)\n"
                                   "- adw_review_iso.py (reviews implementation)\n"
                                   "- adw_document_iso.py (generates docs)")
            )
        console.print(f"[red]{error_msg}[/red]")
        sys.exit(1)

    logger.info("✅ State validation passed - all fields have values")

    # Step 2: Validate worktree exists
    valid, error = validate_worktree(adw_id, state)
    if not valid:
        logger.error(f"Worktree validation failed: {error}")
        if not dry_run:
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, AGENT_SHIPPER, f"❌ Worktree validation failed: {error}")
            )
        console.print(f"[red]Worktree validation failed: {error}[/red]")
        sys.exit(1)

    worktree_path = state.get("worktree_path")
    logger.info(f"✅ Worktree validated at: {worktree_path}")

    # Step 3: Get branch name
    branch_name = state.get("branch_name")
    logger.info(f"Preparing to merge branch: {branch_name}")

    if not dry_run:
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_SHIPPER, f"📋 State validation complete\n"
                               f"🔍 Preparing to merge branch: {branch_name}")
        )

    # Step 4: Perform manual merge (or validate in dry-run)
    logger.info(f"Starting manual merge of {branch_name} to main...")
    if not dry_run:
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_SHIPPER, f"🔀 Merging {branch_name} to main...\n"
                               "Using manual git operations in main repository")
        )

    success, error = manual_merge_to_main(branch_name, logger, dry_run=dry_run)

    if not success:
        logger.error(f"Failed to merge: {error}")
        if not dry_run:
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, AGENT_SHIPPER, f"❌ Failed to merge: {error}")
            )
        console.print(f"[red]Failed to merge: {error}[/red]")
        sys.exit(1)

    if dry_run:
        console.print("[green]✅ DRY RUN VALIDATION PASSED[/green]")
        console.print(f"All validations passed for branch: {branch_name}")
        console.print("Run without --dry-run to execute the merge")
        logger.info("Dry run completed successfully")
        sys.exit(0)

    logger.info(f"✅ Successfully merged {branch_name} to main")

    # Step 5: Post success message
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_SHIPPER,
                           f"🎉 **Successfully shipped!**\n\n"
                           f"✅ Validated all state fields\n"
                           f"✅ Merged branch `{branch_name}` to main\n"
                           f"✅ Pushed to origin/main\n\n"
                           f"🚢 Code has been deployed to production!")
    )

    # Save final state
    state.save("adw_ship_iso")

    # Post final state summary
    make_issue_comment(
        issue_number,
        f"{adw_id}_ops: 📋 Final ship state:\n```json\n{json.dumps(state.data, indent=2)}\n```"
    )

    logger.info("Ship workflow completed successfully")
    console.print("[green]✅ Ship workflow completed successfully[/green]")


if __name__ == "__main__":
    main()
