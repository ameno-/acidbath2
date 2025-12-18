# ONE SENTENCE SUMMARY:
Claude Code's sub-agent feature works best for research tasks that provide summaries, not direct implementation work.

# MAIN POINTS:

1. Claude Code introduced sub-agents to solve context window limitations and prevent conversation compaction
2. Sub-agents save tokens by condensing file operations into small summaries for parent agents
3. Many users experienced poor results when sub-agents tried to do actual implementation work
4. Best practice is using sub-agents as researchers who provide implementation plans, not executors
5. Each sub-agent should be specialized for specific services like Shadcn, Vercel AI SDK, Stripe
6. Context sharing across agents uses file system as ultimate context management solution
7. Parent agents create context files that sub-agents read before starting and update after finishing
8. Sub-agents should never do implementation directly, only create detailed planning documentation
9. Specialized sub-agents equipped with relevant documentation and MCP tools perform much better
10. File-based context management prevents token bloat while maintaining information accessibility across conversations

# TAKEAWAYS:

1. Design sub-agents as specialized researchers for specific technologies rather than general implementation assistants
2. Use file system to share context between agents instead of storing everything in conversation history
3. Always have sub-agents read project context files before starting work and update them afterward
4. Include relevant documentation directly in sub-agent system prompts for better specialized knowledge
5. Structure sub-agent workflows to output implementation plans that parent agents can execute with full context
