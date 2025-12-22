#!/usr/bin/env -S uv run
# /// script
# dependencies = ["click", "pypdf", "requests", "html2text", "beautifulsoup4", "pydantic", "python-dotenv", "claude-code-sdk", "pyyaml"]
# ///

"""
ADW Analyze Iso - Generic content analysis in isolated execution

Usage:
  uv run adw_analyze_iso.py <input-source> [options]

Input Sources:
  https://youtube.com/watch?v=...  - YouTube video
  https://example.com/article      - Web URL
  /path/to/document.pdf            - PDF file
  /path/to/notes.txt               - Text file
  -                                - Read from stdin

Options:
  --patterns, -p     Comma-separated pattern names (or 'all', 'core')
  --content-type, -t Force content type (youtube/url/pdf/text)
  --output-dir, -o   Output directory (default: agents/{adw_id}/analyze)
  --model, -m        Model for execution (haiku/sonnet, default: haiku)
  --parallel         Max parallel executions (default: 4)
  --quick            Use minimal pattern set for speed
  --full             Use all applicable patterns
  --dry-run          Show execution plan without running

Examples:
  ./adw_analyze_iso.py "https://youtube.com/watch?v=abc123"
  ./adw_analyze_iso.py ./paper.pdf --patterns extract_wisdom,extract_insights
  ./adw_analyze_iso.py https://blog.com/post --model sonnet
  cat article.txt | ./adw_analyze_iso.py - --patterns extract_wisdom
"""

import sys
import os
import json
import time
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import click

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adws.adw_modules.data_types import ContentType, SourceInfo, VersionInfo
from adws.adw_modules.content_extractors import detect_content_type, extract_content, ContentExtractionError
from adws.adw_modules.pattern_executor import (
    get_patterns_for_content_type,
    execute_patterns_parallel,
    validate_pattern_exists,
    load_preset,
    get_patterns_for_preset,
)
from adws.adw_modules.brainstorm_ops import (
    get_brainstorm_dir,
    init_brainstorm_dir,
    load_manifest,
    save_manifest,
    find_analysis_by_url,
    generate_slug,
    get_existing_slugs,
    get_next_version,
    create_version_dir,
    create_analysis_entry,
    add_version,
)
from adws.adw_modules.diff_ops import generate_diff_summary
from adws.adw_modules.report_generator import (
    generate_analysis_summary,
    generate_full_report,
    generate_metadata_json,
    generate_html_dashboard,
)
from adws.adw_modules.data_types import AnalysisMetadata, PatternResult
from adws.adw_modules.state import ADWState
from adws.adw_modules.utils import make_adw_id, setup_logger as setup_logger_fn


# Logger will be set up in main() after adw_id is determined
logger = None


@click.command()
@click.argument("input_source")
@click.option(
    "--patterns",
    "-p",
    default=None,
    help="Comma-separated pattern names (e.g., 'extract_wisdom,extract_insights')",
)
@click.option(
    "--content-type",
    "-t",
    type=click.Choice(["youtube", "url", "pdf", "text", "stdin"]),
    default=None,
    help="Force content type (auto-detected if not specified)",
)
@click.option(
    "--output-dir",
    "-o",
    default=None,
    help="Output directory (default: agents/{adw_id}/analyze)",
)
@click.option(
    "--model",
    "-m",
    type=click.Choice(["haiku", "sonnet"]),
    default="haiku",
    help="Model to use for pattern execution",
)
@click.option(
    "--parallel",
    default=4,
    type=int,
    help="Maximum number of parallel pattern executions",
)
@click.option(
    "--quick",
    is_flag=True,
    help="Use minimal core pattern set for speed",
)
@click.option(
    "--full",
    is_flag=True,
    help="Use all applicable patterns (core + specialized + conditional)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show execution plan without running",
)
@click.option(
    "--adw-id",
    default=None,
    help="Specify ADW ID (auto-generated if not provided)",
)
@click.option(
    "--brainstorm",
    is_flag=True,
    help="Save to persistent brainstorm directory with versioning",
)
@click.option(
    "--preset",
    default=None,
    help="Use pattern preset (e.g., 'acidbath') instead of individual patterns",
)
@click.option(
    "--slug",
    default=None,
    help="Custom slug for brainstorm analysis (auto-generated from title if not provided)",
)
@click.option(
    "--save-plan",
    is_flag=True,
    help="Save execution plan to PLAN.md in output directory (can combine with --dry-run)",
)
def main(
    input_source: str,
    patterns: Optional[str],
    content_type: Optional[str],
    output_dir: Optional[str],
    model: str,
    parallel: int,
    quick: bool,
    full: bool,
    dry_run: bool,
    adw_id: Optional[str],
    brainstorm: bool,
    preset: Optional[str],
    slug: Optional[str],
    save_plan: bool,
):
    """Analyze content using fabric patterns.

    Extracts content from various sources (YouTube, URLs, PDFs, text files)
    and executes fabric patterns to extract insights, wisdom, and recommendations.
    """
    try:
        # Generate or use provided ADW ID
        if not adw_id:
            adw_id = make_adw_id()

        # Setup logger now that we have adw_id
        global logger
        logger = setup_logger_fn(adw_id, "analyze")

        # Validate mutually exclusive flags
        if quick and full:
            logger.error("Cannot use both --quick and --full flags")
            sys.exit(1)

        logger.info(f"Starting content analysis [ADW ID: {adw_id}]")
        logger.info(f"Input source: {input_source}")

        # Brainstorm mode variables
        brainstorm_slug = None
        brainstorm_version = None
        previous_version = None
        is_reanalysis = False

        # Step 1: Detect content type
        if content_type:
            detected_type = ContentType(content_type)
            logger.info(f"Content type forced: {detected_type.value}")
        else:
            detected_type = detect_content_type(input_source)
            logger.info(f"Content type detected: {detected_type.value}")

        # Step 2: Determine output directory
        if not output_dir:
            output_dir = f"agents/{adw_id}/analyze"

        output_path = Path(output_dir).resolve()
        logger.info(f"Output directory: {output_path}")

        # Step 2b: Auto-detect brainstorm mode if output_dir is inside BRAINSTORM_DIR
        if not brainstorm and output_dir:
            brainstorm_dir = get_brainstorm_dir().resolve()
            try:
                # Check if output_path is inside brainstorm directory
                relative_path = output_path.relative_to(brainstorm_dir)
                # Extract slug from first path component (e.g., "finance-skills" from "finance-skills/")
                inferred_slug = relative_path.parts[0] if relative_path.parts else None
                if inferred_slug and inferred_slug not in ('.', '..'):
                    brainstorm = True
                    if not slug:
                        slug = inferred_slug
                    logger.info(f"Auto-detected brainstorm mode: output-dir is inside BRAINSTORM_DIR")
                    logger.info(f"Inferred slug: {slug}")
            except ValueError:
                # output_path is not inside brainstorm_dir, that's fine
                pass

        # Step 3: Select patterns
        if patterns:
            if patterns.lower() == "all":
                explicit_patterns = None
                full = True
            elif patterns.lower() == "core":
                explicit_patterns = None
                quick = True
            else:
                explicit_patterns = [p.strip() for p in patterns.split(",")]
        else:
            explicit_patterns = None

        if explicit_patterns:
            selected_patterns = explicit_patterns
        elif preset:
            # Load preset configuration and get pattern names
            try:
                selected_patterns = get_patterns_for_preset(preset)
                logger.info(f"Using preset '{preset}' with {len(selected_patterns)} patterns")
            except Exception as e:
                logger.error(f"Failed to load preset '{preset}': {e}")
                sys.exit(1)
        else:
            selected_patterns = get_patterns_for_content_type(detected_type.value)

        logger.info(f"Selected {len(selected_patterns)} patterns: {', '.join(selected_patterns)}")

        # Build execution plan content
        plan_lines = [
            "# Execution Plan",
            "",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**ADW ID**: {adw_id}",
            "",
            "## Configuration",
            "",
            f"- **Input Source**: {input_source}",
            f"- **Content Type**: {detected_type.value}",
            f"- **Extractor**: extract_{detected_type.value}_content",
            f"- **Model**: {model}",
            f"- **Max Parallel**: {parallel}",
            f"- **Output Directory**: {output_path}",
        ]
        if preset:
            plan_lines.append(f"- **Preset**: {preset}")
        if brainstorm:
            plan_lines.extend([
                "",
                "## Brainstorm Mode",
                "",
                f"- **Directory**: {get_brainstorm_dir()}",
            ])
            if slug:
                plan_lines.append(f"- **Custom Slug**: {slug}")
        plan_lines.extend([
            "",
            f"## Patterns ({len(selected_patterns)})",
            "",
        ])
        for p in selected_patterns:
            plan_lines.append(f"- {p}")
        plan_content = "\n".join(plan_lines)

        # Save plan if requested
        if save_plan:
            output_path.mkdir(parents=True, exist_ok=True)
            plan_file = output_path / "PLAN.md"
            plan_file.write_text(plan_content, encoding="utf-8")
            print(f"Execution plan saved to: {plan_file}")
            if logger:
                logger.info(f"Execution plan saved to: {plan_file}")

        # Dry run mode - print plan and exit
        if dry_run:
            print("\n" + "="*60)
            print("DRY RUN MODE - Execution Plan")
            print("="*60)
            print(f"Content Type: {detected_type.value}")
            print(f"Extractor: extract_{detected_type.value}_content")
            print(f"Patterns ({len(selected_patterns)}): {', '.join(selected_patterns)}")
            print(f"Model: {model}")
            print(f"Max Parallel: {parallel}")
            if brainstorm:
                # Show versioned output path for brainstorm mode
                brainstorm_base = get_brainstorm_dir()
                effective_slug = slug or "(auto-generated from title)"
                existing = find_analysis_by_url(input_source)
                if existing:
                    manifest = load_manifest()
                    entry = manifest.analyses[existing]
                    next_ver = f"v{len(entry.versions) + 1}"
                    print(f"Output Directory: {brainstorm_base}/{existing}/{next_ver}/ (re-analysis)")
                else:
                    print(f"Output Directory: {brainstorm_base}/{effective_slug}/v1/ (new)")
                print(f"Brainstorm Mode: ENABLED")
                print(f"  - Directory: {brainstorm_base}")
                if slug:
                    print(f"  - Slug: {slug}")
            else:
                print(f"Output Directory: {output_path}")
            print(f"ADW ID: {adw_id}")
            if preset:
                print(f"Preset: {preset}")
            print("="*60)
            return

        # Check pattern availability
        if selected_patterns and not validate_pattern_exists(selected_patterns[0]):
            logger.error("Pattern system not available. Ensure .jerry/patterns exists.")
            sys.exit(1)

        # Step 4: Extract content
        start_time = time.time()
        logger.info("Extracting content...")

        try:
            content_obj = extract_content(input_source, detected_type, output_dir=str(output_path))
            logger.info(f"Content extracted: {len(content_obj.text)} characters")
            logger.debug(f"Metadata: {json.dumps(content_obj.metadata, indent=2, default=str)}")
        except ContentExtractionError as e:
            logger.error(f"Content extraction failed: {str(e)}")
            sys.exit(1)

        # Step 4b: Handle brainstorm mode output directory
        if brainstorm:
            logger.info("Brainstorm mode enabled - setting up persistent storage")
            brainstorm_dir = init_brainstorm_dir()

            # Check for existing analysis by URL
            existing_slug = find_analysis_by_url(input_source)

            if existing_slug:
                # Re-analysis: use existing slug, increment version
                brainstorm_slug = existing_slug
                is_reanalysis = True
                manifest = load_manifest()
                entry = manifest.analyses[brainstorm_slug]
                previous_version = entry.latest_version
                brainstorm_version = get_next_version(brainstorm_slug)
                logger.info(f"Re-analysis detected: {brainstorm_slug} (v{previous_version} -> {brainstorm_version})")
            else:
                # New analysis: generate slug
                title = content_obj.title or content_obj.metadata.get("title", input_source[:50])
                if slug:
                    brainstorm_slug = slug
                else:
                    brainstorm_slug = generate_slug(title, get_existing_slugs())
                brainstorm_version = "v1"
                logger.info(f"New analysis: {brainstorm_slug} ({brainstorm_version})")

                # Create new entry in manifest
                manifest = load_manifest()
                source_info = SourceInfo(
                    type=detected_type.value,
                    url=input_source,
                    original_title=title
                )
                entry = create_analysis_entry(brainstorm_slug, title, source_info)
                manifest.analyses[brainstorm_slug] = entry
                manifest.total_analyses = len(manifest.analyses)
                save_manifest(manifest)

            # Create version directory and update output_path
            version_dir = create_version_dir(brainstorm_slug, brainstorm_version)
            output_path = version_dir
            logger.info(f"Output directory (brainstorm): {output_path}")

            # Save source content
            source_file = brainstorm_dir / brainstorm_slug / f"source.{detected_type.value}"
            source_file.write_text(content_obj.text, encoding="utf-8")

        # Step 5: Create output directory structure
        output_path.mkdir(parents=True, exist_ok=True)
        (output_path / "patterns").mkdir(exist_ok=True)

        # Write extracted content
        content_file = output_path / "content.txt"
        content_file.write_text(content_obj.text, encoding="utf-8")
        logger.info(f"Content saved to: {content_file}")

        # Step 6: Execute patterns
        logger.info(f"Executing {len(selected_patterns)} patterns in parallel (max {parallel})...")

        pattern_results = execute_patterns_parallel(
            patterns=selected_patterns,
            input_text=content_obj.text,
            model=model,
            max_workers=parallel,
        )

        # Save individual pattern outputs to patterns directory
        patterns_dir = output_path / "patterns"
        for pattern_name, result in pattern_results.items():
            if result.success and result.output:
                pattern_file = patterns_dir / f"{pattern_name}.md"
                pattern_file.write_text(result.output, encoding="utf-8")

        execution_time = time.time() - start_time
        logger.info(f"Pattern execution completed in {execution_time:.2f}s")

        # Log results
        successful = sum(1 for r in pattern_results.values() if r.success)
        failed = len(pattern_results) - successful
        logger.info(f"Results: {successful} successful, {failed} failed")

        # Step 7: Generate metadata
        metadata = AnalysisMetadata(
            input_source=input_source,
            content_type=detected_type.value,
            patterns_executed=list(pattern_results.keys()),
            execution_time=execution_time,
            model_used=model,
            adw_id=adw_id,
            timestamp=datetime.now(),
            success=(failed == 0),
            error_message=None if failed == 0 else f"{failed} patterns failed",
        )

        # Step 8: Generate reports
        logger.info("Generating reports...")

        # Summary
        summary_file = generate_analysis_summary(content_obj, pattern_results, output_path)
        logger.info(f"Summary saved to: {summary_file}")

        # Full report
        report_file = generate_full_report(content_obj, pattern_results, output_path)
        logger.info(f"Full report saved to: {report_file}")

        # Metadata JSON
        metadata_file = generate_metadata_json(content_obj, pattern_results, metadata, output_path)
        logger.info(f"Metadata saved to: {metadata_file}")

        # HTML dashboard
        html_file = generate_html_dashboard(content_obj, pattern_results, output_path)
        logger.info(f"HTML dashboard saved to: {html_file}")

        # Step 8b: Brainstorm post-processing (version info, diffs)
        diff_file = None
        if brainstorm and brainstorm_slug:
            logger.info("Updating brainstorm manifest...")

            # Generate diff if re-analysis
            changes_summary = None
            if is_reanalysis and previous_version:
                try:
                    full_diff, brief_summary = generate_diff_summary(
                        brainstorm_slug,
                        previous_version,
                        brainstorm_version
                    )
                    diff_file = output_path / f"DIFF_FROM_{previous_version}.md"
                    diff_file.write_text(full_diff, encoding="utf-8")
                    logger.info(f"Diff generated: {diff_file}")
                    changes_summary = brief_summary
                except Exception as e:
                    logger.warning(f"Failed to generate diff: {e}")

            # Add version info to manifest
            version_info = VersionInfo(
                version=brainstorm_version,
                date=datetime.now(),
                preset=preset,
                patterns_run=list(pattern_results.keys()),
                model=model,
                adw_id=adw_id,
                diff_from=previous_version if is_reanalysis else None,
                changes_summary=changes_summary
            )
            add_version(brainstorm_slug, version_info)
            logger.info(f"Brainstorm manifest updated: {brainstorm_slug} {brainstorm_version}")

        # Step 9: Update ADW state
        state = ADWState(adw_id)
        state.update(
            metadata={
                "content_type": detected_type.value,
                "content_source": input_source,
                "patterns_executed": list(pattern_results.keys()),
                "execution_time": execution_time,
                "model_used": model,
                "output_dir": str(output_path),
                "timestamp": metadata.timestamp.isoformat(),
            }
        )
        logger.info(f"ADW state updated for: {adw_id}")

        # Final summary
        print("\n" + "="*60)
        print("Analysis Complete!")
        print("="*60)
        print(f"ADW ID: {adw_id}")
        print(f"Content Type: {detected_type.value}")
        print(f"Patterns: {successful}/{len(pattern_results)} successful")
        print(f"Execution Time: {execution_time:.2f}s")
        print(f"Output Directory: {output_path}")
        if brainstorm:
            print(f"\nBrainstorm:")
            print(f"  - Slug: {brainstorm_slug}")
            print(f"  - Version: {brainstorm_version}")
            if is_reanalysis:
                print(f"  - Re-analysis from: {previous_version}")
            if preset:
                print(f"  - Preset: {preset}")
        print(f"\nReports:")
        print(f"  - Summary: {summary_file}")
        print(f"  - Full Report: {report_file}")
        print(f"  - HTML Dashboard: {html_file}")
        if diff_file:
            print(f"  - Diff: {diff_file}")
        print("="*60)

        # Exit with error code if any patterns failed
        if failed > 0:
            sys.exit(1)

    except Exception as e:
        if logger:
            logger.exception(f"Unexpected error: {str(e)}")
        else:
            print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
