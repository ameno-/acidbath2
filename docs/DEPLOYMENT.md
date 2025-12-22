# Jerry Deployment Guide

This guide explains how to deploy Jerry to any code repository using the export/import/bootstrap system.

## Table of Contents

1. [Quick Start (5 Minutes)](#quick-start-5-minutes)
2. [Prerequisites](#prerequisites)
3. [Export Jerry](#export-jerry)
4. [Bootstrap Jerry](#bootstrap-jerry)
5. [Validation](#validation)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Topics](#advanced-topics)

## Quick Start (5 Minutes)

```bash
# 1. Export Jerry from existing installation
./adws/jerry_export.py --output /tmp/jerry --format tar.gz

# 2. Bootstrap to new repository
./jerry_bootstrap.sh --source /tmp/jerry/jerry-export-*.tar.gz --target /path/to/new-repo

# 3. Validate installation
cd /path/to/new-repo
./adws/jerry_validate.py --level all

# 4. Test with simple workflow
./adws/adw_prompt.py "echo 'Hello from Jerry!'"
```

Done! Jerry is ready to use in your new repository.

## Prerequisites

Before deploying Jerry, ensure you have:

### Required
- **Python 3.11+**: `python3 --version`
- **uv package manager**: Install from [astral.sh/uv](https://astral.sh/uv)
- **git 2.0+**: `git --version`

### Optional but Recommended
- **Claude Code CLI**: Install from [claude.com/code](https://claude.com/code)
- **GitHub CLI**: For GitHub integrations (`gh`)

### Installing Prerequisites

#### macOS
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install git (usually pre-installed)
brew install git

# Install Claude Code CLI
# Visit https://claude.com/code for instructions
```

#### Linux (Ubuntu/Debian)
```bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install git
sudo apt install git
```

## Export Jerry

Export Jerry from an existing installation to create a portable package.

### Basic Export

```bash
cd /path/to/jerry-installation
./adws/jerry_export.py --output /tmp/jerry-export --format tar.gz
```

### Export Options

```bash
# Specify output directory
./adws/jerry_export.py --output ~/exports/jerry --format tar.gz

# Create zip archive instead of tar.gz
./adws/jerry_export.py --output /tmp/jerry --format zip

# Include example workflows
./adws/jerry_export.py --output /tmp/jerry --include-examples
```

### What Gets Exported

The export package includes:
- ✅ Core ADW scripts (`adws/`)
- ✅ Slash commands (`.claude/commands/`)
- ✅ Specifications (`specs/`)
- ✅ Manifest with checksums (`.jerry/manifest.json`)
- ✅ Configuration templates (`.jerry/templates/`)
- ✅ Documentation (`docs/`, `README.md`)
- ❌ Agent outputs (`agents/`) - excluded
- ❌ Worktrees (`trees/`) - excluded
- ❌ Environment files (`.env`) - excluded for security

### Export Output

After export completes, you'll see:
```
✓ Export completed successfully!

Export Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jerry Version    │ 0.1.0
Archive Format   │ tar.gz
Archive Path     │ /tmp/jerry-export/jerry-export-0.1.0-20250106-143022.tar.gz
Archive Size     │ 2.34 MB
Total Files      │ 147
Report           │ /tmp/jerry-export/export-report-20250106-143022.txt

Next steps:
  1. Bootstrap Jerry: ./jerry_bootstrap.sh --source <archive> --target <target-dir>
  2. Review report: cat /tmp/jerry-export/export-report-20250106-143022.txt
```

## Bootstrap Jerry

Bootstrap installs Jerry into a target repository.

### Basic Bootstrap

```bash
# Bootstrap to current directory
./jerry_bootstrap.sh --source /tmp/jerry-export/jerry-export-*.tar.gz --target .

# Bootstrap to specific directory
./jerry_bootstrap.sh --source jerry-export.tar.gz --target /path/to/my-project
```

### Bootstrap Process

The bootstrap script performs these steps:

1. **Prerequisites Check** - Validates Python, uv, git, Claude CLI
2. **Extract Files** - Extracts Jerry package to target directory
3. **Install Dependencies** - Runs `uv sync` or installs from manifest
4. **Setup Directories** - Creates `agents/`, `trees/`, `specs/` directories
5. **Copy Templates** - Copies `.env.template`, `.gitignore.template`, etc.
6. **Validation** - Runs validation to ensure installation is correct

### Bootstrap Options

```bash
# Skip validation (faster, but not recommended)
./jerry_bootstrap.sh --source jerry.tar.gz --target ./project --skip-validation

# Dry run (see what would happen without executing)
./jerry_bootstrap.sh --source jerry.tar.gz --target ./test --dry-run

# Show help
./jerry_bootstrap.sh --help
```

### Bootstrap Output

```
=========================================
  🚀 Jerry Bootstrap
=========================================

Source: /tmp/jerry-export/jerry-export-0.1.0-20250106-143022.tar.gz
Target: /Users/user/my-project

[INFO] Checking prerequisites...
[SUCCESS] Python 3.11.11 found
[SUCCESS] uv 0.4.0 found
[SUCCESS] git 2.40.0 found
[SUCCESS] Claude Code CLI found: 1.2.0
[SUCCESS] All prerequisites satisfied

[INFO] Extracting Jerry package...
[SUCCESS] Extracted tar.gz archive

[INFO] Installing Python dependencies...
[SUCCESS] Dependencies installed via uv sync

[INFO] Setting up directory structure...
[INFO] Created directory: agents/
[INFO] Created directory: trees/
[SUCCESS] Directory structure ready

[INFO] Copying configuration templates...
[INFO] Created: .env
[INFO] Created: .gitignore
[SUCCESS] Templates processed

[INFO] Running validation...
[SUCCESS] Validation passed!

=========================================
  ✓ Jerry bootstrap completed!
=========================================

Next steps:
  1. cd /Users/user/my-project
  2. Review configuration files (e.g., .env)
  3. Test Jerry: ./adws/adw_prompt.py 'echo hello'

[SUCCESS] Happy coding with Jerry! 🎉
```

## Validation

Validate Jerry installation at three levels.

### Run All Validation Levels

```bash
./adws/jerry_validate.py --level all
```

### Validation Levels

#### Level 1: Import Validation
Tests that all core Python modules can be imported.

```bash
./adws/jerry_validate.py --level 1
```

Checks:
- Manifest exists and is valid JSON
- Core directories present (`adws/`, `.claude/`, `specs/`)
- Required files exist
- Python modules import successfully

#### Level 2: CLI Validation
Tests that ADW scripts are executable and respond to `--help`.

```bash
./adws/jerry_validate.py --level 2
```

Checks:
- ADW scripts are executable
- Scripts respond to `--help` flag
- Claude Code CLI is installed

#### Level 3: Dry-Run Validation
Executes a simple workflow to test end-to-end functionality.

```bash
./adws/jerry_validate.py --level 3
```

Checks:
- `adw_prompt.py` executes successfully
- `agents/` output directory is created
- Workflow completes without errors

### Validation Options

```bash
# Generate JSON report
./adws/jerry_validate.py --level all --report /tmp/validation-report.json

# Quiet mode (only show summary)
./adws/jerry_validate.py --level all --quiet
```

### Validation Output

```
🔍 Jerry Validation

Level 1: Import Validation
✓ Manifest exists: Manifest found
✓ Core directories exist: All core directories present
✓ Required files exist: All required files present
✓ Python module imports: All core modules import successfully

Level 2: CLI Validation
✓ CLI: adws/adw_prompt.py: Script is executable and responds to --help
✓ CLI: adws/adw_slash_command.py: Script is executable and responds to --help
✓ Claude Code CLI: Claude Code CLI is installed

Level 3: Dry-Run Validation
✓ Dry-run: adw_prompt.py: Workflow executed successfully
✓ Agents output directory: agents/ directory exists

Validation Summary:
  Total tests: 9
  Passed: 9
  Failed: 0

✓ All validation tests passed! Jerry is ready to use.
```

## Configuration

After bootstrap, configure Jerry for your environment.

### Edit .env File

```bash
# Copy template to .env
cp .jerry/templates/env.template .env

# Edit with your API key
nano .env
```

Required configuration:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Optional integrations:
```bash
# GitHub
GITHUB_TOKEN=your_token
GITHUB_REPO=owner/repo

# Linear
LINEAR_API_KEY=your_key
LINEAR_TEAM_ID=your_team_id

# Notion
NOTION_API_KEY=your_key
NOTION_DATABASE_ID=your_db_id
```

### Update .gitignore

```bash
# Add Jerry patterns to your .gitignore
cat .jerry/templates/gitignore.template >> .gitignore
```

### Configure Worktrees (Optional)

If using worktree-based workflows:

```bash
# Copy template
cp .jerry/templates/worktree.config.template worktree.config.json

# Edit configuration
nano worktree.config.json
```

## Troubleshooting

### Issue: "Manifest not found"

**Problem**: `.jerry/manifest.json` doesn't exist

**Solution**:
```bash
# Verify you're in Jerry root directory
ls -la .jerry/

# If missing, re-extract archive
tar -xzf jerry-export.tar.gz
```

### Issue: "Python module import failed"

**Problem**: Core modules can't be imported

**Solution**:
```bash
# Check Python version
python3 --version  # Must be 3.11+

# Reinstall dependencies
uv sync

# Try manual import test
cd /path/to/jerry
python3 -c "from adws.adw_modules import agent"
```

### Issue: "Claude Code CLI not found"

**Problem**: `claude` command not in PATH

**Solution**:
```bash
# Check if installed
which claude

# If not found, install from https://claude.com/code
# Or specify custom path in .env
CLAUDE_CODE_CLI=/custom/path/to/claude
```

### Issue: "Permission denied" on scripts

**Problem**: ADW scripts not executable

**Solution**:
```bash
# Make scripts executable
chmod +x adws/*.py
chmod +x jerry_bootstrap.sh

# Verify
ls -l adws/adw_prompt.py
```

### Issue: "Validation fails at Level 3"

**Problem**: Dry-run workflow doesn't complete

**Possible causes**:
1. ANTHROPIC_API_KEY not set in .env
2. Claude Code CLI not installed
3. Network connectivity issues

**Solution**:
```bash
# Check API key
grep ANTHROPIC_API_KEY .env

# Test Claude CLI manually
claude --version

# Run simple workflow manually
./adws/adw_prompt.py "echo test"
```

## Advanced Topics

### Deploying to Multiple Repositories

Use a central export package to deploy Jerry to multiple projects:

```bash
# Export once
./adws/jerry_export.py --output ~/jerry-releases/v0.1.0

# Deploy to multiple projects
for project in project1 project2 project3; do
    ./jerry_bootstrap.sh \
        --source ~/jerry-releases/v0.1.0/jerry-export-*.tar.gz \
        --target ~/$project
done
```

### Upgrading Existing Installation

To upgrade Jerry in an existing repository:

```bash
# 1. Backup current installation
cp -r adws adws.backup
cp -r .claude .claude.backup

# 2. Export new version
cd /path/to/new-jerry
./adws/jerry_export.py --output /tmp/upgrade

# 3. Bootstrap to existing repo (it will update files)
./jerry_bootstrap.sh --source /tmp/upgrade/jerry-*.tar.gz --target /path/to/existing-repo

# 4. Merge custom changes if needed
# 5. Validate
cd /path/to/existing-repo
./adws/jerry_validate.py --level all
```

### Custom Bootstrap Process

For advanced users who need custom bootstrap logic:

```bash
# Extract manually
tar -xzf jerry-export.tar.gz -C /target

# Install specific dependencies
cd /target
uv pip install click rich pyyaml

# Custom setup
# ... your custom logic ...

# Validate
./adws/jerry_validate.py --level all
```

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Deploy Jerry
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Bootstrap Jerry
        run: |
          ./jerry_bootstrap.sh \
            --source jerry-export.tar.gz \
            --target .

      - name: Validate
        run: ./adws/jerry_validate.py --level all
```

## Next Steps

After successfully deploying Jerry:

1. **Read the Architecture Guide**: `docs/ARCHITECTURE.md`
2. **Try Example Workflows**: `./adws/adw_prompt.py "your first prompt"`
3. **Create Your First ADW**: Customize Jerry for your needs
4. **Join the Community**: Share your experience and learnings

---

For more information, see:
- [Architecture Guide](./ARCHITECTURE.md)
- [ADW Documentation](../adws/README.md)
- [Main README](../README.md)
