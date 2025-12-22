#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml", "click", "rich"]
# ///

"""
ADW Metaplan Iso - Generate execution metaplans for multi-phase features

Usage:
  uv run adw_metaplan_iso.py <feature-tracking-doc> [--output <path>]

This workflow reads a feature tracking document (like specs/FEATURE_NAME.md)
that references multiple phase specs, and generates a structured metaplan
for execution by the feature-orchestrator agent.

Workflow Position:
  1. adw_plan_iso.py (per phase) → Individual specs
  2. adw_metaplan_iso.py         → Aggregated metaplan  ← THIS WORKFLOW
  3. feature-orchestrator agent  → Execution

Input: Feature tracking document with:
  - Phase table (ADW IDs, issues, specs, dependencies)
  - Worktree locations
  - Dependency graph

Output: Structured metaplan with:
  - Execution order (respecting dependencies)
  - Parallel groups (phases that can run concurrently)
  - Build commands per phase
  - Test checklists per phase
  - Review criteria per phase
  - Commit message templates
  - Final validation commands
  - Status tracking table
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.utils import setup_logger
from adws.adw_modules.agent import execute_template
from adws.adw_modules.data_types import AgentTemplateRequest

console = Console()

METAPLAN_PROMPT = """
You are generating a structured metaplan for feature execution.

# Input Documents

## Feature Tracking Document
{feature_doc}

## Phase Specs
{phase_specs}

# Task

Generate a comprehensive metaplan that the feature-orchestrator agent can execute.

# Required Sections

## 1. Feature Summary
Brief description of the feature and its goals.

## 2. Phases Table
| Phase | ADW ID | Issue | Worktree | Branch | Depends On |
(Extract from feature tracking doc)

## 3. Execution Order
Show dependency graph and identify:
- Sequential phases (must wait for dependencies)
- Parallel groups (can run concurrently)

## 4. For Each Phase
Create a section "## Phase N: [Name]" with:

### Build
```bash
uv run ./adws/adw_build_iso.py local:[issue-name] [adw-id]
```

### Pre-Build (if has dependencies)
```bash
cd trees/[adw-id]
git fetch origin [dependency-branch]
git merge FETCH_HEAD --no-edit -m "Merge dependency"
```

### Test Checklist
Extract from the phase spec's "Validation Commands" or "Testing Strategy" section.
Format as numbered test commands with expected outputs:
```bash
# T[phase].[num]: [Description]
[command]
# Expected: [expected output]
```

### Review Criteria
Extract from phase spec's "Acceptance Criteria" section.
Format as checklist:
- [ ] Criterion 1
- [ ] Criterion 2

### On Success
```bash
cd trees/[adw-id]
git add -A
git commit -m "[commit message from spec]"
git push origin [branch-name]
```

## 5. Final Validation
Commands to run after all phases complete to verify the full feature works.

## 6. Aggregation
```bash
git checkout [aggregator-branch]
for branch in [all-phase-branches]; do
  git merge origin/$branch --no-ff -m "Merge $branch"
done
```

## 7. Execution Status
| Phase | ADW ID | Build | Test | Review | Merged |
|-------|--------|-------|------|--------|--------|
(All phases with ⏳ status initially)

## 8. Documentation Updates
List all docs that need updating after feature completion.

# Output Format

Output ONLY the metaplan markdown content. No commentary or explanation.
Start with "# Metaplan: [Feature Name]"
"""


def extract_phase_table(content: str) -> list[dict]:
    """Extract phase information from feature tracking doc."""
    phases = []

    # Look for phase table
    table_match = re.search(
        r'\|\s*Phase\s*\|\s*ADW ID\s*\|.*?\n\|[-\s|]+\n((?:\|.*\n)+)',
        content,
        re.IGNORECASE
    )

    if table_match:
        rows = table_match.group(1).strip().split('\n')
        for row in rows:
            cols = [c.strip() for c in row.split('|')[1:-1]]
            if len(cols) >= 5:
                phases.append({
                    'phase': cols[0],
                    'adw_id': cols[1].strip('`'),
                    'issue': cols[2],
                    'spec': cols[3] if len(cols) > 3 else '',
                    'depends_on': cols[5] if len(cols) > 5 else '',
                })

    return phases


def read_phase_specs(phases: list[dict], specs_dir: Path) -> dict[str, str]:
    """Read spec content for each phase."""
    specs = {}

    for phase in phases:
        adw_id = phase['adw_id']

        # Try to find spec file
        spec_patterns = [
            f"feature-{adw_id}-*.md",
            f"feature-*-{adw_id}-*.md",
            f"*{adw_id}*.md",
        ]

        for pattern in spec_patterns:
            matches = list(specs_dir.glob(pattern))
            if matches:
                spec_path = matches[0]
                specs[adw_id] = spec_path.read_text()
                break

    return specs


@click.command()
@click.argument('feature_doc', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output path for metaplan')
@click.option('--dry-run', is_flag=True, help='Show what would be generated')
def generate_metaplan(feature_doc: str, output: str, dry_run: bool):
    """
    Generate execution metaplan from feature tracking document.

    FEATURE_DOC: Path to feature tracking document (e.g., specs/FEATURE_NAME.md)
    """
    feature_path = Path(feature_doc)
    console.print(f"[bold]Reading feature document:[/bold] {feature_path}")

    # Read feature tracking doc
    feature_content = feature_path.read_text()

    # Extract phases
    phases = extract_phase_table(feature_content)
    if not phases:
        console.print("[red]Error: Could not extract phase table from document[/red]")
        sys.exit(1)

    console.print(f"[bold]Found {len(phases)} phases[/bold]")

    # Show phases table
    table = Table(title="Phases")
    table.add_column("Phase")
    table.add_column("ADW ID")
    table.add_column("Issue")
    table.add_column("Depends On")

    for p in phases:
        table.add_row(p['phase'], p['adw_id'], p['issue'], p['depends_on'])

    console.print(table)

    # Read phase specs
    specs_dir = feature_path.parent
    phase_specs = read_phase_specs(phases, specs_dir)

    console.print(f"[bold]Read {len(phase_specs)} spec files[/bold]")

    if dry_run:
        console.print("\n[yellow]DRY RUN - Would generate metaplan with:[/yellow]")
        console.print(f"  - {len(phases)} phases")
        console.print(f"  - {len(phase_specs)} specs")
        console.print(f"  - Output: {output or feature_path.stem + '_METAPLAN.md'}")
        return

    # Format specs for prompt
    specs_text = "\n\n".join([
        f"### Phase {adw_id}\n\n{content[:5000]}..."  # Truncate long specs
        for adw_id, content in phase_specs.items()
    ])

    # Generate metaplan using agent
    console.print("\n[bold]Generating metaplan...[/bold]")

    prompt = METAPLAN_PROMPT.format(
        feature_doc=feature_content,
        phase_specs=specs_text,
    )

    request = AgentTemplateRequest(
        agent_name="ops",
        slash_command="/prompt",
        args=[prompt],
        adw_id="metaplan",
    )

    response = execute_template(request)

    if not response.success:
        console.print(f"[red]Error generating metaplan: {response.output}[/red]")
        sys.exit(1)

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = feature_path.parent / f"{feature_path.stem}_METAPLAN.md"

    # Write metaplan
    output_path.write_text(response.output)

    console.print(f"\n[bold green]Metaplan generated:[/bold green] {output_path}")
    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  1. Review the metaplan: cat {output_path}")
    console.print(f"  2. Execute with: Use feature-orchestrator agent with {output_path}")


if __name__ == "__main__":
    generate_metaplan()
