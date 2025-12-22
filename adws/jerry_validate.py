#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
#   "pydantic>=2.0.0",
#   "python-dotenv>=1.0.0",
# ]
# ///
"""
Jerry Validation Script

Validates Jerry installation at multiple levels to ensure it's ready to run workflows.

Usage:
    ./adws/jerry_validate.py --level all
    ./adws/jerry_validate.py --level 1
    ./adws/jerry_validate.py --level all --report /tmp/validation-report.json
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class ValidationResult:
    """Container for validation results."""

    def __init__(self, level: str, name: str):
        self.level = level
        self.name = name
        self.passed = False
        self.message = ""
        self.details = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "details": self.details
        }


def validate_file_exists(base_path: Path, rel_path: str) -> Tuple[bool, str]:
    """Check if a file exists."""
    file_path = base_path / rel_path
    if file_path.exists():
        return True, f"Found: {rel_path}"
    return False, f"Missing: {rel_path}"


def validate_directory_exists(base_path: Path, dir_name: str) -> Tuple[bool, str]:
    """Check if a directory exists."""
    dir_path = base_path / dir_name
    if dir_path.exists() and dir_path.is_dir():
        return True, f"Found: {dir_name}/"
    return False, f"Missing: {dir_name}/"


def validate_level_1(base_path: Path) -> List[ValidationResult]:
    """
    Level 1: Import Validation
    Test that all core modules can be imported.
    """
    results = []

    # Check manifest exists
    result = ValidationResult("1", "Manifest exists")
    manifest_path = base_path / ".jerry" / "manifest.json"
    if manifest_path.exists():
        result.passed = True
        result.message = "Manifest found"
        try:
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            result.details.append(f"Version: {manifest.get('version', 'unknown')}")
        except Exception as e:
            result.passed = False
            result.message = f"Manifest exists but invalid: {e}"
    else:
        result.message = "Manifest not found at .jerry/manifest.json"
    results.append(result)

    # Load manifest for checks
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

    # Check core directories
    result = ValidationResult("1", "Core directories exist")
    core_dirs = manifest.get("core_directories", ["adws/", ".claude/", "specs/"])
    missing_dirs = []
    for dir_name in core_dirs:
        dir_path = base_path / dir_name.rstrip("/")
        if not dir_path.exists():
            missing_dirs.append(dir_name)

    if not missing_dirs:
        result.passed = True
        result.message = "All core directories present"
        result.details = [f"✓ {d}" for d in core_dirs]
    else:
        result.message = f"Missing core directories: {', '.join(missing_dirs)}"
        result.details = missing_dirs
    results.append(result)

    # Check required files
    result = ValidationResult("1", "Required files exist")
    required_files = manifest.get("required_files", [
        "adws/adw_modules/agent.py",
        "adws/adw_modules/state.py",
        "adws/adw_modules/workflow_ops.py",
        "adws/adw_prompt.py",
    ])
    missing_files = []
    for file_path in required_files:
        full_path = base_path / file_path
        if not full_path.exists():
            missing_files.append(file_path)

    if not missing_files:
        result.passed = True
        result.message = "All required files present"
        result.details = [f"✓ {f}" for f in required_files[:5]]  # Show first 5
        if len(required_files) > 5:
            result.details.append(f"... and {len(required_files) - 5} more")
    else:
        result.message = f"Missing required files: {len(missing_files)}"
        result.details = missing_files[:10]  # Show first 10
    results.append(result)

    # Test Python module imports
    result = ValidationResult("1", "Python module imports")
    modules_to_test = [
        "adws.adw_modules.agent",
        "adws.adw_modules.state",
        "adws.adw_modules.workflow_ops",
        "adws.adw_modules.data_types",
    ]

    import_errors = []
    successful_imports = []

    # Change to base directory for imports
    original_cwd = os.getcwd()
    os.chdir(base_path)
    sys.path.insert(0, str(base_path))

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            successful_imports.append(module_name)
        except Exception as e:
            import_errors.append(f"{module_name}: {str(e)[:50]}")

    os.chdir(original_cwd)
    sys.path.remove(str(base_path))

    if not import_errors:
        result.passed = True
        result.message = "All core modules import successfully"
        result.details = [f"✓ {m}" for m in successful_imports]
    else:
        result.message = f"Failed to import {len(import_errors)} modules"
        result.details = import_errors
    results.append(result)

    # Check pattern infrastructure
    result = ValidationResult("1", "Pattern infrastructure")
    patterns_manifest_path = base_path / ".jerry" / "patterns" / "manifest.json"

    if not patterns_manifest_path.exists():
        result.passed = True  # Patterns are optional
        result.message = "Pattern system not initialized (optional)"
        result.details = ["Run jerry_sync_patterns.py to sync patterns"]
        results.append(result)
    else:
        try:
            with open(patterns_manifest_path, "r") as f:
                patterns_manifest = json.load(f)

            # Validate manifest schema
            required_fields = ["version", "last_synced", "bundled_patterns_count", "categories", "patterns"]
            missing_fields = [field for field in required_fields if field not in patterns_manifest]

            if missing_fields:
                result.passed = False
                result.message = f"Pattern manifest missing fields: {', '.join(missing_fields)}"
            else:
                # Count patterns and verify directories
                bundled_count = patterns_manifest.get("bundled_patterns_count", 0)
                patterns_dict = patterns_manifest.get("patterns", {})
                categories = patterns_manifest.get("categories", {})

                # Verify pattern directories exist
                patterns_base = base_path / ".jerry" / "patterns"
                missing_patterns = []
                for pattern_name, pattern_meta in patterns_dict.items():
                    category = pattern_meta.get("category", "unknown")
                    pattern_dir = patterns_base / category / pattern_name
                    system_md = pattern_dir / "system.md"

                    if not pattern_dir.exists():
                        missing_patterns.append(f"{pattern_name} (directory missing)")
                    elif not system_md.exists():
                        missing_patterns.append(f"{pattern_name} (system.md missing)")

                if missing_patterns:
                    result.passed = False
                    result.message = f"Pattern files missing: {len(missing_patterns)}"
                    result.details = missing_patterns[:5]  # Show first 5
                else:
                    result.passed = True

                    # Build category summary
                    category_summary = []
                    for cat, cat_data in categories.items():
                        count = cat_data.get("count", 0)
                        if count > 0:
                            category_summary.append(f"{cat}: {count}")

                    if bundled_count == 0:
                        result.message = "Pattern infrastructure ready, no patterns synced yet"
                        result.details = ["Run jerry_sync_patterns.py to sync patterns"]
                    else:
                        result.message = f"{bundled_count} patterns bundled across {len([c for c, d in categories.items() if d.get('count', 0) > 0])} categories"
                        result.details = category_summary

        except json.JSONDecodeError as e:
            result.passed = False
            result.message = "Pattern manifest JSON is corrupted"
            result.details = [str(e)[:100]]
        except Exception as e:
            result.passed = False
            result.message = f"Error validating pattern infrastructure: {str(e)[:100]}"

        results.append(result)

    return results


def validate_level_2(base_path: Path) -> List[ValidationResult]:
    """
    Level 2: CLI Validation
    Test that ADW scripts are executable and respond to --help.
    """
    results = []

    # Check ADW scripts are executable
    adw_scripts = [
        "adws/adw_prompt.py",
        "adws/adw_slash_command.py",
    ]

    for script_path in adw_scripts:
        result = ValidationResult("2", f"CLI: {script_path}")
        full_path = base_path / script_path

        if not full_path.exists():
            result.message = f"Script not found: {script_path}"
            results.append(result)
            continue

        # Test --help flag
        try:
            proc = subprocess.run(
                [str(full_path), "--help"],
                cwd=base_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "Script is executable and responds to --help"
                result.details = ["--help flag works"]
            else:
                result.message = f"Script exited with code {proc.returncode}"
                result.details = [proc.stderr[:200] if proc.stderr else "No error output"]
        except subprocess.TimeoutExpired:
            result.message = "Script timed out (>10s)"
        except Exception as e:
            result.message = f"Failed to execute: {str(e)[:100]}"

        results.append(result)

    # Check Claude Code CLI is installed
    result = ValidationResult("2", "Claude Code CLI")
    try:
        proc = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode == 0:
            result.passed = True
            result.message = "Claude Code CLI is installed"
            result.details = [proc.stdout.strip()]
        else:
            result.message = "Claude Code CLI not responding correctly"
    except FileNotFoundError:
        result.message = "Claude Code CLI not found in PATH"
        result.details = ["Install from: https://claude.com/code"]
    except Exception as e:
        result.message = f"Error checking Claude Code CLI: {str(e)[:100]}"
    results.append(result)

    # Check GitHub CLI (optional - warning only)
    result = ValidationResult("2", "GitHub CLI (gh)")
    try:
        proc = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode == 0:
            result.passed = True
            result.message = "GitHub CLI installed"
            version_line = proc.stdout.strip().split('\n')[0] if proc.stdout else ""
            result.details = [version_line]
        else:
            result.passed = True  # Still pass, but warn
            result.message = "[Warning] GitHub CLI not configured (optional for GitHub workflows)"
    except FileNotFoundError:
        result.passed = True  # Still pass
        result.message = "[Warning] GitHub CLI not installed - GitHub workflows unavailable"
        result.details = ["Install from: https://cli.github.com"]
    except Exception as e:
        result.passed = True
        result.message = f"[Warning] Error checking GitHub CLI: {str(e)[:50]}"
    results.append(result)

    # Check GitLab CLI (optional - warning only)
    result = ValidationResult("2", "GitLab CLI (glab)")
    try:
        proc = subprocess.run(
            ["glab", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode == 0:
            result.passed = True
            result.message = "GitLab CLI installed"
            version_line = proc.stdout.strip().split('\n')[0] if proc.stdout else ""
            result.details = [version_line]
        else:
            result.passed = True  # Still pass, but warn
            result.message = "[Warning] GitLab CLI not configured (optional for GitLab workflows)"
    except FileNotFoundError:
        result.passed = True  # Still pass
        result.message = "[Warning] GitLab CLI not installed - GitLab workflows unavailable"
        result.details = ["Install from: https://gitlab.com/gitlab-org/cli"]
    except Exception as e:
        result.passed = True
        result.message = f"[Warning] Error checking GitLab CLI: {str(e)[:50]}"
    results.append(result)

    return results


def validate_level_3(base_path: Path) -> List[ValidationResult]:
    """
    Level 3: Workflow Validation
    Test core Jerry workflows including slash commands and worktree isolation.
    CRITICAL for JARI - validates parallel execution capability.
    """
    results = []

    # 3.1 Test adw_prompt with a simple command
    result = ValidationResult("3", "adw_prompt.py execution")
    script_path = base_path / "adws" / "adw_prompt.py"
    if not script_path.exists():
        result.message = "Script not found"
        results.append(result)
    else:
        test_prompt = "echo 'Jerry validation test'"
        try:
            proc = subprocess.run(
                [str(script_path), test_prompt],
                cwd=base_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "adw_prompt.py executed successfully"
                agents_dir = base_path / "agents"
                if agents_dir.exists():
                    result.details = ["agents/ output directory created"]
            else:
                result.message = f"adw_prompt.py failed with code {proc.returncode}"
                result.details = [proc.stderr[:200] if proc.stderr else "No error"]
        except subprocess.TimeoutExpired:
            result.message = "adw_prompt.py timed out (>120s)"
        except Exception as e:
            result.message = f"Error: {str(e)[:100]}"
        results.append(result)

    # 3.2 Test slash command execution
    result = ValidationResult("3", "adw_slash_command.py execution")
    script_path = base_path / "adws" / "adw_slash_command.py"
    if not script_path.exists():
        result.message = "Script not found"
        results.append(result)
    else:
        try:
            proc = subprocess.run(
                [str(script_path), "/chore", "Jerry validation slash command test"],
                cwd=base_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "Slash command executed successfully"
                # Check specs/ directory for output
                specs_dir = base_path / "specs"
                if specs_dir.exists():
                    result.details = ["specs/ directory exists"]
            else:
                result.message = f"Slash command failed with code {proc.returncode}"
                result.details = [proc.stderr[:200] if proc.stderr else "No error"]
        except subprocess.TimeoutExpired:
            result.message = "Slash command timed out (>120s)"
        except Exception as e:
            result.message = f"Error: {str(e)[:100]}"
        results.append(result)

    # 3.3 Test worktree isolation (CRITICAL for JARI)
    result = ValidationResult("3", "Worktree isolation capability")
    script_path = base_path / "adws" / "adw_plan_iso.py"
    build_script_path = base_path / "adws" / "adw_build_iso.py"
    if not script_path.exists():
        result.message = "adw_plan_iso.py not found"
        result.passed = True  # Optional for minimal installs
        result.details = ["Worktree workflows not installed"]
        results.append(result)
    else:
        try:
            # Verify script is valid Python by checking syntax
            proc = subprocess.run(
                ["python3", "-m", "py_compile", str(script_path)],
                cwd=base_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "Worktree isolation scripts ready"
                result.details = ["adw_plan_iso.py syntax valid"]
                # Check build script too
                if build_script_path.exists():
                    result.details.append("adw_build_iso.py found")
                # Check trees/ directory exists or can be created
                trees_dir = base_path / "trees"
                if trees_dir.exists():
                    result.details.append("trees/ directory exists")
            else:
                result.message = f"Worktree script has syntax errors"
                result.details = [proc.stderr[:200] if proc.stderr else "No error"]
        except subprocess.TimeoutExpired:
            result.message = "Script syntax check timed out"
        except Exception as e:
            result.message = f"Error: {str(e)[:100]}"
        results.append(result)

    # 3.4 Check agents directory structure
    result = ValidationResult("3", "Agents output directory")
    agents_dir = base_path / "agents"
    if agents_dir.exists():
        result.passed = True
        result.message = "agents/ directory exists"
        subdirs = [d for d in agents_dir.iterdir() if d.is_dir()]
        result.details = [f"Found {len(subdirs)} agent execution(s)"]
    else:
        result.passed = True  # Not a failure, just means no workflows run yet
        result.message = "agents/ directory not yet created"
        result.details = ["Created after first workflow execution"]
    results.append(result)

    return results


def generate_adw_id() -> str:
    """Generate a unique 8-character ADW ID for validation tests."""
    import random
    import string
    return ''.join(random.choices(string.hexdigits.lower()[:16], k=8))


def cleanup_worktree(base_path: Path, adw_id: str) -> None:
    """Cleanup a test worktree after validation."""
    import shutil
    worktree_path = base_path / "trees" / adw_id
    agents_path = base_path / "agents" / adw_id

    # Remove worktree directory
    if worktree_path.exists():
        try:
            # First try git worktree remove
            subprocess.run(
                ["git", "worktree", "remove", str(worktree_path), "--force"],
                cwd=base_path,
                capture_output=True,
                timeout=30
            )
        except Exception:
            pass
        # If still exists, remove manually
        if worktree_path.exists():
            try:
                shutil.rmtree(worktree_path)
            except Exception:
                pass

    # Remove agents output directory
    if agents_path.exists():
        try:
            shutil.rmtree(agents_path)
        except Exception:
            pass


def validate_level_4(base_path: Path) -> List[ValidationResult]:
    """
    Level 4: Full SDLC Validation
    Test plan, build, and chore workflows with actual execution.
    This is the most comprehensive validation level.
    """
    results = []
    adw_id = f"validate-{generate_adw_id()}"
    issue_ref = "prompt:Jerry validation test - add health check"

    # 4.1 Plan workflow
    result = ValidationResult("4", "adw_plan_iso.py (full execution)")
    script_path = base_path / "adws" / "adw_plan_iso.py"
    if not script_path.exists():
        result.message = "adw_plan_iso.py not found"
        result.passed = True  # Skip if not available
        result.details = ["Worktree workflows not installed"]
        results.append(result)
    else:
        try:
            proc = subprocess.run(
                [str(script_path), issue_ref, adw_id],
                cwd=base_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "Plan workflow completed"
                worktree_path = base_path / "trees" / adw_id
                if worktree_path.exists():
                    result.details = ["Worktree created successfully"]
                agents_path = base_path / "agents" / adw_id
                if agents_path.exists():
                    result.details.append("Agent state created")
            else:
                result.message = f"Plan workflow failed with code {proc.returncode}"
                result.details = [proc.stderr[:300] if proc.stderr else "No error"]
        except subprocess.TimeoutExpired:
            result.message = "Plan workflow timed out (>5min)"
        except Exception as e:
            result.message = f"Error: {str(e)[:100]}"
        results.append(result)

    # 4.2 Build workflow (depends on successful plan)
    result = ValidationResult("4", "adw_build_iso.py (full execution)")
    script_path = base_path / "adws" / "adw_build_iso.py"
    plan_succeeded = results[-1].passed if results else False

    if not script_path.exists():
        result.message = "adw_build_iso.py not found"
        result.passed = True  # Skip if not available
        result.details = ["Build workflow not installed"]
        results.append(result)
    elif not plan_succeeded:
        result.message = "Skipped - plan workflow did not succeed"
        result.passed = True  # Skip if plan failed
        result.details = ["Build depends on successful plan"]
        results.append(result)
    else:
        try:
            # Build requires both issue-ref and adw-id
            proc = subprocess.run(
                [str(script_path), issue_ref, adw_id],
                cwd=base_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "Build workflow completed"
                result.details = ["Implementation executed in worktree"]
            else:
                result.message = f"Build workflow failed with code {proc.returncode}"
                result.details = [proc.stderr[:300] if proc.stderr else "No error"]
        except subprocess.TimeoutExpired:
            result.message = "Build workflow timed out (>5min)"
        except Exception as e:
            result.message = f"Error: {str(e)[:100]}"
        results.append(result)

    # 4.3 Verify directory structure
    result = ValidationResult("4", "Directory structure verification")
    trees_dir = base_path / "trees"
    agents_dir = base_path / "agents"

    if trees_dir.exists() and agents_dir.exists():
        result.passed = True
        result.message = "trees/ and agents/ directories exist"
        tree_count = len([d for d in trees_dir.iterdir() if d.is_dir()])
        agent_count = len([d for d in agents_dir.iterdir() if d.is_dir()])
        result.details = [f"{tree_count} worktrees, {agent_count} agent executions"]
    elif trees_dir.exists():
        result.passed = True
        result.message = "trees/ exists, agents/ may not exist yet"
    elif agents_dir.exists():
        result.passed = True
        result.message = "agents/ exists, trees/ may not exist yet"
    else:
        result.passed = True  # Not a failure for minimal installs
        result.message = "Neither trees/ nor agents/ exist yet"
        result.details = ["Created after first workflow execution"]
    results.append(result)

    # Cleanup test worktree
    cleanup_worktree(base_path, adw_id)

    return results


def validate_level_5(base_path: Path) -> List[ValidationResult]:
    """
    Level 5: Auth Validation
    Test GitHub/GitLab token authentication.
    Only runs if tokens are configured in environment.
    """
    results = []

    # 5.1 GitHub token auth check
    github_pat = os.getenv("GITHUB_PAT")
    if github_pat:
        result = ValidationResult("5", "GitHub token auth")
        try:
            env = {
                "GH_TOKEN": github_pat,
                "PATH": os.environ.get("PATH", ""),
                "HOME": os.environ.get("HOME", ""),
            }
            proc = subprocess.run(
                ["gh", "auth", "status"],
                env=env,
                capture_output=True,
                text=True,
                timeout=10
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "GitHub token authenticated"
                # Extract username if present
                if "Logged in to" in proc.stdout:
                    result.details = [proc.stdout.strip()[:100]]
            else:
                result.message = "GitHub token auth failed"
                result.details = [proc.stderr[:200] if proc.stderr else "No error details"]
        except FileNotFoundError:
            result.message = "GitHub CLI not installed"
            result.details = ["Cannot test token without gh CLI"]
        except subprocess.TimeoutExpired:
            result.message = "GitHub auth check timed out"
        except Exception as e:
            result.message = f"Error: {str(e)[:100]}"
        results.append(result)
    else:
        result = ValidationResult("5", "GitHub token auth")
        result.passed = True
        result.message = "Skipped - GITHUB_PAT not configured"
        result.details = ["Set GITHUB_PAT env var to enable"]
        results.append(result)

    # 5.2 GitLab token auth check
    gitlab_token = os.getenv("GITLAB_TOKEN")
    if gitlab_token:
        result = ValidationResult("5", "GitLab token auth")
        try:
            env = {
                "GITLAB_TOKEN": gitlab_token,
                "PATH": os.environ.get("PATH", ""),
                "HOME": os.environ.get("HOME", ""),
            }
            proc = subprocess.run(
                ["glab", "auth", "status"],
                env=env,
                capture_output=True,
                text=True,
                timeout=10
            )
            if proc.returncode == 0:
                result.passed = True
                result.message = "GitLab token authenticated"
                if "Logged in to" in proc.stdout:
                    result.details = [proc.stdout.strip()[:100]]
            else:
                result.message = "GitLab token auth failed"
                result.details = [proc.stderr[:200] if proc.stderr else "No error details"]
        except FileNotFoundError:
            result.message = "GitLab CLI not installed"
            result.details = ["Cannot test token without glab CLI"]
        except subprocess.TimeoutExpired:
            result.message = "GitLab auth check timed out"
        except Exception as e:
            result.message = f"Error: {str(e)[:100]}"
        results.append(result)
    else:
        result = ValidationResult("5", "GitLab token auth")
        result.passed = True
        result.message = "Skipped - GITLAB_TOKEN not configured"
        result.details = ["Set GITLAB_TOKEN env var to enable"]
        results.append(result)

    return results


def generate_validation_report(
    all_results: List[ValidationResult],
    output_path: Optional[Path] = None
) -> Dict[str, Any]:
    """Generate a comprehensive validation report."""
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_tests": len(all_results),
            "passed": sum(1 for r in all_results if r.passed),
            "failed": sum(1 for r in all_results if not r.passed)
        },
        "by_level": {},
        "tests": [r.to_dict() for r in all_results]
    }

    # Group by level
    for result in all_results:
        level = result.level
        if level not in report["by_level"]:
            report["by_level"][level] = {"passed": 0, "failed": 0}
        if result.passed:
            report["by_level"][level]["passed"] += 1
        else:
            report["by_level"][level]["failed"] += 1

    if output_path:
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

    return report


def display_results(results: List[ValidationResult], level_name: str):
    """Display validation results for a level."""
    console.print(f"\n[bold cyan]Level {results[0].level}: {level_name}[/bold cyan]")

    for result in results:
        status = "[green]✓[/green]" if result.passed else "[red]✗[/red]"
        console.print(f"{status} {result.name}: {result.message}")

        if result.details:
            for detail in result.details[:3]:  # Show first 3 details
                console.print(f"    {detail}", style="dim")


@click.command()
@click.option(
    "--level",
    "-l",
    type=click.Choice(["1", "2", "3", "4", "5", "all"]),
    default="all",
    help="Validation level (1=Import, 2=CLI, 3=Workflows, 4=Full SDLC, 5=Auth, all=All)",
)
@click.option(
    "--report",
    "-r",
    type=click.Path(path_type=Path),
    help="Output report to JSON file",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Minimal output (only show summary)",
)
def main(level: str, report: Optional[Path], quiet: bool):
    """Validate Jerry installation and readiness.

    Validation Levels:
    - Level 1: Import validation (modules load correctly)
    - Level 2: CLI validation (scripts executable, gh/glab available)
    - Level 3: Workflow validation (prompt, slash commands, worktree)
    - Level 4: Full SDLC validation (plan, build workflows)
    - Level 5: Auth validation (GitHub/GitLab token auth)
    """
    if not quiet:
        console.print(Panel.fit("🔍 Jerry Validation", style="bold blue"))

    # Determine base path (project root)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent

    all_results = []

    # Run requested validation levels
    levels_to_run = []
    if level == "all":
        levels_to_run = ["1", "2", "3", "4", "5"]
    else:
        levels_to_run = [level]

    for lvl in levels_to_run:
        if lvl == "1":
            results = validate_level_1(base_path)
            all_results.extend(results)
            if not quiet:
                display_results(results, "Import Validation")

        elif lvl == "2":
            results = validate_level_2(base_path)
            all_results.extend(results)
            if not quiet:
                display_results(results, "CLI Validation")

        elif lvl == "3":
            results = validate_level_3(base_path)
            all_results.extend(results)
            if not quiet:
                display_results(results, "Workflow Validation")

        elif lvl == "4":
            results = validate_level_4(base_path)
            all_results.extend(results)
            if not quiet:
                display_results(results, "Full SDLC Validation")

        elif lvl == "5":
            results = validate_level_5(base_path)
            all_results.extend(results)
            if not quiet:
                display_results(results, "Auth Validation")

    # Generate report
    validation_report = generate_validation_report(all_results, report)

    # Display summary
    passed = validation_report["summary"]["passed"]
    failed = validation_report["summary"]["failed"]
    total = validation_report["summary"]["total_tests"]

    console.print(f"\n[bold]Validation Summary:[/bold]")
    console.print(f"  Total tests: {total}")
    console.print(f"  [green]Passed: {passed}[/green]")
    console.print(f"  [red]Failed: {failed}[/red]")

    if report:
        console.print(f"\n[yellow]Report saved to: {report}[/yellow]")

    if failed > 0:
        console.print("\n[red]✗ Validation failed! Jerry may not function correctly.[/red]")
        sys.exit(1)
    else:
        console.print("\n[green]✓ All validation tests passed! Jerry is ready to use.[/green]")
        sys.exit(0)


if __name__ == "__main__":
    main()
