#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "click", "rich"]
# ///

"""
ADW Rebase ISO - AI Developer Workflow for PR-first merge conflict resolution

Usage:
  uv run adws/adw_rebase_iso.py <pr-number> [adw-id] [--dry-run]

PR Number Formats:
  - PR number: "2" or "123" (GitHub PR identifier)
  - With optional ADW ID: "2 a6edbc74" (explicit state lookup)

Examples:
  uv run adws/adw_rebase_iso.py 2                    # Auto-discover state from PR branch
  uv run adws/adw_rebase_iso.py 2 a6edbc74           # Explicit state lookup
  uv run adws/adw_rebase_iso.py 2 --dry-run          # Validate without executing

Workflow:
1. Fetch PR details via gh pr view (branch name, title, status)
2. Discover ADW state by matching branch name (or use provided adw-id)
3. Validate worktree exists and is properly configured
4. Fetch latest origin/main in the worktree
5. Detect divergence from main (commits ahead)
6. Attempt rebase onto origin/main
7. Report conflict files if rebase fails
8. Force-push rebased branch to update PR if successful
9. Post progress to linked issue (if available)

Key Features:
- PR-first interface (primary input is PR number)
- Auto-discovers ADW state from PR branch name
- Operates entirely in isolated worktree
- Handles conflicts gracefully with detailed reporting
- Force-pushes to update PR automatically
- Posts progress to linked GitHub issues

Note: Force-push is necessary after rebase to update the PR. This only affects
the feature branch in the isolated worktree, never main.
"""

import sys
import os
import logging
import json
import subprocess
import click
from typing import Optional, Dict, Any, Tuple, List
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console

try:
    from adw_modules.state import ADWState
    from adw_modules.git_ops import push_branch, get_current_branch
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
    from adws.adw_modules.git_ops import push_branch, get_current_branch
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
AGENT_REBASER = "rebaser"


def get_project_root() -> str:
    """Get the project root directory."""
    # This script is in adws/, so go up one level to get project root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fetch_pr_details(pr_number: str, logger: logging.Logger) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Fetch PR details using gh CLI.

    Args:
        pr_number: GitHub PR number
        logger: Logger instance

    Returns:
        Tuple of (pr_data_dict, error_message)
    """
    logger.info(f"Fetching PR #{pr_number} details...")

    try:
        result = subprocess.run(
            ["gh", "pr", "view", pr_number, "--json", "headRefName,number,title,state,url"],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            if "could not find pull request" in error_msg.lower():
                return None, f"PR #{pr_number} not found. Please verify the PR number."
            elif "gh: command not found" in error_msg.lower():
                return None, "GitHub CLI (gh) not found. Please install it: https://cli.github.com/"
            else:
                return None, f"Failed to fetch PR: {error_msg}"

        pr_data = json.loads(result.stdout)
        logger.info(f"PR #{pr_data['number']}: {pr_data['title']}")
        logger.info(f"Branch: {pr_data['headRefName']}")
        logger.info(f"State: {pr_data['state']}")
        logger.info(f"URL: {pr_data['url']}")

        return pr_data, None

    except json.JSONDecodeError as e:
        return None, f"Failed to parse PR data: {e}"
    except Exception as e:
        return None, f"Unexpected error fetching PR: {e}"


def find_adw_state_by_branch(branch_name: str, logger: logging.Logger) -> Optional[Tuple[str, ADWState]]:
    """Find ADW state by matching branch name.

    Args:
        branch_name: Branch name from PR
        logger: Logger instance

    Returns:
        Tuple of (adw_id, loaded_state) if found, None otherwise
    """
    logger.info(f"Searching for ADW state with branch: {branch_name}")

    project_root = get_project_root()
    agents_dir = Path(project_root) / "agents"

    if not agents_dir.exists():
        logger.warning(f"Agents directory not found: {agents_dir}")
        return None

    # Scan all agent subdirectories for adw_state.json
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue

        state_file = agent_dir / "adw_state.json"
        if not state_file.exists():
            continue

        try:
            logger.debug(f"Checking state file: {state_file}")
            with open(state_file, 'r') as f:
                state_data = json.load(f)

            # Match branch_name field
            if state_data.get('branch_name') == branch_name:
                adw_id = agent_dir.name
                logger.info(f"Found matching state: adw_id={adw_id}")

                # Load state using ADWState
                state = ADWState.load(adw_id)
                return adw_id, state

        except Exception as e:
            logger.debug(f"Error reading {state_file}: {e}")
            continue

    logger.warning(f"No ADW state found with branch: {branch_name}")
    return None


def detect_rebase_conflicts(worktree_path: str, logger: logging.Logger) -> Tuple[bool, List[str]]:
    """Detect if rebase onto main would have conflicts.

    Args:
        worktree_path: Path to worktree
        logger: Logger instance

    Returns:
        Tuple of (has_divergence, list_of_diverged_commits)
    """
    logger.info("Detecting divergence from origin/main...")

    try:
        # Fetch latest origin/main
        logger.info("Fetching latest origin/main...")
        result = subprocess.run(
            ["git", "fetch", "origin", "main"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
            check=False
        )

        if result.returncode != 0:
            logger.error(f"Failed to fetch origin/main: {result.stderr}")
            return False, []

        # Check for divergence
        result = subprocess.run(
            ["git", "log", "--oneline", "origin/main..HEAD"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
            check=False
        )

        if result.returncode != 0:
            logger.error(f"Failed to check divergence: {result.stderr}")
            return False, []

        diverged_commits = result.stdout.strip().split('\n') if result.stdout.strip() else []

        if diverged_commits:
            logger.info(f"Branch has {len(diverged_commits)} commit(s) ahead of origin/main:")
            for commit in diverged_commits:
                logger.info(f"  {commit}")
            return True, diverged_commits
        else:
            logger.info("Branch is up-to-date with origin/main (no divergence)")
            return False, []

    except Exception as e:
        logger.error(f"Error detecting conflicts: {e}")
        return False, []


def rebase_onto_main(worktree_path: str, logger: logging.Logger, dry_run: bool = False) -> Tuple[bool, Optional[str], List[str]]:
    """Rebase current branch onto origin/main.

    Args:
        worktree_path: Path to worktree
        logger: Logger instance
        dry_run: If True, only validate without executing

    Returns:
        Tuple of (success, error_message, conflict_files_list)
    """
    logger.info("Attempting rebase onto origin/main...")

    if dry_run:
        logger.info("[DRY RUN] Would perform the following operations:")
        logger.info("  1. git fetch origin main")
        logger.info("  2. git rebase origin/main")
        logger.info("  3. Handle conflicts if any")
        return True, None, []

    try:
        # Perform rebase
        result = subprocess.run(
            ["git", "rebase", "origin/main"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
            check=False
        )

        if result.returncode == 0:
            logger.info("✅ Rebase successful!")
            return True, None, []

        # Rebase failed - check for conflicts
        logger.warning("Rebase encountered conflicts")

        # Get list of conflicting files
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
            check=False
        )

        conflict_files = []
        if status_result.returncode == 0:
            for line in status_result.stdout.strip().split('\n'):
                if line.startswith('UU ') or line.startswith('AA ') or line.startswith('DD '):
                    # Unmerged paths
                    conflict_files.append(line[3:].strip())

        # Abort the rebase to preserve worktree state
        logger.info("Aborting rebase to preserve worktree state...")
        abort_result = subprocess.run(
            ["git", "rebase", "--abort"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
            check=False
        )

        if abort_result.returncode != 0:
            logger.warning(f"Failed to abort rebase: {abort_result.stderr}")

        error_msg = result.stderr.strip() if result.stderr else "Unknown rebase error"
        return False, error_msg, conflict_files

    except Exception as e:
        logger.error(f"Unexpected error during rebase: {e}")
        return False, str(e), []


def force_push_branch(branch_name: str, worktree_path: str, logger: logging.Logger) -> Tuple[bool, Optional[str]]:
    """Force-push branch to origin to update PR.

    Args:
        branch_name: Branch name to push
        worktree_path: Path to worktree
        logger: Logger instance

    Returns:
        Tuple of (success, error_message)
    """
    logger.info(f"Force-pushing branch '{branch_name}' to origin...")

    try:
        result = subprocess.run(
            ["git", "push", "origin", branch_name, "--force"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
            check=False
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            logger.error(f"Force-push failed: {error_msg}")
            return False, error_msg

        logger.info("✅ Force-push successful! PR will auto-update.")
        return True, None

    except Exception as e:
        logger.error(f"Unexpected error during force-push: {e}")
        return False, str(e)


@click.command()
@click.argument('pr_number', type=str)
@click.argument('adw_id', type=str, required=False)
@click.option('--dry-run', is_flag=True, help='Validate without executing operations')
def main(pr_number: str, adw_id: Optional[str], dry_run: bool):
    """Rebase feature branch onto origin/main to resolve PR conflicts.

    PR_NUMBER: GitHub PR number (required)
    ADW_ID: Optional ADW ID for direct state lookup
    """
    load_dotenv()

    # Early validation
    if dry_run:
        console.print("[bold yellow]🔍 DRY RUN MODE - Validation only[/bold yellow]")

    # Step 1: Fetch PR details
    console.print(f"[bold cyan]Fetching PR #{pr_number} details...[/bold cyan]")

    # Create temporary logger for PR fetch
    temp_logger = logging.getLogger("adw_rebase_iso_temp")
    temp_logger.setLevel(logging.INFO)
    if not temp_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        temp_logger.addHandler(handler)

    pr_data, pr_error = fetch_pr_details(pr_number, temp_logger)

    if pr_error:
        console.print(f"[bold red]❌ Error: {pr_error}[/bold red]")
        sys.exit(1)

    if not pr_data:
        console.print(f"[bold red]❌ Failed to fetch PR #{pr_number}[/bold red]")
        sys.exit(1)

    branch_name = pr_data['headRefName']
    pr_title = pr_data['title']
    pr_state = pr_data['state']
    pr_url = pr_data['url']

    console.print(f"[green]✅ PR found:[/green] {pr_title}")
    console.print(f"[dim]Branch: {branch_name} | State: {pr_state}[/dim]")

    # Warn if PR is not open
    if pr_state.upper() != 'OPEN':
        console.print(f"[bold yellow]⚠️  Warning: PR is {pr_state}, not OPEN[/bold yellow]")

    # Step 2: Find ADW state
    console.print(f"\n[bold cyan]Discovering ADW state...[/bold cyan]")

    state = None
    resolved_adw_id = adw_id

    if adw_id:
        # Use provided adw_id
        console.print(f"Using provided ADW ID: {adw_id}")
        try:
            state = ADWState.load(adw_id)
            if not state:
                console.print(f"[bold red]❌ No state file found for adw_id={adw_id}[/bold red]")
                console.print(f"[yellow]Expected path: agents/{adw_id}/adw_state.json[/yellow]")
                sys.exit(1)
            console.print(f"[green]✅ State loaded[/green]")
        except Exception as e:
            console.print(f"[bold red]❌ Failed to load state for adw_id={adw_id}: {e}[/bold red]")
            sys.exit(1)
    else:
        # Auto-discover by branch name
        console.print(f"Auto-discovering state by branch: {branch_name}")
        result = find_adw_state_by_branch(branch_name, temp_logger)

        if not result:
            console.print(f"[bold red]❌ No ADW state found for branch: {branch_name}[/bold red]")
            console.print("\n[yellow]💡 Hint: Provide adw-id explicitly if you know it:[/yellow]")
            console.print(f"[dim]  uv run adws/adw_rebase_iso.py {pr_number} <adw-id>[/dim]")
            sys.exit(1)

        resolved_adw_id, state = result
        console.print(f"[green]✅ Found ADW state: {resolved_adw_id}[/green]")

    # Validate state has required fields
    state_branch = state.get("branch_name")
    state_worktree = state.get("worktree_path")

    if not state_branch:
        console.print(f"[bold red]❌ State missing branch_name[/bold red]")
        sys.exit(1)

    if not state_worktree:
        console.print(f"[bold red]❌ State missing worktree_path[/bold red]")
        sys.exit(1)

    # Verify branch matches PR
    if state_branch != branch_name:
        console.print(f"[bold yellow]⚠️  Warning: State branch ({state_branch}) differs from PR branch ({branch_name})[/bold yellow]")

    # Setup logger
    logger = setup_logger(resolved_adw_id, "adw_rebase_iso")
    logger.info(f"Starting rebase workflow for PR #{pr_number} (ADW {resolved_adw_id})")

    # Check environment (gh CLI handles GitHub authentication)
    check_env_vars(logger)

    # Step 3: Validate worktree
    console.print(f"\n[bold cyan]Validating worktree...[/bold cyan]")

    if not validate_worktree(resolved_adw_id, state):
        console.print(f"[bold red]❌ Worktree validation failed[/bold red]")
        console.print(f"[yellow]Expected path: {state_worktree}[/yellow]")
        sys.exit(1)

    console.print(f"[green]✅ Worktree valid: {state_worktree}[/green]")

    # Post initial status to issue
    issue_number = state.get("issue_number")
    if issue_number:
        try:
            message = f"🔄 Starting rebase workflow for PR #{pr_number}\n\n"
            message += f"**Branch:** `{branch_name}`\n"
            message += f"**PR URL:** {pr_url}\n"
            message += f"**Worktree:** `{state_worktree}`"

            make_issue_comment(
                issue_number,
                format_issue_message(resolved_adw_id, AGENT_REBASER, message)
            )
            logger.info(f"Posted initial status to issue #{issue_number}")
        except Exception as e:
            logger.warning(f"Failed to post to issue: {e}")

    # Step 4: Detect conflicts
    console.print(f"\n[bold cyan]Detecting divergence from origin/main...[/bold cyan]")

    has_divergence, diverged_commits = detect_rebase_conflicts(state_worktree, logger)

    if not has_divergence:
        console.print("[green]✅ Branch is up-to-date with origin/main (no rebase needed)[/green]")

        if issue_number:
            try:
                message = "✅ Branch is already up-to-date with origin/main. No rebase needed."
                make_issue_comment(
                    issue_number,
                    format_issue_message(resolved_adw_id, AGENT_REBASER, message)
                )
            except Exception as e:
                logger.warning(f"Failed to post to issue: {e}")

        sys.exit(0)

    console.print(f"[yellow]Branch has {len(diverged_commits)} commit(s) ahead of origin/main[/yellow]")

    # Step 5: Attempt rebase
    console.print(f"\n[bold cyan]Rebasing onto origin/main...[/bold cyan]")

    success, error_msg, conflict_files = rebase_onto_main(state_worktree, logger, dry_run)

    if dry_run:
        console.print("[bold green]✅ DRY RUN COMPLETE - All validations passed[/bold green]")
        sys.exit(0)

    if not success:
        # Rebase failed - report conflicts
        console.print(f"[bold red]❌ Rebase failed with conflicts[/bold red]")

        conflict_report = "## ⚠️ Rebase Conflict Detected\n\n"
        conflict_report += f"**PR:** #{pr_number} ({pr_title})\n"
        conflict_report += f"**Branch:** `{branch_name}`\n"
        conflict_report += f"**Error:** {error_msg}\n\n"

        if conflict_files:
            conflict_report += "### Conflicting Files:\n"
            for file in conflict_files:
                conflict_report += f"- `{file}`\n"
            conflict_report += "\n"

        conflict_report += "### Resolution Options:\n"
        conflict_report += "1. **Manual Resolution:** Resolve conflicts in the worktree and re-run this workflow\n"
        conflict_report += "2. **Agent Assistance:** Use conflict resolver agent (future enhancement)\n"
        conflict_report += f"3. **Worktree Path:** `{state_worktree}`\n"

        console.print(conflict_report)

        # Post to issue
        if issue_number:
            try:
                make_issue_comment(
                    issue_number,
                    format_issue_message(resolved_adw_id, AGENT_REBASER, conflict_report)
                )
                logger.info(f"Posted conflict report to issue #{issue_number}")
            except Exception as e:
                logger.warning(f"Failed to post conflict report: {e}")

        sys.exit(1)

    # Rebase succeeded!
    console.print("[bold green]✅ Rebase successful![/bold green]")

    # Step 6: Force-push to update PR
    console.print(f"\n[bold cyan]Force-pushing to update PR...[/bold cyan]")

    push_success, push_error = force_push_branch(branch_name, state_worktree, logger)

    if not push_success:
        console.print(f"[bold red]❌ Force-push failed: {push_error}[/bold red]")

        if issue_number:
            try:
                message = f"⚠️ Rebase succeeded but force-push failed\n\n"
                message += f"**Error:** {push_error}\n"
                message += f"**Next Steps:** Manually push from worktree or check permissions"
                make_issue_comment(
                    issue_number,
                    format_issue_message(resolved_adw_id, AGENT_REBASER, message)
                )
            except Exception as e:
                logger.warning(f"Failed to post push error to issue: {e}")

        sys.exit(1)

    console.print(f"[bold green]✅ PR #{pr_number} updated successfully![/bold green]")
    console.print(f"[dim]View PR: {pr_url}[/dim]")

    # Post success message to issue
    if issue_number:
        try:
            message = f"✅ Successfully rebased onto origin/main and force-pushed\n\n"
            message += f"**PR #{pr_number}:** {pr_title}\n"
            message += f"**PR URL:** {pr_url}\n"
            message += f"**Branch:** `{branch_name}`\n"
            message += f"**Commits ahead:** {len(diverged_commits)}\n\n"
            message += "The PR has been automatically updated with the rebased commits."

            make_issue_comment(
                issue_number,
                format_issue_message(resolved_adw_id, AGENT_REBASER, message)
            )
            logger.info(f"Posted success message to issue #{issue_number}")
        except Exception as e:
            logger.warning(f"Failed to post success message: {e}")

    # Step 7: Update state
    console.print(f"\n[bold cyan]Updating ADW state...[/bold cyan]")

    # Append to all_adws if not already present
    all_adws = state.get("all_adws", [])
    if 'adw_rebase_iso' not in all_adws:
        all_adws.append('adw_rebase_iso')
        state.update(all_adws=all_adws)

    # Save state
    state.save("adw_rebase_iso")
    logger.info("State updated and saved")

    console.print("[bold green]✅ Rebase workflow complete![/bold green]")


if __name__ == "__main__":
    main()
