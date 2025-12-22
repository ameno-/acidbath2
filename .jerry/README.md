# Jerry Metadata Directory

This directory contains Jerry framework metadata, manifests, and configuration templates for deployment.

## Structure

```
.jerry/
├── manifest.json          # Jerry core manifest with version, dependencies, and checksums
├── templates/            # Configuration templates for deployment
│   ├── env.template      # Environment variables template
│   ├── gitignore.template # Recommended .gitignore additions
│   └── worktree.config.template # Worktree configuration template
└── README.md            # This file
```

## Manifest Schema

The `manifest.json` file contains:

### Core Fields
- `name`: Framework name ("jerry")
- `version`: Semantic version (MAJOR.MINOR.PATCH)
- `description`: Brief framework description
- `python_version`: Required Python version
- `created_at`: Manifest creation timestamp

### Directories
- `core_directories`: Essential Jerry directories (adws/, .claude/, specs/)
- `optional_directories`: Optional directories for enhanced functionality
- `required_files`: Minimum viable files for Jerry to function

### Requirements
- `system_requirements`: System-level dependencies (Python, uv, git, Claude Code CLI)
- `python_dependencies`: Required Python packages
- `optional_dependencies`: Optional integrations (GitHub, Linear, Notion)

### Integrity
- `integrity.algorithm`: Checksum algorithm (sha256)
- `integrity.checksums`: File checksums for verification (populated during export)

## Usage

### Reading the Manifest
```python
import json

with open('.jerry/manifest.json', 'r') as f:
    manifest = json.load(f)

print(f"Jerry version: {manifest['version']}")
print(f"Core dirs: {manifest['core_directories']}")
```

### Validating Installation
The manifest defines what constitutes a complete Jerry installation:
1. All core directories must exist
2. All required files must be present
3. System requirements must be met
4. Python dependencies must be installed

### Export Process
During export (`jerry_export.py`):
1. Manifest is loaded
2. Core files are collected based on manifest definitions
3. Checksums are computed for all files
4. Updated manifest with checksums is included in export package

### Bootstrap Process
During bootstrap (`jerry_bootstrap.sh`):
1. Prerequisites are validated against `system_requirements`
2. Files are extracted and verified using checksums
3. Python dependencies are installed from `python_dependencies`
4. Optional dependencies installed based on user selection

## Templates

Configuration templates in `templates/` are copied during bootstrap to help users set up Jerry in their repositories.

### env.template
Environment variables needed for Jerry to function:
- API keys (ANTHROPIC_API_KEY)
- Optional integration credentials
- Worktree configuration

### gitignore.template
Recommended additions to `.gitignore`:
- agents/ output directory
- trees/ worktree directory
- .env files
- Python cache

### worktree.config.template
Worktree isolation settings:
- Base branch configuration
- Port allocation ranges
- Cleanup policies

## Import State Tracking

When Jerry is bootstrapped into a project, an `import_state.json` file is created to track progress. This enables **resumable imports** - if the process is interrupted, it can be continued from where it left off.

### State File Location

```
<target-repo>/.jerry/import_state.json
```

### State File Structure

```json
{
  "import_id": "abc12345",
  "started_at": "2025-12-07T10:30:00Z",
  "source_repo": "/path/to/jerry",
  "target_repo": "/path/to/my-project",
  "current_phase": "configure",
  "phases": {
    "prereqs": { "status": "completed", "checks": {...} },
    "setup": { "status": "completed", "tasks": {...} },
    "install": { "status": "completed", "tasks": {...} },
    "configure": { "status": "in_progress", "notes": "..." },
    "validate": { "status": "pending" }
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
| `failed` | Failed with error |
| `skipped` | User chose to skip |

### Resuming an Import

```bash
# Check current state
cat .jerry/import_state.json | python3 -m json.tool

# Resume with Claude
claude /bootstrap <target> --resume
```

For full details on the bootstrap process, see [docs/BOOTSTRAP.md](../docs/BOOTSTRAP.md).

## Parallel Phases

Jerry bootstrap executes in 5 parallel phases for efficiency:

1. **PREREQS** - Check Python, uv, git, claude (parallel)
2. **SETUP** - Export + verify target (parallel)
3. **INSTALL** - Extract, deps, dirs, templates (pipeline + parallel)
4. **CONFIGURE** - User sets up .env (sequential, may pause)
5. **VALIDATE** - L1+L2 (parallel), then L3, then L4

This reduces bootstrap time by 40-50% compared to sequential execution.

## Level 4 Validation Required

**Level 4 (Full SDLC) validation is mandatory** for all Jerry installations:

- Tests `adw_plan_iso.py` workflow
- Tests `adw_build_iso.py` workflow
- Verifies worktree isolation
- Takes ~5 minutes to complete

```bash
./adws/jerry_validate.py --level 4
```

## Version Management

Jerry follows semantic versioning:
- **MAJOR**: Breaking changes to manifest schema or core APIs
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, no new features

Example version progression:
- `0.1.0` - Initial release
- `0.2.0` - Add optional directory for plugins
- `0.2.1` - Fix checksum validation bug
- `1.0.0` - Stable API, breaking change to manifest schema

## Future Enhancements

Planned additions to manifest:
- Plugin registry for third-party ADWs
- Migration scripts between versions
- Deprecation warnings
- Feature flags
- Environment-specific overrides
