"""Pattern Executor Module - Execute Bundled Patterns via Claude SDK

This module executes bundled Fabric patterns using the Claude Code SDK,
eliminating the runtime dependency on the Fabric CLI tool. It provides both
synchronous and parallel pattern execution capabilities with comprehensive
error handling and type-safe results.

Key Features:
- Load patterns from .jerry/patterns/{category}/{name}/system.md
- Execute patterns via Claude SDK (agent_sdk.simple_query)
- Support parallel execution with ThreadPoolExecutor
- Pattern discovery and filtering
- In-memory caching for pattern prompts
- Comprehensive error handling and logging

Example Usage:
    # Single pattern execution
    result = execute_pattern_sync("extract_wisdom", "Sample text content")
    if result.success:
        print(f"Output: {result.output}")
        print(f"Time: {result.execution_time:.2f}s")

    # Parallel execution
    results = execute_patterns_parallel(
        ["extract_wisdom", "extract_insights", "rate_content"],
        "Sample text content"
    )
    for pattern_name, result in results.items():
        print(f"{pattern_name}: {result.success}")

    # Pattern discovery
    patterns = list_available_patterns()
    print(f"Available patterns: {patterns}")
"""

import asyncio
import json
import logging
import time
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any

from .agent_sdk import simple_query
from .utils import get_project_root

# Set up logging
logger = logging.getLogger(__name__)


# ============================================================================
# DATA TYPES
# ============================================================================

@dataclass
class PatternResult:
    """Result from executing a single pattern.

    Attributes:
        pattern: Name of the pattern that was executed
        success: Whether execution completed successfully
        output: The pattern's output text
        execution_time: Time taken to execute in seconds
        error: Error message if execution failed (None if successful)
    """
    pattern: str
    success: bool
    output: str
    execution_time: float
    error: Optional[str] = None


@dataclass
class PatternMetadata:
    """Metadata for a pattern.

    Attributes:
        name: Pattern name (e.g., "extract_wisdom")
        category: Pattern category (e.g., "analysis", "rating")
        description: Brief description of what the pattern does
        tags: List of tags for filtering/search
    """
    name: str
    category: str
    description: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class PatternManifest:
    """Pattern manifest containing all available patterns.

    This represents the structure of .jerry/manifest.json or
    dynamically generated pattern metadata.

    Attributes:
        patterns: Dict mapping pattern name to metadata
        categories: List of available categories
        version: Manifest version
    """
    patterns: Dict[str, PatternMetadata] = field(default_factory=dict)
    categories: List[str] = field(default_factory=list)
    version: str = "1.0.0"


# ============================================================================
# PATTERN LOADING AND FILE SYSTEM OPERATIONS
# ============================================================================

# In-memory cache for loaded pattern prompts
_pattern_cache: Dict[str, str] = {}


def _get_patterns_directory() -> Path:
    """Get the absolute path to the .jerry/patterns directory.

    Returns:
        Path object pointing to .jerry/patterns/

    Raises:
        FileNotFoundError: If .jerry/patterns/ directory doesn't exist
    """
    project_root = Path(get_project_root())
    patterns_dir = project_root / ".jerry" / "patterns"

    if not patterns_dir.exists():
        raise FileNotFoundError(
            f"Patterns directory not found: {patterns_dir}. "
            "Ensure Phase 1 (Pattern Infrastructure) is completed."
        )

    return patterns_dir


def get_pattern_prompt(pattern_name: str, use_cache: bool = True) -> str:
    """Load pattern system prompt from bundled patterns.

    Loads the pattern's system.md file from .jerry/patterns/{category}/{name}/system.md.
    The category is discovered by searching through all category directories.

    Args:
        pattern_name: Name of the pattern (e.g., "extract_wisdom")
        use_cache: Whether to use the in-memory cache (default: True)

    Returns:
        Content of the pattern's system.md file

    Raises:
        FileNotFoundError: If pattern doesn't exist or system.md is missing

    Example:
        prompt = get_pattern_prompt("extract_wisdom")
        print(f"Pattern prompt: {prompt[:100]}...")
    """
    # Check cache first
    if use_cache and pattern_name in _pattern_cache:
        logger.debug(f"Loading pattern '{pattern_name}' from cache")
        return _pattern_cache[pattern_name]

    patterns_dir = _get_patterns_directory()

    # Search for pattern in all category directories
    pattern_path = None
    for category_dir in patterns_dir.iterdir():
        if not category_dir.is_dir():
            continue

        candidate = category_dir / pattern_name / "system.md"
        if candidate.exists():
            pattern_path = candidate
            break

    if pattern_path is None:
        available = [
            p.parent.name
            for cat in patterns_dir.iterdir()
            if cat.is_dir()
            for p in cat.iterdir()
            if p.is_dir() and (p / "system.md").exists()
        ]
        raise FileNotFoundError(
            f"Pattern '{pattern_name}' not found. "
            f"Available patterns: {', '.join(available)}"
        )

    # Load and cache the prompt
    logger.debug(f"Loading pattern '{pattern_name}' from {pattern_path}")
    content = pattern_path.read_text(encoding="utf-8")

    if use_cache:
        _pattern_cache[pattern_name] = content

    return content


def validate_pattern_exists(pattern_name: str) -> bool:
    """Check if a pattern is available in the bundle.

    Args:
        pattern_name: Name of the pattern to check

    Returns:
        True if pattern exists, False otherwise

    Example:
        if validate_pattern_exists("extract_wisdom"):
            print("Pattern is available!")
    """
    try:
        get_pattern_prompt(pattern_name, use_cache=False)
        return True
    except FileNotFoundError:
        return False


def clear_pattern_cache():
    """Clear the in-memory pattern cache.

    Useful for cache invalidation after pattern updates.
    """
    global _pattern_cache
    _pattern_cache.clear()
    logger.debug("Pattern cache cleared")


# ============================================================================
# PATTERN DISCOVERY FUNCTIONS
# ============================================================================

def list_available_patterns() -> dict:
    """List all bundled patterns with metadata.

    Scans the .jerry/patterns/ directory and returns a manifest-like structure
    containing all available patterns organized by category.

    Returns:
        Dictionary with structure:
        {
            "patterns": {
                "pattern_name": {
                    "name": "pattern_name",
                    "category": "category_name",
                    "path": "category/pattern_name"
                },
                ...
            },
            "categories": ["category1", "category2", ...],
            "total_count": N
        }

    Raises:
        FileNotFoundError: If .jerry/patterns/ directory doesn't exist

    Example:
        patterns = list_available_patterns()
        print(f"Found {patterns['total_count']} patterns")
        for name, info in patterns['patterns'].items():
            print(f"  - {name} ({info['category']})")
    """
    try:
        patterns_dir = _get_patterns_directory()
    except FileNotFoundError as e:
        logger.error(f"Failed to list patterns: {e}")
        raise

    patterns = {}
    categories = set()

    # Scan all category directories
    for category_dir in patterns_dir.iterdir():
        if not category_dir.is_dir():
            continue

        category_name = category_dir.name
        categories.add(category_name)

        # Scan pattern directories in this category
        for pattern_dir in category_dir.iterdir():
            if not pattern_dir.is_dir():
                continue

            system_md = pattern_dir / "system.md"
            if not system_md.exists():
                continue

            pattern_name = pattern_dir.name
            patterns[pattern_name] = {
                "name": pattern_name,
                "category": category_name,
                "path": f"{category_name}/{pattern_name}",
            }

    result = {
        "patterns": patterns,
        "categories": sorted(list(categories)),
        "total_count": len(patterns),
    }

    logger.debug(
        f"Found {len(patterns)} patterns in {len(categories)} categories"
    )

    return result


def get_pattern_info(pattern_name: str) -> dict:
    """Get full metadata for a specific pattern.

    Args:
        pattern_name: Name of the pattern

    Returns:
        Dictionary with pattern metadata:
        {
            "name": "pattern_name",
            "category": "category_name",
            "path": "category/pattern_name",
            "exists": True,
            "system_md_size": 1234
        }

    Raises:
        FileNotFoundError: If pattern doesn't exist

    Example:
        info = get_pattern_info("extract_wisdom")
        print(f"Pattern: {info['name']}")
        print(f"Category: {info['category']}")
        print(f"Size: {info['system_md_size']} bytes")
    """
    patterns_dir = _get_patterns_directory()

    # Search for pattern in all category directories
    for category_dir in patterns_dir.iterdir():
        if not category_dir.is_dir():
            continue

        pattern_dir = category_dir / pattern_name
        system_md = pattern_dir / "system.md"

        if system_md.exists():
            return {
                "name": pattern_name,
                "category": category_dir.name,
                "path": f"{category_dir.name}/{pattern_name}",
                "exists": True,
                "system_md_size": system_md.stat().st_size,
            }

    raise FileNotFoundError(f"Pattern '{pattern_name}' not found")


# ============================================================================
# PATTERN EXECUTION
# ============================================================================

async def execute_pattern(
    pattern_name: str,
    input_text: str,
    model: str = "haiku"
) -> PatternResult:
    """Execute a single pattern against input text via Claude SDK.

    This is the async version that directly uses the agent_sdk.simple_query()
    function. For synchronous usage, use execute_pattern_sync().

    Args:
        pattern_name: Name of the pattern to execute
        input_text: Input text to analyze with the pattern
        model: Claude model to use ("haiku", "sonnet", or "opus")

    Returns:
        PatternResult with execution details

    Example:
        result = await execute_pattern("extract_wisdom", "Sample text", model="haiku")
        if result.success:
            print(result.output)
        else:
            print(f"Error: {result.error}")
    """
    start_time = time.perf_counter()

    try:
        # Load pattern prompt
        logger.debug(f"Loading pattern '{pattern_name}'")
        system_prompt = get_pattern_prompt(pattern_name)

        # Construct full prompt
        full_prompt = f"{system_prompt}\n\n# INPUT\n\n{input_text}"

        # Map model shorthand to full model name
        model_map = {
            "haiku": "claude-3-5-haiku-20241022",
            "sonnet": "claude-sonnet-4-20250514",
            "opus": "claude-opus-4-20250514",
        }
        full_model = model_map.get(model, f"claude-{model}-4-20250514")

        # Execute using Claude SDK
        logger.info(f"Executing pattern '{pattern_name}' with model '{full_model}'")
        output = await simple_query(full_prompt, model=full_model)

        execution_time = time.perf_counter() - start_time

        logger.info(
            f"Pattern '{pattern_name}' completed successfully in {execution_time:.2f}s"
        )

        return PatternResult(
            pattern=pattern_name,
            success=True,
            output=output,
            execution_time=execution_time,
            error=None
        )

    except FileNotFoundError as e:
        execution_time = time.perf_counter() - start_time
        error_msg = f"Pattern not found: {str(e)}"
        logger.error(f"Pattern '{pattern_name}' failed: {error_msg}")

        return PatternResult(
            pattern=pattern_name,
            success=False,
            output="",
            execution_time=execution_time,
            error=error_msg
        )

    except Exception as e:
        execution_time = time.perf_counter() - start_time
        error_msg = f"Execution error: {str(e)}"
        logger.error(f"Pattern '{pattern_name}' failed: {error_msg}", exc_info=True)

        return PatternResult(
            pattern=pattern_name,
            success=False,
            output="",
            execution_time=execution_time,
            error=error_msg
        )


def execute_pattern_sync(
    pattern_name: str,
    input_text: str,
    model: str = "haiku"
) -> PatternResult:
    """Synchronous wrapper for execute_pattern().

    This function provides a synchronous interface to the async execute_pattern()
    function, making it easier to use in synchronous contexts.

    Args:
        pattern_name: Name of the pattern to execute
        input_text: Input text to analyze with the pattern
        model: Claude model to use ("haiku", "sonnet", or "opus")

    Returns:
        PatternResult with execution details

    Example:
        result = execute_pattern_sync("extract_wisdom", "Sample text")
        print(f"Success: {result.success}, Time: {result.execution_time:.2f}s")
    """
    # Handle event loop properly for different Python versions
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, we need to use asyncio.run in a new thread
            # This is a fallback for nested async contexts
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(
                    asyncio.run,
                    execute_pattern(pattern_name, input_text, model)
                )
                return future.result()
        else:
            # Use the existing loop
            return loop.run_until_complete(execute_pattern(pattern_name, input_text, model))
    except RuntimeError:
        # No event loop exists, create one
        return asyncio.run(execute_pattern(pattern_name, input_text, model))


async def execute_patterns_parallel_async(
    patterns: List[str],
    input_text: str,
    model: str = "haiku",
    max_workers: int = 4
) -> Dict[str, PatternResult]:
    """Execute multiple patterns in parallel (async version).

    Uses asyncio.gather() to execute patterns concurrently, providing
    better performance than ThreadPoolExecutor for I/O-bound operations.

    Args:
        patterns: List of pattern names to execute
        input_text: Input text to analyze with all patterns
        model: Claude model to use ("haiku", "sonnet", or "opus")
        max_workers: Maximum number of concurrent executions (currently unused, kept for API compatibility)

    Returns:
        Dictionary mapping pattern name to PatternResult

    Example:
        results = await execute_patterns_parallel_async(
            ["extract_wisdom", "extract_insights", "rate_content"],
            "Sample text content"
        )
        for name, result in results.items():
            print(f"{name}: {result.success}")
    """
    logger.info(f"Executing {len(patterns)} patterns in parallel with model '{model}'")
    start_time = time.perf_counter()

    # Execute all patterns concurrently using asyncio.gather
    tasks = [execute_pattern(pattern, input_text, model) for pattern in patterns]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)

    # Map results to pattern names
    results = {}
    for pattern, result in zip(patterns, results_list):
        if isinstance(result, Exception):
            # Handle exceptions from gather
            logger.error(f"Pattern '{pattern}' raised exception: {result}", exc_info=result)
            results[pattern] = PatternResult(
                pattern=pattern,
                success=False,
                output="",
                execution_time=0.0,
                error=str(result)
            )
        else:
            results[pattern] = result

    total_time = time.perf_counter() - start_time
    successful = sum(1 for r in results.values() if r.success)
    logger.info(
        f"Parallel execution complete: {successful}/{len(patterns)} succeeded in {total_time:.2f}s"
    )

    return results


def execute_patterns_parallel(
    patterns: List[str],
    input_text: str,
    model: str = "haiku",
    max_workers: int = 4
) -> Dict[str, PatternResult]:
    """Execute multiple patterns in parallel (synchronous version).

    Uses ThreadPoolExecutor to execute patterns concurrently in separate threads.
    Each thread runs its own async event loop for pattern execution.

    Args:
        patterns: List of pattern names to execute
        input_text: Input text to analyze with all patterns
        model: Claude model to use ("haiku", "sonnet", or "opus")
        max_workers: Maximum number of concurrent threads (default: 4)

    Returns:
        Dictionary mapping pattern name to PatternResult

    Example:
        results = execute_patterns_parallel(
            ["extract_wisdom", "extract_insights", "rate_content"],
            "Sample text content",
            max_workers=3
        )
        for name, result in results.items():
            print(f"{name}: {result.success}")
    """
    logger.info(f"Executing {len(patterns)} patterns in parallel (sync) with {max_workers} workers")
    start_time = time.perf_counter()

    results = {}

    # Execute patterns in thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all pattern executions
        future_to_pattern = {
            executor.submit(execute_pattern_sync, pattern, input_text, model): pattern
            for pattern in patterns
        }

        # Collect results as they complete
        for future in as_completed(future_to_pattern):
            pattern = future_to_pattern[future]
            try:
                result = future.result()
                results[pattern] = result
            except Exception as e:
                logger.error(f"Pattern '{pattern}' raised exception: {e}", exc_info=True)
                results[pattern] = PatternResult(
                    pattern=pattern,
                    success=False,
                    output="",
                    execution_time=0.0,
                    error=str(e)
                )

    total_time = time.perf_counter() - start_time
    successful = sum(1 for r in results.values() if r.success)
    logger.info(
        f"Parallel execution complete: {successful}/{len(patterns)} succeeded in {total_time:.2f}s"
    )

    return results


# ============================================================================
# ADVANCED PATTERN FILTERING AND SEARCH
# ============================================================================

def get_patterns_by_category(category: str) -> List[str]:
    """Get all patterns in a specific category.

    Args:
        category: Category name (e.g., "analysis", "rating")

    Returns:
        List of pattern names in the category

    Example:
        analysis_patterns = get_patterns_by_category("analysis")
        print(f"Analysis patterns: {analysis_patterns}")
    """
    patterns_data = list_available_patterns()

    matching_patterns = [
        name
        for name, info in patterns_data["patterns"].items()
        if info["category"] == category
    ]

    logger.debug(f"Found {len(matching_patterns)} patterns in category '{category}'")
    return matching_patterns


def search_patterns(query: str) -> List[str]:
    """Search patterns by name or description.

    Performs case-insensitive substring matching on pattern names.
    Future enhancement: Could add description/tag search if metadata is available.

    Args:
        query: Search query string

    Returns:
        List of matching pattern names

    Example:
        wisdom_patterns = search_patterns("wisdom")
        print(f"Wisdom-related patterns: {wisdom_patterns}")
    """
    patterns_data = list_available_patterns()
    query_lower = query.lower()

    # Simple fuzzy matching on pattern name
    matching_patterns = [
        name
        for name in patterns_data["patterns"].keys()
        if query_lower in name.lower()
    ]

    logger.debug(f"Search '{query}' found {len(matching_patterns)} patterns")
    return matching_patterns


def get_patterns_for_content_type(content_type: str, preset: Optional[str] = None) -> List[str]:
    """Get recommended patterns for a content type.

    This provides content-type-specific pattern recommendations.
    The mapping can be extended based on use cases.

    Args:
        content_type: Type of content (e.g., "article", "video", "code", "general")
        preset: Optional preset name to use instead of content-type recommendations

    Returns:
        List of recommended pattern names

    Example:
        article_patterns = get_patterns_for_content_type("article")
        print(f"Recommended for articles: {article_patterns}")

        # Or with preset
        acidbath_patterns = get_patterns_for_content_type("article", preset="acidbath")
    """
    # If preset specified, use it instead of content type recommendations
    if preset:
        try:
            patterns = get_patterns_for_preset(preset)
            logger.debug(f"Using preset '{preset}' with {len(patterns)} patterns")
            return patterns
        except Exception as e:
            logger.warning(f"Failed to load preset '{preset}': {e}. Falling back to content type.")

    # Content type to pattern recommendations
    # This is a basic mapping that can be extended
    recommendations = {
        "article": ["extract_wisdom", "extract_insights", "summarize", "rate_content"],
        "video": ["extract_wisdom", "extract_insights", "summarize"],
        "code": ["explain_code", "analyze_code", "rate_content"],
        "technical": ["extract_insights", "analyze_tech", "summarize"],
        "general": ["extract_wisdom", "extract_insights", "summarize"],
    }

    # Default to general if content_type not found
    recommended = recommendations.get(content_type.lower(), recommendations["general"])

    # Filter to only patterns that actually exist
    all_patterns = list_available_patterns()["patterns"]
    available_recommended = [p for p in recommended if p in all_patterns]

    logger.debug(
        f"Content type '{content_type}' has {len(available_recommended)} recommended patterns"
    )

    return available_recommended


# ============================================================================
# PRESET SYSTEM
# ============================================================================

def load_preset(preset_name: str) -> Dict[str, Any]:
    """Load a preset configuration from .jerry/presets/{name}.yaml.

    Args:
        preset_name: Name of the preset (e.g., "acidbath")

    Returns:
        Dictionary containing preset configuration

    Raises:
        FileNotFoundError: If preset doesn't exist
        ValueError: If preset YAML is invalid

    Example:
        preset = load_preset("acidbath")
        print(f"Preset: {preset['name']}")
        print(f"Patterns: {get_patterns_for_preset('acidbath')}")
    """
    project_root = Path(get_project_root())
    presets_dir = project_root / ".jerry" / "presets"
    preset_file = presets_dir / f"{preset_name}.yaml"

    if not preset_file.exists():
        raise FileNotFoundError(
            f"Preset '{preset_name}' not found at {preset_file}. "
            f"Available presets: {list_available_presets()}"
        )

    try:
        with open(preset_file, 'r') as f:
            preset_config = yaml.safe_load(f)

        if not preset_config:
            raise ValueError(f"Empty preset configuration: {preset_file}")

        logger.debug(f"Loaded preset '{preset_name}' from {preset_file}")
        return preset_config

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in preset '{preset_name}': {e}")


def get_patterns_for_preset(preset_name: str) -> List[str]:
    """Get the full list of patterns defined in a preset.

    Combines always_run, custom, and supporting patterns from the preset.

    Args:
        preset_name: Name of the preset

    Returns:
        List of pattern names to execute

    Raises:
        FileNotFoundError: If preset doesn't exist
        ValueError: If any pattern in the preset doesn't exist

    Example:
        patterns = get_patterns_for_preset("acidbath")
        print(f"ACIDBATH preset includes {len(patterns)} patterns")
    """
    preset_config = load_preset(preset_name)

    # Collect all patterns from different sections
    all_patterns = []

    # Add always_run patterns
    if "always_run" in preset_config:
        all_patterns.extend(preset_config["always_run"])

    # Add custom patterns
    if "custom" in preset_config:
        all_patterns.extend(preset_config["custom"])

    # Add supporting patterns
    if "supporting" in preset_config:
        all_patterns.extend(preset_config["supporting"])

    # Convert paths like "technical/extract_poc" to just "extract_poc"
    pattern_names = []
    for pattern in all_patterns:
        if "/" in pattern:
            # Extract just the pattern name (last part)
            pattern_name = pattern.split("/")[-1]
        else:
            pattern_name = pattern
        pattern_names.append(pattern_name)

    # Validate all patterns exist
    all_available = list_available_patterns()["patterns"]
    missing = [p for p in pattern_names if p not in all_available]
    if missing:
        raise ValueError(
            f"Preset '{preset_name}' references missing patterns: {', '.join(missing)}"
        )

    logger.debug(f"Preset '{preset_name}' contains {len(pattern_names)} patterns")
    return pattern_names


def list_available_presets() -> List[str]:
    """List all available presets in .jerry/presets/.

    Returns:
        List of preset names (without .yaml extension)

    Example:
        presets = list_available_presets()
        print(f"Available presets: {', '.join(presets)}")
    """
    project_root = Path(get_project_root())
    presets_dir = project_root / ".jerry" / "presets"

    if not presets_dir.exists():
        logger.debug(f"Presets directory not found: {presets_dir}")
        return []

    presets = []
    for preset_file in presets_dir.glob("*.yaml"):
        presets.append(preset_file.stem)

    logger.debug(f"Found {len(presets)} presets")
    return sorted(presets)


def validate_preset(preset_name: str) -> bool:
    """Validate that a preset is correctly formatted and all patterns exist.

    Args:
        preset_name: Name of the preset to validate

    Returns:
        True if preset is valid, False otherwise

    Example:
        if validate_preset("acidbath"):
            print("Preset is valid!")
    """
    try:
        # Load preset
        preset_config = load_preset(preset_name)

        # Check required fields
        if "name" not in preset_config:
            logger.error(f"Preset '{preset_name}' missing 'name' field")
            return False

        # Get and validate patterns
        patterns = get_patterns_for_preset(preset_name)

        # All patterns validated if we get here
        logger.debug(f"Preset '{preset_name}' is valid ({len(patterns)} patterns)")
        return True

    except Exception as e:
        logger.error(f"Preset '{preset_name}' validation failed: {e}")
        return False
