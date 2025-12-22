"""
GitLab Operations Module - Jerry ADW

This module contains all GitLab-related operations including:
- Issue fetching and manipulation
- Comment posting
- Project path extraction
- Issue status management
"""

import subprocess
import sys
import os
import json
from typing import Dict, List, Optional
from .data_types import Issue, IssueSource, IssueStatus

# Bot identifier to prevent webhook loops and filter bot comments
ADW_BOT_IDENTIFIER = "[ADW-AGENTS]"


def get_gitlab_env() -> Optional[dict]:
    """Get environment with GitLab token set up. Returns None if no GITLAB_TOKEN.

    Subprocess env behavior:
    - env=None → Inherits parent's environment (default)
    - env={} → Empty environment (no variables)
    - env=custom_dict → Only uses specified variables

    Returns None to use default glab authentication if no GITLAB_TOKEN is set.
    """
    gitlab_token = os.getenv("GITLAB_TOKEN")
    if not gitlab_token:
        return None

    # Create env with GitLab token and essential system variables
    # HOME is required for glab to find its config in ~/Library/Application Support/glab-cli
    env = {
        "GITLAB_TOKEN": gitlab_token,
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "USER": os.environ.get("USER", ""),
    }
    return env


def get_repo_url(cwd: Optional[str] = None) -> str:
    """Get GitLab repository URL from git remote."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise ValueError(
            "No git remote 'origin' found. Please ensure you're in a git repository with a remote."
        )
    except FileNotFoundError:
        raise ValueError("git command not found. Please ensure git is installed.")


def extract_project_path(gitlab_url: str) -> str:
    """Extract namespace/project from GitLab URL.

    Examples:
        https://gitlab.com/namespace/project -> namespace/project
        https://gitlab.com/namespace/project.git -> namespace/project
        git@gitlab.com:namespace/project.git -> namespace/project
        https://custom-gitlab.com/namespace/project -> namespace/project
    """
    # Handle SSH format
    if ":" in gitlab_url and "@" in gitlab_url:
        # git@gitlab.com:namespace/project.git -> namespace/project.git
        path = gitlab_url.split(":", 1)[1]
    else:
        # Handle HTTPS format - extract path after domain
        # https://gitlab.com/namespace/project -> namespace/project
        parts = gitlab_url.split("/")
        # Find index after domain (skip protocol and domain)
        if "//" in gitlab_url:
            path = "/".join(parts[3:])  # Skip https:, empty, domain
        else:
            path = "/".join(parts[1:])  # Skip domain

    # Remove .git suffix if present
    path = path.replace(".git", "")

    return path


def fetch_issue(issue_number: str, project_path: str) -> Issue:
    """Fetch GitLab issue using glab CLI and return generic Issue model.

    Args:
        issue_number: Issue number (e.g., "123")
        project_path: GitLab project path (e.g., "namespace/project")

    Returns:
        Generic Issue model populated from GitLab issue data
    """
    cmd = [
        "glab",
        "issue",
        "view",
        issue_number,
        "-R",
        project_path,
        "--output",
        "json",
    ]

    env = get_gitlab_env()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        if result.returncode == 0:
            issue_data = json.loads(result.stdout)

            # Convert GitLab issue to generic Issue model
            # GitLab JSON structure: {id, iid, title, description, state, author, assignees, labels, created_at, updated_at, web_url}
            issue = Issue(
                id=str(issue_data.get("iid", issue_data.get("id"))),  # Use iid (issue number) not internal id
                title=issue_data.get("title", ""),
                body=issue_data.get("description", ""),  # GitLab uses "description", Issue model uses "body"
                source=IssueSource.GITLAB,
                status=IssueStatus.OPEN if issue_data.get("state") == "opened" else IssueStatus.CLOSED,
                source_url=issue_data.get("web_url", ""),
                labels=issue_data.get("labels", []),
                repo_path=project_path,  # Store project path for later use
            )
            return issue
        else:
            print(result.stderr, file=sys.stderr)
            raise RuntimeError(f"Failed to fetch GitLab issue: {result.stderr}")
    except FileNotFoundError:
        print("Error: GitLab CLI (glab) is not installed.", file=sys.stderr)
        print("\nTo install glab:", file=sys.stderr)
        print("  - macOS: brew install glab", file=sys.stderr)
        print("  - Linux: See https://gitlab.com/gitlab-org/cli", file=sys.stderr)
        print("\nAfter installation, authenticate with: glab auth login", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Error parsing GitLab issue data: {e}", file=sys.stderr)
        raise


def make_issue_comment(
    issue_id: str, comment: str, project_path: Optional[str] = None, cwd: Optional[str] = None
) -> None:
    """Post a comment to a GitLab issue using glab CLI.

    Args:
        issue_id: The issue number/ID
        comment: The comment text to post
        project_path: GitLab project path (namespace/project). If None, detected from git remote.
        cwd: Working directory for git operations
    """
    if not project_path:
        gitlab_repo_url = get_repo_url(cwd=cwd)
        project_path = extract_project_path(gitlab_repo_url)

    # Ensure comment has ADW_BOT_IDENTIFIER to prevent webhook loops
    if not comment.startswith(ADW_BOT_IDENTIFIER):
        comment = f"{ADW_BOT_IDENTIFIER} {comment}"

    cmd = [
        "glab",
        "issue",
        "note",
        issue_id,
        "-R",
        project_path,
        "--message",
        comment,
    ]

    env = get_gitlab_env()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        if result.returncode == 0:
            print(f"Successfully posted comment to GitLab issue #{issue_id}")
        else:
            print(f"Error posting comment to GitLab: {result.stderr}", file=sys.stderr)
            raise RuntimeError(f"Failed to post comment to GitLab: {result.stderr}")
    except Exception as e:
        print(f"Error posting comment to GitLab: {e}", file=sys.stderr)
        raise


def mark_issue_in_progress(
    issue_id: str, project_path: Optional[str] = None, cwd: Optional[str] = None
) -> None:
    """Mark GitLab issue as in progress by adding label and assigning.

    Args:
        issue_id: The issue number/ID
        project_path: GitLab project path (namespace/project). If None, detected from git remote.
        cwd: Working directory for git operations
    """
    if not project_path:
        gitlab_repo_url = get_repo_url(cwd=cwd)
        project_path = extract_project_path(gitlab_repo_url)

    env = get_gitlab_env()

    # Add "in_progress" label
    cmd = [
        "glab",
        "issue",
        "update",
        issue_id,
        "-R",
        project_path,
        "--add-label",
        "in_progress",
    ]

    # Try to add label (may fail if label doesn't exist)
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Note: Could not add 'in_progress' label to GitLab issue: {result.stderr}")

    # Assign to self (optional)
    # Note: glab uses --assignee @me syntax
    cmd = [
        "glab",
        "issue",
        "update",
        issue_id,
        "-R",
        project_path,
        "--assignee",
        "@me",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode == 0:
        print(f"Assigned GitLab issue #{issue_id} to self")


def fetch_open_issues(project_path: str) -> List[Dict]:
    """Fetch all open issues from the GitLab project."""
    try:
        cmd = [
            "glab",
            "issue",
            "list",
            "--repo",
            project_path,
            "--state",
            "opened",
            "--output",
            "json",
            "--per-page",
            "100",
        ]

        env = get_gitlab_env()

        result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)

        issues_data = json.loads(result.stdout)
        print(f"Fetched {len(issues_data)} open GitLab issues")
        return issues_data

    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to fetch GitLab issues: {e.stderr}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse GitLab issues JSON: {e}", file=sys.stderr)
        return []


def fetch_issue_comments(project_path: str, issue_number: int) -> List[Dict]:
    """Fetch all comments for a specific GitLab issue."""
    try:
        # glab doesn't have a direct command to fetch only notes, so fetch the full issue
        cmd = [
            "glab",
            "issue",
            "view",
            str(issue_number),
            "--repo",
            project_path,
            "--output",
            "json",
        ]

        env = get_gitlab_env()

        result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
        data = json.loads(result.stdout)

        # GitLab issue notes are in the "notes" field
        comments = data.get("notes", [])

        # Sort comments by creation time
        comments.sort(key=lambda c: c.get("created_at", ""))

        return comments

    except subprocess.CalledProcessError as e:
        print(
            f"ERROR: Failed to fetch comments for GitLab issue #{issue_number}: {e.stderr}",
            file=sys.stderr,
        )
        return []
    except json.JSONDecodeError as e:
        print(
            f"ERROR: Failed to parse comments JSON for GitLab issue #{issue_number}: {e}",
            file=sys.stderr,
        )
        return []


def find_keyword_from_comment(keyword: str, issue_comments: List[Dict]) -> Optional[Dict]:
    """Find the latest comment containing a specific keyword.

    Args:
        keyword: The keyword to search for in comments
        issue_comments: List of GitLab issue comments/notes

    Returns:
        The latest comment dict containing the keyword, or None if not found
    """
    # Sort comments by created_at date (newest first)
    sorted_comments = sorted(
        issue_comments,
        key=lambda c: c.get("created_at", ""),
        reverse=True
    )

    # Search through sorted comments (newest first)
    for comment in sorted_comments:
        # Skip ADW bot comments to prevent loops
        body = comment.get("body", "")
        if ADW_BOT_IDENTIFIER in body:
            continue

        if keyword in body:
            return comment

    return None
