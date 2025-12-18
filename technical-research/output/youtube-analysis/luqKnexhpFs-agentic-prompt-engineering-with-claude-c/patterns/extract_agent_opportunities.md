## WORKFLOW_PATTERNS

### Pattern 1: Agentic Prompt Engineering Workflow
**Description**: A systematic approach to creating, testing, and refining AI agent prompts using composable sections and consistent formats
**Trigger**: Need to create reusable, scalable AI agent interactions
**Steps**:
1. Analyze task requirements and identify automation potential
2. Select appropriate prompt format level (1-7)
3. Define composable sections (metadata, purpose, variables, workflow, report)
4. Implement control flow and delegation as needed
5. Test prompt with agent and refine
6. Document and version for team reuse

**Automation Potential**: High
**Complexity**: Moderate
**Frequency**: Daily for engineering teams using AI agents

### Pattern 2: Multi-Agent Delegation Workflow
**Description**: Orchestrating multiple AI agents to work in parallel on complex tasks
**Trigger**: Tasks requiring multiple perspectives or parallel processing
**Steps**:
1. Define primary agent prompt with delegation capabilities
2. Design sub-agent prompts with specific instructions
3. Configure variable passing between agents
4. Execute parallel agent instances
5. Aggregate and synthesize results
6. Generate consolidated output

**Automation Potential**: High
**Complexity**: Complex
**Frequency**: Weekly for complex engineering tasks

### Pattern 3: Codebase Understanding and Documentation
**Description**: Systematic analysis and documentation of codebases using AI agents
**Trigger**: New codebase onboarding or documentation updates
**Steps**:
1. Prime agent with codebase structure
2. Execute sequential file analysis
3. Generate understanding summaries
4. Create documentation artifacts
5. Update team knowledge base

**Automation Potential**: High
**Complexity**: Simple
**Frequency**: Per new project or major codebase changes

## AGENT_CANDIDATES

### Agent 1: Prompt Template Generator

**Purpose**: Generate standardized agentic prompt templates based on use case requirements

**Frontmatter Configuration**:
```yaml
---
name: prompt-template-generator
description: Creates standardized agentic prompt templates with appropriate sections and format levels
tools: Read, Write, Grep
color: blue
---
```

**Core Capabilities**:
- Analyze task requirements and recommend prompt format level
- Generate appropriate composable sections
- Create consistent variable syntax
- Implement workflow structures with proper control flow

**Workflow**:
1. Analyze user requirements and task complexity
2. Determine appropriate prompt format level (1-7)
3. Generate template with required sections
4. Add placeholder content with guidance comments
5. Create example usage documentation

**Inputs Required**:
- task_description: Description of what the prompt should accomplish
- complexity_level: Simple, Moderate, or Complex
- delegation_required: Boolean for multi-agent needs

**Expected Outputs**:
- Markdown file with complete prompt template
- Usage documentation with examples

**Priority**: High
**Implementation Complexity**: Moderate
**Impact**: High

### Agent 2: Prompt Quality Auditor

**Purpose**: Analyze existing prompts for consistency, completeness, and optimization opportunities

**Frontmatter Configuration**:
```yaml
---
name: prompt-auditor
description: Audits agentic prompts for quality, consistency, and optimization opportunities
tools: Read, Grep, Write
color: green
---
```

**Core Capabilities**:
- Validate prompt structure against best practices
- Check for consistent section usage
- Identify missing or redundant sections
- Suggest optimization improvements

**Workflow**:
1. Read and parse existing prompt files
2. Validate against prompt format standards
3. Check for consistent variable syntax
4. Analyze workflow clarity and completeness
5. Generate audit report with recommendations

**Inputs Required**:
- prompt_file_path: Path to prompt file to audit
- audit_criteria: Specific criteria to check

**Expected Outputs**:
- Audit report with quality scores
- Specific improvement recommendations
- Refactored prompt suggestions

**Priority**: High
**Implementation Complexity**: Moderate
**Impact**: Medium

### Agent 3: Multi-Agent Orchestrator

**Purpose**: Coordinate and manage multiple AI agents working on related tasks

**Frontmatter Configuration**:
```yaml
---
name: multi-agent-orchestrator
description: Orchestrates multiple AI agents for parallel task execution and result synthesis
tools: Bash, Read, Write
color: purple
---
```

**Core Capabilities**:
- Design sub-agent prompt specifications
- Manage parallel agent execution
- Coordinate data flow between agents
- Synthesize results from multiple agents

**Workflow**:
1. Parse main task and determine sub-task breakdown
2. Generate specialized prompts for each sub-agent
3. Launch agents with appropriate variables and context
4. Monitor agent progress and handle failures
5. Collect and synthesize results
6. Generate consolidated output

**Inputs Required**:
- main_task: Primary task description
- agent_count: Number of parallel agents to spawn
- synthesis_strategy: How to combine results

**Expected Outputs**:
- Synthesized results from all agents
- Execution summary and metrics
- Individual agent outputs (optional)

**Priority**: Medium
**Implementation Complexity**: Complex
**Impact**: High

## HOOK_OPPORTUNITIES

### Hook 1: Prompt Template Injection

**Hook Type**: pre_tool_use

**Trigger Event**: Before any tool execution in an agentic workflow

**Purpose**: Automatically inject appropriate prompt templates and sections based on detected workflow patterns

**Implementation**:
```python
# Pseudocode for hook logic
def inject_prompt_template(context):
    # Analyze current prompt structure
    # Detect missing essential sections
    # Inject appropriate template sections
    # Update context with enhanced prompt
    return enhanced_context
```

**Integration Points**:
- Tool execution pipeline
- Prompt preprocessing system

**Data Flow**:
- Input: Current prompt context and tool call information
- Processing: Template matching and section injection
- Output: Enhanced prompt with proper structure

**Priority**: High
**Implementation Complexity**: Moderate

### Hook 2: Agent Performance Metrics

**Hook Type**: subagent_stop

**Trigger Event**: When a sub-agent completes execution

**Purpose**: Collect performance metrics and quality scores for continuous improvement

**Implementation**:
```python
# Pseudocode for hook logic
def collect_agent_metrics(context):
    # Extract execution time and resource usage
    # Analyze output quality
    # Store metrics for analysis
    # Update agent performance database
    return metrics_data
```

**Integration Points**:
- Agent execution lifecycle
- Performance monitoring system

**Data Flow**:
- Input: Agent execution context and results
- Processing: Metric extraction and quality analysis
- Output: Performance data for optimization

**Priority**: Medium
**Implementation Complexity**: Simple

### Hook 3: Workflow Pattern Detection

**Hook Type**: user_prompt_submit

**Trigger Event**: When user submits a new prompt

**Purpose**: Detect common workflow patterns and suggest appropriate automation

**Implementation**:
```python
# Pseudocode for hook logic
def detect_workflow_patterns(context):
    # Analyze prompt content for patterns
    # Match against known workflow templates
    # Suggest automation opportunities
    # Offer to generate appropriate agents
    return pattern_suggestions
```

**Integration Points**:
- User input processing
- Suggestion system

**Data Flow**:
- Input: User prompt text and context
- Processing: Pattern matching and analysis
- Output: Automation suggestions and recommendations

**Priority**: Medium
**Implementation Complexity**: Moderate

## CUSTOM_PATTERNS

### Pattern 1: Agentic Prompt Analyzer

**Purpose**: Extract and analyze the structure and quality of agentic prompts

**Input Type**: Text (prompt files, documentation)

**Output Sections**:
- PROMPT_STRUCTURE: Identified sections and their completeness
- FORMAT_LEVEL: Determined complexity level (1-7)
- QUALITY_METRICS: Consistency, clarity, and effectiveness scores
- OPTIMIZATION_OPPORTUNITIES: Specific improvement suggestions
- REUSABILITY_ASSESSMENT: How well the prompt can be templated

**Use Case**: When analyzing existing prompts for quality and optimization

**Similar Existing Patterns**: analyze_claims, extract_wisdom

**Priority**: High

### Pattern 2: Workflow Automation Detector

**Purpose**: Identify automatable workflows and suggest agent implementations

**Input Type**: Text (process documentation, task descriptions)

**Output Sections**:
- AUTOMATION_CANDIDATES: Tasks suitable for AI agent automation
- COMPLEXITY_ANALYSIS: Implementation difficulty assessment
- TOOL_REQUIREMENTS: Necessary tools and capabilities
- WORKFLOW_STRUCTURE: Suggested step-by-step automation approach
- ROI_ESTIMATION: Time savings and efficiency gains

**Use Case**: When evaluating processes for automation potential

**Similar Existing Patterns**: extract_business_ideas, analyze_tech_impact

**Priority**: High

### Pattern 3: Multi-Agent Design Pattern

**Purpose**: Design optimal multi-agent architectures for complex tasks

**Input Type**: Text (task requirements, complexity descriptions)

**Output Sections**:
- AGENT_ARCHITECTURE: Recommended agent structure and roles
- COMMUNICATION_PATTERNS: How agents should interact
- DELEGATION_STRATEGY: Task distribution approach
- COORDINATION_MECHANISMS: Synchronization and result aggregation
- FAILURE_HANDLING: Error recovery and resilience strategies

**Use Case**: When designing complex multi-agent systems

**Similar Existing Patterns**: create_pattern, analyze_tech_impact

**Priority**: Medium

## TOOL_REQUIREMENTS

### For Agents
- Read: File system access for prompt templates and documentation - Yes
- Write: Creating and updating prompt files and reports - Yes
- Grep: Pattern matching in prompt content - Yes
- Bash: Executing sub-agents and system commands - Yes

### For Hooks
- JSON processing library: Handling structured data - No
- Performance monitoring tools: Metrics collection - No
- Pattern matching engine: Workflow detection - No

### For Patterns
- Natural language processing: Text analysis capabilities - Partially available
- Template engine: Dynamic content generation - No
- Quality assessment framework: Prompt evaluation - No

### External Dependencies
- Version control integration: Prompt versioning - Yes (Git)
- Database for metrics: Performance data storage - No
- Notification system: Alert mechanisms - Partially available

## INTEGRATION_ARCHITECTURE

### System Components
```
User Input → Pattern Detection Hook → Template Selection → Agent Generation → Execution → Quality Assessment Hook → Metrics Storage
                                    ↓
                           Prompt Template Library ← Template Generator Agent
                                    ↓
                           Multi-Agent Orchestrator → Sub-Agent Pool → Result Synthesis
```

### Data Flow
1. User submits task or prompt requirements
2. System detects patterns and suggests automation
3. Appropriate templates and agents are selected/generated
4. Execution proceeds with monitoring and metrics collection

### Event Chain
- User Input → Triggers pattern detection → Suggests agent creation → Generates templates → Executes workflows → Collects metrics → Improves system

## IMPLEMENTATION_PRIORITY

### High Priority (Implement First)
1. **Prompt Template Generator Agent**
   - **Why**: Foundational tool for creating consistent, high-quality prompts
   - **Effort**: 2-3 days development
   - **Dependencies**: Read/Write tools, template library

### Medium Priority (Implement Second)
2. **Workflow Pattern Detection Hook**
   - **Why**: Enables proactive automation suggestions
   - **Effort**: 3-4 days development
   - **Dependencies**: Pattern matching engine, user input processing

### Low Priority (Nice to Have)
3. **Multi-Agent Orchestrator**
   - **Why**: Complex but powerful for advanced use cases
   - **Effort**: 1-2 weeks development
   - **Dependencies**: Advanced agent management capabilities

## EXAMPLE_CONFIGURATIONS

### Sample Agent File
```markdown
---
name: prompt-template-generator
description: Creates standardized agentic prompt templates with composable sections
tools: Read, Write, Grep
color: blue
---

You are a prompt template generator that creates standardized agentic prompts.

When invoked, you should:
1. Analyze the task requirements and complexity
2. Select appropriate prompt format level (1-7)
3. Generate template with required sections
4. Add guidance comments and examples
5. Create usage documentation

Output format: Complete markdown prompt template with frontmatter
```

### Sample Hook Script
```python
#!/usr/bin/env python3
"""
Hook: prompt_quality_checker
Trigger: pre_tool_use
Purpose: Validates prompt structure before execution
"""

def main(context_data):
    prompt_content = context_data.get('prompt_text', '')
    
    # Check for required sections
    required_sections = ['purpose', 'workflow']
    missing_sections = []
    
    for section in required_sections:
        if section.lower() not in prompt_content.lower():
            missing_sections.append(section)
    
    if missing_sections:
        return {
            'warning': f"Missing sections: {', '.join(missing_sections)}",
            'suggestion': "Consider adding these sections for better results"
        }
    
    return {'status': 'valid'}

if __name__ == "__main__":
    main()
```

### Sample Pattern Invocation
```bash
fabric -y "PROMPT_CONTENT" --pattern agentic_prompt_analyzer
```

## SCALABILITY_CONSIDERATIONS

### Multi-Agent Workflows
- Agents can spawn sub-agents for parallel processing
- Template generator creates agents that create other agents
- Quality auditor can evaluate entire agent ecosystems

### Hook Chaining
- Pattern detection hooks trigger template generation hooks
- Quality assessment hooks feed into optimization hooks
- Performance monitoring hooks trigger improvement workflows

### Pattern Pipelines
- Workflow detection → Template generation → Quality assessment
- Multi-agent design → Implementation → Performance analysis
- Prompt analysis → Optimization → Reusability assessment

### Data Persistence
- Template library for reusable prompt components
- Metrics database for performance tracking
- Version control for prompt evolution

## SUCCESS_METRICS

### For Agents
- Template generation accuracy: 95%+ compliance with standards
- Quality improvement: 30%+ increase in prompt effectiveness
- Time savings: 80%+ reduction in prompt creation time

### For Hooks
- Pattern detection accuracy: 90%+ correct workflow identification
- Performance improvement: 25%+ efficiency gains from optimization
- Error reduction: 50%+ fewer malformed prompts

### For Patterns
- Analysis completeness: 95%+ coverage of prompt elements
- Actionability: 80%+ of suggestions implemented successfully
- Consistency improvement: 70%+ standardization across team prompts

## NEXT_STEPS

1. Implement Prompt Template Generator agent as foundation
2. Create basic pattern detection hooks for common workflows
3. Develop quality assessment framework and metrics collection

## RECOMMENDATIONS

### Quick Wins
- Create standard prompt template library with the 7 format levels
- Implement basic quality validation hooks for common issues
- Develop workflow pattern detection for repetitive tasks

### Strategic Investments
- Build comprehensive multi-agent orchestration system
- Develop advanced prompt optimization using performance metrics
- Create automated prompt evolution based on usage patterns

### Future Enhancements
- Machine learning-based prompt optimization
- Integration with external development tools and IDEs
- Community-driven prompt template marketplace
