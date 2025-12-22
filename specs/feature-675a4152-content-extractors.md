# Feature: Content Extractors - Multi-Type Content Extraction Pipeline

## Metadata
adw_id: `675a4152`
prompt: `{"number": "content-extractors", "title": "Content Extractors - Multi-Type Content Extraction Pipeline", "body": "## Summary\n\nCreate content extraction modules that can process multiple input types (YouTube, URL, PDF, text) and produce a unified content object for pattern analysis.\n\n## Parent Issue\n\nThis is Phase 3 of `issue-jerry-patterns-content-analysis.md`\n\n## Dependencies\n\n- None (can run in parallel with Phase 2)"}`

## Feature Description

Create a modular content extraction system that processes multiple input types (YouTube videos, web URLs, PDF files, and text files/strings) and produces a unified `ContentObject` data structure. This system will serve as the foundation for pattern-based content analysis workflows in Jerry's agentic layer.

The content extractors abstract away the complexity of different input sources, providing a clean interface where any supported input can be normalized into a consistent format for downstream processing. This enables pattern analysis tools (like fabric patterns) to work with content from any source without understanding the source-specific extraction logic.

## User Story

As a Jerry user running pattern analysis workflows
I want to provide content from multiple sources (YouTube, URLs, PDFs, or text)
So that I can analyze any content type using the same pattern analysis tools without manual conversion

## Problem Statement

Currently, Jerry lacks a unified way to extract and normalize content from different sources. Users who want to analyze YouTube videos, web articles, PDFs, or text files must handle each format separately, leading to:

1. **Workflow fragmentation**: Different workflows for different content types
2. **Code duplication**: Similar extraction logic scattered across multiple locations
3. **Pattern analysis limitation**: Pattern tools can't handle multiple input types
4. **No type detection**: Users must manually specify content type
5. **Inconsistent metadata**: Different sources provide different metadata structures

This creates friction when building content analysis pipelines and prevents reusable pattern-based workflows from operating on diverse content sources.

## Solution Statement

Implement a modular content extraction system with:

1. **Type auto-detection**: Automatically identify content type from input source
2. **Specialized extractors**: Dedicated modules for YouTube, URL, PDF, and text extraction
3. **Unified output**: All extractors produce a consistent `ContentObject` data structure
4. **Metadata preservation**: Source-specific metadata attached to unified objects
5. **Router pattern**: Single entry point (`extract_content()`) routes to appropriate extractor
6. **Extensible design**: Easy to add new content types by implementing the extractor interface

This enables downstream tools to consume any content type through a single, predictable interface, while preserving source-specific details when needed.

## Relevant Files

Use these files to implement the feature:

- **adws/adw_modules/data_types.py** - Add `ContentType` enum and `ContentObject` dataclass to the core type system for Jerry's ADW modules
- **adws/adw_modules/__init__.py** - Export new content extraction modules and types for easy importing across Jerry workflows
- **adws/adw_modules/utils.py** - Reference existing utilities like `get_logger()` and `parse_json()` that content extractors will use

### New Files

- **adws/adw_modules/content_extractors.py** - Main entry point with `extract_content()` router function and content type detection logic
- **adws/adw_modules/youtube_ops.py** - YouTube-specific extraction using yt-dlp for metadata and transcripts
- **adws/adw_modules/web_ops.py** - URL scraping and conversion to markdown using requests + html2text or fabric
- **adws/adw_modules/pdf_ops.py** - PDF text extraction using pypdf or pdfplumber libraries
- **adws/adw_modules/text_ops.py** - Simple text file reading and direct string handling

## Implementation Plan

### Phase 1: Foundation
Establish the core type system and detection logic that all extractors will build upon. This phase creates the data structures and routing logic needed before implementing any specific extractors.

### Phase 2: Core Implementation
Build out each specialized extractor module (YouTube, URL, PDF, text) independently. Each extractor handles a specific content type and returns the unified `ContentObject` format.

### Phase 3: Integration
Connect all extractors through the main router, update module exports, add comprehensive validation, and ensure the system works end-to-end with real content from all supported sources.

## Step by Step Tasks

IMPORTANT: Execute every step in order, respecting group dependencies.

Steps are organized into groups. Groups execute in dependency order.
Steps within a group can be parallel (independent) or sequential (ordered).

### Format:
- `### Group X: Title [parallel: bool, depends: Y, model: strategy]`
- `#### Step X.N: Step Title`

### Options:
- `parallel: true` - Steps in this group can run concurrently
- `parallel: false` - Steps must run sequentially (default)
- `depends: A, B` - This group waits for groups A and B to complete
- `model: auto|sonnet|opus` - Model selection for this group (default: auto)

### Group A: Foundation - Type System and Detection [parallel: false, model: sonnet]
Sequential setup work defining the core type system. All other work depends on these types.

#### Step A.1: Define ContentType Enum and ContentObject Dataclass
- Add `ContentType` enum to `adws/adw_modules/data_types.py` with values: YOUTUBE, URL, PDF, TEXT
- Add `ContentObject` dataclass with these fields:
  - `type: ContentType` - The detected content type
  - `text: str` - Extracted text content (transcript, scraped text, PDF text, or raw text)
  - `source: str` - Original input (URL, file path, or direct text)
  - `metadata: dict` - Type-specific metadata dictionary
  - `video_id: Optional[str]` - YouTube video ID (YouTube only)
  - `transcript_path: Optional[str]` - Path to saved transcript (YouTube only)
  - `url: Optional[str]` - Full URL (YouTube and URL types)
  - `title: Optional[str]` - Content title (YouTube and URL types)
  - `file_path: Optional[str]` - Local file path (PDF and text files)
  - `file_size: Optional[int]` - File size in bytes (PDF and text files)
- Follow existing pattern in data_types.py for docstrings and type annotations
- Validate with `uv run python -m py_compile adws/adw_modules/data_types.py`

#### Step A.2: Implement Content Type Detection Function
- Create skeleton `adws/adw_modules/content_extractors.py` file
- Implement `detect_content_type(input_source: str) -> ContentType` function
- Detection rules (in order of priority):
  - If `input_source` contains "youtube.com" or "youtu.be" → `ContentType.YOUTUBE`
  - If `input_source` starts with "http://" or "https://" → `ContentType.URL`
  - If `input_source` ends with ".pdf" or file exists and has PDF magic bytes (`%PDF`) → `ContentType.PDF`
  - Otherwise → `ContentType.TEXT`
- Add docstring explaining detection logic
- Validate with `uv run python -c "from adws.adw_modules.content_extractors import detect_content_type; print(detect_content_type('https://youtube.com/watch?v=abc'))"`

### Group B: Extractor Implementations [parallel: true, depends: A, model: auto]
Independent extractor modules that can be built in parallel. Each handles one content type.

#### Step B.1: Implement YouTube Extractor
- Create `adws/adw_modules/youtube_ops.py`
- Implement `extract_youtube_metadata(url: str) -> dict`:
  - Use yt-dlp with `--dump-json` flag to extract metadata
  - Return dict with keys: video_id, title, duration, uploader, upload_date
  - Handle errors gracefully (invalid URL, video unavailable, etc.)
- Implement `download_transcript(url: str, output_dir: str) -> str`:
  - Use yt-dlp with `--write-auto-sub --skip-download` flags
  - Save transcript to `{output_dir}/transcript_{video_id}.txt`
  - Return path to saved transcript file
  - Fall back to manual subtitles if auto-generated unavailable
- Implement `extract_youtube_content(url: str, output_dir: str) -> ContentObject`:
  - Call `extract_youtube_metadata()` to get metadata
  - Call `download_transcript()` to get transcript text
  - Read transcript file content
  - Return `ContentObject` with:
    - `type=ContentType.YOUTUBE`
    - `text=<transcript content>`
    - `source=url`
    - `video_id=<extracted ID>`
    - `transcript_path=<path to file>`
    - `url=url`
    - `title=<from metadata>`
    - `metadata=<full metadata dict>`
- Implement `classify_youtube_content(metadata: dict, transcript: str) -> str`:
  - Basic heuristic classification as "technical", "educational", or "general"
  - Check for tech keywords in title/transcript (optional enhancement)
  - Return classification string
- Add comprehensive docstrings and error handling
- Validate with real YouTube URL: `uv run python -c "from adws.adw_modules.youtube_ops import extract_youtube_content; import tempfile; result = extract_youtube_content('https://www.youtube.com/watch?v=dQw4w9WgXcQ', tempfile.gettempdir()); print(f'Success: {result.type} - {result.title}')"`

#### Step B.2: Implement URL Extractor
- Create `adws/adw_modules/web_ops.py`
- Implement `scrape_url_to_markdown(url: str) -> str`:
  - Try using `fabric --scrape_url <url>` command first (if fabric available)
  - Fall back to Python approach:
    - Use `requests` library to fetch HTML
    - Use `html2text` library to convert to markdown
    - Handle HTTP errors (404, 500, timeout)
    - Handle paywalls gracefully (note in metadata if detected)
  - Return cleaned markdown text
- Implement `extract_url_content(url: str) -> ContentObject`:
  - Call `scrape_url_to_markdown()` to get content
  - Extract title from markdown (first H1 heading) or HTML `<title>` tag
  - Return `ContentObject` with:
    - `type=ContentType.URL`
    - `text=<markdown content>`
    - `source=url`
    - `url=url`
    - `title=<extracted title>`
    - `metadata={'scrape_method': 'fabric' or 'requests', 'status_code': <code>}`
- Add error handling for common edge cases:
  - Connection timeouts
  - Invalid URLs
  - JS-heavy sites (note limitation in metadata)
- Add comprehensive docstrings
- Validate with real URL: `uv run python -c "from adws.adw_modules.web_ops import extract_url_content; result = extract_url_content('https://example.com'); print(f'Success: {result.type} - Title: {result.title}')"`

#### Step B.3: Implement PDF Extractor
- Create `adws/adw_modules/pdf_ops.py`
- Check and install PDF library dependency:
  - Try `pypdf` first: `uv add pypdf`
  - If issues, use `pdfplumber`: `uv add pdfplumber`
- Implement `extract_pdf_text(file_path: str) -> str`:
  - Check file exists
  - Use chosen library to extract all text from PDF
  - Concatenate text from all pages
  - Handle scanned PDFs gracefully (return empty string with note)
  - Return extracted text
- Implement `extract_pdf_content(file_path: str) -> ContentObject`:
  - Call `extract_pdf_text()` to get text
  - Get file size using `os.path.getsize()`
  - Extract title from filename (remove .pdf extension)
  - Return `ContentObject` with:
    - `type=ContentType.PDF`
    - `text=<extracted text>`
    - `source=file_path`
    - `file_path=file_path`
    - `file_size=<size in bytes>`
    - `title=<filename without extension>`
    - `metadata={'page_count': <count>, 'is_scanned': <bool>}`
- Add comprehensive docstrings and error handling
- Validate with test PDF: `uv run python -c "from adws.adw_modules.pdf_ops import extract_pdf_content; print('PDF extractor module validated')"`

#### Step B.4: Implement Text Extractor
- Create `adws/adw_modules/text_ops.py`
- Implement `read_text_file(file_path: str) -> str`:
  - Check if file exists
  - Read entire file content with UTF-8 encoding
  - Handle encoding errors gracefully (try latin-1 as fallback)
  - Return text content
- Implement `extract_text_content(source: str) -> ContentObject`:
  - Detect if `source` is a file path (use `os.path.exists()`)
  - If file path:
    - Call `read_text_file()` to get content
    - Get file size
    - Return `ContentObject` with file metadata
  - If direct text (not a file):
    - Use `source` as the text content directly
    - Return `ContentObject` with minimal metadata
  - Handle special case: stdin marker (`-`) for piped input
  - Return `ContentObject` with:
    - `type=ContentType.TEXT`
    - `text=<content>`
    - `source=<original source>`
    - `file_path=<path if file, None otherwise>`
    - `file_size=<size if file, None otherwise>`
    - `metadata={'is_file': <bool>, 'encoding': 'utf-8'}`
- Add comprehensive docstrings and error handling
- Validate with test: `uv run python -c "from adws.adw_modules.text_ops import extract_text_content; result = extract_text_content('test content'); print(f'Success: {result.type} - Length: {len(result.text)}')"`

### Group C: Integration and Validation [parallel: false, depends: B, model: sonnet]
Sequential integration work connecting all components and validating the complete system.

#### Step C.1: Complete Main Router in content_extractors.py
- In `adws/adw_modules/content_extractors.py`, implement:
- Import all extractor functions from B.1-B.4
- Create `CONTENT_EXTRACTORS` dictionary mapping `ContentType` to extractor functions:
  ```python
  CONTENT_EXTRACTORS = {
      ContentType.YOUTUBE: extract_youtube_content,
      ContentType.URL: extract_url_content,
      ContentType.PDF: extract_pdf_content,
      ContentType.TEXT: extract_text_content,
  }
  ```
- Implement `extract_content(input_source: str, content_type: ContentType = None, output_dir: str = None) -> ContentObject`:
  - If `content_type` is None, call `detect_content_type()` to auto-detect
  - Look up appropriate extractor from `CONTENT_EXTRACTORS` dict
  - Handle YouTube special case (needs `output_dir` parameter)
  - Call the extractor function with appropriate arguments
  - Return the resulting `ContentObject`
  - Add comprehensive error handling for unknown types
- Add module-level docstring explaining the router pattern
- Validate routing works: `uv run python -c "from adws.adw_modules.content_extractors import extract_content; print('Router validated')"`

#### Step C.2: Update Module Exports
- Edit `adws/adw_modules/__init__.py`
- Add imports for new types:
  - `ContentType` from data_types
  - `ContentObject` from data_types
- Add imports for new modules:
  - `extract_content` from content_extractors
  - `detect_content_type` from content_extractors
- Add all new exports to `__all__` list:
  - `"ContentType"`
  - `"ContentObject"`
  - `"extract_content"`
  - `"detect_content_type"`
- Validate imports work: `uv run python -c "from adws.adw_modules import ContentType, ContentObject, extract_content; print('Exports validated')"`

#### Step C.3: Create Integration Test Script
- Create test script at `adws/adw_modules/test_content_extractors.py`
- Test YouTube extraction:
  - Use a known-good public YouTube video URL
  - Validate `ContentObject` has correct type, text, video_id, title
  - Print success message
- Test URL extraction:
  - Use `https://example.com` (reliable test URL)
  - Validate `ContentObject` has correct type and text content
  - Print success message
- Test text extraction (direct string):
  - Pass plain text string
  - Validate `ContentObject` has correct type and text
  - Print success message
- Test text extraction (file):
  - Create temporary text file with known content
  - Validate `ContentObject` reads file correctly
  - Clean up temp file
- Test auto-detection:
  - Call `extract_content()` with various inputs without specifying type
  - Validate correct type is detected for each
  - Print success message
- Run test script: `uv run python adws/adw_modules/test_content_extractors.py`

#### Step C.4: Add Error Handling and Edge Case Tests
- Test invalid YouTube URL (should fail gracefully)
- Test invalid web URL (should fail gracefully)
- Test non-existent PDF file (should raise clear error)
- Test non-existent text file (should raise clear error)
- Test empty text input (should handle gracefully)
- Test stdin marker `-` (should handle gracefully)
- Validate all error cases return useful error messages
- Run edge case tests: `uv run python adws/adw_modules/test_content_extractors.py --edge-cases`

## Testing Strategy

### Unit Tests
Each extractor module should be testable independently:

1. **YouTube Extractor Tests** (`youtube_ops.py`):
   - Test metadata extraction with valid YouTube URL
   - Test transcript download with various subtitle availability scenarios
   - Test content classification logic
   - Test error handling for invalid/unavailable videos
   - Mock yt-dlp calls to avoid network dependency in fast tests

2. **URL Extractor Tests** (`web_ops.py`):
   - Test scraping with simple static HTML
   - Test markdown conversion quality
   - Test error handling for 404, timeout, connection errors
   - Test title extraction from various HTML structures
   - Mock HTTP requests for unit tests

3. **PDF Extractor Tests** (`pdf_ops.py`):
   - Test text extraction from sample PDF with known content
   - Test handling of scanned PDFs (graceful degradation)
   - Test error handling for corrupted PDFs
   - Test file size and page count metadata

4. **Text Extractor Tests** (`text_ops.py`):
   - Test file reading with UTF-8 content
   - Test direct string handling
   - Test encoding fallback (UTF-8 → latin-1)
   - Test stdin marker (`-`) handling
   - Test error handling for missing files

5. **Router Tests** (`content_extractors.py`):
   - Test content type detection for all supported formats
   - Test routing to correct extractor based on type
   - Test auto-detection vs explicit type specification
   - Test error handling for unsupported types

### Integration Tests
Full pipeline tests using real or realistic inputs:

1. **End-to-End YouTube Workflow**:
   - Provide real YouTube URL → verify complete `ContentObject` returned
   - Validate transcript file is created and readable
   - Validate metadata includes title, video_id, etc.

2. **End-to-End URL Workflow**:
   - Provide public URL → verify markdown conversion
   - Validate title extraction
   - Check metadata for scrape method used

3. **End-to-End PDF Workflow**:
   - Provide sample PDF → verify text extraction
   - Validate file size and page count in metadata

4. **End-to-End Text Workflow**:
   - Provide text file path → verify content read correctly
   - Provide direct string → verify handled as text
   - Test stdin marker behavior

5. **Cross-Type Auto-Detection**:
   - Mix of YouTube URLs, web URLs, PDF paths, text files
   - Verify each is correctly detected and processed

### Edge Cases

1. **YouTube Edge Cases**:
   - Age-restricted videos
   - Private/unlisted videos
   - Videos with no subtitles/transcripts
   - Live streams vs recorded videos
   - Deleted or unavailable videos
   - Short URLs (youtu.be format)

2. **URL Edge Cases**:
   - Redirects (301, 302)
   - Paywalled content
   - JavaScript-heavy SPAs (note limitation)
   - Very large HTML documents
   - Binary content served as text/html (malformed)
   - Connection timeouts
   - SSL/TLS certificate errors

3. **PDF Edge Cases**:
   - Encrypted/password-protected PDFs
   - Scanned image PDFs (no OCR available)
   - Corrupted PDF files
   - Very large PDFs (100+ MB)
   - PDFs with non-standard fonts or encodings
   - PDF forms with fillable fields

4. **Text Edge Cases**:
   - Empty files
   - Files with mixed encodings (UTF-8 + latin-1)
   - Binary files misidentified as text
   - Very large text files (GB size)
   - Files with no read permissions
   - Symbolic links to text files
   - Stdin marker `-` when no stdin available

5. **Detection Edge Cases**:
   - URLs that look like YouTube but aren't
   - File paths with `.pdf` in the middle but not the end
   - Text that starts with "http://" but isn't a URL
   - Ambiguous inputs (e.g., "example.pdf" text vs file)

## Acceptance Criteria

- [ ] `ContentType` enum defined in `data_types.py` with YOUTUBE, URL, PDF, TEXT values
- [ ] `ContentObject` dataclass defined with all required and optional fields
- [ ] `detect_content_type()` correctly identifies all four content types from input strings
- [ ] YouTube extractor (`youtube_ops.py`) successfully downloads transcripts via yt-dlp
- [ ] YouTube extractor extracts metadata (video_id, title, duration, uploader)
- [ ] URL extractor (`web_ops.py`) scrapes web pages and converts to markdown
- [ ] URL extractor tries fabric first, falls back to requests + html2text
- [ ] PDF extractor (`pdf_ops.py`) extracts text from PDF files using pypdf/pdfplumber
- [ ] PDF extractor handles scanned PDFs gracefully (notes limitation)
- [ ] Text extractor (`text_ops.py`) handles both file paths and direct text strings
- [ ] Text extractor supports stdin marker (`-`) for piped input
- [ ] Unified `extract_content()` router function correctly dispatches to extractors
- [ ] All extractors return consistent `ContentObject` structure
- [ ] Module exports updated in `__init__.py` to expose new types and functions
- [ ] Integration test script validates all extractors with real inputs
- [ ] Edge case handling tested for invalid inputs, errors, and edge conditions
- [ ] All validation commands pass successfully

## Validation Commands

Execute these commands to validate the feature is complete:

- `uv run python -m py_compile adws/adw_modules/data_types.py` - Validate data types compile
- `uv run python -m py_compile adws/adw_modules/content_extractors.py` - Validate main router compiles
- `uv run python -m py_compile adws/adw_modules/youtube_ops.py` - Validate YouTube extractor compiles
- `uv run python -m py_compile adws/adw_modules/web_ops.py` - Validate URL extractor compiles
- `uv run python -m py_compile adws/adw_modules/pdf_ops.py` - Validate PDF extractor compiles
- `uv run python -m py_compile adws/adw_modules/text_ops.py` - Validate text extractor compiles
- `uv run python -c "from adws.adw_modules import ContentType, ContentObject, extract_content; print('Imports OK')"` - Validate module exports
- `uv run python adws/adw_modules/test_content_extractors.py` - Run integration tests
- `uv run python -c "from adws.adw_modules.content_extractors import detect_content_type, ContentType; assert detect_content_type('https://youtube.com/watch?v=abc') == ContentType.YOUTUBE; assert detect_content_type('https://example.com') == ContentType.URL; assert detect_content_type('doc.pdf') == ContentType.PDF; assert detect_content_type('plain text') == ContentType.TEXT; print('Detection OK')"` - Validate content type detection

## Notes

### Dependencies

This feature requires installing additional Python packages via `uv`:

```bash
# YouTube extraction (yt-dlp is already installed system-wide, verify it's accessible)
which yt-dlp  # Should show /Users/ameno/.local/bin/yt-dlp

# URL scraping
uv add requests html2text

# PDF extraction (choose one)
uv add pypdf  # Recommended: pure Python, actively maintained
# OR
uv add pdfplumber  # Alternative: more features, heavier dependencies

# Optional: Check if fabric is available for URL scraping
which fabric  # If available, use as primary method
```

### Design Decisions

1. **yt-dlp vs youtube-dl**: Using yt-dlp (already installed) as it's actively maintained and faster
2. **fabric vs requests**: Prefer fabric if available for URL scraping (better quality), fall back to requests
3. **pypdf vs pdfplumber**: Start with pypdf (lighter), can add pdfplumber support later if needed
4. **Sync vs Async**: Implementation is synchronous for simplicity; async version can be added later if needed
5. **Error Handling**: Fail gracefully with clear error messages rather than silent failures
6. **Metadata Preservation**: Keep source-specific metadata in dict for extensibility

### Limitations to Document

1. **YouTube**: Requires valid URL and available subtitles/transcripts; no support for age-restricted or private videos without authentication
2. **URL**: JavaScript-heavy SPAs may not render correctly; paywall content returns partial text; requires network connectivity
3. **PDF**: Scanned PDFs without embedded text return empty content (no OCR); encrypted PDFs require password (not supported)
4. **Text**: Binary files may produce garbage output; very large files (GB+) may cause memory issues; encoding detection is best-effort

### Future Enhancements

- Add support for audio file transcription (MP3, WAV, etc.) using Whisper
- Add support for video file transcription (MP4, AVI, etc.) using Whisper
- Add OCR support for scanned PDFs using Tesseract
- Add support for other document formats (DOCX, PPTX, EPUB)
- Add caching layer to avoid re-extracting same content
- Add async/await versions of extractors for parallel processing
- Add progress callbacks for long-running extractions
- Add support for streaming large content (chunked extraction)
- Add content fingerprinting/hashing for deduplication

### Related Issues

This is Phase 3 of the larger "Jerry Patterns Content Analysis" project. It depends on:
- Phase 1: Pattern registry and execution framework (separate issue)
- Phase 2: Pattern output aggregation and reporting (separate issue)

Once content extractors are complete, they will be integrated with the pattern analysis workflows to enable commands like:
```bash
# Analyze any content source with fabric patterns
./adws/adw_analyze_content.py "https://youtube.com/watch?v=abc123"
./adws/adw_analyze_content.py "https://example.com/article"
./adws/adw_analyze_content.py "/path/to/document.pdf"
```
