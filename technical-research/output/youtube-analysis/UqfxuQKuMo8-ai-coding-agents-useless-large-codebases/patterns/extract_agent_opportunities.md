# WORKFLOW PATTERNS

### Pattern 1: AI Coding Agent Optimization Workflow
**Description**: Comparing different approaches to AI coding tasks to identify performance bottlenecks and optimization opportunities
**Trigger**: Performance issues with AI coding agents in large codebases
**Steps**:
1. Benchmark manual approach timing
2. Test naive AI agent approach
3. Implement specialized MCP servers
4. Measure token usage and execution time
5. Compare results and calculate improvement factors

**Automation Potential**: High
**Complexity**: Moderate
**Frequency**: Weekly for developers using AI coding tools

### Pattern 2: Large Codebase Refactoring Workflow
**Description**: Systematic approach to refactoring operations in multi-thousand line codebases
**Trigger**: Need to rename, extract, or move code elements across large projects
**Steps**:
1. Identify refactoring target
2. Use semantic search to find all references
3. Execute refactoring with proper tooling
4. Run comprehensive test suite
5. Validate changes across entire codebase

**Automation Potential**: High
**Complexity**: Complex
**Frequency**: Daily for active development teams

### Pattern 3: MCP Server Evaluation and Setup
**Description**: Process for discovering, evaluating, and configuring MCP servers for specific development needs
**Trigger**: Need for specialized tooling in AI coding workflows
**Steps**:
1. Research available MCP servers for language/framework
2. Install and configure selected servers
3. Test integration with AI coding assistant
4. Benchmark performance improvements
5. Document configuration and usage patterns

**Automation Potential**: Medium
**Complexity**: Moderate
**Frequency**: Monthly when adopting new tools

## AGENT_CANDIDATES

### Agent 1: MCP Server Benchmarker

**Purpose**: Automate the process of benchmarking AI coding performance with and without MCP servers

**Frontmatter Configuration**:
```yaml
---
name: mcp-benchmarker
description: Benchmark AI coding performance with different MCP server configurations
tools: Bash, Read, Write, Grep
color: blue
---
```

**Core Capabilities**:
- Execute coding tasks with different tool configurations
- Measure token usage, execution time, and success rates
- Generate comparative performance reports
- Track cost estimates across different approaches

**Workflow**:
1. Parse benchmark task specification
2. Execute task with baseline (no MCP) configuration
3. Execute task with each specified MCP server
4. Collect metrics (tokens, time, cost, success rate)
5. Generate comparison report with improvement factors

**Inputs Required**:
- task_description: Description of coding task to benchmark
- mcp_servers: List of MCP servers to test
- baseline_approach: Configuration for baseline comparison

**Expected Outputs**:
- benchmark_report.md: Detailed performance comparison
- metrics.json: Raw performance data
- recommendations.md: Suggested optimal configuration

**Priority**: High
**Implementation Complexity**: Moderate
**Impact**: High

### Agent 2: Codebase Analyzer

**Purpose**: Analyze large codebases to identify refactoring opportunities and optimal tooling strategies

**Frontmatter Configuration**:
```yaml
---
name: codebase-analyzer
description: Analyze codebase structure and suggest optimization strategies for AI coding
tools: Bash, Read, Write, Grep
color: green
---
```

**Core Capabilities**:
- Count lines of code by language and file type
- Identify heavily used types and symbols
- Suggest appropriate MCP servers based on codebase characteristics
- Generate refactoring opportunity reports

**Workflow**:
1. Scan codebase structure and collect metrics
2. Identify frequently referenced symbols/types
3. Analyze code complexity and coupling
4. Match codebase characteristics to available tools
5. Generate recommendations report

**Inputs Required**:
- codebase_path: Path to codebase root
- languages: Primary programming languages used
- analysis_depth: Level of analysis detail required

**Expected Outputs**:
- codebase_analysis.md: Comprehensive codebase report
- tool_recommendations.md: Suggested MCP servers and configurations
- refactoring_opportunities.json: Identified improvement areas

**Priority**: Medium
**Implementation Complexity**: Complex
**Impact**: High

### Agent 3: MCP Server Configurator

**Purpose**: Automate the discovery, installation, and configuration of MCP servers

**Frontmatter Configuration**:
```yaml
---
name: mcp-configurator
description: Discover and configure MCP servers for development workflows
tools: Bash, Read, Write
color: purple
---
```

**Core Capabilities**:
- Search GitHub for relevant MCP servers
- Install and configure MCP servers
- Generate Claude Desktop configuration
- Test MCP server connectivity and functionality

**Workflow**:
1. Parse language/framework requirements
2. Search for compatible MCP servers
3. Install selected servers
4. Generate configuration files
5. Test integration and functionality

**Inputs Required**:
- languages: Programming languages used
- frameworks: Frameworks and tools in use
- requirements: Specific functionality needed

**Expected Outputs**:
- claude_desktop_config.json: Updated configuration
- installation_log.md: Installation steps and results
- server_test_results.md: Functionality test outcomes

**Priority**: Medium
**Implementation Complexity**: Moderate
**Impact**: Medium

## HOOK_OPPORTUNITIES

### Hook 1: Performance Metrics Collector

**Hook Type**: post_tool_use

**Trigger Event**: After any MCP tool usage

**Purpose**: Automatically collect performance metrics for AI coding operations

**Implementation**:
```python
# Pseudocode for hook logic
def hook_function(context):
    tool_name = context.tool_name
    execution_time = context.execution_time
    tokens_used = context.tokens_used
    success = context.success
    
    # Log metrics to performance database
    log_performance_metrics(tool_name, execution_time, tokens_used, success)
    
    # Check for performance anomalies
    if execution_time > threshold:
        notify_performance_issue(tool_name, execution_time)
    
    return context
```

**Integration Points**:
- Claude Code MCP tool execution pipeline
- Performance monitoring dashboard

**Data Flow**:
- Input: Tool execution context with timing and token data
- Processing: Store metrics, analyze for anomalies
- Output: Performance alerts, trend data

**Priority**: High
**Implementation Complexity**: Simple

### Hook 2: Automatic Tool Selection

**Hook Type**: pre_tool_use

**Trigger Event**: Before tool selection for coding tasks

**Purpose**: Automatically suggest optimal tools based on task characteristics

**Implementation**:
```python
# Pseudocode for hook logic
def hook_function(context):
    task_type = analyze_task_type(context.prompt)
    codebase_size = get_codebase_metrics()
    available_tools = get_available_mcp_servers()
    
    # Suggest optimal tool configuration
    optimal_tools = recommend_tools(task_type, codebase_size, available_tools)
    context.suggested_tools = optimal_tools
    
    return context
```

**Integration Points**:
- Claude Code prompt processing
- MCP server registry

**Data Flow**:
- Input: User prompt and available tools
- Processing: Analyze task requirements, match to optimal tools
- Output: Tool recommendations

**Priority**: Medium
**Implementation Complexity**: Moderate

### Hook 3: Cost Tracking

**Hook Type**: session_start

**Trigger Event**: Start of AI coding session

**Purpose**: Initialize cost tracking for token usage across different tool configurations

**Implementation**:
```python
# Pseudocode for hook logic
def hook_function(context):
    session_id = generate_session_id()
    start_time = get_current_time()
    
    # Initialize cost tracking
    initialize_cost_tracker(session_id, start_time)
    
    # Set up token usage monitoring
    context.cost_tracker = CostTracker(session_id)
    
    return context
```

**Integration Points**:
- Claude Code session management
- Cost reporting dashboard

**Data Flow**:
- Input: Session start event
- Processing: Initialize tracking systems
- Output: Cost tracking context

**Priority**: Medium
**Implementation Complexity**: Simple

## CUSTOM_PATTERNS

### Pattern 1: MCP Performance Analysis

**Purpose**: Extract performance metrics and optimization recommendations from AI coding sessions

**Input Type**: Text logs from AI coding sessions

**Output Sections**:
- PERFORMANCE_METRICS: Token usage, execution time, success rates
- TOOL_EFFECTIVENESS: Which MCP servers provided best results
- OPTIMIZATION_OPPORTUNITIES: Suggested improvements
- COST_ANALYSIS: Financial impact of different approaches
- RECOMMENDATIONS: Best practices for similar tasks

**Use Case**: When analyzing AI coding session logs to optimize future performance

**Similar Existing Patterns**: None directly comparable

**Priority**: High

### Pattern 2: Codebase Readiness Assessment

**Purpose**: Analyze codebases to determine optimal AI coding tool configurations

**Input Type**: Codebase structure and metrics

**Output Sections**:
- CODEBASE_CHARACTERISTICS: Size, complexity, language breakdown
- TOOL_COMPATIBILITY: Which MCP servers are most suitable
- REFACTORING_PRIORITIES: Areas that would benefit most from AI assistance
- SETUP_RECOMMENDATIONS: Specific configuration suggestions
- EXPECTED_BENEFITS: Projected performance improvements

**Use Case**: Before setting up AI coding tools for a new project

**Similar Existing Patterns**: None directly comparable

**Priority**: Medium

### Pattern 3: Tool Configuration Guide

**Purpose**: Generate setup instructions for MCP servers based on development environment

**Input Type**: Development environment description

**Output Sections**:
- ENVIRONMENT_ANALYSIS: Current setup and requirements
- SERVER_SELECTION: Recommended MCP servers
- INSTALLATION_STEPS: Detailed setup instructions
- CONFIGURATION_FILES: Required config file contents
- VERIFICATION_TESTS: How to confirm proper setup

**Use Case**: When setting up AI coding tools in a new environment

**Similar Existing Patterns**: Similar to existing installation guides

**Priority**: Low

## TOOL_REQUIREMENTS

### For Agents
- Bash: Execute system commands and run benchmarks - Already available? Yes
- Read: Access codebase files and configuration - Already available? Yes
- Write: Generate reports and configuration files - Already available? Yes
- Grep: Search through codebases for patterns - Already available? Yes
- Git: Version control operations for testing - Already available? No
- Process Monitor: Track system resource usage - Already available? No

### For Hooks
- Performance Database: Store metrics over time - Already available? No
- Cost Calculator: Calculate token costs - Already available? No
- Notification System: Alert on performance issues - Already available? No

### For Patterns
- Log Parser: Extract structured data from logs - Already available? No
- Metrics API: Access performance data - Already available? No

### External Dependencies
- GitHub API: Search for MCP servers - Installation required? Yes
- Package Managers: Install MCP servers - Installation required? No
- Configuration Validators: Verify MCP setup - Installation required? Yes

## INTEGRATION_ARCHITECTURE

### System Components
```
User Request → Performance Hook → Agent Selection → MCP Server → Results → Metrics Hook → Database
     ↓                                                                           ↓
Pattern Analysis ← Performance Reports ← Cost Tracking ← Session Data ← Performance Logging
```

### Data Flow
1. User initiates AI coding task
2. Pre-hooks analyze and optimize tool selection
3. Task executes with selected MCP servers
4. Post-hooks collect performance metrics
5. Data flows to analysis patterns and reporting

### Event Chain
- session_start → Initialize tracking → Tool selection → Task execution → post_tool_use → Metrics collection → Pattern analysis

## IMPLEMENTATION_PRIORITY

### High Priority (Implement First)
1. **MCP Server Benchmarker Agent**
   - **Why**: Directly addresses the core problem of optimizing AI coding performance
   - **Effort**: 2-3 weeks development time
   - **Dependencies**: Access to various MCP servers, metrics collection system

### Medium Priority (Implement Second)
2. **Performance Metrics Collector Hook**
   - **Why**: Provides essential data for optimization decisions
   - **Effort**: 1 week development time
   - **Dependencies**: Database for metrics storage

3. **MCP Performance Analysis Pattern**
   - **Why**: Enables systematic analysis of performance data
   - **Effort**: 1 week development time
   - **Dependencies**: Performance data collection system

### Low Priority (Nice to Have)
4. **Codebase Analyzer Agent**
   - **Why**: Useful for initial setup but not core functionality
   - **Effort**: 3-4 weeks development time
   - **Dependencies**: Advanced code analysis tools

## EXAMPLE_CONFIGURATIONS

### Sample Agent File
```markdown
---
name: mcp-benchmarker
description: Benchmark AI coding performance across different MCP server configurations
tools: Bash, Read, Write, Grep
color: blue
---

You are an AI coding performance benchmarking agent.

When invoked, you should:
1. Parse the benchmark specification from the user
2. Execute the coding task with baseline configuration (no MCP servers)
3. Execute the same task with each specified MCP server
4. Collect metrics: execution time, token usage, success rate, cost
5. Generate a comparative analysis report

Output format: Structured markdown report with performance tables and recommendations.
```

### Sample Hook Script
```python
#!/usr/bin/env python3
"""
Hook: performance_metrics_collector
Trigger: post_tool_use
Purpose: Collect and analyze AI coding tool performance metrics
"""

def main(context_data):
    # Extract performance data
    tool_name = context_data.get('tool_name')
    execution_time = context_data.get('execution_time')
    tokens_used = context_data.get('tokens_used')
    
    # Store metrics
    store_performance_metrics(tool_name, execution_time, tokens_used)
    
    # Check for anomalies
    if execution_time > get_threshold(tool_name):
        send_performance_alert(tool_name, execution_time)

if __name__ == "__main__":
    main()
```

### Sample Pattern Invocation
```bash
fabric -y "AI coding session log with MCP server usage data" --pattern mcp_performance_analysis
```

## SCALABILITY_CONSIDERATIONS

### Multi-Agent Workflows
- Benchmarker agent could coordinate with analyzer agent to provide comprehensive optimization recommendations
- Configuration agent could automatically apply recommendations from benchmarker

### Hook Chaining
- Performance metrics hook could trigger cost analysis hook when thresholds are exceeded
- Session hooks could chain to provide comprehensive session analytics

### Pattern Pipelines
- Codebase analysis → Tool recommendations → Performance benchmarking → Optimization suggestions
- Session logs → Performance analysis → Cost analysis → Recommendations

### Data Persistence
- Performance metrics database for trend analysis
- Configuration templates for reuse across projects
- Benchmark results for comparative analysis

## SUCCESS_METRICS

### For Agents
- **Benchmark Accuracy**: How well performance predictions match actual results
- **Time Savings**: Reduction in manual benchmarking effort
- **Configuration Success Rate**: Percentage of successful MCP server setups

### For Hooks
- **Data Collection Coverage**: Percentage of tool usage events captured
- **Alert Accuracy**: Ratio of true performance issues to false alarms
- **Processing Overhead**: Impact on system performance

### For Patterns
- **Analysis Accuracy**: Quality of insights extracted from session data
- **Recommendation Effectiveness**: Success rate of optimization suggestions
- **Report Usefulness**: User satisfaction with generated analyses

## NEXT_STEPS

1. **Implement Performance Metrics Collection**: Set up basic hook system to capture tool usage data
2. **Develop Benchmarking Framework**: Create standardized approach for comparing AI coding performance
3. **Build MCP Server Registry**: Catalog available servers with compatibility information

## RECOMMENDATIONS

### Quick Wins
- **Performance Metrics Hook**: Simple to implement, provides immediate value for optimization decisions
- **Basic Benchmarking Script**: Manual version of benchmarker agent for immediate use

### Strategic Investments
- **Comprehensive Benchmarking Agent**: Automated system for continuous performance optimization
- **Intelligent Tool Selection**: AI-powered recommendation system for optimal MCP server selection

### Future Enhancements
- **Predictive Performance Modeling**: ML models to predict optimal configurations
- **Community MCP Server Marketplace**: Platform for sharing and discovering optimization tools
- **Real-time Performance Optimization**: Dynamic tool selection based on current performance metrics
