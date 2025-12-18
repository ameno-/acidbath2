# ONE SENTENCE SUMMARY:
Engineer demonstrates three alternatives to MCP servers for connecting agents to external tools while preserving context window.

# MAIN POINTS:

1. MCP servers consume significant context window tokens (10,000+) before agents even start working effectively.

2. CLI approach uses prompt engineering to teach agents tool usage with 50% context reduction.

3. Script-based approach achieves progressive disclosure, reducing context consumption to under 2,000 tokens (90% savings).

4. Skills provide automatic tool discovery with Claude ecosystem integration but create vendor lock-in.

5. All approaches maintain same functionality as MCP servers while offering different context management benefits.

6. Progressive disclosure prevents loading unused tools, optimizing context window for specific tasks only.

7. CLI works for humans, teams, and agents simultaneously, providing universal tool interface.

8. Script approach uses single-file UV Python scripts with self-contained dependencies for maximum portability.

9. External tools should use MCP servers 80% of time; new tools should start with CLI.

10. Context engineering becomes critical when stacking multiple MCP servers consumes 20%+ of window.

# TAKEAWAYS:

1. Context window preservation is crucial for agent performance - avoid loading unnecessary tool descriptions upfront.

2. Start with CLI for new tools since it works for humans and agents while maintaining upgrade path to MCP.

3. Use progressive disclosure patterns to only load relevant tools when needed rather than everything at startup.

4. Consider vendor lock-in implications when choosing between open standards (MCP) versus proprietary solutions (Skills).

5. Engineer prompts carefully since they execute before context loading and can eliminate thousands of unnecessary tokens.
