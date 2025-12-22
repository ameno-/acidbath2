"""Diff visualization module for generating visual representations of code changes.

Provides utilities to create screenshot-style images of code diffs for non-UI changes.
This helps provide visual evidence in code reviews where traditional screenshots aren't applicable.
"""

import logging
import subprocess
from pathlib import Path
from typing import Optional, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import TerminalFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


logger = logging.getLogger(__name__)


def generate_diff_screenshot(
    branch_name: str,
    output_path: str,
    cwd: Optional[str] = None,
    base_branch: str = "origin/main",
    max_lines: int = 500,
) -> Tuple[bool, Optional[str]]:
    """Generate a screenshot-style image of code diff.

    Args:
        branch_name: The feature branch name
        output_path: Path where the image should be saved (PNG or JPEG)
        cwd: Working directory for git operations
        base_branch: Base branch to compare against (default: origin/main)
        max_lines: Maximum lines to include in visualization (default: 500)

    Returns:
        Tuple of (success, error_message)
    """
    if not PILLOW_AVAILABLE:
        return False, "Pillow not available. Install with: pip install pillow"

    try:
        # Get diff content
        result = subprocess.run(
            ["git", "diff", f"{base_branch}..HEAD", "--unified=3"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, f"Failed to generate diff: {result.stderr}"

        diff_content = result.stdout

        if not diff_content.strip():
            # No diff content, generate a placeholder
            return _generate_no_diff_image(output_path)

        # Split into lines and truncate if too long
        diff_lines = diff_content.split("\n")
        if len(diff_lines) > max_lines:
            logger.warning(f"Diff too large ({len(diff_lines)} lines), using abstract visualization")
            return generate_abstract_visualization(branch_name, output_path, cwd, base_branch)

        # Create image with diff content
        return _render_diff_image(diff_lines, output_path)

    except Exception as e:
        logger.error(f"Error generating diff screenshot: {e}")
        return False, str(e)


def generate_abstract_visualization(
    branch_name: str,
    output_path: str,
    cwd: Optional[str] = None,
    base_branch: str = "origin/main",
) -> Tuple[bool, Optional[str]]:
    """Generate an abstract visualization showing high-level change statistics.

    This is used when diffs are too large for detailed visualization.

    Args:
        branch_name: The feature branch name
        output_path: Path where the image should be saved
        cwd: Working directory for git operations
        base_branch: Base branch to compare against (default: origin/main)

    Returns:
        Tuple of (success, error_message)
    """
    if not PILLOW_AVAILABLE:
        return False, "Pillow not available. Install with: pip install pillow"

    try:
        # Get file statistics
        result = subprocess.run(
            ["git", "diff", f"{base_branch}..HEAD", "--stat"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return False, f"Failed to generate diff stats: {result.stderr}"

        stats_content = result.stdout

        # Get commit count
        commit_result = subprocess.run(
            ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        commit_count = commit_result.stdout.strip() if commit_result.returncode == 0 else "?"

        # Parse stats for summary
        lines = stats_content.strip().split("\n")
        summary_line = lines[-1] if lines else "No changes"

        # Create abstract visualization image
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color='#1e1e1e')
        draw = ImageDraw.Draw(img)

        # Try to load a monospace font, fallback to default
        try:
            font_title = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 24)
            font_body = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 14)
            font_small = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 12)
        except:
            font_title = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Draw title
        title = f"Code Changes: {branch_name}"
        draw.text((20, 20), title, fill='#4ec9b0', font=font_title)

        # Draw commit count
        y_offset = 70
        draw.text((20, y_offset), f"Commits: {commit_count}", fill='#d4d4d4', font=font_body)
        y_offset += 40

        # Draw summary
        draw.text((20, y_offset), "Change Summary:", fill='#569cd6', font=font_body)
        y_offset += 30
        draw.text((20, y_offset), summary_line, fill='#d4d4d4', font=font_small)
        y_offset += 40

        # Draw file statistics (top 15 files)
        draw.text((20, y_offset), "Modified Files:", fill='#569cd6', font=font_body)
        y_offset += 30

        file_lines = [line for line in lines[:-1] if line.strip() and '|' in line][:15]
        for line in file_lines:
            # Truncate long file paths
            if len(line) > 80:
                line = line[:77] + "..."
            color = '#d4d4d4'
            if '+' in line and '-' not in line:
                color = '#6a9955'  # Green for additions
            elif '-' in line and '+' not in line:
                color = '#f48771'  # Red for deletions
            draw.text((20, y_offset), line, fill=color, font=font_small)
            y_offset += 20
            if y_offset > height - 40:
                break

        # Save image
        img.save(output_path)
        logger.info(f"Generated abstract visualization: {output_path}")
        return True, None

    except Exception as e:
        logger.error(f"Error generating abstract visualization: {e}")
        return False, str(e)


def _render_diff_image(diff_lines: list[str], output_path: str) -> Tuple[bool, Optional[str]]:
    """Render diff lines as an image with syntax highlighting colors.

    Args:
        diff_lines: Lines of diff output
        output_path: Path to save the image

    Returns:
        Tuple of (success, error_message)
    """
    # Image dimensions
    font_size = 12
    line_height = 16
    padding = 20
    width = 1200
    height = min(len(diff_lines) * line_height + 2 * padding, 4000)  # Cap at reasonable height

    # Create image
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    # Try to load a monospace font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", font_size)
    except:
        font = ImageFont.load_default()

    # Draw each line with appropriate color
    y_offset = padding
    for line in diff_lines[:min(len(diff_lines), 200)]:  # Limit to 200 lines
        # Truncate very long lines
        if len(line) > 140:
            line = line[:137] + "..."

        # Color based on diff markers
        if line.startswith('+'):
            color = '#6a9955'  # Green for additions
        elif line.startswith('-'):
            color = '#f48771'  # Red for deletions
        elif line.startswith('@@'):
            color = '#569cd6'  # Blue for chunk headers
        elif line.startswith('diff --git') or line.startswith('index '):
            color = '#4ec9b0'  # Cyan for file headers
        else:
            color = '#d4d4d4'  # Default gray

        draw.text((padding, y_offset), line, fill=color, font=font)
        y_offset += line_height

        if y_offset > height - padding:
            break

    # Save image
    img.save(output_path)
    logger.info(f"Generated diff screenshot: {output_path}")
    return True, None


def _generate_no_diff_image(output_path: str) -> Tuple[bool, Optional[str]]:
    """Generate a placeholder image when there's no diff.

    Args:
        output_path: Path to save the image

    Returns:
        Tuple of (success, error_message)
    """
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 20)
    except:
        font = ImageFont.load_default()

    message = "No changes detected"
    # Center the text
    bbox = draw.textbbox((0, 0), message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    draw.text((x, y), message, fill='#d4d4d4', font=font)

    img.save(output_path)
    logger.info(f"Generated no-diff placeholder: {output_path}")
    return True, None


def get_diff_stats(
    base_branch: str = "origin/main",
    cwd: Optional[str] = None,
) -> dict:
    """Get statistics about the diff.

    Args:
        base_branch: Base branch to compare against
        cwd: Working directory for git operations

    Returns:
        Dictionary with diff statistics
    """
    try:
        # Get file count and line stats
        result = subprocess.run(
            ["git", "diff", f"{base_branch}..HEAD", "--shortstat"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode != 0:
            return {"error": result.stderr}

        stats_text = result.stdout.strip()

        # Parse stats (format: "X files changed, Y insertions(+), Z deletions(-)")
        stats = {
            "files_changed": 0,
            "insertions": 0,
            "deletions": 0,
        }

        if "file" in stats_text:
            parts = stats_text.split(",")
            for part in parts:
                part = part.strip()
                if "file" in part:
                    stats["files_changed"] = int(part.split()[0])
                elif "insertion" in part:
                    stats["insertions"] = int(part.split()[0])
                elif "deletion" in part:
                    stats["deletions"] = int(part.split()[0])

        return stats

    except Exception as e:
        logger.error(f"Error getting diff stats: {e}")
        return {"error": str(e)}
