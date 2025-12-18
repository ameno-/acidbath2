# YouTube Analysis Output Directory

This directory contains comprehensive analysis output from the `youtube-analyzer` agent.

## Directory Structure

Each analyzed video gets its own subdirectory named by video ID:

```
/output/youtube-analysis/
├── README.md (this file)
├── {video-id-1}/
│   ├── metadata.json
│   ├── transcript.txt
│   ├── patterns/
│   │   ├── youtube_summary.md
│   │   ├── extract_wisdom.md
│   │   ├── extract_insights.md
│   │   ├── extract_recommendations.md
│   │   ├── get_wow_per_minute.md
│   │   ├── rate_content.md
│   │   ├── extract_youtube_metadata.md
│   │   ├── extract_technical_content.md (conditional)
│   │   ├── extract_educational_value.md (conditional)
│   │   ├── extract_agent_opportunities.md
│   │   └── create_knowledge_artifacts.md (conditional)
│   ├── aggregated-report.md
│   ├── audio-summary.mp3 (optional)
│   └── generated-artifacts/
│       ├── agents/
│       │   └── [generated-agent].md
│       ├── hooks/
│       │   └── [generated-hook].py
│       ├── patterns/
│       │   └── [custom-pattern]/
│       │       └── system.md
│       └── knowledge/
│           ├── flashcards.csv
│           ├── quiz.md
│           └── diagrams.md
├── {video-id-2}/
│   └── ...
└── {video-id-3}/
    └── ...
```

## File Descriptions

### Root Level Files

**metadata.json**
- Raw YouTube video metadata from yt-dlp
- Includes: title, channel, upload date, views, likes, description, tags
- Used for content classification and quality assessment

**transcript.txt**
- Full video transcript with timestamps
- Auto-generated or official captions
- Source for all pattern analysis

**aggregated-report.md**
- Comprehensive markdown report combining all pattern outputs
- Includes executive summary, navigation, insights, recommendations
- Primary deliverable for human consumption

**audio-summary.mp3** (optional)
- Text-to-speech audio summary of key findings
- Generated via ElevenLabs/OpenAI/pyttsx3
- Ultra-concise (2-3 minutes)

### Patterns Directory

Contains individual output from each fabric pattern:

**Core Patterns** (always generated):
- `youtube_summary.md` - Video summary with timestamps
- `extract_wisdom.md` - Comprehensive knowledge extraction
- `extract_insights.md` - Key takeaways
- `extract_recommendations.md` - Actionable items
- `get_wow_per_minute.md` - Content quality scoring (JSON)
- `rate_content.md` - Content classification and rating
- `extract_youtube_metadata.md` - Metadata analysis
- `extract_agent_opportunities.md` - Automation identification

**Conditional Patterns** (based on content type):
- `extract_technical_content.md` - Code, tools, commands (if technical)
- `extract_educational_value.md` - Learning objectives (if educational)
- `create_knowledge_artifacts.md` - Study materials (if educational/general)

### Generated Artifacts Directory

Output from `meta-agent` when automation opportunities are identified:

**agents/** - Claude Code agent configurations
- Properly formatted .md files with frontmatter
- Ready to use or install to `~/.claude/agents/`
- Include usage instructions and examples

**hooks/** - Event-driven automation scripts
- Python scripts for Claude Code hooks
- Include installation instructions
- Require adding to `settings.json`

**patterns/** - Custom fabric patterns
- Pattern directory structure with system.md
- Ready to use or install to `~/.config/fabric/patterns/`
- Tailored to specific content or workflows

**knowledge/** - Learning artifacts
- Flashcards in CSV/Anki format
- Quizzes with questions and answers
- Mermaid diagrams and concept maps
- Reference materials and cheat sheets

## Usage

### Analyzing a New Video

```bash
# Use youtube-analyzer agent
Task: youtube-analyzer
Input: https://youtube.com/watch?v=VIDEO_ID
```

The agent will:
1. Create `/output/youtube-analysis/VIDEO_ID/` directory
2. Extract metadata and transcript
3. Run all applicable patterns
4. Generate aggregated report
5. Optionally create audio summary
6. Identify automation opportunities

### Accessing Results

```bash
# View the main report
cat /output/youtube-analysis/VIDEO_ID/aggregated-report.md

# Check specific pattern output
cat /output/youtube-analysis/VIDEO_ID/patterns/extract_insights.md

# Review automation opportunities
cat /output/youtube-analysis/VIDEO_ID/patterns/extract_agent_opportunities.md

# Listen to audio summary
open /output/youtube-analysis/VIDEO_ID/audio-summary.mp3
```

### Generating Agents/Hooks

If `extract_agent_opportunities` identified high-value automation:

```bash
# Use meta-agent
Task: meta-agent
Input: /output/youtube-analysis/VIDEO_ID/patterns/extract_agent_opportunities.md
```

Generated artifacts will be saved to:
- `generated-artifacts/` subdirectory
- Appropriate system directories (`~/.claude/agents/`, etc.)

### Batch Analysis

For analyzing multiple videos:

```bash
# Create a list of URLs
urls=(
  "https://youtube.com/watch?v=VIDEO_ID_1"
  "https://youtube.com/watch?v=VIDEO_ID_2"
  "https://youtube.com/watch?v=VIDEO_ID_3"
)

# Analyze each (pseudocode - would need actual implementation)
for url in "${urls[@]}"; do
  # Invoke youtube-analyzer agent
  echo "Analyzing: $url"
done
```

## Organization Tips

### Naming Conventions

Video IDs are unique and persistent, making them ideal for directory names.

Example:
- `dQw4w9WgXcQ/` - Rick Astley video
- `OIKTsVjTVJE/` - MCP alternatives video

### Cleanup

Old analyses can be removed:

```bash
# Remove specific analysis
rm -rf /output/youtube-analysis/VIDEO_ID/

# Remove analyses older than 30 days
find /output/youtube-analysis/ -type d -mtime +30 -exec rm -rf {} \;
```

### Archiving

For long-term storage:

```bash
# Archive specific video analysis
tar -czf VIDEO_ID-analysis.tar.gz /output/youtube-analysis/VIDEO_ID/

# Archive all analyses
tar -czf youtube-analyses-$(date +%Y%m%d).tar.gz /output/youtube-analysis/
```

## Integration with Other Tools

### Fabric CLI

Run additional patterns on existing transcripts:

```bash
cat /output/youtube-analysis/VIDEO_ID/transcript.txt | \
  fabric --pattern PATTERN_NAME > custom-output.md
```

### Meta-Agent

Generate artifacts from existing analysis:

```bash
# Point meta-agent to opportunities file
meta-agent /output/youtube-analysis/VIDEO_ID/patterns/extract_agent_opportunities.md
```

### Knowledge Management

Import generated knowledge artifacts:

```bash
# Import Anki flashcards
# (from generated-artifacts/knowledge/flashcards.csv)

# Add diagrams to documentation
cp generated-artifacts/knowledge/diagrams.md ~/docs/
```

## Example Workflow

1. **User submits YouTube URL**
   ```
   User: Analyze https://youtube.com/watch?v=ABC123
   ```

2. **Hook detects URL** (if `--detect-youtube` enabled)
   ```
   System: YouTube video detected. Consider using youtube-analyzer agent.
   ```

3. **User invokes agent**
   ```
   User: Use youtube-analyzer agent
   ```

4. **Agent analyzes video**
   - Creates `/output/youtube-analysis/ABC123/`
   - Runs all patterns
   - Generates aggregated report
   - Identifies 3 automation opportunities

5. **User reviews report**
   ```bash
   cat /output/youtube-analysis/ABC123/aggregated-report.md
   ```

6. **User generates artifacts** (optional)
   ```
   User: Use meta-agent with ABC123 opportunities
   ```

7. **Meta-agent creates agents/hooks**
   - Saves to `/output/youtube-analysis/ABC123/generated-artifacts/`
   - Installs to system directories
   - Provides integration instructions

8. **User tests and integrates**
   - Reviews generated agents
   - Enables hooks in settings.json
   - Uses new capabilities

## Troubleshooting

### Permission Errors

Ensure output directory is writable:

```bash
chmod -R u+w /output/youtube-analysis/
```

### Missing Patterns

If pattern output is missing:

1. Check if pattern exists: `fabric --listpatterns`
2. Test pattern manually: `echo "test" | fabric --pattern PATTERN_NAME`
3. Review youtube-analyzer logs

### Large Files

Transcripts and reports can be large:

```bash
# Check directory size
du -sh /output/youtube-analysis/VIDEO_ID/

# Compress if needed
gzip /output/youtube-analysis/VIDEO_ID/transcript.txt
```

### Failed Analysis

If analysis fails partially:

- Individual pattern outputs are preserved
- Aggregated report shows which sections completed
- Can re-run specific patterns manually

## Best Practices

1. **Review before generating artifacts** - Not all opportunities need automation
2. **Archive old analyses** - Keep directory size manageable
3. **Customize patterns** - Modify fabric patterns for your specific needs
4. **Test generated code** - Always review agents/hooks before enabling
5. **Document custom workflows** - Add notes to README files
6. **Use version control** - Track generated artifacts that you modify

## Related Documentation

- **youtube-analyzer agent**: `/Users/ameno/.claude/agents/youtube-analyzer.md`
- **meta-agent**: `/Users/ameno/.claude/agents/meta-agent.md`
- **Fabric patterns**: `/Users/ameno/.config/fabric/patterns/*/system.md`
- **Hook documentation**: `/Users/ameno/.claude/hooks/README-youtube-detection.md`
