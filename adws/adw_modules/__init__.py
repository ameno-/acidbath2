"""Jerry ADW Modules - Agentic orchestration building blocks.

This package provides the core modules for Jerry's ADW system:
- data_types: Pydantic models for type-safe operations
- utils: Core utilities (make_adw_id, parse_json, setup_logger)
- state: Persistent state management
- agent: Claude Code CLI execution
- git_ops: Git operations
- github: GitHub API operations
- pattern_executor: Execute bundled Fabric patterns via Claude SDK
- openrouter_image: Image generation via OpenRouter API (Nano Banana fallback)
"""

from .data_types import (
    RetryCode,
    ModelSet,
    ADWWorkflow,
    SlashCommand,
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
    ClaudeCodeResultMessage,
    ADWStateData,
    ADWExtractionResult,
    GitHubUser,
    GitHubLabel,
    GitHubComment,
    GitHubIssue,
    GitHubIssueListItem,
    ContentType,
    ContentObject,
)

from .utils import (
    make_adw_id,
    setup_logger,
    get_logger,
    parse_json,
    check_env_vars,
    get_safe_subprocess_env,
    get_project_root,
    create_youtube_output_dir,
)

from .state import ADWState

# Pattern executor requires claude-code-sdk, make import optional
try:
    from .pattern_executor import (
        PatternResult,
        PatternMetadata,
        PatternManifest,
        execute_pattern,
        execute_pattern_sync,
        execute_patterns_parallel,
        execute_patterns_parallel_async,
        list_available_patterns,
        validate_pattern_exists,
        get_pattern_info,
        get_patterns_by_category,
        search_patterns,
        get_patterns_for_content_type,
        clear_pattern_cache,
    )
    _PATTERN_EXECUTOR_AVAILABLE = True
except ImportError:
    _PATTERN_EXECUTOR_AVAILABLE = False

__all__ = [
    # Data types
    "RetryCode",
    "ModelSet",
    "ADWWorkflow",
    "SlashCommand",
    "AgentPromptRequest",
    "AgentPromptResponse",
    "AgentTemplateRequest",
    "ClaudeCodeResultMessage",
    "ADWStateData",
    "ADWExtractionResult",
    "GitHubUser",
    "GitHubLabel",
    "GitHubComment",
    "GitHubIssue",
    "GitHubIssueListItem",
    "ContentType",
    "ContentObject",
    # Utils
    "make_adw_id",
    "setup_logger",
    "get_logger",
    "parse_json",
    "check_env_vars",
    "get_safe_subprocess_env",
    "get_project_root",
    "create_youtube_output_dir",
    # State
    "ADWState",
]

# Add pattern executor exports if available
if _PATTERN_EXECUTOR_AVAILABLE:
    __all__.extend([
        "PatternResult",
        "PatternMetadata",
        "PatternManifest",
        "execute_pattern",
        "execute_pattern_sync",
        "execute_patterns_parallel",
        "execute_patterns_parallel_async",
        "list_available_patterns",
        "validate_pattern_exists",
        "get_pattern_info",
        "get_patterns_by_category",
        "search_patterns",
        "get_patterns_for_content_type",
        "clear_pattern_cache",
    ])
