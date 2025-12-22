# Jerry Patterns System

## Overview

Jerry bundles curated [Fabric](https://github.com/danielmiessler/fabric) patterns as part of its framework, enabling powerful content analysis capabilities without requiring users to install Fabric separately. Patterns are development-time assets synced from Fabric and committed to Jerry's repository, versioned and distributed as part of the framework.

This infrastructure provides the foundation for Jerry's content analysis capabilities, including YouTube video analysis, technical content extraction, and research synthesis.

## Directory Structure

```
.jerry/patterns/
├── manifest.json          # Pattern registry and metadata
├── README.md             # This file
├── core/                 # Core analysis patterns (7)
├── youtube/              # YouTube-specific patterns (4)
├── technical/            # Technical content patterns (5)
├── educational/          # Educational patterns (3)
├── research/             # Research patterns (5)
└── custom/               # User custom patterns (extensible)
```

Each pattern is organized in its own directory:

```
.jerry/patterns/{category}/{pattern_name}/
├── system.md      # Pattern system prompt (required)
├── user.md        # Pattern user prompt template (optional)
└── meta.json      # Pattern metadata
```

## Categories

### Core (7 patterns)
Fundamental content analysis applicable to any content type. Extract universal insights, wisdom, recommendations, and summaries.

**Patterns:**
- `extract_wisdom` - Extract key insights and wisdom
- `extract_insights` - Extract actionable insights
- `extract_recommendations` - Extract recommendations
- `rate_content` - Rate content quality
- `create_summary` - Create comprehensive summary
- `create_5_sentence_summary` - Create concise 5-sentence summary
- `extract_references` - Extract references and citations

### YouTube (4 patterns)
Specialized for YouTube video content analysis. Extract metadata, generate summaries, calculate engagement metrics.

**Patterns:**
- `youtube_summary` - Summarize YouTube videos
- `extract_youtube_metadata` - Extract video metadata
- `get_wow_per_minute` - Calculate engagement metrics
- `extract_agent_opportunities` - Identify automation opportunities

### Technical (5 patterns)
Analysis of technical content including code, infrastructure, and operational data.

**Patterns:**
- `extract_technical_content` - Extract technical details
- `analyze_code` - Analyze code quality
- `extract_poc` - Extract proof of concept
- `analyze_terraform_plan` - Analyze Terraform plans
- `analyze_logs` - Analyze log files

### Educational (3 patterns)
Extract learning value and create educational artifacts from content.

**Patterns:**
- `extract_educational_value` - Extract learning value
- `create_knowledge_artifacts` - Create knowledge artifacts
- `create_flash_cards` - Generate flash cards

### Research (5 patterns)
Academic and professional research analysis. Analyze papers, claims, security reports, patents.

**Patterns:**
- `analyze_paper` - Analyze research papers
- `analyze_claims` - Analyze claims and evidence
- `analyze_threat_report` - Analyze security threats
- `analyze_patent` - Analyze patent documents
- `extract_article_wisdom` - Extract article insights

### Custom (0 patterns initially)
Reserved for user-contributed or project-specific patterns. Allows extensibility without modifying Jerry's core patterns.

## Sync Process

Patterns are synced from a local Fabric installation during development using the `jerry_sync_patterns.py` tool.

### Prerequisites

1. Install Fabric CLI:
   ```bash
   brew install fabric
   # or from https://github.com/danielmiessler/fabric
   ```

2. Fabric patterns are expected at: `~/.config/fabric/patterns/`

### Sync Commands

**List available Fabric patterns:**
```bash
./adws/jerry_sync_patterns.py --list
```

**Sync all bundled patterns:**
```bash
./adws/jerry_sync_patterns.py
```

**Sync specific category:**
```bash
./adws/jerry_sync_patterns.py --category youtube
```

**Sync specific pattern:**
```bash
./adws/jerry_sync_patterns.py --pattern extract_wisdom
```

**Preview changes (dry run):**
```bash
./adws/jerry_sync_patterns.py --dry-run
```

### Sync Behavior

- **Incremental sync**: Only changed patterns are updated (based on file checksums)
- **Manifest updates**: Automatically updates `.jerry/patterns/manifest.json` with metadata
- **Version tracking**: Records Fabric version and sync timestamp
- **File preservation**: Existing patterns are not removed, only updated or added

### What Gets Synced

From each Fabric pattern directory, the sync tool copies:
- `system.md` (required) - System prompt for the pattern
- `user.md` (optional) - User prompt template (if exists)

And generates:
- `meta.json` - Pattern metadata (name, category, source, timestamp, checksum)

## Manifest Schema

The `manifest.json` file tracks all pattern metadata:

```json
{
  "version": "1.0.0",
  "last_synced": "2025-12-15T20:27:00Z",
  "fabric_version": "1.4.0",
  "source_patterns_count": 231,
  "bundled_patterns_count": 24,
  "categories": {
    "core": {
      "count": 7,
      "patterns": ["extract_wisdom", "extract_insights", ...]
    }
  },
  "patterns": {
    "extract_wisdom": {
      "name": "extract_wisdom",
      "category": "core",
      "description": "Extract key insights and wisdom",
      "fabric_source": "~/.config/fabric/patterns/extract_wisdom",
      "synced_at": "2025-12-15T20:30:00Z",
      "files": ["system.md", "user.md"],
      "checksum": "sha256:abc123..."
    }
  }
}
```

## Usage (Future Implementation)

Pattern execution capabilities will be implemented in Phase 2. The planned interface:

```bash
# Execute pattern on content
./adws/jerry_run_pattern.py --pattern extract_wisdom --input content.txt

# Chain patterns (output of one → input of another)
./adws/jerry_run_pattern.py --chain extract_wisdom,create_summary --input video_transcript.txt
```

## Contributing Custom Patterns

Custom patterns can be added to the `custom/` directory for project-specific analysis needs.

### Custom Pattern Structure

Create a directory in `.jerry/patterns/custom/{pattern_name}/`:

```
.jerry/patterns/custom/my_pattern/
├── system.md      # Your system prompt
├── user.md        # (Optional) User prompt template
└── meta.json      # Pattern metadata
```

### Custom Pattern Metadata

Create `meta.json`:

```json
{
  "name": "my_pattern",
  "category": "custom",
  "description": "Description of what this pattern does",
  "author": "Your Name",
  "created_at": "2025-12-15T20:00:00Z",
  "version": "1.0.0"
}
```

### Guidelines

1. **Clear prompts**: Write clear, specific system prompts that define the pattern's behavior
2. **Focused scope**: Each pattern should do one thing well
3. **Output structure**: Define expected output format in the system prompt
4. **Test thoroughly**: Validate pattern outputs with sample content
5. **Document**: Explain pattern purpose and usage in meta.json

## Validation

Pattern integrity is validated as part of Jerry's validation system:

```bash
./adws/jerry_validate.py --level 1
```

Validation checks:
- Manifest exists and has valid JSON syntax
- All patterns in manifest have corresponding directories
- Each pattern has required `system.md` file
- Category counts match actual pattern counts
- No orphaned pattern directories (not in manifest)

## Version Compatibility

The pattern system uses semantic versioning:
- **Major version**: Breaking changes to manifest schema or sync tool
- **Minor version**: New pattern categories or sync features
- **Patch version**: Pattern updates, bug fixes

Current version: **1.0.0**

### Fabric Version Tracking

The manifest records the Fabric version used as the source. If Fabric updates with breaking changes to pattern formats, re-sync and validate:

```bash
./adws/jerry_sync_patterns.py
./adws/jerry_validate.py --level 1
```

## Troubleshooting

### Fabric Not Found

**Error**: "Fabric not found at ~/.config/fabric/patterns/"

**Solution**: Install Fabric CLI:
```bash
brew install fabric
# or from https://github.com/danielmiessler/fabric
```

### Pattern Not Found

**Error**: "Pattern 'xyz' not found in Fabric installation"

**Solution**: List available patterns and verify name:
```bash
./adws/jerry_sync_patterns.py --list
```

### Corrupted Manifest

**Error**: "Manifest JSON is corrupted"

**Solution**: Backup current manifest and rebuild:
```bash
mv .jerry/patterns/manifest.json .jerry/patterns/manifest.json.backup
./adws/jerry_sync_patterns.py  # Rebuilds manifest
```

### Git Tracking Issues

**Error**: "Patterns directory not tracked by git"

**Solution**: Ensure `.jerry/patterns/` is not in `.gitignore`:
```bash
git check-ignore .jerry/patterns/
# Should return nothing (not ignored)
```

## Future Roadmap

### Phase 2 - Pattern Execution
- `jerry_run_pattern.py` tool for executing patterns on content
- Integration with Claude Code agent system
- Pattern chaining (output of one → input of another)

### Phase 3 - Custom Patterns
- Enhanced custom pattern validation
- Pattern contribution workflow
- Pattern testing framework

### Phase 4 - Pattern Versioning
- Track pattern versions separately from Jerry version
- Support multiple pattern versions simultaneously
- Migration guides for pattern updates

### Phase 5 - Pattern Discovery
- Auto-discover new patterns in Fabric
- Suggest patterns based on content type
- Pattern recommendation engine

## References

- **Fabric Project**: https://github.com/danielmiessler/fabric
- **Jerry Documentation**: `.jerry/README.md`
- **Pattern Sync Tool**: `adws/jerry_sync_patterns.py`
- **Validation Tool**: `adws/jerry_validate.py`

---

**Version**: 1.0.0
**Last Updated**: 2025-12-15
**Maintainer**: Jerry Framework Team
