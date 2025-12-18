## WORKFLOW_PATTERNS

### Pattern 1: File-Based Agent Automation
**Description**: Drag-and-drop files into specific directories to trigger automated agent workflows without manual chat interactions
**Trigger**: File creation/modification events in monitored directories
**Steps**:
1. User drops file into designated directory
2. File system watcher detects event
3. Pattern matching determines appropriate agent/prompt
4. Agent executes predefined workflow on file content
5. Results are generated and organized automatically

**Automation Potential**: High
**Complexity**: Moderate
**Frequency**: Daily/multiple times per day

### Pattern 2: Morning Debrief Processing
**Description**: Audio recording transcription, analysis, and formatting into structured daily planning documents
**Trigger**: Audio file dropped into morning debrief zone
**Steps**:
1. Audio file transcription using Whisper
2. Content analysis and idea extraction
3. Priority identification and organization
4. Extension suggestions and follow-up questions generation
5. Formatted output with actionable insights

**Automation Potential**: High
**Complexity**: Moderate
**Frequency**: Daily

### Pattern 3: Bulk Image Generation
**Description**: Generate multiple images from text prompts at scale using AI models
**Trigger**: Text file with image prompts dropped into generation zone
**Steps**:
1. Parse text file for image descriptions
2. Iterate through each prompt
3. Generate images via Replicate API
4. Save with descriptive filenames
5. Archive source file and open output directory

**Automation Potential**: High
**Complexity**: Simple
**Frequency**: Weekly/project-based

### Pattern 4: Financial Data Processing
**Description**: Categorize and analyze financial transactions from CSV files
**Trigger**: CSV file dropped into finance zone
**Steps**:
1. Parse CSV financial data
2. Categorize transactions automatically
3. Generate spending analysis charts
4. Create summary reports
5. Archive processed data

**Automation Potential**: High
**Complexity**: Moderate
**Frequency**: Monthly

### Pattern 5: Training Data Expansion
**Description**: Extend existing datasets with additional synthetic examples
**Trigger**: CSV/JSONL file dropped into training data zone
**Steps**:
1. Analyze existing data patterns
2. Generate similar examples
3. Validate data quality
4. Append to original dataset
5. Create expansion report

**Automation Potential**: High
**Complexity**: Moderate
**Frequency**: Project-based

## AGENT_CANDIDATES

### Agent 1: Drop Zone Orchestrator

**Purpose**: Coordinate file-based agent workflows with configurable drop zones

**Frontmatter Configuration**:
```yaml
---
name: drop-zone-orchestrator
description: Automate file-based workflows by monitoring directories and triggering appropriate agents
tools: Bash, Read, Write, Grep, Watch
color: blue
---
```

**Core Capabilities**:
- File system monitoring with Watchdog
- Pattern matching for file types and directories
- Agent selection and execution
- Parallel workflow processing
- Rich terminal logging and progress tracking

**Workflow**:
1. Initialize directory watchers based on configuration
2. Detect file events (create, modify, move)
3. Match against configured patterns
4. Load appropriate prompt template
5. Execute agent with file context
6. Stream results and manage outputs

**Inputs Required**:
- drops.yaml: Configuration file defining zones and agents
- Prompt templates: Markdown files with agent instructions
- Environment variables: API keys and model configurations

**Expected Outputs**:
- Processed files in designated output directories
- Execution logs with colored terminal output
- Archived input files post-processing

**Priority**: High
**Implementation Complexity**: Moderate
**Impact**: High

### Agent 2: Prompt Template Manager

**Purpose**: Standardize and manage reusable agent prompt templates

**Frontmatter Configuration**:
```yaml
---
name: prompt-template-manager
description: Create, validate, and manage standardized agent prompt templates
tools: Read, Write, Grep
color: green
---
```

**Core Capabilities**:
- Template validation and syntax checking
- Variable substitution and templating
- Prompt versioning and history
- Template library management
- Cross-agent compatibility testing

**Workflow**:
1. Validate prompt template structure
2. Check for required sections (Purpose, Variables, Workflow)
3. Test variable substitution
4. Store in template library
5. Generate usage documentation

**Inputs Required**:
- Template files: Markdown with YAML frontmatter
- Variable definitions: Expected input parameters
- Validation rules: Template structure requirements

**Expected Outputs**:
- Validated template files
- Template documentation
- Usage examples and test cases

**Priority**: Medium
**Implementation Complexity**: Simple
**Impact**: Medium

### Agent 3: Workflow Analytics Tracker

**Purpose**: Monitor and analyze agent workflow performance and usage patterns

**Frontmatter Configuration**:
```yaml
---
name: workflow-analytics-tracker
description: Track agent performance, usage patterns, and optimization opportunities
tools: Read, Write, Bash
color: purple
---
```

**Core Capabilities**:
- Execution time tracking
- Success/failure rate monitoring
- Resource usage analysis
- Pattern identification in workflow usage
- Performance optimization recommendations

**Workflow**:
1. Collect execution metrics from agent runs
2. Analyze performance patterns
3. Identify bottlenecks and optimization opportunities
4. Generate usage reports
5. Recommend workflow improvements

**Inputs Required**:
- Execution logs: Timestamped agent activity
- Resource metrics: CPU, memory, API usage
- Configuration data: Agent settings and parameters

**Expected Outputs**:
- Performance dashboards
- Usage analytics reports
- Optimization recommendations

**Priority**: Low
**Implementation Complexity**: Complex
**Impact**: Medium

## HOOK_OPPORTUNITIES

### Hook 1: Pre-Workflow Validation

**Hook Type**: pre_tool_use

**Trigger Event**: Before agent execution begins

**Purpose**: Validate input files and configuration before processing

**Implementation**:
```python
# Pseudocode for pre-workflow validation
def validate_workflow(context):
    # Check file format and size
    # Validate configuration completeness
    # Verify agent availability
    # Test API connectivity
    return validation_result
```

**Integration Points**:
- File system watcher before agent trigger
- Configuration loader validation
- API health checks

**Data Flow**:
- Input: File path, agent configuration, environment state
- Processing: Format validation, dependency checks, resource verification
- Output: Validation status, error messages, proceed/halt decision

**Priority**: High
**Implementation Complexity**: Simple

### Hook 2: Post-Processing Cleanup

**Hook Type**: post_tool_use

**Trigger Event**: After agent workflow completion

**Purpose**: Archive files, clean temporary data, and update tracking

**Implementation**:
```python
# Pseudocode for post-processing cleanup
def cleanup_workflow(context):
    # Archive processed files
    # Clean temporary directories
    # Update workflow logs
    # Send completion notifications
    return cleanup_status
```

**Integration Points**:
- Agent completion handlers
- File system management
- Notification systems

**Data Flow**:
- Input: Workflow results, file paths, execution metadata
- Processing: File archival, cleanup operations, status updates
- Output: Cleanup confirmation, updated file locations, notifications

**Priority**: Medium
**Implementation Complexity**: Simple

### Hook 3: Dynamic Agent Selection

**Hook Type**: user_prompt_submit

**Trigger Event**: When file is dropped into zone

**Purpose**: Intelligently select optimal agent based on file content analysis

**Implementation**:
```python
# Pseudocode for dynamic agent selection
def select_agent(context):
    # Analyze file content and type
    # Check agent availability and load
    # Match capabilities to requirements
    # Select optimal agent configuration
    return selected_agent
```

**Integration Points**:
- File analysis pipeline
- Agent registry and capability mapping
- Load balancing system

**Data Flow**:
- Input: File content, available agents, current system load
- Processing: Content analysis, capability matching, load assessment
- Output: Selected agent, configuration parameters, execution priority

**Priority**: Medium
**Implementation Complexity**: Complex

## CUSTOM_PATTERNS

### Pattern 1: Agent Workflow Analyzer

**Purpose**: Extract and analyze agentic workflow patterns from video transcripts and documentation

**Input Type**: Video transcript, text documentation

**Output Sections**:
- WORKFLOW_PATTERNS: Identified automatable processes
- AGENT_CANDIDATES: Potential agents to build
- HOOK_OPPORTUNITIES: Event-driven automation points
- IMPLEMENTATION_PRIORITY: Ranked development roadmap

**Use Case**: Analyzing content to identify automation opportunities and agent development priorities

**Similar Existing Patterns**: extract_wisdom, analyze_tech_landscape

**Priority**: High

### Pattern 2: Drop Zone Configuration Generator

**Purpose**: Generate drop zone YAML configurations from workflow descriptions

**Input Type**: Text descriptions of desired workflows

**Output Sections**:
- ZONE_DEFINITIONS: Directory structures and patterns
- AGENT_MAPPINGS: Agent-to-zone assignments
- PROMPT_TEMPLATES: Generated template files
- CONFIGURATION_YAML: Complete drops.yaml file

**Use Case**: Rapidly prototype and deploy new drop zone workflows

**Similar Existing Patterns**: create_coding_project, extract_patterns

**Priority**: Medium

### Pattern 3: Agent Performance Optimizer

**Purpose**: Analyze agent execution logs and recommend optimizations

**Input Type**: Agent execution logs, performance metrics

**Output Sections**:
- PERFORMANCE_ANALYSIS: Execution time and resource usage patterns
- BOTTLENECK_IDENTIFICATION: Performance constraint analysis
- OPTIMIZATION_RECOMMENDATIONS: Specific improvement suggestions
- CONFIGURATION_TUNING: Parameter adjustment recommendations

**Use Case**: Continuously improve agent workflow efficiency

**Similar Existing Patterns**: analyze_logs, improve_performance

**Priority**: Low

## TOOL_REQUIREMENTS

### For Agents
- Watchdog: File system monitoring - Already available? Yes
- Rich: Terminal formatting and logging - Already available? Yes
- PyYAML: Configuration file parsing - Already available? Yes
- Anthropic SDK: Claude API integration - Already available? Yes
- Replicate SDK: Image generation API - Already available? No
- Whisper: Audio transcription - Already available? No

### For Hooks
- asyncio: Asynchronous processing - Already available? Yes
- pathlib: File path manipulation - Already available? Yes
- logging: Event tracking - Already available? Yes

### For Patterns
- Natural Language Toolkit: Text analysis - Already available? No
- Pandas: Data processing - Already available? No
- Matplotlib: Chart generation - Already available? No

### External Dependencies
- UV: Python package management - Installation required? No
- FFmpeg: Audio processing - Installation required? Yes
- Git: Version control for templates - Installation required? No

## INTEGRATION_ARCHITECTURE

### System Components
```
File Drop → Watchdog Monitor → Pattern Matcher → Agent Selector → Prompt Builder → Agent Execution → Result Handler → Archive Manager

Hook System:
Pre-validation → Execution → Post-processing → Cleanup → Notification
```

### Data Flow
1. User drops file into monitored directory
2. Watchdog detects file system event
3. Pattern matcher determines appropriate workflow
4. Agent selector chooses optimal agent configuration
5. Prompt builder assembles context and instructions
6. Agent executes workflow with streaming output
7. Results are processed and archived

### Event Chain
- File Event → Triggers → Pattern Match → Results in → Agent Selection → Triggers → Workflow Execution → Results in → Output Generation → Triggers → Cleanup

## IMPLEMENTATION_PRIORITY

### High Priority (Implement First)
1. **Drop Zone Orchestrator Agent**
   - **Why**: Core functionality enabling all other workflows
   - **Effort**: 2-3 days development time
   - **Dependencies**: Watchdog, Rich, PyYAML

### Medium Priority (Implement Second)
2. **Prompt Template Manager**
   - **Why**: Standardizes agent development and reduces errors
   - **Effort**: 1-2 days development time
   - **Dependencies**: Template validation framework

### Low Priority (Nice to Have)
3. **Workflow Analytics Tracker**
   - **Why**: Optimization insights valuable but not critical for basic operation
   - **Effort**: 3-5 days development time
   - **Dependencies**: Analytics database, visualization tools

## EXAMPLE_CONFIGURATIONS

### Sample Agent File
```markdown
---
name: image-generator
description: Generate images from text prompts using AI models
tools: Read, Write, Bash
color: blue
---

You are an image generation agent that processes text files containing image prompts.

Variables:
- DROP_FILE_PATH: Path to the input text file
- IMAGE_OUTPUT_DIR: Directory for generated images
- IMAGE_MODEL: Replicate model identifier

Workflow:
1. Read the dropped file and parse image prompts
2. Create output directory if it doesn't exist
3. For each prompt, generate image via Replicate API
4. Save images with descriptive filenames
5. Archive the input file and open output directory

Output format: Generated images in specified directory with prompt text files
```

### Sample Hook Script
```python
#!/usr/bin/env python3
"""
Hook: pre_workflow_validation
Trigger: Before agent execution
Purpose: Validate inputs and environment
"""

def main(context_data):
    file_path = context_data.get('file_path')
    agent_config = context_data.get('agent_config')
    
    # Validate file exists and is readable
    if not os.path.exists(file_path):
        return {'valid': False, 'error': 'File not found'}
    
    # Check agent configuration
    if not agent_config.get('prompt'):
        return {'valid': False, 'error': 'No prompt configured'}
    
    return {'valid': True}

if __name__ == "__main__":
    main()
```

### Sample Pattern Invocation
```bash
fabric -y "$(cat video_transcript.txt)" --pattern agent_workflow_analyzer
```

## SCALABILITY_CONSIDERATIONS

### Multi-Agent Workflows
- Parallel processing of multiple drop zones simultaneously
- Agent pooling and load balancing for high-volume scenarios
- Workflow chaining where one agent's output becomes another's input

### Hook Chaining
- Pre-validation hooks can trigger additional setup hooks
- Post-processing hooks can cascade to notification and archival hooks
- Error hooks can trigger recovery and retry mechanisms

### Pattern Pipelines
- Agent workflow analysis followed by configuration generation
- Performance monitoring feeding into optimization recommendations
- Content analysis chaining into multiple specialized agents

### Data Persistence
- SQLite database for workflow execution history
- File-based configuration with Git version control
- Temporary processing directories with automatic cleanup

## SUCCESS_METRICS

### For Agents
- Execution Success Rate: Percentage of workflows completed without errors
- Processing Time: Average time from file drop to completion
- Resource Efficiency: CPU/memory usage per workflow
- User Adoption: Number of files processed per day/week

### For Hooks
- Hook Execution Time: Overhead added by hook processing
- Validation Accuracy: Percentage of issues caught before execution
- Cleanup Effectiveness: Successful archival and cleanup rate

### For Patterns
- Pattern Accuracy: Quality of extracted workflow patterns
- Configuration Validity: Generated configs that work without modification
- Time Savings: Reduction in manual configuration time

## NEXT_STEPS

1. Set up development environment with required dependencies
2. Implement core Drop Zone Orchestrator agent
3. Create initial set of prompt templates for common workflows
4. Test with simple file processing scenarios
5. Add hook system for validation and cleanup
6. Expand with additional specialized agents

## RECOMMENDATIONS

### Quick Wins
- Start with simple echo/copy workflows to validate the drop zone concept
- Use existing agent SDKs (Claude) before building custom integrations
- Focus on file-based workflows you already perform manually

### Strategic Investments
- Build comprehensive template library for reusable workflows
- Develop robust error handling and recovery mechanisms
- Create monitoring and analytics for continuous improvement

### Future Enhancements
- Web interface for drop zone management and monitoring
- Integration with cloud storage services for remote file processing
- Machine learning for intelligent agent selection and optimization
