#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fastapi", "uvicorn", "python-dotenv", "pydantic"]
# ///

"""
GitHub Webhook Trigger - AI Developer Workflow (ADW)

FastAPI webhook endpoint that receives GitHub issue events and triggers ADW workflows.
Responds immediately to meet GitHub's 10-second timeout by launching workflows
in the background. Deployment-agnostic implementation for Jerry's agentic layer.

Usage: uv run trigger_github.py

Environment Requirements:
- PORT: Server port (default: 8001)
- All workflow requirements (GITHUB_PAT, ANTHROPIC_API_KEY, etc.)
"""

import os
import subprocess
import sys
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import uvicorn

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adw_modules.utils import make_adw_id, setup_logger, get_safe_subprocess_env
from adw_modules.github import make_issue_comment, ADW_BOT_IDENTIFIER
from adw_modules.workflow_ops import extract_adw_info
from adw_modules.state import ADWState

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", "8001"))

# Extensibility: Load workflow constraints from environment or config
# Format: DEPENDENT_WORKFLOWS="adw_build_iso,adw_test_iso,adw_review_iso"
DEPENDENT_WORKFLOWS_ENV = os.getenv("DEPENDENT_WORKFLOWS", "")
DEPENDENT_WORKFLOWS: List[str] = (
    [w.strip() for w in DEPENDENT_WORKFLOWS_ENV.split(",") if w.strip()]
    if DEPENDENT_WORKFLOWS_ENV
    else []
)

# Create FastAPI app
app = FastAPI(
    title="ADW GitHub Webhook Trigger",
    description="GitHub webhook endpoint for ADW workflows",
)

print(f"Starting ADW GitHub Webhook Trigger on port {PORT}")
if DEPENDENT_WORKFLOWS:
    print(f"Dependent workflows requiring ADW ID: {', '.join(DEPENDENT_WORKFLOWS)}")


def get_workflow_metadata(workflow: str) -> Dict[str, Any]:
    """
    Get metadata about a workflow (extensibility hook).

    This can be extended to read from manifest files or a workflow registry.
    Returns default metadata for now.
    """
    return {
        "requires_adw_id": workflow in DEPENDENT_WORKFLOWS,
        "timeout": 300,  # Default timeout in seconds
        "background": True,  # Run in background
    }


@app.post("/gh-webhook")
async def github_webhook(request: Request):
    """Handle GitHub webhook events."""
    try:
        # Get event type from header
        event_type = request.headers.get("X-GitHub-Event", "")

        # Parse webhook payload
        payload = await request.json()

        # Extract event details
        action = payload.get("action", "")
        issue = payload.get("issue", {})
        issue_number = issue.get("number")

        print(
            f"Received webhook: event={event_type}, action={action}, issue_number={issue_number}"
        )

        workflow = None
        provided_adw_id = None
        model_set = None
        trigger_reason = ""
        content_to_check = ""

        # Check if this is an issue opened event
        if event_type == "issues" and action == "opened" and issue_number:
            issue_body = issue.get("body", "")
            content_to_check = issue_body

            # Ignore issues from ADW bot to prevent loops
            if ADW_BOT_IDENTIFIER in issue_body:
                print(f"Ignoring ADW bot issue to prevent loop")
                workflow = None
            # Check if body contains "adw_"
            elif "adw_" in issue_body.lower():
                # Use temporary ID for classification
                temp_id = make_adw_id()
                extraction_result = extract_adw_info(issue_body, temp_id)
                if extraction_result.has_workflow:
                    workflow = extraction_result.workflow_command
                    provided_adw_id = extraction_result.adw_id
                    model_set = extraction_result.model_set
                    trigger_reason = f"New issue with {workflow} workflow"

        # Check if this is an issue comment
        elif event_type == "issue_comment" and action == "created" and issue_number:
            comment = payload.get("comment", {})
            comment_body = comment.get("body", "")
            content_to_check = comment_body

            print(f"Comment body: '{comment_body}'")

            # Ignore comments from ADW bot to prevent loops
            if ADW_BOT_IDENTIFIER in comment_body:
                print(f"Ignoring ADW bot comment to prevent loop")
                workflow = None
            # Check if comment contains "adw_"
            elif "adw_" in comment_body.lower():
                # Use temporary ID for classification
                temp_id = make_adw_id()
                extraction_result = extract_adw_info(comment_body, temp_id)
                if extraction_result.has_workflow:
                    workflow = extraction_result.workflow_command
                    provided_adw_id = extraction_result.adw_id
                    model_set = extraction_result.model_set
                    trigger_reason = f"Comment with {workflow} workflow"

        # Validate workflow constraints using metadata
        if workflow:
            metadata = get_workflow_metadata(workflow)

            if metadata["requires_adw_id"] and not provided_adw_id:
                print(
                    f"{workflow} is a dependent workflow that requires an existing ADW ID"
                )
                print(f"Cannot trigger {workflow} directly via webhook without ADW ID")
                workflow = None
                # Post error comment to issue
                try:
                    make_issue_comment(
                        str(issue_number),
                        f"❌ Error: `{workflow}` is a dependent workflow that requires an existing ADW ID.\n\n"
                        f"To run this workflow, you must provide the ADW ID in your comment, for example:\n"
                        f"`{workflow} adw-12345678`\n\n"
                        f"The ADW ID should come from a previous workflow run.",
                    )
                except Exception as e:
                    print(f"Failed to post error comment: {e}")

        if workflow:
            # Use provided ADW ID or generate a new one
            adw_id = provided_adw_id or make_adw_id()

            # If ADW ID was provided, update/create state file
            if provided_adw_id:
                # Try to load existing state first
                state = ADWState.load(provided_adw_id)
                if state:
                    # Update issue_number and model_set if state exists
                    state.update(issue_number=str(issue_number), model_set=model_set)
                else:
                    # Only create new state if it doesn't exist
                    state = ADWState(provided_adw_id)
                    state.update(
                        adw_id=provided_adw_id,
                        issue_number=str(issue_number),
                        model_set=model_set,
                    )
                state.save("github_trigger")
            else:
                # Create new state for newly generated ADW ID
                state = ADWState(adw_id)
                state.update(
                    adw_id=adw_id, issue_number=str(issue_number), model_set=model_set
                )
                state.save("github_trigger")

            # Set up logger
            logger = setup_logger(adw_id, "github_trigger")
            logger.info(
                f"Detected workflow: {workflow} from content: {content_to_check[:100]}..."
            )
            if provided_adw_id:
                logger.info(f"Using provided ADW ID: {provided_adw_id}")

            # Post comment to issue about detected workflow
            try:
                make_issue_comment(
                    str(issue_number),
                    f"🤖 ADW GitHub Trigger: Detected `{workflow}` workflow request\n\n"
                    f"Starting workflow with ID: `{adw_id}`\n"
                    f"Workflow: `{workflow}` 🏗️\n"
                    f"Model Set: `{model_set}` ⚙️\n"
                    f"Reason: {trigger_reason}\n\n"
                    f"Logs will be available at: `agents/{adw_id}/{workflow}/`",
                )
            except Exception as e:
                logger.warning(f"Failed to post issue comment: {e}")

            # Build command to run the appropriate workflow
            script_dir = os.path.dirname(os.path.abspath(__file__))
            adws_dir = os.path.dirname(script_dir)
            repo_root = os.path.dirname(adws_dir)  # Go up to repository root
            trigger_script = os.path.join(adws_dir, f"{workflow}.py")

            cmd = ["uv", "run", trigger_script, str(issue_number), adw_id]

            print(f"Launching {workflow} for issue #{issue_number}")
            print(f"Command: {' '.join(cmd)} (reason: {trigger_reason})")
            print(f"Working directory: {repo_root}")

            # Launch in background using Popen with filtered environment
            process = subprocess.Popen(
                cmd,
                cwd=repo_root,  # Run from repository root where .claude/commands/ is located
                env=get_safe_subprocess_env(),  # Pass only required environment variables
                start_new_session=True,
            )

            print(
                f"Background process started for issue #{issue_number} with ADW ID: {adw_id}"
            )
            print(f"Logs will be written to: agents/{adw_id}/{workflow}/execution.log")

            # Return immediately
            return {
                "status": "accepted",
                "issue": issue_number,
                "adw_id": adw_id,
                "workflow": workflow,
                "message": f"ADW {workflow} triggered for issue #{issue_number}",
                "reason": trigger_reason,
                "logs": f"agents/{adw_id}/{workflow}/",
            }
        else:
            print(
                f"Ignoring webhook: event={event_type}, action={action}, issue_number={issue_number}"
            )
            return {
                "status": "ignored",
                "reason": f"Not a triggering event (event={event_type}, action={action})",
            }

    except Exception as e:
        print(f"Error processing webhook: {e}")
        # Always return 200 to GitHub to prevent retries
        return {"status": "error", "message": "Internal error processing webhook"}


@app.get("/health")
async def health():
    """Health check endpoint - runs comprehensive system health check."""
    try:
        # Run the health check script if available
        script_dir = os.path.dirname(os.path.abspath(__file__))
        health_check_script = os.path.join(
            os.path.dirname(script_dir), "adw_tests", "health_check.py"
        )

        # Check if health check script exists
        if not os.path.exists(health_check_script):
            return {
                "status": "healthy",
                "service": "adw-github-trigger",
                "health_check": {
                    "success": True,
                    "warnings": ["Health check script not found - using basic check"],
                    "errors": [],
                    "details": "Server is running",
                },
            }

        # Run health check with timeout
        result = subprocess.run(
            ["uv", "run", health_check_script],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(script_dir),  # Run from adws directory
        )

        # Print the health check output for debugging
        print("=== Health Check Output ===")
        print(result.stdout)
        if result.stderr:
            print("=== Health Check Errors ===")
            print(result.stderr)

        # Parse the output - look for the overall status
        output_lines = result.stdout.strip().split("\n")
        is_healthy = result.returncode == 0

        # Extract key information from output
        warnings = []
        errors = []

        capturing_warnings = False
        capturing_errors = False

        for line in output_lines:
            if "⚠️  Warnings:" in line:
                capturing_warnings = True
                capturing_errors = False
                continue
            elif "❌ Errors:" in line:
                capturing_errors = True
                capturing_warnings = False
                continue
            elif "📝 Next Steps:" in line:
                break

            if capturing_warnings and line.strip().startswith("-"):
                warnings.append(line.strip()[2:])
            elif capturing_errors and line.strip().startswith("-"):
                errors.append(line.strip()[2:])

        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "service": "adw-github-trigger",
            "health_check": {
                "success": is_healthy,
                "warnings": warnings,
                "errors": errors,
                "details": "Run health_check.py directly for full report",
            },
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "unhealthy",
            "service": "adw-github-trigger",
            "error": "Health check timed out",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "adw-github-trigger",
            "error": f"Health check failed: {str(e)}",
        }


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "ADW GitHub Webhook Trigger",
        "version": "1.0.0",
        "endpoints": {
            "webhook": "POST /gh-webhook",
            "health": "GET /health",
        },
        "configuration": {
            "port": PORT,
            "dependent_workflows": DEPENDENT_WORKFLOWS,
        },
    }


if __name__ == "__main__":
    print(f"Starting server on http://0.0.0.0:{PORT}")
    print(f"Webhook endpoint: POST /gh-webhook")
    print(f"Health check: GET /health")

    uvicorn.run(app, host="0.0.0.0", port=PORT)
