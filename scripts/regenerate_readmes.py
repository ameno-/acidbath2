#!/usr/bin/env python3
"""
Regenerate READMEs in acidbath-code with improved content.
"""

import json
from pathlib import Path
from datetime import datetime


def extract_code_description(code: str, language: str) -> str:
    """Extract a meaningful description from the code itself."""
    lines = code.strip().split('\n')

    if language == 'python':
        in_docstring = False
        docstring_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#!') or stripped.startswith('# ///'):
                continue
            if stripped.startswith('# dependencies'):
                continue

            if '"""' in stripped or "'''" in stripped:
                if not in_docstring:
                    in_docstring = True
                    if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                        content = stripped.strip('"""').strip("'''").strip()
                        if content:
                            return content
                    continue
                else:
                    break

            if in_docstring:
                if stripped:
                    docstring_lines.append(stripped)

        if docstring_lines:
            return ' '.join(docstring_lines[:3])

    if language in ['typescript', 'javascript']:
        comment_lines = []
        for line in lines[:20]:
            stripped = line.strip()
            if stripped.startswith('//'):
                comment_lines.append(stripped.lstrip('/').strip())
            elif stripped.startswith('*') and not stripped.startswith('*/'):
                comment_lines.append(stripped.lstrip('*').strip())

        if comment_lines:
            return ' '.join(comment_lines[:3])

    if language in ['yaml', 'yml']:
        keys = []
        for line in lines[:10]:
            if line and not line.startswith(' ') and not line.startswith('#'):
                key = line.split(':')[0].strip()
                if key:
                    keys.append(key)
        if keys:
            return f"Configuration file with: {', '.join(keys[:5])}"

    if language == 'markdown':
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                return stripped[:200]

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

ACIDBATH_CODE = Path.home() / "dev" / "acidbath-code"
BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"

# Post title mapping
POST_TITLES = {
    "agent-architecture": "Agent Architecture: From Custom Agents to Effective Delegation",
    "context-engineering": "Context Engineering: From Token Optimization to Large Codebase Mastery",
    "directory-watchers": "Directory Watchers: File-Based AI Automation That Scales",
    "document-generation-skills": "AI Document Skills: Automated File Generation That Actually Ships",
    "single-file-scripts": "Single-File Scripts: When One File Beats an Entire MCP Server",
    "workflow-prompts": "Workflow Prompts: The Pattern That Makes AI Engineering Predictable",
    "claude-skills-deep-dive": "Claude Code Skills: A Deep Dive into Custom Agent Behaviors",
}


def regenerate_readme(example_dir: Path):
    """Regenerate README for an example directory."""
    # Parse path components
    parts = example_dir.relative_to(ACIDBATH_CODE).parts
    if len(parts) < 3:
        return

    category, post_slug, example_name = parts[0], parts[1], parts[2]
    post_title = POST_TITLES.get(post_slug, post_slug.replace("-", " ").title())

    # Find the code file
    code_files = [
        f for f in example_dir.iterdir()
        if f.is_file() and f.name != "README.md"
    ]

    if not code_files:
        return

    code_file = code_files[0]
    code = code_file.read_text()
    language = code_file.suffix.lstrip(".")

    # Map extension to language name
    lang_map = {
        "py": "python",
        "ts": "typescript",
        "js": "javascript",
        "sh": "bash",
        "yaml": "yaml",
        "md": "markdown",
        "txt": "text",
    }
    language = lang_map.get(language, language)

    # Extract description from code
    description = extract_code_description(code, language)

    line_count = len(code.strip().split("\n"))
    today = datetime.now().strftime("%Y-%m-%d")

    # Generate README
    readme = []
    readme.append(f"# {example_name.replace('-', ' ').title()}\n\n")

    readme.append("## Source\n\n")
    readme.append(f"**Blog Post:** [{post_title}](https://blog.acidbath.com/blog/{post_slug})\n")
    readme.append(f"**Date Extracted:** {today}\n\n")

    readme.append("## Description\n\n")
    if description:
        readme.append(f"{description}\n\n")
    else:
        readme.append(f"Complete {language} example from the ACIDBATH blog.\n\n")

    readme.append("## Quick Start\n\n")
    if language == "python":
        if "# /// script" in code:
            readme.append("```bash\n")
            readme.append(f"uv run {code_file.name}\n")
            readme.append("```\n\n")
        else:
            readme.append("```bash\n")
            readme.append(f"python {code_file.name}\n")
            readme.append("```\n\n")
    elif language == "typescript":
        readme.append("```bash\n")
        readme.append(f"npx ts-node {code_file.name}\n")
        readme.append("# or\n")
        readme.append(f"bun run {code_file.name}\n")
        readme.append("```\n\n")
    elif language == "bash":
        readme.append("```bash\n")
        readme.append(f"bash {code_file.name}\n")
        readme.append("```\n\n")

    readme.append("## Files\n\n")
    readme.append(f"- **`{code_file.name}`** - {language.title()} implementation ({line_count} lines)\n\n")

    # Dependencies (for Python scripts with inline deps)
    if language == "python" and "# dependencies" in code.lower():
        readme.append("## Dependencies\n\n")
        readme.append("This script uses inline dependencies (PEP 723). Run with `uv run` to auto-install:\n\n")
        in_deps = False
        deps = []
        for line in code.split("\n"):
            if "# dependencies" in line.lower():
                in_deps = True
                continue
            if in_deps:
                if line.strip().startswith("#") or line.strip() == "# ///":
                    break
                if '"' in line:
                    dep = line.split('"')[1].split(">=")[0].split("==")[0]
                    deps.append(dep)
        if deps:
            for dep in deps:
                readme.append(f"- {dep}\n")
            readme.append("\n")

    readme.append("## Blog Context\n\n")
    readme.append(f"This code is from [{post_title}](https://blog.acidbath.com/blog/{post_slug}).\n\n")
    readme.append("The blog post provides:\n")
    readme.append("- Detailed explanation of the implementation\n")
    readme.append("- Context for when and why to use this pattern\n")
    readme.append("- Related examples and best practices\n\n")

    readme.append("## License\n\n")
    readme.append("This code follows the **POC Rule**: working, copy-paste code you can use immediately.\n")
    readme.append("See the [ACIDBATH blog](https://blog.acidbath.com) for more AI engineering content.\n")

    # Write README
    readme_path = example_dir / "README.md"
    readme_path.write_text("".join(readme))
    print(f"Updated: {example_dir.relative_to(ACIDBATH_CODE)}")


def update_manifest():
    """Update manifest.json with correct paths."""
    manifest_path = ACIDBATH_CODE / "manifest.json"
    if not manifest_path.exists():
        return

    manifest = json.loads(manifest_path.read_text())

    # Update paths in manifest
    for post_slug, post_data in manifest.get("posts", {}).items():
        for example in post_data.get("extracted_examples", []):
            old_path = example.get("path", "")
            if old_path.startswith("examples/"):
                example["path"] = old_path.replace("examples/", "", 1)

    manifest["generated"] = datetime.now().isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("Updated manifest.json")


def main():
    """Regenerate all READMEs."""
    print("Regenerating READMEs in acidbath-code...\n")

    # Find all example directories
    for category in ["agentic-patterns", "production-patterns", "workflow-tools"]:
        category_dir = ACIDBATH_CODE / category
        if not category_dir.exists():
            continue

        for post_dir in category_dir.iterdir():
            if not post_dir.is_dir():
                continue

            for example_dir in post_dir.iterdir():
                if not example_dir.is_dir():
                    continue

                regenerate_readme(example_dir)

    # Update manifest
    update_manifest()

    print("\nDone!")


if __name__ == "__main__":
    main()
