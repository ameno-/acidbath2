# Quick Start Guide
## Claude Code SDK Custom Agents - Rapid Implementation

---

## 5-Minute Setup

### Step 1: Install UV Package Manager (1 min)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Set API Key (1 min)
```bash
# Add to ~/.zshrc or ~/.bashrc
export ANTHROPIC_API_KEY="your-api-key-here"

# Reload shell
source ~/.zshrc  # or source ~/.bashrc
```

### Step 3: Create Project Directory (1 min)
```bash
mkdir claude-agents
cd claude-agents
uv init
```

### Step 4: Install Dependencies (1 min)
```bash
uv add claude-code-sdk rich
```

### Step 5: Verify Setup (1 min)
```bash
uv run python -c "from claude_code_sdk import CloudCodeOptions; print('Setup complete!')"
```

---

## 10-Minute First Agent

### Create `pong_agent.py`
```python
from claude_code_sdk import CloudCodeOptions, query

def main():
    # System prompt defines agent behavior
    system_prompt = """
    You are a pong agent.
    Always respond exactly with "pong" and nothing else.
    """

    # Configure agent options
    options = CloudCodeOptions(
        model="claude-3-haiku-20240307",  # Fast, cheap model
        system_prompt=system_prompt
    )

    # Test the agent
    test_prompts = [
        "Hello!",
        "What's your name?",
        "Can you help me code?",
        "ping"
    ]

    print("Testing Pong Agent:\n")
    for prompt in test_prompts:
        response = query(prompt, options)
        print(f"User: {prompt}")
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()
```

### Run It
```bash
uv run pong_agent.py
```

### Expected Output
```
Testing Pong Agent:

User: Hello!
Agent: pong

User: What's your name?
Agent: pong

User: Can you help me code?
Agent: pong

User: ping
Agent: pong
```

**Key Insight**: System prompt completely overrides default behavior!

---

## 20-Minute Custom Tool Agent

### Create `echo_agent.py`
```python
from claude_code_sdk import (
    CloudCodeOptions,
    ClaudeSDKClient,
    create_sdk_mcp_server,
    tool
)

# Define custom tool
@tool
def echo_transform(args: dict) -> str:
    """
    Echo text with optional transformations.

    Use this tool to transform text in the following ways:
    - reverse: Reverse the text
    - uppercase: Convert to uppercase
    - repeat: Repeat the text N times

    Parameters:
    - text (str): The text to transform
    - reverse (bool): Whether to reverse the text (default: false)
    - uppercase (bool): Whether to convert to uppercase (default: false)
    - repeat (int): How many times to repeat (default: 1)
    """
    text = args.get("text", "")
    reverse = args.get("reverse", False)
    uppercase = args.get("uppercase", False)
    repeat = args.get("repeat", 1)

    # Apply transformations
    if reverse:
        text = text[::-1]
    if uppercase:
        text = text.upper()

    # Repeat
    result = (text + " ") * repeat
    return result.strip()

def main():
    # System prompt for echo agent
    system_prompt = """
    You are an echo assistant that helps users transform text.

    You have access to an echo_transform tool that can:
    - Reverse text
    - Convert to uppercase
    - Repeat text multiple times

    When users ask for text transformations, use the tool.
    Explain what transformation you applied.
    """

    # Create MCP server with the tool
    mcp_server = create_sdk_mcp_server([echo_transform])

    # Configure agent with tool
    options = CloudCodeOptions(
        model="claude-3-haiku-20240307",
        system_prompt=system_prompt,
        mcp_servers=[mcp_server]
    )

    # Create client for conversation
    client = ClaudeSDKClient(options)

    # Test the agent
    print("Echo Agent with Custom Tools\n")

    prompts = [
        "Reverse the word 'hello'",
        "Make 'world' uppercase",
        "Repeat 'hi' three times",
        "Reverse 'Claude' and make it uppercase"
    ]

    for prompt in prompts:
        print(f"\nUser: {prompt}")
        response = client.query(prompt)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()
```

### Run It
```bash
uv run echo_agent.py
```

### Expected Output
```
Echo Agent with Custom Tools

User: Reverse the word 'hello'
Agent: I reversed "hello" to get "olleh"

User: Make 'world' uppercase
Agent: I converted "world" to uppercase: WORLD

User: Repeat 'hi' three times
Agent: I repeated "hi" three times: hi hi hi

User: Reverse 'Claude' and make it uppercase
Agent: I reversed and uppercased "Claude": EDUALC
```

**Key Insights**:
- Tools are defined with `@tool` decorator
- Tool description tells agent how to use it
- MCP servers package tools for agents
- Agent automatically knows when to use tools

---

## 30-Minute Multi-Agent System

### Create `researcher_writer.py`
```python
from claude_code_sdk import CloudCodeOptions, ClaudeSDKClient

class ResearchWriter:
    def __init__(self):
        self.researcher = self._create_researcher()
        self.writer = self._create_writer()

    def _create_researcher(self):
        """Create specialized research agent"""
        system_prompt = """
        You are a research specialist.

        When given a topic:
        1. Identify key aspects to research
        2. Outline important points to cover
        3. Provide factual information
        4. Structure findings clearly

        Focus on accuracy and completeness.
        Output your research as a structured outline.
        """

        options = CloudCodeOptions(
            model="claude-3-sonnet-20240229",  # Better for research
            system_prompt=system_prompt
        )

        return ClaudeSDKClient(options)

    def _create_writer(self):
        """Create specialized writing agent"""
        system_prompt = """
        You are a professional writer.

        When given research notes:
        1. Create engaging introduction
        2. Develop each point into a paragraph
        3. Add smooth transitions
        4. Write concise conclusion
        5. Use clear, accessible language

        Focus on readability and flow.
        Output a complete article.
        """

        options = CloudCodeOptions(
            model="claude-3-haiku-20240307",  # Cheaper for writing
            system_prompt=system_prompt
        )

        return ClaudeSDKClient(options)

    def create_article(self, topic: str) -> dict:
        """Process topic through research and writing pipeline"""
        print(f"\n{'='*60}")
        print(f"Creating article about: {topic}")
        print(f"{'='*60}\n")

        # Step 1: Research
        print("Step 1: Researching topic...")
        research_prompt = f"Research this topic and provide a structured outline: {topic}"
        research = self.researcher.query(research_prompt)
        print(f"\nResearch completed ({len(research)} characters)\n")

        # Step 2: Write
        print("Step 2: Writing article...")
        write_prompt = f"Turn this research into an engaging article:\n\n{research}"
        article = self.writer.query(write_prompt)
        print(f"\nArticle completed ({len(article)} characters)\n")

        return {
            "topic": topic,
            "research": research,
            "article": article
        }

def main():
    # Create multi-agent system
    system = ResearchWriter()

    # Test topics
    topics = [
        "The benefits of Claude Code SDK for developers",
        "How multi-agent systems improve productivity"
    ]

    for topic in topics:
        result = system.create_article(topic)

        print(f"\n{'='*60}")
        print("FINAL ARTICLE")
        print(f"{'='*60}\n")
        print(result["article"])
        print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
```

### Run It
```bash
uv run researcher_writer.py
```

### Expected Behavior
```
============================================================
Creating article about: The benefits of Claude Code SDK for developers
============================================================

Step 1: Researching topic...

Research completed (847 characters)

Step 2: Writing article...

Article completed (1234 characters)

============================================================
FINAL ARTICLE
============================================================

[Complete article text here]

============================================================
```

**Key Insights**:
- Different agents for different roles
- Researcher uses Sonnet (complex analysis)
- Writer uses Haiku (simpler task)
- Agent handoff through prompt passing
- Specialized system prompts per role

---

## Common Patterns Cheat Sheet

### Pattern 1: One-Shot Query
**Use When**: Single, independent requests
**Cost**: Low (one call)
**Code**:
```python
from claude_code_sdk import CloudCodeOptions, query

options = CloudCodeOptions(system_prompt="Your prompt")
response = query("User input", options)
```

### Pattern 2: Conversation Client
**Use When**: Multi-turn conversation with context
**Cost**: Higher (maintains context)
**Code**:
```python
from claude_code_sdk import CloudCodeOptions, ClaudeSDKClient

options = CloudCodeOptions(system_prompt="Your prompt")
client = ClaudeSDKClient(options)

response1 = client.query("First question")
response2 = client.query("Follow-up question")  # Has context
```

### Pattern 3: Custom Tools
**Use When**: Need deterministic operations
**Cost**: Same as base, tools don't add cost
**Code**:
```python
from claude_code_sdk import tool, create_sdk_mcp_server, CloudCodeOptions

@tool
def my_tool(args: dict) -> str:
    """Tool description for the agent"""
    return "result"

mcp_server = create_sdk_mcp_server([my_tool])
options = CloudCodeOptions(mcp_servers=[mcp_server])
```

### Pattern 4: Multi-Agent Pipeline
**Use When**: Complex workflows with specialization
**Cost**: Multiple calls (one per agent)
**Code**:
```python
class Pipeline:
    def __init__(self):
        self.agent1 = create_agent("prompt1", "haiku")
        self.agent2 = create_agent("prompt2", "sonnet")

    def process(self, input):
        result1 = self.agent1.query(input)
        result2 = self.agent2.query(result1)
        return result2
```

---

## Model Selection Quick Guide

### Use Claude Haiku When:
- Simple, straightforward tasks
- High-volume operations
- Cost optimization is priority
- Speed is important
- Examples: Greetings, simple transforms, classification

**Pricing**: ~Cheapest
**Speed**: ~Fastest

### Use Claude Sonnet When:
- Complex reasoning required
- Quality matters more than cost
- Moderate task complexity
- Examples: Research, analysis, code review, content creation

**Pricing**: ~Medium
**Speed**: ~Medium

### Use Claude Opus When:
- Extremely complex tasks
- Highest quality needed
- Cost is not a concern
- Examples: Advanced coding, deep analysis, complex decision making

**Pricing**: ~Most expensive
**Speed**: ~Slowest

---

## Troubleshooting Guide

### Problem: Agent not behaving as expected
**Solution**: Check system prompt specificity
```python
# Bad: Vague
system_prompt = "Be helpful"

# Good: Specific
system_prompt = """
You are a code reviewer.
Only check for:
1. PEP 8 style violations
2. Missing docstrings
3. Variable naming issues

Do NOT review logic or performance.
Output findings as a numbered list.
"""
```

### Problem: Agent not using tools
**Solution**: Improve tool description
```python
# Bad: Unclear
@tool
def process(args: dict) -> str:
    """Processes data"""
    pass

# Good: Clear with examples
@tool
def process(args: dict) -> str:
    """
    Process text data by removing special characters.

    Use this when user wants to clean text data.

    Examples:
    - "Clean this text: Hello@World!" -> "Hello World"
    - "Remove special chars from: test#123" -> "test 123"

    Parameters:
    - text (str): The text to clean
    """
    pass
```

### Problem: High costs
**Solutions**:
1. Use Haiku instead of Sonnet for simple tasks
2. Minimize system prompt length
3. Reduce tool count per agent
4. Use query() instead of Client when context not needed

### Problem: Context overflow
**Solutions**:
1. Monitor context with token counting
2. Implement conversation summarization
3. Reset conversation when context full
4. Minimize tool descriptions

### Problem: Slow responses
**Solutions**:
1. Use Haiku for speed-critical tasks
2. Reduce system prompt length
3. Minimize number of tools
4. Consider caching repeated queries

---

## Best Practices Summary

### System Prompts
1. Be extremely specific about behavior
2. Define exact output format
3. List what NOT to do
4. Keep concise but complete
5. Test with edge cases

### Tool Development
1. Write clear descriptions with examples
2. Validate all inputs
3. Return consistent output format
4. Handle errors gracefully
5. Keep tools focused (single responsibility)

### Model Selection
1. Start with Haiku, upgrade if needed
2. Match model to task complexity
3. Monitor costs per agent
4. Don't over-engineer simple tasks

### Agent Design
1. One agent, one purpose
2. Minimize tool count
3. Test behavior thoroughly
4. Monitor token usage
5. Iterate based on real usage

### Multi-Agent Systems
1. Define clear agent roles
2. Design explicit handoff protocols
3. Implement error handling
4. Add logging and monitoring
5. Start simple, add complexity gradually

---

## Next Steps

### Beginner
1. Build the three examples above
2. Modify system prompts and observe changes
3. Create 2-3 custom tools
4. Experiment with different models

### Intermediate
1. Build a 2-3 agent pipeline for real task
2. Create an MCP server with 5+ tools
3. Implement conversation management
4. Add error handling and logging

### Advanced
1. Build production multi-agent system
2. Optimize costs by 50%+
3. Implement monitoring and analytics
4. Create reusable agent framework

---

## Essential Commands Reference

```bash
# Setup
curl -LsSf https://astral.sh/uv/install.sh | sh
export ANTHROPIC_API_KEY="your-key"

# Project init
uv init
uv add claude-code-sdk rich

# Run agents
uv run agent_name.py

# Development
uv add --dev pytest  # Testing
uv run pytest        # Run tests

# Verify setup
uv run python -c "from claude_code_sdk import CloudCodeOptions; print('OK')"
```

---

## File Structure Template

```
my-agents/
├── pyproject.toml          # UV config
├── .env                    # API keys (DON'T COMMIT!)
├── agents/
│   ├── __init__.py
│   ├── pong_agent.py       # Simple example
│   ├── echo_agent.py       # Tool example
│   └── researcher.py       # Multi-agent example
├── tools/
│   ├── __init__.py
│   ├── text_tools.py       # Text processing tools
│   └── file_tools.py       # File operations tools
├── prompts/
│   ├── researcher.txt      # System prompts
│   └── writer.txt
└── tests/
    ├── test_agents.py
    └── test_tools.py
```

---

## Quick Wins (30 mins each)

### Win 1: Custom Greeter
Make an agent with your personality that greets users

### Win 2: Text Transformer
Create tools: uppercase, lowercase, reverse, leetspeak

### Win 3: Code Explainer
Agent that explains code in simple terms

### Win 4: Meeting Summarizer
Agent that summarizes meeting notes into action items

### Win 5: Git Message Generator
Agent that creates conventional commit messages

---

## Resources

- **Video**: IndyDevDan - "Agentic Coding ENDGAME" (16:56)
- **Docs**: Claude Code SDK documentation
- **API**: Anthropic Claude API docs
- **Community**: Anthropic Discord, GitHub Discussions
- **Tools**: UV package manager, Rich library

---

**You're ready to build! Start with the 10-minute first agent and go from there.**
