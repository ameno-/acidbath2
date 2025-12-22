"""Issue providers for different sources (GitHub, Linear, Local, Prompt).

This module provides a unified interface for working with issues from
multiple sources. Each provider implements the same interface, allowing
ADW workflows to work with issues regardless of their origin.

Usage:
    from adws.adw_modules.issue_providers import resolve_issue

    # Resolve any issue reference
    issue = resolve_issue("123")  # GitHub issue
    issue = resolve_issue("local:fix-validation")  # Local issue
    issue = resolve_issue("prompt:Fix the bug")  # Ephemeral prompt issue
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Protocol, runtime_checkable

import yaml

from .data_types import Issue, IssueSource, IssueStatus, GitHubIssue


def get_project_root() -> str:
    """Get the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def make_issue_id() -> str:
    """Generate a unique issue ID (8 hex characters)."""
    import uuid

    return uuid.uuid4().hex[:8]


@runtime_checkable
class IssueProvider(Protocol):
    """Protocol for issue providers."""

    def fetch_issue(self, issue_ref: str) -> Issue:
        """Fetch an issue by reference."""
        ...

    def update_status(
        self, issue: Issue, status: IssueStatus, message: str, agent_id: Optional[str] = None
    ) -> None:
        """Update issue status."""
        ...

    def add_comment(self, issue: Issue, comment: str, agent_id: Optional[str] = None) -> None:
        """Add a comment to the issue."""
        ...


class GitHubIssueProvider:
    """Provider for GitHub issues.

    Wraps existing github.py functions to provide a consistent interface.
    """

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize with optional repo path.

        Args:
            repo_path: GitHub repo path (owner/repo). If None, will be detected.
        """
        self.repo_path = repo_path

    def _get_repo_path(self) -> str:
        """Get the repo path, detecting if not provided."""
        if self.repo_path:
            return self.repo_path

        from .git_ops import get_repo_url, extract_repo_path

        return extract_repo_path(get_repo_url())

    def fetch_issue(self, issue_number: str) -> Issue:
        """Fetch GitHub issue and convert to generic Issue."""
        from .github import fetch_issue as github_fetch_issue

        gh_issue = github_fetch_issue(issue_number, self._get_repo_path())
        return Issue.from_github_issue(gh_issue)

    def update_status(
        self, issue: Issue, status: IssueStatus, message: str, agent_id: Optional[str] = None
    ) -> None:
        """Update via GitHub comment."""
        from .github import make_issue_comment

        status_message = f"**Status**: {status.value}\n\n{message}"
        if agent_id:
            status_message = f"[{agent_id}] {status_message}"
        make_issue_comment(issue.id, status_message)

    def add_comment(self, issue: Issue, comment: str, agent_id: Optional[str] = None) -> None:
        """Add GitHub comment."""
        from .github import make_issue_comment

        if agent_id:
            comment = f"[{agent_id}] {comment}"
        make_issue_comment(issue.id, comment)


class GitLabIssueProvider:
    """Provider for GitLab issues.

    Wraps gitlab.py functions to provide a consistent interface.
    """

    def __init__(self, project_path: Optional[str] = None):
        """Initialize with optional project path.

        Args:
            project_path: GitLab project path (namespace/project). If None, will be detected.
        """
        self.project_path = project_path

    def _get_project_path(self) -> str:
        """Get the project path, detecting if not provided."""
        if self.project_path:
            return self.project_path

        from .git_ops import get_repo_url
        from .gitlab import extract_project_path

        return extract_project_path(get_repo_url())

    def fetch_issue(self, issue_number: str) -> Issue:
        """Fetch GitLab issue and return as generic Issue."""
        from .gitlab import fetch_issue as gitlab_fetch_issue

        return gitlab_fetch_issue(issue_number, self._get_project_path())

    def update_status(
        self, issue: Issue, status: IssueStatus, message: str, agent_id: Optional[str] = None
    ) -> None:
        """Update via GitLab comment."""
        from .gitlab import make_issue_comment

        status_message = f"**Status**: {status.value}\n\n{message}"
        if agent_id:
            status_message = f"[{agent_id}] {status_message}"
        make_issue_comment(issue.id, status_message, project_path=self._get_project_path())

    def add_comment(self, issue: Issue, comment: str, agent_id: Optional[str] = None) -> None:
        """Add GitLab comment."""
        from .gitlab import make_issue_comment

        if agent_id:
            comment = f"[{agent_id}] {comment}"
        make_issue_comment(issue.id, comment, project_path=self._get_project_path())


class LocalIssueProvider:
    """Provider for local markdown issues in issues/ directory.

    Local issues are stored as markdown files with YAML frontmatter.
    Multiple agents can update the same issue, with updates tracked
    in the frontmatter.
    """

    ISSUES_DIR = "issues"

    def __init__(self, project_root: Optional[str] = None):
        """Initialize with optional project root.

        Args:
            project_root: Project root directory. If None, will be detected.
        """
        self.project_root = project_root or get_project_root()
        self.issues_dir = Path(self.project_root) / self.ISSUES_DIR

    def _ensure_dir(self) -> None:
        """Ensure issues directory exists."""
        self.issues_dir.mkdir(exist_ok=True)

    def _parse_issue_file(self, path: Path) -> Issue:
        """Parse markdown file with YAML frontmatter."""
        content = path.read_text()

        # Split frontmatter and body
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
            else:
                frontmatter = {}
                body = content
        else:
            frontmatter = {}
            body = content

        # Extract issue ID from filename (issue-{id}.md)
        issue_id = path.stem
        if issue_id.startswith("issue-"):
            issue_id = issue_id[6:]  # Remove "issue-" prefix

        # Parse timestamps
        created_at = frontmatter.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                created_at = None

        updated_at = frontmatter.get("updated_at")
        if isinstance(updated_at, str):
            try:
                updated_at = datetime.fromisoformat(updated_at)
            except ValueError:
                updated_at = None

        # Parse status
        status_str = frontmatter.get("status", "open")
        try:
            status = IssueStatus(status_str)
        except ValueError:
            status = IssueStatus.OPEN

        return Issue(
            id=issue_id,
            title=frontmatter.get("title", f"Local Issue {issue_id}"),
            body=body,
            source=IssueSource.LOCAL,
            status=status,
            labels=frontmatter.get("labels", []),
            created_at=created_at,
            updated_at=updated_at,
            source_ref=f"local:{issue_id}",
            local_path=str(path),
            agent_updates=frontmatter.get("agent_updates", []),
        )

    def fetch_issue(self, issue_ref: str) -> Issue:
        """Fetch local issue by ID or path.

        Args:
            issue_ref: Issue ID or path to markdown file.

        Returns:
            Issue object.

        Raises:
            FileNotFoundError: If issue file doesn't exist.
        """
        self._ensure_dir()

        # Handle path reference
        if issue_ref.endswith(".md"):
            if Path(issue_ref).is_absolute():
                path = Path(issue_ref)
            else:
                path = self.issues_dir / issue_ref
        else:
            # Assume it's an ID
            path = self.issues_dir / f"issue-{issue_ref}.md"

        if not path.exists():
            raise FileNotFoundError(f"Local issue not found: {path}")

        return self._parse_issue_file(path)

    def create_issue(
        self,
        title: str,
        body: str,
        issue_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Issue:
        """Create a new local issue.

        Args:
            title: Issue title.
            body: Issue body content.
            issue_id: Optional ID. If None, generates one.
            labels: Optional list of labels.

        Returns:
            Created Issue object.
        """
        self._ensure_dir()

        # Generate ID if not provided
        if not issue_id:
            issue_id = make_issue_id()

        now = datetime.now().isoformat()

        frontmatter = {
            "title": title,
            "status": "open",
            "labels": labels or [],
            "created_at": now,
            "updated_at": now,
            "agent_updates": [],
        }

        content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)}---

{body}
"""

        path = self.issues_dir / f"issue-{issue_id}.md"
        path.write_text(content)

        return self.fetch_issue(issue_id)

    def update_status(
        self, issue: Issue, status: IssueStatus, message: str, agent_id: Optional[str] = None
    ) -> None:
        """Update local issue status with agent tracking.

        Args:
            issue: Issue to update.
            status: New status.
            message: Status message.
            agent_id: Optional agent ID for tracking.
        """
        if not issue.local_path:
            raise ValueError("Issue has no local path")

        path = Path(issue.local_path)
        content = path.read_text()

        # Parse and update frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError(f"Invalid issue format: {path}")

        frontmatter = yaml.safe_load(parts[1]) or {}
        body = parts[2].strip()

        frontmatter["status"] = status.value
        frontmatter["updated_at"] = datetime.now().isoformat()

        # Add agent update
        update = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "status": status.value,
            "message": message,
        }
        if "agent_updates" not in frontmatter:
            frontmatter["agent_updates"] = []
        frontmatter["agent_updates"].append(update)

        # Write back
        new_content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)}---

{body}
"""
        path.write_text(new_content)

    def add_comment(self, issue: Issue, comment: str, agent_id: Optional[str] = None) -> None:
        """Add comment to local issue (appends to body).

        Args:
            issue: Issue to comment on.
            comment: Comment content.
            agent_id: Optional agent ID for attribution.
        """
        if not issue.local_path:
            raise ValueError("Issue has no local path")

        path = Path(issue.local_path)
        content = path.read_text()

        timestamp = datetime.now().isoformat()
        agent_attr = f" by {agent_id}" if agent_id else ""
        comment_block = f"""

---

**Comment** ({timestamp}){agent_attr}

{comment}
"""

        path.write_text(content + comment_block)

    def list_issues(self, status: Optional[IssueStatus] = None) -> List[Issue]:
        """List all local issues, optionally filtered by status.

        Args:
            status: Optional status filter.

        Returns:
            List of Issue objects, sorted by creation date (newest first).
        """
        self._ensure_dir()

        issues = []
        for path in self.issues_dir.glob("issue-*.md"):
            try:
                issue = self._parse_issue_file(path)
                if status is None or issue.status == status:
                    issues.append(issue)
            except Exception:
                # Skip malformed issues
                continue

        return sorted(issues, key=lambda i: i.created_at or datetime.min, reverse=True)


class PromptIssueProvider:
    """Provider for prompt-based issues (passed via CLI).

    Prompt issues are ephemeral - they exist only for the duration
    of the workflow execution and have no persistence.
    """

    def create_from_prompt(self, prompt: str, title: Optional[str] = None) -> Issue:
        """Create an issue from a prompt string.

        Args:
            prompt: The prompt text (becomes issue body).
            title: Optional title. If None, derived from prompt.

        Returns:
            Issue object.
        """
        issue_id = f"prompt-{make_issue_id()}"

        # Generate title from prompt if not provided
        if not title:
            # Use first line or first 50 chars
            first_line = prompt.split("\n")[0].strip()
            if len(first_line) > 50:
                title = first_line[:47] + "..."
            else:
                title = first_line

        return Issue(
            id=issue_id,
            title=title,
            body=prompt,
            source=IssueSource.PROMPT,
            status=IssueStatus.OPEN,
            created_at=datetime.now(),
            source_ref=f"prompt:{issue_id}",
        )

    def update_status(
        self, issue: Issue, status: IssueStatus, message: str, agent_id: Optional[str] = None
    ) -> None:
        """Prompts are ephemeral - status updates are no-ops."""
        pass

    def add_comment(self, issue: Issue, comment: str, agent_id: Optional[str] = None) -> None:
        """Prompts are ephemeral - comments are no-ops."""
        pass


def resolve_issue(
    issue_ref: str,
    repo_path: Optional[str] = None,
    project_root: Optional[str] = None,
) -> Issue:
    """Resolve an issue reference to an Issue object.

    This is the main entry point for the issue abstraction layer.
    It detects the issue source from the reference format and
    delegates to the appropriate provider.

    Supports:
    - GitHub: "123", "github:123"
    - GitLab: "gitlab:123" (simple), "gitlab:PROJECT_PATH:123" (extended)
    - Local: "local:abc123", "issues/issue-abc.md"
    - Prompt: "prompt:Some task description"
    - Direct text: Any text not matching above patterns (treated as prompt)

    GitLab Extended Format:
    The extended format allows referencing GitLab issues from any project,
    regardless of the current repository's hosting platform:
    - "gitlab:ameno13/jerry:1" - Issue #1 from ameno13/jerry project
    - "gitlab:namespace/project:456" - Issue #456 from namespace/project

    This is required when:
    - Working in a GitHub repo but referencing a GitLab issue
    - Referencing issues from a different GitLab project than the current repo
    - Current repository has no git remote or remote is not GitLab

    Args:
        issue_ref: Issue reference string.
        repo_path: GitHub repo path (owner/repo) or GitLab project path (namespace/project).
        project_root: Project root for local issues.

    Returns:
        Issue object.

    Examples:
        >>> issue = resolve_issue("123")  # GitHub issue #123 (auto-detected)
        >>> issue = resolve_issue("github:456")  # Explicit GitHub
        >>> issue = resolve_issue("gitlab:789")  # GitLab (requires GitLab remote)
        >>> issue = resolve_issue("gitlab:ameno13/jerry:1")  # GitLab extended format
        >>> issue = resolve_issue("local:fix-val")  # Local issue
        >>> issue = resolve_issue("prompt:Fix the bug")  # Prompt
        >>> issue = resolve_issue("Fix the validation")  # Treated as prompt
    """
    # Remove leading/trailing whitespace
    issue_ref = issue_ref.strip()

    # Check for explicit prefixes
    if issue_ref.startswith("local:"):
        provider = LocalIssueProvider(project_root)
        return provider.fetch_issue(issue_ref[6:])  # Remove "local:" prefix

    if issue_ref.startswith("prompt:"):
        provider = PromptIssueProvider()
        return provider.create_from_prompt(issue_ref[7:])  # Remove "prompt:" prefix

    if issue_ref.startswith("github:"):
        provider = GitHubIssueProvider(repo_path)
        return provider.fetch_issue(issue_ref[7:])  # Remove "github:" prefix

    if issue_ref.startswith("gitlab:"):
        # Support both formats:
        # - Simple: gitlab:123 (uses current repo's remote)
        # - Extended: gitlab:PROJECT_PATH:123 (explicit project)
        gitlab_ref = issue_ref[7:]  # Remove "gitlab:" prefix

        # Check if extended format (contains colon)
        if ":" in gitlab_ref:
            # Extended format: gitlab:PROJECT_PATH:ISSUE_NUMBER
            parts = gitlab_ref.rsplit(":", 1)  # Split from right to handle paths with colons
            if len(parts) == 2:
                project_path = parts[0]
                issue_number = parts[1]

                # Validate project path format (should be namespace/project)
                if "/" not in project_path:
                    raise ValueError(
                        f"Invalid GitLab project path format: '{project_path}'. "
                        f"Expected format: 'namespace/project' (e.g., 'ameno13/jerry')"
                    )

                provider = GitLabIssueProvider(project_path=project_path)
                return provider.fetch_issue(issue_number)
            else:
                raise ValueError(
                    f"Invalid GitLab issue reference format: '{issue_ref}'. "
                    f"Expected 'gitlab:ISSUE_NUMBER' or 'gitlab:PROJECT_PATH:ISSUE_NUMBER'"
                )
        else:
            # Simple format: gitlab:123
            # Check for platform mismatch
            from .git_ops import detect_git_platform, get_repo_url

            try:
                platform = detect_git_platform()
                remote_url = get_repo_url()
            except Exception as e:
                # If we can't detect platform, provide helpful message anyway
                raise ValueError(
                    f"Cannot resolve GitLab issue '{issue_ref}' - unable to detect git platform.\n\n"
                    f"To specify the GitLab project explicitly, use the extended format:\n"
                    f"  gitlab:PROJECT_PATH:ISSUE_NUMBER\n\n"
                    f"Example:\n"
                    f"  gitlab:ameno13/jerry:{gitlab_ref}\n\n"
                    f"Original error: {e}"
                )

            if platform != "gitlab":
                # Platform mismatch - provide helpful error
                raise ValueError(
                    f"Cannot resolve GitLab issue '{issue_ref}' - current repository "
                    f"is hosted on {platform} ({remote_url}).\n\n"
                    f"To reference a GitLab issue from a different project, use the extended format:\n"
                    f"  gitlab:PROJECT_PATH:ISSUE_NUMBER\n\n"
                    f"Example:\n"
                    f"  gitlab:ameno13/jerry:{gitlab_ref}"
                )

            # Platform matches, use simple format
            provider = GitLabIssueProvider(project_path=repo_path)
            return provider.fetch_issue(gitlab_ref)

    # Check for local file path
    if issue_ref.endswith(".md") and ("issues/" in issue_ref or "/" in issue_ref):
        provider = LocalIssueProvider(project_root)
        return provider.fetch_issue(issue_ref)

    # Check for numeric issue number - auto-detect platform from git remote
    if issue_ref.isdigit():
        from .git_ops import detect_git_platform

        platform = detect_git_platform()
        if platform == "gitlab":
            provider = GitLabIssueProvider(repo_path)
            return provider.fetch_issue(issue_ref)
        else:
            # Default to GitHub for backward compatibility
            provider = GitHubIssueProvider(repo_path)
            return provider.fetch_issue(issue_ref)

    # Default: treat as prompt
    provider = PromptIssueProvider()
    return provider.create_from_prompt(issue_ref)


def get_provider_for_issue(
    issue: Issue,
    repo_path: Optional[str] = None,
    project_root: Optional[str] = None,
) -> IssueProvider:
    """Get the appropriate provider for an issue.

    Args:
        issue: Issue object.
        repo_path: GitHub repo path (owner/repo) or GitLab project path (namespace/project).
                   If None, uses issue.repo_path if available.
        project_root: Project root for local issues.

    Returns:
        Provider instance for the issue's source.
    """
    # Use issue.repo_path if not explicitly provided
    effective_repo_path = repo_path or issue.repo_path

    if issue.source == IssueSource.GITHUB:
        return GitHubIssueProvider(effective_repo_path)
    elif issue.source == IssueSource.GITLAB:
        return GitLabIssueProvider(effective_repo_path)
    elif issue.source == IssueSource.LOCAL:
        return LocalIssueProvider(project_root)
    elif issue.source == IssueSource.PROMPT:
        return PromptIssueProvider()
    else:
        raise ValueError(f"Unknown issue source: {issue.source}")
