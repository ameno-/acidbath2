#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml"]
# ///
"""Parallel Review Orchestrator - Reviews all open PRs/MRs in parallel.

This ADW orchestrates parallel execution of code reviews across multiple branches.
It discovers all open PRs/MRs, syncs each branch with main, and launches reviews
concurrently with configurable parallelism.

Usage:
    python adw_review_all_iso.py --max-concurrent 3 --platform github
    python adw_review_all_iso.py --skip-sync --skip-resolution
    python adw_review_all_iso.py --retry-failed

Features:
    - Discovers all open PRs/MRs on GitHub and/or GitLab
    - Syncs branches with latest main before review
    - Parallel execution with configurable concurrency
    - Generates visual evidence (screenshots/diff visualizations)
    - Posts review results to each PR/MR
    - Creates consolidated report across all reviews
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from adws.adw_modules.code_review_providers import (
    get_code_review_provider,
    GitHubCodeReviewProvider,
    GitLabCodeReviewProvider,
)
from adws.adw_modules.data_types import CodeReview, CodeReviewPlatform
from adws.adw_modules.git_ops import sync_branch_with_main, get_commits_behind_main


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Setup a logger with console output.

    Args:
        name: Logger name
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Only add handler if logger doesn't have one already
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Parallel Review Orchestrator - Review all open PRs/MRs"
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=3,
        help="Maximum number of concurrent reviews (default: 3)",
    )
    parser.add_argument(
        "--platform",
        choices=["github", "gitlab", "all"],
        default="all",
        help="Platform to review (default: all)",
    )
    parser.add_argument(
        "--skip-sync",
        action="store_true",
        help="Skip syncing branches with main",
    )
    parser.add_argument(
        "--skip-resolution",
        action="store_true",
        help="Skip blocker issue resolution",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry only previously failed reviews",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be reviewed without actually running reviews",
    )
    parser.add_argument(
        "--cwd",
        type=str,
        default=".",
        help="Working directory for git operations (default: current directory)",
    )
    parser.add_argument(
        "--adw-id",
        type=str,
        help="ADW ID for tracking (generated if not provided)",
    )
    parser.add_argument(
        "--main-branch",
        type=str,
        default="main",
        help="Main branch name (default: main)",
    )
    return parser.parse_args()


def generate_adw_id() -> str:
    """Generate a unique ADW ID for this orchestration run."""
    import hashlib
    timestamp = datetime.now().isoformat()
    return hashlib.sha256(timestamp.encode()).hexdigest()[:8]


def discover_open_reviews(
    platform: str,
    cwd: str,
    logger: logging.Logger,
) -> List[CodeReview]:
    """Discover all open PRs/MRs on the specified platform(s).

    Args:
        platform: Platform to check ("github", "gitlab", or "all")
        cwd: Working directory for git operations
        logger: Logger instance

    Returns:
        List of CodeReview objects for open PRs/MRs
    """
    all_reviews: List[CodeReview] = []

    if platform in ["github", "all"]:
        try:
            github_provider = GitHubCodeReviewProvider(logger=logger)
            github_reviews = github_provider.list_open_reviews(cwd=cwd)
            all_reviews.extend(github_reviews)
            logger.info(f"Discovered {len(github_reviews)} open GitHub PRs")
        except Exception as e:
            logger.error(f"Failed to discover GitHub PRs: {e}")

    if platform in ["gitlab", "all"]:
        try:
            gitlab_provider = GitLabCodeReviewProvider(logger=logger)
            gitlab_reviews = gitlab_provider.list_open_reviews(cwd=cwd)
            all_reviews.extend(gitlab_reviews)
            logger.info(f"Discovered {len(gitlab_reviews)} open GitLab MRs")
        except Exception as e:
            logger.error(f"Failed to discover GitLab MRs: {e}")

    return all_reviews


def sync_branch_if_needed(
    code_review: CodeReview,
    main_branch: str,
    cwd: str,
    logger: logging.Logger,
) -> Dict[str, Any]:
    """Sync a branch with latest main if it's behind.

    Args:
        code_review: CodeReview object containing branch info
        main_branch: Name of the main branch
        cwd: Working directory for git operations
        logger: Logger instance

    Returns:
        Dictionary with sync result information
    """
    branch_name = code_review.branch_name
    result = {
        "branch": branch_name,
        "synced": False,
        "commits_behind": 0,
        "error": None,
    }

    try:
        # Check how far behind main
        commits_behind, error = get_commits_behind_main(branch_name, main_branch, cwd)
        if error:
            result["error"] = f"Failed to check commits behind: {error}"
            return result

        result["commits_behind"] = commits_behind

        if commits_behind == 0:
            logger.info(f"Branch {branch_name} is up to date with {main_branch}")
            result["synced"] = True
            return result

        # Sync the branch
        logger.info(f"Syncing {branch_name} with {main_branch} ({commits_behind} commits behind)")
        success, sync_error = sync_branch_with_main(branch_name, "merge", main_branch, cwd)

        if not success:
            result["error"] = sync_error
            logger.warning(f"Failed to sync {branch_name}: {sync_error}")
        else:
            result["synced"] = True
            logger.info(f"Successfully synced {branch_name} with {main_branch}")

    except Exception as e:
        result["error"] = str(e)
        logger.error(f"Exception while syncing {branch_name}: {e}")

    return result


def extract_adw_info_from_branch(branch_name: str) -> tuple[Optional[str], Optional[str]]:
    """Extract ADW ID and issue number from branch name.

    Branch naming convention: {type}-issue-{num}-adw-{id}-{description}
    Example: feature-issue-29-adw-1318773a-enhance-review-parallel-workflow

    Args:
        branch_name: Git branch name

    Returns:
        Tuple of (issue_number, adw_id) or (None, None) if not found
    """
    import re

    # Pattern: *-issue-{num}-adw-{id}-*
    match = re.search(r'-issue-(\d+)-adw-([a-f0-9]+)-', branch_name)
    if match:
        return match.group(1), match.group(2)

    # Alternative pattern: issue-{num} anywhere and adw-{id} anywhere
    issue_match = re.search(r'issue-(\d+)', branch_name)
    adw_match = re.search(r'adw-([a-f0-9]+)', branch_name)

    if issue_match and adw_match:
        return issue_match.group(1), adw_match.group(2)

    return None, None


def check_adw_state_exists(adw_id: str, cwd: str = ".") -> tuple[bool, Optional[str]]:
    """Check if ADW state file exists for the given ADW ID.

    Looks in multiple locations:
    1. Relative to cwd (for worktree execution)
    2. In the main repository (for cross-worktree access)

    Args:
        adw_id: The ADW workflow ID
        cwd: Working directory for the search

    Returns:
        Tuple of (exists: bool, path: Optional[str])
    """
    # Try relative to cwd first
    state_path = Path(cwd) / "agents" / adw_id / "adw_state.json"
    if state_path.exists():
        return True, str(state_path)

    # Try to find the main repository by looking for .git in parent directories
    current = Path(cwd).resolve()
    while current != current.parent:
        git_dir = current / ".git"
        if git_dir.exists():
            # Check if this is a worktree (has a file .git instead of directory)
            if git_dir.is_file():
                # This is a worktree - read the gitdir path to find main repo
                try:
                    gitdir_content = git_dir.read_text().strip()
                    if gitdir_content.startswith("gitdir:"):
                        gitdir_path = gitdir_content[7:].strip()
                        # gitdir points to .git/worktrees/{name}, go up to main repo
                        main_repo = Path(gitdir_path).parent.parent.parent
                        main_state_path = main_repo / "agents" / adw_id / "adw_state.json"
                        if main_state_path.exists():
                            return True, str(main_state_path)
                except Exception:
                    pass
            else:
                # Regular .git directory - check agents here
                main_state_path = current / "agents" / adw_id / "adw_state.json"
                if main_state_path.exists():
                    return True, str(main_state_path)
            break
        current = current.parent

    return False, None


def review_single_branch(
    code_review: CodeReview,
    orchestrator_adw_id: str,
    skip_resolution: bool,
    cwd: str,
    logger: logging.Logger,
) -> Dict[str, Any]:
    """Review a single branch in isolation.

    This wraps the existing adw_review_iso.py workflow.

    Args:
        code_review: CodeReview object to review
        orchestrator_adw_id: ADW ID for this orchestration run
        skip_resolution: Whether to skip blocker resolution
        cwd: Working directory
        logger: Logger instance

    Returns:
        Dictionary with review result information
    """
    branch_name = code_review.branch_name
    result = {
        "branch": branch_name,
        "pr_url": code_review.url,
        "success": False,
        "blocker_count": 0,
        "screenshot_count": 0,
        "error": None,
        "review_file": None,
    }

    try:
        logger.info(f"Starting review for branch: {branch_name}")

        # Extract ADW ID and issue number from branch name
        issue_number, branch_adw_id = extract_adw_info_from_branch(branch_name)

        if not issue_number or not branch_adw_id:
            result["error"] = f"Could not extract issue number and ADW ID from branch name: {branch_name}"
            logger.warning(result["error"])
            return result

        # Check if ADW state exists for this branch
        state_exists, state_path = check_adw_state_exists(branch_adw_id, cwd)
        if not state_exists:
            result["error"] = f"No ADW state found for ID '{branch_adw_id}'. Branch may not have been created via ADW pipeline."
            logger.warning(result["error"])
            return result

        logger.info(f"Found ADW state for branch: issue={issue_number}, adw_id={branch_adw_id}, state_path={state_path}")

        # Ensure state is accessible from the working directory
        # adw_review_iso.py expects state at agents/{adw_id}/adw_state.json relative to cwd
        local_state_dir = Path(cwd) / "agents" / branch_adw_id
        local_state_path = local_state_dir / "adw_state.json"

        if not local_state_path.exists():
            try:
                # Create the directory structure and symlink the state file
                local_state_dir.mkdir(parents=True, exist_ok=True)
                # Use symlink so changes propagate back to main repo
                local_state_path.symlink_to(state_path)
                logger.info(f"Created symlink for state: {local_state_path} -> {state_path}")
            except Exception as e:
                result["error"] = f"Failed to create state symlink: {e}"
                logger.error(result["error"])
                return result

        # Build command to run adw_review_iso.py with correct positional arguments
        # Usage: adw_review_iso.py <issue-number> <adw-id> [--skip-resolution]
        cmd = [
            "uv", "run",
            str(Path(__file__).parent / "adw_review_iso.py"),
            issue_number,  # Positional arg 1: issue number
            branch_adw_id,  # Positional arg 2: ADW ID
        ]

        if skip_resolution:
            cmd.append("--skip-resolution")

        # Execute review
        review_result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=1800,  # 30 minute timeout
        )

        if review_result.returncode == 0:
            result["success"] = True
            logger.info(f"Review completed successfully for {branch_name}")

            # Try to parse review output for statistics
            try:
                output_lines = review_result.stdout.split("\n")
                for line in output_lines:
                    if "blocker" in line.lower():
                        # Try to extract blocker count
                        import re
                        match = re.search(r'(\d+)\s+blocker', line, re.IGNORECASE)
                        if match:
                            result["blocker_count"] = int(match.group(1))
                    if "screenshot" in line.lower():
                        match = re.search(r'(\d+)\s+screenshot', line, re.IGNORECASE)
                        if match:
                            result["screenshot_count"] = int(match.group(1))
            except:
                pass  # Best effort parsing

        else:
            result["error"] = review_result.stderr or "Review process failed"
            logger.error(f"Review failed for {branch_name}: {result['error']}")

    except subprocess.TimeoutExpired:
        result["error"] = "Review timed out after 30 minutes"
        logger.error(f"Review timed out for {branch_name}")
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"Exception while reviewing {branch_name}: {e}")

    return result


def run_parallel_reviews(
    reviews: List[CodeReview],
    max_concurrent: int,
    adw_id: str,
    skip_sync: bool,
    skip_resolution: bool,
    main_branch: str,
    cwd: str,
    logger: logging.Logger,
) -> Dict[str, Any]:
    """Execute reviews in parallel with controlled concurrency.

    Args:
        reviews: List of CodeReview objects to process
        max_concurrent: Maximum number of concurrent reviews
        adw_id: ADW ID for this orchestration
        skip_sync: Whether to skip branch syncing
        skip_resolution: Whether to skip blocker resolution
        main_branch: Name of the main branch
        cwd: Working directory
        logger: Logger instance

    Returns:
        Dictionary with consolidated results
    """
    results = {
        "total": len(reviews),
        "successful": 0,
        "failed": 0,
        "synced": 0,
        "sync_failed": 0,
        "reviews": [],
        "started_at": datetime.now().isoformat(),
    }

    # Phase 1: Sync branches if requested
    if not skip_sync:
        logger.info(f"Syncing {len(reviews)} branches with {main_branch}...")
        sync_futures = []
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            for review in reviews:
                future = executor.submit(
                    sync_branch_if_needed,
                    review,
                    main_branch,
                    cwd,
                    logger,
                )
                sync_futures.append((review, future))

            # Collect sync results
            for review, future in sync_futures:
                try:
                    sync_result = future.result()
                    if sync_result["synced"]:
                        results["synced"] += 1
                    if sync_result["error"]:
                        results["sync_failed"] += 1
                        logger.warning(f"Sync failed for {review.branch_name}: {sync_result['error']}")
                except Exception as e:
                    results["sync_failed"] += 1
                    logger.error(f"Exception during sync for {review.branch_name}: {e}")

        logger.info(f"Sync complete: {results['synced']} synced, {results['sync_failed']} failed")

    # Phase 2: Run reviews in parallel
    logger.info(f"Starting {len(reviews)} reviews with max concurrency {max_concurrent}...")
    review_futures = []
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        for review in reviews:
            future = executor.submit(
                review_single_branch,
                review,
                adw_id,
                skip_resolution,
                cwd,
                logger,
            )
            review_futures.append((review, future))

        # Collect review results
        for review, future in review_futures:
            try:
                review_result = future.result()
                results["reviews"].append(review_result)
                if review_result["success"]:
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                logger.info(
                    f"Review completed: {review.branch_name} - "
                    f"{'SUCCESS' if review_result['success'] else 'FAILED'}"
                )
            except Exception as e:
                results["failed"] += 1
                results["reviews"].append({
                    "branch": review.branch_name,
                    "success": False,
                    "error": str(e),
                })
                logger.error(f"Exception during review for {review.branch_name}: {e}")

    results["completed_at"] = datetime.now().isoformat()
    return results


def save_consolidated_report(
    results: Dict[str, Any],
    adw_id: str,
    logger: logging.Logger,
) -> str:
    """Save consolidated report to disk.

    Args:
        results: Dictionary with consolidated results
        adw_id: ADW ID for this orchestration
        logger: Logger instance

    Returns:
        Path to the saved report
    """
    # Create agents directory if it doesn't exist
    agents_dir = Path("agents") / adw_id
    agents_dir.mkdir(parents=True, exist_ok=True)

    report_path = agents_dir / "consolidated_review_report.json"

    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Consolidated report saved to: {report_path}")
    return str(report_path)


def print_summary(results: Dict[str, Any], logger: logging.Logger):
    """Print a human-readable summary of results.

    Args:
        results: Dictionary with consolidated results
        logger: Logger instance
    """
    print("\n" + "=" * 80)
    print("PARALLEL REVIEW ORCHESTRATION SUMMARY")
    print("=" * 80)
    print(f"Total Reviews: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")

    if "synced" in results:
        print(f"Branches Synced: {results['synced']}")
        print(f"Sync Failures: {results['sync_failed']}")

    print("\nPer-Branch Results:")
    print("-" * 80)

    for review in results["reviews"]:
        status = "✅ SUCCESS" if review["success"] else "❌ FAILED"
        print(f"{status} | {review['branch']}")
        if review.get("pr_url"):
            print(f"         PR: {review['pr_url']}")
        if review.get("blocker_count", 0) > 0:
            print(f"         Blockers: {review['blocker_count']}")
        if review.get("error"):
            print(f"         Error: {review['error']}")
        print()

    print("=" * 80)


def main():
    """Main orchestrator entry point."""
    args = parse_args()

    # Generate ADW ID if not provided
    adw_id = args.adw_id or generate_adw_id()

    # Setup logging
    logger = setup_logger(f"adw_review_all_{adw_id}", level=logging.INFO)
    logger.info(f"Starting Parallel Review Orchestrator (ADW ID: {adw_id})")
    logger.info(f"Platform: {args.platform}, Max Concurrent: {args.max_concurrent}")

    # Discover open reviews
    logger.info("Discovering open PRs/MRs...")
    reviews = discover_open_reviews(args.platform, args.cwd, logger)

    if not reviews:
        logger.warning("No open PRs/MRs found. Exiting.")
        print("No open PRs/MRs to review.")
        return 0

    logger.info(f"Found {len(reviews)} open reviews")

    # Print what will be reviewed
    print(f"\nFound {len(reviews)} open reviews:")
    for review in reviews:
        print(f"  - {review.branch_name} ({review.platform.value}): {review.title}")

    if args.dry_run:
        print("\nDry run mode - exiting without running reviews")
        return 0

    # Run parallel reviews
    results = run_parallel_reviews(
        reviews=reviews,
        max_concurrent=args.max_concurrent,
        adw_id=adw_id,
        skip_sync=args.skip_sync,
        skip_resolution=args.skip_resolution,
        main_branch=args.main_branch,
        cwd=args.cwd,
        logger=logger,
    )

    # Save consolidated report
    report_path = save_consolidated_report(results, adw_id, logger)

    # Print summary
    print_summary(results, logger)

    # Return non-zero exit code if any reviews failed
    if results["failed"] > 0:
        logger.warning(f"{results['failed']} reviews failed")
        return 1

    logger.info("All reviews completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
