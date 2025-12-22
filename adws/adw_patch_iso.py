#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml"]
# ///

"""
ADW Patch Isolated - AI Developer Workflow for single-issue patches with worktree isolation

Usage:
  uv run adw_patch_iso.py <issue-ref> [adw-id] [--dry-run]

Issue Reference Formats:
  - GitHub: "123" or "github:123"
  - Local: "local:abc123" or "issues/issue-abc.md"
  - Prompt: "prompt:Fix the validation error"
  - Direct: Any text not matching above patterns (treated as prompt)

Examples:
  uv run adw_patch_iso.py 123                        # GitHub issue #123
  uv run adw_patch_iso.py github:456                 # Explicit GitHub issue
  uv run adw_patch_iso.py local:fix-validation       # Local issue
  uv run adw_patch_iso.py "Fix the CLI parsing bug"  # Prompt-based (creates ephemeral issue)

Workflow:
1. Resolve issue from any source (GitHub, Local, Prompt)
2. Create/validate isolated worktree
3. Allocate dedicated ports (9100-9114 backend, 9200-9214 frontend)
4. Get patch content from issue body
5. Create patch plan based on issue content
6. Implement the patch plan
7. Commit changes
8. Push and create/update PR (if applicable)

For GitHub issues:
- The 'adw_patch' keyword is required in comments or issue body
- Progress updates are posted as issue comments

For Local/Prompt issues:
- The full issue body is used as patch content
- Status updates are written to the local issue file (if local)

Key features:
- Runs in isolated git worktree under trees/<adw_id>/
- Uses dedicated ports to avoid conflicts
- Passes working_dir to all agent and git operations
- Enables parallel execution of multiple patches
- Supports multiple issue sources for flexibility
"""

import sys
import os
import logging
import json
import subprocess
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from adws.adw_modules.state import ADWState
from adws.adw_modules.git_ops import commit_changes, finalize_git_operations
from adws.adw_modules.github import (
    fetch_issue,
    make_issue_comment,
    get_repo_url,
    extract_repo_path,
    find_keyword_from_comment,
)
from adws.adw_modules.workflow_ops import (
    create_commit,
    format_issue_message,
    ensure_adw_id,
    implement_plan,
    create_and_implement_patch,
    AGENT_IMPLEMENTOR,
)
from adws.adw_modules.worktree_ops import (
    create_worktree,
    validate_worktree,
    get_ports_for_adw,
    is_port_available,
    find_next_available_ports,
    setup_worktree_environment,
    cleanup_worktree_config_files,
)
from adws.adw_modules.utils import setup_logger, check_env_vars
from adws.adw_modules.data_types import (
    GitHubIssue,
    Issue,
    IssueSource,
    IssueStatus,
    AgentTemplateRequest,
    AgentPromptResponse,
)
from adws.adw_modules.agent import execute_template
from adws.adw_modules.issue_providers import (
    resolve_issue,
    get_provider_for_issue,
    LocalIssueProvider,
)

# Agent name constants
AGENT_PATCH_PLANNER = "patch_planner"
AGENT_PATCH_IMPLEMENTOR = "patch_implementor"


def notify_issue(
    issue: Issue,
    adw_id: str,
    agent_name: str,
    message: str,
    logger: logging.Logger,
) -> None:
    """Send notification to issue based on source type.

    Args:
        issue: The issue to notify
        adw_id: ADW ID for formatting messages
        agent_name: Name of the agent sending notification
        message: Message content
        logger: Logger instance
    """
    # Use the provider abstraction for all issue sources
    if issue.source in (IssueSource.GITHUB, IssueSource.GITLAB, IssueSource.LOCAL):
        try:
            provider = get_provider_for_issue(issue)
            provider.add_comment(
                issue,
                format_issue_message(adw_id, agent_name, message),
                adw_id,
            )
        except Exception as e:
            logger.warning(f"Failed to add comment to issue: {e}")
    # Prompt issues are ephemeral - no notifications


def update_issue_status(
    issue: Issue,
    status: IssueStatus,
    message: str,
    adw_id: str,
    logger: logging.Logger,
) -> None:
    """Update issue status based on source type.

    Args:
        issue: The issue to update
        status: New status
        message: Status message
        adw_id: ADW ID for tracking
        logger: Logger instance
    """
    if issue.source == IssueSource.LOCAL:
        try:
            provider = LocalIssueProvider()
            provider.update_status(issue, status, message, agent_id=adw_id)
        except Exception as e:
            logger.warning(f"Failed to update local issue status: {e}")
    # GitHub issues use labels, Prompt issues are ephemeral


def get_patch_content_from_github(
    gh_issue: GitHubIssue, issue_id: str, adw_id: str, logger: logging.Logger
) -> Optional[str]:
    """Get patch content from GitHub issue comments or body containing 'adw_patch'.

    Args:
        gh_issue: The GitHub issue
        issue_id: Issue ID for comments
        adw_id: ADW ID for formatting messages
        logger: Logger instance

    Returns:
        The patch content or None if 'adw_patch' keyword is not found
    """
    # First, check for the latest comment containing 'adw_patch'
    keyword_comment = find_keyword_from_comment("adw_patch", gh_issue)

    if keyword_comment:
        # Use the comment body as the review change request
        logger.info(
            f"Found 'adw_patch' in comment, using comment body: {keyword_comment.body}"
        )
        review_change_request = keyword_comment.body
        make_issue_comment(
            issue_id,
            format_issue_message(
                adw_id,
                AGENT_PATCH_PLANNER,
                f"✅ Creating patch plan from comment containing 'adw_patch':\n\n```\n{keyword_comment.body}\n```",
            ),
        )
        return review_change_request
    elif "adw_patch" in gh_issue.body:
        # Use issue title and body as the review change request
        logger.info("Found 'adw_patch' in issue body, using issue title and body")
        review_change_request = f"Issue #{gh_issue.number}: {gh_issue.title}\n\n{gh_issue.body}"
        make_issue_comment(
            issue_id,
            format_issue_message(
                adw_id,
                AGENT_PATCH_PLANNER,
                "✅ Creating patch plan from issue containing 'adw_patch'",
            ),
        )
        return review_change_request
    else:
        return None


def get_patch_content(
    issue: Issue, adw_id: str, logger: logging.Logger, repo_path: Optional[str] = None
) -> str:
    """Get patch content based on issue source.

    For GitHub issues:
    - Requires 'adw_patch' keyword in comments or body

    For Local/Prompt issues:
    - Uses the full issue body as patch content

    Args:
        issue: The generic Issue object
        adw_id: ADW ID for formatting messages
        logger: Logger instance
        repo_path: GitHub repo path (for fetching full GitHub issue)

    Returns:
        The patch content to use for creating the patch plan

    Raises:
        SystemExit: If GitHub issue lacks 'adw_patch' keyword
    """
    if issue.source == IssueSource.GITHUB:
        # For GitHub, we need to fetch the full issue with comments
        gh_issue = fetch_issue(issue.id, repo_path)

        content = get_patch_content_from_github(gh_issue, issue.id, adw_id, logger)
        if content:
            return content

        # No 'adw_patch' keyword found, exit
        logger.error("No 'adw_patch' keyword found in issue body or comments")
        make_issue_comment(
            issue.id,
            format_issue_message(
                adw_id,
                "ops",
                "❌ No 'adw_patch' keyword found in issue body or comments. Add 'adw_patch' to trigger patch workflow.",
            ),
        )
        sys.exit(1)

    else:
        # For Local and Prompt issues, use the full body
        logger.info(f"Using issue body as patch content (source: {issue.source.value})")

        review_change_request = f"Issue: {issue.title}\n\n{issue.body}"

        notify_issue(
            issue, adw_id, AGENT_PATCH_PLANNER,
            "✅ Creating patch plan from issue content",
            logger,
        )

        return review_change_request


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse command line args
    if len(sys.argv) < 2:
        print("Usage: uv run adw_patch_iso.py <issue-ref> [adw-id] [--dry-run]")
        print("\nIssue Reference Formats:")
        print("  - GitHub: 123 or github:123")
        print("  - Local: local:abc123 or issues/issue-abc.md")
        print("  - Prompt: prompt:Fix the validation error")
        print("  - Direct: Any text not matching above (treated as prompt)")
        sys.exit(1)

    issue_ref = sys.argv[1]

    # Handle optional arguments
    adw_id = None
    dry_run = False

    for arg in sys.argv[2:]:
        if arg == "--dry-run":
            dry_run = True
        elif not arg.startswith("-"):
            adw_id = arg

    # Dry-run mode: exit early with minimal operations (no network calls)
    if dry_run:
        # Generate placeholder ADW ID if not provided
        if not adw_id:
            import uuid
            adw_id = uuid.uuid4().hex[:8]

        print("[DRY RUN] Would execute isolated patch workflow:")
        print(f"  - Issue ref: {issue_ref}")
        print(f"  - ADW ID: {adw_id}")
        print(f"  - Create/validate isolated worktree at: trees/{adw_id}/")
        print(f"  - Allocate dedicated ports")
        print(f"  - Get patch content from issue")
        print(f"  - Create and implement patch plan")
        print(f"  - Commit changes")
        print(f"  - Push and create/update PR (if applicable)")
        return

    # Get repo information (needed for GitHub issues)
    repo_path = None
    try:
        github_repo_url = get_repo_url()
        repo_path = extract_repo_path(github_repo_url)
    except ValueError:
        # Not in a git repo with remote, OK for local/prompt issues
        pass

    # Resolve issue from any source
    try:
        issue: Issue = resolve_issue(issue_ref, repo_path=repo_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error resolving issue: {e}")
        sys.exit(1)

    # Use issue ID for state tracking
    issue_id = issue.id

    # Ensure ADW ID exists with initialized state
    temp_logger = setup_logger(adw_id, "adw_patch_iso") if adw_id else None
    adw_id = ensure_adw_id(issue_id, adw_id, temp_logger)

    # Load the state that was created/found by ensure_adw_id
    state = ADWState.load(adw_id, temp_logger)

    # Ensure state has the adw_id field
    if not state.get("adw_id"):
        state.update(adw_id=adw_id)

    # Store issue information in state
    state.update_issue(issue)

    # Track that this ADW workflow has run
    state.append_adw_id("adw_patch_iso")

    # Set up logger with ADW ID
    logger = setup_logger(adw_id, "adw_patch_iso")
    logger.info(f"ADW Patch Isolated starting - ID: {adw_id}, Issue: {issue_id} (source: {issue.source.value})")

    # Validate environment
    check_env_vars(logger)

    # Update issue status to in_progress
    update_issue_status(issue, IssueStatus.IN_PROGRESS, "Starting isolated patch workflow", adw_id, logger)

    logger.debug(f"Resolved issue: {issue.model_dump_json(indent=2)}")
    notify_issue(issue, adw_id, "ops", "✅ Starting isolated patch workflow", logger)

    # Determine branch name without checking out in main repo
    # 1. Check if branch name is already in state
    branch_name = state.get("branch_name")

    if not branch_name:
        # 2. Look for existing branch without checking it out
        from adws.adw_modules.workflow_ops import find_existing_branch_for_issue

        existing_branch = find_existing_branch_for_issue(issue_id, adw_id)

        if existing_branch:
            logger.info(f"Found existing branch: {existing_branch}")
            branch_name = existing_branch
        else:
            # 3. No existing branch, need to classify and generate name
            logger.info("No existing branch found, creating new one")

            # Classify the issue - use minimal dict for agent
            from adws.adw_modules.workflow_ops import classify_issue

            issue_command, error = classify_issue(issue.to_minimal_dict(), adw_id, logger)
            if error:
                logger.error(f"Failed to classify issue: {error}")
                notify_issue(issue, adw_id, "ops", f"❌ Failed to classify issue: {error}", logger)
                sys.exit(1)

            state.update(issue_class=issue_command)

            # Generate branch name - use minimal dict for agent
            from adws.adw_modules.workflow_ops import generate_branch_name

            branch_name, error = generate_branch_name(
                issue.to_minimal_dict(), issue_command, adw_id, logger
            )
            if error:
                logger.error(f"Error generating branch name: {error}")
                notify_issue(issue, adw_id, "ops", f"❌ Error generating branch name: {error}", logger)
                sys.exit(1)

    # Update state with branch name
    state.update(branch_name=branch_name)

    # Save state with branch name
    state.save("adw_patch_iso")
    logger.info(f"Working on branch: {branch_name}")
    notify_issue(issue, adw_id, "ops", f"✅ Working on branch: {branch_name}", logger)

    # Check if worktree already exists
    worktree_path = state.get("worktree_path")
    if worktree_path and os.path.exists(worktree_path):
        logger.info(f"Using existing worktree: {worktree_path}")
        backend_port = state.get("backend_port", 9100)
        frontend_port = state.get("frontend_port", 9200)
    else:
        # Create isolated worktree
        logger.info("Creating isolated worktree")
        worktree_path, error = create_worktree(adw_id, branch_name, logger)

        if error:
            logger.error(f"Error creating worktree: {error}")
            notify_issue(issue, adw_id, "ops", f"❌ Error creating worktree: {error}", logger)
            sys.exit(1)

        # Get deterministic ports for this ADW ID
        backend_port, frontend_port = get_ports_for_adw(adw_id)

        # Check if ports are available, find alternatives if not
        if not is_port_available(backend_port) or not is_port_available(frontend_port):
            logger.warning(
                f"Preferred ports {backend_port}/{frontend_port} not available, finding alternatives"
            )
            backend_port, frontend_port = find_next_available_ports(adw_id)

        logger.info(
            f"Allocated ports - Backend: {backend_port}, Frontend: {frontend_port}"
        )

        # Clean up stale worktree config files from main repo
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cleanup_worktree_config_files(project_root, logger)

        # Set up worktree environment (copy files, create .ports.env)
        setup_worktree_environment(worktree_path, backend_port, frontend_port, logger)

        # Update state with worktree info
        state.update(
            worktree_path=worktree_path,
            backend_port=backend_port,
            frontend_port=frontend_port,
        )
        state.save("adw_patch_iso")

    notify_issue(
        issue, adw_id, "ops",
        f"✅ Using isolated worktree\n"
        f"🏠 Path: {worktree_path}\n"
        f"🔌 Ports - Backend: {backend_port}, Frontend: {frontend_port}",
        logger,
    )

    notify_issue(
        issue, adw_id, "ops",
        f"🔍 Using state\n```json\n{json.dumps(state.data, indent=2)}\n```",
        logger,
    )

    # Get patch content from issue based on source
    logger.info("Getting patch content from issue")
    review_change_request = get_patch_content(issue, adw_id, logger, repo_path=repo_path)

    # Use the shared method to create and implement patch
    patch_file, implement_response = create_and_implement_patch(
        adw_id=adw_id,
        review_change_request=review_change_request,
        logger=logger,
        agent_name_planner=AGENT_PATCH_PLANNER,
        agent_name_implementor=AGENT_PATCH_IMPLEMENTOR,
        spec_path=None,  # No spec file for direct issue patches
        working_dir=worktree_path,  # Pass worktree path for isolated execution
    )

    if not patch_file:
        logger.error("Failed to create patch plan")
        notify_issue(issue, adw_id, AGENT_PATCH_PLANNER, "❌ Failed to create patch plan", logger)
        sys.exit(1)

    state.update(patch_file=patch_file)
    state.save("adw_patch_iso")
    logger.info(f"Patch plan created: {patch_file}")
    notify_issue(issue, adw_id, AGENT_PATCH_PLANNER, f"✅ Patch plan created: {patch_file}", logger)

    if not implement_response.success:
        logger.error(f"Error implementing patch: {implement_response.output}")
        notify_issue(issue, adw_id, AGENT_PATCH_IMPLEMENTOR, f"❌ Error implementing patch: {implement_response.output}", logger)
        sys.exit(1)

    logger.debug(f"Implementation response: {implement_response.output}")
    notify_issue(issue, adw_id, AGENT_PATCH_IMPLEMENTOR, "✅ Patch implemented", logger)

    # Create commit message
    logger.info("Creating patch commit")

    issue_command = "/patch"
    commit_msg, error = create_commit(
        AGENT_PATCH_IMPLEMENTOR, issue.to_minimal_dict(), issue_command, adw_id, logger, worktree_path
    )

    if error:
        logger.error(f"Error creating commit message: {error}")
        notify_issue(issue, adw_id, AGENT_PATCH_IMPLEMENTOR, f"❌ Error creating commit message: {error}", logger)
        sys.exit(1)

    # Commit the patch (in worktree)
    success, error = commit_changes(commit_msg, cwd=worktree_path)

    if not success:
        logger.error(f"Error committing patch: {error}")
        notify_issue(issue, adw_id, AGENT_PATCH_IMPLEMENTOR, f"❌ Error committing patch: {error}", logger)
        sys.exit(1)

    logger.info(f"Committed patch: {commit_msg}")
    notify_issue(issue, adw_id, AGENT_PATCH_IMPLEMENTOR, "✅ Patch committed", logger)

    logger.info("Finalizing git operations")
    notify_issue(issue, adw_id, "ops", "🔧 Finalizing git operations", logger)

    # Finalize git operations (push and PR) - passing cwd for worktree
    finalize_git_operations(state, logger, cwd=worktree_path)

    # Update issue status to resolved
    update_issue_status(issue, IssueStatus.RESOLVED, "Isolated patch workflow completed", adw_id, logger)

    logger.info("Isolated patch workflow completed successfully")
    notify_issue(issue, adw_id, "ops", "✅ Isolated patch workflow completed", logger)

    # Save final state
    state.save("adw_patch_iso")

    # Post final state summary to issue
    notify_issue(
        issue, adw_id, "ops",
        f"📋 Final isolated patch state:\n```json\n{json.dumps(state.data, indent=2)}\n```",
        logger,
    )


if __name__ == "__main__":
    main()
