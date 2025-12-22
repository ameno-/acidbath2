# Jerry Bootstrap Guide

This document describes how to export, import, and bootstrap Jerry into new or existing projects. It is included in all Jerry exports and serves as the primary specification for cloud instance deployments.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Parallel Phases](#parallel-phases)
- [Resumable State Tracking](#resumable-state-tracking)
- [Level 4 Validation Required](#level-4-validation-required)
- [Export Process](#export-process)
- [Bootstrap Process](#bootstrap-process)
- [Validation Levels](#validation-levels)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Cloud Deployment](#cloud-deployment)

---

## Overview

Jerry bootstrap is a comprehensive process that installs the Jerry framework into your project. The process is designed to be:

- **Fast**: 5 parallel phases reduce installation time by 40-50%
- **Resumable**: State tracking allows pausing and resuming at any step
- **Validated**: Level 4 (Full SDLC) validation ensures everything works
- **Claude-Assisted**: Use `/bootstrap` for guided installation

---

## Prerequisites

Before bootstrapping Jerry, ensure you have:

| Tool | Version | Check Command | Install |
|------|---------|---------------|---------|
| Python | 3.11+ | `python3 --version` | [python.org](https://python.org) |
| uv | latest | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Git | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com) |
| Claude Code | latest | `claude --version` | [claude.com/code](https://claude.com/code) |

**Required Environment Variables:**
```bash
export ANTHROPIC_API_KEY="your-api-key"  # Required
export GITHUB_PAT="your-token"           # Optional - for GitHub integration
```

---

## Quick Start

### Option 1: Claude-Assisted (Recommended)

From the Jerry source repository:
```bash
claude /bootstrap ~/dev/my-project
```

Claude will guide you through all steps with state tracking.

### Option 2: Manual Bootstrap

```bash
# 1. Export Jerry
./adws/jerry_export.py --output /tmp/jerry-export

# 2. Bootstrap into target
./jerry_bootstrap.sh --source /tmp/jerry-export/jerry-export-*.tar.gz --target ~/dev/my-project

# 3. Configure environment
cd ~/dev/my-project
cp .jerry/templates/env.template .env
# Edit .env with your ANTHROPIC_API_KEY

# 4. Validate (Level 4 required)
./adws/jerry_validate.py --level 4
```

---

## Parallel Phases

Jerry bootstrap executes in **5 parallel phases** for maximum efficiency:

```
Phase 1: PREREQS (parallel)
├── Check Python 3.11+
├── Check uv
├── Check git
└── Check claude CLI
    [ALL must pass to continue]

Phase 2: SETUP (parallel after Phase 1)
├── Export Jerry → jerry_export.py
└── Verify/create target directory
    [BOTH must complete to continue]

Phase 3: INSTALL (pipeline + parallel)
├── Extract archive to target
├── Install Python dependencies (after extract)
├── Create directories (agents/, trees/, specs/, ai_docs/)
└── Copy configuration templates
    [Wait for deps install to continue]

Phase 4: CONFIGURE (sequential - user input required)
└── Help user set up .env
    [May pause here - state is saved]

Phase 5: VALIDATE (tiered parallelism)
├── Level 1 + Level 2 (parallel - no deps)
├── Level 3 (depends on L1+L2 passing)
├── Level 4 (depends on L3 passing) ← REQUIRED
└── Smoke test (after L4)
    [ALL must pass for complete]
```

### Efficiency Gains

| Approach | Time | Notes |
|----------|------|-------|
| Sequential (14 steps) | ~8-10 min | Original approach |
| Parallel phases | ~4-6 min | **40-50% faster** |

---

## Resumable State Tracking

Bootstrap progress is tracked in `<target>/.jerry/import_state.json`. If the process is interrupted (e.g., to configure external services), it can be resumed.

### State File Location

```
<target-repo>/
└── .jerry/
    └── import_state.json
```

### State File Structure

```json
{
  "import_id": "abc12345",
  "started_at": "2025-12-07T10:30:00Z",
  "source_repo": "/path/to/jerry",
  "target_repo": "/path/to/my-project",
  "export_archive": "/tmp/jerry-export/jerry-export-0.1.0-20251207.tar.gz",
  "current_phase": "configure",
  "phases": {
    "prereqs": {
      "status": "completed",
      "completed_at": "2025-12-07T10:30:15Z",
      "checks": {
        "python": "completed",
        "uv": "completed",
        "git": "completed",
        "claude": "completed"
      }
    },
    "setup": {
      "status": "completed",
      "completed_at": "2025-12-07T10:31:00Z",
      "tasks": {
        "export": "completed",
        "target_verify": "completed"
      }
    },
    "install": {
      "status": "completed",
      "completed_at": "2025-12-07T10:32:00Z",
      "tasks": {
        "extract": "completed",
        "deps": "completed",
        "dirs": "completed",
        "templates": "completed"
      }
    },
    "configure": {
      "status": "in_progress",
      "started_at": "2025-12-07T10:32:05Z",
      "notes": "Waiting for user to set ANTHROPIC_API_KEY"
    },
    "validate": {
      "status": "pending"
    }
  },
  "last_updated": "2025-12-07T10:35:00Z"
}
```

### Status Values

| Status | Description |
|--------|-------------|
| `pending` | Not started |
| `in_progress` | Currently running |
| `completed` | Successfully finished |
| `failed` | Failed with error (includes error message) |
| `skipped` | User chose to skip |

### Resuming an Interrupted Import

```bash
# Check current state
cat ~/dev/my-project/.jerry/import_state.json | python3 -m json.tool

# Resume with Claude
claude /bootstrap ~/dev/my-project --resume

# Or manually continue from where you left off
cd ~/dev/my-project
source .env
./adws/jerry_validate.py --level 4
```

---

## Level 4 Validation Required

**Level 4 (Full SDLC) validation is MANDATORY** for all Jerry installations. This ensures the framework is fully functional.

### Why Level 4 is Required

Level 4 validation tests the core Jerry workflows:
- **Plan workflow** (`adw_plan_iso.py`) creates isolated worktrees
- **Build workflow** (`adw_build_iso.py`) implements in worktrees
- **Worktree isolation** confirms parallel execution capability
- **Cleanup** verifies worktrees are properly removed

### What Level 4 Tests

1. Creates a test worktree in `trees/`
2. Runs `adw_plan_iso.py` with a test prompt
3. Verifies agent outputs in `agents/`
4. Runs `adw_build_iso.py` to test implementation
5. Cleans up test artifacts

### Expected Duration

Level 4 validation takes approximately **5 minutes** to complete.

### Running Level 4 Validation

```bash
cd ~/dev/my-project
./adws/jerry_validate.py --level 4
```

---

## Export Process

The export process creates a distributable Jerry package.

### Running Export

```bash
./adws/jerry_export.py --output /tmp/jerry-export --format tar.gz
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output, -o` | `/tmp/jerry-export` | Output directory |
| `--format, -f` | `tar.gz` | Archive format (`tar.gz` or `zip`) |
| `--include-examples` | false | Include example workflows |

### What Gets Exported

| Directory | Contents |
|-----------|----------|
| `adws/` | AI Developer Workflows and modules |
| `.claude/` | Commands and configuration |
| `specs/` | Specification files |
| `.jerry/` | Manifest and templates |
| `docs/` | Documentation (including this file) |

### Export Output

```
/tmp/jerry-export/
├── jerry-export-0.1.0-20251207-103000.tar.gz
└── export-report-20251207-103000.txt
```

The export report contains:
- File counts by category
- Python version used
- Archive size
- System requirements
- SHA256 checksums for integrity verification

---

## Bootstrap Process

The bootstrap script installs Jerry into your target project.

### Running Bootstrap

```bash
./jerry_bootstrap.sh --source <archive> --target <directory>
```

### Options

| Option | Description |
|--------|-------------|
| `--source PATH` | Path to Jerry export archive (required) |
| `--target PATH` | Target directory for installation (required) |
| `--skip-validation` | Skip validation phase |
| `--dry-run` | Show what would be done |

### Bootstrap Phases

1. **Check Prerequisites** - Validates Python, uv, git, claude
2. **Extract Archive** - Unpacks files to target
3. **Install Dependencies** - Runs `uv sync` or `uv pip install`
4. **Create Directories** - Creates `agents/`, `trees/`, `specs/`, `ai_docs/`
5. **Copy Templates** - Copies configuration templates
6. **Run Validation** - Executes `jerry_validate.py --level all`

---

## Validation Levels

Jerry validation runs at 5 levels:

| Level | Name | Time | What It Checks |
|-------|------|------|----------------|
| 1 | Import | ~5s | Manifest, directories, Python imports |
| 2 | CLI | ~30s | Scripts executable, Claude CLI available |
| 3 | Workflow | ~2min | Basic ADW execution, slash commands |
| 4 | Full SDLC | ~5min | Plan/build workflows, worktree isolation |
| 5 | Auth | ~10s | GitHub/GitLab token validation |

### Running Validation

```bash
# Quick check
./adws/jerry_validate.py --level 2

# Full validation (required for new installations)
./adws/jerry_validate.py --level 4

# All levels with report
./adws/jerry_validate.py --level all --report validation-report.json
```

---

## Configuration

### Environment Variables

Copy the template and set your values:

```bash
cp .jerry/templates/env.template .env
```

**Required:**
```bash
ANTHROPIC_API_KEY=your-api-key
```

**Optional:**
```bash
GITHUB_PAT=your-github-token
GITLAB_TOKEN=your-gitlab-token
GITHUB_REPO=owner/repo
```

### Worktree Configuration

Review `.jerry/templates/worktree.config.template` for:
- `base_port`: Starting port for isolated worktrees (default: 8000)
- `cleanup_policy`: When to cleanup worktrees
- `parallel_limit`: Max concurrent worktrees

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Python version too old` | Install Python 3.11+ |
| `uv not found` | Run `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `claude not found` | Install Claude Code CLI from [claude.com/code](https://claude.com/code) |
| `Permission denied` | Ensure scripts are executable: `chmod +x adws/*.py` |
| `Port in use` | Check `.ports.env` and kill conflicting processes |
| `Validation failed` | Check `validation-report.json` for details |

### Checking Import State

```bash
cat .jerry/import_state.json | python3 -m json.tool
```

### Restarting from Scratch

```bash
# Remove state file to start fresh
rm .jerry/import_state.json

# Re-run bootstrap
claude /bootstrap ~/dev/my-project
```

---

## Cloud Deployment

### Fresh Instance Setup

```bash
# 1. Install prerequisites
sudo apt update && sudo apt install -y python3.11 python3.11-venv git

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 3. Install Claude Code CLI
npm install -g @anthropic-ai/claude-code
# Or follow: https://claude.com/code

# 4. Set environment variables
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc

# 5. Clone Jerry or transfer export archive
git clone https://github.com/yourorg/jerry ~/jerry
# Or: scp jerry-export-*.tar.gz user@instance:~/

# 6. Bootstrap into project
cd ~/jerry
./jerry_bootstrap.sh --source /tmp/jerry-export/*.tar.gz --target ~/my-project

# 7. Validate
cd ~/my-project
./adws/jerry_validate.py --level 4
```

### Post-Bootstrap Checklist

- [ ] `.env` configured with `ANTHROPIC_API_KEY`
- [ ] Level 4 validation passes
- [ ] Smoke test succeeds: `./adws/adw_prompt.py "test"`
- [ ] Git initialized if not already

---

## Key Scripts Reference

| Script | Purpose |
|--------|---------|
| `adws/jerry_export.py` | Create distributable Jerry package |
| `jerry_bootstrap.sh` | Install Jerry into target project |
| `adws/jerry_validate.py` | Validate Jerry installation |
| `adws/adw_prompt.py` | Execute ad-hoc Claude prompts |
| `adws/adw_slash_command.py` | Execute slash command templates |
| `adws/adw_plan_iso.py` | Planning in isolated worktrees |
| `adws/adw_build_iso.py` | Building in isolated worktrees |

---

## Next Steps

After successful bootstrap:

1. **Prime the agent**: `./adws/adw_slash_command.py /prime`
2. **Create your first spec**: `./adws/adw_slash_command.py /chore "Your task"`
3. **Run isolated planning**: `./adws/adw_plan_iso.py "Your feature"`

For more information, see:
- [README.md](../README.md) - Full Jerry documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [adws/README.md](../adws/README.md) - ADW workflow documentation
