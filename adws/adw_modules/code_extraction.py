"""
Code extraction utilities for ACIDBATH blog posts.

Provides functions to parse code blocks from markdown, categorize them,
extract context, and generate README files for code examples.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class CodeBlock:
    """Represents a code block extracted from markdown."""

    def __init__(
        self,
        language: str,
        code: str,
        line_number: int,
        context: str,
        filepath: str
    ):
        self.language = language
        self.code = code
        self.line_number = line_number
        self.context = context
        self.filepath = filepath
        self.line_count = len(code.strip().split('\n'))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'language': self.language,
            'code': self.code,
            'line_number': self.line_number,
            'line_count': self.line_count,
            'context': self.context,
            'filepath': self.filepath,
        }


def parse_code_blocks(markdown_content: str, filepath: str) -> List[CodeBlock]:
    """
    Extract all code blocks from markdown with context.

    Args:
        markdown_content: Raw markdown content
        filepath: Path to the markdown file

    Returns:
        List of CodeBlock objects
    """
    blocks = []

    # Pattern to match code blocks with optional language
    pattern = r'```(\w*)\n(.*?)```'

    # Split content into lines for context extraction
    lines = markdown_content.split('\n')

    # Find all code blocks
    for match in re.finditer(pattern, markdown_content, re.DOTALL):
        language = match.group(1) or 'unknown'
        code = match.group(2)

        # Find the line number where this code block starts
        start_pos = match.start()
        line_num = markdown_content[:start_pos].count('\n') + 1

        # Extract context (previous heading)
        context = extract_context(lines, line_num)

        block = CodeBlock(
            language=language,
            code=code,
            line_number=line_num,
            context=context,
            filepath=filepath
        )
        blocks.append(block)

    return blocks


def extract_context(lines: List[str], code_line_num: int) -> str:
    """
    Extract the nearest heading before the code block.

    Args:
        lines: All lines from the markdown file
        code_line_num: Line number where code block starts

    Returns:
        The nearest heading or "No context"
    """
    # Search backwards from code block to find the last heading
    for i in range(code_line_num - 1, max(0, code_line_num - 50), -1):
        if i < len(lines) and lines[i].startswith('#'):
            return lines[i].strip()
    return "No context"


def categorize_code_block(block: CodeBlock) -> str:
    """
    Determine category based on content and metadata.

    Args:
        block: CodeBlock object

    Returns:
        Category string: 'complete_example', 'medium_example', 'snippet',
        'configuration', or 'diagram'
    """
    line_count = block.line_count
    language = block.language.lower()

    # Diagrams and special formats
    if language in ['mermaid', 'diff']:
        return 'diagram'

    # Configuration files
    if language in ['json', 'yaml', 'yml', 'toml', 'ini', 'env']:
        if line_count >= 20:
            return 'configuration'
        else:
            return 'snippet'

    # Code categorization by size
    if line_count >= 40:
        return 'complete_example'
    elif line_count <= 20:
        return 'snippet'
    else:
        return 'medium_example'


def determine_category_directory(block: CodeBlock, post_slug: str) -> str:
    """
    Determine which top-level category directory this code belongs to.

    Args:
        block: CodeBlock object
        post_slug: Blog post slug (e.g., 'agent-architecture')

    Returns:
        Category directory name: 'agentic-patterns', 'production-patterns',
        'workflow-tools', or 'configurations'
    """
    # Map post slugs to categories
    agentic_posts = [
        'agent-architecture',
        'claude-skills-deep-dive',
        'context-engineering'
    ]
    production_posts = [
        'directory-watchers',
        'document-generation-skills'
    ]
    workflow_posts = [
        'single-file-scripts',
        'workflow-prompts'
    ]

    # Categorize based on post
    if post_slug in agentic_posts:
        return 'agentic-patterns'
    elif post_slug in production_posts:
        return 'production-patterns'
    elif post_slug in workflow_posts:
        return 'workflow-tools'
    else:
        # Fallback: categorize by language
        language = block.language.lower()
        if language in ['json', 'yaml', 'yml', 'toml', 'ini', 'env']:
            return 'configurations'
        else:
            return 'workflow-tools'  # Default fallback


def extract_code_description(code: str, language: str) -> str:
    """
    Extract a meaningful description from the code itself.

    Args:
        code: The source code
        language: Programming language

    Returns:
        Description string extracted from docstrings, comments, or code analysis
    """
    lines = code.strip().split('\n')

    # For Python, look for module docstring or main function docstring
    if language == 'python':
        # Check for module docstring (triple quotes at start)
        in_docstring = False
        docstring_lines = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Skip shebang and script metadata
            if stripped.startswith('#!') or stripped.startswith('# ///'):
                continue
            if stripped.startswith('# dependencies'):
                continue

            # Look for docstring
            if '"""' in stripped or "'''" in stripped:
                if not in_docstring:
                    in_docstring = True
                    # Single line docstring
                    if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                        content = stripped.strip('"""').strip("'''").strip()
                        if content:
                            return content
                    continue
                else:
                    # End of multiline docstring
                    break

            if in_docstring:
                if stripped:
                    docstring_lines.append(stripped)

        if docstring_lines:
            return ' '.join(docstring_lines[:3])  # First 3 lines

    # For TypeScript/JavaScript, look for JSDoc or leading comments
    if language in ['typescript', 'javascript']:
        comment_lines = []
        for line in lines[:20]:
            stripped = line.strip()
            if stripped.startswith('//'):
                comment_lines.append(stripped.lstrip('/').strip())
            elif stripped.startswith('*') and not stripped.startswith('*/'):
                comment_lines.append(stripped.lstrip('*').strip())
            elif stripped.startswith('/**'):
                continue
            elif comment_lines and not stripped.startswith(('/', '*')):
                break

        if comment_lines:
            return ' '.join(comment_lines[:3])

    # For YAML/configs, describe based on content
    if language in ['yaml', 'yml']:
        # Look for top-level keys
        keys = []
        for line in lines[:10]:
            if line and not line.startswith(' ') and not line.startswith('#'):
                key = line.split(':')[0].strip()
                if key:
                    keys.append(key)
        if keys:
            return f"Configuration file with: {', '.join(keys[:5])}"

    # For markdown, use first non-empty line
    if language == 'markdown':
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                return stripped[:200]

    # Fallback: analyze imports and main structures
    if language == 'python':
        imports = []
        for line in lines[:30]:
            if line.startswith('import ') or line.startswith('from '):
                module = line.split()[1].split('.')[0]
                if module not in imports:
                    imports.append(module)

        if imports:
            return f"Python script using {', '.join(imports[:4])}"

    return ""


def generate_example_readme(
    example_name: str,
    post_title: str,
    post_slug: str,
    section_heading: str,
    description: str,
    blocks: List[CodeBlock],
    usage_notes: Optional[str] = None
) -> str:
    """
    Create README content for a code example.

    Args:
        example_name: Name of the example (e.g., 'multi-agent-orchestrator')
        post_title: Title of the blog post
        post_slug: Slug of the blog post
        section_heading: Section heading in the post
        description: Description of what this code does
        blocks: List of CodeBlock objects in this example
        usage_notes: Optional usage notes

    Returns:
        README markdown content
    """
    today = datetime.now().strftime('%Y-%m-%d')

    # Try to extract better description from code if generic
    if blocks and ('demonstrating' in description.lower() or not description.strip()):
        code_desc = extract_code_description(blocks[0].code, blocks[0].language)
        if code_desc:
            description = code_desc

    readme = []
    readme.append(f"# {example_name.replace('-', ' ').title()}\n\n")

    # Source section with correct URL
    readme.append("## Source\n\n")
    readme.append(f"**Blog Post:** [{post_title}](https://blog.acidbath.com/blog/{post_slug})\n")
    readme.append(f"**Section:** {section_heading.lstrip('#').strip()}\n")
    readme.append(f"**Date Extracted:** {today}\n\n")

    # Description
    readme.append("## Description\n\n")
    if description:
        readme.append(f"{description}\n\n")
    else:
        readme.append(f"Complete code example from the ACIDBATH blog post on {post_title.lower()}.\n\n")

    # Quick Start
    readme.append("## Quick Start\n\n")

    primary_lang = blocks[0].language if blocks else 'unknown'
    filename = generate_filename(primary_lang, example_name, len(blocks))

    if primary_lang == 'python':
        # Check if it's a uv script
        if blocks and '# /// script' in blocks[0].code:
            readme.append("```bash\n")
            readme.append(f"uv run {filename}\n")
            readme.append("```\n\n")
        else:
            readme.append("```bash\n")
            readme.append(f"python {filename}\n")
            readme.append("```\n\n")
    elif primary_lang in ['typescript']:
        readme.append("```bash\n")
        readme.append(f"npx ts-node {filename}\n")
        readme.append("# or\n")
        readme.append(f"bun run {filename}\n")
        readme.append("```\n\n")
    elif primary_lang == 'bash':
        readme.append("```bash\n")
        readme.append(f"bash {filename}\n")
        readme.append("```\n\n")

    # Files section
    readme.append("## Files\n\n")
    for block in blocks:
        fname = generate_filename(block.language, example_name, len(blocks))
        readme.append(f"- **`{fname}`** - {block.language.title()} implementation ({block.line_count} lines)\n")
    readme.append("\n")

    # Dependencies (for Python scripts with inline deps)
    if primary_lang == 'python' and blocks:
        code = blocks[0].code
        if '# dependencies' in code.lower():
            readme.append("## Dependencies\n\n")
            readme.append("This script uses inline dependencies (PEP 723). Run with `uv run` to auto-install:\n\n")
            # Extract dependencies
            in_deps = False
            deps = []
            for line in code.split('\n'):
                if '# dependencies' in line.lower():
                    in_deps = True
                    continue
                if in_deps:
                    if line.strip().startswith('#'):
                        break
                    if '"' in line:
                        dep = line.split('"')[1].split('>=')[0].split('==')[0]
                        deps.append(dep)
            if deps:
                for dep in deps:
                    readme.append(f"- {dep}\n")
                readme.append("\n")

    # Blog Context
    readme.append("## Blog Context\n\n")
    section_clean = section_heading.lstrip('#').strip()
    readme.append(f"This code is from the **{section_clean}** section of [{post_title}](https://blog.acidbath.com/blog/{post_slug}).\n\n")
    readme.append("The blog post provides:\n")
    readme.append("- Detailed explanation of the implementation\n")
    readme.append("- Context for when and why to use this pattern\n")
    readme.append("- Related examples and best practices\n\n")

    # Notes
    readme.append("## License\n\n")
    readme.append("This code follows the **POC Rule**: working, copy-paste code you can use immediately.\n")
    readme.append("See the [ACIDBATH blog](https://blog.acidbath.com) for more AI engineering content.\n")

    return ''.join(readme)


def generate_filename(language: str, example_name: str, count: int) -> str:
    """
    Generate appropriate filename based on language and context.

    Args:
        language: Programming language
        example_name: Name of the example
        count: Total number of blocks in example

    Returns:
        Filename string
    """
    extensions = {
        'python': '.py',
        'javascript': '.js',
        'typescript': '.ts',
        'bash': '.sh',
        'yaml': '.yaml',
        'yml': '.yaml',
        'json': '.json',
        'toml': '.toml',
        'html': '.html',
        'css': '.css',
        'markdown': '.md',
    }

    ext = extensions.get(language.lower(), '.txt')

    # For single-file examples, use a descriptive name
    if count == 1:
        # Convert example-name to snake_case for Python, etc.
        if language == 'python':
            base = example_name.replace('-', '_')
        else:
            base = example_name

        return base + ext
    else:
        # For multi-file examples, use generic names
        return 'main' + ext


def extract_post_metadata(markdown_content: str) -> Dict[str, str]:
    """
    Extract frontmatter metadata from blog post.

    Args:
        markdown_content: Raw markdown content

    Returns:
        Dictionary with metadata (title, description, etc.)
    """
    metadata = {}

    # Extract frontmatter
    frontmatter_pattern = r'^---\n(.*?)\n---'
    match = re.search(frontmatter_pattern, markdown_content, re.DOTALL)

    if match:
        frontmatter = match.group(1)
        # Parse YAML-like frontmatter
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata


def get_post_slug(filepath: str) -> str:
    """
    Extract post slug from filepath.

    Args:
        filepath: Path to markdown file

    Returns:
        Post slug (e.g., 'agent-architecture')
    """
    return Path(filepath).stem
