# PATTERNS

- MCP servers consume significant context window tokens (10,000+ tokens) before agents begin working
- Context window depletion becomes critical when stacking multiple MCP servers together
- CLI-based approaches reduce context consumption by approximately 50% compared to MCP servers
- Script-based approaches achieve 90% context window savings through progressive disclosure
- Prompt engineering is more critical than context engineering for agent performance
- Progressive disclosure prevents agents from loading unnecessary tool context upfront
- Skills provide automatic invocation while scripts require manual priming commands
- CLI tools work effectively for users, teams, and agents simultaneously
- Raw code as tools performs equally well as MCP servers in benchmarks
- Single-file scripts enable maximum portability and code sharing capabilities
- Context preservation becomes essential when using multiple large tool sets
- MCP servers excel for external tools requiring minimal engineering investment
- CLI approaches offer full control over tool functionality and context management
- Scripts enable conditional tool loading based on specific use cases
- Skills create Claude ecosystem lock-in despite their convenience benefits
- Tool discovery methods vary significantly between MCP, CLI, scripts, and skills
- Anthropic recommends wrapping MCP functionality in CLI for progressive disclosure
- Self-contained scripts reduce complexity while increasing code duplication overhead
- Dedicated focused agents sidestep most context engineering problems entirely
- Building CLI first enables easy MCP server wrapping when scaling needs arise
- Prediction markets provide valuable future state information through betting behavior
- UV dependency management enables powerful single-file script architectures
- Agent context windows require careful engineering when tools stack together
- External MCP servers provide zero customization control for developers
- Progressive disclosure maps conditions to files for dynamic context activation

# META

- Context window consumption pattern mentioned by Indie Dev Dan across all approaches
- MCP server token usage repeatedly emphasized as 5-10% context window drain
- CLI approach benefits highlighted by both Dan and referenced Mario engineer
- Progressive disclosure concept sourced from both Anthropic blog and practical demonstration
- Script-based context savings demonstrated through live agent testing comparisons
- Skills vs scripts trade-offs analyzed through direct feature comparison matrix
- Portability advantages shown through actual file structure and copying examples
- Tool discovery differences illustrated through multiple working agent demonstrations
- External vs internal tool control mentioned across MCP and CLI discussions
- Prediction market use cases demonstrated consistently across all four approaches
- Engineering investment levels compared between MCP, CLI, scripts, and skills
- Context preservation needs identified through multi-server stacking scenarios
- Claude ecosystem lock-in explicitly acknowledged for skills-based approach only
- Anthropic recommendations referenced from their official blog post documentation
- Mario's engineering insights cited for CLI-first development methodology approach

# ANALYSIS

These patterns reveal a fundamental trade-off between convenience and control in agent tooling, where context window preservation emerges as the primary driver for choosing alternatives to standard MCP servers.

# BEST 5

- MCP servers consume 10,000+ tokens before agents work, becoming critical when stacking multiple servers together, demonstrated through live context window measurements
- CLI approaches achieve 50% context savings while maintaining full tool control, working effectively for users, teams and agents simultaneously
- Script-based progressive disclosure saves 90% context through conditional loading, proven through benchmarks showing no quality degradation
- Skills provide automatic invocation with Claude lock-in, while scripts require manual priming but offer maximum portability
- Building CLI first enables easy MCP wrapping when needed, following the 80/10/10 rule for tool selection

# ADVICE FOR BUILDERS

- Start with MCP servers for external tools to minimize engineering investment
- Switch to CLI when you need control over tool functionality and context
- Use scripts for maximum context preservation when stacking multiple tool sets
- Build CLI first then wrap MCP server for scalability and interoperability
- Choose skills for Claude-specific workflows accepting ecosystem lock-in trade-offs
- Implement progressive disclosure to prevent unnecessary context window consumption
- Focus agents on single purposes to sidestep context engineering problems
- Use single-file scripts for maximum portability and sharing capabilities
- Apply prompt engineering before context engineering for better agent performance
- Consider UV dependency management for powerful single-file script architectures
- Map conditions to files for dynamic context activation in script approaches
- Prioritize context window preservation when designing multi-tool agent systems
- Test context consumption across approaches before committing to architecture decisions
- Balance convenience against control based on your specific use case requirements
- Document tool usage patterns to optimize context window management strategies
