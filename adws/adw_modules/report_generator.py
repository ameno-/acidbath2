"""Report generation for content analysis workflows.

Generates structured reports from pattern execution results:
- ANALYSIS_SUMMARY.md - Executive summary
- report.md - Full aggregated report
- metadata.json - Execution metadata
- index.html - Interactive dashboard (optional)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from .data_types import AnalysisMetadata, PatternResult, ContentObject


def generate_analysis_summary(
    content: ContentObject,
    results: Dict[str, PatternResult],
    output_dir: Path,
) -> Path:
    """Generate executive summary markdown.

    Args:
        content: Source content object
        results: Pattern execution results
        output_dir: Output directory

    Returns:
        Path to generated summary file
    """
    summary_path = output_dir / "ANALYSIS_SUMMARY.md"

    successful = [r for r in results.values() if r.success]
    failed = [r for r in results.values() if not r.success]

    lines = [
        f"# Analysis Summary",
        "",
        f"**Source:** {content.source}",
        f"**Type:** {content.type.value}",
        f"**Analyzed:** {datetime.now().isoformat()}",
        "",
        "## Results Overview",
        "",
        f"- **Patterns Executed:** {len(results)}",
        f"- **Successful:** {len(successful)}",
        f"- **Failed:** {len(failed)}",
        "",
    ]

    if successful:
        lines.extend([
            "## Key Insights",
            "",
        ])

        # Extract key insights from successful patterns
        for name, result in results.items():
            if result.success and result.output:
                lines.append(f"### {name}")
                # Take first 500 chars as preview
                preview = result.output[:500]
                if len(result.output) > 500:
                    preview += "..."
                lines.append(preview)
                lines.append("")

    if failed:
        lines.extend([
            "## Failed Patterns",
            "",
        ])
        for name, result in results.items():
            if not result.success:
                lines.append(f"- **{name}:** {result.error}")
        lines.append("")

    summary_path.write_text("\n".join(lines))
    return summary_path


def generate_full_report(
    content: ContentObject,
    results: Dict[str, PatternResult],
    output_dir: Path,
) -> Path:
    """Generate full aggregated report with all pattern outputs.

    Args:
        content: Source content object
        results: Pattern execution results
        output_dir: Output directory

    Returns:
        Path to generated report file
    """
    report_path = output_dir / "report.md"

    lines = [
        f"# Content Analysis Report",
        "",
        f"**Source:** {content.source}",
        f"**Type:** {content.type.value}",
        f"**Title:** {content.title or 'N/A'}",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "---",
        "",
    ]

    # Add each pattern's output as a section
    for name, result in results.items():
        lines.append(f"## {name}")
        lines.append("")

        if result.success:
            lines.append(result.output or "_No output_")
        else:
            lines.append(f"**Error:** {result.error}")

        lines.append("")
        lines.append("---")
        lines.append("")

    # Add content metadata
    if content.metadata:
        lines.extend([
            "## Content Metadata",
            "",
            "```json",
            json.dumps(content.metadata, indent=2, default=str),
            "```",
        ])

    report_path.write_text("\n".join(lines))
    return report_path


def generate_metadata_json(
    content: ContentObject,
    results: Dict[str, PatternResult],
    metadata: AnalysisMetadata,
    output_dir: Path,
) -> Path:
    """Generate metadata JSON file.

    Args:
        content: Source content object
        results: Pattern execution results
        metadata: Analysis execution metadata
        output_dir: Output directory

    Returns:
        Path to generated metadata file
    """
    metadata_path = output_dir / "metadata.json"

    data = {
        "source": content.source,
        "content_type": content.type.value,
        "title": content.title,
        "content_metadata": content.metadata,
        "execution": {
            "adw_id": metadata.adw_id,
            "timestamp": metadata.timestamp.isoformat() if metadata.timestamp else None,
            "execution_time": metadata.execution_time,
            "model": metadata.model_used,
            "patterns_executed": metadata.patterns_executed,
            "success": metadata.success,
        },
        "results": {
            name: {
                "success": result.success,
                "execution_time": result.execution_time,
                "error": result.error,
            }
            for name, result in results.items()
        },
    }

    metadata_path.write_text(json.dumps(data, indent=2, default=str))
    return metadata_path


def generate_html_dashboard(
    content: ContentObject,
    results: Dict[str, PatternResult],
    output_dir: Path,
) -> Path:
    """Generate interactive HTML dashboard.

    Args:
        content: Source content object
        results: Pattern execution results
        output_dir: Output directory

    Returns:
        Path to generated HTML file
    """
    html_path = output_dir / "index.html"

    successful = sum(1 for r in results.values() if r.success)
    failed = len(results) - successful

    # Build pattern sections
    pattern_sections = []
    for name, result in results.items():
        status_class = "success" if result.success else "error"
        content_html = result.output.replace("<", "&lt;").replace(">", "&gt;") if result.output else result.error or "No output"

        pattern_sections.append(f'''
        <div class="pattern {status_class}">
            <h3>{name}</h3>
            <pre>{content_html}</pre>
        </div>
        ''')

    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Analysis: {content.title or content.source}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .meta {{ background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .stat {{ background: #e8e8e8; padding: 15px 25px; border-radius: 8px; }}
        .stat.success {{ background: #d4edda; }}
        .stat.error {{ background: #f8d7da; }}
        .pattern {{ border: 1px solid #ddd; border-radius: 8px; margin-bottom: 15px; overflow: hidden; }}
        .pattern h3 {{ background: #f0f0f0; margin: 0; padding: 10px 15px; }}
        .pattern.success h3 {{ background: #d4edda; }}
        .pattern.error h3 {{ background: #f8d7da; }}
        .pattern pre {{ padding: 15px; margin: 0; white-space: pre-wrap; word-wrap: break-word; max-height: 400px; overflow-y: auto; }}
    </style>
</head>
<body>
    <h1>Content Analysis Dashboard</h1>

    <div class="meta">
        <p><strong>Source:</strong> {content.source}</p>
        <p><strong>Type:</strong> {content.type.value}</p>
        <p><strong>Title:</strong> {content.title or 'N/A'}</p>
    </div>

    <div class="stats">
        <div class="stat">Total: {len(results)}</div>
        <div class="stat success">Success: {successful}</div>
        <div class="stat error">Failed: {failed}</div>
    </div>

    <h2>Pattern Results</h2>
    {''.join(pattern_sections)}
</body>
</html>'''

    html_path.write_text(html)
    return html_path
