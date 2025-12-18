# SUMMARY

Agentic engineering tutorial by an unnamed creator demonstrating custom agent development using Claude Code SDK, progressing from simple pong agents to multi-agent SDLC systems.

# IDEAS

- Agentic engineering follows a predictable progression: better agents, more agents, then custom agents for maximum impact
- Out-of-the-box agents are built for everyone's codebase, not yours, creating massive inefficiency costs
- Custom agents solve the hard specific problems that most engineers and generic agents cannot handle
- The system prompt is the single most important element of custom agents with zero exceptions
- System prompts affect every single user prompt the agent runs, multiplying all your work
- When you modify the system prompt, you completely change the product - it's no longer Claude Code anymore
- Custom agents require mastering the "core four" elements to understand compute scaling
- The Claude Code SDK enables incremental adoption of custom agent capabilities
- Tools consume context window space in your agent's mind, requiring careful management
- Multi-agent systems can orchestrate complex workflows like software development lifecycles
- Agent coding is shifting from "what we can do" to "what we can teach our agents to do"
- Custom agents work best for specialized, high-return-on-investment problems in your domain
- The mismatch between generic tools and specific codebases costs hundreds of hours and millions of tokens
- Cheaper, faster models like Claude Haiku can be effective for simple custom agent tasks
- Continuous conversations require the Claude SDK client class instead of one-off query commands
- MCP servers can be built in memory within scripts for powerful custom tool integration
- Permission systems and tool interception can be built into multi-agent workflows
- Agent perspective adoption is crucial for improving and managing custom agents effectively
- Out-of-loop review systems using the Peter framework enable zero-touch execution
- Custom agents should focus on repeat workflows that benefit from automation within your specific constraints

# QUOTES

- "Better agents, more agents, and then custom agents."
- "They're built for everyone's codebase, not yours."
- "This is where all the alpha is in engineering. It's in the hard specific problems that most engineers and most agents can't solve out of the box."
- "The system prompt is the most important element of your custom agents with zero exceptions."
- "All of your work is multiplied by your system prompt."
- "We have completely overwritten the clawed code system prompt."
- "The system prompt is truly what builds the agent."
- "If you understand the core 4 and how each element flows and controls your agent, you will understand compute."
- "This is not clawed code anymore."
- "Agent coding is not so much about what we can do anymore. It's about what we can teach our agents to do."
- "If you don't know what your agent is doing, if you don't adopt your agent's perspective, it will be hard to improve them."
- "Everything that's going into your agent winds up in the context window at some point."
- "As soon as you touch the system prompt and once you start dialing into the tools, you change the product, you change the agent."
- "If you don't need to reinvent the wheel, don't do it."
- "This work shipped with a single prompt outside the loop."
- "Deploying effective compute and deploying effective agents is all about finding the constraints in your personal workflow."

# FACTS

- The Claude Code SDK allows building custom agents with modified system prompts and tools
- MCP servers can be created in memory within Python scripts for custom tool integration
- Claude Haiku is a cheaper, less intelligent but faster model suitable for simple agent tasks
- The Claude SDK client class enables continuous conversations while query commands are for one-off prompts
- Out-of-the-box Claude Code comes with 15 built-in tools that consume context window space
- Multi-agent systems can orchestrate software development lifecycles with planning, building, reviewing, and shipping phases
- WebSocket connections can stream agent messages and tool calls to front-end interfaces in real-time
- System prompts can either completely overwrite or append to existing agent instructions
- Tool descriptions help agents understand how to use custom functions in addition to parameter specifications
- Agent message blocks, tool use blocks, and text blocks are the core response types from custom agents

# REFERENCES

- Claude Code SDK
- Codeex CLI
- Gemini CLI
- Peter framework
- TAC lessons
- UV (Python package manager)
- MCP (Model Context Protocol)
- WebSocket technology
- Rich Python library for logging
- Out-of-loop review systems

# RECOMMENDATIONS

- Master single agent prompt and context engineering before scaling to multiple agents
- Use out-of-the-box agents for one-size-fits-all work rather than over-engineering custom solutions
- Focus custom agent development on specialized, domain-specific problems with high ROI
- Carefully manage the system prompt as it affects every user interaction with your agent
- Monitor and control tool sets to avoid unnecessary context window consumption
- Use cheaper models like Claude Haiku for simple custom agent tasks to optimize costs
- Implement permission systems and tool interception for multi-agent workflows
- Build agent perspective adoption into your development process for better debugging and improvement
- Deploy agents across repeat workflows that benefit from automation within your specific constraints
- Progress systematically from better agents to more agents to custom agents for maximum impact
- Use the Claude SDK client for continuous conversations and query commands for one-off prompts
- Create MCP servers in memory for powerful custom tool integration without external dependencies
- Implement real-time streaming of agent messages to user interfaces via WebSocket connections
- Focus on transitioning from in-loop to out-loop to zero-touch execution patterns
- Find and address constraints in your personal workflow and products before building custom agents
