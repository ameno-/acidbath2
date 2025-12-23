# Feature: Code Block Extraction and Repository Organization

## Metadata
adw_id: `40d4951f`
prompt: `The blog is currently suffering from a problem where long code blocks are affecting overall readability. The formatting of those code blocks will be handled separately but we need to work on maintaining the integrity of those code blocks and uploading all code blocks and all examples in an organized fashion into this brand new repository that I've created https://github.com/ameno-/acidbath-code

Work on a plan to review all code used in blog posts and extract complete working code. Upload that working code in an organized fashion to this GitHub repository

Use parallel workflows effectively to handle moving codeblocks over to the new codebase create a new skill that handles the documentation organization. As blog posts change, as new posts are made, posts are deleted, we must make sure that documentation of code blocks in this repo is implemented correctly. This will be part of the review process`

## Feature Description

This feature extracts all code blocks from ACIDBATH blog posts into a separate GitHub repository (acidbath-code) while maintaining code integrity and establishing automation for ongoing synchronization. The system will:

1. Parse all blog posts and extract code blocks with context
2. Organize extracted code in a logical structure in the acidbath-code repository
3. Replace long code blocks in blog posts with references to the repository
4. Create automation workflows to keep code blocks synchronized as posts change
5. Integrate code block validation into the review process

The goal is to improve blog readability while maintaining the "POC Rule" (working, copy-paste code) by hosting complete examples in a dedicated repository.

## User Story

As a **blog reader**
I want to **access complete, working code examples from blog posts without scrolling through long embedded code blocks**
So that **I can quickly understand concepts in the post and access full working code when needed**

As a **blog author**
I want to **maintain code examples in a separate repository that automatically syncs with blog posts**
So that **code stays up-to-date, blog posts remain readable, and the POC rule is maintained**

## Problem Statement

ACIDBATH blog posts currently embed long code blocks directly in markdown, which:

1. **Reduces readability** - Long code blocks (50+ lines) disrupt the reading flow
2. **Maintenance burden** - Code duplicated across posts becomes stale
3. **No validation** - Code blocks aren't tested or validated for correctness
4. **Poor organization** - No centralized location for reusable code examples
5. **Synchronization drift** - When code is updated, blog posts may reference outdated versions

The blog's "POC Rule" (working, copy-paste code) is at risk when code blocks are too long to embed effectively, yet too important to omit.

## Solution Statement

Build a **Code Block Extraction and Synchronization System** that:

1. **Extraction Pipeline**:
   - Parse all blog posts and identify code blocks with language tags
   - Extract code blocks with context (post title, section, purpose)
   - Categorize code as: complete examples, snippets, configuration, or illustrations
   - Create organized directory structure in acidbath-code repo

2. **Repository Organization**:
   - Structure: `acidbath-code/{category}/{post-slug}/{example-name}/`
   - Include README per example explaining context and usage
   - Add testing/validation where applicable (Python scripts, configs)
   - Maintain mapping manifest between blog posts and code locations

3. **Blog Post Transformation**:
   - Keep essential snippets (< 20 lines) inline for context
   - Replace long code blocks with references to repository
   - Add "Complete Example" callouts with GitHub links
   - Maintain the POC rule by linking to runnable code

4. **Automation & Synchronization**:
   - Create `/sync-code-blocks` skill for blog post updates
   - Add pre-commit hook to validate code block references
   - Build `/extract-code` command for new posts
   - Integrate into `/review` and `/new-post` workflows

5. **Validation & Review**:
   - Code blocks in Python are syntax-validated
   - Bash scripts are shellcheck-validated
   - JSON/YAML configs are schema-validated
   - Links to acidbath-code are verified during build

## Relevant Files

### Blog Posts (Source)
- `/Users/ameno/dev/acidbath2/trees/40d4951f/src/content/blog/*.md` - All published blog posts containing code blocks to extract
  - Most code-heavy posts (by code block count):
    - `directory-watchers.md` (54 code blocks)
    - `claude-skills-deep-dive.md` (54 code blocks)
    - `agent-architecture.md` (52 code blocks)
    - `document-generation-skills.md` (38 code blocks)

### Existing ADWs & Modules
- `/Users/ameno/dev/acidbath2/trees/40d4951f/adws/adw_modules/agent.py` - Agent execution module for creating extraction agents
- `/Users/ameno/dev/acidbath2/trees/40d4951f/adws/adw_modules/workflow_ops.py` - Workflow orchestration utilities
- `/Users/ameno/dev/acidbath2/trees/40d4951f/adws/adw_analyze_iso.py` - Pattern-based analysis workflow (reference for structure)

### Commands & Skills
- `/Users/ameno/dev/acidbath2/trees/40d4951f/.claude/commands/new-post.md` - Blog post creation command (extend with code extraction)
- `/Users/ameno/dev/acidbath2/trees/40d4951f/.claude/commands/review.md` - Review command (add code block validation)
- `/Users/ameno/dev/acidbath2/trees/40d4951f/.claude/commands/ai-audit.md` - Content audit (add code block checks)

### Configuration
- `/Users/ameno/dev/acidbath2/trees/40d4951f/README.md` - Project documentation (update with code repository references)
- `/Users/ameno/dev/acidbath2/trees/40d4951f/ai_docs/content_strategy.md` - Content strategy (update with code organization approach)

### New Files

#### Scripts & Workflows
- `/Users/ameno/dev/acidbath2/trees/40d4951f/adws/adw_extract_code_blocks.py` - Main code extraction workflow script
- `/Users/ameno/dev/acidbath2/trees/40d4951f/adws/adw_sync_code_repo.py` - Synchronization workflow for acidbath-code repository
- `/Users/ameno/dev/acidbath2/trees/40d4951f/adws/adw_modules/code_extraction.py` - Code block parsing and extraction utilities
- `/Users/ameno/dev/acidbath2/trees/40d4951f/adws/adw_modules/code_validator.py` - Code validation utilities (syntax check, linting)

#### Skills & Commands
- `/Users/ameno/dev/acidbath2/trees/40d4951f/.claude/commands/extract-code.md` - Extract code blocks from a blog post
- `/Users/ameno/dev/acidbath2/trees/40d4951f/.claude/commands/sync-code-blocks.md` - Synchronize code blocks between blog and repository
- `/Users/ameno/dev/acidbath2/trees/40d4951f/.claude/skills/code-block-manager/SKILL.md` - Comprehensive code block management skill

#### Configuration & Manifests
- `/Users/ameno/dev/acidbath2/trees/40d4951f/code-blocks-manifest.json` - Mapping of blog posts to code repository locations
- `/Users/ameno/dev/acidbath2/trees/40d4951f/.claude/code-block-config.yaml` - Configuration for code extraction rules

#### Documentation
- `/Users/ameno/dev/acidbath2/trees/40d4951f/ai_docs/code-repository-integration.md` - Guide for code repository integration
- `/Users/ameno/dev/acidbath2/trees/40d4951f/specs/code-block-organization-schema.md` - Schema definition for repository organization

#### acidbath-code Repository (External)
- `acidbath-code/README.md` - Repository overview and usage guide
- `acidbath-code/examples/{category}/{post-slug}/{example-name}/` - Organized code structure
- `acidbath-code/.github/workflows/validate-code.yml` - CI workflow for code validation
- `acidbath-code/scripts/validate-all.py` - Validation script for all code examples

## Implementation Plan

### Phase 1: Foundation & Analysis
**Goal**: Understand current state, design repository structure, and build extraction utilities

1. **Audit existing code blocks**
   - Scan all blog posts and categorize code blocks by language
   - Identify complete examples vs. snippets vs. configuration
   - Measure code block lengths and determine inline vs. external threshold
   - Document code block patterns (mermaid diagrams, bash, python, yaml, markdown, etc.)

2. **Design repository organization schema**
   - Define directory structure for acidbath-code repository
   - Create taxonomy: categories (agentic-patterns, production-patterns, tools, configs)
   - Design README template for code examples
   - Define manifest schema for blog-to-code mapping

3. **Build core extraction utilities**
   - Create code block parser (markdown → structured data)
   - Build code categorization logic (language detection, size thresholds)
   - Implement context extraction (surrounding headings, descriptions)
   - Create validation functions (syntax checking per language)

### Phase 2: Core Implementation
**Goal**: Extract code from existing posts and populate acidbath-code repository

1. **Initialize acidbath-code repository**
   - Clone and set up local repository
   - Create directory structure based on schema
   - Add root README with usage instructions
   - Set up validation workflows (GitHub Actions)

2. **Extract code blocks from all blog posts**
   - Process each blog post through extraction pipeline
   - Generate structured code examples with README files
   - Create manifest mapping blog posts to code locations
   - Commit organized code to acidbath-code repository

3. **Transform blog posts with references**
   - Replace long code blocks (>20 lines) with references
   - Add callout boxes linking to full examples
   - Maintain essential snippets inline for context
   - Generate before/after comparison for review

4. **Build validation system**
   - Implement Python syntax validation
   - Add shellcheck for bash scripts
   - Create JSON/YAML schema validation
   - Build link checker for code repository references

### Phase 3: Integration & Automation
**Goal**: Automate code synchronization and integrate into existing workflows

1. **Create code block management skills**
   - `/extract-code` - Extract code from new/updated posts
   - `/sync-code-blocks` - Synchronize blog and repository
   - `/validate-code-refs` - Verify all code references are valid

2. **Integrate into existing workflows**
   - Update `/new-post` to automatically extract code blocks
   - Extend `/review` to validate code block references
   - Enhance `/ai-audit` to check code organization compliance
   - Add pre-commit hooks for code block validation

3. **Build monitoring & maintenance**
   - Create dashboard showing code block statistics
   - Add alerts for broken code references
   - Build report generation for code coverage
   - Implement automated testing for extracted code examples

## Step by Step Tasks

### Group A: Foundation & Research [parallel: false, model: sonnet]
Sequential analysis and design work that establishes the foundation.

#### Step A.1: Audit Blog Posts and Code Blocks
- Scan all markdown files in `src/content/blog/`
- Extract metadata for each code block: language, line count, file location, section context
- Categorize code blocks: complete examples (>40 lines), snippets (<20 lines), configs, diagrams
- Generate audit report with statistics and recommendations
- Output: `specs/code-block-audit-report.md`

#### Step A.2: Design Repository Organization Schema
- Define category taxonomy (agentic-patterns, production-patterns, workflow-tools, configurations)
- Design directory structure: `{category}/{post-slug}/{example-name}/`
- Create README template for code examples with metadata (post reference, usage, requirements)
- Define manifest schema for mapping blog posts to code locations (JSON schema)
- Output: `specs/code-block-organization-schema.md`

#### Step A.3: Design Code Reference Format
- Define inline vs. external code block thresholds (≤20 lines inline, >20 external)
- Create callout box design for "Complete Example" references
- Design URL structure for code repository links
- Create before/after examples for blog post transformation
- Output: `specs/code-reference-format-spec.md`

### Group B: Core Utilities & Repository Setup [parallel: true, depends: A, model: sonnet]
Independent infrastructure work that can be built in parallel.

#### Step B.1: Build Code Extraction Utilities
- Create `adws/adw_modules/code_extraction.py`:
  - `parse_code_blocks()` - Extract code blocks from markdown with context
  - `categorize_code_block()` - Determine category based on content and metadata
  - `extract_context()` - Get surrounding headings and descriptions
  - `generate_example_readme()` - Create README for code example
- Add unit tests for extraction functions
- Output: Working extraction utilities module

#### Step B.2: Build Code Validation Utilities
- Create `adws/adw_modules/code_validator.py`:
  - `validate_python()` - Syntax check with `ast.parse()`
  - `validate_bash()` - Shellcheck validation
  - `validate_json_yaml()` - Schema validation
  - `validate_code_reference()` - Verify GitHub links are valid
- Add validation tests with sample code blocks
- Output: Working validation utilities module

#### Step B.3: Initialize acidbath-code Repository
- Clone `https://github.com/ameno-/acidbath-code` locally
- Create directory structure based on schema from Step A.2
- Add root README explaining repository purpose and organization
- Create `.github/workflows/validate-code.yml` for CI validation
- Create `scripts/validate-all.py` for local validation
- Initial commit and push to remote
- Output: Initialized and structured acidbath-code repository

### Group C: Extraction Pipeline [parallel: false, depends: B, model: auto]
Sequential extraction and transformation work.

#### Step C.1: Create Code Extraction Workflow
- Create `adws/adw_extract_code_blocks.py`:
  - Parse target blog post markdown
  - Extract all code blocks with context
  - Categorize each code block
  - Generate structured output to acidbath-code repository
  - Create manifest entry mapping post to code locations
  - Commit code to acidbath-code repository
- Add CLI interface with arguments: `--post`, `--dry-run`, `--category`
- Output: Working extraction workflow script

#### Step C.2: Extract Code from All Blog Posts
- Run extraction workflow on each blog post:
  - `directory-watchers.md` (54 code blocks)
  - `claude-skills-deep-dive.md` (54 code blocks)
  - `agent-architecture.md` (52 code blocks)
  - `document-generation-skills.md` (38 code blocks)
  - `single-file-scripts.md` (36 code blocks)
  - `context-engineering.md` (28 code blocks)
  - `workflow-prompts.md` (16 code blocks)
- Validate all extracted code with validation utilities
- Generate `code-blocks-manifest.json` mapping
- Commit all code to acidbath-code repository
- Output: Populated acidbath-code repository with all blog code

#### Step C.3: Transform Blog Posts with References
- For each blog post, replace code blocks >20 lines with references:
  - Keep essential snippets (≤20 lines) inline
  - Replace long code blocks with callout boxes
  - Add GitHub links to complete examples
  - Maintain POC rule by ensuring code is accessible
- Create before/after diff for review
- Update blog posts in `src/content/blog/`
- Output: Transformed blog posts with code references

### Group D: Skills & Commands [parallel: true, depends: C, model: sonnet]
Independent command and skill creation.

#### Step D.1: Create Extract Code Command
- Create `.claude/commands/extract-code.md`:
  - Parse blog post path argument
  - Run code extraction workflow
  - Commit extracted code to acidbath-code repository
  - Update manifest mapping
  - Report extraction statistics
- Test command on sample post
- Output: `/extract-code` command

#### Step D.2: Create Sync Code Blocks Command
- Create `.claude/commands/sync-code-blocks.md`:
  - Compare blog posts with acidbath-code repository
  - Detect code block changes since last sync
  - Update acidbath-code repository with changes
  - Update blog post references if needed
  - Report sync status
- Test command with modified post
- Output: `/sync-code-blocks` command

#### Step D.3: Create Code Block Manager Skill
- Create `.claude/skills/code-block-manager/SKILL.md`:
  - Comprehensive skill combining extraction, sync, and validation
  - Multi-step workflow for code block management
  - Integration with review and audit processes
  - Documentation of code organization patterns
- Test skill end-to-end
- Output: Code block manager skill

### Group E: Integration & Validation [parallel: false, depends: D, model: opus]
Sequential integration requiring heavy reasoning about workflow interactions.

#### Step E.1: Integrate into New Post Workflow
- Update `.claude/commands/new-post.md`:
  - Add code extraction step after post creation
  - Automatically categorize and extract code blocks
  - Generate manifest entry for new post
  - Validate extracted code before committing
- Test on new sample post creation
- Output: Enhanced `/new-post` command

#### Step E.2: Integrate into Review Workflow
- Update `.claude/commands/review.md`:
  - Add code block validation checks
  - Verify code repository references are valid
  - Check for code blocks exceeding inline threshold
  - Validate manifest is up-to-date
- Test on blog post with code changes
- Output: Enhanced `/review` command

#### Step E.3: Integrate into AI Audit Workflow
- Update `.claude/commands/ai-audit.md`:
  - Add code organization compliance check
  - Verify POC rule is maintained (all code is accessible)
  - Check for broken code references
  - Validate code examples have proper context
- Test on sample blog post
- Output: Enhanced `/ai-audit` command

#### Step E.4: Add Pre-commit Validation Hooks
- Create `.git/hooks/pre-commit` (or git hook config):
  - Run code reference validator
  - Check manifest consistency
  - Validate no large code blocks in blog posts
  - Run code syntax validation
- Test hook with sample commit
- Output: Working pre-commit hook

### Group F: Documentation & Finalization [parallel: false, depends: E, model: sonnet]
Sequential documentation and cleanup work.

#### Step F.1: Create Integration Documentation
- Create `ai_docs/code-repository-integration.md`:
  - Explain acidbath-code repository purpose and structure
  - Document code extraction workflow
  - Provide examples of using `/extract-code` and `/sync-code-blocks`
  - Explain code reference format in blog posts
  - Include troubleshooting guide
- Output: Complete integration guide

#### Step F.2: Update Project Documentation
- Update `README.md`:
  - Add section on code repository integration
  - Document new commands and skills
  - Explain code organization approach
- Update `ai_docs/content_strategy.md`:
  - Add code block organization strategy
  - Update POC rule implementation details
- Output: Updated project documentation

#### Step F.3: Create Migration Report
- Generate comprehensive migration report:
  - Statistics: total code blocks extracted, blog posts transformed
  - Before/after comparison for each blog post
  - List of all code examples in acidbath-code repository
  - Validation results for all extracted code
  - Links to all updated workflows and commands
- Output: `specs/code-block-migration-report.md`

## Testing Strategy

### Unit Tests

1. **Code Extraction Utilities**:
   - Test code block parsing with various markdown formats
   - Test categorization logic with sample code blocks
   - Test context extraction from different post structures
   - Test README generation with various metadata

2. **Code Validation Utilities**:
   - Test Python syntax validation with valid/invalid code
   - Test bash validation with shellcheck integration
   - Test JSON/YAML validation with schema checking
   - Test link validation with mock HTTP responses

3. **Workflow Scripts**:
   - Test extraction workflow with sample blog post
   - Test sync workflow with modified code blocks
   - Test manifest generation and updates
   - Test repository commit operations

### Integration Tests

1. **End-to-End Extraction**:
   - Extract code from complete blog post
   - Verify code in acidbath-code repository
   - Validate blog post transformation
   - Check manifest accuracy

2. **Command Integration**:
   - Test `/extract-code` on new blog post
   - Test `/sync-code-blocks` after post modification
   - Test `/new-post` with automatic code extraction
   - Test `/review` with code validation

3. **Repository Validation**:
   - Run GitHub Actions validation workflow
   - Execute local validation script
   - Verify all code examples have READMEs
   - Check all blog references resolve correctly

### Edge Cases

1. **Code Block Variations**:
   - Code blocks without language tags
   - Nested code blocks within lists
   - Code blocks with special characters
   - Very long code blocks (>200 lines)
   - Mermaid diagrams and non-executable "code"

2. **Blog Post Edge Cases**:
   - Posts with no code blocks
   - Posts with only inline snippets
   - Posts with multiple examples of same language
   - Archived posts (should they be extracted?)

3. **Repository Edge Cases**:
   - Duplicate example names (add conflict resolution)
   - Code block modifications (version handling)
   - Deleted blog posts (cleanup code repository?)
   - Repository unavailable (graceful degradation)

4. **Synchronization Edge Cases**:
   - Code modified in both blog and repository
   - Manifest out of sync with reality
   - Code repository commit failures
   - Blog post reference link rot

## Acceptance Criteria

1. **Code Extraction**:
   - ✅ All code blocks from 7 blog posts extracted to acidbath-code repository
   - ✅ Code organized in logical directory structure matching schema
   - ✅ Each code example has README with context and usage instructions
   - ✅ Manifest correctly maps all blog posts to code locations

2. **Blog Post Transformation**:
   - ✅ Long code blocks (>20 lines) replaced with references in all posts
   - ✅ Essential snippets (≤20 lines) remain inline for context
   - ✅ Callout boxes link to complete examples in acidbath-code
   - ✅ All code repository links are valid and functional
   - ✅ POC rule maintained: all code is accessible with one click

3. **Code Validation**:
   - ✅ All Python code passes syntax validation
   - ✅ All bash scripts pass shellcheck validation
   - ✅ All JSON/YAML passes schema validation
   - ✅ GitHub Actions validation workflow passes on acidbath-code

4. **Automation & Integration**:
   - ✅ `/extract-code` command successfully extracts from new posts
   - ✅ `/sync-code-blocks` command synchronizes changes correctly
   - ✅ `/new-post` automatically extracts and organizes code
   - ✅ `/review` validates code references and organization
   - ✅ `/ai-audit` checks code organization compliance

5. **Documentation**:
   - ✅ Integration guide explains entire code organization system
   - ✅ README updated with code repository information
   - ✅ Migration report documents all changes and statistics
   - ✅ acidbath-code README provides clear usage instructions

6. **Repository Health**:
   - ✅ acidbath-code repository has clear, logical structure
   - ✅ All code examples are tested and validated
   - ✅ READMEs provide sufficient context for each example
   - ✅ CI/CD validates code on every commit

## Validation Commands

Execute these commands to validate the feature is complete:

### 1. Code Extraction Validation
```bash
# Verify extraction utilities work
uv run python -m pytest adws/adw_modules/test_code_extraction.py -v

# Run code extraction on sample post
uv run ./adws/adw_extract_code_blocks.py --post src/content/blog/workflow-prompts.md --dry-run

# Verify manifest is valid JSON
python -m json.tool code-blocks-manifest.json > /dev/null && echo "Manifest is valid JSON"
```

### 2. Code Validation
```bash
# Validate all Python code in acidbath-code repository
uv run python -m py_compile acidbath-code/examples/**/*.py

# Validate bash scripts with shellcheck
find acidbath-code -name "*.sh" -exec shellcheck {} \;

# Run full validation suite
cd acidbath-code && uv run python scripts/validate-all.py
```

### 3. Blog Post Transformation Validation
```bash
# Check for long code blocks remaining in blog posts (should be zero or minimal)
for post in src/content/blog/*.md; do
  echo "Checking $post..."
  awk '/^```/{flag=!flag; lines=0; next} flag{lines++} !flag && lines>20{print FILENAME": Found code block with "lines" lines"; exit 1}' "$post"
done

# Verify all code references resolve
node scripts/validate-code-refs.js

# Build blog and check for broken links
npm run build && npx playwright test
```

### 4. Command & Skill Validation
```bash
# Test extract-code command
claude /extract-code src/content/blog/single-file-scripts.md

# Test sync-code-blocks command
claude /sync-code-blocks

# Verify commands are registered
ls -la .claude/commands/ | grep -E "(extract-code|sync-code-blocks)"
```

### 5. Integration Validation
```bash
# Test new-post with code extraction
claude /new-post "Test Post with Code Examples"

# Test review with code validation
claude /review

# Test ai-audit with code checks
claude /ai-audit src/content/blog/workflow-prompts.md
```

### 6. Repository Health Check
```bash
# Check acidbath-code structure
cd acidbath-code && tree -L 3

# Verify GitHub Actions workflow exists
cat acidbath-code/.github/workflows/validate-code.yml

# Count extracted code examples
find acidbath-code/examples -type f -name "*.py" -o -name "*.sh" -o -name "*.js" | wc -l

# Verify all examples have READMEs
find acidbath-code/examples -type d -mindepth 3 -maxdepth 3 | while read dir; do
  if [ ! -f "$dir/README.md" ]; then
    echo "Missing README in $dir"
  fi
done
```

### 7. End-to-End Validation
```bash
# Full validation sequence
echo "1. Extract code from all posts..."
uv run ./adws/adw_extract_code_blocks.py --all

echo "2. Validate all extracted code..."
cd acidbath-code && uv run python scripts/validate-all.py

echo "3. Build blog and test..."
cd ../.. && npm run build && npm run test

echo "4. Verify manifest integrity..."
python -c "import json; manifest = json.load(open('code-blocks-manifest.json')); print(f'Mapped {len(manifest)} posts to code repository')"

echo "5. Generate migration report..."
uv run ./adws/adw_extract_code_blocks.py --report > specs/code-block-migration-report.md

echo "✅ All validation checks complete"
```

## Notes

### Implementation Priorities

1. **Start with high-value posts**: Focus on the 4 posts with 50+ code blocks first (directory-watchers, claude-skills-deep-dive, agent-architecture, document-generation-skills)

2. **Incremental rollout**: Extract and transform posts one at a time to validate the approach before bulk processing

3. **Preserve git history**: Ensure blog post transformations are committed with clear messages referencing code extraction

### Technical Decisions

1. **Inline threshold**: 20 lines chosen as a balance between context and readability. Can be adjusted based on post layout.

2. **Repository structure**: Organize by category + post slug to maintain clear lineage and support multiple examples per post

3. **Validation approach**: Syntax validation only (no execution) to avoid security concerns and dependency management complexity

4. **Synchronization strategy**: Manual sync via `/sync-code-blocks` command initially. Can automate via GitHub Actions later if needed.

### Future Enhancements

1. **Automated testing**: Run extracted code in isolated environments to verify functionality
2. **Version management**: Track code example versions and link blog posts to specific versions
3. **Interactive examples**: Add Replit/CodeSandbox embeds for web-based code exploration
4. **Code search**: Build search index for code examples across all posts
5. **Usage analytics**: Track which code examples are accessed most frequently
6. **Bi-directional sync**: Support updating blog posts when code repository is modified
7. **Multi-language support**: Extend validation to more languages (Go, Rust, TypeScript, etc.)

### Dependencies

**New Python packages** (add via `uv add`):
- `pyyaml` - For YAML configuration parsing
- `shellcheck-py` - Python wrapper for shellcheck
- `jsonschema` - For JSON schema validation
- `pygments` - For syntax highlighting and language detection
- `pytest` - For testing extraction and validation utilities

**External tools**:
- `shellcheck` - Bash script validation (system package)
- `gh` CLI - For GitHub repository operations
- Git - For repository cloning and commits

### Risk Assessment

**Medium Risk**: Blog post readability impact
- Mitigation: Validate transformed posts with sample readers, ensure callouts are clear and visually distinct

**Low Risk**: Code repository availability
- Mitigation: Graceful degradation if acidbath-code is unavailable, cache locally

**Low Risk**: Manifest synchronization drift
- Mitigation: Add validation step in CI to verify manifest consistency

**Low Risk**: Code example staleness
- Mitigation: Regular reviews of code examples, versioning strategy for major changes
