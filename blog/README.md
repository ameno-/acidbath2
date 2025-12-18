# The Agentic Engineering Playbook

A 6-part blog series transforming technical YouTube research into actionable, polarizing content about AI agents and prompt engineering.

## Series Overview

| # | Title | Angle | Tier |
|---|-------|-------|------|
| 1 | **Prompts Are the New Code** | Engineers ignoring prompt engineering will be obsolete | S |
| 2 | **Your Context Window Is Bleeding** | MCP servers are a bandaid on a bullet wound | B |
| 3 | **You're Using Sub-Agents Wrong** | 90% of developers are sabotaging themselves | A |
| 4 | **Chat UI Is Dead** | File-based automation is the future | A |
| 5 | **The Agent Endgame** | Stop renting, start owning | A |
| 6 | **55,000 Files in 5 Minutes** | The fix for AI + large codebases | A |

## Structure

```
blog/
├── README.md                 # This file
├── _utils/
│   └── ascii_callout.py      # ASCII art quote generator
├── _meta/
│   ├── series.json           # Series metadata
│   └── keywords.json         # SEO keywords
└── posts/
    ├── 01-prompts-are-the-new-code/
    │   ├── post.md           # Blog content
    │   ├── metadata.json     # SEO & structured data
    │   ├── diagrams/         # Mermaid sources
    │   └── callouts/         # ASCII art blocks
    ├── 02-context-window-bleeding/
    ├── 03-subagents-wrong/
    ├── 04-chat-ui-is-dead/
    ├── 05-agent-endgame/
    └── 06-55k-files-5-minutes/
```

## Using ASCII Callouts

Generate callout quotes with the utility:

```bash
# Classic style
uv run _utils/ascii_callout.py "Your quote here" --author "Author" --style classic

# Provocative (controversial takes)
uv run _utils/ascii_callout.py "Hot take here" --style provocative

# Insight (aha moments)
uv run _utils/ascii_callout.py "Revelation here" --style insight

# Data (metrics)
uv run _utils/ascii_callout.py "30x faster" --style data --title "THE NUMBERS"

# Warning
uv run _utils/ascii_callout.py "Danger zone" --style warning
```

## Sources

Based on analysis of 6 YouTube videos from:
- **IndyDevDan** (4 videos)
- **AI Jason** (1 video)
- **Jo Van Eyck** (1 video)

Total research: ~32.5 MB of multi-pattern fabric analysis

## Content Philosophy

- **Polarizing, not pandering** - Strong takes that make readers feel something
- **Data-driven** - Specific numbers, benchmarks, and proof
- **Actionable** - Every post ends with concrete next steps
- **No forced humor** - Emotion through truth, not jokes

---

*Generated: 2025-12-15*
