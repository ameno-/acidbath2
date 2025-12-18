# Learning Objectives & Implementation Guide
## Claude Code SDK Custom Agents - Structured Learning Path

---

## Primary Learning Objectives

By the end of this learning path, you will be able to:

1. **Understand Agent Architecture**
   - Explain the four core elements of Claude Code agents
   - Describe how system prompts control agent behavior
   - Identify when to use different Claude models
   - Understand the role of tools in agent capabilities

2. **Build Single-Purpose Agents**
   - Create agents with custom system prompts
   - Override default Claude Code behavior
   - Test and validate agent responses
   - Select appropriate models for tasks

3. **Develop Custom Tools**
   - Define tools using the @tool decorator
   - Implement deterministic tool logic
   - Write effective tool descriptions
   - Validate tool inputs and outputs

4. **Create MCP Servers**
   - Package custom tools into MCP servers
   - Integrate MCP servers with agents
   - Manage tool availability per agent
   - Optimize context consumption

5. **Orchestrate Multi-Agent Systems**
   - Design agent workflows and handoffs
   - Implement agent-to-agent communication
   - Build specialized agent roles
   - Monitor and debug multi-agent systems

6. **Optimize Agent Performance**
   - Select models based on task complexity
   - Minimize context window consumption
   - Monitor token usage and costs
   - Implement efficient conversation patterns

---

## Learning Path Levels

### Level 1: Foundation (2-3 hours)

**Prerequisites**:
- Basic Python programming knowledge
- Understanding of function definitions and decorators
- Familiarity with API concepts
- Command-line comfort

**Objectives**:
- [ ] Understand the four core elements of agents
- [ ] Identify the role of system prompts
- [ ] Recognize when to use different Claude models
- [ ] Set up development environment

**Activities**:
1. Watch the "Agentic Coding ENDGAME" video completely
2. Review TAC (Think, Act, Check) framework prerequisite
3. Install UV package manager
4. Set up Anthropic API key
5. Verify Claude Code SDK installation

**Deliverable**: Successfully run a basic Claude Code agent

**Resources**:
- Video: Agentic Coding ENDGAME (16:56)
- Claude Code SDK documentation
- UV installation guide
- Anthropic API documentation

---

### Level 2: Single-Purpose Agents (4-6 hours)

**Prerequisites**:
- Completed Level 1
- Python function and class knowledge
- Basic understanding of API calls

**Objectives**:
- [ ] Create an agent with custom system prompt
- [ ] Understand system prompt override mechanics
- [ ] Test agent behavior variations
- [ ] Choose appropriate models for simple tasks

**Activities**:

#### Exercise 1: Build a Pong Agent (30 minutes)
```python
# Goal: Create agent that only responds with "pong"
# Skills: System prompt override, basic agent setup
# Model: Claude Haiku
```

**Steps**:
1. Create `pong_agent.py`
2. Define system prompt: "You are a pong agent. Always respond exactly with 'pong'."
3. Configure CloudCodeOptions with system prompt
4. Test with various user inputs
5. Verify consistent "pong" responses

**Success Criteria**: Agent responds with only "pong" to any input

#### Exercise 2: Build a Greeting Agent (45 minutes)
```python
# Goal: Create friendly greeter with personality
# Skills: Detailed system prompts, behavior control
# Model: Claude Haiku
```

**Steps**:
1. Create `greeting_agent.py`
2. Write system prompt with personality traits
3. Define greeting style (formal, casual, enthusiastic)
4. Test with different scenarios
5. Iterate on system prompt based on results

**Success Criteria**: Consistent personality across all greetings

#### Exercise 3: Build a Code Reviewer Agent (60 minutes)
```python
# Goal: Agent that reviews code for style issues only
# Skills: Domain-specific system prompts
# Model: Claude Sonnet
```

**Steps**:
1. Create `style_reviewer_agent.py`
2. Write system prompt focused on style guidelines
3. Define specific style rules to check
4. Test with sample code snippets
5. Analyze review quality and consistency

**Success Criteria**: Agent identifies style issues, ignores logic problems

**Deliverable**: Three working single-purpose agents with distinct behaviors

**Key Learnings**:
- System prompt is the most powerful control mechanism
- Specificity in system prompts improves consistency
- Model selection impacts response quality and cost
- Testing is essential to validate behavior

---

### Level 3: Custom Tools & MCP Servers (6-8 hours)

**Prerequisites**:
- Completed Level 2
- Understanding of Python decorators
- Knowledge of function parameters and return types

**Objectives**:
- [ ] Create custom tools using @tool decorator
- [ ] Write effective tool descriptions for agents
- [ ] Build an MCP server with multiple tools
- [ ] Integrate MCP servers into agents

**Activities**:

#### Exercise 4: Build an Echo Tool (60 minutes)
```python
# Goal: Create tool that echoes text with transformations
# Skills: Tool decorator, parameter handling, return values
# Model: Claude Haiku
```

**Steps**:
1. Create `echo_tool.py`
2. Define tool function with @tool decorator
3. Implement text transformations (reverse, uppercase, repeat)
4. Write clear tool description
5. Test tool independently
6. Create agent that uses the tool
7. Test agent's tool usage

**Success Criteria**: Agent correctly uses tool for transformations

**Code Template**:
```python
from claude_code_sdk import tool

@tool
def echo_tool(args: dict) -> str:
    """
    Echo text with optional transformations.

    Parameters:
    - text: The text to echo
    - reverse: Boolean to reverse the text
    - uppercase: Boolean to convert to uppercase
    - repeat: Number of times to repeat (default 1)
    """
    text = args.get("text", "")
    reverse = args.get("reverse", False)
    uppercase = args.get("uppercase", False)
    repeat = args.get("repeat", 1)

    if reverse:
        text = text[::-1]
    if uppercase:
        text = text.upper()

    result = (text + " ") * repeat
    return result.strip()
```

#### Exercise 5: Build a Calculator Tool Set (90 minutes)
```python
# Goal: Multiple math tools in one MCP server
# Skills: Multiple tools, MCP server creation, tool organization
# Model: Claude Haiku
```

**Steps**:
1. Create `calculator_tools.py`
2. Define basic math tools (add, subtract, multiply, divide)
3. Add advanced tools (power, sqrt, factorial)
4. Create MCP server with all tools
5. Build calculator agent using the server
6. Test complex calculations requiring multiple tools

**Success Criteria**: Agent chains multiple tools to solve problems

#### Exercise 6: Build a File System Tool (120 minutes)
```python
# Goal: Tools for file operations with safety checks
# Skills: Input validation, error handling, secure tools
# Model: Claude Sonnet
```

**Steps**:
1. Create `file_tools.py`
2. Define tools: read_file, write_file, list_files
3. Implement validation (path safety, file existence)
4. Add error handling with informative messages
5. Create MCP server
6. Build file assistant agent
7. Test with various file operations

**Success Criteria**: Safe file operations with proper error messages

**Deliverable**: Three MCP servers with different tool sets

**Key Learnings**:
- Tool descriptions directly affect agent behavior
- Input validation is critical for reliability
- MCP servers package tools for reusability
- Minimize tools to reduce context consumption

---

### Level 4: Conversation Management (4-5 hours)

**Prerequisites**:
- Completed Level 3
- Understanding of stateful vs stateless patterns

**Objectives**:
- [ ] Understand query vs Client usage
- [ ] Implement multi-turn conversations
- [ ] Manage conversation context
- [ ] Handle conversation state

**Activities**:

#### Exercise 7: One-Shot Query Pattern (45 minutes)
```python
# Goal: Simple question-answering without context
# Skills: query() function, single-turn interactions
# Model: Claude Haiku
```

**Steps**:
1. Create `one_shot_agent.py`
2. Use query() for independent prompts
3. Test with unrelated questions
4. Measure response times
5. Compare token usage to multi-turn

**Success Criteria**: Each query is independent, no context retention

#### Exercise 8: Conversation Client Pattern (90 minutes)
```python
# Goal: Multi-turn conversation with context
# Skills: ClaudeSDKClient, conversation state, context management
# Model: Claude Sonnet
```

**Steps**:
1. Create `conversation_agent.py`
2. Initialize ClaudeSDKClient with options
3. Implement conversation loop
4. Test context retention across turns
5. Monitor context window usage
6. Implement conversation reset when needed

**Success Criteria**: Agent remembers previous exchanges, provides contextual responses

#### Exercise 9: Context-Aware Assistant (120 minutes)
```python
# Goal: Build assistant that maintains long conversations
# Skills: Advanced context management, conversation summarization
# Model: Claude Sonnet
```

**Steps**:
1. Create `smart_assistant.py`
2. Implement conversation client with context tracking
3. Add context window monitoring
4. Implement auto-summarization when context fills
5. Test with long conversations (10+ turns)
6. Measure context efficiency

**Success Criteria**: Handles long conversations without context overflow

**Deliverable**: Three conversation patterns implemented

**Key Learnings**:
- query() for stateless, Client for stateful
- Context window is finite and valuable
- Summarization extends conversation length
- Monitor token usage continuously

---

### Level 5: Multi-Agent Orchestration (8-10 hours)

**Prerequisites**:
- Completed Level 4
- Understanding of workflows and pipelines
- Basic architecture design knowledge

**Objectives**:
- [ ] Design multi-agent workflows
- [ ] Implement agent-to-agent handoffs
- [ ] Build specialized agent roles
- [ ] Monitor and debug multi-agent systems

**Activities**:

#### Exercise 10: Two-Agent Pipeline (120 minutes)
```python
# Goal: Researcher → Writer workflow
# Skills: Agent handoff, output passing, role specialization
# Models: Sonnet for research, Haiku for writing
```

**Steps**:
1. Create `researcher_agent.py` (gathers information)
2. Create `writer_agent.py` (creates content from research)
3. Build `research_pipeline.py` orchestrator
4. Implement handoff: user query → researcher → writer → output
5. Test with various topics
6. Measure end-to-end time

**Success Criteria**: Coordinated research and writing, better than single agent

#### Exercise 11: Three-Agent Review System (180 minutes)
```python
# Goal: Generator → Reviewer → Editor workflow
# Skills: Multi-step processing, iterative improvement
# Models: Sonnet for generation/review, Haiku for editing
```

**Steps**:
1. Create `generator_agent.py` (creates initial content)
2. Create `reviewer_agent.py` (provides feedback)
3. Create `editor_agent.py` (applies improvements)
4. Build `content_pipeline.py` orchestrator
5. Implement feedback loop option
6. Test content quality improvement
7. Compare to single-agent approach

**Success Criteria**: Higher quality output than single-agent generation

#### Exercise 12: Micro-SDLC System (240 minutes)
```python
# Goal: Planner → Builder → Reviewer → Shipper
# Skills: Complex orchestration, specialized roles, error handling
# Models: Varied by agent role
```

**Steps**:
1. Create `planner_agent.py` (analyzes requirements, creates plan)
2. Create `builder_agent.py` (implements code from plan)
3. Create `reviewer_agent.py` (reviews code quality)
4. Create `shipper_agent.py` (prepares deployment artifacts)
5. Build `micro_sdlc.py` orchestrator
6. Add error handling and retry logic
7. Implement logging and monitoring
8. Test with real feature requests
9. Measure accuracy and time

**Success Criteria**: End-to-end feature implementation from description to code

**Deliverable**: Three working multi-agent systems

**Key Learnings**:
- Specialized agents outperform generalists
- Clear role definition is critical
- Handoff protocols need careful design
- Monitoring is essential for debugging

---

### Level 6: Production-Ready Agents (10-12 hours)

**Prerequisites**:
- Completed Level 5
- Understanding of error handling and logging
- Knowledge of deployment patterns

**Objectives**:
- [ ] Implement robust error handling
- [ ] Add comprehensive logging and monitoring
- [ ] Optimize for cost and performance
- [ ] Deploy agents to production

**Activities**:

#### Exercise 13: Error Handling & Retry Logic (120 minutes)
```python
# Goal: Production-grade error handling
# Skills: Exception handling, retry strategies, graceful degradation
```

**Implementation Areas**:
1. API failure handling (rate limits, timeouts)
2. Tool execution errors
3. Invalid input handling
4. Context overflow management
5. Retry with exponential backoff
6. Fallback behaviors

**Success Criteria**: Agent handles all error scenarios gracefully

#### Exercise 14: Logging & Monitoring (90 minutes)
```python
# Goal: Comprehensive observability
# Skills: Structured logging, metrics collection, debugging
```

**Implementation Areas**:
1. Request/response logging
2. Tool usage tracking
3. Token consumption metrics
4. Error rate monitoring
5. Performance timing
6. Cost tracking per agent

**Success Criteria**: Full visibility into agent operations

#### Exercise 15: Cost Optimization (120 minutes)
```python
# Goal: Minimize operational costs
# Skills: Model selection, caching, prompt optimization
```

**Optimization Strategies**:
1. Model selection analysis (Haiku vs Sonnet usage)
2. Prompt compression techniques
3. Response caching for repeated queries
4. Tool minimization per agent
5. Batch processing where possible

**Success Criteria**: 50%+ cost reduction without quality loss

#### Exercise 16: Production Deployment (180 minutes)
```python
# Goal: Deploy multi-agent system to production
# Skills: Containerization, API design, scaling
```

**Steps**:
1. Containerize agents (Docker)
2. Create REST API interface
3. Implement rate limiting
4. Add authentication/authorization
5. Set up monitoring and alerts
6. Deploy to cloud platform
7. Load test the system
8. Implement auto-scaling

**Success Criteria**: Production-ready, scalable agent system

**Deliverable**: Production-deployed multi-agent system

**Key Learnings**:
- Error handling is non-negotiable
- Monitoring enables rapid debugging
- Cost optimization is continuous
- Production requires different mindset than development

---

## Skill Validation Checkpoints

### Checkpoint 1: Basic Agent Creation
**Can you**:
- [ ] Explain what a system prompt does
- [ ] Create an agent with custom behavior
- [ ] Choose appropriate Claude model for a task
- [ ] Test agent behavior systematically

### Checkpoint 2: Tool Development
**Can you**:
- [ ] Create a custom tool with @tool decorator
- [ ] Write effective tool descriptions
- [ ] Build an MCP server with multiple tools
- [ ] Debug tool usage issues

### Checkpoint 3: Conversation Management
**Can you**:
- [ ] Explain query vs Client usage
- [ ] Implement multi-turn conversations
- [ ] Monitor context window consumption
- [ ] Handle context overflow scenarios

### Checkpoint 4: Multi-Agent Systems
**Can you**:
- [ ] Design agent workflows
- [ ] Implement agent handoffs
- [ ] Debug multi-agent interactions
- [ ] Measure system performance

### Checkpoint 5: Production Readiness
**Can you**:
- [ ] Implement comprehensive error handling
- [ ] Add logging and monitoring
- [ ] Optimize for cost and performance
- [ ] Deploy to production environment

---

## Practical Projects

After completing the learning path, build one of these projects:

### Project 1: Personal Research Assistant
**Complexity**: Medium
**Time**: 2-3 weeks
**Skills**: Multi-agent orchestration, tool development, conversation management

**Components**:
- Search agent (find sources)
- Analysis agent (extract insights)
- Synthesis agent (create reports)
- Citation agent (format references)

### Project 2: Code Review Automation
**Complexity**: Medium-High
**Time**: 3-4 weeks
**Skills**: Specialized agents, MCP servers, integration with Git

**Components**:
- Style checker agent
- Security analyzer agent
- Logic reviewer agent
- Performance optimizer agent
- Summary generator agent

### Project 3: Content Creation Pipeline
**Complexity**: Medium
**Time**: 2 weeks
**Skills**: Sequential agent workflows, content processing

**Components**:
- Idea generator agent
- Outline creator agent
- Content writer agent
- Editor agent
- SEO optimizer agent

### Project 4: Customer Support System
**Complexity**: Medium-High
**Time**: 3 weeks
**Skills**: Tiered agents, escalation logic, knowledge base integration

**Components**:
- FAQ agent (Tier 1)
- Technical support agent (Tier 2)
- Escalation agent (Tier 3)
- Knowledge base manager

---

## Common Pitfalls & Solutions

### Pitfall 1: Vague System Prompts
**Problem**: Agent behavior is inconsistent
**Solution**: Be extremely specific about expected behavior
**Example**: "Respond professionally" → "Respond in 2-3 sentences using formal business language without jargon"

### Pitfall 2: Too Many Tools
**Problem**: Agent confused about which tool to use, high context consumption
**Solution**: Minimize tools per agent, create specialized agents instead
**Example**: Don't give one agent 20 tools, create 4 agents with 5 tools each

### Pitfall 3: Wrong Model Selection
**Problem**: High costs or slow responses
**Solution**: Use Haiku for simple tasks, Sonnet for complex reasoning
**Example**: Greeting agent uses Haiku, legal analysis uses Sonnet

### Pitfall 4: No Error Handling
**Problem**: Agent crashes on unexpected input
**Solution**: Validate all inputs, handle API failures gracefully
**Example**: Wrap tool calls in try-except, implement retry logic

### Pitfall 5: Ignoring Context Window
**Problem**: Agent loses context mid-conversation
**Solution**: Monitor token usage, implement summarization
**Example**: Track context percentage, summarize when >80% full

### Pitfall 6: Poor Tool Descriptions
**Problem**: Agent doesn't use tools correctly
**Solution**: Write clear, specific tool descriptions with examples
**Example**: "Calculate" → "Calculate mathematical expressions. Use for: addition (2+2), multiplication (3*4), etc."

---

## Assessment Criteria

### Beginner Level
- Can create single-purpose agents
- Understands system prompt override
- Can choose appropriate models
- Can test agent behavior

### Intermediate Level
- Can create custom tools
- Can build MCP servers
- Can implement multi-turn conversations
- Can debug tool usage issues

### Advanced Level
- Can orchestrate multi-agent systems
- Can optimize for cost and performance
- Can implement production-ready error handling
- Can design complex agent workflows

### Expert Level
- Can architect large-scale agent systems
- Can optimize context consumption strategically
- Can implement advanced monitoring and observability
- Can mentor others in agent development

---

## Next Steps After Completion

1. **Join Community**: Engage with Claude Code SDK community
2. **Contribute**: Share your agents and tools
3. **Build Portfolio**: Create showcase of agent projects
4. **Explore Advanced**: Dive into agent-to-agent communication protocols
5. **Stay Updated**: Follow Claude API updates and new capabilities

---

## Recommended Resources

### Documentation
- Claude Code SDK Official Docs
- Anthropic API Documentation
- MCP Protocol Specification
- UV Package Manager Guide

### Videos
- IndyDevDan's "Agentic Coding ENDGAME" (this video)
- TAC Framework series (prerequisite)
- Additional Claude Code tutorials

### Tools
- VS Code with Python extension
- Claude Code CLI
- UV package manager
- Git for version control

### Community
- Claude Code GitHub Discussions
- Anthropic Developer Discord
- IndyDevDan YouTube channel comments

---

## Time Commitment Summary

- **Level 1 (Foundation)**: 2-3 hours
- **Level 2 (Single-Purpose)**: 4-6 hours
- **Level 3 (Tools & MCP)**: 6-8 hours
- **Level 4 (Conversations)**: 4-5 hours
- **Level 5 (Multi-Agent)**: 8-10 hours
- **Level 6 (Production)**: 10-12 hours

**Total**: 34-44 hours for complete mastery

**Recommended Pace**: 5-10 hours per week = 4-9 weeks to completion
