"""Shared AI Developer Workflow (ADW) operations - deployment-agnostic."""

import glob
import json
import logging
import os
import subprocess
import re
from typing import Tuple, Optional, Dict, Any, List
from .data_types import (
    AgentTemplateRequest,
    AgentPromptResponse,
    ADWExtractionResult,
)
from .agent import execute_template
from .state import ADWState


# Agent name constants - can be extended by deployment-specific modules
AGENT_PLANNER = "sdlc_planner"
AGENT_IMPLEMENTOR = "sdlc_implementor"
AGENT_CLASSIFIER = "issue_classifier"
AGENT_BRANCH_GENERATOR = "branch_generator"
AGENT_PR_CREATOR = "pr_creator"

# Bot identifier for preventing webhook loops - can be overridden
ADW_BOT_IDENTIFIER = "[ADW_BOT]"

# Available ADW workflows for runtime validation - can be extended
AVAILABLE_ADW_WORKFLOWS = [
    # Isolated workflows (all workflows are now iso-based)
    "adw_plan_iso",
    "adw_patch_iso",
    "adw_build_iso",
    "adw_test_iso",
    "adw_review_iso",
    "adw_document_iso",
    "adw_ship_iso",
    "adw_sdlc_ZTE_iso",  # Zero Touch Execution workflow
    "adw_plan_build_iso",
    "adw_plan_build_test_iso",
    "adw_plan_build_test_review_iso",
    "adw_plan_build_document_iso",
    "adw_plan_build_review_iso",
    "adw_sdlc_iso",
]


def format_issue_message(
    adw_id: str, agent_name: str, message: str, session_id: Optional[str] = None
) -> str:
    """Format a message for issue comments with ADW tracking and bot identifier."""
    # Always include ADW_BOT_IDENTIFIER to prevent webhook loops
    if session_id:
        return f"{ADW_BOT_IDENTIFIER} {adw_id}_{agent_name}_{session_id}: {message}"
    return f"{ADW_BOT_IDENTIFIER} {adw_id}_{agent_name}: {message}"


def extract_adw_info(text: str, temp_adw_id: str) -> ADWExtractionResult:
    """Extract ADW workflow, ID, and model_set from text using classify_adw agent.
    Returns ADWExtractionResult with workflow_command, adw_id, and model_set."""

    # Use classify_adw to extract structured info
    request = AgentTemplateRequest(
        agent_name="adw_classifier",
        slash_command="/classify_adw",
        args=[text],
        adw_id=temp_adw_id,
    )

    try:
        response = execute_template(request)  # No logger available in this function

        if not response.success:
            print(f"Failed to classify ADW: {response.output}")
            return ADWExtractionResult()  # Empty result

        # Parse JSON response using utility that handles markdown
        try:
            from .utils import parse_json
            data = parse_json(response.output, dict)
            adw_command = data.get("adw_slash_command", "").replace(
                "/", ""
            )  # Remove slash
            adw_id = data.get("adw_id")
            model_set = data.get("model_set", "base")  # Default to "base"

            # Validate command
            if adw_command and adw_command in AVAILABLE_ADW_WORKFLOWS:
                return ADWExtractionResult(
                    workflow_command=adw_command,
                    adw_id=adw_id,
                    model_set=model_set
                )

            return ADWExtractionResult()  # Empty result

        except ValueError as e:
            print(f"Failed to parse classify_adw response: {e}")
            return ADWExtractionResult()  # Empty result

    except Exception as e:
        print(f"Error calling classify_adw: {e}")
        return ADWExtractionResult()  # Empty result


def classify_issue(
    issue_data: Dict[str, Any], adw_id: str, logger: logging.Logger
) -> Tuple[Optional[str], Optional[str]]:
    """Classify issue and return appropriate slash command.

    Args:
        issue_data: Dictionary containing issue details (must have 'number', 'title', 'body')
        adw_id: ADW identifier
        logger: Logger instance

    Returns:
        (command, error_message) tuple where command is like '/chore', '/bug', '/feature' or None
    """

    # Extract minimal fields for classification
    minimal_issue = {
        "number": issue_data.get("number"),
        "title": issue_data.get("title"),
        "body": issue_data.get("body")
    }
    minimal_issue_json = json.dumps(minimal_issue)

    request = AgentTemplateRequest(
        agent_name=AGENT_CLASSIFIER,
        slash_command="/classify_issue",
        args=[minimal_issue_json],
        adw_id=adw_id,
    )

    logger.debug(f"Classifying issue: {issue_data.get('title')}")

    response = execute_template(request)

    logger.debug(
        f"Classification response: {response.model_dump_json(indent=2, by_alias=True)}"
    )

    if not response.success:
        return None, response.output

    # Extract the classification from the response
    output = response.output.strip()

    # Look for the classification pattern in the output
    # Claude might add explanation, so we need to extract just the command
    classification_match = re.search(r"(/chore|/bug|/feature|/patch|0)", output)

    if classification_match:
        issue_command = classification_match.group(1)
    else:
        issue_command = output

    if issue_command == "0":
        return None, f"No command selected: {response.output}"

    if issue_command not in ["/chore", "/bug", "/feature", "/patch"]:
        return None, f"Invalid command selected: {response.output}"

    return issue_command, None


def build_plan(
    issue_data: Dict[str, Any],
    command: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> AgentPromptResponse:
    """Build implementation plan for the issue using the specified command.

    Args:
        issue_data: Dictionary containing issue details (must have 'number', 'title', 'body')
        command: Classification command (e.g., '/feature', '/bug', '/chore')
        adw_id: ADW identifier
        logger: Logger instance
        working_dir: Optional working directory for the agent

    Returns:
        AgentPromptResponse with the plan result
    """
    # Use minimal payload for efficiency
    minimal_issue = {
        "number": issue_data.get("number"),
        "title": issue_data.get("title"),
        "body": issue_data.get("body")
    }
    minimal_issue_json = json.dumps(minimal_issue)

    issue_plan_template_request = AgentTemplateRequest(
        agent_name=AGENT_PLANNER,
        slash_command=command,
        args=[str(issue_data.get("number")), adw_id, minimal_issue_json],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(
        f"issue_plan_template_request: {issue_plan_template_request.model_dump_json(indent=2, by_alias=True)}"
    )

    issue_plan_response = execute_template(issue_plan_template_request)

    logger.debug(
        f"issue_plan_response: {issue_plan_response.model_dump_json(indent=2, by_alias=True)}"
    )

    return issue_plan_response


def implement_plan(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    agent_name: Optional[str] = None,
    working_dir: Optional[str] = None,
) -> AgentPromptResponse:
    """Implement the plan using the /implement command."""
    # Use provided agent_name or default to AGENT_IMPLEMENTOR
    implementor_name = agent_name or AGENT_IMPLEMENTOR

    implement_template_request = AgentTemplateRequest(
        agent_name=implementor_name,
        slash_command="/implement",
        args=[plan_file],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(
        f"implement_template_request: {implement_template_request.model_dump_json(indent=2, by_alias=True)}"
    )

    implement_response = execute_template(implement_template_request)

    logger.debug(
        f"implement_response: {implement_response.model_dump_json(indent=2, by_alias=True)}"
    )

    return implement_response


def implement_plan_with_tracking(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
    max_concurrent: int = 3,
    model_strategy: str = "auto",
) -> AgentPromptResponse:
    """Implement plan with step-level tracking and parallel execution.

    Uses the MultiPhaseOrchestrator for step-by-step execution with:
    - Group-level dependency ordering
    - Parallel execution within groups (when marked parallel)
    - Per-step model selection based on strategy
    - Progress tracking and resume capability

    Args:
        plan_file: Path to the spec/plan file to implement
        adw_id: ADW identifier
        logger: Logger instance
        working_dir: Optional working directory for execution
        max_concurrent: Maximum concurrent steps for parallel groups (default: 3)
        model_strategy: Model selection strategy (auto/sonnet/opus/heavy-for-build)

    Returns:
        AgentPromptResponse with implementation summary
    """
    from .plan_executor import MultiPhaseOrchestrator, PlanParser
    from pathlib import Path

    logger.info(f"Starting tracked implementation of {plan_file}")
    logger.info(f"Model strategy: {model_strategy}, max_concurrent: {max_concurrent}")

    try:
        # Resolve plan file path relative to working_dir if needed
        plan_path = Path(plan_file)
        if not plan_path.is_absolute() and working_dir:
            plan_path = Path(working_dir) / plan_file

        # Parse the plan
        parser = PlanParser(logger)
        plan = parser.parse_file(str(plan_path))

        if not plan.groups:
            return AgentPromptResponse(
                output=f"No steps found in plan file: {plan_file}",
                success=False,
            )

        logger.info(
            f"Parsed plan: {len(plan.groups)} groups, {plan.total_steps()} steps"
        )

        # Execute with orchestrator
        orchestrator = MultiPhaseOrchestrator(
            adw_id=adw_id,
            working_dir=working_dir or os.getcwd(),
            logger=logger,
            max_workers=max_concurrent,
        )

        result = orchestrator.execute_plan(plan)

        # Format summary
        summary_lines = [
            "═" * 50,
            "IMPLEMENTATION SUMMARY",
            "═" * 50,
            f"Plan: {plan_file}",
            f"Steps Completed: {result.completed_steps}/{result.total_steps}",
            f"Success: {result.success}",
            "",
            "Group Results:",
        ]

        for gr in result.group_results:
            status = "✓" if gr.success else "✗"
            summary_lines.append(f"  {status} Group {gr.group_id}: {len(gr.step_results)} steps")
            for sr in gr.step_results:
                step_status = "✓" if sr.success else "✗"
                summary_lines.append(f"      {step_status} {sr.step_id}")
                if sr.error_message:
                    summary_lines.append(f"          Error: {sr.error_message[:100]}")

        if result.error_message:
            summary_lines.append("")
            summary_lines.append(f"Error: {result.error_message}")

        summary_lines.append("═" * 50)
        summary = "\n".join(summary_lines)

        logger.info(summary)

        return AgentPromptResponse(
            output=summary,
            success=result.success,
        )

    except FileNotFoundError as e:
        error_msg = f"Plan file not found: {e}"
        logger.error(error_msg)
        return AgentPromptResponse(output=error_msg, success=False)

    except Exception as e:
        error_msg = f"Error during tracked implementation: {e}"
        logger.error(error_msg, exc_info=True)
        return AgentPromptResponse(output=error_msg, success=False)


def generate_branch_name(
    issue_data: Dict[str, Any],
    issue_class: str,
    adw_id: str,
    logger: logging.Logger,
) -> Tuple[Optional[str], Optional[str]]:
    """Generate a git branch name for the issue.

    Args:
        issue_data: Dictionary containing issue details (must have 'number', 'title', 'body')
        issue_class: Issue classification (e.g., '/feature', '/bug', '/chore')
        adw_id: ADW identifier
        logger: Logger instance

    Returns:
        (branch_name, error_message) tuple
    """
    # Remove the leading slash from issue_class for the branch name
    issue_type = issue_class.replace("/", "")

    # Use minimal payload
    minimal_issue = {
        "number": issue_data.get("number"),
        "title": issue_data.get("title"),
        "body": issue_data.get("body")
    }
    minimal_issue_json = json.dumps(minimal_issue)

    request = AgentTemplateRequest(
        agent_name=AGENT_BRANCH_GENERATOR,
        slash_command="/generate_branch_name",
        args=[issue_type, adw_id, minimal_issue_json],
        adw_id=adw_id,
    )

    response = execute_template(request)

    if not response.success:
        return None, response.output

    branch_name = response.output.strip()
    logger.info(f"Generated branch name: {branch_name}")
    return branch_name, None


def create_commit(
    agent_name: str,
    issue_data: Dict[str, Any],
    issue_class: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: str,
) -> Tuple[Optional[str], Optional[str]]:
    """Create a git commit with a properly formatted message.

    Args:
        agent_name: Name of the agent creating the commit
        issue_data: Dictionary containing issue details (must have 'number', 'title', 'body')
        issue_class: Issue classification (e.g., '/feature', '/bug', '/chore')
        adw_id: ADW identifier
        logger: Logger instance
        working_dir: Working directory for git operations

    Returns:
        (commit_message, error_message) tuple
    """
    # Remove the leading slash from issue_class
    issue_type = issue_class.replace("/", "")

    # Create unique committer agent name by suffixing '_committer'
    unique_agent_name = f"{agent_name}_committer"

    # Use minimal payload
    minimal_issue = {
        "number": issue_data.get("number"),
        "title": issue_data.get("title"),
        "body": issue_data.get("body")
    }
    minimal_issue_json = json.dumps(minimal_issue)

    request = AgentTemplateRequest(
        agent_name=unique_agent_name,
        slash_command="/commit",
        args=[agent_name, issue_type, minimal_issue_json],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        return None, response.output

    commit_message = response.output.strip()
    logger.info(f"Created commit message: {commit_message}")
    return commit_message, None


def create_pull_request(
    branch_name: str,
    issue_data: Optional[Dict[str, Any]],
    state: ADWState,
    logger: logging.Logger,
    working_dir: str,
) -> Tuple[Optional[str], Optional[str]]:
    """Create a pull request for the implemented changes.

    Args:
        branch_name: Name of the branch to create PR from
        issue_data: Optional dictionary containing issue details
        state: ADW state object
        logger: Logger instance
        working_dir: Working directory for git operations

    Returns:
        (pr_url, error_message) tuple
    """

    # Get plan file from state (may be None for test runs)
    plan_file = state.get("plan_file") or "No plan file (test run)"
    adw_id = state.get("adw_id")

    # If we don't have issue data, try to get from state
    if not issue_data:
        issue_data = state.get("issue", {})

    # Create minimal issue JSON
    if issue_data:
        minimal_issue = {
            "number": issue_data.get("number"),
            "title": issue_data.get("title"),
            "body": issue_data.get("body")
        }
        issue_json = json.dumps(minimal_issue)
    else:
        issue_json = "{}"

    request = AgentTemplateRequest(
        agent_name=AGENT_PR_CREATOR,
        slash_command="/pull_request",
        args=[branch_name, issue_json, plan_file, adw_id],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        return None, response.output

    pr_url = response.output.strip()
    logger.info(f"Created pull request: {pr_url}")
    return pr_url, None


def ensure_plan_exists(state: ADWState, issue_number: str) -> str:
    """Find or error if no plan exists for issue.
    Used by isolated build workflows in standalone mode."""
    # Check if plan file is in state
    if state.get("plan_file"):
        return state.get("plan_file")

    # Check current branch
    from .git_ops import get_current_branch

    branch = get_current_branch()

    # Look for plan in branch name
    if f"-{issue_number}-" in branch:
        # Look for plan file
        plans = glob.glob(f"specs/*{issue_number}*.md")
        if plans:
            return plans[0]

    # No plan found
    raise ValueError(
        f"No plan found for issue {issue_number}. Run adw_plan_iso.py first."
    )


def ensure_adw_id(
    issue_number: str,
    adw_id: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> str:
    """Get ADW ID or create a new one and initialize state.

    Args:
        issue_number: The issue number to find/create ADW ID for
        adw_id: Optional existing ADW ID to use
        logger: Optional logger instance

    Returns:
        The ADW ID (existing or newly created)
    """
    # If ADW ID provided, check if state exists
    if adw_id:
        state = ADWState.load(adw_id, logger)
        if state:
            if logger:
                logger.info(f"Found existing ADW state for ID: {adw_id}")
            else:
                print(f"Found existing ADW state for ID: {adw_id}")
            return adw_id
        # ADW ID provided but no state exists, create state
        state = ADWState(adw_id)
        state.update(adw_id=adw_id, issue_number=issue_number)
        state.save("ensure_adw_id")
        if logger:
            logger.info(f"Created new ADW state for provided ID: {adw_id}")
        else:
            print(f"Created new ADW state for provided ID: {adw_id}")
        return adw_id

    # No ADW ID provided, create new one with state
    from .utils import make_adw_id

    new_adw_id = make_adw_id()
    state = ADWState(new_adw_id)
    state.update(adw_id=new_adw_id, issue_number=issue_number)
    state.save("ensure_adw_id")
    if logger:
        logger.info(f"Created new ADW ID and state: {new_adw_id}")
    else:
        print(f"Created new ADW ID and state: {new_adw_id}")
    return new_adw_id


def find_existing_branch_for_issue(
    issue_number: str, adw_id: Optional[str] = None, cwd: Optional[str] = None
) -> Optional[str]:
    """Find an existing branch for the given issue number.
    Returns branch name if found, None otherwise."""
    # List all branches
    result = subprocess.run(
        ["git", "branch", "-a"], capture_output=True, text=True, cwd=cwd
    )

    if result.returncode != 0:
        return None

    branches = result.stdout.strip().split("\n")

    # Look for branch with standardized pattern: *-issue-{issue_number}-adw-{adw_id}-*
    for branch in branches:
        branch = branch.strip().replace("* ", "").replace("remotes/origin/", "")
        # Check for the standardized pattern
        if f"-issue-{issue_number}-" in branch:
            if adw_id and f"-adw-{adw_id}-" in branch:
                return branch
            elif not adw_id:
                # Return first match if no adw_id specified
                return branch

    return None


def find_plan_for_issue(
    issue_number: str, adw_id: Optional[str] = None
) -> Optional[str]:
    """Find plan file for the given issue number and optional adw_id.
    Returns path to plan file if found, None otherwise."""
    import os

    # Get project root
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    agents_dir = os.path.join(project_root, "agents")

    if not os.path.exists(agents_dir):
        return None

    # If adw_id is provided, check specific directory first
    if adw_id:
        plan_path = os.path.join(agents_dir, adw_id, AGENT_PLANNER, "plan.md")
        if os.path.exists(plan_path):
            return plan_path

    # Otherwise, search all agent directories
    for agent_id in os.listdir(agents_dir):
        agent_path = os.path.join(agents_dir, agent_id)
        if os.path.isdir(agent_path):
            plan_path = os.path.join(agent_path, AGENT_PLANNER, "plan.md")
            if os.path.exists(plan_path):
                # Check if this plan is for our issue by reading branch info or checking commits
                # For now, return the first plan found (can be improved)
                return plan_path

    return None


def create_or_find_branch(
    issue_number: str,
    issue_data: Dict[str, Any],
    state: ADWState,
    logger: logging.Logger,
    cwd: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """Create or find a branch for the given issue.

    1. First checks state for existing branch name
    2. Then looks for existing branches matching the issue
    3. If none found, classifies the issue and creates a new branch

    Args:
        issue_number: Issue number
        issue_data: Dictionary containing issue details
        state: ADW state object
        logger: Logger instance
        cwd: Optional working directory

    Returns:
        (branch_name, error_message) tuple.
    """
    # 1. Check state for branch name
    branch_name = state.get("branch_name") or state.get("branch", {}).get("name")
    if branch_name:
        logger.info(f"Found branch in state: {branch_name}")
        # Check if we need to checkout
        from .git_ops import get_current_branch

        current = get_current_branch(cwd=cwd)
        if current != branch_name:
            result = subprocess.run(
                ["git", "checkout", branch_name],
                capture_output=True,
                text=True,
                cwd=cwd,
            )
            if result.returncode != 0:
                # Branch might not exist locally, try to create from remote
                result = subprocess.run(
                    ["git", "checkout", "-b", branch_name, f"origin/{branch_name}"],
                    capture_output=True,
                    text=True,
                    cwd=cwd,
                )
                if result.returncode != 0:
                    return "", f"Failed to checkout branch: {result.stderr}"
        return branch_name, None

    # 2. Look for existing branch
    adw_id = state.get("adw_id")
    existing_branch = find_existing_branch_for_issue(issue_number, adw_id, cwd=cwd)
    if existing_branch:
        logger.info(f"Found existing branch: {existing_branch}")
        # Checkout the branch
        result = subprocess.run(
            ["git", "checkout", existing_branch],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        if result.returncode != 0:
            return "", f"Failed to checkout branch: {result.stderr}"
        state.update(branch_name=existing_branch)
        return existing_branch, None

    # 3. Create new branch - classify issue first
    logger.info("No existing branch found, creating new one")

    # Classify the issue
    issue_command, error = classify_issue(issue_data, adw_id, logger)
    if error:
        return "", f"Failed to classify issue: {error}"

    state.update(issue_class=issue_command)

    # Generate branch name
    branch_name, error = generate_branch_name(issue_data, issue_command, adw_id, logger)
    if error:
        return "", f"Failed to generate branch name: {error}"

    # Create the branch
    from .git_ops import create_branch

    success, error = create_branch(branch_name, cwd=cwd)
    if not success:
        return "", f"Failed to create branch: {error}"

    state.update(branch_name=branch_name)
    logger.info(f"Created and checked out new branch: {branch_name}")

    return branch_name, None


def find_spec_file(state: ADWState, logger: logging.Logger) -> Optional[str]:
    """Find the spec file from state or by examining git diff.

    For isolated workflows, automatically uses worktree_path from state.
    """
    # Get worktree path if in isolated workflow
    worktree_path = state.get("worktree_path")

    # Check if spec file is already in state (from plan phase)
    spec_file = state.get("plan_file")
    if spec_file:
        # If worktree_path exists and spec_file is relative, make it absolute
        if worktree_path and not os.path.isabs(spec_file):
            spec_file = os.path.join(worktree_path, spec_file)

        if os.path.exists(spec_file):
            logger.info(f"Using spec file from state: {spec_file}")
            return spec_file

    # Otherwise, try to find it from git diff
    logger.info("Looking for spec file in git diff")
    result = subprocess.run(
        ["git", "diff", "origin/main", "--name-only"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    )

    if result.returncode == 0:
        files = result.stdout.strip().split("\n")
        spec_files = [f for f in files if f.startswith("specs/") and f.endswith(".md")]

        if spec_files:
            # Use the first spec file found
            spec_file = spec_files[0]
            if worktree_path:
                spec_file = os.path.join(worktree_path, spec_file)
            logger.info(f"Found spec file: {spec_file}")
            return spec_file

    # If still not found, try to derive from branch name
    branch_name = state.get("branch_name")
    if branch_name:
        # Extract issue number from branch name
        import re

        match = re.search(r"issue-(\d+)", branch_name)
        if match:
            issue_num = match.group(1)
            adw_id = state.get("adw_id")

            # Look for spec files matching the pattern
            import glob

            # Use worktree_path if provided, otherwise current directory
            search_dir = worktree_path if worktree_path else os.getcwd()
            pattern = os.path.join(
                search_dir, f"specs/issue-{issue_num}-adw-{adw_id}*.md"
            )
            spec_files = glob.glob(pattern)

            if spec_files:
                spec_file = spec_files[0]
                logger.info(f"Found spec file by pattern: {spec_file}")
                return spec_file

    logger.warning("No spec file found")
    return None


def create_and_implement_patch(
    adw_id: str,
    review_change_request: str,
    logger: logging.Logger,
    agent_name_planner: str,
    agent_name_implementor: str,
    spec_path: Optional[str] = None,
    issue_screenshots: Optional[str] = None,
    working_dir: Optional[str] = None,
) -> Tuple[Optional[str], AgentPromptResponse]:
    """Create a patch plan and implement it.
    Returns (patch_file_path, implement_response) tuple."""

    # Create patch plan using /patch command
    args = [adw_id, review_change_request]

    # Add optional arguments in the correct order
    if spec_path:
        args.append(spec_path)
    else:
        args.append("")  # Empty string for optional spec_path

    args.append(agent_name_planner)

    if issue_screenshots:
        args.append(issue_screenshots)

    request = AgentTemplateRequest(
        agent_name=agent_name_planner,
        slash_command="/patch",
        args=args,
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(
        f"Patch plan request: {request.model_dump_json(indent=2, by_alias=True)}"
    )

    response = execute_template(request)

    logger.debug(
        f"Patch plan response: {response.model_dump_json(indent=2, by_alias=True)}"
    )

    if not response.success:
        logger.error(f"Error creating patch plan: {response.output}")
        # Return None and a failed response
        return None, AgentPromptResponse(
            output=f"Failed to create patch plan: {response.output}", success=False
        )

    # Extract the patch plan file path from the response
    patch_file_path = response.output.strip()

    # Validate that it looks like a file path
    if "specs/patch/" not in patch_file_path or not patch_file_path.endswith(".md"):
        logger.error(f"Invalid patch plan path returned: {patch_file_path}")
        return None, AgentPromptResponse(
            output=f"Invalid patch plan path: {patch_file_path}", success=False
        )

    logger.info(f"Created patch plan: {patch_file_path}")

    # Now implement the patch plan using the provided implementor agent name
    implement_response = implement_plan(
        patch_file_path, adw_id, logger, agent_name_implementor, working_dir=working_dir
    )

    return patch_file_path, implement_response


# ============================================================================
# Export/Bootstrap Utilities
# ============================================================================


def collect_jerry_core_files(base_path: str = ".") -> List[str]:
    """
    Collect list of Jerry core files for export.

    Returns:
        List of relative file paths that constitute Jerry's core
    """
    from pathlib import Path

    base = Path(base_path)
    core_files = []

    # Core directories
    core_dirs = ["adws", ".claude", "specs", ".jerry"]

    for dir_name in core_dirs:
        dir_path = base / dir_name
        if dir_path.exists():
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    # Skip cache and test files
                    if any(
                        part.startswith(("__pycache__", ".pytest_cache", "test_"))
                        for part in file_path.parts
                    ):
                        continue
                    if file_path.suffix in [".pyc", ".pyo"]:
                        continue

                    rel_path = str(file_path.relative_to(base))
                    core_files.append(rel_path)

    # Add root files
    root_files = ["README.md", "LICENSE", ".gitignore", "jerry_bootstrap.sh"]
    for filename in root_files:
        file_path = base / filename
        if file_path.exists():
            core_files.append(filename)

    return sorted(core_files)


def get_jerry_version(base_path: str = ".") -> str:
    """
    Extract Jerry version from manifest.

    Returns:
        Version string (e.g., "0.1.0")
    """
    from pathlib import Path

    manifest_path = Path(base_path) / ".jerry" / "manifest.json"

    if not manifest_path.exists():
        return "unknown"

    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        return manifest.get("version", "unknown")
    except Exception:
        return "unknown"


def verify_prerequisites() -> Tuple[bool, List[str]]:
    """
    Verify that system prerequisites are met for Jerry.

    Returns:
        Tuple of (all_satisfied: bool, missing: List[str])
    """
    missing = []

    # Check Python version
    try:
        result = subprocess.run(
            ["python3", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_str = result.stdout.strip()
            # Parse version (e.g., "Python 3.11.0")
            import re
            match = re.search(r"(\d+)\.(\d+)", version_str)
            if match:
                major, minor = int(match.group(1)), int(match.group(2))
                if major < 3 or (major == 3 and minor < 11):
                    missing.append("python3.11+ (found older version)")
        else:
            missing.append("python3")
    except Exception:
        missing.append("python3")

    # Check uv
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            missing.append("uv")
    except FileNotFoundError:
        missing.append("uv")
    except Exception:
        missing.append("uv")

    # Check git
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            missing.append("git")
    except FileNotFoundError:
        missing.append("git")
    except Exception:
        missing.append("git")

    # Check Claude Code CLI (optional)
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            missing.append("claude (optional)")
    except FileNotFoundError:
        missing.append("claude (optional)")
    except Exception:
        pass  # Claude is optional

    return len(missing) == 0, missing


def validate_jerry_installation(base_path: str = ".", level: int = 1) -> Tuple[bool, str]:
    """
    Validate Jerry installation.

    Args:
        base_path: Path to Jerry installation
        level: Validation level (1=basic, 2=cli, 3=dry-run)

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    from pathlib import Path

    base = Path(base_path)

    # Level 1: Basic validation
    manifest_path = base / ".jerry" / "manifest.json"
    if not manifest_path.exists():
        return False, "Manifest not found at .jerry/manifest.json"

    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except Exception as e:
        return False, f"Invalid manifest: {e}"

    # Check core directories
    for dir_name in manifest.get("core_directories", []):
        dir_path = base / dir_name.rstrip("/")
        if not dir_path.exists():
            return False, f"Missing core directory: {dir_name}"

    # Check required files
    for file_path in manifest.get("required_files", []):
        full_path = base / file_path
        if not full_path.exists():
            return False, f"Missing required file: {file_path}"

    if level == 1:
        return True, "Level 1 validation passed"

    # Level 2: CLI validation
    if level >= 2:
        adw_prompt = base / "adws" / "adw_prompt.py"
        if not adw_prompt.exists():
            return False, "ADW script not found: adws/adw_prompt.py"

        if not os.access(adw_prompt, os.X_OK):
            return False, "ADW script not executable: adws/adw_prompt.py"

    if level == 2:
        return True, "Level 2 validation passed"

    # Level 3: Dry-run validation would require actual execution
    # which is better handled by jerry_validate.py script

    return True, f"Level {level} validation passed"
