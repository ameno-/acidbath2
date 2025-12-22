#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml"]
# ///

"""
ADW Plan Iso - AI Developer Workflow for agentic planning in isolated worktrees

Usage:
  uv run adw_plan_iso.py <issue-ref> [adw-id] [--dry-run]

Issue References:
  123                - GitHub issue #123
  github:123         - GitHub issue (explicit)
  local:fix-bug      - Local issue (issues/issue-fix-bug.md)
  prompt:Fix bug     - Ephemeral prompt-based issue

Workflow:
1. Resolve issue from source (GitHub, GitLab, Local, Prompt)
2. Check/create worktree for isolated execution
3. Allocate unique ports for services
4. Setup worktree environment
5. Classify issue type (/chore, /bug, /feature)
6. Create feature branch in worktree
7. Generate implementation plan in worktree
8. Commit plan in worktree
9. Push and create/update PR/MR (GitHub/GitLab)

This workflow creates an isolated git worktree under trees/<adw_id>/ for
parallel execution without interference.
"""

import sys
import os
import logging
import json
import re
from typing import Optional
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.state import ADWState
from adws.adw_modules.git_ops import (
    commit_changes,
    push_branch,
    check_pr_exists,
    get_current_branch,
)
from adws.adw_modules.workflow_ops import (
    classify_issue,
    build_plan,
    generate_branch_name,
    create_commit,
    format_issue_message,
    ensure_adw_id,
    create_pull_request,
    AGENT_PLANNER,
)
from adws.adw_modules.utils import setup_logger, check_env_vars
from adws.adw_modules.data_types import Issue, IssueSource, AgentTemplateRequest
from adws.adw_modules.agent import execute_template
from adws.adw_modules.worktree_ops import (
    create_worktree,
    validate_worktree,
    get_ports_for_adw,
    is_port_available,
    find_next_available_ports,
    setup_worktree_environment,
    cleanup_worktree_config_files,
)
from adws.adw_modules.issue_providers import (
    resolve_issue,
    get_provider_for_issue,
    IssueProvider,
)
from adws.adw_modules.code_review_providers import GitLabCodeReviewProvider


def extract_plan_path(output: str, worktree_path: str) -> Optional[str]:
    """Extract the plan file path from command output.

    Handles both absolute paths and relative paths.
    Returns a path relative to the worktree if found.

    Args:
        output: The command output text
        worktree_path: The worktree directory path

    Returns:
        The plan file path relative to worktree, or None if not found
    """
    # Pattern to match specs/*.md files (any type: chore, feature, bug, etc.)
    # Matches both relative and absolute paths
    patterns = [
        # Absolute path containing specs/
        r'[`"\']?(/[^\s`"\']+/specs/[a-zA-Z0-9_\-]+\.md)[`"\']?',
        # Relative path specs/
        r'[`"\']?(specs/[a-zA-Z0-9_\-]+\.md)[`"\']?',
    ]

    for pattern in patterns:
        match = re.search(pattern, output, re.MULTILINE)
        if match:
            found_path = match.group(1)

            # If it's an absolute path, make it relative to worktree
            if found_path.startswith('/'):
                # Check if the path is within the worktree (possibly nested)
                if worktree_path in found_path:
                    # Get the part after worktree_path
                    relative_part = found_path[len(worktree_path):].lstrip('/')
                    return relative_part
                # Otherwise just get the specs/ part
                specs_idx = found_path.find('specs/')
                if specs_idx >= 0:
                    return found_path[specs_idx:]

            return found_path

    return None


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse command line args
    if len(sys.argv) < 2:
        print("Usage: uv run adw_plan_iso.py <issue-ref> [adw-id] [--dry-run]")
        print("")
        print("Issue references:")
        print("  123              - GitHub issue #123")
        print("  github:123       - GitHub issue (explicit)")
        print("  local:fix-bug    - Local issue in issues/issue-fix-bug.md")
        print("  prompt:Fix bug   - Ephemeral prompt-based issue")
        sys.exit(1)

    issue_ref = sys.argv[1]
    adw_id = None
    dry_run = False

    # Parse optional arguments
    for arg in sys.argv[2:]:
        if arg == "--dry-run":
            dry_run = True
        else:
            adw_id = arg

    # Dry-run mode: exit early with minimal operations (no network calls)
    if dry_run:
        # Generate placeholder ADW ID if not provided
        if not adw_id:
            import uuid
            adw_id = uuid.uuid4().hex[:8]

        print("[DRY RUN] Would execute isolated planning workflow:")
        print(f"  - Issue ref: {issue_ref}")
        print(f"  - ADW ID: {adw_id}")
        print(f"  - Create worktree at: trees/{adw_id}/")
        print(f"  - Resolve issue from source")
        print(f"  - Classify issue type")
        print(f"  - Generate branch name")
        print(f"  - Build implementation plan")
        print(f"  - Commit and push to PR (if applicable)")
        return

    # Ensure ADW ID exists with initialized state
    temp_logger = setup_logger(adw_id, "adw_plan_iso") if adw_id else None
    adw_id = ensure_adw_id(issue_ref, adw_id, temp_logger)

    # Load the state that was created/found by ensure_adw_id
    state = ADWState.load(adw_id, temp_logger)

    # Ensure state has the adw_id field
    if not state.get("adw_id"):
        state.update(adw_id=adw_id)

    # Track that this ADW workflow has run
    state.append_adw_id("adw_plan_iso")

    # Set up logger with ADW ID
    logger = setup_logger(adw_id, "adw_plan_iso")
    logger.info(f"ADW Plan Iso starting - ID: {adw_id}, Issue ref: {issue_ref}")

    # Validate environment
    check_env_vars(logger)

    # Resolve issue from any supported source (GitHub, Local, Prompt)
    try:
        issue: Issue = resolve_issue(issue_ref)
        logger.info(f"Resolved issue from {issue.source.value}: {issue.title}")
    except Exception as e:
        logger.error(f"Error resolving issue: {e}")
        sys.exit(1)

    # Get the provider for this issue (for comments/updates)
    provider: IssueProvider = get_provider_for_issue(issue)

    # Store issue source info in state
    state.update(
        issue_number=issue.id,
        issue_source=issue.source.value,
        issue_ref=issue.source_ref or issue_ref,
    )
    state.save("adw_plan_iso")

    # Check if worktree already exists
    valid, error = validate_worktree(adw_id, state)
    if valid:
        logger.info(f"Using existing worktree for {adw_id}")
        worktree_path = state.get("worktree_path")
        backend_port = state.get("backend_port")
        frontend_port = state.get("frontend_port")
    else:
        # Allocate ports for this instance
        backend_port, frontend_port = get_ports_for_adw(adw_id)

        # Check port availability
        if not (is_port_available(backend_port) and is_port_available(frontend_port)):
            logger.warning(f"Deterministic ports {backend_port}/{frontend_port} are in use, finding alternatives")
            backend_port, frontend_port = find_next_available_ports(adw_id)

        logger.info(f"Allocated ports - Backend: {backend_port}, Frontend: {frontend_port}")
        state.update(backend_port=backend_port, frontend_port=frontend_port)
        state.save("adw_plan_iso")

    # Issue already resolved above - log details and notify
    logger.debug(f"Issue details: {issue.model_dump_json(indent=2)}")
    provider.add_comment(
        issue, format_issue_message(adw_id, "ops", "✅ Starting isolated planning phase"), adw_id
    )

    provider.add_comment(
        issue,
        f"{adw_id}_ops: 🔍 Using state\n```json\n{json.dumps(state.data, indent=2)}\n```",
        adw_id,
    )

    # Classify the issue
    issue_command, error = classify_issue(issue.to_minimal_dict(), adw_id, logger)

    if error:
        logger.error(f"Error classifying issue: {error}")
        provider.add_comment(
            issue,
            format_issue_message(adw_id, "ops", f"❌ Error classifying issue: {error}"),
            adw_id,
        )
        sys.exit(1)

    state.update(issue_class=issue_command)
    state.save("adw_plan_iso")
    logger.info(f"Issue classified as: {issue_command}")
    provider.add_comment(
        issue,
        format_issue_message(adw_id, "ops", f"✅ Issue classified as: {issue_command}"),
        adw_id,
    )

    # Generate branch name
    branch_name, error = generate_branch_name(issue.to_minimal_dict(), issue_command, adw_id, logger)

    if error:
        logger.error(f"Error generating branch name: {error}")
        provider.add_comment(
            issue,
            format_issue_message(
                adw_id, "ops", f"❌ Error generating branch name: {error}"
            ),
            adw_id,
        )
        sys.exit(1)

    # Don't create branch here - let worktree create it
    # The worktree command will create the branch when we specify -b
    state.update(branch_name=branch_name)
    state.save("adw_plan_iso")
    logger.info(f"Will create branch in worktree: {branch_name}")

    # Create worktree if it doesn't exist
    if not valid:
        logger.info(f"Creating worktree for {adw_id}")
        worktree_path, error = create_worktree(adw_id, branch_name, logger)

        if error:
            logger.error(f"Error creating worktree: {error}")
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"❌ Error creating worktree: {error}"),
                adw_id,
            )
            sys.exit(1)

        state.update(worktree_path=worktree_path)
        state.save("adw_plan_iso")
        logger.info(f"Created worktree at {worktree_path}")

        # Clean up stale worktree config files from main repo
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cleanup_worktree_config_files(project_root, logger)

        # Setup worktree environment (create .ports.env)
        setup_worktree_environment(worktree_path, backend_port, frontend_port, logger)

        # Run install_worktree command to set up the isolated environment
        logger.info("Setting up isolated environment with custom ports")
        install_request = AgentTemplateRequest(
            agent_name="ops",
            slash_command="/install_worktree",
            args=[worktree_path, str(backend_port), str(frontend_port)],
            adw_id=adw_id,
            working_dir=worktree_path,  # Execute in worktree
        )

        install_response = execute_template(install_request)
        if not install_response.success:
            logger.error(f"Error setting up worktree: {install_response.output}")
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"❌ Error setting up worktree: {install_response.output}"),
                adw_id,
            )
            sys.exit(1)

        logger.info("Worktree environment setup complete")

    provider.add_comment(
        issue,
        format_issue_message(adw_id, "ops", f"✅ Working in isolated worktree: {worktree_path}\n"
                           f"🔌 Ports - Backend: {backend_port}, Frontend: {frontend_port}"),
        adw_id,
    )

    # Build the implementation plan (now executing in worktree)
    logger.info("Building implementation plan in worktree")
    provider.add_comment(
        issue,
        format_issue_message(adw_id, AGENT_PLANNER, "✅ Building implementation plan in isolated environment"),
        adw_id,
    )

    plan_response = build_plan(issue.to_minimal_dict(), issue_command, adw_id, logger, working_dir=worktree_path)

    if not plan_response.success:
        logger.error(f"Error building plan: {plan_response.output}")
        provider.add_comment(
            issue,
            format_issue_message(
                adw_id, AGENT_PLANNER, f"❌ Error building plan: {plan_response.output}"
            ),
            adw_id,
        )
        sys.exit(1)

    logger.debug(f"Plan response: {plan_response.output}")
    provider.add_comment(
        issue,
        format_issue_message(adw_id, AGENT_PLANNER, "✅ Implementation plan created"),
        adw_id,
    )

    # Get the plan file path from response using regex extraction
    logger.info("Getting plan file path")
    plan_file_path = extract_plan_path(plan_response.output, worktree_path)

    # Validate we found a path
    if not plan_file_path:
        error = f"Could not extract plan file path from output: {plan_response.output[:200]}..."
        logger.error(error)
        provider.add_comment(
            issue,
            format_issue_message(adw_id, "ops", f"❌ {error}"),
            adw_id,
        )
        sys.exit(1)

    # Check if file exists in worktree
    worktree_plan_path = os.path.join(worktree_path, plan_file_path)
    if not os.path.exists(worktree_plan_path):
        error = f"Plan file does not exist in worktree: {plan_file_path} (full: {worktree_plan_path})"
        logger.error(error)
        provider.add_comment(
            issue,
            format_issue_message(adw_id, "ops", f"❌ {error}"),
            adw_id,
        )
        sys.exit(1)

    state.update(plan_file=plan_file_path)
    state.save("adw_plan_iso")
    logger.info(f"Plan file created: {plan_file_path}")
    provider.add_comment(
        issue,
        format_issue_message(adw_id, "ops", f"✅ Plan file created: {plan_file_path}"),
        adw_id,
    )

    # Create commit message
    logger.info("Creating plan commit")
    commit_msg, error = create_commit(
        AGENT_PLANNER, issue.to_minimal_dict(), issue_command, adw_id, logger, worktree_path
    )

    if error:
        logger.error(f"Error creating commit message: {error}")
        provider.add_comment(
            issue,
            format_issue_message(
                adw_id, AGENT_PLANNER, f"❌ Error creating commit message: {error}"
            ),
            adw_id,
        )
        sys.exit(1)

    # Commit the plan (in worktree)
    success, error = commit_changes(commit_msg, cwd=worktree_path)

    if not success:
        logger.error(f"Error committing plan: {error}")
        provider.add_comment(
            issue,
            format_issue_message(
                adw_id, AGENT_PLANNER, f"❌ Error committing plan: {error}"
            ),
            adw_id,
        )
        sys.exit(1)

    logger.info(f"Committed plan: {commit_msg}")
    provider.add_comment(
        issue, format_issue_message(adw_id, AGENT_PLANNER, "✅ Plan committed"), adw_id
    )

    # Finalize git operations (push and PR)
    # Note: This will work from the worktree context
    logger.info("Finalizing git operations: push and PR")

    # Push the branch and create PR/MR (for remote issues, skip for local/prompt)
    if issue.source == IssueSource.GITHUB:
        success, error = push_branch(branch_name, cwd=worktree_path)
        if not success:
            logger.error(f"Failed to push branch: {error}")
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"❌ Failed to push branch: {error}"),
                adw_id,
            )
        else:
            logger.info(f"Pushed branch: {branch_name}")

            # Handle PR
            pr_url = check_pr_exists(branch_name, cwd=worktree_path)

            if pr_url:
                logger.info(f"Found existing PR: {pr_url}")
                provider.add_comment(issue, f"{adw_id}_ops: ✅ Pull request: {pr_url}", adw_id)
            else:
                # Create new PR
                logger.info("Creating new pull request")
                pr_url, error = create_pull_request(branch_name, issue.to_minimal_dict(), state, logger, worktree_path)

                if error:
                    logger.error(f"Failed to create PR: {error}")
                    provider.add_comment(
                        issue,
                        format_issue_message(adw_id, "ops", f"❌ Failed to create PR: {error}"),
                        adw_id,
                    )
                elif pr_url:
                    logger.info(f"Created PR: {pr_url}")
                    state.update(pr_url=pr_url)
                    state.save("adw_plan_iso")
                    provider.add_comment(issue, f"{adw_id}_ops: ✅ Pull request created: {pr_url}", adw_id)
    elif issue.source == IssueSource.GITLAB:
        # Handle GitLab issues - push and create MR
        success, error = push_branch(branch_name, cwd=worktree_path)
        if not success:
            logger.error(f"Failed to push branch to GitLab: {error}")
            provider.add_comment(
                issue,
                format_issue_message(adw_id, "ops", f"❌ Failed to push branch: {error}"),
                adw_id,
            )
        else:
            logger.info(f"Pushed branch to GitLab: {branch_name}")

            # Handle MR using GitLabCodeReviewProvider
            gitlab_provider = GitLabCodeReviewProvider(project_path=issue.repo_path, logger=logger)
            existing_mr = gitlab_provider.check_exists(branch_name, cwd=worktree_path)

            if existing_mr:
                logger.info(f"Found existing MR: {existing_mr.url}")
                state.update(mr_url=existing_mr.url)
                state.save("adw_plan_iso")
                provider.add_comment(issue, f"{adw_id}_ops: ✅ Merge request: {existing_mr.url}", adw_id)
            else:
                # Create new MR
                logger.info("Creating new merge request")
                mr_title = f"[{adw_id}] {issue.title}"
                mr_body = f"Implementation plan for issue #{issue.id}\n\n{AGENT_PLANNER}: Plan created in isolated worktree."

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
                    state.save("adw_plan_iso")
                    provider.add_comment(issue, f"{adw_id}_ops: ✅ Merge request created: {mr.url}", adw_id)
    else:
        # For local/prompt issues, just log completion (branch stays local)
        logger.info(f"Local/prompt issue - branch {branch_name} created locally only")

    logger.info("Isolated planning phase completed successfully")
    provider.add_comment(
        issue, format_issue_message(adw_id, "ops", "✅ Isolated planning phase completed"), adw_id
    )

    # Save final state
    state.save("adw_plan_iso")

    # Post final state summary to issue
    provider.add_comment(
        issue,
        f"{adw_id}_ops: 📋 Final planning state:\n```json\n{json.dumps(state.data, indent=2)}\n```",
        adw_id,
    )


if __name__ == "__main__":
    main()
