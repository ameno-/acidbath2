#!/usr/bin/env python3
"""
Audit all code blocks in blog posts and generate statistics.
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

def extract_code_blocks(markdown_content: str, filepath: str) -> List[Dict[str, Any]]:
    """Extract all code blocks from markdown with metadata."""
    blocks = []

    # Pattern to match code blocks with optional language
    pattern = r'```(\w*)\n(.*?)```'

    # Split content into lines for context extraction
    lines = markdown_content.split('\n')

    # Find all code blocks
    for match in re.finditer(pattern, markdown_content, re.DOTALL):
        language = match.group(1) or 'unknown'
        code = match.group(2)
        line_count = len(code.strip().split('\n'))

        # Find the line number where this code block starts
        start_pos = match.start()
        line_num = markdown_content[:start_pos].count('\n') + 1

        # Extract context (previous heading)
        context = extract_context(lines, line_num)

        blocks.append({
            'language': language,
            'line_count': line_count,
            'filepath': filepath,
            'line_number': line_num,
            'context': context,
            'code_preview': code.strip()[:100] + '...' if len(code.strip()) > 100 else code.strip()
        })

    return blocks

def extract_context(lines: List[str], code_line_num: int) -> str:
    """Extract the nearest heading before the code block."""
    # Search backwards from code block to find the last heading
    for i in range(code_line_num - 1, max(0, code_line_num - 50), -1):
        if i < len(lines) and lines[i].startswith('#'):
            return lines[i].strip()
    return "No context"

def categorize_code_block(block: Dict[str, Any]) -> str:
    """Categorize code block based on size and content."""
    line_count = block['line_count']
    language = block['language']

    # Categorization logic
    if language in ['mermaid', 'diff']:
        return 'diagram'
    elif line_count >= 40:
        return 'complete_example'
    elif line_count <= 20:
        return 'snippet'
    elif language in ['json', 'yaml', 'yml', 'toml', 'ini', 'env']:
        return 'configuration'
    else:
        return 'medium_example'

def analyze_blog_posts(blog_dir: Path) -> Dict[str, Any]:
    """Analyze all blog posts and extract code block statistics."""
    all_blocks = []
    post_stats = {}

    # Process each blog post
    for post_path in sorted(blog_dir.glob('*.md')):
        content = post_path.read_text()
        blocks = extract_code_blocks(content, str(post_path))

        # Categorize each block
        for block in blocks:
            block['category'] = categorize_code_block(block)

        all_blocks.extend(blocks)
        post_stats[post_path.name] = {
            'total_blocks': len(blocks),
            'blocks': blocks
        }

    # Generate overall statistics
    language_stats = defaultdict(int)
    category_stats = defaultdict(int)
    size_distribution = {'1-10': 0, '11-20': 0, '21-40': 0, '41-100': 0, '100+': 0}

    for block in all_blocks:
        language_stats[block['language']] += 1
        category_stats[block['category']] += 1

        # Size distribution
        lc = block['line_count']
        if lc <= 10:
            size_distribution['1-10'] += 1
        elif lc <= 20:
            size_distribution['11-20'] += 1
        elif lc <= 40:
            size_distribution['21-40'] += 1
        elif lc <= 100:
            size_distribution['41-100'] += 1
        else:
            size_distribution['100+'] += 1

    return {
        'total_posts': len(post_stats),
        'total_blocks': len(all_blocks),
        'post_stats': post_stats,
        'language_stats': dict(language_stats),
        'category_stats': dict(category_stats),
        'size_distribution': size_distribution,
        'all_blocks': all_blocks
    }

def generate_report(stats: Dict[str, Any], output_path: Path):
    """Generate markdown report from statistics."""
    report = []

    report.append("# Code Block Audit Report\n")
    report.append(f"**Generated:** {Path(__file__).name}\n")
    report.append(f"**Total Blog Posts:** {stats['total_posts']}\n")
    report.append(f"**Total Code Blocks:** {stats['total_blocks']}\n\n")

    # Per-post statistics
    report.append("## Per-Post Statistics\n")
    sorted_posts = sorted(stats['post_stats'].items(),
                         key=lambda x: x[1]['total_blocks'],
                         reverse=True)

    report.append("| Post | Total Blocks | Complete Examples | Snippets | Configs | Diagrams |\n")
    report.append("|------|--------------|-------------------|----------|---------|----------|\n")

    for post_name, post_data in sorted_posts:
        blocks = post_data['blocks']
        complete = sum(1 for b in blocks if b['category'] == 'complete_example')
        snippets = sum(1 for b in blocks if b['category'] == 'snippet')
        configs = sum(1 for b in blocks if b['category'] == 'configuration')
        diagrams = sum(1 for b in blocks if b['category'] == 'diagram')

        report.append(f"| {post_name} | {post_data['total_blocks']} | {complete} | {snippets} | {configs} | {diagrams} |\n")

    report.append("\n## Language Distribution\n")
    sorted_langs = sorted(stats['language_stats'].items(),
                         key=lambda x: x[1],
                         reverse=True)

    report.append("| Language | Count | Percentage |\n")
    report.append("|----------|-------|------------|\n")

    for lang, count in sorted_langs:
        pct = (count / stats['total_blocks']) * 100
        report.append(f"| {lang or 'unknown'} | {count} | {pct:.1f}% |\n")

    report.append("\n## Category Distribution\n")
    report.append("| Category | Count | Percentage |\n")
    report.append("|----------|-------|------------|\n")

    for category, count in stats['category_stats'].items():
        pct = (count / stats['total_blocks']) * 100
        report.append(f"| {category} | {count} | {pct:.1f}% |\n")

    report.append("\n## Size Distribution\n")
    report.append("| Lines | Count | Percentage |\n")
    report.append("|-------|-------|------------|\n")

    for size_range, count in stats['size_distribution'].items():
        pct = (count / stats['total_blocks']) * 100
        report.append(f"| {size_range} | {count} | {pct:.1f}% |\n")

    # Recommendations
    report.append("\n## Recommendations\n\n")

    complete_count = stats['category_stats'].get('complete_example', 0)
    medium_count = stats['category_stats'].get('medium_example', 0)

    report.append(f"1. **Extract {complete_count} complete examples** (≥40 lines) to acidbath-code repository\n")
    report.append(f"2. **Consider extracting {medium_count} medium examples** (21-39 lines) based on context\n")
    report.append(f"3. **Keep {stats['category_stats'].get('snippet', 0)} snippets** (≤20 lines) inline for readability\n")
    report.append(f"4. **Handle {stats['category_stats'].get('diagram', 0)} diagrams** separately (mermaid, diff)\n")

    # Top posts to prioritize
    report.append("\n## Priority Posts for Extraction\n\n")
    report.append("Focus on posts with highest complete example counts:\n\n")

    for post_name, post_data in sorted_posts[:4]:
        blocks = post_data['blocks']
        complete = sum(1 for b in blocks if b['category'] == 'complete_example')
        report.append(f"- **{post_name}**: {complete} complete examples, {post_data['total_blocks']} total blocks\n")

    # Write report
    output_path.write_text(''.join(report))
    print(f"Report generated: {output_path}")

    # Also write raw JSON data
    json_path = output_path.with_suffix('.json')
    json_path.write_text(json.dumps(stats, indent=2))
    print(f"Raw data saved: {json_path}")

def main():
    """Main execution."""
    repo_root = Path(__file__).parent.parent
    blog_dir = repo_root / 'src' / 'content' / 'blog'
    output_path = repo_root / 'specs' / 'code-block-audit-report.md'

    print(f"Analyzing blog posts in: {blog_dir}")
    stats = analyze_blog_posts(blog_dir)

    print(f"\nFound {stats['total_blocks']} code blocks across {stats['total_posts']} posts")
    generate_report(stats, output_path)

    print("\n✅ Audit complete")

if __name__ == '__main__':
    main()
