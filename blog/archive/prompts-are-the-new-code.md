---
title: "The Prompt Is The New Code"
description: "The workflow section is the most important thing you'll write in any agentic prompt. Learn how to build workflow prompts that actually work, with templates you can use today."
pubDate: 2025-12-15
author: "Acidbath"
tags: ["ai", "prompts", "claude-code", "workflow", "automation"]
---

The workflow section is the most important thing you'll write in any agentic prompt.

Not the metadata. Not the variables. Not the fancy control flow. The workflow—your step-by-step play for what the agent should do—drives 90% of the value you'll capture from AI-assisted engineering.

This post shows you how to build workflow prompts that actually work, with templates you can use today.

## The Core Pattern: Input → Workflow → Output

Every effective agentic prompt follows this three-step structure:

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC PROMPT FLOW                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐      ┌─────────────┐      ┌──────────┐       │
│   │  INPUT  │ ───▶ │  WORKFLOW   │ ───▶ │  OUTPUT  │       │
│   └─────────┘      └─────────────┘      └──────────┘       │
│        │                  │                   │             │
│        ▼                  ▼                   ▼             │
│   Variables          Sequential           Report           │
│   Parameters         Step-by-Step         Format           │
│   Context            Instructions         Structure        │
│                                                             │
│   "What goes in"     "What happens"      "What comes out"  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

The workflow section is where your agent's actual work happens. It's rated S-tier usefulness with C-tier difficulty—the most valuable component is also the easiest to execute well.

## POC: A Working Workflow Prompt

Here's a complete, production-ready workflow prompt you can use as a Claude Code command:

```markdown
---
description: Analyze a file and create implementation plan
allowed-tools: Read, Glob, Grep, Write
argument-hint: <file_path>
---

# File Analysis and Planning Agent

## Purpose
Analyze the provided file and create a detailed implementation plan for improvements.

## Variables
- **target_file**: $ARGUMENTS (the file to analyze)
- **output_dir**: ./specs

## Workflow

1. **Read the target file**
   - Load the complete contents of {{target_file}}
   - Note the file type, structure, and purpose

2. **Analyze the codebase context**
   - Use Glob to find related files (same directory, similar names)
   - Use Grep to find references to functions/classes in this file
   - Identify dependencies and dependents

3. **Identify improvement opportunities**
   - List potential refactoring targets
   - Note any code smells or anti-patterns
   - Consider performance optimizations
   - Check for missing error handling

4. **Create implementation plan**
   - For each improvement, specify:
     - What to change
     - Why it matters
     - Files affected
     - Risk level (low/medium/high)

5. **Write the plan to file**
   - Save to {{output_dir}}/{{filename}}-plan.md
   - Include timestamp and file hash for tracking

## Output Format
file_analyzed: {{target_file}}
timestamp: {{current_time}}
improvements:
  - id: 1
    type: refactor|performance|error-handling|cleanup
    description: "What to change"
    rationale: "Why it matters"
    files_affected: [list]
    risk: low|medium|high
    effort: small|medium|large

## Early Returns
- If {{target_file}} doesn't exist, stop and report error
- If file is binary or unreadable, stop and explain
- If no improvements found, report "file looks good" with reasoning
```

Save this as `.claude/commands/analyze.md` and run with `/analyze src/main.py`.

## The Workflow Section Deep Dive

What makes workflow sections powerful:

**Sequential clarity** - Numbered steps eliminate ambiguity. The agent knows exactly what order to execute.

```markdown
## Workflow

1. Read the config file
2. Parse the JSON structure
3. Validate required fields exist
4. Transform data to new format
5. Write output file
```

**Nested detail** - Add specifics under each step without breaking the sequence:

```markdown
## Workflow

1. **Gather requirements**
   - Read the user's request carefully
   - Identify explicit requirements
   - Note implicit assumptions
   - List questions if anything is unclear

2. **Research existing code**
   - Search for similar implementations
   - Check for utility functions that could help
   - Review relevant documentation
```

**Conditional branches** - Handle different scenarios:

```markdown
## Workflow

1. Check if package.json exists
2. **If exists:**
   - Parse dependencies
   - Check for outdated packages
   - Generate update recommendations
3. **If not exists:**
   - Stop and inform user this isn't a Node project
```

## Agent Opportunity: Build a Prompt Library

Here's where you can multiply your impact:

```
┌─────────────────────────────────────────────────────────────┐
│                 PROMPT LIBRARY STRUCTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   .claude/commands/                                         │
│   ├── analyze.md        # File analysis (above)            │
│   ├── refactor.md       # Guided refactoring               │
│   ├── test.md           # Generate tests for file          │
│   ├── document.md       # Add documentation                │
│   ├── review.md         # Code review checklist            │
│   └── debug.md          # Systematic debugging             │
│                                                             │
│   Each prompt follows: Input → Workflow → Output           │
│   Each prompt is reusable across projects                  │
│   Each prompt serves you, your team, AND your agents       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Why Workflows Beat Ad-Hoc Prompting

```
┌─────────────────────────────────────────────────────────────┐
│              AD-HOC vs WORKFLOW COMPARISON                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   AD-HOC PROMPTING              WORKFLOW PROMPTING          │
│   ─────────────────             ──────────────────          │
│   "Help me refactor this"       Step 1: Backup              │
│                                 Step 2: Analyze             │
│   → Unpredictable scope         Step 3: Plan                │
│   → Inconsistent output         Step 4: Execute             │
│   → No error handling           Step 5: Verify              │
│   → Can't reuse                 Step 6: Document            │
│   → Team can't use it                                       │
│                                 → Predictable execution     │
│                                 → Consistent format         │
│                                 → Early returns on error    │
│                                 → Reusable forever          │
│                                 → Team multiplier           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

The workflow prompt transforms a vague request into an executable engineering plan. One workflow prompt executing for an hour can generate work that would take you 20 hours.

## Building Your First Workflow Prompt

Start with your most common task. The one you do every day. The one where you think "I should automate this."

1. Write out the steps you take manually
2. Convert each step to a numbered instruction
3. Add variables for the parts that change
4. Add early returns for failure cases
5. Specify the output format you want

Test it. Iterate. Add to your library.

The prompt is the new fundamental unit of engineering. The workflow section is where that engineering actually happens.

---

**Key Takeaways:**
- Workflow sections are S-tier value, C-tier difficulty
- Input → Workflow → Output is the universal pattern
- Numbered steps create predictable execution
- Early returns handle failure cases cleanly
- Build a library of reusable workflow prompts
- One good workflow prompt = 20+ hours of work

**Try It Now:**
Copy the analyze.md template above, save to `.claude/commands/analyze.md`, and run `/analyze` on any file in your codebase.
