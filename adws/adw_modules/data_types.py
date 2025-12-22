"""Data types for Jerry ADW system.

Generic, deployment-agnostic types for agentic orchestration.
App-specific types should be added per-deployment, not here.
"""

from datetime import datetime
from typing import Optional, List, Literal, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# Content extraction types for multi-source content analysis
class ContentType(str, Enum):
    """Type of content being extracted."""

    YOUTUBE = "youtube"
    URL = "url"
    PDF = "pdf"
    TEXT = "text"
    GITHUB = "github"


class ContentObject(BaseModel):
    """Unified content object from any source.

    All content extractors return this unified structure, enabling
    pattern analysis tools to work with any content type.

    Attributes:
        type: The detected content type
        text: Extracted text content (transcript, scraped text, PDF text, or raw text)
        source: Original input (URL, file path, or direct text)
        metadata: Type-specific metadata dictionary
        video_id: YouTube video ID (YouTube only)
        transcript_path: Path to saved transcript (YouTube only)
        url: Full URL (YouTube and URL types)
        title: Content title (YouTube and URL types)
        file_path: Local file path (PDF and text files)
        file_size: File size in bytes (PDF and text files)
    """

    type: ContentType
    text: str
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    video_id: Optional[str] = None
    transcript_path: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None


# Issue source types for multi-source issue abstraction
class IssueSource(str, Enum):
    """Source of an issue."""

    GITHUB = "github"
    GITLAB = "gitlab"
    LINEAR = "linear"
    LOCAL = "local"
    PROMPT = "prompt"


class IssueStatus(str, Enum):
    """Status for local issue tracking."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


# Retry codes for Claude Code execution errors
class RetryCode(str, Enum):
    """Codes indicating different types of errors that may be retryable."""

    CLAUDE_CODE_ERROR = "claude_code_error"  # General Claude Code CLI error
    TIMEOUT_ERROR = "timeout_error"  # Command timed out
    EXECUTION_ERROR = "execution_error"  # Error during execution
    ERROR_DURING_EXECUTION = "error_during_execution"  # Agent encountered an error
    NONE = "none"  # No retry needed


# Model set types for ADW workflows
ModelSet = Literal["base", "heavy"]

# Model selection strategy for step-level orchestration
# - auto: Estimate complexity, use opus for large/complex steps
# - sonnet: Always use sonnet (fast, cost-effective)
# - opus: Always use opus (deep reasoning)
# - heavy-for-build: Use opus for implementation steps, sonnet otherwise
ModelStrategy = Literal["auto", "sonnet", "opus", "heavy-for-build"]


# Step status matching legacy tac8_app2 pattern: [] → [⏰] → [🟡] → [✅]/[❌]
class StepStatus(str, Enum):
    """Status of a step in an execution plan."""

    PENDING = "pending"  # [] - ready to run, no dependencies blocking
    BLOCKED = "blocked"  # [⏰] - waiting on dependencies to complete
    IN_PROGRESS = "in_progress"  # [🟡, adw_id] - agent currently working
    COMPLETED = "completed"  # [✅ commit, adw_id] - successfully finished
    FAILED = "failed"  # [❌, adw_id] - error occurred
    SKIPPED = "skipped"  # Skipped due to upstream failure


class StepDefinition(BaseModel):
    """Definition of a single step in an execution plan.

    Tracks step metadata and execution state for step-level orchestration.
    """

    step_id: str  # Unique identifier, e.g., "A.1", "B.2"
    group_id: str  # Parent group identifier
    title: str  # Step title from spec
    description: str  # Full step description/instructions
    status: StepStatus = StepStatus.PENDING
    adw_id: Optional[str] = None  # Agent ID that claimed this step
    commit_hash: Optional[str] = None  # Commit hash if successful
    result_summary: Optional[str] = None  # Brief summary of what was done
    error_message: Optional[str] = None  # Error message if failed


class StepGroup(BaseModel):
    """Group of steps with execution configuration.

    Groups can be:
    - Sequential (parallel=False): Steps run one at a time
    - Parallel (parallel=True): Steps can run concurrently

    Groups respect dependencies: a group only starts when all
    groups in depends_on have completed successfully.
    """

    group_id: str  # Unique identifier, e.g., "A", "B", "C"
    title: str  # Group title from spec
    parallel: bool = False  # Whether steps in this group can run in parallel
    depends_on: List[str] = Field(default_factory=list)  # Group IDs this depends on
    model_strategy: ModelStrategy = "auto"  # Model selection for this group
    steps: List[StepDefinition] = Field(default_factory=list)

    def all_completed(self) -> bool:
        """Check if all steps in this group are completed."""
        return all(s.status == StepStatus.COMPLETED for s in self.steps)

    def any_failed(self) -> bool:
        """Check if any step in this group failed."""
        return any(s.status == StepStatus.FAILED for s in self.steps)


class ExecutionPlan(BaseModel):
    """Full execution plan parsed from a spec file.

    Represents the structured form of a spec's "Step by Step Tasks"
    section with groups, dependencies, and execution status.
    """

    plan_file: str  # Path to the spec file
    groups: List[StepGroup] = Field(default_factory=list)
    current_group: Optional[str] = None  # Currently executing group
    current_step: Optional[str] = None  # Currently executing step

    def get_group(self, group_id: str) -> Optional[StepGroup]:
        """Get a group by ID."""
        for group in self.groups:
            if group.group_id == group_id:
                return group
        return None

    def get_step(self, step_id: str) -> Optional[StepDefinition]:
        """Get a step by ID (searches all groups)."""
        for group in self.groups:
            for step in group.steps:
                if step.step_id == step_id:
                    return step
        return None

    def get_eligible_groups(self) -> List[StepGroup]:
        """Get groups whose dependencies are all completed."""
        completed_groups = {g.group_id for g in self.groups if g.all_completed()}
        eligible = []
        for group in self.groups:
            if group.all_completed() or group.any_failed():
                continue  # Skip completed or failed groups
            if all(dep in completed_groups for dep in group.depends_on):
                eligible.append(group)
        return eligible

    def total_steps(self) -> int:
        """Get total number of steps."""
        return sum(len(g.steps) for g in self.groups)

    def completed_steps(self) -> int:
        """Get number of completed steps."""
        return sum(
            1 for g in self.groups for s in g.steps if s.status == StepStatus.COMPLETED
        )


# ADW workflow types - generic orchestration workflows only
# App-specific workflows should extend this per-deployment
ADWWorkflow = Literal[
    "adw_plan_iso",  # Planning only
    "adw_build_iso",  # Building only (dependent workflow)
    "adw_patch_iso",  # Direct patch from issue
    "adw_ship_iso",  # Ship/deployment workflow
    "adw_plan_build_iso",  # Plan + Build
    "adw_import_workflow",  # Import workflow from sibling
]

# Core slash commands for orchestration
# App-specific commands should be added per-deployment
SlashCommand = Literal[
    # Core orchestration commands
    "/plan",
    "/build",
    "/implement",
    "/commit",
    "/pull_request",
    # Meta commands
    "/classify_issue",
    "/classify_adw",
    "/generate_branch_name",
    "/import_workflow",
    # Worktree commands
    "/init_worktree",
    "/install_worktree",
    "/clean_worktree",
    "/cleanup_worktrees",
]


class AgentPromptRequest(BaseModel):
    """Claude Code agent prompt configuration."""

    prompt: str
    adw_id: str
    agent_name: str = "ops"
    model: Literal["sonnet", "opus"] = "sonnet"
    dangerously_skip_permissions: bool = False
    output_file: str
    working_dir: Optional[str] = None


class AgentPromptResponse(BaseModel):
    """Claude Code agent response with token usage tracking.

    Includes comprehensive token usage statistics for efficiency tracking
    and cost management. Token data is extracted from the result message.
    """

    output: str
    success: bool
    session_id: Optional[str] = None
    retry_code: RetryCode = RetryCode.NONE
    # Token usage tracking (populated from result message)
    token_usage: Optional["TokenUsage"] = None
    model_usage: Optional[List["ModelUsage"]] = None

    def get_usage_summary(self) -> str:
        """Get a formatted summary of token usage for logging."""
        if not self.token_usage:
            return "Token usage: Not available"
        summary = self.token_usage.format_summary()
        if self.model_usage:
            model_summaries = [m.format_summary() for m in self.model_usage]
            summary += "\n  " + "\n  ".join(model_summaries)
        return summary


class AgentTemplateRequest(BaseModel):
    """Claude Code agent template execution request."""

    agent_name: str
    slash_command: str  # String to allow extension beyond SlashCommand literal
    args: List[str]
    adw_id: str
    model: Literal["sonnet", "opus"] = "sonnet"
    working_dir: Optional[str] = None


class TokenUsage(BaseModel):
    """Token usage statistics from Claude Code execution.

    Provides accurate accounting of tokens consumed per agent execution
    for tracking efficiency and cost management.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    total_tokens: int = 0  # Computed: input + output
    total_cost_usd: float = 0.0
    duration_ms: int = 0
    duration_api_ms: int = 0
    num_turns: int = 0

    @classmethod
    def from_result_message(cls, result_msg: Dict[str, Any]) -> "TokenUsage":
        """Create TokenUsage from a Claude Code result message."""
        usage = result_msg.get("usage", {})
        return cls(
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            cache_read_input_tokens=usage.get("cache_read_input_tokens", 0),
            cache_creation_input_tokens=usage.get("cache_creation_input_tokens", 0),
            total_tokens=usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
            total_cost_usd=result_msg.get("total_cost_usd", 0.0),
            duration_ms=result_msg.get("duration_ms", 0),
            duration_api_ms=result_msg.get("duration_api_ms", 0),
            num_turns=result_msg.get("num_turns", 0),
        )

    def format_summary(self) -> str:
        """Format token usage as a human-readable summary string."""
        return (
            f"Tokens: {self.total_tokens:,} (in: {self.input_tokens:,}, out: {self.output_tokens:,}) | "
            f"Cache: {self.cache_read_input_tokens:,} read, {self.cache_creation_input_tokens:,} created | "
            f"Cost: ${self.total_cost_usd:.4f} | "
            f"Duration: {self.duration_ms / 1000:.1f}s ({self.num_turns} turns)"
        )


class ModelUsage(BaseModel):
    """Per-model token usage breakdown.

    When multiple models are used in a single execution (e.g., haiku for
    classification, sonnet for implementation), this tracks usage per model.
    """

    model_id: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cost_usd: float = 0.0

    @classmethod
    def from_model_entry(cls, model_id: str, data: Dict[str, Any]) -> "ModelUsage":
        """Create ModelUsage from a modelUsage entry."""
        return cls(
            model_id=model_id,
            input_tokens=data.get("inputTokens", 0),
            output_tokens=data.get("outputTokens", 0),
            cache_read_input_tokens=data.get("cacheReadInputTokens", 0),
            cache_creation_input_tokens=data.get("cacheCreationInputTokens", 0),
            cost_usd=data.get("costUSD", 0.0),
        )

    def format_summary(self) -> str:
        """Format model usage as a human-readable summary string."""
        return (
            f"{self.model_id}: {self.input_tokens + self.output_tokens:,} tokens "
            f"(in: {self.input_tokens:,}, out: {self.output_tokens:,}) "
            f"${self.cost_usd:.4f}"
        )


class ClaudeCodeResultMessage(BaseModel):
    """Claude Code JSONL result message (last line)."""

    type: str
    subtype: str
    is_error: bool
    duration_ms: int
    duration_api_ms: int
    num_turns: int
    result: str
    session_id: str
    total_cost_usd: float
    # Token usage fields (optional for backward compatibility)
    usage: Optional[Dict[str, Any]] = None
    model_usage: Optional[Dict[str, Any]] = Field(default=None, alias="modelUsage")

    class Config:
        populate_by_name = True


class ADWStateData(BaseModel):
    """Minimal persistent state for ADW workflow.

    Stored in agents/{adw_id}/adw_state.json
    Contains only essential identifiers to connect workflow steps.

    This is the core state - app-specific state should extend this.
    """

    adw_id: str
    issue_number: Optional[str] = None
    issue_source: Optional[str] = None  # "github", "local", "prompt", "linear"
    issue_ref: Optional[str] = None  # Full reference for re-fetching (e.g., "github:123")
    branch_name: Optional[str] = None
    plan_file: Optional[str] = None
    issue_class: Optional[str] = None  # Generic string, not hardcoded to specific commands
    worktree_path: Optional[str] = None
    backend_port: Optional[int] = None
    frontend_port: Optional[int] = None
    model_set: Optional[ModelSet] = "base"
    all_adws: List[str] = Field(default_factory=list)

    # Step-level execution tracking (new)
    execution_plan: Optional[Dict[str, Any]] = None  # Serialized ExecutionPlan for progress tracking
    model_strategy: Optional[ModelStrategy] = "auto"  # Model selection strategy for this ADW
    phases_completed: List[str] = Field(default_factory=list)  # List of completed phase/group IDs

    # Generic metadata for extensibility
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ADWExtractionResult(BaseModel):
    """Result from extracting ADW information from text."""

    workflow_command: Optional[str] = None  # e.g., "adw_plan_iso" (without slash)
    adw_id: Optional[str] = None  # 8-character ADW ID
    model_set: Optional[ModelSet] = "base"  # Model set to use, defaults to "base"

    @property
    def has_workflow(self) -> bool:
        """Check if a workflow command was extracted."""
        return self.workflow_command is not None


# GitHub types - generic for any GitHub-integrated workflow
class GitHubUser(BaseModel):
    """GitHub user model."""

    id: Optional[str] = None
    login: str
    name: Optional[str] = None
    is_bot: bool = Field(default=False, alias="is_bot")


class GitHubLabel(BaseModel):
    """GitHub label model."""

    id: str
    name: str
    color: str
    description: Optional[str] = None


class GitHubComment(BaseModel):
    """GitHub comment model."""

    id: str
    author: GitHubUser
    body: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")


class GitHubIssue(BaseModel):
    """GitHub issue model."""

    number: int
    title: str
    body: str
    state: str
    author: GitHubUser
    assignees: List[GitHubUser] = []
    labels: List[GitHubLabel] = []
    comments: List[GitHubComment] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    closed_at: Optional[datetime] = Field(None, alias="closedAt")
    url: str

    class Config:
        populate_by_name = True


class GitHubIssueListItem(BaseModel):
    """GitHub issue model for list responses (simplified)."""

    number: int
    title: str
    body: str
    labels: List[GitHubLabel] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True


# Code review platform types
class CodeReviewPlatform(str, Enum):
    """Platform for code reviews (PRs, MRs)."""

    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"
    LOCAL = "local"  # For dry-run/testing


class CodeReviewStatus(str, Enum):
    """Status of a code review."""

    DRAFT = "draft"
    OPEN = "open"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    MERGED = "merged"
    CLOSED = "closed"


class CodeReview(BaseModel):
    """Generic code review model - works with any platform (GitHub PRs, GitLab MRs, etc.).

    This abstraction enables ADWs to create and manage code reviews
    without tight coupling to any specific platform.
    """

    id: str  # PR number for GitHub, MR iid for GitLab
    title: str
    body: str
    branch_name: str
    platform: CodeReviewPlatform
    url: Optional[str] = None
    status: CodeReviewStatus = CodeReviewStatus.OPEN
    issue_ref: Optional[str] = None  # Linked issue reference
    base_branch: str = "main"  # Target branch for merge

    # Merge details
    merge_method: Optional[str] = None  # "merge", "squash", "rebase"
    merged_at: Optional[datetime] = None
    merged_by: Optional[str] = None

    class Config:
        populate_by_name = True


class Issue(BaseModel):
    """Generic issue model - works with any source (GitHub, Linear, Local, Prompt).

    This is the core abstraction that enables ADWs to work with issues
    from multiple sources without tight coupling to any specific provider.
    """

    # Required fields (minimal interface)
    id: str  # Unique identifier (issue number for GitHub, UUID for local)
    title: str
    body: str
    source: IssueSource

    # Optional metadata
    status: IssueStatus = IssueStatus.OPEN
    labels: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Source-specific reference
    source_url: Optional[str] = None  # URL if available (GitHub, Linear)
    source_ref: Optional[str] = None  # Full reference (e.g., "github:123", "local:abc")
    repo_path: Optional[str] = None  # Repository path (owner/repo for GitHub, namespace/project for GitLab)

    # Local issue tracking
    local_path: Optional[str] = None  # Path to local markdown file
    agent_updates: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        populate_by_name = True

    @property
    def number(self) -> str:
        """Alias for id to maintain compatibility with existing code."""
        return self.id

    def to_minimal_dict(self) -> Dict[str, Any]:
        """Return minimal dict for agent operations (backward compatible)."""
        return {"number": self.id, "title": self.title, "body": self.body}

    @classmethod
    def from_github_issue(cls, gh_issue: GitHubIssue) -> "Issue":
        """Create Issue from GitHubIssue for backward compatibility."""
        return cls(
            id=str(gh_issue.number),
            title=gh_issue.title,
            body=gh_issue.body,
            source=IssueSource.GITHUB,
            status=IssueStatus.OPEN if gh_issue.state == "OPEN" else IssueStatus.CLOSED,
            labels=[label.name for label in gh_issue.labels],
            created_at=gh_issue.created_at,
            updated_at=gh_issue.updated_at,
            source_url=gh_issue.url,
            source_ref=f"github:{gh_issue.number}",
        )


class ReviewIssue(BaseModel):
    """Individual review issue found during spec verification."""

    review_issue_number: int
    screenshot_path: str  # Local file path to screenshot (e.g., "agents/ADW-123/reviewer/review_img/error.png")
    screenshot_url: Optional[str] = (
        None  # Public URL after upload (e.g., "https://domain.com/adw/ADW-123/review/error.png")
    )
    issue_description: str
    issue_resolution: str
    issue_severity: Literal["skippable", "tech_debt", "blocker"]


class ReviewResult(BaseModel):
    """Result from reviewing implementation against specification."""

    success: bool
    review_summary: (
        str  # 2-4 sentences describing what was built and whether it matches the spec
    )
    review_issues: List[ReviewIssue] = []
    screenshots: List[str] = (
        []
    )  # Local file paths (e.g., ["agents/ADW-123/reviewer/review_img/ui.png"])
    screenshot_urls: List[str] = (
        []
    )  # Public URLs after upload, indexed-aligned with screenshots


# Content Analysis Types
class AnalysisMetadata(BaseModel):
    """Metadata for content analysis execution."""

    input_source: str  # Original input (URL, file path, or "-")
    content_type: str  # Type of content (youtube, url, pdf, text, stdin)
    patterns_executed: List[str] = Field(default_factory=list)  # Pattern names that were run
    execution_time: float = 0.0  # Total execution time in seconds
    model_used: str = "haiku"  # Model used for pattern execution
    adw_id: str  # ADW ID for this analysis
    timestamp: datetime = Field(default_factory=datetime.now)  # When analysis started
    success: bool = True  # Whether analysis completed successfully
    error_message: Optional[str] = None  # Error message if failed


class PatternResult(BaseModel):
    """Result from executing a single pattern."""

    pattern_name: str  # Name of the pattern executed
    success: bool  # Whether pattern execution succeeded
    output: str = ""  # Pattern output (markdown content)
    error: Optional[str] = None  # Error message if failed
    execution_time: float = 0.0  # Time taken to execute this pattern in seconds
    output_file: Optional[str] = None  # Path to output file if written


class AnalysisReport(BaseModel):
    """Aggregated analysis report from multiple patterns."""

    metadata: AnalysisMetadata
    pattern_results: Dict[str, PatternResult] = Field(default_factory=dict)  # Pattern name -> result
    content_preview: str = ""  # First 500 chars of extracted content
    summary: str = ""  # Executive summary
    full_report: str = ""  # Full aggregated report in markdown


# Brainstorm System Types
class SourceInfo(BaseModel):
    """Source information for analyzed content."""

    type: str  # "youtube", "github", "url", "pdf", "text"
    url: str  # Original URL or file path
    original_title: Optional[str] = None  # Title from source


class VersionInfo(BaseModel):
    """Version information for a single analysis version."""

    version: str  # "v1", "v2", "v3", etc.
    date: datetime  # When this version was created
    preset: Optional[str] = None  # Preset used (e.g., "acidbath")
    patterns_run: List[str] = Field(default_factory=list)  # List of pattern names executed
    model: str = "haiku"  # Model used for analysis
    adw_id: str  # ADW ID that created this version
    diff_from: Optional[str] = None  # Previous version this was diffed from (e.g., "v1")
    changes_summary: Optional[str] = None  # Brief summary of changes from previous version


class AnalysisEntry(BaseModel):
    """Entry for a single analyzed content item in the brainstorm manifest."""

    slug: str  # Kebab-case slug (e.g., "how-to-build-agents")
    title: str  # Human-readable title
    source: SourceInfo  # Source information
    versions: List[VersionInfo] = Field(default_factory=list)  # All versions
    tags: List[str] = Field(default_factory=list)  # Tags for categorization
    blog_status: Optional[str] = None  # "draft", "published", "archived"
    blog_post: Optional[str] = None  # Path to blog post if linked
    latest_version: Optional[str] = None  # "v1", "v2", etc. (cached for quick access)


class BrainstormManifest(BaseModel):
    """Root manifest for brainstorm directory tracking all analyses."""

    version: str = "1.0"  # Manifest schema version
    last_updated: datetime = Field(default_factory=datetime.now)  # Last modification time
    total_analyses: int = 0  # Total number of analyses
    analyses: Dict[str, AnalysisEntry] = Field(default_factory=dict)  # Slug -> AnalysisEntry
