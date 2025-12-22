#!/usr/bin/env -S uv run
# /// script
# dependencies = ["click", "rich", "pydantic", "python-dotenv", "claude-code-sdk"]
# ///

"""
ADW YouTube Iso - YouTube-specific analysis workflow

Specialized wrapper around Jerry's generic analysis workflow that optimizes
for YouTube video analysis with metadata extraction, transcript processing,
content classification, and multi-pattern analysis.

Usage:
  uv run adw_youtube_iso.py <youtube-url> [options]

Options:
  --mode, -m         Analysis mode: quick|full (default: full)
                     - quick: Fast haiku-based core patterns only (~60-90s)
                     - full: Comprehensive sonnet-based with all patterns (~120-180s)
  --output-dir, -o   Output directory (overrides default agents/{adw_id}/youtube/{video_id})
  --adw-id           Custom ADW ID (default: auto-generated)
  --no-audio         Skip audio summary generation
  --no-html          Skip HTML dashboard generation

Examples:
  # Quick analysis (fast mode, haiku model)
  ./adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode quick

  # Full analysis (comprehensive mode, sonnet model)
  ./adw_youtube_iso.py "https://youtube.com/watch?v=OIKTsVjTVJE" --mode full

  # Custom ADW ID with no audio
  ./adw_youtube_iso.py "https://youtu.be/OIKTsVjTVJE" --adw-id my-analysis --no-audio

Output Structure:
  agents/{adw_id}/youtube/{video_id}/
  ├── metadata.json              # Video metadata
  ├── transcript.txt             # Full transcript
  ├── content-type.txt           # Classification (technical/educational/general)
  ├── patterns/                  # Pattern analysis outputs
  │   ├── extract_wisdom.md
  │   ├── youtube_summary.md
  │   └── ...
  ├── ANALYSIS_SUMMARY.md        # Executive summary
  ├── aggregated-report.md       # Full detailed report
  ├── README.md                  # Navigation guide
  ├── index.html                 # Interactive dashboard (if --no-html not set)
  ├── audio/
  │   ├── audio-summary.txt      # Summary text
  │   └── audio-summary.mp3      # TTS audio (if available and --no-audio not set)
  └── adw_state.json             # Workflow state tracking
"""

import sys
import os
import re
import logging
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.utils import make_adw_id, create_youtube_output_dir
from adws.adw_modules.state import ADWState

# Rich console for pretty output
console = Console()

# Logger (will be set up after adw_id is determined)
logger = None


def extract_video_id(youtube_url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats.

    Supports:
    - Full URLs: https://youtube.com/watch?v=VIDEO_ID
    - Short URLs: https://youtu.be/VIDEO_ID
    - Video ID only: VIDEO_ID (must be exactly 11 characters)
    - URLs with timestamps: ...?v=VIDEO_ID&t=123s
    - URLs with playlists: ...?v=VIDEO_ID&list=...

    Args:
        youtube_url: YouTube URL or video ID

    Returns:
        Extracted video ID or None if invalid format

    Example:
        extract_video_id("https://youtube.com/watch?v=dQw4w9WgXcQ")
        # Returns: "dQw4w9WgXcQ"
    """
    # Try various YouTube URL patterns first (more specific)
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    # If no URL match and it's exactly 11 characters, treat as video ID
    # But only if it looks like a valid video ID (alphanumeric, -, _)
    if len(youtube_url) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', youtube_url):
        return youtube_url

    return None


@click.command()
@click.argument("youtube_url")
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["quick", "full"]),
    default="full",
    help="Analysis mode: quick (haiku, fast) or full (sonnet, comprehensive)",
)
@click.option(
    "--output-dir",
    "-o",
    default=None,
    help="Override default output directory",
)
@click.option(
    "--adw-id",
    default=None,
    help="Custom ADW ID (default: auto-generated)",
)
@click.option(
    "--no-audio",
    is_flag=True,
    help="Skip audio summary generation",
)
@click.option(
    "--no-html",
    is_flag=True,
    help="Skip HTML dashboard generation",
)
def main(
    youtube_url: str,
    mode: str,
    output_dir: Optional[str],
    adw_id: Optional[str],
    no_audio: bool,
    no_html: bool,
):
    """Execute YouTube video analysis workflow.

    This is the main entry point for YouTube analysis. It orchestrates:
    1. Video ID extraction and validation
    2. Output directory creation
    3. ADW state initialization
    4. Orchestrator agent execution (delegates to specialized agents)
    5. Result summary and exit code
    """
    global logger

    # Generate or use provided ADW ID
    if adw_id is None:
        adw_id = make_adw_id()

    # Extract video ID from URL
    video_id = extract_video_id(youtube_url)
    if video_id is None:
        console.print(
            Panel(
                f"[red]Invalid YouTube URL format:[/red] {youtube_url}\n\n"
                f"Supported formats:\n"
                f"  - https://youtube.com/watch?v=VIDEO_ID\n"
                f"  - https://youtu.be/VIDEO_ID\n"
                f"  - VIDEO_ID (11 characters)",
                title="Error",
                border_style="red",
            )
        )
        sys.exit(1)

    # Create output directory structure
    if output_dir is None:
        output_dir = create_youtube_output_dir(adw_id, video_id)
    else:
        # Use custom output dir
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        # Create subdirectories
        os.makedirs(os.path.join(output_dir, "patterns"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "audio"), exist_ok=True)

    # Display workflow start banner
    console.print()
    console.print(
        Panel(
            f"[bold cyan]YouTube Analysis Workflow[/bold cyan]\n\n"
            f"ADW ID: {adw_id}\n"
            f"Video ID: {video_id}\n"
            f"Mode: {mode}\n"
            f"Output: {output_dir}\n"
            f"Audio: {'disabled' if no_audio else 'enabled'}\n"
            f"HTML: {'disabled' if no_html else 'enabled'}",
            title="Workflow Configuration",
            border_style="cyan",
        )
    )
    console.print()

    # Initialize ADW state
    state = ADWState(adw_id=adw_id)
    state.update(
        phase="youtube_analysis",
        status="initializing",
        metadata={
            "video_id": video_id,
            "mode": mode,
            "output_dir": output_dir,
            "skip_audio": no_audio,
            "skip_html": no_html,
        }
    )

    # Import analysis modules
    from adws.adw_modules.youtube_ops import extract_youtube_content
    from adws.adw_modules.pattern_executor import (
        execute_patterns_parallel,
        get_patterns_for_content_type,
    )
    from adws.adw_modules.report_generator import (
        generate_analysis_summary,
        generate_full_report,
        generate_metadata_json,
        generate_html_dashboard,
    )
    from adws.adw_modules.data_types import ContentType, ContentObject, AnalysisMetadata, PatternResult
    from pathlib import Path
    from datetime import datetime
    import json
    import time

    start_time = time.time()

    # Step 1: Extract YouTube content
    console.print("[bold]Step 1:[/bold] Extracting YouTube content...")
    state.update(status="extracting")

    try:
        content = extract_youtube_content(youtube_url, output_dir)
        console.print(f"  [green]✓[/green] Title: {content.title}")
        console.print(f"  [green]✓[/green] Transcript: {len(content.text)} characters")
    except Exception as e:
        console.print(f"  [red]✗[/red] Failed to extract content: {e}")
        state.update(status="failed", error=str(e))
        return 1

    # Save transcript
    transcript_path = Path(output_dir) / "transcript.txt"
    transcript_path.write_text(content.text)
    console.print(f"  [green]✓[/green] Saved transcript to {transcript_path}")

    # Save metadata
    metadata_path = Path(output_dir) / "metadata.json"
    metadata_path.write_text(json.dumps(content.metadata or {}, indent=2, default=str))

    # Step 2: Select patterns based on mode
    console.print(f"\n[bold]Step 2:[/bold] Selecting patterns ({mode} mode)...")
    state.update(status="selecting_patterns")

    youtube_patterns = get_patterns_for_content_type("youtube")

    if mode == "quick":
        # Quick mode: just core patterns
        selected_patterns = ["extract_wisdom", "extract_insights"]
        model = "haiku"
    else:
        # Full mode: all YouTube patterns
        selected_patterns = youtube_patterns[:8] if len(youtube_patterns) > 8 else youtube_patterns
        model = "sonnet"

    console.print(f"  [green]✓[/green] Selected {len(selected_patterns)} patterns: {', '.join(selected_patterns)}")
    console.print(f"  [green]✓[/green] Model: {model}")

    # Step 3: Execute patterns
    console.print(f"\n[bold]Step 3:[/bold] Executing patterns...")
    state.update(status="executing_patterns")

    try:
        results = execute_patterns_parallel(
            patterns=selected_patterns,
            input_text=content.text,
            model=model,
            max_workers=4,
        )

        # Save individual pattern outputs
        patterns_dir = Path(output_dir) / "patterns"
        successful = 0
        failed = 0

        for pattern_name, result in results.items():
            if result.success:
                pattern_file = patterns_dir / f"{pattern_name}.md"
                pattern_file.write_text(result.output or "")
                successful += 1
            else:
                failed += 1
                console.print(f"  [yellow]⚠[/yellow] {pattern_name}: {result.error}")

        console.print(f"  [green]✓[/green] Completed: {successful} successful, {failed} failed")

    except Exception as e:
        console.print(f"  [red]✗[/red] Pattern execution failed: {e}")
        state.update(status="failed", error=str(e))
        return 1

    # Step 4: Generate reports
    console.print(f"\n[bold]Step 4:[/bold] Generating reports...")
    state.update(status="generating_reports")

    output_path = Path(output_dir)

    # Create analysis metadata
    analysis_metadata = AnalysisMetadata(
        input_source=youtube_url,
        content_type="youtube",
        patterns_executed=list(results.keys()),
        execution_time=time.time() - start_time,
        model_used=model,
        adw_id=adw_id,
        success=successful > 0,
    )

    try:
        # Generate summary
        summary_path = generate_analysis_summary(content, results, output_path)
        console.print(f"  [green]✓[/green] Summary: {summary_path}")

        # Generate full report
        report_path = generate_full_report(content, results, output_path)
        console.print(f"  [green]✓[/green] Report: {report_path}")

        # Generate metadata JSON
        meta_path = generate_metadata_json(content, results, analysis_metadata, output_path)
        console.print(f"  [green]✓[/green] Metadata: {meta_path}")

        # Generate HTML dashboard if enabled
        if not no_html:
            html_path = generate_html_dashboard(content, results, output_path)
            console.print(f"  [green]✓[/green] Dashboard: {html_path}")

    except Exception as e:
        console.print(f"  [yellow]⚠[/yellow] Report generation warning: {e}")

    # Calculate elapsed time
    elapsed = time.time() - start_time
    state.update(status="completed", elapsed_time=elapsed)

    # Display completion summary
    console.print()
    console.print(
        Panel(
            f"[green]✓[/green] YouTube analysis completed!\n\n"
            f"ADW ID: {adw_id}\n"
            f"Video ID: {video_id}\n"
            f"Title: {content.title}\n"
            f"Patterns: {successful}/{len(selected_patterns)} successful\n"
            f"Time: {elapsed:.1f}s\n"
            f"Output: {output_dir}",
            title="Analysis Complete",
            border_style="green",
        )
    )
    console.print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
