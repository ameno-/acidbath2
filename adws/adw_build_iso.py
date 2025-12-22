#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml"]
# ///

"""
ADW Build Iso - AI Developer Workflow for agentic building in isolated worktrees

Usage:
  uv run adw_build_iso.py <issue-ref> <adw-id> [--dry-run]

Issue References:
  123                - GitHub issue #123
  github:123         - GitHub issue (explicit)
  local:fix-bug      - Local issue (issues/issue-fix-bug.md)
  prompt:Fix bug     - Ephemeral prompt-based issue

Workflow:
1. Load state and validate worktree exists
2. Find existing plan (from state)
3. Implement the solution based on plan in worktree
4. Commit implementation in worktree
5. Push and update PR/MR (GitHub/GitLab)

This workflow REQUIRES that adw_plan_iso.py or adw_patch_iso.py has been run first
to create the worktree. It cannot create worktrees itself.

Arguments:
  issue-ref: Issue reference (GitHub, local, or prompt)
  adw-id: Agentic Deployment Workflow ID (used to locate worktree and state)
  --dry-run: Validate inputs and show what would be done without executing
"""

import sys
import os
import logging
import json
import subprocess
from typing import Optional
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.state import ADWState
from adws.adw_modules.git_ops import commit_changes, push_branch, check_pr_exists, get_current_branch
from adws.adw_modules.workflow_ops import (
    implement_plan,
    implement_plan_with_tracking,
    create_commit,
    classify_issue,
    format_issue_message,
    AGENT_IMPLEMENTOR,
)
from adws.adw_modules.utils import setup_logger, check_env_vars
from adws.adw_modules.data_types import Issue, IssueSource
from adws.adw_modules.worktree_ops import validate_worktree
from adws.adw_modules.issue_providers import (
    resolve_issue,
    get_provider_for_issue,
    IssueProvider,
)
from adws.adw_modules.code_review_providers import GitLabCodeReviewProvider


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse command line args
    # INTENTIONAL: adw-id is REQUIRED - we need it to find the worktree
    dry_run = "--dry-run" in sys.argv
    use_tracked = "--tracked" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ("--dry-run", "--tracked")]

    if len(args) < 2:
        print("Usage: uv run adw_build_iso.py <issue-ref> <adw-id> [--dry-run] [--tracked]")
        print("")
        print("Issue references:")
        print("  123              - GitHub issue #123")
        print("  github:123       - GitHub issue (explicit)")
        print("  local:fix-bug    - Local issue in issues/issue-fix-bug.md")
        print("  prompt:Fix bug   - Ephemeral prompt-based issue")
        print("\nError: adw-id is required to locate the worktree and plan file")
        print("Run adw_plan_iso.py or adw_patch_iso.py first to create the worktree")
        print("\nOptions:")
        print("  --dry-run    Validate without executing (show what would be done)")
        print("  --tracked    Use step-level tracking with parallel group support")
        sys.exit(1)

    issue_ref = args[0]
    adw_id = args[1]

    # Dry-run mode: exit early with minimal operations (no network calls)
    if dry_run:
        print("[DRY RUN] Would execute isolated build workflow:")
        print(f"  - Issue ref: {issue_ref}")
        print(f"  - ADW ID: {adw_id}")
        print(f"  - Tracked mode: {use_tracked}")
        print(f"  - Load state from: agents/{adw_id}/adw_state.json")
        print(f"  - Validate worktree exists")
        print(f"  - Implement plan from state")
        print(f"  - Commit changes to branch")
        print(f"  - Push branch and update PR (if applicable)")
        return

    # Try to load existing state
    temp_logger = setup_logger(adw_id, "adw_build_iso")
    state = ADWState.load(adw_id, temp_logger)
    if not state:
        # No existing state found
        logger = setup_logger(adw_id, "adw_build_iso")
        logger.error(f"No state found for ADW ID: {adw_id}")
        logger.error("Run adw_plan_iso.py first to create the worktree and state")
        print(f"\nError: No state found for ADW ID: {adw_id}")
        print("Run adw_plan_iso.py first to create the worktree and state")
        sys.exit(1)

    # Found existing state - use the issue ref from state if available
    stored_issue_ref = state.get("issue_ref", issue_ref)

    # Track that this ADW workflow has run
    state.append_adw_id("adw_build_iso")

    # Set up logger with ADW ID from command line
    logger = setup_logger(adw_id, "adw_build_iso")
    logger.info(f"ADW Build Iso starting - ID: {adw_id}, Issue ref: {stored_issue_ref}")

    # Validate environment
    check_env_vars(logger)

    # Resolve issue from any supported source (GitHub, Local, Prompt)
    try:
        issue: Issue = resolve_issue(stored_issue_ref)
        logger.info(f"Resolved issue from {issue.source.value}: {issue.title}")
    except Exception as e:
        logger.error(f"Error resolving issue: {e}")
        sys.exit(1)

    # Get the provider for this issue (for comments/updates)
    provider: IssueProvider = get_provider_for_issue(issue)

    provider.add_comment(
        issue,
        f"{adw_id}_ops: 🔍 Found existing state - resuming isolated build\n```json\n{json.dumps(state.data, indent=2)}\n```",
        adw_id,
    )

    # Validate worktree exists
    valid, error = validate_worktree(adw_id, state)
    if not valid:
        logger.error(f"Worktree validation failed: {error}")
        logger.error("Run adw_plan_iso.py or adw_patch_iso.py first")
        provider.add_comment(
            issue,
            format_issue_message(adw_id, "ops", f"❌ Worktree validation failed: {error}\n"
                               "Run adw_plan_iso.py or adw_patch_iso.py first"),
            adw_id,
        )
        sys.exit(1)

    # Get worktree path for explicit context
    worktree_path = state.get("worktree_path")
    logger.info(f"Using worktree at: {worktree_path}")

    # Ensure we have required state fields
    if not state.get("branch_name"):
        error_msg = "No branch name in state - run adw_plan_iso.py first"
        logger.error(error_msg)
        provider.add_comment(
            issue,
            format_issue_message(adw_id, "ops", f"❌ {error_msg}"),
            adw_id,
        )
        sys.exit(1)

    if not state.get("plan_file"):
        error_msg = "No plan file in state - run adw_plan_iso.py first"
        logger.error(error_msg)
        provider.add_comment(
            issue,
            format_issue_message(adw_id, "ops", f"❌ {error_msg}"),
            adw_id,
        )
        sys.exit(1)

    # Get branch and plan info
    branch_name = state.get("branch_name")
    plan_file = state.get("plan_file")
    backend_port = state.get("backend_port", "N/A")
    frontend_port = state.get("frontend_port", "N/A")

    # Checkout the branch in the worktree
    result = subprocess.run(["git", "checkout", branch_name], capture_output=True, text=True, cwd=worktree_path)
    if result.returncode != 0:
        logger.error(f"Failed to checkout branch {branch_name} in worktree: {result.stderr}")
        provider.add_comment(
            issue,
            format_issue_message(adw_id, "ops", f"❌ Failed to checkout branch {branch_name} in worktree"),
            adw_id,
        )
        sys.exit(1)
    logger.info(f"Checked out branch in worktree: {branch_name}")

    logger.info(f"Using plan file: {plan_file}")

    provider.add_comment(
        issue,
        format_issue_message(adw_id, "ops", f"✅ Starting isolated implementation phase\n"
                           f"🏠 Worktree: {worktree_path}\n"
                           f"🔌 Ports - Backend: {backend_port}, Frontend: {frontend_port}"),
        adw_id,
    )

    # Implement the plan (executing in worktree)
    logger.info("Implementing solution in worktree")

    # Get model strategy from state (defaults to "auto")
    model_strategy = state.get("model_strategy") or "auto"

    if use_tracked:
        logger.info(f"Using tracked implementation with model_strategy={model_strategy}")
        provider.add_comment(
            issue,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution with step tracking in isolated environment"),
            adw_id,
        )
        implement_response = implement_plan_with_tracking(
            plan_file=plan_file,
            adw_id=adw_id,
            logger=logger,
            working_dir=worktree_path,
            max_concurrent=3,
            model_strategy=model_strategy,
        )
    else:
        provider.add_comment(
            issue,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution in isolated environment"),
            adw_id,
        )
        implement_response = implement_plan(plan_file, adw_id, logger, working_dir=worktree_path)

    if not implement_response.success:
        logger.error(f"Error implementing solution: {implement_response.output}")
        provider.add_comment(
            issue,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, f"❌ Error implementing solution: {implement_response.output}"),
            adw_id,
        )
        sys.exit(1)

    logger.debug(f"Implementation response: {implement_response.output}")
    provider.add_comment(
        issue,
        format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Solution implemented"),
        adw_id,
    )

    # Get issue classification from state or classify if needed
    issue_command = state.get("issue_class")
    if not issue_command:
        logger.info("No issue classification in state, running classify_issue")
        issue_command, cls_error = classify_issue(issue.to_minimal_dict(), adw_id, logger)
        if cls_error:
            logger.error(f"Error classifying issue: {cls_error}")
            # Default to feature if classification fails
            issue_command = "/feature"
            logger.warning("Defaulting to /feature after classification error")
        else:
            # Save the classification for future use
            state.update(issue_class=issue_command)
            state.save("adw_build_iso")

    # Create commit message
    logger.info("Creating implementation commit")
    commit_msg, error = create_commit(AGENT_IMPLEMENTOR, issue.to_minimal_dict(), issue_command, adw_id, logger, worktree_path)

    if error:
        logger.error(f"Error creating commit message: {error}")
        provider.add_comment(
            issue,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, f"❌ Error creating commit message: {error}"),
            adw_id,
        )
        sys.exit(1)

    # Commit the implementation (in worktree)
    success, error = commit_changes(commit_msg, cwd=worktree_path)

    if not success:
        logger.error(f"Error committing implementation: {error}")
        provider.add_comment(
            issue,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, f"❌ Error committing implementation: {error}"),
            adw_id,
        )
        sys.exit(1)

    logger.info(f"Committed implementation: {commit_msg}")
    provider.add_comment(
        issue, format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementation committed"), adw_id
    )

    # Finalize git operations (push and PR/MR) - for remote issues
    if issue.source == IssueSource.GITHUB:
        logger.info(f"Pushing branch: {branch_name}")
        push_success, push_error = push_branch(branch_name, cwd=worktree_path)
        if not push_success:
            logger.error(f"Failed to push branch: {push_error}")
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"❌ Failed to push branch: {push_error}"),
                adw_id,
            )
            sys.exit(1)

        logger.info(f"Branch pushed successfully: {branch_name}")

        # Check if PR exists, if not create one
        pr_url = check_pr_exists(branch_name, cwd=worktree_path)
        if pr_url:
            logger.info(f"PR already exists: {pr_url}")
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"✅ Updated existing PR: {pr_url}"),
                adw_id,
            )
        else:
            logger.info("Creating new PR")
            # Create PR using gh CLI
            pr_title = f"Fix #{issue.id}: {issue.title}"
            pr_body = f"Fixes #{issue.id}\n\nImplementation completed in isolated worktree."

            result = subprocess.run(
                ["gh", "pr", "create", "--title", pr_title, "--body", pr_body],
                capture_output=True,
                text=True,
                cwd=worktree_path
            )

            if result.returncode == 0:
                pr_url = result.stdout.strip()
                logger.info(f"Created PR: {pr_url}")
                provider.add_comment(
                    issue,
                    format_issue_message(adw_id, "ops", f"✅ Created PR: {pr_url}"),
                    adw_id,
                )
                # Save PR URL to state
                state.update(pr_url=pr_url)
            else:
                logger.error(f"Failed to create PR: {result.stderr}")
                provider.add_comment(
                    issue,
                    format_issue_message(adw_id, "ops", f"❌ Failed to create PR: {result.stderr}"),
                    adw_id,
                )
    elif issue.source == IssueSource.GITLAB:
        # Handle GitLab issues - push and create/update MR
        logger.info(f"Pushing branch to GitLab: {branch_name}")
        push_success, push_error = push_branch(branch_name, cwd=worktree_path)
        if not push_success:
            logger.error(f"Failed to push branch to GitLab: {push_error}")
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"❌ Failed to push branch: {push_error}"),
                adw_id,
            )
            sys.exit(1)

        logger.info(f"Branch pushed to GitLab successfully: {branch_name}")

        # Handle MR using GitLabCodeReviewProvider
        gitlab_provider = GitLabCodeReviewProvider(project_path=issue.repo_path, logger=logger)
        existing_mr = gitlab_provider.check_exists(branch_name, cwd=worktree_path)

        if existing_mr:
            logger.info(f"MR already exists: {existing_mr.url}")
            state.update(mr_url=existing_mr.url)
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"✅ Updated existing MR: {existing_mr.url}"),
                adw_id,
            )
        else:
            logger.info("Creating new MR")
            mr_title = f"[{adw_id}] Fix #{issue.id}: {issue.title}"
            mr_body = f"Closes #{issue.id}\n\n{AGENT_IMPLEMENTOR}: Implementation completed in isolated worktree."

            mr, error = gitlab_provider.create(
                branch_name=branch_name,
                title=mr_title,
                body=mr_body,
                issue=issue,
                cwd=worktree_path,
            )

            if error:
                logger.error(f"Failed to create MR: {error}")
                provider.add_comment(
                    issue,
                    format_issue_message(adw_id, "ops", f"❌ Failed to create MR: {error}"),
                    adw_id,
                )
            elif mr:
                logger.info(f"Created MR: {mr.url}")
                state.update(mr_url=mr.url)
                provider.add_comment(
                    issue,
                    format_issue_message(adw_id, "ops", f"✅ Created MR: {mr.url}"),
                    adw_id,
                )
    else:
        # For local/prompt issues, just log completion (branch stays local)
        logger.info(f"Local/prompt issue - branch {branch_name} stays local")

    logger.info("Isolated implementation phase completed successfully")
    provider.add_comment(
        issue, format_issue_message(adw_id, "ops", "✅ Isolated implementation phase completed"), adw_id
    )

    # Save final state
    state.save("adw_build_iso")

    # Post final state summary to issue
    provider.add_comment(
        issue,
        f"{adw_id}_ops: 📋 Final build state:\n```json\n{json.dumps(state.data, indent=2)}\n```",
        adw_id,
    )


if __name__ == "__main__":
    main()
