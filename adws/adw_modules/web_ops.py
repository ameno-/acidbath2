"""URL content extraction with web scraping.

This module handles scraping web pages and converting them to markdown
format, returning a unified ContentObject structure.

Tries fabric first (if available), falls back to requests + html2text.
"""

import re
import subprocess
from typing import Optional
from adws.adw_modules.data_types import ContentType, ContentObject


def scrape_url_to_markdown(url: str) -> str:
    """Scrape URL and convert to markdown.

    Tries fabric --scrape_url first, falls back to requests + html2text.

    Args:
        url: URL to scrape

    Returns:
        str: Content as markdown

    Raises:
        RuntimeError: If scraping fails
    """
    # Try fabric first
    try:
        result = subprocess.run(
            ["fabric", "--scrape_url", url],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass  # Fall back to Python approach

    # Fall back to requests + html2text
    try:
        import requests
        import html2text

        # Fetch HTML
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Convert to markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        markdown = h.handle(response.text)

        return markdown.strip()

    except ImportError:
        raise RuntimeError(
            "Neither fabric nor requests+html2text available. "
            "Install with: uv add requests html2text"
        )
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Request timed out while fetching {url}")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP error {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch URL: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during URL scraping: {e}")


def extract_title_from_markdown(markdown: str, url: str) -> str:
    """Extract title from markdown content.

    Looks for first H1 heading, falls back to domain name.

    Args:
        markdown: Markdown content
        url: Original URL (for fallback)

    Returns:
        str: Extracted title
    """
    # Try to find first H1 heading
    h1_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()

    # Fall back to domain name from URL
    domain_match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    if domain_match:
        return domain_match.group(1)

    return "Untitled"


def extract_url_content(url: str) -> ContentObject:
    """Extract content from web URL.

    Args:
        url: Web URL to scrape

    Returns:
        ContentObject: Unified content object with URL data

    Raises:
        RuntimeError: If scraping fails
    """
    # Determine scrape method
    scrape_method = "unknown"

    # Try fabric first
    try:
        subprocess.run(
            ["which", "fabric"], capture_output=True, check=True, timeout=5
        )
        scrape_method = "fabric"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        scrape_method = "requests"

    # Scrape content
    markdown = scrape_url_to_markdown(url)

    # Extract title
    title = extract_title_from_markdown(markdown, url)

    # Build metadata
    metadata = {
        "scrape_method": scrape_method,
        "content_length": len(markdown),
    }

    # Build ContentObject
    return ContentObject(
        type=ContentType.URL,
        text=markdown,
        source=url,
        url=url,
        title=title,
        metadata=metadata,
    )
