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

    readme = []
    readme.append(f"# {example_name.replace('-', ' ').title()}\n\n")

    # Source section
    readme.append("## Source\n\n")
    readme.append(f"**Blog Post:** [{post_title}](https://acidbath.sh/blog/{post_slug})\n")
    readme.append(f"**Section:** {section_heading}\n")
    readme.append(f"**Date Extracted:** {today}\n\n")

    # Description
    readme.append("## Description\n\n")
    readme.append(f"{description}\n\n")

    # Context
    readme.append("## Context\n\n")
    readme.append(f"This code example is from the '{section_heading}' section of the blog post. ")
    readme.append("It demonstrates a complete, working implementation that you can use as-is ")
    readme.append("or adapt for your own projects.\n\n")

    # Files section
    readme.append("## Files\n\n")
    file_descriptions = {}
    for block in blocks:
        # Generate filename from language
        filename = generate_filename(block.language, example_name, len(blocks))
        file_descriptions[filename] = f"Main {block.language} implementation"

    for filename, desc in file_descriptions.items():
        readme.append(f"- `{filename}` - {desc}\n")
    readme.append("\n")

    # Usage section
    readme.append("## Usage\n\n")
    readme.append("### Prerequisites\n\n")

    # Detect prerequisites from language
    languages = set(block.language for block in blocks)
    if 'python' in languages:
        readme.append("- Python 3.11+\n")
    if 'typescript' in languages or 'javascript' in languages:
        readme.append("- Node.js 18+\n")
    if 'bash' in languages:
        readme.append("- Bash shell\n")

    readme.append("\n### Running the Example\n\n")

    if usage_notes:
        readme.append(f"{usage_notes}\n\n")
    else:
        # Generate default usage based on language
        primary_lang = blocks[0].language if blocks else 'unknown'
        if primary_lang == 'python':
            readme.append("```bash\n")
            readme.append("python " + list(file_descriptions.keys())[0] + "\n")
            readme.append("```\n\n")
        elif primary_lang in ['typescript', 'javascript']:
            readme.append("```bash\n")
            readme.append("node " + list(file_descriptions.keys())[0] + "\n")
            readme.append("```\n\n")
        elif primary_lang == 'bash':
            readme.append("```bash\n")
            readme.append("bash " + list(file_descriptions.keys())[0] + "\n")
            readme.append("```\n\n")

    # Key Concepts
    readme.append("## Key Concepts\n\n")
    readme.append("This example demonstrates:\n\n")
    readme.append("- **Implementation Pattern:** See the blog post for detailed explanation\n")
    readme.append("- **Best Practices:** Code follows production-ready patterns\n")
    readme.append("- **Extensibility:** Adapt for your specific use case\n\n")

    # Modifications
    readme.append("## Modifications\n\n")
    readme.append("To adapt this code for your use case:\n\n")
    readme.append("1. Review the code and understand the core logic\n")
    readme.append("2. Modify configuration or parameters as needed\n")
    readme.append("3. Test thoroughly before using in production\n\n")

    # Notes
    readme.append("## Notes\n\n")
    readme.append("This code is extracted from the ACIDBATH blog and follows the POC Rule: ")
    readme.append("it's working, copy-paste code that you can use immediately. ")
    readme.append("See the original blog post for context and detailed explanation.\n")

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
