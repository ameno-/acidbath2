"""PDF text extraction.

This module handles extracting text content from PDF files,
returning a unified ContentObject structure.

Uses pypdf library (fallback to pdfplumber if needed).
"""

import os
from typing import Optional
from adws.adw_modules.data_types import ContentType, ContentObject


def extract_pdf_text(file_path: str) -> str:
    """Extract text from PDF file.

    Tries pypdf first, falls back to pdfplumber if available.

    Args:
        file_path: Path to PDF file

    Returns:
        str: Extracted text from all pages

    Raises:
        FileNotFoundError: If file doesn't exist
        RuntimeError: If extraction fails
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    # Try pypdf first
    try:
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        full_text = "\n\n".join(text_parts)

        if not full_text.strip():
            # Empty text might indicate scanned PDF
            return ""

        return full_text

    except ImportError:
        pass  # Fall back to pdfplumber

    # Try pdfplumber
    try:
        import pdfplumber

        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        full_text = "\n\n".join(text_parts)

        if not full_text.strip():
            return ""

        return full_text

    except ImportError:
        raise RuntimeError(
            "No PDF library available. Install with: uv add pypdf (or: uv add pdfplumber)"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to extract PDF text: {e}")


def is_scanned_pdf(text: str, file_size: int) -> bool:
    """Heuristic to detect if PDF is scanned (no embedded text).

    Args:
        text: Extracted text
        file_size: PDF file size in bytes

    Returns:
        bool: True if likely scanned, False otherwise
    """
    # If no text extracted, likely scanned
    if not text.strip():
        return True

    # If very little text relative to file size (less than 0.1% ratio)
    # This is a rough heuristic - scanned PDFs tend to have large file sizes
    # with minimal extractable text
    text_size = len(text.encode("utf-8"))
    if file_size > 100000 and text_size / file_size < 0.001:
        return True

    return False


def extract_pdf_content(file_path: str) -> ContentObject:
    """Extract content from PDF file.

    Args:
        file_path: Path to PDF file

    Returns:
        ContentObject: Unified content object with PDF data

    Raises:
        FileNotFoundError: If file doesn't exist
        RuntimeError: If extraction fails
    """
    # Extract text
    text = extract_pdf_text(file_path)

    # Get file size
    file_size = os.path.getsize(file_path)

    # Count pages
    page_count = 0
    try:
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        page_count = len(reader.pages)
    except ImportError:
        try:
            import pdfplumber

            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
        except ImportError:
            pass  # Page count will remain 0

    # Check if scanned
    is_scanned = is_scanned_pdf(text, file_size)

    # Extract title from filename
    title = os.path.splitext(os.path.basename(file_path))[0]

    # Build metadata
    metadata = {
        "page_count": page_count,
        "is_scanned": is_scanned,
        "file_size_bytes": file_size,
    }

    # Build ContentObject
    return ContentObject(
        type=ContentType.PDF,
        text=text,
        source=file_path,
        file_path=file_path,
        file_size=file_size,
        title=title,
        metadata=metadata,
    )
