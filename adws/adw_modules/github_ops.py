"""GitHub content extraction for brainstorm system.

This module handles extraction of GitHub files, notebooks, and directory trees
for content analysis.
"""

import os
import re
import json
import urllib.request
import urllib.error
from typing import Literal, Dict, Any
from pathlib import Path

from adws.adw_modules.data_types import ContentObject, ContentType


def detect_github_url_type(url: str) -> Literal["blob", "tree", "unknown"]:
    """Detect GitHub URL type (file or directory).

    Args:
        url: GitHub URL

    Returns:
        "blob" for file URLs, "tree" for directory URLs, "unknown" otherwise

    Examples:
        https://github.com/owner/repo/blob/main/file.py -> "blob"
        https://github.com/owner/repo/tree/main/dir -> "tree"
    """
    if "/blob/" in url:
        return "blob"
    elif "/tree/" in url:
        return "tree"
    else:
        return "unknown"


def get_raw_github_url(url: str) -> str:
    """Convert GitHub blob URL to raw content URL.

    Args:
        url: GitHub blob URL

    Returns:
        Raw content URL

    Examples:
        github.com/owner/repo/blob/main/file.py ->
        raw.githubusercontent.com/owner/repo/main/file.py
    """
    # Pattern: https://github.com/OWNER/REPO/blob/BRANCH/PATH
    pattern = r'github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)'
    match = re.search(pattern, url)

    if not match:
        raise ValueError(f"Invalid GitHub blob URL: {url}")

    owner, repo, branch, path = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"


def fetch_url_content(url: str, timeout: int = 30) -> str:
    """Fetch content from URL with GitHub token if available.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Content as string

    Raises:
        urllib.error.HTTPError: If request fails
    """
    headers = {}

    # Add GitHub token if available for higher rate limits
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token and "github" in url:
        headers["Authorization"] = f"token {github_token}"

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"GitHub content not found (404): {url}")
        elif e.code == 403:
            raise ValueError(f"GitHub API rate limit exceeded (403). Set GITHUB_TOKEN env var.")
        else:
            raise ValueError(f"Failed to fetch GitHub content ({e.code}): {url}")


def parse_notebook_to_markdown(ipynb_content: str) -> str:
    """Convert Jupyter notebook JSON to readable markdown.

    Args:
        ipynb_content: Raw .ipynb JSON content

    Returns:
        Markdown-formatted notebook content

    Format:
        # Cell 1 (code)
        ```python
        code here
        ```

        **Output:**
        ```
        output here
        ```

        # Cell 2 (markdown)
        markdown content here
    """
    try:
        nb = json.loads(ipynb_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid notebook JSON: {e}")

    if "cells" not in nb:
        raise ValueError("Invalid notebook format: no cells found")

    markdown_parts = []
    cell_num = 1

    for cell in nb["cells"]:
        cell_type = cell.get("cell_type", "unknown")
        source = cell.get("source", [])

        # Join source lines
        if isinstance(source, list):
            source_text = "".join(source)
        else:
            source_text = source

        if cell_type == "code":
            markdown_parts.append(f"# Cell {cell_num} (code)\n")
            markdown_parts.append(f"```python\n{source_text}\n```\n")

            # Add outputs if present
            outputs = cell.get("outputs", [])
            if outputs:
                markdown_parts.append("\n**Output:**\n")
                for output in outputs:
                    if "text" in output:
                        text = output["text"]
                        if isinstance(text, list):
                            text = "".join(text)
                        markdown_parts.append(f"```\n{text}\n```\n")
                    elif "data" in output:
                        # Handle display data (images, html, etc.)
                        data = output["data"]
                        if "text/plain" in data:
                            text = data["text/plain"]
                            if isinstance(text, list):
                                text = "".join(text)
                            markdown_parts.append(f"```\n{text}\n```\n")

        elif cell_type == "markdown":
            markdown_parts.append(f"# Cell {cell_num} (markdown)\n")
            markdown_parts.append(f"{source_text}\n")

        markdown_parts.append("\n---\n\n")
        cell_num += 1

    return "".join(markdown_parts)


def extract_github_file(url: str) -> ContentObject:
    """Extract content from a GitHub file (blob).

    Args:
        url: GitHub blob URL

    Returns:
        ContentObject with extracted file content

    Raises:
        ValueError: If URL is invalid or fetch fails
    """
    raw_url = get_raw_github_url(url)
    content = fetch_url_content(raw_url)

    # Extract metadata from URL
    pattern = r'github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)'
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f"Invalid GitHub blob URL: {url}")

    owner, repo, branch, path = match.groups()
    filename = Path(path).name
    title = f"{owner}/{repo}: {filename}"

    # Special handling for .ipynb files
    if path.endswith('.ipynb'):
        try:
            markdown_content = parse_notebook_to_markdown(content)
            return ContentObject(
                type=ContentType.GITHUB,
                text=markdown_content,
                source=url,
                url=url,
                title=title,
                metadata={
                    "owner": owner,
                    "repo": repo,
                    "branch": branch,
                    "path": path,
                    "filename": filename,
                    "file_type": "notebook",
                    "raw_url": raw_url
                }
            )
        except Exception as e:
            # If notebook parsing fails, fall back to raw content
            return ContentObject(
                type=ContentType.GITHUB,
                text=f"# Notebook Parsing Failed\n\nError: {e}\n\n# Raw Content\n```json\n{content}\n```",
                source=url,
                url=url,
                title=title,
                metadata={
                    "owner": owner,
                    "repo": repo,
                    "branch": branch,
                    "path": path,
                    "filename": filename,
                    "file_type": "notebook",
                    "parse_error": str(e),
                    "raw_url": raw_url
                }
            )

    return ContentObject(
        type=ContentType.GITHUB,
        text=content,
        source=url,
        url=url,
        title=title,
        metadata={
            "owner": owner,
            "repo": repo,
            "branch": branch,
            "path": path,
            "filename": filename,
            "file_type": Path(path).suffix,
            "raw_url": raw_url
        }
    )


def extract_github_tree(url: str) -> ContentObject:
    """Extract content from a GitHub directory (tree).

    Aggregates README and key files (*.py, *.md, *.ts, *.tsx, *.js, *.jsx).

    Args:
        url: GitHub tree URL

    Returns:
        ContentObject with aggregated directory content

    Note:
        This is a simple implementation that constructs file URLs.
        For production, should use GitHub API to list directory contents.
    """
    # For now, return a placeholder indicating tree extraction needs API
    pattern = r'github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)'
    match = re.search(pattern, url)

    if not match:
        raise ValueError(f"Invalid GitHub tree URL: {url}")

    owner, repo, branch, path = match.groups()
    title = f"{owner}/{repo}: {path or 'root'}"

    # Simple approach: try to fetch README
    readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/README.md"
    try:
        readme_content = fetch_url_content(readme_url)
        text = f"# {title}\n\n## README\n\n{readme_content}\n"
    except Exception:
        text = f"# {title}\n\nNo README found.\n"

    return ContentObject(
        type=ContentType.GITHUB,
        text=text,
        source=url,
        url=url,
        title=title,
        metadata={
            "owner": owner,
            "repo": repo,
            "branch": branch,
            "path": path,
            "content_type": "directory",
            "note": "Directory extraction is limited. Use GitHub API for full tree."
        }
    )


def extract_github_content(url: str) -> ContentObject:
    """Extract content from GitHub URL (auto-detect blob vs tree).

    Args:
        url: GitHub URL

    Returns:
        ContentObject with extracted content

    Raises:
        ValueError: If URL is invalid or extraction fails
    """
    url_type = detect_github_url_type(url)

    if url_type == "blob":
        return extract_github_file(url)
    elif url_type == "tree":
        return extract_github_tree(url)
    else:
        raise ValueError(f"Unsupported GitHub URL type: {url}")
