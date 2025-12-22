# Feature: Implement GitLab Support

## Metadata
adw_id: `3-5ae3a090`
prompt: `{"number": "3", "title": "Implement Gitlab support", "body": "/adw_plan_build_iso\n\nDescription\nIn the legacy directory there is a GitLab ADW integration with supported utilities and functionality.\n\nImport this workflow into Jerry making sure that all related utilities are also included. Sure that GitLab is treated as a new provider. It is a repository that has code. It also has access to issues. It also has access to comments. Merge requests can be commented on. Issues can be commented on. Schemas for comments and some of the nomenclature will be different. In order to integrate this new provider, we must implement a generic service or enhance the existing generic service for providers to support GitLab and all the features that it has access to without conflict. An issue or a code change will only exist with one provider. So GitLab or GitHub will host a set of issues, GitHub and GitLab will host a set of code repositories or what have you. The goal here is to make sure that we can access read issues from GitHub and read issues from GitLab and make the necessary code changes. And also ensure that when those code changes are being pushed, pull requests in Git for GitHub or merge requests for GitLab are being opened we must do it in the correct repository using the correct APIs. \n\nGoals\nAdd Gitlab as a new provider\nConsider core features: ADWs, slash commands, worktree isolation, multi-source issues\nEmphasize scalability, observability, and composability\nView the legacy implementation in legacy/tac-4 in the ADWs \nMake sure that you use the existing ADW workflows for importing a workflow, validating a workflow \nMake sure that documentation is updated after the workflow, the new workflow is integrated \nMake sure that the new workflow is tested and verified after the implementation \n\nNon-goals\nThe webhook implementation that exists inside the legacy/tac-4 repo will not be integrated into the app yet. That will be a separate plan "}`

## Feature Description
This feature adds GitLab as a new platform provider alongside GitHub, enabling the Jerry ADW system to interact with GitLab repositories, issues, merge requests, and comments. The implementation follows the existing provider abstraction pattern established for GitHub, ensuring that workflows can operate on GitLab resources without modification. The feature leverages the `glab` CLI tool (GitLab equivalent of `gh`) to interact with GitLab's API, maintaining consistency with the existing GitHub integration approach.

The core value is enabling multi-platform agentic development where a single ADW workflow can handle issues and code reviews from both GitHub and GitLab, automatically routing operations to the correct platform based on the issue source.

## User Story
As an ADW workflow orchestrator
I want to support GitLab as a first-class provider alongside GitHub
So that I can manage issues, merge requests, and code reviews across both platforms using the same unified interface, enabling agentic workflows to operate seamlessly regardless of the git hosting platform

## Problem Statement
Currently, the Jerry ADW system is tightly coupled to GitHub as the sole git hosting provider. This creates several limitations:
1. Teams using GitLab cannot leverage Jerry's agentic workflows
2. Organizations with mixed GitHub/GitLab infrastructure cannot use a unified workflow
3. The provider abstraction exists but is only implemented for GitHub
4. There is no way to route operations (issue fetching, MR creation, comments) to GitLab repositories
5. Legacy tac-4 directory contains GitLab utilities that need to be imported and integrated

The problem is architectural: while the codebase has provider abstractions (`issue_providers.py`, `code_review_providers.py`, `notification_providers.py`), only GitHub is implemented, and there's no mechanism to detect and route to the correct provider based on repository context.

## Solution Statement
Implement GitLab as a full provider by:
1. Adding GitLab implementations to all three provider modules (`GitLabIssueProvider`, `GitLabCodeReviewProvider`, `GitLabNotificationProvider`)
2. Extending the `IssueSource` enum to include `GITLAB`
3. Creating a `gitlab.py` module parallel to `github.py` for GitLab-specific operations using the `glab` CLI
4. Implementing provider detection logic that determines whether a repository is GitHub or GitLab based on git remote URL
5. Ensuring all factory functions (`resolve_issue`, `get_code_review_provider`, `get_notification_provider`) correctly route to GitLab when appropriate
6. Updating data types to handle GitLab-specific terminology (merge requests vs pull requests, etc.)
7. Importing any existing GitLab utilities from legacy/tac-4 using the existing `adw_import_workflow.py` process

The solution maintains backward compatibility with existing GitHub workflows while adding parallel GitLab support through the provider abstraction layer.

## Relevant Files
Core files that need modification to implement GitLab support:

- **adws/adw_modules/data_types.py** - Extend enums and types for GitLab (IssueSource.GITLAB, CodeReviewPlatform.GITLAB)
- **adws/adw_modules/issue_providers.py** - Add GitLabIssueProvider class implementing IssueProvider protocol
- **adws/adw_modules/code_review_providers.py** - Add GitLabCodeReviewProvider class implementing CodeReviewProvider protocol
- **adws/adw_modules/notification_providers.py** - Add GitLabNotificationProvider class implementing NotificationProvider protocol
- **adws/adw_modules/git_ops.py** - Add functions to detect GitLab remotes and extract GitLab project paths

### New Files

- **adws/adw_modules/gitlab.py** - New module for GitLab-specific operations (mirrors github.py structure)
  - Purpose: Encapsulate glab CLI interactions (fetch issues, create MRs, post comments)
  - Key functions: `fetch_issue`, `make_issue_comment`, `extract_project_path`, `get_gitlab_env`

- **adws/adw_tests/test_gitlab_providers.py** - Unit tests for GitLab provider implementations
  - Purpose: Validate GitLab provider functionality with mocked glab CLI calls

- **specs/gitlab-integration-guide.md** - Documentation for GitLab setup and usage
  - Purpose: Guide users on installing glab CLI, authentication, and using GitLab with Jerry

## Implementation Plan

### Phase 1: Foundation - Data Types and Core Abstractions
Establish the foundational types and detection mechanisms needed for GitLab support. This phase ensures that the type system can represent GitLab entities and that the system can detect when it's working with a GitLab repository.

**Key Deliverables:**
- Extended enums in data_types.py to include GitLab
- Git remote detection logic to identify GitLab repositories
- GitLab-specific data models (if needed beyond existing abstractions)

### Phase 2: Core Implementation - GitLab Module and Providers
Build the core GitLab integration by creating the gitlab.py module and implementing all three provider interfaces. This phase creates the parallel implementation to the existing GitHub providers.

**Key Deliverables:**
- gitlab.py module with glab CLI integration
- GitLabIssueProvider implementation
- GitLabCodeReviewProvider implementation
- GitLabNotificationProvider implementation

### Phase 3: Integration - Factory Functions and Routing
Integrate GitLab providers into the existing factory functions and ensure correct routing based on repository context. This phase makes GitLab providers discoverable and usable by existing workflows.

**Key Deliverables:**
- Updated factory functions to return GitLab providers when appropriate
- Provider auto-detection based on git remote URL
- End-to-end workflow testing with GitLab repositories

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Extend Data Types for GitLab Support
- Add `GITLAB = "gitlab"` to `IssueSource` enum in `adws/adw_modules/data_types.py:14`
- Verify `CodeReviewPlatform.GITLAB` already exists at `adws/adw_modules/data_types.py:232`
- Add GitLab-specific type aliases if needed (e.g., `GitLabMergeRequest` model)
- Create unit tests for new data types to ensure serialization/deserialization works

### 2. Create GitLab Operations Module
- Create `adws/adw_modules/gitlab.py` modeled after `github.py` structure
- Implement `get_gitlab_env()` - return environment dict with GITLAB_TOKEN if set
- Implement `get_repo_url(cwd)` - reuse from git_ops.py or github.py
- Implement `extract_project_path(gitlab_url)` - convert GitLab URL to namespace/project format
- Implement `fetch_issue(issue_number, project_path)` - use glab CLI to fetch issue details as JSON
- Implement `make_issue_comment(issue_id, comment, cwd)` - post comment using glab CLI
- Implement `mark_issue_in_progress(issue_id, cwd)` - add label and assign using glab CLI
- Add `ADW_BOT_IDENTIFIER` constant for comment filtering (same as GitHub)
- Write unit tests mocking glab CLI calls

### 3. Add GitLab Remote Detection to Git Operations
- Add `is_gitlab_remote(url: str) -> bool` function to `adws/adw_modules/git_ops.py`
- Logic: check if URL contains "gitlab.com" or self-hosted GitLab patterns
- Add `detect_git_platform(cwd: Optional[str] = None) -> Literal["github", "gitlab", "unknown"]` function
- Use this function to auto-detect platform in provider factory functions
- Test with various remote URL formats (HTTPS, SSH, self-hosted)

### 4. Implement GitLabIssueProvider
- Create `GitLabIssueProvider` class in `adws/adw_modules/issue_providers.py`
- Implement `__init__(self, project_path: Optional[str] = None)` constructor
- Implement `fetch_issue(self, issue_number: str) -> Issue` using gitlab.fetch_issue()
- Convert GitLab issue JSON to generic `Issue` model (map GitLab fields to Issue fields)
- Implement `update_status(self, issue, status, message, agent_id)` via GitLab comments
- Implement `add_comment(self, issue, comment, agent_id)` using gitlab.make_issue_comment()
- Handle GitLab-specific label system (ensure labels exist before applying)
- Add error handling for glab CLI failures

### 5. Update Issue Resolution Logic for GitLab
- Modify `resolve_issue()` function in `adws/adw_modules/issue_providers.py:411`
- Add support for "gitlab:" prefix (e.g., "gitlab:123")
- Add auto-detection: if git remote is GitLab and issue_ref is numeric, use GitLab provider
- Update docstring with GitLab examples
- Update `get_provider_for_issue()` to return GitLabIssueProvider for IssueSource.GITLAB
- Test with various issue reference formats

### 6. Implement GitLabCodeReviewProvider
- Create `GitLabCodeReviewProvider` class in `adws/adw_modules/code_review_providers.py`
- Follow the same structure as `GitHubCodeReviewProvider`
- Implement `check_exists(self, branch_name, cwd)` - check for existing MRs using glab CLI
- Implement `create(self, branch_name, title, body, issue, base_branch, cwd)` - create MR with glab CLI
- Handle issue auto-close: use "Closes #123" syntax in MR description
- Implement `approve(self, review_id, message, cwd)` - approve MR using glab CLI
- Implement `merge(self, review_id, method, message, cwd)` - merge MR with specified method
- Implement `get_status(self, review_id, cwd)` - fetch MR status from glab CLI
- Map GitLab MR states to `CodeReviewStatus` enum values

### 7. Update Code Review Factory Function
- Modify `get_code_review_provider()` in `adws/adw_modules/code_review_providers.py:491`
- Add `IssueSource.GITLAB -> CodeReviewPlatform.GITLAB` mapping
- Handle case where platform is explicitly set to GITLAB
- Add logic to detect GitLab from git remote if platform is not specified
- Return `GitLabCodeReviewProvider` instance when appropriate
- Test with GitLab repositories

### 8. Implement GitLabNotificationProvider
- Create `GitLabNotificationProvider` class in `adws/adw_modules/notification_providers.py`
- Follow the same structure as `GitHubNotificationProvider`
- Implement `__init__(self, project_path, logger)` constructor
- Implement `notify(self, target, message, agent_id)` - post comment to GitLab issue or MR
- Implement `_get_project_path(self, cwd)` - extract namespace/project from git remote
- Format messages with agent_id prefix for tracking
- Handle glab CLI authentication and errors

### 9. Update Notification Factory Function
- Modify `get_notification_provider()` in `adws/adw_modules/notification_providers.py:211`
- Add case for "gitlab" platform string
- Map `IssueSource.GITLAB` to GitLab notification provider
- Test notification delivery to GitLab issues

### 10. Import Legacy GitLab Utilities (if any exist)
- Check legacy/tac-4 directory for existing GitLab-related code
- Use `uv run adws/adw_import_workflow.py <source> --mode adapt` to import relevant utilities
- Adapt legacy code to match current architecture and provider abstraction
- Validate imports with unit tests

### 11. Create Integration Tests
- Create `adws/adw_tests/test_gitlab_integration.py`
- Test end-to-end workflow: fetch GitLab issue -> create branch -> create MR -> post comment
- Mock glab CLI calls to avoid requiring actual GitLab access during tests
- Test provider auto-detection with GitLab remote URLs
- Test mixed scenarios (GitHub issue with GitLab repo should fail gracefully)

### 12. Update Existing ADW Workflows
- Review `adw_plan_iso.py`, `adw_build_iso.py`, `adw_ship_iso.py` for any GitHub-specific assumptions
- Ensure workflows use provider abstractions rather than direct GitHub calls
- Verify that issue resolution via `resolve_issue()` works with GitLab references
- Test full workflow with a GitLab repository

### 13. Create Documentation
- Create `specs/gitlab-integration-guide.md` with setup instructions
- Document glab CLI installation steps (brew install glab, glab auth login)
- Document environment variable setup (GITLAB_TOKEN)
- Provide examples of using Jerry with GitLab repositories
- Document GitLab-specific issue reference formats ("gitlab:123")
- Add troubleshooting section for common glab CLI issues

### 14. Update README and Main Documentation
- Update main `README.md` to mention GitLab support alongside GitHub
- Add GitLab to the list of supported platforms in architecture documentation
- Update any GitHub-specific examples to show GitLab alternatives
- Document the provider abstraction architecture

## Testing Strategy

### Unit Tests
- **gitlab.py module tests**: Mock glab CLI subprocess calls, verify correct arguments and response parsing
- **GitLabIssueProvider tests**: Test issue fetching, status updates, comments with mocked gitlab.py functions
- **GitLabCodeReviewProvider tests**: Test MR creation, approval, merge with mocked glab CLI
- **GitLabNotificationProvider tests**: Test notification delivery with mocked glab CLI
- **Provider factory tests**: Test correct provider selection based on issue source and git remote detection
- **Data type tests**: Validate GitLab-specific models serialize/deserialize correctly

### Integration Tests
- **End-to-end GitLab workflow**: Use a test GitLab repository to validate full workflow
  - Fetch GitLab issue
  - Create worktree and branch
  - Make code changes
  - Create merge request
  - Post status comments
  - Approve and merge (in test environment only)
- **Mixed platform scenarios**: Test that GitHub workflows are not affected by GitLab additions
- **Provider auto-detection**: Verify correct provider is selected based on git remote URL

### Edge Cases
- **Missing glab CLI**: Graceful error message with installation instructions
- **Invalid GitLab authentication**: Clear error message about GITLAB_TOKEN
- **Self-hosted GitLab**: Verify support for custom GitLab domain URLs
- **GitLab issue not found**: Proper error handling and reporting
- **Merge request conflicts**: Test behavior when MR cannot be auto-merged
- **Rate limiting**: Handle GitLab API rate limits gracefully
- **Invalid project path format**: Test with various GitLab URL formats (SSH, HTTPS, custom domains)
- **Empty or malformed responses**: Test resilience to unexpected glab CLI output
- **Permission errors**: Test scenarios where bot lacks permissions to create MRs or comment

## Acceptance Criteria
- [ ] GitLab is added to `IssueSource` enum and recognized throughout the codebase
- [ ] `gitlab.py` module exists with functions parallel to `github.py` for glab CLI operations
- [ ] `GitLabIssueProvider` implements `IssueProvider` protocol and fetches GitLab issues via glab CLI
- [ ] `GitLabCodeReviewProvider` implements `CodeReviewProvider` protocol and manages merge requests
- [ ] `GitLabNotificationProvider` implements `NotificationProvider` protocol and posts comments
- [ ] `resolve_issue("gitlab:123")` correctly fetches a GitLab issue
- [ ] Provider factory functions auto-detect GitLab from git remote URL and return GitLab providers
- [ ] Full ADW workflow (`adw_plan_build_iso.py`) works with a GitLab repository
- [ ] Merge requests are created successfully with proper issue linking ("Closes #123")
- [ ] Status updates and comments are posted to GitLab issues correctly
- [ ] All unit tests pass with >80% code coverage for new GitLab modules
- [ ] Integration tests validate end-to-end workflow with GitLab
- [ ] Documentation is updated with GitLab setup instructions and examples
- [ ] Existing GitHub workflows continue to function without modification
- [ ] Error handling provides clear guidance when glab CLI is missing or misconfigured

## Validation Commands
Execute these commands to validate the feature is complete:

- `uv run python -m py_compile adws/adw_modules/gitlab.py` - Test that gitlab.py compiles without syntax errors
- `uv run python -m py_compile adws/adw_modules/issue_providers.py` - Verify issue_providers.py compiles with GitLab additions
- `uv run python -m py_compile adws/adw_modules/code_review_providers.py` - Verify code_review_providers.py compiles with GitLab additions
- `uv run python -m py_compile adws/adw_modules/notification_providers.py` - Verify notification_providers.py compiles with GitLab additions
- `uv run python -c "from adws.adw_modules.data_types import IssueSource; assert IssueSource.GITLAB == 'gitlab'"` - Verify GITLAB enum value exists
- `uv run python -c "from adws.adw_modules.gitlab import fetch_issue, make_issue_comment; print('GitLab module imports successfully')"` - Test gitlab module imports
- `uv run python -c "from adws.adw_modules.issue_providers import resolve_issue; print('Issue resolution imports successfully')"` - Verify provider resolution imports
- `uv run python -m pytest adws/adw_tests/test_gitlab_providers.py -v` - Run GitLab provider unit tests (once created)
- `uv run python -m pytest adws/adw_tests/test_gitlab_integration.py -v` - Run GitLab integration tests (once created)
- `glab version` - Verify glab CLI is installed and accessible
- `glab auth status` - Verify glab CLI is authenticated (for manual testing with real GitLab instance)

## Notes

### Dependencies
- **glab CLI**: GitLab's official CLI tool (analogous to gh for GitHub)
  - Installation: `brew install glab` (macOS), see https://gitlab.com/gitlab-org/cli for other platforms
  - Authentication: `glab auth login` or set `GITLAB_TOKEN` environment variable
  - Minimum version: 1.20.0+ recommended

### Environment Variables
- `GITLAB_TOKEN`: Personal access token for GitLab API authentication (optional if using glab auth)
- Should be documented in .env.example if added to project

### Design Considerations
- **Provider Abstraction**: Follow the exact same pattern as GitHub providers to maintain consistency
- **CLI Tool Usage**: Use glab CLI exclusively (like gh for GitHub) rather than direct REST API calls for simplicity
- **Backward Compatibility**: Existing GitHub workflows must continue to work without any changes
- **Error Messages**: Provide helpful error messages pointing users to glab installation/auth setup
- **Self-Hosted GitLab**: Design should support self-hosted GitLab instances via glab CLI configuration

### Future Enhancements (Out of Scope for This Feature)
- GitLab webhook support for automated ADW triggering (mentioned as non-goal in issue)
- GitLab CI/CD pipeline integration
- GitLab-specific features like epics, roadmaps
- Advanced GitLab permissions and approval rules
- GitLab container registry operations

### Testing Notes
- Unit tests should mock subprocess calls to glab CLI to avoid requiring real GitLab access
- Integration tests should use a dedicated test GitLab project or mock server
- Document how to run tests that require real GitLab credentials (should be optional)

### Migration Path for Existing Users
- No migration needed - this is purely additive functionality
- Users with GitHub repositories will see no changes
- Users can start using GitLab repositories by installing glab and authenticating
