# PATTERNS

- Initial user excitement about sub-agents quickly turned to disappointment due to poor performance
- Sub-agents consume excessive tokens and feel slow compared to regular Claude Code usage
- Context compaction dramatically degrades agent performance by losing conversation history
- Users expected sub-agents to handle both research and implementation but this approach fails
- Limited context sharing between agents creates isolated sessions without historical awareness
- Parent agents only see task assignment and completion summaries, missing implementation details
- File system serves as ultimate context management solution instead of conversation history
- Documentation and planning should be saved as retrievable files rather than conversation tokens
- Sub-agents work best when focused purely on research and information gathering tasks
- Implementation should remain with parent agent to maintain full context and debugging capability
- Specialized service-specific agents with embedded documentation provide superior results than generic ones
- MCP tools enable agents to access current documentation and examples for better implementation
- Context files shared between agents dramatically improve coordination and success rates
- Research reports saved as markdown files enable better cross-agent knowledge sharing
- Parent agent orchestration works when sub-agents return concise summaries not full implementations
- Token optimization achieved by converting massive file contents into small summary reports
- Sub-agents must read context files before starting work to understand project state
- Output format standardization ensures consistent communication between parent and sub-agents
- Rules preventing recursive agent calls avoid confusion in sub-agent behavior patterns
- Background monitoring sessions provide continuous feedback during long-running development tasks

# META

- Pattern emerged from author's personal experience transitioning from disappointment to success with sub-agents
- Multiple sources mentioned including Adam Wolf from Claude Code team confirming research-focused approach
- Manus team blog provided inspiration for file-system based context management strategy
- Author tested specialized agents for services like Vercel AI SDK, Supabase, Tailwind, Stripe
- Context sharing optimization learned from Manus team's approach to long-running tasks
- File system pattern observed across multiple successful AI agent implementations
- Token consumption issues identified through direct usage experience with Claude Code
- Implementation vs research distinction clarified through trial and error with different approaches
- MCP tool integration tested with specific examples like Shadcn components and design retrieval
- Success rate improvements measured through practical application building ChatGPT replica

# ANALYSIS

Sub-agents succeed when designed as specialized researchers rather than implementers, with file-based context sharing dramatically improving coordination and reducing token waste.

# BEST 5

- **Sub-agents excel at research but fail at implementation**: Evidence shows isolated implementation sessions lack debugging context while research provides valuable summaries to parent agents for better execution.

- **File system context management outperforms conversation history**: Manus team approach of saving tool results to retrievable files prevents token bloat while maintaining accessible knowledge base.

- **Specialized service agents with embedded docs beat generic ones**: Custom agents with current Vercel SDK v5 documentation and MCP tools produce higher fidelity results than general-purpose agents.

- **Context files enable cross-agent coordination**: Shared markdown files documenting project state allow agents to understand previous work and maintain consistency across sessions.

- **Token optimization through summary conversion**: Converting massive file reads into concise reports maintains essential information while dramatically reducing context window consumption and preventing compaction.

# ADVICE FOR BUILDERS

- Design sub-agents as researchers not implementers to maintain parent agent debugging context
- Use file system for context management instead of storing everything in conversation history
- Create specialized agents with embedded documentation for each service you frequently use
- Implement shared context files that agents read before starting and update after completing work
- Convert large tool outputs to concise summaries to prevent token bloat and context loss
- Establish output format standards to ensure consistent communication between agent layers
- Include explicit rules preventing agents from calling themselves to avoid recursive confusion
- Focus sub-agents on planning and research while keeping implementation with parent agent
- Embed current documentation directly in agent system prompts for accurate implementation guidance
- Test agent coordination with real projects to validate context sharing and success rates
- Use MCP tools to provide agents access to current examples and documentation
- Create template structures for consistent agent behavior across different specialized domains
- Monitor background sessions to catch issues early during long-running development tasks
- Document successful patterns in reusable templates for future agent development projects
- Join communities sharing proven agent configurations to accelerate your development workflow
