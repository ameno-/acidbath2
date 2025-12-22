# Feature: Jerry Simple Update System

## Metadata
adw_id: `2fa04caa`
prompt: `{"number": "jerry-simple-update", "title": "Local Issue jerry-simple-update", "body": "# Issue: Jerry Simple Update System (Option B)\n\n## Summary\n\nImplement a simple version-based update system for Jerry installations using git-diff style updates. This replaces the over-engineered migration framework proposal with a minimal, maintainable solution.\n\n## Problem\n\n1. Jerry installations currently have no update mechanism\n2. Two external applications have Jerry bootstrapped but are unversioned\n3. Users must manually re-bootstrap to get updates, risking loss of customizations\n4. The previously proposed update system was over-engineered (2000+ lines, migration framework, rollback logic)\n\n## Solution: Option B - Version File + Diff-Based Update\n\nA simple update script (~100-150 lines) that:\n1. Reads local version from manifest (treats missing version as \"0.0.0\")\n2. Fetches remote version from GitHub releases or export tarball\n3. Downloads and extracts update package\n4. Rsyncs core files while preserving user directories\n5. Updates manifest version"}`

## Feature Description
Implement a minimal, maintainable update system for Jerry installations that enables users to safely update their Jerry framework without losing customizations. The system will use version-based detection from `.jerry/manifest.json` and support multiple update sources (GitHub releases, local tarballs, or directory paths). The implementation will be a single ~100-150 line script using `rsync` to update core directories (`adws/`, `.claude/`, `.jerry/`) while preserving user-specific directories (`agents/`, `trees/`, `specs/`, `.env`, `.ports.env`).

This replaces manual re-bootstrapping with an automated, safe update process that treats unversioned installations as "0.0.0" baseline and migrates them to versioned updates.

## User Story
As a Jerry framework user with a bootstrapped installation
I want to update my Jerry framework to the latest version
So that I can get new features and bug fixes without losing my customizations and without manually re-bootstrapping

## Problem Statement
Jerry installations currently lack an update mechanism, forcing users to manually re-bootstrap to receive updates. This process:
1. Risks losing user customizations (custom agents, slash commands, specs)
2. Is error-prone and time-consuming
3. Leaves two external applications with unversioned Jerry installations
4. Has no tracking of which version is installed
5. Provides no clear migration path for breaking changes

A previously proposed solution was over-engineered with 2000+ lines, migration frameworks, and rollback logic - far too complex for this use case.

## Solution Statement
Create a simple, focused update script (`jerry_update.py`) that:
1. Detects local version from `.jerry/manifest.json` (defaulting to "0.0.0" for unversioned installations)
2. Supports multiple update sources: GitHub releases, local tarballs, or directory paths
3. Uses `rsync` to update core directories while preserving user directories
4. Updates the manifest version after successful sync
5. Provides dry-run mode for safety
6. Points users to CHANGELOG.md for breaking changes (no automated migrations)

The script will be ~100-150 lines total, following Jerry's existing CLI patterns with `click` and `rich` for UX.

## Relevant Files

### Existing Files to Reference
- `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/.jerry/manifest.json` - Contains Jerry metadata, will be extended with version field
- `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/adws/adw_modules/agent.py` - Reference for CLI patterns and retry logic
- `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/adws/jerry_export.py` - Reference for export logic and manifest handling
- `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/adws/jerry_validate.py` - Reference for validation patterns
- `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/adws/adw_prompt.py` - Reference for click CLI structure with rich output
- `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/pyproject.toml` - Dependency management

### New Files

#### `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/adws/jerry_update.py`
Main update script (~100-150 lines). Implements version detection, update source resolution, rsync core files, and manifest updates. Uses click for CLI and rich for progress/output formatting.

#### `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/adws/tests/test_jerry_update.py`
Comprehensive unit tests covering all functions and edge cases. Uses pytest with fixtures for temporary directories and mock manifest files.

#### `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/CHANGELOG.md`
Initial changelog file following Keep a Changelog format. Documents version history and breaking changes. Users will be pointed here after updates.

### Modified Files

#### `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/.jerry/manifest.json`
Add `version` field (current: "0.1.0") and optional `update_url` field for default update source.

## Implementation Plan

### Phase 1: Foundation
Set up the basic infrastructure for the update system by creating the initial script structure, updating the manifest with version tracking, and creating the CHANGELOG. This phase establishes the core data model and provides the foundation for update operations.

### Phase 2: Core Implementation
Implement the core update functionality including version detection, update source resolution (GitHub/tarball/path), file synchronization logic, and manifest updates. This is the heart of the update system.

### Phase 3: Integration
Create comprehensive unit tests, validate the script works with dry-run mode, test update scenarios (unversioned to versioned, version upgrades), and ensure the implementation follows Jerry's existing patterns and conventions.

## Step by Step Tasks
IMPORTANT: Execute every step in order, respecting group dependencies.

Steps are organized into groups. Groups execute in dependency order.
Steps within a group can be parallel (independent) or sequential (ordered).

### Group A: Foundation [parallel: false, model: sonnet]
Sequential setup work establishing version tracking and documentation infrastructure.

#### Step A.1: Update Manifest with Version Field
- Read existing `.jerry/manifest.json`
- Add `"version": "0.1.0"` field to manifest
- Add optional `"update_url": "https://github.com/ameno-/tac"` field
- Validate JSON structure remains correct
- File path: `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/.jerry/manifest.json`

#### Step A.2: Create Initial CHANGELOG
- Create `CHANGELOG.md` in root directory following Keep a Changelog format
- Add `## [Unreleased]` section
- Add `## [0.1.0] - YYYY-MM-DD` section with initial release notes
- Include note about introducing update system
- File path: `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/CHANGELOG.md`

#### Step A.3: Create Test Directory Structure
- Create `adws/tests/` directory if it doesn't exist
- Create `adws/tests/__init__.py` to make it a package
- Set up test fixtures structure

### Group B: Core Implementation [parallel: false, depends: A, model: sonnet]
Sequential implementation of update script functions, building from foundational utilities to high-level orchestration.

#### Step B.1: Implement Version Detection Function
- Create `adws/jerry_update.py` with script header and dependencies
- Implement `get_local_version(jerry_root: Path) -> str` function
- Read `.jerry/manifest.json` and extract version field
- Return "0.0.0" if version field is missing or manifest doesn't exist
- Handle JSON parsing errors gracefully
- Add docstring documenting behavior

#### Step B.2: Implement Version Comparison Function
- Implement `compare_versions(local: str, remote: str) -> int` function
- Parse semver strings (e.g., "1.2.3")
- Return -1 if local < remote, 0 if equal, 1 if local > remote
- Handle edge cases like "0.0.0" baseline
- Validate semver format and raise ValueError if invalid

#### Step B.3: Implement Update Source Resolution
- Implement `resolve_update_source(source: Optional[str], jerry_root: Path) -> Tuple[str, Path]` function
- If source is None, check manifest for `update_url`, else use default GitHub
- If source is URL, download and extract to temp directory
- If source is tarball path, extract to temp directory
- If source is directory path, use directly
- Return tuple of (version, source_path)
- Raise ValueError for invalid sources

#### Step B.4: Implement File Sync Function
- Implement `sync_core_files(source: Path, target: Path, dry_run: bool) -> List[str]` function
- Use subprocess to call `rsync -av --dry-run` (if dry_run=True) or `rsync -av` (if dry_run=False)
- Sync core directories: `adws/`, `.claude/`, `.jerry/`
- Exclude user directories: `agents/`, `trees/`, `specs/`, `.env`, `.ports.env`
- Parse rsync output to collect list of changed files
- Return list of changed file paths
- Handle rsync errors and provide clear error messages

#### Step B.5: Implement Manifest Update Function
- Implement `update_manifest_version(jerry_root: Path, version: str) -> None` function
- Read existing `.jerry/manifest.json`
- Update `version` field with new version
- Write updated manifest back to file with proper formatting (indent=2)
- Validate JSON structure before writing
- Handle file I/O errors

#### Step B.6: Implement CLI Interface
- Create click command group with main entry point
- Add `--source` option (default: None, uses manifest or GitHub)
- Add `--dry-run` flag (default: False)
- Add `--force` flag (default: False, allows downgrade)
- Implement main update flow orchestrating all functions
- Add rich console output for progress, version comparison, and results
- Display changed files summary
- Point users to CHANGELOG.md after successful update

### Group C: Testing [parallel: true, depends: B, model: sonnet]
Parallel test development covering all functions and edge cases.

#### Step C.1: Write Version Detection Tests
- Test `test_get_local_version_exists` - version field present
- Test `test_get_local_version_missing` - no version field returns "0.0.0"
- Test `test_get_local_version_no_manifest` - missing manifest returns "0.0.0"
- Test `test_get_local_version_invalid_json` - malformed JSON raises appropriate error
- Use pytest fixtures for temporary manifest files

#### Step C.2: Write Version Comparison Tests
- Test `test_compare_versions_older` - local < remote returns -1
- Test `test_compare_versions_equal` - local == remote returns 0
- Test `test_compare_versions_newer` - local > remote returns 1
- Test `test_compare_versions_baseline` - "0.0.0" < any version
- Test `test_compare_versions_invalid` - invalid semver raises ValueError
- Test edge cases with different version component counts

#### Step C.3: Write File Sync Tests
- Test `test_sync_core_files_dry_run` - dry run mode makes no changes
- Test `test_sync_core_files_preserves_user_dirs` - agents/, trees/, specs/ untouched
- Test `test_sync_core_files_updates_core_dirs` - adws/, .claude/, .jerry/ updated
- Test `test_sync_core_files_new_files` - new files added correctly
- Test `test_sync_core_files_preserves_env` - .env and .ports.env preserved
- Use pytest fixtures for temporary source and target directories
- Mock rsync subprocess calls for unit testing

#### Step C.4: Write Manifest Update Tests
- Test `test_update_manifest_version_success` - version updated correctly
- Test `test_update_manifest_version_preserves_fields` - other fields untouched
- Test `test_update_manifest_version_invalid_json` - handles corrupt manifest
- Test `test_update_manifest_version_file_errors` - handles I/O errors
- Validate JSON formatting (indent=2)

#### Step C.5: Write Integration Tests
- Test `test_full_update_flow_unversioned_to_versioned` - 0.0.0 → 0.1.0
- Test `test_full_update_flow_version_upgrade` - 0.1.0 → 0.2.0
- Test `test_full_update_flow_dry_run` - no changes made in dry-run mode
- Test `test_full_update_flow_force_downgrade` - --force allows downgrade
- Test `test_full_update_flow_same_version` - no update when versions equal
- Use temporary directories and mock update sources

### Group D: Validation & Documentation [parallel: false, depends: C, model: sonnet]
Final validation and documentation updates.

#### Step D.1: Run All Tests and Fix Issues
- Execute `uv run pytest adws/tests/test_jerry_update.py -v`
- Address any test failures
- Ensure 100% test coverage for core functions
- Validate all edge cases pass

#### Step D.2: Test Manual Execution Scenarios
- Create temporary test Jerry installation
- Test update from GitHub (mock or actual if safe)
- Test update from local tarball
- Test update from directory path
- Test dry-run mode
- Test unversioned → versioned migration
- Validate --force flag behavior

#### Step D.3: Update README Documentation
- Add "Updating Jerry" section to README.md
- Document update command usage and options
- Document update sources (GitHub, tarball, path)
- Document migration path for unversioned installations
- Add examples of common update scenarios
- File path: `/Users/ameno/dev/tac/tac-8/trees/2fa04caa/README.md`

#### Step D.4: Validate Code Compiles
- Run `uv run python -m py_compile adws/jerry_update.py`
- Ensure no syntax errors
- Validate script header and dependencies are correct

## Testing Strategy

### Unit Tests
1. **Version Detection Tests** (`test_jerry_update.py`)
   - Test version field exists in manifest
   - Test missing version field defaults to "0.0.0"
   - Test missing manifest file defaults to "0.0.0"
   - Test malformed JSON handling

2. **Version Comparison Tests**
   - Test all comparison cases (older, equal, newer)
   - Test baseline "0.0.0" comparison
   - Test invalid semver format rejection
   - Test edge cases (1.0 vs 1.0.0, etc.)

3. **Update Source Resolution Tests**
   - Test GitHub URL resolution
   - Test local tarball extraction
   - Test directory path validation
   - Test default source from manifest
   - Test invalid source error handling

4. **File Sync Tests**
   - Test dry-run mode (no changes)
   - Test core directories updated
   - Test user directories preserved
   - Test new files added
   - Test environment files preserved (.env, .ports.env)
   - Mock rsync subprocess for isolation

5. **Manifest Update Tests**
   - Test version field updated correctly
   - Test other manifest fields preserved
   - Test JSON formatting maintained
   - Test file I/O error handling

6. **Integration Tests**
   - Test full unversioned → versioned flow
   - Test version upgrade flow
   - Test dry-run end-to-end
   - Test force downgrade
   - Test no-op when versions equal

### Edge Cases
1. **Missing Manifest**: Installation has no `.jerry/manifest.json` file
2. **Corrupt Manifest**: Manifest file exists but contains invalid JSON
3. **Missing Version Field**: Manifest exists but has no `version` field
4. **Invalid Semver**: Version string doesn't follow semver format
5. **Network Failures**: GitHub download fails or times out
6. **Disk Space**: Insufficient space for update
7. **Permission Errors**: Cannot write to target directories
8. **Partial Sync**: rsync interrupted mid-operation
9. **Downgrade Attempt**: User tries to update to older version without --force
10. **Same Version**: User attempts update when already on target version

## Acceptance Criteria
1. ✅ `jerry_update.py` script exists in `adws/` directory
2. ✅ Script is executable with proper shebang and uv dependencies
3. ✅ All core functions implemented: `get_local_version`, `compare_versions`, `resolve_update_source`, `sync_core_files`, `update_manifest_version`
4. ✅ CLI interface supports `--source`, `--dry-run`, and `--force` flags
5. ✅ Unversioned installations (missing version field) default to "0.0.0"
6. ✅ Update preserves user directories: `agents/`, `trees/`, `specs/`, `.env`, `.ports.env`
7. ✅ Update syncs core directories: `adws/`, `.claude/`, `.jerry/`
8. ✅ Dry-run mode shows changes without applying them
9. ✅ Manifest version field updated after successful update
10. ✅ All unit tests pass (`test_jerry_update.py`)
11. ✅ Integration tests validate full update flows
12. ✅ CHANGELOG.md created with initial entry for version 0.1.0
13. ✅ README.md updated with "Updating Jerry" section
14. ✅ Script handles all edge cases gracefully with clear error messages
15. ✅ Users pointed to CHANGELOG.md after update for breaking changes

## Validation Commands
Execute these commands to validate the feature is complete:

```bash
# 1. Validate script compiles
uv run python -m py_compile adws/jerry_update.py

# 2. Run all unit tests
uv run pytest adws/tests/test_jerry_update.py -v --tb=short

# 3. Test dry-run mode (should not modify files)
./adws/jerry_update.py --dry-run

# 4. Validate manifest has version field
cat .jerry/manifest.json | grep -q '"version"' && echo "✅ Version field present" || echo "❌ Version field missing"

# 5. Validate CHANGELOG exists
test -f CHANGELOG.md && echo "✅ CHANGELOG.md exists" || echo "❌ CHANGELOG.md missing"

# 6. Test script help output
./adws/jerry_update.py --help

# 7. Validate test coverage (optional)
uv run pytest adws/tests/test_jerry_update.py --cov=adws.jerry_update --cov-report=term-missing

# 8. Run integration test with temp directory (manual validation)
# Create temp Jerry installation, run update, verify core dirs updated and user dirs preserved
```

## Notes

### Design Decisions
1. **No Migration Framework**: Users read CHANGELOG.md for breaking changes rather than automated migrations. Keeps implementation simple and maintainable.
2. **No Rollback**: Failed updates leave installation in partial state; users can re-run or manually fix. Adding rollback would double complexity for minimal benefit.
3. **rsync vs Copy**: Using rsync provides efficient incremental updates and is widely available on Unix systems.
4. **Baseline Version "0.0.0"**: Treats all unversioned installations as baseline, enabling smooth migration path.

### Dependencies
- No new dependencies required beyond existing: `click`, `rich`, `pyyaml` already in `pyproject.toml`
- System dependency: `rsync` (available by default on macOS/Linux)

### Future Considerations
1. **Auto-update Check**: Could add optional check-for-updates command (out of scope)
2. **Update Notifications**: Could integrate with notification providers (out of scope)
3. **Version Compatibility Matrix**: Could add min/max version constraints (out of scope)
4. **GitHub Release Integration**: Could fetch versions from GitHub releases API instead of hardcoded (future enhancement)

### Security Considerations
1. **Source Validation**: Validate tarball checksums against manifest (current: basic validation)
2. **HTTPS Only**: Ensure GitHub downloads use HTTPS
3. **Path Traversal**: Validate extracted paths don't escape target directory

### Testing Notes
- Tests will use pytest fixtures for temporary directories
- Mock rsync subprocess calls to avoid actual file operations during unit tests
- Integration tests will use real temporary Jerry installations
- Test both happy path and error conditions for all functions
