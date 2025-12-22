"""Code Review Provider abstraction for Jerry ADW system.

Provides platform-agnostic code review operations (PR/MR creation, approval, merge).
Follows the same pattern as issue_providers.py for consistency.

Supported platforms:
- GitHub (gh CLI)
- GitLab (gitlab CLI - future)
- Bitbucket (bitbucket CLI - future)
- Local (dry-run/testing mode)
"""

import json
import logging
import subprocess
from typing import Optional, Tuple, Dict, Any, Protocol, runtime_checkable

from .data_types import (
    CodeReview,
    CodeReviewPlatform,
    CodeReviewStatus,
    Issue,
    IssueSource,
)


@runtime_checkable
class CodeReviewProvider(Protocol):
    """Protocol for code review systems (PRs, MRs).

    Implementations handle platform-specific operations while presenting
    a unified interface to ADW workflows.
    """

    def check_exists(
        self, branch_name: str, cwd: Optional[str] = None
    ) -> Optional[CodeReview]:
        """Check if a code review exists for the given branch.

        Args:
            branch_name: The feature branch name
            cwd: Working directory for git operations

        Returns:
            CodeReview if exists, None otherwise
        """
        ...

    def create(
        self,
        branch_name: str,
        title: str,
        body: str,
        issue: Optional[Issue] = None,
        base_branch: str = "main",
        cwd: Optional[str] = None,
    ) -> Tuple[Optional[CodeReview], Optional[str]]:
        """Create a new code review.

        Args:
            branch_name: The feature branch name
            title: PR/MR title
            body: PR/MR description
            issue: Optional linked issue for auto-close
            base_branch: Target branch for merge
            cwd: Working directory for git operations

        Returns:
            Tuple of (CodeReview, error_message)
        """
        ...

    def approve(
        self,
        review_id: str,
        message: str = "Approved by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Approve a code review.

        Args:
            review_id: The PR/MR identifier
            message: Approval message
            cwd: Working directory for git operations

        Returns:
            Tuple of (success, error_message)
        """
        ...

    def merge(
        self,
        review_id: str,
        method: str = "squash",
        message: str = "Merged by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Merge a code review.

        Args:
            review_id: The PR/MR identifier
            method: Merge method (merge, squash, rebase)
            message: Merge commit message
            cwd: Working directory for git operations

        Returns:
            Tuple of (success, error_message)
        """
        ...

    def get_status(
        self, review_id: str, cwd: Optional[str] = None
    ) -> Tuple[Optional[CodeReviewStatus], Optional[str]]:
        """Get the status of a code review.

        Args:
            review_id: The PR/MR identifier
            cwd: Working directory for git operations

        Returns:
            Tuple of (status, error_message)
        """
        ...

    def list_open_reviews(
        self, cwd: Optional[str] = None
    ) -> list[CodeReview]:
        """List all open code reviews.

        Args:
            cwd: Working directory for git operations

        Returns:
            List of open CodeReview objects
        """
        ...

    @property
    def platform(self) -> CodeReviewPlatform:
        """Return the platform type."""
        ...


class GitHubCodeReviewProvider:
    """GitHub PR operations using gh CLI."""

    def __init__(self, repo_path: Optional[str] = None, logger: Optional[logging.Logger] = None):
        """Initialize GitHub provider.

        Args:
            repo_path: Repository path (owner/repo format)
            logger: Optional logger instance
        """
        self._repo_path = repo_path
        self._logger = logger or logging.getLogger(__name__)

    @property
    def platform(self) -> CodeReviewPlatform:
        return CodeReviewPlatform.GITHUB

    def _get_repo_path(self, cwd: Optional[str] = None) -> Optional[str]:
        """Get repository path from remote URL or cached value."""
        if self._repo_path:
            return self._repo_path

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

    def check_exists(
        self, branch_name: str, cwd: Optional[str] = None
    ) -> Optional[CodeReview]:
        """Check if PR exists for branch."""
        repo_path = self._get_repo_path(cwd)
        if not repo_path:
            return None

        result = subprocess.run(
            [
                "gh", "pr", "list",
                "--repo", repo_path,
                "--head", branch_name,
                "--json", "number,title,body,url,state",
                "--limit", "1",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return None

        prs = json.loads(result.stdout)
        if not prs:
            return None

        pr = prs[0]
        status_map = {
            "OPEN": CodeReviewStatus.OPEN,
            "CLOSED": CodeReviewStatus.CLOSED,
            "MERGED": CodeReviewStatus.MERGED,
        }

        return CodeReview(
            id=str(pr["number"]),
            title=pr["title"],
            body=pr["body"] or "",
            branch_name=branch_name,
            platform=CodeReviewPlatform.GITHUB,
            url=pr["url"],
            status=status_map.get(pr["state"], CodeReviewStatus.OPEN),
        )

    def create(
        self,
        branch_name: str,
        title: str,
        body: str,
        issue: Optional[Issue] = None,
        base_branch: str = "main",
        cwd: Optional[str] = None,
    ) -> Tuple[Optional[CodeReview], Optional[str]]:
        """Create a new GitHub PR."""
        repo_path = self._get_repo_path(cwd)
        if not repo_path:
            return None, "Failed to determine repository path"

        # Check if PR already exists
        existing = self.check_exists(branch_name, cwd)
        if existing:
            self._logger.info(f"PR already exists: {existing.url}")
            return existing, None

        # Build PR body with issue reference if available
        pr_body = body
        if issue and issue.source == IssueSource.GITHUB:
            pr_body += f"\n\nCloses #{issue.id}"

        cmd = [
            "gh", "pr", "create",
            "--repo", repo_path,
            "--head", branch_name,
            "--base", base_branch,
            "--title", title,
            "--body", pr_body,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)

        if result.returncode != 0:
            return None, result.stderr

        # Extract PR URL from output
        pr_url = result.stdout.strip()
        pr_number = pr_url.split("/")[-1] if "/" in pr_url else ""

        return CodeReview(
            id=pr_number,
            title=title,
            body=pr_body,
            branch_name=branch_name,
            platform=CodeReviewPlatform.GITHUB,
            url=pr_url,
            status=CodeReviewStatus.OPEN,
            issue_ref=f"github:{issue.id}" if issue else None,
            base_branch=base_branch,
        ), None

    def approve(
        self,
        review_id: str,
        message: str = "Approved by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Approve a GitHub PR."""
        repo_path = self._get_repo_path(cwd)
        if not repo_path:
            return False, "Failed to determine repository path"

        result = subprocess.run(
            [
                "gh", "pr", "review", review_id,
                "--repo", repo_path,
                "--approve",
                "--body", message,
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, result.stderr

        self._logger.info(f"Approved PR #{review_id}")
        return True, None

    def merge(
        self,
        review_id: str,
        method: str = "squash",
        message: str = "Merged by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Merge a GitHub PR."""
        repo_path = self._get_repo_path(cwd)
        if not repo_path:
            return False, "Failed to determine repository path"

        # Check if PR is mergeable
        result = subprocess.run(
            [
                "gh", "pr", "view", review_id,
                "--repo", repo_path,
                "--json", "mergeable,mergeStateStatus",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, f"Failed to check PR status: {result.stderr}"

        pr_status = json.loads(result.stdout)
        if pr_status.get("mergeable") != "MERGEABLE":
            return False, f"PR not mergeable. Status: {pr_status.get('mergeStateStatus', 'unknown')}"

        # Merge the PR
        result = subprocess.run(
            [
                "gh", "pr", "merge", review_id,
                "--repo", repo_path,
                f"--{method}",
                "--body", message,
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, result.stderr

        self._logger.info(f"Merged PR #{review_id} using {method} method")
        return True, None

    def get_status(
        self, review_id: str, cwd: Optional[str] = None
    ) -> Tuple[Optional[CodeReviewStatus], Optional[str]]:
        """Get status of a GitHub PR."""
        repo_path = self._get_repo_path(cwd)
        if not repo_path:
            return None, "Failed to determine repository path"

        result = subprocess.run(
            [
                "gh", "pr", "view", review_id,
                "--repo", repo_path,
                "--json", "state,reviewDecision",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return None, result.stderr

        pr_data = json.loads(result.stdout)
        state = pr_data.get("state", "")
        review_decision = pr_data.get("reviewDecision", "")

        if state == "MERGED":
            return CodeReviewStatus.MERGED, None
        elif state == "CLOSED":
            return CodeReviewStatus.CLOSED, None
        elif review_decision == "APPROVED":
            return CodeReviewStatus.APPROVED, None
        elif review_decision == "CHANGES_REQUESTED":
            return CodeReviewStatus.CHANGES_REQUESTED, None
        else:
            return CodeReviewStatus.OPEN, None

    def list_open_reviews(
        self, cwd: Optional[str] = None
    ) -> list[CodeReview]:
        """List all open GitHub PRs."""
        repo_path = self._get_repo_path(cwd)
        if not repo_path:
            self._logger.warning("Failed to determine repository path")
            return []

        result = subprocess.run(
            [
                "gh", "pr", "list",
                "--repo", repo_path,
                "--state", "open",
                "--json", "number,title,body,url,headRefName,state",
                "--limit", "100",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            self._logger.error(f"Failed to list PRs: {result.stderr}")
            return []

        prs = json.loads(result.stdout) if result.stdout.strip() else []

        code_reviews = []
        for pr in prs:
            status_map = {
                "OPEN": CodeReviewStatus.OPEN,
                "CLOSED": CodeReviewStatus.CLOSED,
                "MERGED": CodeReviewStatus.MERGED,
            }

            code_reviews.append(CodeReview(
                id=str(pr["number"]),
                title=pr["title"],
                body=pr.get("body", ""),
                branch_name=pr["headRefName"],
                platform=CodeReviewPlatform.GITHUB,
                url=pr["url"],
                status=status_map.get(pr["state"], CodeReviewStatus.OPEN),
            ))

        self._logger.info(f"Found {len(code_reviews)} open GitHub PRs")
        return code_reviews


class GitLabCodeReviewProvider:
    """GitLab MR operations using glab CLI."""

    def __init__(self, project_path: Optional[str] = None, logger: Optional[logging.Logger] = None):
        """Initialize GitLab provider.

        Args:
            project_path: Project path (namespace/project format)
            logger: Optional logger instance
        """
        self._project_path = project_path
        self._logger = logger or logging.getLogger(__name__)

    @property
    def platform(self) -> CodeReviewPlatform:
        return CodeReviewPlatform.GITLAB

    def _get_project_path(self, cwd: Optional[str] = None) -> Optional[str]:
        """Get project path from remote URL or cached value."""
        if self._project_path:
            return self._project_path

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

    def check_exists(
        self, branch_name: str, cwd: Optional[str] = None
    ) -> Optional[CodeReview]:
        """Check if MR exists for branch."""
        project_path = self._get_project_path(cwd)
        if not project_path:
            return None

        result = subprocess.run(
            [
                "glab", "mr", "list",
                "--repo", project_path,
                "--source-branch", branch_name,
                "--output", "json",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return None

        mrs = json.loads(result.stdout) if result.stdout.strip() else []
        if not mrs:
            return None

        mr = mrs[0]
        # Map GitLab states to CodeReviewStatus
        state_map = {
            "opened": CodeReviewStatus.OPEN,
            "closed": CodeReviewStatus.CLOSED,
            "merged": CodeReviewStatus.MERGED,
        }

        return CodeReview(
            id=str(mr.get("iid", mr.get("id"))),
            title=mr.get("title", ""),
            body=mr.get("description", ""),
            branch_name=branch_name,
            platform=CodeReviewPlatform.GITLAB,
            url=mr.get("web_url", ""),
            status=state_map.get(mr.get("state", "opened").lower(), CodeReviewStatus.OPEN),
        )

    def create(
        self,
        branch_name: str,
        title: str,
        body: str,
        issue: Optional[Issue] = None,
        base_branch: str = "main",
        cwd: Optional[str] = None,
    ) -> Tuple[Optional[CodeReview], Optional[str]]:
        """Create a new GitLab MR."""
        project_path = self._get_project_path(cwd)
        if not project_path:
            return None, "Failed to determine project path"

        # Check if MR already exists
        existing = self.check_exists(branch_name, cwd)
        if existing:
            self._logger.info(f"MR already exists: {existing.url}")
            return existing, None

        # Build MR body with issue reference if available
        mr_body = body
        if issue and issue.source == IssueSource.GITLAB:
            # GitLab uses "Closes #123" syntax
            mr_body += f"\n\nCloses #{issue.id}"

        cmd = [
            "glab", "mr", "create",
            "--repo", project_path,
            "--source-branch", branch_name,
            "--target-branch", base_branch,
            "--title", title,
            "--description", mr_body,
            "--yes",  # Skip confirmation
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)

        if result.returncode != 0:
            return None, result.stderr

        # Extract MR URL from output
        mr_url = result.stdout.strip()
        # Parse MR number from URL (e.g., https://gitlab.com/namespace/project/-/merge_requests/123)
        mr_number = ""
        if "merge_requests/" in mr_url:
            mr_number = mr_url.split("merge_requests/")[-1].split("/")[0]

        return CodeReview(
            id=mr_number,
            title=title,
            body=mr_body,
            branch_name=branch_name,
            platform=CodeReviewPlatform.GITLAB,
            url=mr_url,
            status=CodeReviewStatus.OPEN,
            issue_ref=f"gitlab:{issue.id}" if issue else None,
            base_branch=base_branch,
        ), None

    def approve(
        self,
        review_id: str,
        message: str = "Approved by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Approve a GitLab MR."""
        project_path = self._get_project_path(cwd)
        if not project_path:
            return False, "Failed to determine project path"

        result = subprocess.run(
            [
                "glab", "mr", "approve", review_id,
                "--repo", project_path,
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, result.stderr

        # Add approval comment
        subprocess.run(
            [
                "glab", "mr", "note", review_id,
                "--repo", project_path,
                "--message", message,
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        self._logger.info(f"Approved MR !{review_id}")
        return True, None

    def merge(
        self,
        review_id: str,
        method: str = "squash",
        message: str = "Merged by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Merge a GitLab MR."""
        project_path = self._get_project_path(cwd)
        if not project_path:
            return False, "Failed to determine project path"

        # Check if MR is mergeable
        result = subprocess.run(
            [
                "glab", "mr", "view", review_id,
                "--repo", project_path,
                "--output", "json",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, f"Failed to check MR status: {result.stderr}"

        mr_data = json.loads(result.stdout)
        if mr_data.get("state") == "merged":
            return True, None  # Already merged

        # Map merge methods: squash -> squash, merge -> merge, rebase -> rebase
        # GitLab uses: merge, squash (called squash_commit), rebase_merge
        gitlab_method_map = {
            "squash": "squash",
            "merge": "merge",
            "rebase": "rebase",
        }
        gitlab_method = gitlab_method_map.get(method, "squash")

        # Merge the MR
        result = subprocess.run(
            [
                "glab", "mr", "merge", review_id,
                "--repo", project_path,
                f"--{gitlab_method}",
                "--yes",  # Skip confirmation
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, result.stderr

        self._logger.info(f"Merged MR !{review_id} using {method} method")
        return True, None

    def get_status(
        self, review_id: str, cwd: Optional[str] = None
    ) -> Tuple[Optional[CodeReviewStatus], Optional[str]]:
        """Get status of a GitLab MR."""
        project_path = self._get_project_path(cwd)
        if not project_path:
            return None, "Failed to determine project path"

        result = subprocess.run(
            [
                "glab", "mr", "view", review_id,
                "--repo", project_path,
                "--output", "json",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return None, result.stderr

        mr_data = json.loads(result.stdout)
        state = mr_data.get("state", "").lower()

        if state == "merged":
            return CodeReviewStatus.MERGED, None
        elif state == "closed":
            return CodeReviewStatus.CLOSED, None
        elif state == "opened":
            # Check approval status
            # GitLab MRs have approved_by field
            if mr_data.get("approved_by"):
                return CodeReviewStatus.APPROVED, None
            return CodeReviewStatus.OPEN, None
        else:
            return CodeReviewStatus.OPEN, None

    def list_open_reviews(
        self, cwd: Optional[str] = None
    ) -> list[CodeReview]:
        """List all open GitLab MRs."""
        project_path = self._get_project_path(cwd)
        if not project_path:
            self._logger.warning("Failed to determine project path")
            return []

        result = subprocess.run(
            [
                "glab", "mr", "list",
                "--repo", project_path,
                "--state", "opened",
                "--output", "json",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            self._logger.error(f"Failed to list MRs: {result.stderr}")
            return []

        mrs = json.loads(result.stdout) if result.stdout.strip() else []

        code_reviews = []
        for mr in mrs:
            # Map GitLab states to CodeReviewStatus
            state_map = {
                "opened": CodeReviewStatus.OPEN,
                "closed": CodeReviewStatus.CLOSED,
                "merged": CodeReviewStatus.MERGED,
            }

            code_reviews.append(CodeReview(
                id=str(mr.get("iid", mr.get("id"))),
                title=mr.get("title", ""),
                body=mr.get("description", ""),
                branch_name=mr.get("source_branch", ""),
                platform=CodeReviewPlatform.GITLAB,
                url=mr.get("web_url", ""),
                status=state_map.get(mr.get("state", "opened").lower(), CodeReviewStatus.OPEN),
            ))

        self._logger.info(f"Found {len(code_reviews)} open GitLab MRs")
        return code_reviews


class LocalCodeReviewProvider:
    """Local/dry-run mode - tracks operations without executing."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize local provider."""
        self._logger = logger or logging.getLogger(__name__)
        self._reviews: Dict[str, CodeReview] = {}
        self._next_id = 1

    @property
    def platform(self) -> CodeReviewPlatform:
        return CodeReviewPlatform.LOCAL

    def check_exists(
        self, branch_name: str, cwd: Optional[str] = None
    ) -> Optional[CodeReview]:
        """Check if a local code review exists for the branch."""
        for review in self._reviews.values():
            if review.branch_name == branch_name:
                return review
        return None

    def create(
        self,
        branch_name: str,
        title: str,
        body: str,
        issue: Optional[Issue] = None,
        base_branch: str = "main",
        cwd: Optional[str] = None,
    ) -> Tuple[Optional[CodeReview], Optional[str]]:
        """Create a local code review (for dry-run/testing)."""
        # Check if already exists
        existing = self.check_exists(branch_name, cwd)
        if existing:
            return existing, None

        review_id = str(self._next_id)
        self._next_id += 1

        review = CodeReview(
            id=review_id,
            title=title,
            body=body,
            branch_name=branch_name,
            platform=CodeReviewPlatform.LOCAL,
            url=f"local://review/{review_id}",
            status=CodeReviewStatus.OPEN,
            issue_ref=issue.source_ref if issue else None,
            base_branch=base_branch,
        )

        self._reviews[review_id] = review
        self._logger.info(f"[LOCAL] Created code review #{review_id}: {title}")
        return review, None

    def approve(
        self,
        review_id: str,
        message: str = "Approved by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Approve a local code review."""
        if review_id not in self._reviews:
            return False, f"Code review #{review_id} not found"

        self._reviews[review_id].status = CodeReviewStatus.APPROVED
        self._logger.info(f"[LOCAL] Approved code review #{review_id}")
        return True, None

    def merge(
        self,
        review_id: str,
        method: str = "squash",
        message: str = "Merged by ADW workflow",
        cwd: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Merge a local code review."""
        if review_id not in self._reviews:
            return False, f"Code review #{review_id} not found"

        from datetime import datetime

        self._reviews[review_id].status = CodeReviewStatus.MERGED
        self._reviews[review_id].merge_method = method
        self._reviews[review_id].merged_at = datetime.now()
        self._logger.info(f"[LOCAL] Merged code review #{review_id} using {method}")
        return True, None

    def get_status(
        self, review_id: str, cwd: Optional[str] = None
    ) -> Tuple[Optional[CodeReviewStatus], Optional[str]]:
        """Get status of a local code review."""
        if review_id not in self._reviews:
            return None, f"Code review #{review_id} not found"

        return self._reviews[review_id].status, None

    def list_open_reviews(
        self, cwd: Optional[str] = None
    ) -> list[CodeReview]:
        """List all open local code reviews."""
        open_reviews = [
            review for review in self._reviews.values()
            if review.status == CodeReviewStatus.OPEN
        ]
        self._logger.info(f"Found {len(open_reviews)} open local code reviews")
        return open_reviews


def get_code_review_provider(
    issue: Optional[Issue] = None,
    platform: Optional[CodeReviewPlatform] = None,
    repo_path: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    cwd: Optional[str] = None,
) -> CodeReviewProvider:
    """Factory function to get the appropriate code review provider.

    Args:
        issue: Optional issue to determine platform from source
        platform: Explicit platform to use (overrides issue source)
        repo_path: Repository path for GitHub (owner/repo) or GitLab (namespace/project)
        logger: Optional logger instance
        cwd: Working directory for git platform detection

    Returns:
        CodeReviewProvider instance for the appropriate platform
    """
    # Determine platform
    if platform:
        target_platform = platform
    elif issue:
        # Map issue source to code review platform
        source_to_platform = {
            IssueSource.GITHUB: CodeReviewPlatform.GITHUB,
            IssueSource.GITLAB: CodeReviewPlatform.GITLAB,
            IssueSource.LOCAL: CodeReviewPlatform.LOCAL,
            IssueSource.PROMPT: CodeReviewPlatform.LOCAL,
            IssueSource.LINEAR: CodeReviewPlatform.LOCAL,  # Linear uses GitHub for PRs typically
        }
        target_platform = source_to_platform.get(issue.source, CodeReviewPlatform.LOCAL)
    else:
        # Try to auto-detect from git remote
        from .git_ops import detect_git_platform

        git_platform = detect_git_platform(cwd=cwd)
        if git_platform == "github":
            target_platform = CodeReviewPlatform.GITHUB
        elif git_platform == "gitlab":
            target_platform = CodeReviewPlatform.GITLAB
        else:
            # Default to local for safety
            target_platform = CodeReviewPlatform.LOCAL

    # Create and return provider
    if target_platform == CodeReviewPlatform.GITHUB:
        return GitHubCodeReviewProvider(repo_path=repo_path, logger=logger)
    elif target_platform == CodeReviewPlatform.GITLAB:
        return GitLabCodeReviewProvider(project_path=repo_path, logger=logger)
    else:
        # All other platforms fall back to local for now
        return LocalCodeReviewProvider(logger=logger)
