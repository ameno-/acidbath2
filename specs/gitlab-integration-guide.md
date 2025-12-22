# GitLab Integration Guide

This guide explains how to set up and use Jerry ADW with GitLab repositories, issues, and merge requests.

## Overview

Jerry ADW now supports GitLab as a first-class platform provider alongside GitHub. You can use GitLab to:
- Fetch and manage issues from GitLab projects
- Create merge requests (MRs) automatically
- Post comments and status updates to GitLab issues and MRs
- Run complete ADW workflows with GitLab repositories

## Prerequisites

### 1. Install glab CLI

The GitLab integration uses the official `glab` CLI tool (analogous to `gh` for GitHub).

**macOS:**
```bash
brew install glab
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install glab

# Or download from releases
curl -s https://api.github.com/repos/profclems/glab/releases/latest | grep "browser_download_url.*linux" | cut -d '"' -f 4 | wget -qi -
sudo dpkg -i glab_*.deb
```

**Windows:**
```bash
scoop install glab
```

For other installation methods, see: https://gitlab.com/gitlab-org/cli

### 2. Authenticate with GitLab

After installing `glab`, authenticate with your GitLab instance:

```bash
glab auth login
```

This will prompt you to:
1. Choose your GitLab instance (gitlab.com or self-hosted)
2. Select authentication method (browser or token)
3. Complete the authentication flow

Verify authentication:
```bash
glab auth status
```

### 3. (Optional) Set GITLAB_TOKEN Environment Variable

If you prefer to use a personal access token instead of interactive auth:

1. Create a personal access token at https://gitlab.com/-/profile/personal_access_tokens
2. Grant it the following scopes:
   - `api` - Full API access
   - `read_repository` - Read repository data
   - `write_repository` - Write repository data

3. Set the environment variable:

```bash
# Add to ~/.bashrc or ~/.zshrc
export GITLAB_TOKEN="your-gitlab-token-here"
```

## Usage

### Issue Reference Formats

Jerry ADW supports multiple ways to reference GitLab issues:

```bash
# Explicit GitLab prefix (simple format - requires GitLab remote)
/adw_plan_build_iso gitlab:123

# Extended format (cross-platform support)
/adw_plan_build_iso gitlab:ameno13/jerry:1

# Auto-detected (if in GitLab repository)
/adw_plan_build_iso 123

# Using resolve_issue() in code
from adws.adw_modules.issue_providers import resolve_issue

# Simple format (requires GitLab remote)
issue = resolve_issue("gitlab:456")

# Extended format (works from any repo)
issue = resolve_issue("gitlab:ameno13/jerry:1")
```

#### Extended Format: Cross-Platform Issue References

The extended format `gitlab:PROJECT_PATH:ISSUE_NUMBER` allows referencing GitLab issues from any repository, regardless of its hosting platform.

**When to use:**
- Working in a GitHub repository but need to reference a GitLab issue
- Referencing issues from a different GitLab project
- Current repository has no git remote or remote is not GitLab

**Format:**
```bash
gitlab:NAMESPACE/PROJECT:ISSUE_NUMBER
```

**Examples:**
```bash
# Reference GitLab issue from GitHub repo
/adw_plan_build_iso gitlab:ameno13/jerry:1

# Reference issue from different GitLab project
/adw_plan_build_iso gitlab:acme-corp/api-service:456

# In Python code
from adws.adw_modules.issue_providers import resolve_issue

issue = resolve_issue("gitlab:ameno13/jerry:1")
# Fetches issue #1 from gitlab.com/ameno13/jerry
```

**Error handling:**

If you try to use the simple format (`gitlab:123`) from a non-GitLab repository, you'll get a helpful error message:

```
Error: Cannot resolve GitLab issue 'gitlab:1' - current repository
is hosted on github (https://github.com/ameno-/jerry.git).

To reference a GitLab issue from a different project, use the extended format:
  gitlab:PROJECT_PATH:ISSUE_NUMBER

Example:
  gitlab:ameno13/jerry:1
```

### Running ADW Workflows with GitLab

When working in a GitLab repository, Jerry automatically detects the platform and routes operations accordingly:

```bash
# Navigate to your GitLab repository
cd /path/to/gitlab-repo

# Run an ADW workflow with a GitLab issue
/adw_plan_build_iso 123

# The workflow will:
# 1. Fetch issue #123 from GitLab using glab CLI
# 2. Create a feature branch
# 3. Make code changes
# 4. Create a GitLab merge request
# 5. Post status updates as GitLab issue comments
```

### Platform Auto-Detection

Jerry detects the git platform from your remote URL:

```bash
# GitLab.com
git remote add origin git@gitlab.com:namespace/project.git

# Self-hosted GitLab
git remote add origin git@gitlab.example.com:namespace/project.git

# HTTPS
git remote add origin https://gitlab.com/namespace/project.git
```

The system automatically:
- Uses `GitLabIssueProvider` for issue operations
- Uses `GitLabCodeReviewProvider` for merge requests
- Uses `GitLabNotificationProvider` for comments

### Explicit Platform Selection

You can force GitLab mode even with a GitHub remote:

```python
from adws.adw_modules.issue_providers import resolve_issue
from adws.adw_modules.data_types import IssueSource

# Explicit GitLab issue
issue = resolve_issue("gitlab:123", repo_path="namespace/project")

# Or use GitLabIssueProvider directly
from adws.adw_modules.issue_providers import GitLabIssueProvider
provider = GitLabIssueProvider(project_path="namespace/project")
issue = provider.fetch_issue("123")
```

## GitLab-Specific Features

### Merge Request Auto-Close

GitLab MRs support auto-closing issues using keywords in the description:

```markdown
Closes #123
```

Jerry automatically adds this when creating MRs from issues:

```python
from adws.adw_modules.code_review_providers import GitLabCodeReviewProvider

provider = GitLabCodeReviewProvider(project_path="namespace/project")
review, error = provider.create(
    branch_name="feat-123",
    title="Fix validation bug",
    body="Implementation details...",
    issue=issue,  # Automatically adds "Closes #123" to description
)
```

### Merge Methods

GitLab supports three merge methods:

```python
# Squash commits (default)
provider.merge(mr_id, method="squash")

# Regular merge commit
provider.merge(mr_id, method="merge")

# Rebase and merge
provider.merge(mr_id, method="rebase")
```

### Issue Comments (Notes)

GitLab calls comments "notes". Jerry abstracts this:

```python
from adws.adw_modules.gitlab import make_issue_comment

# Post a comment to GitLab issue
make_issue_comment("123", "Status update", cwd="/path/to/repo")
```

## Self-Hosted GitLab

Jerry supports self-hosted GitLab instances:

1. Configure `glab` for your instance:
```bash
glab auth login
# Select "GitLab Self-hosted Instance"
# Enter your GitLab URL: https://gitlab.example.com
```

2. Use as normal - Jerry detects self-hosted instances automatically:
```bash
git remote add origin git@gitlab.example.com:team/project.git
/adw_plan_build_iso 42
```

## Troubleshooting

### glab not found

**Error:**
```
Error: GitLab CLI (glab) is not installed.
```

**Solution:**
Install glab using the instructions in Prerequisites section.

### Authentication Failed

**Error:**
```
Failed to fetch GitLab issue: 401 Unauthorized
```

**Solution:**
1. Re-authenticate with `glab auth login`
2. Or check your `GITLAB_TOKEN` environment variable
3. Verify token has correct scopes (api, read_repository, write_repository)

### Project Path Not Found

**Error:**
```
Failed to determine project path
```

**Solution:**
Ensure you're in a git repository with a GitLab remote:
```bash
git remote -v
# Should show gitlab.com or your GitLab instance
```

Or specify the project path explicitly:
```python
provider = GitLabIssueProvider(project_path="namespace/project")
```

### MR Creation Failed

**Error:**
```
Failed to create MR: target branch not found
```

**Solution:**
Ensure your branch is pushed to GitLab before creating MR:
```bash
git push -u origin your-branch-name
```

## Differences from GitHub

| Feature | GitHub | GitLab |
|---------|--------|--------|
| CLI Tool | `gh` | `glab` |
| Pull Request | PR | MR (Merge Request) |
| Issue Comment | Comment | Note |
| Token Variable | `GITHUB_PAT` | `GITLAB_TOKEN` |
| Repo Format | `owner/repo` | `namespace/project` |
| Auto-close Syntax | `Closes #123` | `Closes #123` (same) |
| CLI Auth | `gh auth login` | `glab auth login` |

## API Reference

### GitLab Module Functions

```python
from adws.adw_modules import gitlab

# Get project path from remote
project_path = gitlab.extract_project_path("git@gitlab.com:ns/proj.git")
# Returns: "ns/proj"

# Fetch issue
issue = gitlab.fetch_issue("123", "namespace/project")

# Post comment
gitlab.make_issue_comment("123", "Update message", cwd="/path/to/repo")

# Mark issue as in progress
gitlab.mark_issue_in_progress("123", cwd="/path/to/repo")
```

### GitLab Providers

```python
from adws.adw_modules.issue_providers import GitLabIssueProvider
from adws.adw_modules.code_review_providers import GitLabCodeReviewProvider
from adws.adw_modules.notification_providers import GitLabNotificationProvider

# Issue provider
issue_provider = GitLabIssueProvider(project_path="namespace/project")
issue = issue_provider.fetch_issue("123")
issue_provider.add_comment(issue, "Status update", agent_id="adw_agent")

# Code review provider
cr_provider = GitLabCodeReviewProvider(project_path="namespace/project")
mr, error = cr_provider.create(
    branch_name="feat-123",
    title="Feature Title",
    body="Description",
    issue=issue,
)

# Notification provider
notif_provider = GitLabNotificationProvider(project_path="namespace/project")
notif_provider.notify(issue, "Workflow completed", agent_id="adw_agent")
```

## Examples

### Complete Workflow Example

```python
from adws.adw_modules.issue_providers import resolve_issue
from adws.adw_modules.code_review_providers import get_code_review_provider
import logging

logger = logging.getLogger(__name__)

# Fetch GitLab issue (auto-detected from repo)
issue = resolve_issue("123")

# Create feature branch
# ... make code changes ...

# Get code review provider (auto-detects GitLab)
cr_provider = get_code_review_provider(issue=issue, logger=logger)

# Create merge request
mr, error = cr_provider.create(
    branch_name="feat-123-fix-bug",
    title=issue.title,
    body=f"Fixes issue #{issue.id}\n\n{issue.description}",
    issue=issue,
)

if mr:
    logger.info(f"Created MR: {mr.url}")
else:
    logger.error(f"Failed to create MR: {error}")
```

### Mixed Platform Scenario

```python
# Fetch issue from GitLab (extended format - works from any repo)
gitlab_issue = resolve_issue("gitlab:ameno13/jerry:1")

# Fetch issue from GitHub
github_issue = resolve_issue("github:456")

# Each issue knows its platform
assert gitlab_issue.source == IssueSource.GITLAB
assert github_issue.source == IssueSource.GITHUB

# Providers route correctly
gitlab_provider = get_provider_for_issue(gitlab_issue)  # Returns GitLabIssueProvider
github_provider = get_provider_for_issue(github_issue)  # Returns GitHubIssueProvider

# Example: Working in a GitHub repo but referencing GitLab issues
# This is useful for tracking issues across multiple projects
from adws.adw_modules.issue_providers import resolve_issue

# Reference a GitLab issue using extended format
external_issue = resolve_issue("gitlab:external-team/service:789")
print(f"External GitLab issue: {external_issue.title}")

# Reference a GitHub issue from current repo
local_issue = resolve_issue("github:123")
print(f"Local GitHub issue: {local_issue.title}")
```

## Next Steps

- Check out the [ADW Workflow Documentation](../README.md) for general workflow usage
- See [Architecture Documentation](../docs/architecture.md) for provider design details
- Review [GitHub Integration Guide](./github-integration-guide.md) for comparison

## Support

For issues or questions:
1. Check GitLab CLI docs: https://gitlab.com/gitlab-org/cli
2. Review Jerry ADW issues: [GitHub Issues](https://github.com/your-org/jerry-adw/issues)
3. Verify `glab` version: `glab version` (recommended: 1.20.0+)
