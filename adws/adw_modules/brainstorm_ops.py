"""Brainstorm operations for persistent content analysis management.

This module provides operations for managing the brainstorm directory,
including manifest CRUD, slug generation, version management, and
directory structure creation.
"""

import os
import json
import re
import tempfile
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

from adws.adw_modules.data_types import (
    BrainstormManifest,
    AnalysisEntry,
    VersionInfo,
    SourceInfo,
)


def get_brainstorm_dir() -> Path:
    """Get brainstorm directory path from env or default.

    Returns:
        Path to brainstorm directory (default: ~/dev/brainstorm)
    """
    default_dir = Path.home() / "dev" / "brainstorm"
    brainstorm_dir = os.environ.get("BRAINSTORM_DIR", str(default_dir))
    return Path(brainstorm_dir)


def generate_slug(title: str, existing_slugs: Optional[set] = None) -> str:
    """Generate kebab-case slug from title with collision handling.

    Args:
        title: Content title to convert to slug
        existing_slugs: Set of existing slugs to check for collisions

    Returns:
        Unique kebab-case slug

    Examples:
        "How to Build Agents" -> "how-to-build-agents"
        "API Design (2024)" -> "api-design-2024"
        "test" (collision) -> "test-2"
    """
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)  # Remove leading/trailing hyphens
    slug = re.sub(r'-+', '-', slug)  # Collapse multiple hyphens

    # Truncate if too long (max 100 chars before suffix)
    if len(slug) > 100:
        slug = slug[:100].rstrip('-')

    # Handle collisions with numeric suffix
    if existing_slugs is None:
        return slug

    if slug not in existing_slugs:
        return slug

    # Try -2, -3, -4, etc.
    counter = 2
    while f"{slug}-{counter}" in existing_slugs:
        counter += 1

    return f"{slug}-{counter}"


def init_brainstorm_dir() -> Path:
    """Initialize brainstorm directory structure.

    Creates:
        - Brainstorm root directory
        - .schema/ subdirectory
        - manifest.json (if not exists)

    Returns:
        Path to brainstorm directory
    """
    brainstorm_dir = get_brainstorm_dir()
    brainstorm_dir.mkdir(parents=True, exist_ok=True)

    # Create .schema directory
    schema_dir = brainstorm_dir / ".schema"
    schema_dir.mkdir(exist_ok=True)

    # Create manifest if it doesn't exist
    manifest_path = brainstorm_dir / "manifest.json"
    if not manifest_path.exists():
        manifest = BrainstormManifest()
        save_manifest(manifest)

    return brainstorm_dir


def load_manifest() -> BrainstormManifest:
    """Load manifest from disk.

    Returns:
        Parsed BrainstormManifest object

    Raises:
        FileNotFoundError: If manifest doesn't exist
        json.JSONDecodeError: If manifest is invalid JSON
    """
    manifest_path = get_brainstorm_dir() / "manifest.json"

    if not manifest_path.exists():
        # Initialize if missing
        init_brainstorm_dir()
        return BrainstormManifest()

    try:
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        return BrainstormManifest.model_validate(data)
    except Exception as e:
        raise ValueError(f"Failed to load manifest: {e}")


def save_manifest(manifest: BrainstormManifest) -> None:
    """Save manifest to disk with atomic write.

    Uses temp file + rename to prevent corruption.

    Args:
        manifest: Manifest object to save
    """
    manifest_path = get_brainstorm_dir() / "manifest.json"

    # Update last_updated timestamp
    manifest.last_updated = datetime.now()

    # Atomic write: write to temp file, then rename
    with tempfile.NamedTemporaryFile(
        mode='w',
        dir=manifest_path.parent,
        delete=False,
        prefix='.manifest.tmp.',
        suffix='.json'
    ) as f:
        temp_path = f.name
        json.dump(
            manifest.model_dump(mode='json'),
            f,
            indent=2,
            default=str  # Handle datetime serialization
        )

    # Rename temp file to manifest.json (atomic on POSIX)
    os.rename(temp_path, manifest_path)


def find_analysis_by_url(url: str) -> Optional[str]:
    """Find existing analysis by source URL.

    Args:
        url: Source URL to search for

    Returns:
        Slug of matching analysis, or None if not found
    """
    try:
        manifest = load_manifest()
    except Exception:
        return None

    for slug, entry in manifest.analyses.items():
        if entry.source.url == url:
            return slug

    return None


def create_analysis_entry(
    slug: str,
    title: str,
    source_info: SourceInfo
) -> AnalysisEntry:
    """Create new analysis entry.

    Args:
        slug: Unique slug for this analysis
        title: Human-readable title
        source_info: Source information

    Returns:
        New AnalysisEntry object
    """
    return AnalysisEntry(
        slug=slug,
        title=title,
        source=source_info,
        versions=[],
        tags=[],
        blog_status=None,
        blog_post=None,
        latest_version=None
    )


def add_version(
    slug: str,
    version_info: VersionInfo
) -> None:
    """Add version to existing analysis entry.

    Args:
        slug: Analysis slug
        version_info: Version information to add

    Raises:
        ValueError: If analysis doesn't exist
    """
    manifest = load_manifest()

    if slug not in manifest.analyses:
        raise ValueError(f"Analysis {slug} not found in manifest")

    entry = manifest.analyses[slug]
    entry.versions.append(version_info)
    entry.latest_version = version_info.version

    save_manifest(manifest)


def create_version_dir(slug: str, version: str) -> Path:
    """Create version directory and update 'latest' symlink.

    Args:
        slug: Analysis slug
        version: Version string (e.g., "v1", "v2")

    Returns:
        Path to version directory
    """
    brainstorm_dir = get_brainstorm_dir()
    analysis_dir = brainstorm_dir / slug
    version_dir = analysis_dir / version

    # Create analysis directory if needed
    analysis_dir.mkdir(parents=True, exist_ok=True)

    # Create version directory
    version_dir.mkdir(parents=True, exist_ok=True)

    # Create patterns subdirectory
    (version_dir / "patterns").mkdir(exist_ok=True)

    # Update 'latest' symlink
    latest_link = analysis_dir / "latest"
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(version, target_is_directory=True)

    return version_dir


def get_existing_slugs() -> set:
    """Get set of all existing slugs from manifest.

    Returns:
        Set of slug strings
    """
    try:
        manifest = load_manifest()
        return set(manifest.analyses.keys())
    except Exception:
        return set()


def get_next_version(slug: str) -> str:
    """Get next version number for an analysis.

    Args:
        slug: Analysis slug

    Returns:
        Next version string (e.g., "v2", "v3")

    Raises:
        ValueError: If analysis doesn't exist
    """
    manifest = load_manifest()

    if slug not in manifest.analyses:
        raise ValueError(f"Analysis {slug} not found")

    entry = manifest.analyses[slug]

    if not entry.versions:
        return "v1"

    # Get latest version number
    version_nums = []
    for v in entry.versions:
        match = re.match(r'v(\d+)', v.version)
        if match:
            version_nums.append(int(match.group(1)))

    if not version_nums:
        return "v1"

    next_num = max(version_nums) + 1
    return f"v{next_num}"


def update_blog_status(
    slug: str,
    blog_status: str,
    blog_post_path: Optional[str] = None
) -> None:
    """Update blog post status and link for an analysis.

    Args:
        slug: Analysis slug
        blog_status: Status ("draft", "published", "archived")
        blog_post_path: Optional path to blog post file

    Raises:
        ValueError: If analysis doesn't exist
    """
    manifest = load_manifest()

    if slug not in manifest.analyses:
        raise ValueError(f"Analysis {slug} not found")

    entry = manifest.analyses[slug]
    entry.blog_status = blog_status
    if blog_post_path is not None:
        entry.blog_post = blog_post_path

    save_manifest(manifest)
