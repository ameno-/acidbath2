# Feature: Export, Import, and Bootstrap Jerry

## Metadata
adw_id: `53fe41e6`
prompt: `{"number": "18", "title": "Export, import, bootstrap jerry", "body": "adw_plan_build_iso\nfeature\nmodel: Heavy\n\nJerry needs the ability to export itself, be imported, and bootstrapped. The goal for Jerry is that it can be deployed to any code repository. The current directories include an apps directory which is irrelevant and unused. Must first get rid of those two directories. We must then define clearly workflows or implementations for us to export Jerry in an easy way. Potentially as a Bash script or some way that we can execute in a directory that would set up all the files that are needed. Inside of that directory, install all the necessary packages and dependencies that Jerry needs to run and bootstraps Jerry and verifies that it's ready to run workflows. "}`

## Feature Description
Jerry needs to become a portable, self-contained agentic framework that can be deployed to ANY code repository. This feature will enable Jerry to:
1. **Export** itself as a complete package with all necessary files and dependencies
2. **Import** into new repositories with a simple bootstrap script
3. **Bootstrap** and validate itself to ensure it's ready to run workflows
4. **Clean up** unused application directories (apps/ and legacy apps in apps/)

This makes Jerry truly deployment-ready - teams can add Jerry to their repositories in minutes, not hours.

## User Story
As a **development team lead**
I want to **deploy Jerry to any of our repositories with a single command**
So that **we can scale our development velocity through AI agents without complex setup processes**

## Problem Statement
Currently, Jerry is tightly coupled with application code in the `apps/` directory, making it difficult to deploy Jerry's agentic layer to new repositories. The current structure includes:
- An unused `apps/` directory with minimal placeholder files (main.py, main.ts)
- Legacy application directories inside `apps/` that are irrelevant
- No standardized export/import mechanism
- No bootstrap validation to ensure Jerry is ready to run
- No clear separation between Jerry's core framework and application code

This prevents Jerry from being the portable, deployment-ready framework described in the README.

## Solution Statement
Create a comprehensive export/import/bootstrap system that:

1. **Removes unused application directories** - Clean up `apps/` and legacy app directories
2. **Exports Jerry as a deployable package** - Create a script that bundles Jerry's core files
3. **Provides a bootstrap script** - Single command to install Jerry in any repository
4. **Validates the installation** - Automated checks to ensure Jerry is ready to run
5. **Documents the deployment process** - Clear instructions for deployment and usage

The solution centers around three main scripts:
- `jerry_export.py` - Export Jerry to a distributable package
- `jerry_bootstrap.sh` - Install Jerry in a target repository
- `jerry_validate.py` - Verify Jerry installation and functionality

## Relevant Files

### Existing Files to Modify
- `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/README.md` - Update with export/import/bootstrap documentation
- `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/.gitignore` - Ensure export artifacts are ignored
- `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/adws/adw_modules/workflow_ops.py` - Add export/validation utilities

### Files to Remove
- `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/apps/main.py` - Unused placeholder
- `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/apps/main.ts` - Unused placeholder
- `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/apps/` directory (after cleaning)

### New Files

#### Core Export/Import/Bootstrap Scripts
- `adws/jerry_export.py` - Export Jerry to a distributable package
- `jerry_bootstrap.sh` - Install Jerry in any repository (Bash script)
- `adws/jerry_validate.py` - Validate Jerry installation and readiness

#### Documentation
- `docs/DEPLOYMENT.md` - Comprehensive deployment guide
- `docs/ARCHITECTURE.md` - Jerry's architecture and design principles
- `.jerry/manifest.json` - Jerry's core file manifest and metadata

#### Configuration Templates
- `.jerry/templates/env.template` - Environment variable template
- `.jerry/templates/gitignore.template` - Recommended .gitignore additions
- `.jerry/templates/worktree.config.template` - Worktree configuration template

## Implementation Plan

### Phase 1: Foundation - Cleanup and Preparation
**Goal**: Remove unused directories and establish the foundation for portability

1. **Audit and remove unused apps directory**
   - Verify apps/main.py and apps/main.ts are not referenced anywhere
   - Remove the apps/ directory entirely
   - Update .gitignore to reflect removal

2. **Create Jerry manifest structure**
   - Define `.jerry/` directory for Jerry-specific metadata
   - Create manifest.json with core file lists and dependencies
   - Document the minimal viable Jerry structure

3. **Extract core dependencies**
   - Audit all Python dependencies across adws/ modules
   - Create a consolidated dependency list
   - Document system requirements (Python, uv, Claude Code CLI, Git)

### Phase 2: Core Implementation - Export, Bootstrap, Validate
**Goal**: Implement the three core scripts that enable Jerry portability

1. **Implement jerry_export.py**
   - Scan and collect all Jerry core files (adws/, .claude/, specs/)
   - Create a distributable tarball or zip
   - Include manifest with version info and checksums
   - Generate export report

2. **Implement jerry_bootstrap.sh**
   - Check prerequisites (Python, uv, git, Claude Code CLI)
   - Copy Jerry files to target repository
   - Install dependencies using uv
   - Configure worktree isolation
   - Run initial validation

3. **Implement jerry_validate.py**
   - Level 1: Import validation (can Python modules load?)
   - Level 2: CLI validation (can ADWs be invoked?)
   - Level 3: Dry-run validation (can simple workflow execute?)
   - Generate validation report

### Phase 3: Integration - Documentation and Templates
**Goal**: Integrate the export/import/bootstrap system with Jerry's existing workflows

1. **Create comprehensive documentation**
   - DEPLOYMENT.md with step-by-step instructions
   - ARCHITECTURE.md explaining Jerry's structure
   - Update README.md with deployment section

2. **Create configuration templates**
   - Environment variable template (.env.sample)
   - Gitignore additions template
   - Worktree configuration template

3. **Add export/bootstrap to ADW workflows**
   - Create adw_export.py wrapper for export workflow
   - Create adw_bootstrap.py for bootstrapping existing installations
   - Add validation checks to existing ADWs

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Verify and Remove Unused Apps Directory
- Run `grep -r "apps/" adws/ .claude/` to find references to apps/
- Run `grep -r "main.py\|main.ts" adws/ .claude/` to verify no usage
- Delete `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/apps/` directory
- Update `.gitignore` to remove apps/ references if present
- Commit the cleanup: "chore: remove unused apps directory"

### 2. Create Jerry Manifest Structure
- Create `.jerry/` directory in project root
- Create `.jerry/manifest.json` with:
  - Jerry version
  - Core directories (adws/, .claude/, specs/)
  - Required dependencies
  - Python version requirement
  - Checksum for integrity verification
- Create `.jerry/templates/` directory for configuration templates
- Document the manifest schema in `.jerry/README.md`

### 3. Implement jerry_export.py Script
- Create `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/adws/jerry_export.py`
- Use uv script format with dependencies (click, rich, pyyaml)
- Implement functions:
  - `collect_core_files()` - Gather Jerry's core files
  - `generate_manifest()` - Create export manifest
  - `create_package()` - Bundle into tarball/zip
  - `validate_export()` - Verify export integrity
- Add CLI options:
  - `--output` - Output directory/filename
  - `--format` - zip or tar.gz
  - `--include-examples` - Include example workflows
- Generate export report with file counts and sizes

### 4. Implement jerry_bootstrap.sh Bash Script
- Create `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/jerry_bootstrap.sh`
- Implement bootstrap phases:
  - **Phase 1: Prerequisites Check**
    - Check for Python 3.11+, uv, git, claude CLI
    - Exit with clear error messages if missing
  - **Phase 2: Extract and Copy Files**
    - Extract Jerry package if provided
    - Copy files to target directory
    - Preserve file permissions and structure
  - **Phase 3: Install Dependencies**
    - Run `uv sync` or install dependencies
    - Create virtual environment if needed
  - **Phase 4: Configure Jerry**
    - Copy template files (.env.sample, worktree.config)
    - Initialize specs/, agents/, trees/ directories
    - Set up worktree isolation
  - **Phase 5: Validate Installation**
    - Run jerry_validate.py
    - Report validation results
- Add CLI options:
  - `--source` - Path to Jerry export package
  - `--target` - Target repository directory
  - `--skip-validation` - Skip validation phase
  - `--dry-run` - Show what would be done without executing

### 5. Implement jerry_validate.py Script
- Create `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/adws/jerry_validate.py`
- Use uv script format with dependencies (click, rich)
- Implement validation levels:
  - **Level 1: Import Validation**
    - Test: `from adws.adw_modules import *`
    - Verify all core modules can be imported
  - **Level 2: CLI Validation**
    - Test: `./adws/adw_prompt.py --help`
    - Verify ADW scripts are executable
    - Check `gh --version` (optional warning if missing)
    - Check `glab --version` (optional warning if missing)
    - Check `claude --version`
  - **Level 3: Workflow Validation** (CRITICAL for JARI)
    - Test: Execute `adw_prompt.py` with simple command
    - Test: Execute `adw_slash_command.py /chore "test"`
    - Test: Worktree isolation dry-run (`adw_plan_iso.py --dry-run`)
    - Verify slash commands and worktree creation work
  - **Level 4: Full SDLC Validation**
    - Test: Execute `adw_plan_iso.py` with test prompt
    - Test: Execute `adw_build_iso.py` after plan
    - Test: Execute `adw_chore_implement.py`
    - Verify trees/ and agents/ directories created
    - Cleanup test worktrees after validation
  - **Level 5: Auth Validation** (Optional)
    - Test: `gh auth status` with GITHUB_PAT if set
    - Test: `glab auth status` with GITLAB_TOKEN if set
    - Skip if tokens not configured
- Generate validation report:
  - JSON format for programmatic consumption
  - Human-readable summary
  - Specific error messages for failures
- Add CLI options:
  - `--level` - Maximum validation level (1, 2, 3, 4, 5, or all)
  - `--report` - Output report to file
  - `--quiet` - Minimal output

### 6. Create Configuration Templates
- Create `.jerry/templates/env.template`:
  - API keys (ANTHROPIC_API_KEY)
  - Optional integrations (GitHub, Linear, Notion)
  - Worktree configuration variables
- Create `.jerry/templates/gitignore.template`:
  - agents/ output directory
  - trees/ worktree directory
  - .env files
  - Python cache directories
- Create `.jerry/templates/worktree.config.template`:
  - Base branch configuration
  - Port allocation ranges
  - Cleanup policies

### 7. Write Comprehensive Documentation
- Create `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/docs/DEPLOYMENT.md`:
  - Prerequisites section
  - Quick start (5-minute deployment)
  - Step-by-step deployment guide
  - Troubleshooting common issues
  - Examples for different scenarios
- Create `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/docs/ARCHITECTURE.md`:
  - Jerry's layer separation (agentic vs application)
  - Directory structure and purposes
  - Core concepts (ADWs, slash commands, agents)
  - Extension points and customization
- Update `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/README.md`:
  - Add "Deploying Jerry" section
  - Link to DEPLOYMENT.md
  - Update Quick Start to reference bootstrap
  - Add export/import/bootstrap to feature list

### 8. Add Export Utilities to workflow_ops.py
- Edit `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/adws/adw_modules/workflow_ops.py`
- Add functions:
  - `collect_jerry_core_files()` - Get list of core Jerry files
  - `validate_jerry_installation()` - Run validation checks
  - `get_jerry_version()` - Extract version from manifest
  - `verify_prerequisites()` - Check system dependencies
- Document functions with docstrings

### 9. Create ADW Wrappers for Export/Bootstrap
- Create `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/adws/adw_export.py`:
  - Wrapper around jerry_export.py
  - Uses AgentTemplateRequest for consistency
  - Includes state tracking via ADWState
- Create `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/adws/adw_bootstrap.py`:
  - Orchestrates bootstrap process
  - Provides agent-based feedback
  - Logs progress to agents/ directory

### 10. Update .gitignore
- Edit `/Users/ameno/dev/tac/tac-8/trees/53fe41e6/.gitignore`
- Add export artifacts:
  - jerry-export-*.tar.gz
  - jerry-export-*.zip
  - .jerry/exports/
- Ensure existing patterns cover:
  - agents/
  - trees/
  - .env files

### 11. Create End-to-End Tests
- Create test script `adws/adw_modules/test_export_bootstrap.py`
- Test scenarios:
  - **Test 1**: Export creates valid package
  - **Test 2**: Bootstrap succeeds in clean directory
  - **Test 3**: Validation catches missing dependencies
  - **Test 4**: Bootstrap is idempotent (can run multiple times)
  - **Test 5**: Exported Jerry can execute basic workflows
- Use pytest or unittest framework
- Add to validation workflow

### 12. Create Example Usage Scripts
- Create `examples/deploy_to_new_repo.sh`:
  - Complete example of deploying Jerry to a new repository
  - Includes all steps with explanations
- Create `examples/update_existing_jerry.sh`:
  - Example of updating an existing Jerry installation
  - Handles version migration
- Add examples to docs/DEPLOYMENT.md

## Testing Strategy

### Unit Tests
1. **Manifest Generation**
   - Test: `generate_manifest()` creates valid JSON
   - Verify: All required fields present
   - Verify: Checksums match file contents

2. **File Collection**
   - Test: `collect_core_files()` finds all Jerry files
   - Verify: No application files included
   - Verify: All critical files present (adws/, .claude/, etc.)

3. **Prerequisites Check**
   - Test: `verify_prerequisites()` detects missing tools
   - Mock: System without Python, uv, git, claude
   - Verify: Clear error messages returned

4. **Validation Levels**
   - Test: Each validation level independently
   - Mock: Various failure scenarios
   - Verify: Proper error reporting and recovery

### Integration Tests
1. **Full Export/Bootstrap Cycle**
   - Export Jerry from current location
   - Bootstrap to temporary directory
   - Run validation
   - Execute sample workflow
   - Verify: All steps succeed

2. **Bootstrap in Existing Repository**
   - Create mock repository with existing code
   - Bootstrap Jerry
   - Verify: Existing files untouched
   - Verify: Jerry directories created correctly

3. **Validation Failure Scenarios**
   - Bootstrap with missing dependencies
   - Bootstrap with incorrect Python version
   - Bootstrap without Claude Code CLI
   - Verify: Clear error messages and recovery suggestions

### Edge Cases
1. **Bootstrap Over Existing Jerry Installation**
   - Should detect existing installation
   - Should offer to upgrade/replace
   - Should preserve user customizations

2. **Export from Modified Jerry**
   - Jerry with custom ADWs added
   - Should include custom content
   - Should note modifications in manifest

3. **Cross-Platform Compatibility**
   - Export on macOS, bootstrap on Linux
   - Verify: Path separators handled correctly
   - Verify: Line endings preserved

4. **Partial Installation Recovery**
   - Bootstrap interrupted mid-process
   - Should be resumable
   - Should clean up partial state

5. **Permission Issues**
   - Bootstrap to directory without write access
   - Should fail gracefully with clear error
   - Should not leave partial installation

## Acceptance Criteria

1. ✅ **Unused apps directory is removed**
   - `apps/` directory no longer exists
   - No references to `apps/` in codebase
   - Clean commit documenting removal

2. ✅ **Jerry can be exported**
   - `jerry_export.py` creates valid package
   - Package includes all core files (adws/, .claude/, specs/)
   - Manifest contains version, checksums, dependencies
   - Export report shows file counts and sizes

3. ✅ **Jerry can be bootstrapped**
   - `jerry_bootstrap.sh` succeeds in clean directory
   - All dependencies installed via uv
   - Directory structure created (specs/, agents/, trees/)
   - Configuration templates copied

4. ✅ **Installation can be validated**
   - `jerry_validate.py` runs all 3 validation levels
   - Level 1: Import validation passes
   - Level 2: CLI validation passes
   - Level 3: Dry-run validation passes
   - Validation report generated

5. ✅ **Bootstrapped Jerry is functional**
   - Can execute `./adws/adw_prompt.py "test"`
   - Can execute `./adws/adw_slash_command.py /chore "test"`
   - Agents output directory created and populated
   - Workflows complete successfully

6. ✅ **Documentation is comprehensive**
   - DEPLOYMENT.md covers full deployment process
   - ARCHITECTURE.md explains Jerry's structure
   - README.md updated with deployment section
   - Examples provided for common scenarios

7. ✅ **Bootstrap is idempotent**
   - Running bootstrap twice doesn't break installation
   - Existing configurations preserved
   - Safe upgrade path documented

8. ✅ **Prerequisites are validated**
   - Bootstrap checks for Python 3.11+
   - Bootstrap checks for uv package manager
   - Bootstrap checks for git
   - Bootstrap checks for Claude Code CLI
   - Clear error messages for missing prerequisites

9. ✅ **Worktree isolation is validated (CRITICAL for JARI)**
   - jerry_validate.py Level 3 tests worktree creation
   - Parallel execution works in isolated trees/
   - `adw_plan_iso.py --dry-run` succeeds

10. ✅ **Full SDLC workflows are validated**
    - Plan → Build workflow chain works
    - Chore + Implement composite works
    - agents/ and trees/ directories created correctly
    - Test worktrees cleaned up after validation

11. ✅ **GitHub/GitLab access is validated**
    - gh CLI check shows warning if not installed (does not fail)
    - glab CLI check shows warning if not installed (does not fail)
    - Token auth validated if GITHUB_PAT/GITLAB_TOKEN set

## Validation Commands
Execute these commands to validate the feature is complete:

### 1. Verify Apps Directory Removed
```bash
ls /Users/ameno/dev/tac/tac-8/trees/53fe41e6/apps 2>&1 | grep -q "No such file" && echo "✅ apps/ removed" || echo "❌ apps/ still exists"
```

### 2. Test Export Script
```bash
cd /Users/ameno/dev/tac/tac-8/trees/53fe41e6
./adws/jerry_export.py --output /tmp/jerry-export --format tar.gz
test -f /tmp/jerry-export/jerry-*.tar.gz && echo "✅ Export created" || echo "❌ Export failed"
```

### 3. Test Bootstrap Script
```bash
cd /tmp
mkdir jerry-test
./jerry_bootstrap.sh --source /tmp/jerry-export/jerry-*.tar.gz --target jerry-test
cd jerry-test && test -d adws && test -d .claude && echo "✅ Bootstrap succeeded" || echo "❌ Bootstrap failed"
```

### 4. Test Validation Script
```bash
cd /tmp/jerry-test
./adws/jerry_validate.py --level all
test $? -eq 0 && echo "✅ Validation passed" || echo "❌ Validation failed"
```

### 5. Test Functional Workflow
```bash
cd /tmp/jerry-test
./adws/adw_prompt.py "Create a hello.py file that prints 'Hello from Jerry!'"
test -f hello.py && grep -q "Hello from Jerry!" hello.py && echo "✅ Workflow functional" || echo "❌ Workflow failed"
```

### 6. Verify Documentation
```bash
cd /Users/ameno/dev/tac/tac-8/trees/53fe41e6
test -f docs/DEPLOYMENT.md && test -f docs/ARCHITECTURE.md && echo "✅ Documentation complete" || echo "❌ Documentation missing"
```

### 7. Test Python Module Compilation
```bash
cd /Users/ameno/dev/tac/tac-8/trees/53fe41e6
uv run python -m py_compile adws/jerry_export.py adws/jerry_validate.py adws/adw_modules/workflow_ops.py
test $? -eq 0 && echo "✅ Code compiles" || echo "❌ Compilation errors"
```

### 8. Test Import Validation
```bash
cd /Users/ameno/dev/tac/tac-8/trees/53fe41e6
uv run python -c "from adws.adw_modules import workflow_ops, agent, state; print('✅ Imports successful')"
```

### 9. Verify Manifest Structure
```bash
cd /Users/ameno/dev/tac/tac-8/trees/53fe41e6
test -f .jerry/manifest.json && cat .jerry/manifest.json | python -m json.tool > /dev/null && echo "✅ Manifest valid" || echo "❌ Manifest invalid"
```

### 10. Full Integration Test
```bash
cd /Users/ameno/dev/tac/tac-8/trees/53fe41e6
# Export
./adws/jerry_export.py --output /tmp/jerry-integration-test --format tar.gz

# Bootstrap to new location
cd /tmp && rm -rf jerry-integration && mkdir jerry-integration
cd jerry-integration
/Users/ameno/dev/tac/tac-8/trees/53fe41e6/jerry_bootstrap.sh --source /tmp/jerry-integration-test/jerry-*.tar.gz --target .

# Validate
./adws/jerry_validate.py --level all --report /tmp/validation-report.json

# Test workflow
./adws/adw_prompt.py "print('Integration test successful')"

# Verify
test $? -eq 0 && echo "✅ Full integration test passed" || echo "❌ Integration test failed"
```

### 11. Test Level 3 Workflow Validation
```bash
cd /tmp/jerry-test
./adws/jerry_validate.py --level 3
test $? -eq 0 && echo "✅ Workflow validation passed" || echo "❌ Workflow validation failed"
```

### 12. Test Level 4 SDLC Validation
```bash
cd /tmp/jerry-test
./adws/jerry_validate.py --level 4
test -d trees && test -d agents && echo "✅ SDLC validation passed" || echo "❌ SDLC validation failed"
```

### 13. Test Level 5 Auth Validation (if tokens set)
```bash
cd /tmp/jerry-test
export GITHUB_PAT="your-token"
./adws/jerry_validate.py --level 5
test $? -eq 0 && echo "✅ Auth validation passed" || echo "❌ Auth validation failed"
```

## Post-Merge Fixes

### Fix 1: Make ANTHROPIC_API_KEY Optional (Subscription Auth Support)
**Date**: 2025-12-07
**Files Modified**:
- `adws/adw_modules/utils.py` - `check_env_vars()` no longer requires API key; detects auth mode
- `.env.sample` - Updated documentation to explain both auth options

**Problem**: ADW workflows required `ANTHROPIC_API_KEY` even for users with Claude Code Max subscriptions. When API key was set, it was passed to Claude Code CLI which preferred API key auth over subscription auth, causing:
- API rate limits to be hit instead of using subscription quota
- Unnecessary API charges for subscription users

**Solution**:
- Made `ANTHROPIC_API_KEY` optional in `check_env_vars()`
- Added auth mode detection with informative messages:
  - `✓ Using Claude Code subscription authentication` (no API key)
  - `⚠️ Note: ANTHROPIC_API_KEY is set - using API key authentication (has rate limits)` (with API key)

### Fix 2: Exclude settings.local.json from Export
**Date**: 2025-12-07
**Files Modified**:
- `adws/jerry_export.py` - Added exclusion for `settings.local.json`

**Problem**: `settings.local.json` contains machine-specific paths and MCP configurations that should not be exported to other machines.

**Solution**: Added filter in `collect_core_files()` to skip `settings.local.json` during export.

## Notes

### Dependencies
All scripts will use `uv run` for dependency management. Core dependencies include:
- `click` - CLI framework
- `rich` - Beautiful terminal output
- `pyyaml` - Configuration parsing
- `pydantic` - Data validation

Add dependencies using:
```bash
uv add click rich pyyaml pydantic
```

### Deployment Modes
Support three deployment modes:
1. **Minimal**: Core Jerry only (adws/, .claude/commands/)
2. **Standard**: Core + examples + documentation
3. **Full**: Everything including tests and development tools

### Version Management
- Manifest includes Jerry version number
- Bootstrap checks version compatibility
- Upgrade path documented for version migrations
- Semantic versioning (MAJOR.MINOR.PATCH)

### Security Considerations
- Export includes checksums for integrity verification
- Bootstrap validates checksums before installation
- .env template includes warnings about API key security
- Documentation covers secure credential management

### Future Enhancements
- **Package Registry**: Publish Jerry to package registry (PyPI, npm, etc.)
- **Homebrew Formula**: Create brew formula for easy installation
- **Docker Image**: Containerized Jerry for isolated execution
- **Version Manager**: Tool to manage multiple Jerry versions (like nvm, rbenv)
- **Plugin System**: Extensible architecture for third-party ADWs
- **Cloud Bootstrap**: Deploy Jerry to cloud environments (AWS, GCP, Azure)

### Related Issues
- Issue #18 (this feature)
- Consider creating follow-up issues for:
  - Package registry publication
  - Docker containerization
  - Plugin system architecture
  - Cloud deployment automation

### Migration Notes
For existing Jerry installations:
1. Backup current installation
2. Export using new export script
3. Bootstrap to clean directory
4. Migrate custom ADWs and configurations
5. Validate new installation
6. Switch to new installation

Provide migration guide in DEPLOYMENT.md with specific steps and rollback procedures.
