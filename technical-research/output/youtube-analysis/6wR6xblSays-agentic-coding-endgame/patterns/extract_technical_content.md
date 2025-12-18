# TECH_STACK

### Languages
- Python - Primary language for all custom agent implementations
- JavaScript/TypeScript - Frontend implementation for multi-agent UI
- HTML - Web interface structure

### Frameworks & Libraries
- Claude Code SDK - Core framework for building custom agents
- Rich - Python library for terminal formatting and panels
- WebSockets - Real-time communication between frontend and backend agents
- UV - Python package management and execution

### Tools & Platforms
- Claude Code - Base agent platform and tooling
- Claude Haiku - Faster, cheaper model for simple agent tasks
- MCP (Model Context Protocol) - Server protocol for tool integration

### Services & APIs
- Anthropic Claude API - Underlying language model service

## CODE_SNIPPETS

### Snippet 1: Basic Agent Setup with System Prompt Override
**Context**: Setting up a simple pong agent with custom system prompt
**Timestamp**: 02:47

```python
from claude_code_sdk import CloudCodeOptions

def load_system_prompt():
    return """
    You are a pong agent.
    Always respond exactly with "pong".
    """

options = CloudCodeOptions(
    system_prompt=load_system_prompt()
)
```

**Explanation**: Completely overrides the default Claude Code system prompt with custom behavior
**Key Points**: System prompt is the most important element - it affects every single user prompt

### Snippet 2: Custom Tool Definition
**Context**: Creating a custom echo tool for the echo agent
**Timestamp**: 06:50

```python
@tool
def echo_tool(args: dict) -> str:
    """Echo text with transformations like reverse, uppercase, repeat"""
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

**Explanation**: Custom tools use decorators and receive dict arguments, returning deterministic results
**Key Points**: Tool descriptions tell the agent how to use them; you step back into traditional deterministic code

### Snippet 3: MCP Server Creation
**Context**: Building an in-memory MCP server for custom tools
**Timestamp**: 06:54

```python
from claude_code_sdk import create_sdk_mcp_server

mcp_server = create_sdk_mcp_server([echo_tool])

options = CloudCodeOptions(
    model="claude-3-haiku-20240307",
    mcp_servers=[mcp_server]
)
```

**Explanation**: Creates an entire MCP server in memory with custom tools for the agent
**Key Points**: Powerful way to package custom functionality; allows precise tool control

### Snippet 4: Client vs Query Usage
**Context**: Difference between one-off prompts and continuous conversations
**Timestamp**: 08:20

```python
# For one-off prompts
result = query(user_prompt, options)

# For continuous conversations  
client = ClaudeSDKClient(options)
response1 = client.query(user_prompt)
response2 = client.query(follow_up_prompt)  # Maintains conversation context
```

**Explanation**: Query is for single interactions, Client maintains conversation history
**Key Points**: Client enables multi-turn conversations with context retention

### Snippet 5: Multi-Agent Orchestration Structure
**Context**: Setting up multiple specialized agents in workflow
**Timestamp**: 13:00

```python
class MicroSDLCAgent:
    def __init__(self):
        self.planner_agent = self.create_agent("planner")
        self.builder_agent = self.create_agent("builder") 
        self.reviewer_agent = self.create_agent("reviewer")
        self.shipper_agent = self.create_agent("shipper")
    
    def process_task(self, task):
        plan = self.planner_agent.query(task)
        implementation = self.builder_agent.query(plan)
        review = self.reviewer_agent.query(implementation)
        return self.shipper_agent.query(review)
```

**Explanation**: Each agent has specialized role in software development lifecycle
**Key Points**: Demonstrates agent-to-agent handoff in structured workflow

## COMMANDS & SCRIPTS

### Installation & Setup
```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies (implied from UV usage)
uv sync
```

### Configuration
```bash
# Set up Claude API key (implied)
export ANTHROPIC_API_KEY="your-key-here"
```

### Execution & Testing
```bash
# Run pong agent
uv run pong_agent.py

# Run echo agent
uv run echo_agent.py

# Run multi-agent SDLC system
uv run micro_sdlc_agent.py
```

### Deployment
```bash
# Start backend and frontend for multi-agent UI
# (Commands not explicitly shown but implied from demo)
```

## TECHNICAL_CONCEPTS

### Architectural Patterns
- **System Prompt Override**: Complete replacement of default agent behavior - changes everything about the agent
- **Multi-Agent Orchestration**: Specialized agents working together in defined workflows
- **MCP Server Pattern**: In-memory tool servers for custom agent capabilities
- **Out-of-Loop Review**: Agents operating without human intervention in the workflow

### Design Principles
- **Core Four Elements**: User prompt, agent response, tool calls, and system prompt control agent behavior
- **Incremental Adoption**: Start with out-of-box agents, then better/more/custom agents
- **Tool Minimalism**: Only include tools the agent actually needs to reduce context consumption

### Best Practices
- **System Prompt is King**: Most important element affecting every interaction
- **Context Management**: Be aware that all tools consume space in agent's "mind"
- **Model Selection**: Use cheaper/faster models (like Haiku) for simple tasks
- **Deterministic Tools**: Custom tools should provide predictable, reliable functionality

### Common Pitfalls
- **Tool Bloat**: Including unnecessary tools that consume context without value
- **One-Size-Fits-All**: Using generic agents for specialized work that needs custom solutions
- **Ignoring Context**: Not understanding what goes into the agent's context window

## DEPENDENCIES & REQUIREMENTS

### System Requirements
- Python 3.8+ - For Claude Code SDK compatibility
- Node.js - For frontend components (implied from UI demo)

### Package Dependencies
- claude-code-sdk - Core agent framework
- rich - Terminal formatting and logging
- anthropic - Claude API client (implied)
- websockets - Real-time communication (implied)

### Environment Variables
```bash
ANTHROPIC_API_KEY=your_claude_api_key_here
```

### Prerequisites
- Anthropic API access - Required for Claude model usage
- Understanding of TAC (Think, Act, Check) framework - Referenced as prerequisite knowledge

## RESOURCES & LINKS

### Official Documentation
- Claude Code SDK Documentation: (URL not provided in transcript)
- Anthropic Claude API Docs: (URL not provided in transcript)

### Repository Links
- Building Specialized Agents Codebase: Contains 8 custom agent examples (URL not provided)

### Related Tools & Extensions
- UV Package Manager: Modern Python package management
- Rich Library: Python library for rich text and beautiful formatting
- MCP Protocol: Model Context Protocol for tool integration

### Learning Resources
- TAC Framework Lessons: Referenced as prerequisite for understanding in-loop vs out-loop workflows

### Community & Support
- None identified

## CONFIGURATION_FILES

### System Prompt File
**Purpose**: Defines agent behavior and personality
**Location**: Configurable path in agent setup

```text
You are a pong agent.
Always respond exactly with "pong".
```

### Agent Configuration
**Purpose**: Sets up agent options and capabilities
**Location**: Within Python agent scripts

```python
options = CloudCodeOptions(
    model="claude-3-haiku-20240307",
    system_prompt=load_system_prompt(),
    mcp_servers=[custom_mcp_server]
)
```

## WORKFLOW_STEPS

### Setup Process
1. Install UV package manager for Python dependency management
2. Set up Anthropic API key in environment variables
3. Install required dependencies using UV
4. Create system prompt files for custom agent behavior

### Development Workflow
1. Define agent purpose and create system prompt
2. Implement custom tools using @tool decorator
3. Create MCP server with custom tools if needed
4. Set up CloudCodeOptions with model and configuration
5. Test agent with simple prompts to verify behavior

### Testing & Validation
1. Run agent with test prompts to verify system prompt override
2. Check tool functionality with various input parameters
3. Validate conversation continuity with SDK client
4. Monitor context consumption and tool usage

### Deployment Process
1. Package agents into appropriate runtime environments
2. Set up WebSocket connections for real-time UI updates
3. Deploy multi-agent systems with proper orchestration
4. Monitor agent performance and adjust model selection

## AUTOMATION_OPPORTUNITIES

- **Agent Workflow Orchestration**: Automate handoffs between specialized agents in multi-step processes
- **Context Optimization**: Automatically select minimal tool sets based on task requirements
- **Model Selection**: Dynamic model selection based on task complexity (Haiku for simple, Sonnet for complex)
- **System Prompt Management**: Version control and testing framework for system prompts
- **Tool Usage Analytics**: Monitor which tools are actually used to optimize agent configurations

## TECHNICAL_NOTES

### Performance Considerations
- Use Claude Haiku for simple tasks to reduce cost and increase speed
- Minimize tool sets to reduce context window consumption
- Consider conversation length when using SDK client vs single query

### Security Considerations
- System prompt override completely changes agent behavior - validate thoroughly
- Custom tools execute deterministic code - ensure proper input validation
- API key management for Anthropic services

### Compatibility Notes
- Claude Code SDK version compatibility with different Claude models
- MCP server protocol compatibility across different tool implementations
- WebSocket connection handling for real-time multi-agent UIs

### Troubleshooting Tips
- **Agent not responding as expected**: Check system prompt override and tool descriptions
- **Context window issues**: Reduce number of tools or conversation length
- **Tool not being used**: Verify tool description clearly explains when and how to use it

## QUICK_REFERENCE

### Essential Commands
```bash
# Run basic agent
uv run agent_name.py

# Check tool availability
# (Use agent prompt: "list your available tools")

# Start multi-agent system
uv run micro_sdlc_agent.py
```

### Key File Locations
- System Prompts: Configurable file paths defined in agent setup
- Agent Scripts: Python files with CloudCodeOptions configuration
- Custom Tools: Defined with @tool decorator in agent modules

### Important URLs
- Claude Code SDK: (Documentation URL not provided)
- Anthropic Console: For API key management
- MCP Protocol Specs: For custom tool development
