#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Plan Build Iso - Compositional workflow for isolated planning and building

Usage: uv run adw_plan_build_iso.py <issue-number> [adw-id] [--dry-run]

This script runs:
1. adw_plan_iso.py - Planning phase (isolated)
2. adw_build_iso.py - Implementation phase (isolated)

The scripts are chained together via persistent state (adw_state.json).
"""

import subprocess
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from adws.adw_modules.workflow_ops import ensure_adw_id


def main():
    """Main entry point."""
    # Parse arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    flags = [arg for arg in sys.argv[1:] if arg.startswith("--")]
    dry_run = "--dry-run" in flags

    if len(args) < 1:
        print("Usage: uv run adw_plan_build_iso.py <issue-number> [adw-id] [--dry-run]")
        print("\nThis runs the isolated plan and build workflow:")
        print("  1. Plan (isolated)")
        print("  2. Build (isolated)")
        print("\nOptions:")
        print("  --dry-run    Validate without executing (passes flag to sub-workflows)")
        sys.exit(1)

    issue_number = args[0]
    adw_id = args[1] if len(args) > 1 else None

    # Ensure ADW ID exists with initialized state
    adw_id = ensure_adw_id(issue_number, adw_id)
    print(f"Using ADW ID: {adw_id}")

    if dry_run:
        print("\n[DRY RUN MODE] - Will pass --dry-run to sub-workflows")

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Run isolated plan with the ADW ID
    plan_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_plan_iso.py"),
        issue_number,
        adw_id,
    ]
    if dry_run:
        plan_cmd.append("--dry-run")

    print(f"\n=== ISOLATED PLAN PHASE ===")
    print(f"Running: {' '.join(plan_cmd)}")

    if not dry_run:
        plan = subprocess.run(plan_cmd)
        if plan.returncode != 0:
            print("Isolated plan phase failed")
            sys.exit(1)
    else:
        print("[DRY RUN] Would execute: adw_plan_iso.py")

    # Run isolated build with the ADW ID
    build_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_build_iso.py"),
        issue_number,
        adw_id,
    ]
    if dry_run:
        build_cmd.append("--dry-run")

    print(f"\n=== ISOLATED BUILD PHASE ===")
    print(f"Running: {' '.join(build_cmd)}")

    if not dry_run:
        build = subprocess.run(build_cmd)
        if build.returncode != 0:
            print("Isolated build phase failed")
            sys.exit(1)
    else:
        print("[DRY RUN] Would execute: adw_build_iso.py")

    print(f"\n=== ISOLATED WORKFLOW COMPLETED ===")
    print(f"ADW ID: {adw_id}")
    if dry_run:
        print("[DRY RUN] All phases validated successfully!")
    else:
        print("All phases completed successfully!")


if __name__ == "__main__":
    main()
