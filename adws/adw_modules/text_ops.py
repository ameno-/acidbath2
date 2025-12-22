"""Text content extraction.

This module handles reading text files and direct text strings,
returning a unified ContentObject structure.

Supports:
- Text file paths (with encoding fallback)
- Direct text strings
- Stdin marker ('-') for piped input
"""

import os
import sys
from typing import Optional
from adws.adw_modules.data_types import ContentType, ContentObject


def read_text_file(file_path: str) -> str:
    """Read text file with encoding fallback.

    Tries UTF-8 first, falls back to latin-1 if UTF-8 fails.

    Args:
        file_path: Path to text file

    Returns:
        str: File content

    Raises:
        FileNotFoundError: If file doesn't exist
        RuntimeError: If reading fails
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Text file not found: {file_path}")

    # Try UTF-8 first
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        pass  # Fall back to latin-1

    # Try latin-1 fallback
    try:
        with open(file_path, "r", encoding="latin-1") as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read text file: {e}")


def read_stdin() -> str:
    """Read text from stdin.

    Returns:
        str: Content from stdin

    Raises:
        RuntimeError: If reading stdin fails
    """
    try:
        return sys.stdin.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read from stdin: {e}")


def extract_text_content(source: str) -> ContentObject:
    """Extract content from text source.

    Handles three cases:
    1. File path: Read file content with encoding fallback
    2. Stdin marker '-': Read from stdin
    3. Direct text: Use source as text content

    Args:
        source: File path, stdin marker '-', or direct text

    Returns:
        ContentObject: Unified content object with text data

    Raises:
        FileNotFoundError: If file path doesn't exist
        RuntimeError: If reading fails
    """
    text = ""
    is_file = False
    file_path = None
    file_size = None
    encoding = "utf-8"

    # Check for stdin marker
    if source == "-":
        text = read_stdin()
        metadata = {
            "is_file": False,
            "encoding": "utf-8",
            "source_type": "stdin",
        }
        return ContentObject(
            type=ContentType.TEXT,
            text=text,
            source=source,
            metadata=metadata,
        )

    # Check if source is a file path
    if os.path.exists(source):
        is_file = True
        file_path = source
        file_size = os.path.getsize(source)

        # Try UTF-8, fall back to latin-1
        try:
            text = read_text_file(source)
            # If we got here, it's UTF-8 or latin-1 worked
            # Try to detect which one was used
            try:
                with open(source, "r", encoding="utf-8") as f:
                    f.read()
                encoding = "utf-8"
            except UnicodeDecodeError:
                encoding = "latin-1"
        except Exception as e:
            raise RuntimeError(f"Failed to read text file: {e}")
    else:
        # Treat as direct text string
        text = source

    # Build metadata
    metadata = {
        "is_file": is_file,
        "encoding": encoding,
        "source_type": "file" if is_file else "string",
    }

    # Build ContentObject
    return ContentObject(
        type=ContentType.TEXT,
        text=text,
        source=source,
        file_path=file_path,
        file_size=file_size,
        metadata=metadata,
    )
