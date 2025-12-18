# SUMMARY

Instructor demonstrates custom agent engineering using Claude Code SDK, showcasing eight specialized agents from simple pong to complex multi-agent systems.

# IDEAS

- Agentic engineering follows predictable progression: better agents, more agents, then custom specialized agents for specific domains.
- Out-of-box agents work for everyone's codebase but create massive inefficiencies scaling with your specific problems.
- System prompts are most important element of custom agents, multiplying effect of every user prompt interaction.
- Custom agents require careful balance between model intelligence, speed, and cost for specific use cases.
- Multi-agent orchestration enables complex workflows like software development lifecycle automation with specialized agent roles.
- Agent coding shifts focus from what we can do to what we teach agents to do.
- Context window management becomes critical when agents carry unnecessary tools consuming valuable computational space.
- Custom tools enable agents to perform deterministic operations while maintaining conversational flow and memory.
- Claude SDK client enables continuous conversations while query method handles single prompt-response interactions effectively.
- System prompt modifications completely change agent behavior, essentially creating new products from existing models.
- MCP servers can be built in-memory for agents, providing powerful tool integration capabilities.
- Agent perspective adoption is crucial for improving, tweaking, and managing custom agent performance effectively.
- Specialized agents solve hard problems that general-purpose agents and engineers cannot handle out-of-box.
- Agent workflows can operate on themselves, creating self-modifying systems with real-time updates and improvements.
- Permission systems and tool interception provide necessary control mechanisms for multi-agent system security.
- WebSocket integration enables real-time agent communication and status updates for user interface applications.
- Out-loop review systems using specialized frameworks enable autonomous quality control without human intervention required.
- Agent deployment should target repeat workflows with high return on investment for teams and businesses.
- Custom agents excel at domain-specific problems, edge cases, and specialized workflows unique to organizations.
- Tool descriptions guide agent behavior as much as actual parameters and arguments passed to functions.
- Model selection affects agent capabilities: cheaper models for simple tasks, powerful models for complex reasoning.
- Agent message blocks and result messages provide structured data parsing opportunities for system integration.
- Custom agents can downgrade from powerful models to faster, cheaper alternatives for appropriate tasks.
- Incremental adoption of SDK features allows gradual transition from simple to complex agent implementations.
- Agent compute scaling requires understanding constraints in personal workflows and product development processes effectively.

# INSIGHTS

- System prompts fundamentally redefine agents, transforming existing models into entirely new specialized computational products.
- Agent engineering progression mirrors software development: start simple, add complexity, then customize for domains.
- Context window efficiency becomes critical constraint as agents scale, requiring careful tool selection and management.
- Multi-agent systems enable complex orchestration by distributing specialized tasks across purpose-built computational entities.
- Custom agents unlock value by solving organization-specific problems that general-purpose tools cannot address effectively.
- Agent perspective adoption is essential for debugging, optimization, and understanding computational decision-making processes.
- Tool integration bridges deterministic programming with conversational AI, combining predictable operations with intelligent reasoning.
- Model selection should match task complexity: avoid over-engineering simple problems with expensive computational resources.
- Agent workflows can achieve self-modification, creating systems that improve and update themselves autonomously over time.
- Effective agent deployment targets repetitive high-value workflows where automation provides significant productivity multipliers.

# QUOTES

- "Better agents, more agents, and then custom agents. If you can prompt engineer and context engineer a single agent successfully, then the next step is to add more agents."
- "They're built for everyone's codebase, not yours. This mismatch can cost you hundreds of hours and millions of tokens scaling as your codebase grows."
- "This is where all the alpha is in engineering. It's in the hard specific problems that most engineers and most agents can't solve out of the box."
- "The system prompt is the most important element of your custom agents with zero exceptions."
- "All of your work is multiplied by your system prompt."
- "Remember all that work that the clawed code team has put into making a great agent, right? The claw code agent that you know and love is now gone."
- "The system prompt is truly what builds the agent."
- "If you understand the core 4 and how each element flows and controls your agent, you will understand compute and you'll understand how to scale your compute."
- "If you don't know what your agent is doing, if you don't adopt your agent's perspective, it will be hard to improve them and tweak them and manage them."
- "As soon as you touch the system prompt and once you start dialing into the tools, you change the product, you change the agent."
- "Agent coding is not so much about what we can do anymore. It's about what we can teach our agents to do."
- "This is how we push our compute to its useful limits."
- "Deploying effective compute and deploying effective agents is all about finding the constraints in your personal workflow and in your products."
- "If you're doing one-sizefits-all work, use the out-of-the-box agent. Don't think super hard about this. Just deploy compute to get the job done."
- "But as your work becomes more specialized, as you deploy agents across all aspects of your engineering, you first want better agents, more agents, and then custom agents."

# HABITS

- Always examine system prompts first when analyzing custom agents to understand their fundamental behavioral modifications.
- Search for "cloud code options" to quickly identify agent configuration and understand computational resource allocation.
- Collapse code sections to rapidly understand overall structure before diving into implementation details and specifics.
- Monitor agent message blocks and result messages to parse structured data and understand agent reasoning.
- Use rich panels for clean logging to clearly communicate agent activities and decision-making processes.
- Track core four elements (system prompts, user prompts, tools, responses) to understand agent behavior.
- Adopt agent perspective by monitoring their activities to improve debugging and optimization capabilities effectively.
- Start with simple agents before progressing to complex multi-agent systems to build foundational understanding.
- Use cheaper models for simple tasks and reserve powerful models for complex reasoning requirements.
- Implement permission systems and tool interception for security in multi-agent system deployments and operations.
- Build MCP servers in-memory for efficient tool integration without external infrastructure complexity and overhead.
- Use Claude SDK client for continuous conversations and query method for single prompt-response interactions.
- Monitor context window usage to identify unnecessary tools consuming valuable computational space and resources.
- Test agent capabilities by asking them to list available tools to understand their operational scope.
- Implement websocket integration for real-time agent communication and status updates in user interface applications.
- Target repeat workflows with high ROI when deploying agents for maximum productivity and business impact.
- Use out-of-box tools when possible instead of reinventing functionality that already exists and works.
- Implement out-loop review systems for autonomous quality control without requiring constant human intervention and oversight.
- Focus on domain-specific problems and edge cases where custom agents provide maximum value over solutions.
- Practice incremental adoption of SDK features to gradually build complexity and understanding over time.

# FACTS

- Claude Code SDK enables building custom agents with complete control over system prompts and tools.
- System prompts affect every single user prompt interaction, multiplying the impact of customization efforts.
- Out-of-box agents carry approximately 15 additional tools that consume context window space unnecessarily for tasks.
- MCP servers can be created in-memory using the SDK, eliminating need for external infrastructure.
- Claude Haiku model provides faster, cheaper alternative to more powerful models for simple agent tasks.
- Agent message blocks and result messages provide structured data that can be parsed for integration.
- WebSocket connections enable real-time communication between agents and user interfaces for live updates.
- Multi-agent systems can implement software development lifecycle automation with specialized roles and handoffs.
- Custom agents can operate on themselves, creating self-modifying systems with real-time capability updates.
- Tool descriptions guide agent behavior as much as actual parameters passed to function calls.
- Context window efficiency becomes critical constraint as agent complexity and tool sets scale upward.
- Agent workflows can achieve autonomous operation without human intervention using out-loop review systems.
- Custom agents excel at solving organization-specific problems that general-purpose tools cannot address.
- Model selection directly impacts agent performance, cost, and speed for different computational task types.
- Agent compute scaling requires identifying constraints in personal workflows and product development processes effectively.
- Permission systems provide necessary security controls for multi-agent system deployments in production environments.
- Incremental SDK feature adoption allows gradual transition from simple to complex agent implementation strategies.
- Agent perspective adoption is essential for debugging, optimization, and understanding decision-making processes within systems.
- Custom tools enable deterministic operations while maintaining conversational flow and memory across agent interactions.
- Agent engineering follows predictable progression from better agents to more agents to custom agents.

# REFERENCES

- Claude Code SDK
- Claude Haiku model
- MCP (Model Context Protocol) servers
- TAC lessons (mentioned as prerequisite)
- Peter framework for out-loop review systems
- WebSocket technology for real-time communication
- Rich panels for logging and display
- UV run command for Python execution
- Agentic Horizon extended lessons series

# ONE-SENTENCE TAKEAWAY

Custom agents solve specialized problems by controlling system prompts, tools, and workflows.

# RECOMMENDATIONS

- Start with simple pong agents to understand system prompt control before building complex systems.
- Use cheaper models like Claude Haiku for simple tasks to optimize cost and speed.
- Monitor context window usage and remove unnecessary tools that consume valuable computational space.
- Implement permission systems and tool interception for security in multi-agent production deployments.
- Build MCP servers in-memory using SDK to avoid external infrastructure complexity and overhead.
- Adopt agent perspective by monitoring activities to improve debugging and optimization capabilities effectively.
- Use out-of-box tools when possible instead of reinventing existing functionality that works.
- Target repeat workflows with high ROI when deploying agents for maximum productivity impact.
- Implement websocket integration for real-time agent communication and status updates in applications.
- Practice incremental SDK feature adoption to gradually build complexity and understanding over time.
- Focus on domain-specific problems where custom agents provide maximum value over general solutions.
- Use Claude SDK client for conversations and query method for single prompt-response interactions.
- Implement out-loop review systems for autonomous quality control without requiring human intervention.
- Search for "cloud code options" to quickly identify agent configuration and resource allocation.
- Collapse code sections first to understand overall structure before diving into implementation details.
- Track core four elements (prompts, tools, responses) to understand and control agent behavior.
- Use rich panels for clean logging to clearly communicate agent activities and processes.
- Test agent capabilities by asking them to list available tools to understand scope.
- Start with better agents, progress to more agents, then advance to custom specialized agents.
- Deploy agents across repeat workflows that benefit from automation and computational scaling effectively.
