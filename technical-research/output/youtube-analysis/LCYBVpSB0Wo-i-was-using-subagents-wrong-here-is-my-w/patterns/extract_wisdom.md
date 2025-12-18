OAuth token expired, refreshing...
Token refresh failed, re-authenticating...
# SUMMARY

Jason demonstrates best practices for using Claude Code's sub-agent feature effectively, focusing on research-oriented tasks rather than direct implementation to improve AI coding workflows.

# IDEAS

- Claude Code's sub-agent feature was initially exciting but often delivered poor user experiences
- Sub-agents consume massive tokens and feel slow without contributing to better results significantly
- Context engineering and optimization are the core purposes behind Claude Code's sub-agent functionality
- File system serves as ultimate context management system for long-running AI agent tasks
- Sub-agents work best when focused on information gathering and providing small summary reports
- Each sub-agent should be considered almost as a researcher rather than implementation executor
- Context sharing across different agents remains a major challenge in current sub-agent implementations
- Specialized sub-agents for each service provider can dramatically improve coding workflow effectiveness
- MCP tools enable sub-agents to retrieve relevant components and design patterns efficiently
- Documentation should be included directly in system prompts for latest practice adherence
- Parent agents should always maintain project plans in centralized context files for coordination
- Sub-agents must read context files before starting work and update them after completion
- Output format instructions help ensure consistent communication between sub-agents and parent agents
- Background sessions in Claude Code allow continuous monitoring and execution of long tasks
- Context files prevent information loss during conversation compacting which degrades AI performance significantly

# INSIGHTS

- Sub-agents excel at research and planning but struggle with direct implementation due to context limitations
- File-based context management prevents token bloat while maintaining essential information for AI agents
- Specialized expertise through documentation embedding creates more effective sub-agents than generalist approaches
- Parent-child agent communication requires structured protocols to maintain project coherence and prevent confusion
- Context preservation across agent interactions is crucial for maintaining high-quality AI coding assistance
- Research-focused sub-agents provide better value than implementation-focused ones in current AI coding workflows
- Proper sub-agent design transforms Claude Code from token-heavy to efficient through strategic context management
- Agent specialization through service-specific knowledge dramatically improves implementation quality and architectural decisions
- Structured communication protocols between agents prevent information silos and improve overall project execution
- Context engineering represents the fundamental challenge in multi-agent AI systems for software development

# QUOTES

- "However, for people who tried it, they often get quite negative experience where sub agent feels slow" - Jason
- "That's why later they introduce this task tool for the cloud code agent" - Jason
- "By doing that you fatally turn those massive token consumption from the read file search file actions to something like just a few hundred token summary" - Jason
- "The whole purpose of sub agent has been around context engineer and context optimization" - Jason
- "Where things fail is when people start trying to get a sub agent not only doing the research work but also directly doing the implementation" - Jason
- "For each agent it only has very limited information about what is going on" - Jason
- "The best practice would be consider each sub agent almost as a researcher" - Jason
- "Sub aent works best when they just looking for information and provide a small amount of summary back to main conversation thread" - Adam Wolf
- "How they use file system as ultimate context management system" - Jason
- "Instead of storing all the tool results in the conversation history directly they receive a result to a local file which can be retrieved later" - Jason
- "This setup has dramatically improved the success rate and result for my cloud code" - Jason
- "Building product is just one part of puzzle" - Jason
- "You also need to learn how to acquire users, how to price it, and how to prove value to customers" - Jason
- "Different framework of work with enterprise versus SMB and how to estimate the value from your client's point of view" - Jason
- "It has more than one hour practical guide plus guides that you can start using for free" - Jason

# HABITS

- Always include important documentation directly inside system prompts for sub-agents to ensure latest practices
- Create specialized sub-agents for each service provider with relevant MCP tools and documentation access
- Maintain project context in centralized MD files that all agents read before starting work
- Structure sub-agent communication with specific output formats to ensure consistent parent-agent coordination
- Focus sub-agents on research and planning rather than direct implementation to maximize their effectiveness
- Update context files after completing tasks to maintain project coherence across different agent sessions
- Use file system for context management instead of storing everything in conversation history
- Read context files first before any sub-agent begins work to understand overall project status
- Delegate tasks to sub-agents with specific file names and context references for better coordination
- Create background sessions for long-running tasks to enable continuous monitoring and execution
- Design sub-agents with clear goals that explicitly exclude direct implementation to prevent confusion
- Include migration guides and version-specific documentation for services to ensure current implementation approaches
- Test sub-agents in production environments before including them in curated template collections
- Join weekly sessions to discuss best practices and learn from community experiences
- Use MCP tools to retrieve relevant components and examples for more informed sub-agent decisions

# FACTS

- Claude Code introduced sub-agent feature a few weeks ago as an exciting new concept
- Context compacting dramatically reduces AI performance by causing agents to lose previous work context
- Sub-agents inherit the same tool set as parent agents including file reading and searching capabilities
- File system context management can reduce token consumption from thousands to hundreds while preserving information
- Vercel AI SDK v5 was released a couple weeks ago with significant changes from version 4.0
- Background sessions in Claude Code can keep running and monitoring results continuously during development
- MCP servers enable specialized tools for retrieving components and design patterns from specific services
- Context files prevent information loss that occurs during conversation history compacting in long sessions
- Sub-agents can access special MCP tools for service-specific information retrieval and component examples
- Parent agents can only see task assignment and completion messages, not intermediate sub-agent actions
- Chassis components and design tools provide specialized MCP capabilities for front-end development workflows
- Context engineering represents the fundamental challenge behind effective sub-agent implementation in coding workflows
- Token consumption optimization is the primary technical benefit of properly implemented sub-agent architectures
- Specialized documentation embedding in system prompts improves sub-agent adherence to latest service practices
- Weekly community sessions provide ongoing education about evolving best practices in AI-assisted development

# REFERENCES

- Claude Code's sub-agent feature
- Adam Wolf from Claude Code team
- Manus team's blog on context engineering
- Chassis component library and MCP tools
- Vercel AI SDK v5 documentation and migration guide
- Twix design system website
- HubSpot's money-making AI agents material by Dimitri Shapier
- M Studio (fastest growing AI startup)
- Context 7 tools for complex Stripe pricing setups
- AI Builder Club weekly sessions
- Claude Code template collection
- ChatGPT replica implementation example
- Next.js project setup with Chassis
- Stripe documentation and payment integration tools
- Background session monitoring in Claude Code

# ONE-SENTENCE TAKEAWAY

Sub-agents work best as specialized researchers providing focused summaries rather than direct implementation executors.

# RECOMMENDATIONS

- Focus sub-agents on research and planning tasks rather than direct code implementation for better results
- Create specialized sub-agents for each service provider with embedded documentation and relevant MCP tools
- Use file-based context management instead of conversation history to prevent token bloat and information loss
- Maintain centralized project context files that all agents read before starting and update after completing work
- Structure sub-agent communication with specific output formats to ensure consistent coordination with parent agents
- Include service-specific documentation directly in system prompts to ensure adherence to latest best practices
- Design clear goals for sub-agents that explicitly exclude direct implementation to prevent scope creep
- Implement background sessions for long-running tasks to enable continuous monitoring and execution without blocking
- Test sub-agents thoroughly in production environments before including them in curated template collections
- Join community sessions to learn evolving best practices and share experiences with other AI-assisted developers
- Use MCP tools to retrieve relevant components and examples for more informed architectural decisions
- Create migration guides for service updates to ensure sub-agents use current implementation approaches
- Delegate tasks with specific context file references to maintain project coherence across different agent sessions
- Focus on context engineering as the fundamental challenge in multi-agent AI systems for development
- Embed specialized knowledge through documentation rather than relying on general-purpose agent capabilities
