# Jerry Patterns + Content Analysis Feature

## Overview

This document tracks the comprehensive feature implementation for Jerry's pattern management system and generic content analysis capabilities.

## Feature Summary

**Goal**: Make Jerry self-contained with bundled Fabric patterns and enable generic content analysis (YouTube, URL, PDF, text) without runtime Fabric dependency.

**Key Changes**:
1. Patterns become bundled assets synced at development time
2. Content analysis works for any input type
3. YouTube analyzer migrated into Jerry as specialized workflow
4. No runtime Fabric CLI dependency

## Implementation Phases

| Phase | ADW ID | Issue | Spec | Status | Depends On |
|-------|--------|-------|------|--------|------------|
| 1 | `c1d6900b` | `pattern-infrastructure` | `feature-c1d6900b-pattern-infrastructure.md` | ✅ Planned | - |
| 2 | `4d650f33` | `pattern-executor` | `feature-4d650f33-pattern-executor.md` | ✅ Planned | Phase 1 |
| 3 | `675a4152` | `content-extractors` | `feature-675a4152-content-extractors.md` | ✅ Planned | - |
| 4 | `85080678` | `generic-analysis-adw` | `feature-85080678-unified-content-analysis.md` | ✅ Planned | Phase 2, 3 |
| 5 | `b636eeb6` | `youtube-migration` | `feature-youtube-migration-b636eeb6-youtube-analyzer-migration.md` | ✅ Planned | Phase 4 |

## Worktrees

```
trees/
├── c1d6900b/  → feat-issue-pattern-infrastructure-adw-c1d6900b-jerry-patterns-foundation
├── 4d650f33/  → feat-issue-pattern-executor-adw-4d650f33-execute-bundled-patterns
├── 675a4152/  → feat-issue-content-extractors-adw-675a4152-multi-type-content-extraction
├── 85080678/  → feat-issue-generic-analysis-adw-adw-85080678-unified-content-analysis
└── b636eeb6/  → feat-issue-youtube-migration-adw-b636eeb6-youtube-analyzer-migration
```

## Dependency Graph

```
Phase 1: Pattern Infrastructure (c1d6900b)
    │
    ├─────────────────────────────────┐
    │                                 │
    ▼                                 ▼
Phase 2: Pattern Executor      Phase 3: Content Extractors
(4d650f33)                     (675a4152)
    │                                 │
    └────────────┬────────────────────┘
                 │
                 ▼
         Phase 4: Generic Analysis ADW
         (85080678)
                 │
                 ▼
         Phase 5: YouTube Migration
         (b636eeb6)
```

---

# META-PLAN: One-Shot Execution

## Execution Overview

This meta-plan enables a single agent to execute the entire Jerry Patterns feature implementation with proper build/test loops at each phase.

### Execution Timeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Pattern Infrastructure (~30 min)                                    │
│   Build → Test → Review → Merge                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│ PHASE 2: Pattern Executor   │ │ PHASE 3: Content Extractors │
│ (~25 min) [PARALLEL]        │ │ (~25 min) [PARALLEL]        │
│ Build → Test → Review       │ │ Build → Test → Review       │
└─────────────────────────────┘ └─────────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: Generic Analysis ADW (~30 min)                                      │
│   Build → Test → Review → Merge                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: YouTube Migration (~35 min)                                         │
│   Build → Test → Review → Merge                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ FINAL: Documentation + Integration Test + PR                                 │
│   (~20 min)                                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Total Estimated Time: 2.5 - 3 hours
```

---

## STEP 1: Phase 1 - Pattern Infrastructure

### 1.1 Build
```bash
cd /Users/ameno/dev/tac/tac-8
uv run ./adws/adw_build_iso.py local:pattern-infrastructure c1d6900b
```

### 1.2 Test Checklist
```bash
# Navigate to worktree
cd trees/c1d6900b

# T1.1: Verify directory structure
ls -la .jerry/patterns/
# Expected: core/, youtube/, technical/, educational/, research/, custom/, manifest.json

# T1.2: Verify manifest schema
cat .jerry/patterns/manifest.json | python3 -m json.tool > /dev/null && echo "✅ Valid JSON"

# T1.3: Test sync tool
./adws/jerry_sync_patterns.py --list
# Expected: Lists 200+ patterns from Fabric

# T1.4: Sync patterns
./adws/jerry_sync_patterns.py
# Expected: 24 patterns synced

# T1.5: Verify patterns synced
find .jerry/patterns -name "system.md" | wc -l
# Expected: 24

# T1.6: Run validation
./adws/jerry_validate.py --level 1
# Expected: All checks pass, "24 patterns bundled"
```

### 1.3 Review Criteria
- [ ] `.jerry/patterns/manifest.json` has valid schema
- [ ] 24 patterns synced across 5 categories (7+4+5+3+5)
- [ ] Each pattern has `system.md` file
- [ ] `jerry_sync_patterns.py` has all CLI flags working
- [ ] `jerry_validate.py` includes pattern checks
- [ ] No hardcoded paths remain

### 1.4 On Success
```bash
cd trees/c1d6900b
git add -A
git commit -m "feat(patterns): complete pattern infrastructure implementation

- Add .jerry/patterns/ directory structure
- Create manifest.json with pattern registry
- Implement jerry_sync_patterns.py with full CLI
- Bundle 24 patterns (core:7, youtube:4, technical:5, educational:3, research:5)
- Add pattern validation to jerry_validate.py

ADW: c1d6900b
Phase: 1/5 - Pattern Infrastructure"
```

---

## STEP 2: Phase 2 & 3 - Parallel Execution

### 2.1 Launch Both Builds
```bash
cd /Users/ameno/dev/tac/tac-8

# Start both in parallel
uv run ./adws/adw_build_iso.py local:pattern-executor 4d650f33 &
PID2=$!

uv run ./adws/adw_build_iso.py local:content-extractors 675a4152 &
PID3=$!

# Wait for both
wait $PID2 $PID3
echo "Phase 2 and 3 builds complete"
```

### 2.2 Test Phase 2 (Pattern Executor)
```bash
cd trees/4d650f33

# T2.1: Module exists and imports
python3 -c "from adws.adw_modules.pattern_executor import execute_pattern, execute_patterns_parallel, list_available_patterns; print('✅ Imports OK')"

# T2.2: List patterns function
python3 -c "
from adws.adw_modules.pattern_executor import list_available_patterns
patterns = list_available_patterns()
print(f'✅ Found {patterns.get(\"bundled_patterns_count\", 0)} patterns')
"

# T2.3: Execute single pattern (requires merging Phase 1 first)
# This test requires patterns from Phase 1
python3 -c "
from adws.adw_modules.pattern_executor import execute_pattern
result = execute_pattern('extract_wisdom', 'Sample content for testing the pattern executor.')
print(f'Success: {result.success}')
print(f'Output length: {len(result.output)} chars')
print(f'Execution time: {result.execution_time:.2f}s')
"

# T2.4: Execute parallel patterns
python3 -c "
from adws.adw_modules.pattern_executor import execute_patterns_parallel
results = execute_patterns_parallel(['extract_wisdom', 'extract_insights'], 'Sample content')
print(f'✅ Executed {len(results)} patterns in parallel')
for name, result in results.items():
    print(f'  {name}: {\"✅\" if result.success else \"❌\"} ({result.execution_time:.2f}s)')
"
```

### 2.3 Test Phase 3 (Content Extractors)
```bash
cd trees/675a4152

# T3.1: Module exists and imports
python3 -c "from adws.adw_modules.content_extractors import detect_content_type, extract_content, ContentType; print('✅ Imports OK')"

# T3.2: Content type detection
python3 -c "
from adws.adw_modules.content_extractors import detect_content_type
tests = [
    ('https://youtube.com/watch?v=abc123', 'youtube'),
    ('https://youtu.be/abc123', 'youtube'),
    ('https://example.com/article', 'url'),
    ('/path/to/doc.pdf', 'pdf'),
    ('/path/to/notes.txt', 'text'),
]
for input, expected in tests:
    result = detect_content_type(input)
    status = '✅' if result == expected else '❌'
    print(f'{status} {input[:40]:40} → {result}')
"

# T3.3: YouTube extraction (requires yt-dlp)
which yt-dlp && python3 -c "
from adws.adw_modules.content_extractors import extract_content
# Use a short video for testing
result = extract_content('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
print(f'✅ Type: {result.type}')
print(f'✅ Text length: {len(result.text)} chars')
print(f'✅ Video ID: {result.video_id}')
" || echo "⚠️ yt-dlp not installed, skipping YouTube test"

# T3.4: Text extraction
echo "Sample text content for testing" > /tmp/test.txt
python3 -c "
from adws.adw_modules.content_extractors import extract_content
result = extract_content('/tmp/test.txt')
print(f'✅ Type: {result.type}')
print(f'✅ Text: {result.text[:50]}...')
"
```

### 2.4 Review Criteria Phase 2
- [ ] `pattern_executor.py` exists in `adw_modules/`
- [ ] All functions implemented: `execute_pattern`, `execute_patterns_parallel`, `list_available_patterns`
- [ ] Claude SDK integration working
- [ ] Parallel execution uses ThreadPoolExecutor
- [ ] Error handling for missing patterns

### 2.5 Review Criteria Phase 3
- [ ] All extractor modules exist
- [ ] Content type detection accurate
- [ ] YouTube extraction works (yt-dlp)
- [ ] URL extraction works
- [ ] PDF extraction works
- [ ] Text/stdin extraction works
- [ ] Unified ContentObject returned

### 2.6 On Success (Both Phases)
```bash
# Phase 2
cd trees/4d650f33
git add -A
git commit -m "feat(patterns): implement pattern executor module

- Add pattern_executor.py with Claude SDK integration
- Implement execute_pattern() for single pattern execution
- Implement execute_patterns_parallel() for concurrent execution
- Add pattern discovery and listing functions

ADW: 4d650f33
Phase: 2/5 - Pattern Executor"

# Phase 3
cd trees/675a4152
git add -A
git commit -m "feat(content): implement multi-type content extractors

- Add content_extractors.py main module
- Implement YouTube extraction via yt-dlp
- Implement URL extraction/scraping
- Implement PDF text extraction
- Implement text/stdin handling
- Add unified ContentObject interface

ADW: 675a4152
Phase: 3/5 - Content Extractors"
```

---

## STEP 3: Merge Phase 1 Into Phase 2 & 3

Before Phase 4, ensure Phase 2 and 3 have access to Phase 1's patterns:

```bash
# In Phase 2 worktree
cd trees/4d650f33
git fetch origin feat-issue-pattern-infrastructure-adw-c1d6900b-jerry-patterns-foundation
git merge FETCH_HEAD --no-edit -m "Merge Phase 1 patterns for testing"

# In Phase 3 worktree
cd trees/675a4152
git fetch origin feat-issue-pattern-infrastructure-adw-c1d6900b-jerry-patterns-foundation
git merge FETCH_HEAD --no-edit -m "Merge Phase 1 patterns for testing"
```

---

## STEP 4: Phase 4 - Generic Analysis ADW

### 4.1 Build
```bash
cd /Users/ameno/dev/tac/tac-8
uv run ./adws/adw_build_iso.py local:generic-analysis-adw 85080678
```

### 4.2 Pre-Requisites
Phase 4 requires merging Phase 1, 2, and 3:
```bash
cd trees/85080678

# Merge all dependencies
git fetch origin feat-issue-pattern-infrastructure-adw-c1d6900b-jerry-patterns-foundation
git merge FETCH_HEAD --no-edit

git fetch origin feat-issue-pattern-executor-adw-4d650f33-execute-bundled-patterns
git merge FETCH_HEAD --no-edit

git fetch origin feat-issue-content-extractors-adw-675a4152-multi-type-content-extraction
git merge FETCH_HEAD --no-edit
```

### 4.3 Test Checklist
```bash
cd trees/85080678

# T4.1: ADW script exists
test -f ./adws/adw_analyze_iso.py && echo "✅ ADW script exists"

# T4.2: Script is executable
test -x ./adws/adw_analyze_iso.py && echo "✅ Script is executable"

# T4.3: Help output
./adws/adw_analyze_iso.py --help

# T4.4: Dry run with URL
./adws/adw_analyze_iso.py "https://example.com" --dry-run

# T4.5: Dry run with YouTube
./adws/adw_analyze_iso.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --dry-run

# T4.6: Full test with text input
echo "This is sample content for testing the generic analysis workflow. It should extract wisdom, insights, and recommendations from this text." | ./adws/adw_analyze_iso.py - --patterns extract_wisdom,extract_insights

# T4.7: Verify outputs created
ls agents/*/analyze/patterns/
```

### 4.4 Review Criteria
- [ ] `adw_analyze_iso.py` accepts all input types
- [ ] Content type auto-detection works
- [ ] Pattern selection based on content type
- [ ] Outputs generated in correct directory
- [ ] ANALYSIS_SUMMARY.md created
- [ ] `/analyze` command exists and works

### 4.5 On Success
```bash
cd trees/85080678
git add -A
git commit -m "feat(analyze): implement generic content analysis ADW

- Add adw_analyze_iso.py for unified content analysis
- Support YouTube, URL, PDF, and text inputs
- Auto-detect content type and select patterns
- Generate structured outputs (patterns/, reports)
- Add /analyze slash command

ADW: 85080678
Phase: 4/5 - Generic Analysis ADW"
```

---

## STEP 5: Phase 5 - YouTube Migration

### 5.1 Build
```bash
cd /Users/ameno/dev/tac/tac-8
uv run ./adws/adw_build_iso.py local:youtube-migration b636eeb6
```

### 5.2 Pre-Requisites
```bash
cd trees/b636eeb6

# Merge Phase 4 (includes all dependencies)
git fetch origin feat-issue-generic-analysis-adw-adw-85080678-unified-content-analysis
git merge FETCH_HEAD --no-edit
```

### 5.3 Test Checklist
```bash
cd trees/b636eeb6

# T5.1: Agents exist
ls -la .claude/agents/youtube/
# Expected: metadata-extractor.md, core-analyzer.md, conditional-analyzer.md,
#           report-aggregator.md, audio-summarizer.md, html-generator.md, orchestrator.md

# T5.2: YouTube ADW script exists
test -f ./adws/adw_youtube_iso.py && echo "✅ YouTube ADW exists"

# T5.3: Commands exist
ls .claude/commands/yt_*.md
# Expected: yt_analyze.md, yt_quick.md, yt_full.md, yt_metadata.md

# T5.4: Dry run quick mode
./adws/adw_youtube_iso.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --mode quick --dry-run

# T5.5: Dry run full mode
./adws/adw_youtube_iso.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --mode full --dry-run

# T5.6: Full integration test (quick mode)
./adws/adw_youtube_iso.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mode quick

# T5.7: Verify outputs
ls agents/*/youtube/*/
# Expected: metadata.json, transcript.txt, patterns/, ANALYSIS_SUMMARY.md, etc.

# T5.8: Verify no hardcoded user paths
grep -r "/Users/ameno" .claude/agents/youtube/ adws/adw_youtube_iso.py && echo "❌ Hardcoded paths found" || echo "✅ No hardcoded paths"
```

### 5.4 Review Criteria
- [ ] All YouTube agents migrated
- [ ] Agents use `pattern_executor` not Fabric CLI
- [ ] `adw_youtube_iso.py` works in both modes
- [ ] Output structure matches original
- [ ] No hardcoded user paths
- [ ] TTS is optional (no failure if unavailable)
- [ ] HTML dashboard generated

### 5.5 On Success
```bash
cd trees/b636eeb6
git add -A
git commit -m "feat(youtube): migrate YouTube analyzer to Jerry

- Migrate all YouTube agents to .claude/agents/youtube/
- Update agents to use pattern_executor
- Create adw_youtube_iso.py specialized workflow
- Add yt_* slash commands
- Make TTS optional
- Generate HTML dashboard

ADW: b636eeb6
Phase: 5/5 - YouTube Migration"
```

---

## STEP 6: Documentation Updates

### 6.1 Files to Update

```bash
cd /Users/ameno/dev/tac/tac-8

# Checkout aggregator branch
git checkout feat-jerry-patterns-content-analysis-aggregator
```

### 6.2 README.md Updates

Add to main README.md:

```markdown
## Content Analysis

Jerry includes a powerful content analysis system built on bundled Fabric patterns.

### Quick Start

```bash
# Analyze any content
./adws/adw_analyze_iso.py "https://youtube.com/watch?v=VIDEO_ID"

# Analyze a document
./adws/adw_analyze_iso.py ./document.pdf --patterns analyze_paper

# Analyze URL
./adws/adw_analyze_iso.py "https://example.com/article"

# YouTube-specific analysis
./adws/adw_youtube_iso.py "https://youtube.com/watch?v=VIDEO_ID" --mode full
```

### Pattern System

Jerry bundles 24 curated Fabric patterns:

| Category | Count | Examples |
|----------|-------|----------|
| Core | 7 | extract_wisdom, extract_insights, rate_content |
| YouTube | 4 | youtube_summary, get_wow_per_minute |
| Technical | 5 | extract_technical_content, analyze_code |
| Educational | 3 | extract_educational_value, create_flash_cards |
| Research | 5 | analyze_paper, analyze_claims |

### For Developers

Patterns are synced from Fabric at development time:

```bash
# List available Fabric patterns
./adws/jerry_sync_patterns.py --list

# Sync patterns to Jerry
./adws/jerry_sync_patterns.py
```
```

### 6.3 adws/README.md Updates

Add new workflows to the table and document pattern system.

### 6.4 docs/ARCHITECTURE.md Updates

Add Patterns Layer to architecture documentation.

### 6.5 Create .jerry/patterns/README.md

Comprehensive documentation of the pattern system.

---

## STEP 7: Final Integration Test

```bash
cd /Users/ameno/dev/tac/tac-8
git checkout feat-jerry-patterns-content-analysis-aggregator

# Merge all phase branches
for branch in \
  feat-issue-pattern-infrastructure-adw-c1d6900b-jerry-patterns-foundation \
  feat-issue-pattern-executor-adw-4d650f33-execute-bundled-patterns \
  feat-issue-content-extractors-adw-675a4152-multi-type-content-extraction \
  feat-issue-generic-analysis-adw-adw-85080678-unified-content-analysis \
  feat-issue-youtube-migration-adw-b636eeb6-youtube-analyzer-migration
do
  echo "Merging $branch..."
  git merge origin/$branch --no-ff -m "Merge $branch into aggregator"
done

# Run full validation
./adws/jerry_validate.py --level 1

# Test complete workflow
./adws/adw_youtube_iso.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mode full

# Verify all outputs
echo "=== Final Verification ==="
echo "Patterns: $(find .jerry/patterns -name 'system.md' | wc -l)"
echo "YouTube Agents: $(ls .claude/agents/youtube/*.md | wc -l)"
echo "Analysis Output: $(ls agents/*/youtube/*/ 2>/dev/null | head -1)"
```

---

## STEP 8: Create Final PR

```bash
git push origin feat-jerry-patterns-content-analysis-aggregator

gh pr create \
  --title "feat: Jerry Patterns System + Content Analysis" \
  --body-file - <<'EOF'
## Summary

Implements Jerry's pattern management system and generic content analysis capabilities, making Jerry self-contained without runtime Fabric CLI dependency.

## Changes

### Phase 1: Pattern Infrastructure (c1d6900b)
- `.jerry/patterns/` directory structure
- Pattern manifest with 24 bundled patterns
- `jerry_sync_patterns.py` development tool
- Pattern validation in `jerry_validate.py`

### Phase 2: Pattern Executor (4d650f33)
- `pattern_executor.py` module
- Claude SDK integration for execution
- Parallel pattern execution support

### Phase 3: Content Extractors (675a4152)
- Multi-type content extraction
- YouTube, URL, PDF, text support
- Unified ContentObject interface

### Phase 4: Generic Analysis ADW (85080678)
- `adw_analyze_iso.py` unified workflow
- Auto content type detection
- Pattern selection by content type

### Phase 5: YouTube Migration (b636eeb6)
- YouTube agents in `.claude/agents/youtube/`
- `adw_youtube_iso.py` specialized workflow
- `/yt_*` slash commands

## Testing

- [ ] `./adws/jerry_validate.py --level 1` passes
- [ ] `./adws/jerry_sync_patterns.py --list` shows patterns
- [ ] `./adws/adw_analyze_iso.py "https://example.com"` works
- [ ] `./adws/adw_youtube_iso.py "https://youtube.com/watch?v=VIDEO" --mode quick` works

## How to Use

```bash
# Generic content analysis
./adws/adw_analyze_iso.py "https://youtube.com/watch?v=VIDEO_ID"
./adws/adw_analyze_iso.py ./document.pdf
./adws/adw_analyze_iso.py "https://example.com/article"

# YouTube-specific
./adws/adw_youtube_iso.py "https://youtube.com/watch?v=VIDEO_ID" --mode full
```

## Documentation

- Updated README.md with content analysis section
- Updated adws/README.md with new workflows
- Created .jerry/patterns/README.md
- Updated docs/ARCHITECTURE.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
```

---

## Execution Status

| Phase | ADW ID | Issue | Build | Test | Review | Merged |
|-------|--------|-------|-------|------|--------|--------|
| 1 | c1d6900b | pattern-infrastructure | ⏳ | ⏳ | ⏳ | ⏳ |
| 2 | 4d650f33 | pattern-executor | ⏳ | ⏳ | ⏳ | ⏳ |
| 3 | 675a4152 | content-extractors | ⏳ | ⏳ | ⏳ | ⏳ |
| 4 | 85080678 | generic-analysis-adw | ⏳ | ⏳ | ⏳ | ⏳ |
| 5 | b636eeb6 | youtube-migration | ⏳ | ⏳ | ⏳ | ⏳ |

**Legend**: ⏳ Pending | 🔄 In Progress | ✅ Complete | ❌ Failed

---

## Files Created/Modified Summary

### New Files
- `.jerry/patterns/manifest.json`
- `.jerry/patterns/*/system.md` (24 patterns)
- `.jerry/patterns/README.md`
- `adws/jerry_sync_patterns.py`
- `adws/adw_modules/pattern_executor.py`
- `adws/adw_modules/content_extractors.py`
- `adws/adw_modules/youtube_ops.py`
- `adws/adw_modules/web_ops.py`
- `adws/adw_modules/pdf_ops.py`
- `adws/adw_modules/text_ops.py`
- `adws/adw_analyze_iso.py`
- `adws/adw_youtube_iso.py`
- `.claude/agents/youtube/*.md` (7 agents)
- `.claude/commands/yt_*.md` (4 commands)
- `.claude/commands/analyze.md`
- `.claude/agents/feature-orchestrator.md`

### Modified Files
- `README.md`
- `adws/README.md`
- `adws/jerry_validate.py`
- `.jerry/manifest.json`
- `docs/ARCHITECTURE.md`

---

## Aggregator Branch

Branch: `feat-jerry-patterns-content-analysis-aggregator`
GitHub: https://github.com/ameno-/jerry/tree/feat-jerry-patterns-content-analysis-aggregator

## Related Issues

- Parent: `issues/issue-jerry-patterns-content-analysis.md`
- Phase 1: `issues/issue-pattern-infrastructure.md`
- Phase 2: `issues/issue-pattern-executor.md`
- Phase 3: `issues/issue-content-extractors.md`
- Phase 4: `issues/issue-generic-analysis-adw.md`
- Phase 5: `issues/issue-youtube-migration.md`
