"""Git operations for Jerry ADW composable architecture.

Provides centralized git operations that build on top of github.py module.
"""

import subprocess
import json
import logging
from typing import Optional, Tuple, Literal

# Import GitHub functions from existing module
from .github import get_repo_url, extract_repo_path
from .issue_providers import get_provider_for_issue


def is_gitlab_remote(url: str) -> bool:
    """Check if a git remote URL is for GitLab.

    Args:
        url: Git remote URL (e.g., https://gitlab.com/foo/bar or git@gitlab.com:foo/bar)

    Returns:
        True if the URL is a GitLab remote, False otherwise
    """
    if not url:
        return False

    # Check for gitlab.com or common self-hosted GitLab patterns
    gitlab_indicators = [
        "gitlab.com",
        "gitlab.",  # Matches custom GitLab instances like gitlab.example.com
    ]

    url_lower = url.lower()
    return any(indicator in url_lower for indicator in gitlab_indicators)


def detect_git_platform(cwd: Optional[str] = None) -> Literal["github", "gitlab", "unknown"]:
    """Detect the git hosting platform from the remote URL.

    Args:
        cwd: Optional working directory

    Returns:
        "github" if GitHub remote detected
        "gitlab" if GitLab remote detected
        "unknown" if unable to determine
    """
    try:
        remote_url = get_repo_url(cwd=cwd)

        if "github.com" in remote_url.lower():
            return "github"
        elif is_gitlab_remote(remote_url):
            return "gitlab"
        else:
            return "unknown"
    except Exception:
        return "unknown"


def get_current_branch(cwd: Optional[str] = None) -> str:
    """Get current git branch name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.stdout.strip()


def push_branch(
    branch_name: str, cwd: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Push current branch to remote. Returns (success, error_message)."""
    result = subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, None


def check_pr_exists(branch_name: str, cwd: Optional[str] = None) -> Optional[str]:
    """Check if PR exists for branch. Returns PR URL if exists."""
    try:
        repo_url = get_repo_url(cwd=cwd)
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return None

    result = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo_path,
            "--head",
            branch_name,
            "--json",
            "url",
        ],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode == 0:
        prs = json.loads(result.stdout)
        if prs:
            return prs[0]["url"]
    return None


def create_branch(
    branch_name: str, cwd: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Create and checkout a new branch. Returns (success, error_message)."""
    # Create branch
    result = subprocess.run(
        ["git", "checkout", "-b", branch_name], capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        # Check if error is because branch already exists
        if "already exists" in result.stderr:
            # Try to checkout existing branch
            result = subprocess.run(
                ["git", "checkout", branch_name],
                capture_output=True,
                text=True,
                cwd=cwd,
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, None
        return False, result.stderr
    return True, None


def commit_changes(
    message: str, cwd: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Stage all changes and commit. Returns (success, error_message)."""
    # Check if there are changes to commit
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, cwd=cwd
    )
    if not result.stdout.strip():
        return True, None  # No changes to commit

    # Stage all changes
    result = subprocess.run(
        ["git", "add", "-A"], capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        return False, result.stderr

    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", message], capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, None


def get_pr_number(branch_name: str, cwd: Optional[str] = None) -> Optional[str]:
    """Get PR number for a branch. Returns PR number if exists."""
    try:
        repo_url = get_repo_url(cwd=cwd)
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return None

    result = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo_path,
            "--head",
            branch_name,
            "--json",
            "number",
            "--limit",
            "1",
        ],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode == 0:
        prs = json.loads(result.stdout)
        if prs:
            return str(prs[0]["number"])
    return None


def approve_pr(pr_number: str, logger: logging.Logger, cwd: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Approve a PR. Returns (success, error_message)."""
    try:
        repo_url = get_repo_url(cwd=cwd)
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return False, f"Failed to get repo info: {e}"

    result = subprocess.run(
        [
            "gh",
            "pr",
            "review",
            pr_number,
            "--repo",
            repo_path,
            "--approve",
            "--body",
            "ADW workflow approved this PR after validation.",
        ],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return False, result.stderr

    logger.info(f"Approved PR #{pr_number}")
    return True, None


def merge_pr(
    pr_number: str, logger: logging.Logger, merge_method: str = "squash", cwd: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Merge a PR. Returns (success, error_message).

    Args:
        pr_number: The PR number to merge
        logger: Logger instance
        merge_method: One of 'merge', 'squash', 'rebase' (default: 'squash')
        cwd: Working directory
    """
    try:
        repo_url = get_repo_url(cwd=cwd)
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return False, f"Failed to get repo info: {e}"

    # First check if PR is mergeable
    result = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            pr_number,
            "--repo",
            repo_path,
            "--json",
            "mergeable,mergeStateStatus",
        ],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return False, f"Failed to check PR status: {result.stderr}"

    pr_status = json.loads(result.stdout)
    if pr_status.get("mergeable") != "MERGEABLE":
        return (
            False,
            f"PR is not mergeable. Status: {pr_status.get('mergeStateStatus', 'unknown')}",
        )

    # Merge the PR
    merge_cmd = [
        "gh",
        "pr",
        "merge",
        pr_number,
        "--repo",
        repo_path,
        f"--{merge_method}",
        "--body",
        "Merged by ADW workflow after successful validation.",
    ]

    result = subprocess.run(merge_cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        return False, result.stderr

    logger.info(f"Merged PR #{pr_number} using {merge_method} method")
    return True, None


def get_diff_files(base_branch: str = "origin/main", cwd: Optional[str] = None) -> list:
    """Get list of files changed from base branch."""
    result = subprocess.run(
        ["git", "diff", base_branch, "--name-only"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode == 0:
        return result.stdout.strip().split("\n")
    return []


def get_commit_hash(cwd: Optional[str] = None) -> str:
    """Get current commit hash (short)."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.stdout.strip()


def fetch_latest_main(main_branch: str = "main", cwd: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Fetch latest changes from origin/main.

    Args:
        main_branch: Name of the main branch (default: "main")
        cwd: Working directory for git operations

    Returns:
        Tuple of (success, error_message)
    """
    result = subprocess.run(
        ["git", "fetch", "origin", main_branch],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, None


def get_commits_behind_main(
    branch_name: str, main_branch: str = "main", cwd: Optional[str] = None
) -> Tuple[int, Optional[str]]:
    """Get number of commits the branch is behind main.

    Args:
        branch_name: The feature branch name
        main_branch: Name of the main branch (default: "main")
        cwd: Working directory for git operations

    Returns:
        Tuple of (commits_behind, error_message)
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{branch_name}..origin/{main_branch}"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return 0, result.stderr

    try:
        count = int(result.stdout.strip())
        return count, None
    except ValueError:
        return 0, "Failed to parse commit count"


def check_merge_conflicts(cwd: Optional[str] = None) -> Tuple[bool, list[str]]:
    """Check if there are merge conflicts in the working directory.

    Args:
        cwd: Working directory for git operations

    Returns:
        Tuple of (has_conflicts, list_of_conflicted_files)
    """
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return False, []

    conflicted_files = [f for f in result.stdout.strip().split("\n") if f]
    return len(conflicted_files) > 0, conflicted_files


def sync_branch_with_main(
    branch_name: str,
    strategy: Literal["merge", "rebase"] = "merge",
    main_branch: str = "main",
    cwd: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """Sync a branch with latest main changes using merge or rebase.

    Args:
        branch_name: The feature branch name
        strategy: Sync strategy - "merge" or "rebase" (default: "merge")
        main_branch: Name of the main branch (default: "main")
        cwd: Working directory for git operations

    Returns:
        Tuple of (success, error_message)
    """
    # First, fetch latest main
    fetch_success, fetch_error = fetch_latest_main(main_branch, cwd=cwd)
    if not fetch_success:
        return False, f"Failed to fetch latest main: {fetch_error}"

    # Check how many commits behind
    commits_behind, count_error = get_commits_behind_main(branch_name, main_branch, cwd=cwd)
    if count_error:
        return False, f"Failed to check commits behind: {count_error}"

    if commits_behind == 0:
        return True, None  # Already up to date

    # Ensure we're on the correct branch
    result = subprocess.run(
        ["git", "checkout", branch_name],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return False, f"Failed to checkout branch: {result.stderr}"

    # Perform sync based on strategy
    if strategy == "rebase":
        result = subprocess.run(
            ["git", "rebase", f"origin/{main_branch}"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
    else:  # merge
        result = subprocess.run(
            ["git", "merge", f"origin/{main_branch}", "--no-edit"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

    if result.returncode != 0:
        # Check for conflicts
        has_conflicts, conflicted_files = check_merge_conflicts(cwd=cwd)
        if has_conflicts:
            # Abort the merge/rebase
            if strategy == "rebase":
                subprocess.run(["git", "rebase", "--abort"], cwd=cwd)
            else:
                subprocess.run(["git", "merge", "--abort"], cwd=cwd)
            return False, f"Merge conflicts detected in: {', '.join(conflicted_files)}"
        return False, result.stderr

    return True, None


def finalize_git_operations(
    state, logger: logging.Logger, cwd: Optional[str] = None
) -> None:
    """Standard git finalization: push branch and create/update PR.

    Args:
        state: ADWState object containing workflow state
        logger: Logger instance
        cwd: Optional working directory for git operations
    """
    branch_name = state.get("branch_name")
    if not branch_name:
        # Fallback: use current git branch if not main
        current_branch = get_current_branch(cwd=cwd)
        if current_branch and current_branch != "main":
            logger.warning(
                f"No branch name in state, using current branch: {current_branch}"
            )
            branch_name = current_branch
        else:
            logger.error(
                "No branch name in state and current branch is main, skipping git operations"
            )
            return

    # Always push
    success, error = push_branch(branch_name, cwd=cwd)
    if not success:
        logger.error(f"Failed to push branch: {error}")
        return

    logger.info(f"Pushed branch: {branch_name}")

    # Handle PR
    pr_url = check_pr_exists(branch_name, cwd=cwd)
    issue_number = state.get("issue_number")
    adw_id = state.get("adw_id")
    issue = state.get("issue")

    # Get provider for posting comments
    provider = None
    if issue:
        provider = get_provider_for_issue(issue)

    if pr_url:
        logger.info(f"Found existing PR: {pr_url}")
        # Post PR link for easy reference
        if issue and adw_id and provider:
            provider.add_comment(issue, f"{adw_id}_ops: ✅ Pull request: {pr_url}", adw_id)
    else:
        # Create new PR - fetch issue data first
        if issue_number:
            try:
                repo_url = get_repo_url(cwd=cwd)
                repo_path = extract_repo_path(repo_url)
                from .github import fetch_issue
                from .workflow_ops import create_pull_request

                issue = fetch_issue(issue_number, repo_path)
                pr_url, error = create_pull_request(branch_name, issue, state, logger, cwd)

                if pr_url:
                    logger.info(f"Created PR: {pr_url}")
                    # Post new PR link
                    if issue and adw_id and provider:
                        provider.add_comment(issue, f"{adw_id}_ops: ✅ Pull request: {pr_url}", adw_id)
                else:
                    logger.error(f"Failed to create PR: {error}")
                    if issue and adw_id and provider:
                        provider.add_comment(issue, f"{adw_id}_ops: ❌ Failed to create PR: {error}", adw_id)
            except Exception as e:
                logger.error(f"Failed to fetch issue for PR creation: {e}")
        else:
            logger.warning("No issue number in state, cannot create PR")
