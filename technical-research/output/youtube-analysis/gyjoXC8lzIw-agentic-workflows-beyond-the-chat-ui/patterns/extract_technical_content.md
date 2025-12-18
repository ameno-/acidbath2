# TECH_STACK

## Languages
- Python - Primary language for the agentic drop zone implementation
- YAML - Configuration file format for drop zones
- Markdown - Prompt templates and documentation
- JSON - Training data format and configuration

## Frameworks & Libraries
- Rich - Terminal-based interface and logging
- Watchdog - File system event monitoring
- Astral UV - Python dependency management
- OpenAI Whisper - Audio transcription (tiny model)

## Tools & Platforms
- Claude Code - Primary AI agent with SDK support
- Gemini CLI - Alternative AI agent (work in progress)
- Replicate API - Image generation and editing services
- MCP (Model Context Protocol) - Server integration

## Services & APIs
- Claude Code SDK - TypeScript and Python SDKs available
- Replicate MCP Server - Image generation through API
- Google Nano Banana (Gemini 2.5 Flash) - Image generation model

# CODE_SNIPPETS

## Snippet 1: Drop Zone Configuration Entry
**Context**: YAML configuration for defining agentic workflows
**Timestamp**: 07:15

```yaml
name: echo_zone
file_patterns: ["*.txt"]
prompt: echo.md
agent: claude_code
model: claude-3-5-sonnet
color: blue
events: ["created", "modified"]
```

**Explanation**: Configures a drop zone that triggers when text files are added, using the echo.md prompt template with Claude Code
**Key Points**: Agent-agnostic configuration allows switching between different AI providers

## Snippet 2: Prompt Template Structure
**Context**: Standard prompt format for agentic workflows
**Timestamp**: 09:00

```markdown
# PURPOSE
You are an expert at echoing content from files.

# VARIABLES
- drop_file_path: {drop_file_path}
- output_directory: ./output

# WORKFLOW
1. Read the file at {drop_file_path}
2. Echo the content exactly as provided
3. Save output to designated directory

# OUTPUT FORMAT
## Echo Result
Content: [echoed content]
Source: {drop_file_path}
```

**Explanation**: Demonstrates variable templating and structured workflow definition
**Key Points**: Variables can be referenced throughout prompts, XML sections provide clear structure

## Snippet 3: Agent Execution Method
**Context**: Python code for running Claude Code programmatically
**Timestamp**: 19:00

```python
def prompt_claude_code(prompt, model="claude-3-5-sonnet"):
    # Build prompt with file path replacement
    full_prompt = prompt.replace("{drop_file_path}", file_path)
    
    # Configure Claude Code client
    client = anthropic.Anthropic()
    
    # Execute workflow
    for message in client.messages.stream(
        model=model,
        messages=[{"role": "user", "content": full_prompt}]
    ):
        if message.type == "content_block_delta":
            yield message.delta.text
```

**Explanation**: Shows how to programmatically execute AI agents with dynamic prompts
**Key Points**: Streaming responses allow real-time feedback during workflow execution

# COMMANDS & SCRIPTS

## Installation & Setup
```bash
# Install with UV (single file script)
uv run adz.py

# Set up environment variables
export ANTHROPIC_API_KEY="your_key_here"
export REPLICATE_API_TOKEN="your_token_here"
```

## Configuration
```bash
# Create drops.yaml configuration file
touch drops.yaml

# Set up drop zone directories
mkdir -p drop_zones/echo_zone
mkdir -p drop_zones/generate_images
mkdir -p drop_zones/morning_debrief
```

## Execution & Testing
```bash
# Run the agentic drop zone system
python adz.py

# Test with file drop
cp test.txt drop_zones/echo_zone/

# Monitor workflow execution
tail -f logs/workflow.log
```

## Deployment
```bash
# Run as background service
nohup python adz.py &

# Set up file system watchers
systemctl enable adz-watcher.service
```

# TECHNICAL_CONCEPTS

## Architectural Patterns
- **Event-Driven Architecture**: File system events trigger automated workflows
- **Template Pattern**: Reusable prompt templates with variable substitution
- **Agent Abstraction**: Unified interface for different AI providers

## Design Principles
- **Single Responsibility**: Each drop zone handles one specific workflow type
- **Agent Agnostic**: System works with any AI agent that has an SDK
- **File-Based Interface**: Leverages familiar file system interactions

## Best Practices
- **Prompt Engineering**: Structured prompts with clear sections (Purpose, Variables, Workflow)
- **Variable Templating**: Reusable components with dynamic content replacement
- **Streaming Responses**: Real-time feedback during long-running operations

## Common Pitfalls
- **Agent Lock-in**: Avoid hardcoding specific agent APIs; use abstraction layers
- **File Pattern Conflicts**: Ensure drop zones have unique file pattern matching
- **Resource Management**: Monitor concurrent workflow execution to prevent overload

# DEPENDENCIES & REQUIREMENTS

## System Requirements
- Python 3.8+: Core runtime environment
- File system access: For directory watching and file operations
- Network connectivity: For AI API calls

## Package Dependencies
- anthropic: Latest - Claude Code SDK integration
- replicate: Latest - Image generation API
- rich: Latest - Terminal UI and logging
- watchdog: Latest - File system event monitoring
- pyyaml: Latest - Configuration file parsing

## Environment Variables
```bash
ANTHROPIC_API_KEY=Your Claude API key for agent access
REPLICATE_API_TOKEN=Your Replicate token for image generation
ADZ_CONFIG_PATH=Path to drops.yaml configuration file
```

## Prerequisites
- AI API access: Claude Code, Gemini, or other supported agents
- File system permissions: Read/write access to drop zone directories
- Terminal environment: For rich logging and user interface

# RESOURCES & LINKS

## Official Documentation
- Claude Code SDK: https://docs.anthropic.com/claude/docs
- Replicate API: https://replicate.com/docs

## Repository Links
- Agentic Drop Zones: [URL in video description] - Complete implementation
- Phase 2 Agentic Coding Course: [Upcoming release] - Advanced workflows

## Related Tools & Extensions
- Rich Terminal Library: https://rich.readthedocs.io/ - Enhanced terminal output
- Watchdog: https://python-watchdog.readthedocs.io/ - File system monitoring

## Learning Resources
- Principled AI Coding: [Previous course] - Foundation concepts
- Five Agent Interaction Patterns: [Previous video] - Engineering impact patterns

## Community & Support
- Channel Subscription: Essential for course release notifications
- Video Comments: Community discussion and troubleshooting

# CONFIGURATION_FILES

## drops.yaml
**Purpose**: Main configuration file defining all drop zones and their behaviors
**Location**: Root directory of the project

```yaml
drop_zones:
  echo_zone:
    name: "Simple Echo Test"
    file_patterns: ["*.txt"]
    prompt: "prompts/echo.md"
    agent: "claude_code"
    model: "claude-3-5-sonnet"
    color: "blue"
    events: ["created", "modified"]
  
  generate_images:
    name: "Image Generation"
    file_patterns: ["*.txt", "*.md"]
    prompt: "prompts/create_image.md"
    agent: "claude_code"
    model: "claude-3-5-sonnet"
    color: "green"
    events: ["created"]
    
  morning_debrief:
    name: "Audio Transcription & Analysis"
    file_patterns: ["*.mp3", "*.wav", "*.m4a"]
    prompt: "prompts/morning_debrief.md"
    agent: "claude_code"
    model: "claude-3-5-sonnet"
    color: "yellow"
    events: ["created"]
```

## prompts/echo.md
**Purpose**: Simple echo workflow template
**Location**: prompts/ directory

```markdown
# PURPOSE
You are an expert at echoing content from files.

# VARIABLES
- drop_file_path: {drop_file_path}

# WORKFLOW
1. Read the file at {drop_file_path}
2. Echo the content exactly as provided

# OUTPUT FORMAT
## Echo Result
Content: [echoed content]
Source: {drop_file_path}
```

# WORKFLOW_STEPS

## Setup Process
1. Install Python dependencies using UV package manager
2. Create drops.yaml configuration file with desired workflows
3. Set up prompt templates in prompts/ directory
4. Configure environment variables for AI API access
5. Create drop zone directories matching configuration

## Development Workflow
1. Define new workflow in drops.yaml configuration
2. Create corresponding prompt template with variables and workflow steps
3. Test workflow by dropping sample files into designated directories
4. Monitor execution through rich terminal logging
5. Iterate on prompt engineering for optimal results

## Testing & Validation
1. Create test files matching configured file patterns
2. Drop files into appropriate zones and verify workflow triggers
3. Check output quality and format against expectations
4. Validate error handling for malformed inputs
5. Test concurrent workflow execution

## Deployment Process
1. Set up production environment with required dependencies
2. Configure file system permissions for drop zone directories
3. Deploy as background service with proper logging
4. Set up monitoring for workflow success/failure rates
5. Implement backup and recovery procedures for critical workflows

# AUTOMATION_OPPORTUNITIES

- **Workflow Orchestration**: Chain multiple drop zones together for complex multi-step processes
- **Batch Processing**: Automatically process multiple files dropped simultaneously
- **Error Recovery**: Implement retry logic for failed workflows with exponential backoff
- **Performance Monitoring**: Track workflow execution times and success rates
- **Dynamic Scaling**: Automatically adjust concurrent workflow limits based on system load

# TECHNICAL_NOTES

## Performance Considerations
- File system watching has minimal overhead but monitor for high-frequency file operations
- Concurrent workflow execution should be limited based on available system resources
- Large file processing may require chunking strategies for memory management

## Security Considerations
- Validate file types and sizes before processing to prevent malicious uploads
- Sanitize file paths to prevent directory traversal attacks
- Implement rate limiting to prevent API abuse through rapid file drops
- Store API keys securely using environment variables, never in code

## Compatibility Notes
- Python 3.8+ required for modern async/await syntax and type hints
- Cross-platform compatibility maintained through pathlib usage
- AI agent SDKs may have different version requirements - check documentation

## Troubleshooting Tips
- **File not processing**: Check file pattern matching in drops.yaml configuration
- **Agent errors**: Verify API keys and network connectivity to AI services
- **Permission denied**: Ensure proper file system permissions for drop zone directories
- **Concurrent limit exceeded**: Reduce parallel workflow execution or increase system resources

# QUICK_REFERENCE

## Essential Commands
```bash
# Start the agentic drop zone system
python adz.py

# Test with sample file
echo "Hello World" > drop_zones/echo_zone/test.txt

# Monitor logs in real-time
tail -f logs/adz.log

# Validate configuration
python adz.py --validate-config
```

## Key File Locations
- drops.yaml: ./drops.yaml - Main configuration file
- Prompts: ./prompts/ - Template directory
- Drop Zones: ./drop_zones/ - Active monitoring directories
- Output: ./output/ - Generated workflow results
- Logs: ./logs/ - System and workflow logging

## Important URLs
- Claude Code SDK Documentation: https://docs.anthropic.com/claude/docs
- Replicate API Reference: https://replicate.com/docs
- Rich Terminal Library: https://rich.readthedocs.io/
