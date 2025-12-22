"""Content extraction router for multi-source content analysis.

This module provides a unified interface for extracting content from various
sources (YouTube, URLs, PDFs, text files/strings). All extractors return a
consistent ContentObject structure, enabling pattern analysis tools to work
with any content type without understanding source-specific extraction logic.

The router pattern:
1. Auto-detect content type from input source
2. Route to appropriate specialized extractor
3. Return unified ContentObject
"""

import os
import tempfile
from typing import Optional, Dict, Callable
from adws.adw_modules.data_types import ContentType, ContentObject
from adws.adw_modules.youtube_ops import extract_youtube_content
from adws.adw_modules.web_ops import extract_url_content
from adws.adw_modules.pdf_ops import extract_pdf_content
from adws.adw_modules.text_ops import extract_text_content
from adws.adw_modules.github_ops import extract_github_content


class ContentExtractionError(Exception):
    """Raised when content extraction fails."""
    pass


def detect_content_type(input_source: str) -> ContentType:
    """Detect content type from input source string.

    Detection rules (in order of priority):
    1. YouTube: Contains "youtube.com" or "youtu.be"
    2. GitHub: Contains "github.com" with /blob/ or /tree/
    3. URL: Starts with "http://" or "https://"
    4. PDF: Ends with ".pdf" or file exists with PDF magic bytes
    5. TEXT: Default fallback for all other inputs

    Args:
        input_source: Input string (URL, file path, or text)

    Returns:
        ContentType: Detected content type

    Examples:
        >>> detect_content_type("https://youtube.com/watch?v=abc")
        ContentType.YOUTUBE
        >>> detect_content_type("https://github.com/owner/repo/blob/main/file.py")
        ContentType.GITHUB
        >>> detect_content_type("https://example.com")
        ContentType.URL
        >>> detect_content_type("document.pdf")
        ContentType.PDF
        >>> detect_content_type("plain text content")
        ContentType.TEXT
    """
    # YouTube detection (highest priority for URLs)
    if "youtube.com" in input_source or "youtu.be" in input_source:
        return ContentType.YOUTUBE

    # GitHub detection (before generic URL)
    if "github.com" in input_source and ("/blob/" in input_source or "/tree/" in input_source):
        return ContentType.GITHUB

    # Generic URL detection
    if input_source.startswith("http://") or input_source.startswith("https://"):
        return ContentType.URL

    # PDF detection
    if input_source.endswith(".pdf"):
        return ContentType.PDF

    # Check for PDF magic bytes if file exists
    if os.path.exists(input_source):
        try:
            with open(input_source, "rb") as f:
                magic_bytes = f.read(4)
                if magic_bytes == b"%PDF":
                    return ContentType.PDF
        except Exception:
            pass  # If we can't read the file, fall through to TEXT

    # Default to text
    return ContentType.TEXT


def extract_content(
    input_source: str,
    content_type: Optional[ContentType] = None,
    output_dir: Optional[str] = None,
) -> ContentObject:
    """Extract content from any source (unified router).

    This is the main entry point for content extraction. It auto-detects
    the content type (if not specified) and routes to the appropriate
    specialized extractor.

    Args:
        input_source: URL, file path, or direct text string
        content_type: Optional explicit content type (auto-detected if None)
        output_dir: Output directory for temporary files (YouTube transcripts)
                   Defaults to system temp directory if None

    Returns:
        ContentObject: Unified content object from the appropriate extractor

    Raises:
        ValueError: If content_type is invalid or unsupported
        RuntimeError: If extraction fails

    Examples:
        >>> # Auto-detect YouTube
        >>> content = extract_content("https://youtube.com/watch?v=abc123")
        >>> content.type
        ContentType.YOUTUBE

        >>> # Explicit type specification
        >>> content = extract_content("example.com", content_type=ContentType.URL)

        >>> # Direct text
        >>> content = extract_content("Hello world")
        >>> content.type
        ContentType.TEXT
    """
    # Auto-detect content type if not specified
    if content_type is None:
        content_type = detect_content_type(input_source)

    # Default output directory for YouTube transcripts
    if output_dir is None:
        output_dir = tempfile.gettempdir()

    # Route to appropriate extractor
    if content_type == ContentType.YOUTUBE:
        return extract_youtube_content(input_source, output_dir)
    elif content_type == ContentType.GITHUB:
        return extract_github_content(input_source)
    elif content_type == ContentType.URL:
        return extract_url_content(input_source)
    elif content_type == ContentType.PDF:
        return extract_pdf_content(input_source)
    elif content_type == ContentType.TEXT:
        return extract_text_content(input_source)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")


# Content extractor registry for programmatic access
CONTENT_EXTRACTORS: Dict[ContentType, Callable] = {
    ContentType.YOUTUBE: extract_youtube_content,
    ContentType.GITHUB: extract_github_content,
    ContentType.URL: extract_url_content,
    ContentType.PDF: extract_pdf_content,
    ContentType.TEXT: extract_text_content,
}
