"""Notification Provider abstraction for Jerry ADW system.

Provides platform-agnostic notification operations (comments, updates).
Follows the same pattern as issue_providers.py and code_review_providers.py.

Supported platforms:
- GitHub (gh CLI for issue/PR comments)
- Local (appends to issue markdown files)
- Logging (dry-run/testing mode)
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Protocol, runtime_checkable

from .data_types import Issue, IssueSource


@runtime_checkable
class NotificationProvider(Protocol):
    """Protocol for notification systems.

    Implementations handle platform-specific notification delivery while
    presenting a unified interface to ADW workflows.
    """

    def notify(
        self,
        target: Issue,
        message: str,
        agent_id: Optional[str] = None,
    ) -> bool:
        """Send a notification (comment) to an issue.

        Args:
            target: The issue to notify
            message: The notification message
            agent_id: Optional agent/workflow ID for prefixing

        Returns:
            True if notification was sent successfully
        """
        ...

    @property
    def platform(self) -> str:
        """Return the platform identifier."""
        ...


class GitHubNotificationProvider:
    """GitHub notification operations using gh CLI."""

    def __init__(self, repo_path: Optional[str] = None, logger: Optional[logging.Logger] = None):
        """Initialize GitHub notification provider.

        Args:
            repo_path: Repository path (owner/repo format)
            logger: Optional logger instance
        """
        self._repo_path = repo_path
        self._logger = logger or logging.getLogger(__name__)

    @property
    def platform(self) -> str:
        return "github"

    def _get_repo_path(self, cwd: Optional[str] = None) -> Optional[str]:
        """Get repository path from remote URL or cached value."""
        if self._repo_path:
            return self._repo_path

        import subprocess

        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        if result.returncode != 0:
            return None

        url = result.stdout.strip()
        # Extract owner/repo from URL
        if url.startswith("git@github.com:"):
            path = url.replace("git@github.com:", "").replace(".git", "")
        elif "github.com" in url:
            parts = url.split("github.com/")[-1].replace(".git", "")
            path = parts
        else:
            return None

        self._repo_path = path
        return path

    def notify(
        self,
        target: Issue,
        message: str,
        agent_id: Optional[str] = None,
    ) -> bool:
        """Post a comment to a GitHub issue."""
        import subprocess

        repo_path = self._get_repo_path()
        if not repo_path:
            self._logger.error("Failed to determine repository path")
            return False

        # Format message with agent ID prefix if provided
        formatted_message = message
        if agent_id:
            formatted_message = f"{agent_id}: {message}"

        result = subprocess.run(
            [
                "gh", "issue", "comment", target.id,
                "--repo", repo_path,
                "--body", formatted_message,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self._logger.error(f"Failed to post comment: {result.stderr}")
            return False

        self._logger.info(f"Posted comment to issue #{target.id}")
        return True


class GitLabNotificationProvider:
    """GitLab notification operations using glab CLI."""

    def __init__(self, project_path: Optional[str] = None, logger: Optional[logging.Logger] = None):
        """Initialize GitLab notification provider.

        Args:
            project_path: Project path (namespace/project format)
            logger: Optional logger instance
        """
        self._project_path = project_path
        self._logger = logger or logging.getLogger(__name__)

    @property
    def platform(self) -> str:
        return "gitlab"

    def _get_project_path(self, cwd: Optional[str] = None) -> Optional[str]:
        """Get project path from remote URL or cached value."""
        if self._project_path:
            return self._project_path

        import subprocess

        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        if result.returncode != 0:
            return None

        url = result.stdout.strip()
        # Extract namespace/project from URL
        from .gitlab import extract_project_path

        try:
            path = extract_project_path(url)
            self._project_path = path
            return path
        except Exception:
            return None

    def notify(
        self,
        target: Issue,
        message: str,
        agent_id: Optional[str] = None,
    ) -> bool:
        """Post a comment to a GitLab issue."""
        import subprocess

        project_path = self._get_project_path()
        if not project_path:
            self._logger.error("Failed to determine project path")
            return False

        # Format message with agent ID prefix if provided
        formatted_message = message
        if agent_id:
            formatted_message = f"{agent_id}: {message}"

        result = subprocess.run(
            [
                "glab", "issue", "note", target.id,
                "--repo", project_path,
                "--message", formatted_message,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self._logger.error(f"Failed to post comment to GitLab: {result.stderr}")
            return False

        self._logger.info(f"Posted comment to GitLab issue #{target.id}")
        return True


class LocalNotificationProvider:
    """Local notification provider - appends to issue markdown files."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize local notification provider.

        Args:
            logger: Optional logger instance
        """
        self._logger = logger or logging.getLogger(__name__)

    @property
    def platform(self) -> str:
        return "local"

    def notify(
        self,
        target: Issue,
        message: str,
        agent_id: Optional[str] = None,
    ) -> bool:
        """Append a comment to a local issue file."""
        if not target.local_path:
            self._logger.warning(f"No local path for issue {target.id}, logging only")
            self._logger.info(f"[NOTIFICATION] {agent_id or 'ADW'}: {message}")
            return True

        path = Path(target.local_path)
        if not path.exists():
            self._logger.error(f"Local issue file not found: {path}")
            return False

        # Format the update
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        agent_prefix = f"{agent_id}: " if agent_id else ""
        update = f"\n\n---\n**Update** ({timestamp})\n\n{agent_prefix}{message}\n"

        try:
            with open(path, "a") as f:
                f.write(update)
            self._logger.info(f"Appended notification to {path}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to append to {path}: {e}")
            return False


class LoggingNotificationProvider:
    """Logging-only notification provider for dry-run/testing."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize logging notification provider.

        Args:
            logger: Optional logger instance
        """
        self._logger = logger or logging.getLogger(__name__)

    @property
    def platform(self) -> str:
        return "logging"

    def notify(
        self,
        target: Issue,
        message: str,
        agent_id: Optional[str] = None,
    ) -> bool:
        """Log a notification without sending it anywhere."""
        agent_prefix = f"{agent_id}: " if agent_id else ""
        self._logger.info(
            f"[NOTIFICATION] Issue #{target.id}: {agent_prefix}{message}"
        )
        return True


def get_notification_provider(
    issue: Optional[Issue] = None,
    platform: Optional[str] = None,
    repo_path: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    dry_run: bool = False,
) -> NotificationProvider:
    """Factory function to get the appropriate notification provider.

    Args:
        issue: Optional issue to determine platform from source
        platform: Explicit platform to use (overrides issue source)
        repo_path: Repository path for GitHub (owner/repo) or GitLab (namespace/project)
        logger: Optional logger instance
        dry_run: If True, use logging provider instead of actual delivery

    Returns:
        NotificationProvider instance for the appropriate platform
    """
    if dry_run:
        return LoggingNotificationProvider(logger=logger)

    # Determine platform
    if platform:
        target_platform = platform
    elif issue:
        target_platform = issue.source.value
    else:
        target_platform = "logging"

    # Create and return provider
    if target_platform == "github":
        return GitHubNotificationProvider(repo_path=repo_path, logger=logger)
    elif target_platform == "gitlab":
        return GitLabNotificationProvider(project_path=repo_path, logger=logger)
    elif target_platform == "local":
        return LocalNotificationProvider(logger=logger)
    else:
        return LoggingNotificationProvider(logger=logger)
