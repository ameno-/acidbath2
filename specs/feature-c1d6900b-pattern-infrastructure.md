# Feature: Pattern Infrastructure - Jerry Patterns System Foundation

## Metadata
adw_id: `c1d6900b`
prompt: `pattern-infrastructure c1d6900b {"number": "pattern-infrastructure", "title": "Pattern Infrastructure - Jerry Patterns System Foundation", "body": "## Summary\n\nCreate the foundational pattern management infrastructure for Jerry. This establishes the directory structure, manifest schema, and development tooling for bundling Fabric patterns.\n\n## Parent Issue\n\nThis is Phase 1 of `issue-jerry-patterns-content-analysis.md`"}`

## Feature Description

This feature establishes the foundational infrastructure for Jerry's pattern management system. Jerry will bundle curated Fabric patterns as part of its framework, enabling content analysis capabilities without requiring users to install Fabric separately. This is Phase 1 of a larger content analysis initiative.

The feature creates:
- A structured directory system for organizing patterns by category
- A manifest schema for tracking pattern metadata
- A development tool (`jerry_sync_patterns.py`) for syncing patterns from local Fabric installations
- Initial bundle of 24 curated patterns across 5 categories
- Validation checks to ensure pattern integrity

Patterns are **development-time assets** synced from Fabric and committed to Jerry's repository, not runtime dependencies. This means patterns are versioned with Jerry and distributed as part of the framework.

## User Story

As a **Jerry framework maintainer**
I want to **bundle curated Fabric patterns within Jerry's codebase**
So that **users can leverage content analysis capabilities without managing Fabric installations themselves**

## Problem Statement

Jerry aims to provide content analysis capabilities (YouTube analysis, technical content extraction, research synthesis) but currently lacks the infrastructure to bundle and manage Fabric patterns. This creates several issues:

1. **No pattern storage structure** - Nowhere to organize patterns within Jerry
2. **No pattern metadata tracking** - Can't track which patterns are bundled, their versions, or sources
3. **No sync mechanism** - No way to import patterns from Fabric during development
4. **No validation** - Can't verify pattern integrity or completeness
5. **Manual management burden** - Pattern updates require manual file copying

This prevents Jerry from evolving toward its content analysis goals outlined in the parent issue.

## Solution Statement

Create a comprehensive pattern infrastructure that:

1. **Establishes directory structure** - `.jerry/patterns/` with category-based organization
2. **Defines manifest schema** - Track all pattern metadata in `manifest.json`
3. **Provides sync tooling** - `jerry_sync_patterns.py` automates pattern imports from Fabric
4. **Bundles initial patterns** - 24 curated patterns across core, YouTube, technical, educational, and research categories
5. **Integrates validation** - Extend `jerry_validate.py` to check pattern integrity

The solution treats patterns as first-class Jerry assets with proper tooling, versioning, and validation.

## Relevant Files

### Existing Files to Modify

- `/Users/ameno/dev/tac/tac-8/trees/c1d6900b/.jerry/manifest.json` - Add `patterns_version` field and pattern-related metadata
- `/Users/ameno/dev/tac/tac-8/trees/c1d6900b/adws/jerry_validate.py` - Add Level 1 validation checks for pattern infrastructure (manifest exists, pattern files present, category counts)
- `/Users/ameno/dev/tac/tac-8/trees/c1d6900b/.gitignore` - Ensure `.jerry/patterns/` is tracked (not ignored), while excluding temporary sync artifacts

### New Files

#### Pattern Infrastructure

- `.jerry/patterns/manifest.json` - Pattern manifest with metadata schema (version, last_synced, fabric_version, pattern registry)
- `.jerry/patterns/core/` - Core analysis patterns directory (7 patterns)
- `.jerry/patterns/youtube/` - YouTube-specific patterns directory (4 patterns)
- `.jerry/patterns/technical/` - Technical content patterns directory (5 patterns)
- `.jerry/patterns/educational/` - Educational patterns directory (3 patterns)
- `.jerry/patterns/research/` - Research patterns directory (5 patterns)
- `.jerry/patterns/custom/` - User custom patterns directory (empty, for future extensions)
- `.jerry/patterns/README.md` - Pattern system documentation (explains structure, categories, sync process)

#### Pattern Sync Tool

- `adws/jerry_sync_patterns.py` - Development tool to sync patterns from local Fabric installation with features:
  - List available Fabric patterns (`--list`)
  - Sync all bundled patterns (default)
  - Sync specific category (`--category youtube`)
  - Sync specific pattern (`--pattern extract_wisdom`)
  - Dry run mode (`--dry-run`)
  - Incremental sync (only changed patterns)
  - Automatic manifest updates

#### Pattern Files (24 initial patterns)

Each pattern includes:
- `system.md` - Pattern system prompt (required)
- `user.md` - Pattern user prompt template (if exists in Fabric)
- `meta.json` - Pattern metadata (name, category, description, fabric_source)

**Core Patterns (7)**:
- `.jerry/patterns/core/extract_wisdom/` - Extract key insights and wisdom
- `.jerry/patterns/core/extract_insights/` - Extract actionable insights
- `.jerry/patterns/core/extract_recommendations/` - Extract recommendations
- `.jerry/patterns/core/rate_content/` - Rate content quality
- `.jerry/patterns/core/create_summary/` - Create comprehensive summary
- `.jerry/patterns/core/create_5_sentence_summary/` - Create 5-sentence summary
- `.jerry/patterns/core/extract_references/` - Extract references and citations

**YouTube Patterns (4)**:
- `.jerry/patterns/youtube/youtube_summary/` - Summarize YouTube videos
- `.jerry/patterns/youtube/extract_youtube_metadata/` - Extract video metadata
- `.jerry/patterns/youtube/get_wow_per_minute/` - Calculate engagement metrics
- `.jerry/patterns/youtube/extract_agent_opportunities/` - Identify automation opportunities

**Technical Patterns (5)**:
- `.jerry/patterns/technical/extract_technical_content/` - Extract technical details
- `.jerry/patterns/technical/analyze_code/` - Analyze code quality
- `.jerry/patterns/technical/extract_poc/` - Extract proof of concept
- `.jerry/patterns/technical/analyze_terraform_plan/` - Analyze Terraform plans
- `.jerry/patterns/technical/analyze_logs/` - Analyze log files

**Educational Patterns (3)**:
- `.jerry/patterns/educational/extract_educational_value/` - Extract learning value
- `.jerry/patterns/educational/create_knowledge_artifacts/` - Create knowledge artifacts
- `.jerry/patterns/educational/create_flash_cards/` - Generate flash cards

**Research Patterns (5)**:
- `.jerry/patterns/research/analyze_paper/` - Analyze research papers
- `.jerry/patterns/research/analyze_claims/` - Analyze claims and evidence
- `.jerry/patterns/research/analyze_threat_report/` - Analyze security threats
- `.jerry/patterns/research/analyze_patent/` - Analyze patent documents
- `.jerry/patterns/research/extract_article_wisdom/` - Extract article insights

## Implementation Plan

### Phase 1: Foundation
Create the directory structure and manifest schema to establish the pattern infrastructure foundation.

**Deliverables:**
- `.jerry/patterns/` directory with category subdirectories
- Pattern manifest schema defined and documented
- Updated `.jerry/manifest.json` with patterns_version field

### Phase 2: Core Implementation
Build the pattern sync tool and integrate validation checks.

**Deliverables:**
- `jerry_sync_patterns.py` with full feature set (list, sync, category filters, dry-run)
- Pattern validation added to `jerry_validate.py`
- Pattern system documentation (`.jerry/patterns/README.md`)

### Phase 3: Integration
Sync the initial 24 patterns and validate the complete infrastructure.

**Deliverables:**
- 24 patterns synced from local Fabric installation
- All patterns tracked in manifest with metadata
- Validation passing for all pattern checks
- `.gitignore` updated to track patterns correctly

## Step by Step Tasks

### Group A: Foundation [parallel: false, model: sonnet]
Sequential foundation work establishing directory structure and schemas.

#### Step A.1: Create Pattern Directory Structure
- Create `.jerry/patterns/` base directory
- Create category subdirectories: `core/`, `youtube/`, `technical/`, `educational/`, `research/`, `custom/`
- Verify all directories are created successfully

#### Step A.2: Define Pattern Manifest Schema
- Create `.jerry/patterns/manifest.json` with schema:
  ```json
  {
    "version": "1.0.0",
    "last_synced": "2025-12-15T16:00:00Z",
    "fabric_version": "1.4.0",
    "source_patterns_count": 231,
    "bundled_patterns_count": 0,
    "categories": {
      "core": {"count": 0, "patterns": []},
      "youtube": {"count": 0, "patterns": []},
      "technical": {"count": 0, "patterns": []},
      "educational": {"count": 0, "patterns": []},
      "research": {"count": 0, "patterns": []},
      "custom": {"count": 0, "patterns": []}
    },
    "patterns": {}
  }
  ```
- Validate JSON syntax
- Document schema fields in comments or README

#### Step A.3: Update Jerry Manifest
- Open `/Users/ameno/dev/tac/tac-8/trees/c1d6900b/.jerry/manifest.json`
- Add `"patterns_version": "1.0.0"` field to root object
- Add patterns directory to `optional_directories` array: `".jerry/patterns/"`
- Validate JSON syntax

#### Step A.4: Create Pattern Documentation
- Create `.jerry/patterns/README.md` with:
  - Overview of pattern system
  - Directory structure explanation
  - Category descriptions
  - Sync process documentation
  - Usage instructions (for future pattern execution)
  - Contribution guidelines for custom patterns

### Group B: Sync Tool Implementation [parallel: false, depends: A, model: sonnet]
Build the pattern sync tool with incremental features.

#### Step B.1: Create jerry_sync_patterns.py Base Structure
- Create `/Users/ameno/dev/tac/tac-8/trees/c1d6900b/adws/jerry_sync_patterns.py`
- Add shebang: `#!/usr/bin/env -S uv run --quiet --script`
- Add script dependencies in PEP 723 format: click, rich, pyyaml
- Create CLI skeleton with Click framework
- Add `--help` flag functionality
- Test script is executable: `chmod +x adws/jerry_sync_patterns.py`

#### Step B.2: Implement Pattern Discovery
- Add function `discover_fabric_patterns()` to scan `~/.config/fabric/patterns/`
- Return list of available pattern names
- Handle case where Fabric is not installed (graceful error)
- Add `--list` command to display discovered patterns
- Test listing functionality

#### Step B.3: Implement Pattern Sync Logic
- Add function `sync_pattern(pattern_name, category, base_path)` to:
  - Read `system.md` from Fabric pattern directory
  - Read `user.md` if it exists
  - Create target pattern directory in `.jerry/patterns/{category}/{pattern_name}/`
  - Copy `system.md` and `user.md` files
  - Generate `meta.json` with pattern metadata (name, category, fabric_source, synced_at)
  - Return sync result (success/failure, files copied)

#### Step B.4: Implement Manifest Updates
- Add function `update_manifest(pattern_name, category, meta)` to:
  - Read `.jerry/patterns/manifest.json`
  - Add/update pattern entry in `patterns` object
  - Increment category count in `categories[category].count`
  - Add pattern name to `categories[category].patterns` array
  - Update `last_synced` timestamp
  - Update `bundled_patterns_count`
  - Write updated manifest back to file
- Add incremental sync support (skip if pattern unchanged)

#### Step B.5: Add CLI Features
- Implement `--category` filter to sync specific category
- Implement `--pattern` filter to sync specific pattern
- Implement `--dry-run` flag to preview changes without writing
- Add rich progress bars and status output
- Add error handling and validation
- Test all CLI flags

### Group C: Validation Integration [parallel: false, depends: B, model: sonnet]
Integrate pattern validation into jerry_validate.py.

#### Step C.1: Add Pattern Validation to jerry_validate.py
- Open `/Users/ameno/dev/tac/tac-8/trees/c1d6900b/adws/jerry_validate.py`
- Add to `validate_level_1()` function:
  - Check `.jerry/patterns/manifest.json` exists
  - Validate manifest JSON syntax
  - Read manifest and verify schema fields
  - Check all patterns in manifest have corresponding directories
  - Verify each pattern has `system.md` file
  - Report pattern count by category
  - Warn if `bundled_patterns_count` is 0
- Add validation result to Level 1 output
- Test validation with empty patterns directory

#### Step C.2: Update .gitignore
- Open `/Users/ameno/dev/tac/tac-8/trees/c1d6900b/.gitignore`
- Ensure `.jerry/patterns/` is **not** ignored (patterns should be committed)
- Add patterns to be tracked: `!.jerry/patterns/`
- Add temp sync artifacts to ignore if needed: `.jerry/patterns/.sync_tmp/`
- Verify git tracking with `git status`

### Group D: Pattern Sync Execution [parallel: true, depends: C, model: sonnet]
Sync all 24 initial patterns in parallel by category.

#### Step D.1: Sync Core Patterns (7)
- Run `./adws/jerry_sync_patterns.py --category core` for:
  - extract_wisdom
  - extract_insights
  - extract_recommendations
  - rate_content
  - create_summary
  - create_5_sentence_summary
  - extract_references
- Verify all 7 patterns synced successfully
- Check manifest updated correctly

#### Step D.2: Sync YouTube Patterns (4)
- Run `./adws/jerry_sync_patterns.py --category youtube` for:
  - youtube_summary
  - extract_youtube_metadata
  - get_wow_per_minute
  - extract_agent_opportunities
- Verify all 4 patterns synced successfully
- Check manifest updated correctly

#### Step D.3: Sync Technical Patterns (5)
- Run `./adws/jerry_sync_patterns.py --category technical` for:
  - extract_technical_content
  - analyze_code
  - extract_poc
  - analyze_terraform_plan
  - analyze_logs
- Verify all 5 patterns synced successfully
- Check manifest updated correctly

#### Step D.4: Sync Educational Patterns (3)
- Run `./adws/jerry_sync_patterns.py --category educational` for:
  - extract_educational_value
  - create_knowledge_artifacts
  - create_flash_cards
- Verify all 3 patterns synced successfully
- Check manifest updated correctly

#### Step D.5: Sync Research Patterns (5)
- Run `./adws/jerry_sync_patterns.py --category research` for:
  - analyze_paper
  - analyze_claims
  - analyze_threat_report
  - analyze_patent
  - extract_article_wisdom
- Verify all 5 patterns synced successfully
- Check manifest updated correctly

### Group E: Final Validation [parallel: false, depends: D, model: sonnet]
Validate the complete pattern infrastructure.

#### Step E.1: Run Full Validation Suite
- Execute `./adws/jerry_validate.py --level 1`
- Verify all pattern checks pass:
  - Manifest exists and valid
  - All 24 patterns present
  - All patterns have system.md files
  - Category counts correct (core:7, youtube:4, technical:5, educational:3, research:5, custom:0)
  - bundled_patterns_count equals 24
- Review validation output for warnings or errors

#### Step E.2: Verify Git Tracking
- Run `git status` to verify patterns are staged
- Check `.jerry/patterns/` shows in git status (not ignored)
- Verify all pattern files tracked: `git ls-files .jerry/patterns/ | wc -l` (should be ~72 files: 24 patterns × 3 files average)
- Run `git diff --cached` to review pattern content before commit

#### Step E.3: Final Manual Verification
- Manually inspect 3 sample patterns (one from each category):
  - `.jerry/patterns/core/extract_wisdom/system.md` exists and has content
  - `.jerry/patterns/youtube/youtube_summary/meta.json` has valid metadata
  - `.jerry/patterns/technical/analyze_code/system.md` exists and has content
- Verify manifest.json has all 24 pattern entries
- Check `last_synced` timestamp is recent
- Confirm `fabric_version` is populated

#### Step E.4: Test Sync Tool Edge Cases
- Test `--dry-run` flag: `./adws/jerry_sync_patterns.py --dry-run`
- Test `--list` flag: `./adws/jerry_sync_patterns.py --list`
- Test re-sync (incremental): run sync again, verify only changed patterns updated
- Test error handling: try syncing non-existent pattern
- Verify all edge cases handled gracefully

## Testing Strategy

### Unit Tests

**Pattern Sync Tool Tests:**
- Test pattern discovery from Fabric installation
- Test single pattern sync with all metadata fields
- Test category-based filtering
- Test dry-run mode (no writes)
- Test incremental sync (skip unchanged patterns)
- Test manifest updates (add, update entries)
- Test error handling (missing Fabric, invalid pattern names)

**Validation Tests:**
- Test manifest existence check
- Test manifest JSON schema validation
- Test pattern file existence checks
- Test category count accuracy
- Test warning generation for empty patterns

### Integration Tests

**End-to-End Sync Test:**
1. Start with empty `.jerry/patterns/` directory
2. Run `jerry_sync_patterns.py` with `--dry-run` (verify no writes)
3. Run full sync without filters
4. Verify all 24 patterns synced
5. Verify manifest updated correctly
6. Run validation and confirm pass

**Incremental Sync Test:**
1. Sync all patterns
2. Modify one pattern in Fabric
3. Re-run sync
4. Verify only modified pattern re-synced
5. Verify manifest updated correctly

### Edge Cases

**Missing Fabric Installation:**
- Fabric not installed at `~/.config/fabric/patterns/`
- Tool should display helpful error: "Fabric not found. Install from: https://github.com/danielmiessler/fabric"
- Exit gracefully with code 1

**Invalid Pattern Names:**
- User specifies `--pattern nonexistent_pattern`
- Tool should display: "Pattern 'nonexistent_pattern' not found in Fabric installation"
- List available patterns as suggestion

**Corrupted Manifest:**
- Manifest JSON is invalid
- Tool should display: "Manifest JSON is corrupted. Run with --reset to rebuild"
- Provide recovery instructions

**Git Tracking Issues:**
- Patterns ignored by .gitignore
- Validation should warn: "Patterns directory not tracked by git. Update .gitignore"
- Provide fix instructions

**Pattern File Missing:**
- Pattern directory exists but `system.md` missing
- Validation should fail: "Pattern '{pattern}' missing system.md"
- List affected patterns

**Fabric Version Mismatch:**
- Fabric updated to new version with breaking changes
- Manifest tracks `fabric_version`
- Validation warns if version mismatch detected
- Recommend re-sync

## Acceptance Criteria

- [ ] `.jerry/patterns/` directory structure exists with all 6 category subdirectories
- [ ] `.jerry/patterns/manifest.json` exists with valid schema (version, last_synced, fabric_version, categories, patterns)
- [ ] `.jerry/manifest.json` updated with `patterns_version` field
- [ ] `jerry_sync_patterns.py` successfully syncs patterns from local Fabric installation
- [ ] All CLI flags work: `--list`, `--category`, `--pattern`, `--dry-run`
- [ ] 24 initial patterns bundled in correct categories:
  - Core: 7 patterns
  - YouTube: 4 patterns
  - Technical: 5 patterns
  - Educational: 3 patterns
  - Research: 5 patterns
  - Custom: 0 patterns (empty directory)
- [ ] Every pattern has `system.md` file with content from Fabric
- [ ] Every pattern has `meta.json` with metadata (name, category, fabric_source, synced_at)
- [ ] Patterns with `user.md` in Fabric have it copied
- [ ] `jerry_validate.py` Level 1 includes pattern validation checks
- [ ] Validation reports pattern count: "24 patterns bundled across 5 categories"
- [ ] Validation warns if patterns directory empty
- [ ] All synced patterns tracked in git (not ignored)
- [ ] `.jerry/patterns/README.md` documents pattern system
- [ ] Incremental sync only updates changed patterns
- [ ] Error handling graceful for missing Fabric installation

## Validation Commands

Execute these commands to validate the feature is complete:

**1. Verify Directory Structure:**
```bash
# Check pattern directories exist
ls -la .jerry/patterns/
# Expected: core/, youtube/, technical/, educational/, research/, custom/, manifest.json, README.md

# Check category directories have patterns
find .jerry/patterns/ -name "system.md" | wc -l
# Expected: 24 (one per pattern)
```

**2. Validate Manifest Schema:**
```bash
# Check manifest is valid JSON
cat .jerry/patterns/manifest.json | python3 -m json.tool > /dev/null && echo "Valid JSON"

# Check manifest has required fields
cat .jerry/patterns/manifest.json | grep -E '"version"|"last_synced"|"fabric_version"|"bundled_patterns_count"'
# Expected: All 4 fields present

# Verify pattern count
cat .jerry/patterns/manifest.json | grep '"bundled_patterns_count"'
# Expected: "bundled_patterns_count": 24
```

**3. Test Sync Tool:**
```bash
# Test help flag
./adws/jerry_sync_patterns.py --help
# Expected: CLI help text displays

# Test list command
./adws/jerry_sync_patterns.py --list
# Expected: Lists all available Fabric patterns

# Test dry-run
./adws/jerry_sync_patterns.py --dry-run
# Expected: Shows what would be synced, no writes

# Test category sync
./adws/jerry_sync_patterns.py --category core --dry-run
# Expected: Shows 7 core patterns would be synced
```

**4. Run Validation:**
```bash
# Run Level 1 validation (includes pattern checks)
./adws/jerry_validate.py --level 1
# Expected: All pattern validation checks pass
# Expected output includes: "24 patterns bundled across 5 categories"

# Check for warnings
./adws/jerry_validate.py --level 1 | grep -i warning
# Expected: No warnings if all patterns synced correctly
```

**5. Verify Git Tracking:**
```bash
# Check patterns are tracked
git ls-files .jerry/patterns/ | head -5
# Expected: Lists pattern files (not empty)

# Verify not ignored
git check-ignore .jerry/patterns/core/extract_wisdom/system.md
# Expected: No output (not ignored)

# Count tracked pattern files
git ls-files .jerry/patterns/ | wc -l
# Expected: ~72+ files (24 patterns × average 3 files each)
```

**6. Sample Pattern Inspection:**
```bash
# Check core pattern exists
cat .jerry/patterns/core/extract_wisdom/system.md | head -5
# Expected: Fabric system prompt content

# Check pattern metadata
cat .jerry/patterns/core/extract_wisdom/meta.json
# Expected: Valid JSON with name, category, fabric_source, synced_at

# Verify YouTube pattern
ls .jerry/patterns/youtube/youtube_summary/
# Expected: system.md, user.md (if exists), meta.json
```

**7. Test Incremental Sync:**
```bash
# First sync
./adws/jerry_sync_patterns.py --pattern extract_wisdom

# Re-sync same pattern (should skip if unchanged)
./adws/jerry_sync_patterns.py --pattern extract_wisdom
# Expected: Message like "Pattern 'extract_wisdom' unchanged, skipping"
```

**8. Python Module Validation:**
```bash
# Test Python syntax
uv run python -m py_compile adws/jerry_sync_patterns.py
# Expected: No output (syntax valid)

# Test script is executable
test -x adws/jerry_sync_patterns.py && echo "Executable"
# Expected: "Executable"
```

**9. Manifest Integration Check:**
```bash
# Check Jerry manifest updated
cat .jerry/manifest.json | grep "patterns_version"
# Expected: "patterns_version": "1.0.0"

# Verify optional_directories includes patterns
cat .jerry/manifest.json | grep "\.jerry/patterns"
# Expected: ".jerry/patterns/" in optional_directories array
```

**10. Documentation Check:**
```bash
# Verify README exists
test -f .jerry/patterns/README.md && echo "README exists"
# Expected: "README exists"

# Check README has required sections
grep -E "## Overview|## Directory Structure|## Categories|## Sync Process" .jerry/patterns/README.md
# Expected: All 4 section headers present
```

## Notes

### Technical Implementation Notes

**Pattern Metadata Schema (meta.json):**
```json
{
  "name": "extract_wisdom",
  "category": "core",
  "description": "Extract key insights, wisdom, and actionable items from content",
  "fabric_source": "~/.config/fabric/patterns/extract_wisdom",
  "synced_at": "2025-12-15T16:30:00Z",
  "files": ["system.md", "user.md"],
  "checksum": "sha256:abc123..."
}
```

**Fabric Pattern Source:**
- Default Fabric location: `~/.config/fabric/patterns/`
- Each pattern is a directory containing:
  - `system.md` (required) - System prompt
  - `user.md` (optional) - User prompt template
  - Other files (ignored by sync tool)

**Incremental Sync Strategy:**
- Compare file checksums (SHA256) to detect changes
- Skip patterns where checksums match
- Update `last_synced` timestamp only for changed patterns
- Rebuild manifest categories on every sync

**Error Recovery:**
- If sync fails mid-process, patterns directory may be incomplete
- Manifest tracks partial state
- Re-running sync completes missing patterns
- `--dry-run` useful for previewing before real sync

### Future Considerations

**Phase 2 - Pattern Execution:**
- Create `jerry_run_pattern.py` to execute patterns on content
- Integrate with Claude Code agent system
- Pattern chaining (output of one → input of another)

**Phase 3 - Custom Patterns:**
- Allow users to add patterns to `custom/` directory
- Custom pattern validation
- Pattern contribution workflow

**Phase 4 - Pattern Versioning:**
- Track pattern versions separately from Jerry version
- Support multiple pattern versions simultaneously
- Migration guides for pattern updates

**Phase 5 - Pattern Discovery:**
- Auto-discover new patterns in Fabric
- Suggest patterns based on content type
- Pattern recommendation engine

### Dependencies

**Development Dependencies:**
- Local Fabric CLI installation (for pattern sync)
  - Install: `brew install fabric` or from https://github.com/danielmiessler/fabric
  - Fabric patterns at: `~/.config/fabric/patterns/`
- Python 3.11+ with `uv` package manager
- Git (for tracking patterns)

**Runtime Dependencies:**
- None (patterns bundled with Jerry, no Fabric required for execution)

**Python Package Dependencies (for jerry_sync_patterns.py):**
- `click>=8.0.0` - CLI framework
- `rich>=13.0.0` - Rich terminal output
- `pyyaml>=6.0.0` - YAML parsing (for future pattern metadata)

### Pattern Categories Rationale

**Core (7 patterns):**
Fundamental content analysis applicable to any content type. These patterns extract universal insights (wisdom, insights, recommendations) and provide summarization capabilities.

**YouTube (4 patterns):**
Specialized for YouTube video content. Extract metadata, generate summaries, calculate engagement metrics, and identify automation opportunities from video transcripts.

**Technical (5 patterns):**
Analysis of technical content including code, infrastructure (Terraform), and operational data (logs). Essential for engineering content analysis.

**Educational (3 patterns):**
Extract learning value and create educational artifacts. Useful for analyzing tutorials, courses, and knowledge-sharing content.

**Research (5 patterns):**
Academic and professional research analysis. Covers papers, claims analysis, security reports, and patents. Supports evidence-based reasoning.

**Custom (0 patterns initially):**
Reserved for user-contributed or project-specific patterns. Allows extensibility without modifying Jerry's core patterns.

### Manifest Schema Rationale

The manifest tracks:
- **version**: Pattern infrastructure version (semantic versioning)
- **last_synced**: Timestamp of most recent sync (ISO 8601 UTC)
- **fabric_version**: Version of Fabric used as source (for compatibility tracking)
- **source_patterns_count**: Total patterns available in Fabric installation (for reference)
- **bundled_patterns_count**: Total patterns bundled in Jerry (should equal sum of category counts)
- **categories**: Per-category metadata (count, pattern list)
- **patterns**: Full pattern registry with individual metadata

This structure supports:
- Version compatibility tracking
- Incremental sync detection
- Validation and integrity checks
- Future pattern versioning

### Sync Tool Design Decisions

**Why Python script instead of Bash:**
- Better error handling and validation
- Structured JSON/YAML parsing
- Rich CLI output with progress bars
- Cross-platform compatibility
- Easier to test and maintain

**Why `uv run --script` instead of requirements.txt:**
- Self-contained dependency declaration (PEP 723)
- No separate requirements file needed
- Faster execution with uv
- Consistent with other Jerry scripts

**Why incremental sync:**
- Avoid re-copying unchanged patterns
- Faster development workflow
- Preserve local customizations (if any)
- Reduce git noise (fewer unnecessary changes)

**Why category organization:**
- Logical grouping for discoverability
- Easier to sync subsets of patterns
- Future-proof for category-specific features
- Aligns with Fabric's pattern taxonomy

### Git Tracking Strategy

**Patterns should be committed:**
- Patterns are development-time assets, not build artifacts
- Users without Fabric installation need patterns available
- Pattern versions tied to Jerry releases
- Enables pattern evolution tracking in git history

**Temporary files should be ignored:**
- Sync artifacts (`.sync_tmp/`)
- Pattern execution outputs (created by future execution tool)
- User-specific customizations (if implemented)

**Recommended .gitignore additions:**
```
# Jerry pattern sync artifacts
.jerry/patterns/.sync_tmp/

# Jerry pattern execution outputs (future)
.jerry/patterns/.execution_cache/
```
