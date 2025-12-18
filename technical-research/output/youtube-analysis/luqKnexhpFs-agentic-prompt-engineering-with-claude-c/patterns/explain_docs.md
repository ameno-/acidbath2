# OVERVIEW

What It Does: A framework for creating structured, reusable prompts that effectively communicate with AI agents to automate complex engineering workflows.

Why People Use It: Enables engineers to scale their productivity by building reliable, composable prompt templates that work consistently across teams and agents.

# HOW TO USE IT

Most Common Syntax: 
```
# TITLE
# PURPOSE
# VARIABLES
# WORKFLOW
# REPORT
```

# COMMON USE CASES

For Simple Task Automation: `Level 1 - Ad Hoc Prompt (basic instructions)`
For Sequential Workflows: `Level 2 - Workflow Prompt (step-by-step processes)`
For Conditional Logic: `Level 3 - Control Flow Prompt (if/then/loops)`
For Multi-Agent Tasks: `Level 4 - Delegation Prompt (agent coordination)`
For Background Processing: `Level 5 - Background Prompt (autonomous operation)`
For Prompt Generation: `Level 6 - Template Meta Prompt (prompts that build prompts)`

# MOST IMPORTANT AND USED OPTIONS AND FEATURES

**WORKFLOW Section** - The core step-by-step instructions for your agent. This is the most critical section that defines exactly what actions the agent should take in sequence.

**VARIABLES Section** - Allows dynamic input (user-provided) and static variables (fixed values) that can be referenced throughout the prompt using consistent syntax like `{variable_name}`.

**PURPOSE Section** - Clear, direct statement of what the prompt accomplishes. Should be 1-2 sentences using direct language that speaks to the agent.

**REPORT Section** - Defines the output format and structure you want from the agent. Controls whether responses are JSON, YAML, or specific structured formats.

**METADATA Section** - Specifies technical constraints like allowed tools, model requirements, and execution parameters for the agent environment.

**INSTRUCTIONS Section** - Auxiliary information that supports the workflow steps. Provides additional context without cluttering the main workflow sequence.

**CONTROL FLOW Elements** - Natural language conditionals, loops, and early returns that allow prompts to handle different scenarios and repeat operations.

**CODEBASE STRUCTURE Section** - Context mapping that gives agents a quick reference to file locations and purposes without requiring them to search or read files directly.
