"""Diff generation for brainstorm version comparison.

This module generates per-pattern diffs when re-analyzing content,
showing exactly what insights changed between versions.
"""

import difflib
from pathlib import Path
from typing import Dict, Tuple, List

from adws.adw_modules.brainstorm_ops import get_brainstorm_dir


def generate_pattern_diff(
    pattern_name: str,
    old_output: str,
    new_output: str
) -> str:
    """Generate unified diff for a single pattern.

    Args:
        pattern_name: Name of the pattern
        old_output: Output from previous version
        new_output: Output from new version

    Returns:
        Unified diff string with context
    """
    old_lines = old_output.splitlines(keepends=True)
    new_lines = new_output.splitlines(keepends=True)

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"old/{pattern_name}",
        tofile=f"new/{pattern_name}",
        lineterm='',
        n=3  # 3 lines of context
    )

    return ''.join(diff)


def categorize_change(old_output: str, new_output: str) -> str:
    """Categorize the magnitude of change between two outputs.

    Args:
        old_output: Previous output
        new_output: New output

    Returns:
        "major" (>50% changed), "minor" (10-50%), or "no_change" (<10%)
    """
    if not old_output and not new_output:
        return "no_change"

    if not old_output or not new_output:
        return "major"

    # Calculate similarity using SequenceMatcher
    matcher = difflib.SequenceMatcher(None, old_output, new_output)
    similarity = matcher.ratio()

    if similarity >= 0.9:
        return "no_change"
    elif similarity >= 0.5:
        return "minor"
    else:
        return "major"


def load_pattern_output(version_dir: Path, pattern_name: str) -> str:
    """Load pattern output from version directory.

    Args:
        version_dir: Path to version directory
        pattern_name: Pattern name (e.g., "extract_wisdom")

    Returns:
        Pattern output content, or empty string if not found
    """
    # Pattern output is in: version_dir/patterns/{pattern_name}.md
    pattern_file = version_dir / "patterns" / f"{pattern_name}.md"

    if not pattern_file.exists():
        return ""

    try:
        return pattern_file.read_text()
    except Exception:
        return ""


def get_all_patterns(old_dir: Path, new_dir: Path) -> List[str]:
    """Get union of all patterns from both versions.

    Args:
        old_dir: Old version directory
        new_dir: New version directory

    Returns:
        Sorted list of unique pattern names
    """
    patterns = set()

    # Get patterns from old version
    old_patterns_dir = old_dir / "patterns"
    if old_patterns_dir.exists():
        for f in old_patterns_dir.glob("*.md"):
            patterns.add(f.stem)

    # Get patterns from new version
    new_patterns_dir = new_dir / "patterns"
    if new_patterns_dir.exists():
        for f in new_patterns_dir.glob("*.md"):
            patterns.add(f.stem)

    return sorted(patterns)


def generate_diff_summary(
    slug: str,
    old_version: str,
    new_version: str
) -> Tuple[str, str]:
    """Generate comprehensive diff summary between two versions.

    Args:
        slug: Analysis slug
        old_version: Previous version (e.g., "v1")
        new_version: New version (e.g., "v2")

    Returns:
        Tuple of (full_diff_markdown, brief_summary)

    Raises:
        ValueError: If versions don't exist
    """
    brainstorm_dir = get_brainstorm_dir()
    analysis_dir = brainstorm_dir / slug

    old_dir = analysis_dir / old_version
    new_dir = analysis_dir / new_version

    if not old_dir.exists():
        raise ValueError(f"Old version {old_version} not found for {slug}")

    if not new_dir.exists():
        raise ValueError(f"New version {new_version} not found for {slug}")

    # Get all patterns from both versions
    patterns = get_all_patterns(old_dir, new_dir)

    # Generate diffs for each pattern
    diff_parts = []
    diff_parts.append(f"# Diff: {old_version} → {new_version}\n\n")
    diff_parts.append(f"Analysis: **{slug}**\n\n")
    diff_parts.append(f"Comparing {old_version} to {new_version}\n\n")

    # Track statistics
    stats = {
        "major": [],
        "minor": [],
        "no_change": [],
        "added": [],
        "removed": []
    }

    diff_parts.append("## Summary of Changes\n\n")

    for pattern in patterns:
        old_output = load_pattern_output(old_dir, pattern)
        new_output = load_pattern_output(new_dir, pattern)

        # Categorize change
        if not old_output and new_output:
            stats["added"].append(pattern)
            category = "added"
        elif old_output and not new_output:
            stats["removed"].append(pattern)
            category = "removed"
        else:
            category = categorize_change(old_output, new_output)
            stats[category].append(pattern)

    # Write summary statistics
    if stats["major"]:
        diff_parts.append(f"**Major changes ({len(stats['major'])}):** ")
        diff_parts.append(", ".join(stats["major"]) + "\n\n")

    if stats["minor"]:
        diff_parts.append(f"**Minor changes ({len(stats['minor'])}):** ")
        diff_parts.append(", ".join(stats["minor"]) + "\n\n")

    if stats["added"]:
        diff_parts.append(f"**Added patterns ({len(stats['added'])}):** ")
        diff_parts.append(", ".join(stats["added"]) + "\n\n")

    if stats["removed"]:
        diff_parts.append(f"**Removed patterns ({len(stats['removed'])}):** ")
        diff_parts.append(", ".join(stats["removed"]) + "\n\n")

    if stats["no_change"]:
        diff_parts.append(f"**No changes ({len(stats['no_change'])}):** ")
        diff_parts.append(", ".join(stats["no_change"]) + "\n\n")

    # Generate detailed diffs for changed patterns
    diff_parts.append("\n## Detailed Pattern Diffs\n\n")

    for pattern in patterns:
        old_output = load_pattern_output(old_dir, pattern)
        new_output = load_pattern_output(new_dir, pattern)

        # Skip if no change
        if old_output == new_output:
            continue

        diff_parts.append(f"### {pattern}\n\n")

        if not old_output and new_output:
            diff_parts.append("**Status:** Added in this version\n\n")
            diff_parts.append("```markdown\n")
            diff_parts.append(new_output[:500])  # Show first 500 chars
            if len(new_output) > 500:
                diff_parts.append("\n... (truncated)")
            diff_parts.append("\n```\n\n")
        elif old_output and not new_output:
            diff_parts.append("**Status:** Removed in this version\n\n")
        else:
            category = categorize_change(old_output, new_output)
            diff_parts.append(f"**Change magnitude:** {category}\n\n")
            diff_parts.append("```diff\n")
            diff = generate_pattern_diff(pattern, old_output, new_output)
            diff_parts.append(diff)
            diff_parts.append("\n```\n\n")

    full_diff = "".join(diff_parts)

    # Generate brief summary
    total_changed = len(stats["major"]) + len(stats["minor"]) + len(stats["added"]) + len(stats["removed"])
    brief = f"{total_changed} patterns changed: "
    brief += f"{len(stats['major'])} major, "
    brief += f"{len(stats['minor'])} minor, "
    brief += f"{len(stats['added'])} added, "
    brief += f"{len(stats['removed'])} removed"

    return full_diff, brief


def write_diff_file(slug: str, new_version: str, old_version: str) -> Path:
    """Write diff summary to DIFF_FROM_vN.md in new version directory.

    Args:
        slug: Analysis slug
        new_version: New version (e.g., "v2")
        old_version: Previous version (e.g., "v1")

    Returns:
        Path to written diff file

    Raises:
        ValueError: If versions don't exist
    """
    full_diff, _ = generate_diff_summary(slug, old_version, new_version)

    brainstorm_dir = get_brainstorm_dir()
    version_dir = brainstorm_dir / slug / new_version
    diff_file = version_dir / f"DIFF_FROM_{old_version}.md"

    diff_file.write_text(full_diff)

    return diff_file
