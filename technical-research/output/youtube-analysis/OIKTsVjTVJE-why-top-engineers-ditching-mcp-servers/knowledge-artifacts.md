# Knowledge Artifacts
## MCP Server Alternatives & Context Optimization

Generated from: "Why are top engineers DITCHING MCP Servers? (3 PROVEN Solutions)"
Date: 2025-11-23

---

## Flashcard Deck

### Foundational Concepts (Cards 1-10)

**Card 1**
Q: What is the primary problem with MCP servers?
A: They consume 10,000+ tokens (5% of context window) before agents even start working. Stacking multiple servers can consume 20%+ of available context.

---

**Card 2**
Q: What are the three main alternatives to MCP servers?
A: 1) CLI tools (50% context savings), 2) File system scripts (90% savings with progressive disclosure), 3) Claude skills (automatic progressive disclosure with vendor lock-in)

---

**Card 3**
Q: What is progressive disclosure in the context of AI agents?
A: Loading tools and context conditionally based on agent needs rather than front-loading everything. Maps conditions to files for dynamic context activation.

---

**Card 4**
Q: What is the recommended tool selection strategy (80/15/5 rule)?
A: Use MCP servers 80% of time for external tools, CLI approach 15% of time for control, and scripts/skills 5% of time for critical context preservation.

---

**Card 5**
Q: Why does prompt engineering come before context engineering?
A: Because prompts execute and appear before context loads into the window, allowing you to control what context gets loaded through well-engineered prompts.

---

**Card 6**
Q: What is info finance?
A: Concept by Vitalik Buterin - using betting markets/prediction markets to understand incentives and future sentiment before events actually occur.

---

**Card 7**
Q: What is UV and why is it useful for agent scripts?
A: UV is a Python dependency manager by Astral that enables single-file scripts with dependencies declared at the top, eliminating dependency management complexity.

---

**Card 8**
Q: How do you sidestep most context engineering problems?
A: Build single-purpose focused agents that delete themselves when tasks are completed, resetting context automatically.

---

**Card 9**
Q: What is the CLI trifecta benefit?
A: CLI tools work for you (individual), your team (collaboration), and your agents (automation) simultaneously without modification.

---

**Card 10**
Q: What context savings do each approach achieve?
A: MCP: 10,000 tokens baseline, CLI: 5,600 tokens (50% savings), Scripts: 2,000 tokens (90% savings), Skills: 1,500 tokens (automatic progressive disclosure)

---

### Implementation Details (Cards 11-20)

**Card 11**
Q: What is the file structure pattern for Beyond MCP approaches?
A: Four directories: 1-mcp-server/ (traditional), 2-cli-tools/ (CLI with prime), 3-file-system-scripts/ (progressive scripts), 4-skills/ (Claude native)

---

**Card 12**
Q: What are the key components of a CLI tool for agents?
A: 1) Main CLI implementation, 2) Comprehensive help docs, 3) Prime prompt (agent instructions), 4) README, 5) Optional MCP wrapper

---

**Card 13**
Q: How do you implement progressive disclosure with scripts?
A: Create single-purpose script files (search.py, get_market.py, etc.), teach agent to load only needed scripts based on conditions, avoid loading all at once.

---

**Card 14**
Q: What is a UV single-file script header?
A: `#!/usr/bin/env -S uv run` followed by `# /// script` block with `dependencies = ["package1", "package2"]` and closing `# ///`

---

**Card 15**
Q: What are the trade-offs between MCP and CLI approaches?
A: MCP: Simpler, standardized, but high context cost. CLI: More control, lower context, works for humans+agents, but requires more engineering.

---

**Card 16**
Q: When should you use Claude skills instead of scripts?
A: When working exclusively in Claude ecosystem, want automatic tool discovery, and accept vendor lock-in. Best for bundled self-contained functionality.

---

**Card 17**
Q: How do you prime an agent to use CLI tools?
A: Create prime prompt that teaches: 1) Read CLI help/README first, 2) Use specific commands, 3) When to use each tool, 4) Don't load unnecessary context

---

**Card 18**
Q: What is the context window consumption formula?
A: (Tokens Consumed / Total Available Tokens) × 100 = Percentage Used. Warning at 15%, Critical at 20%, Optimize above 25%.

---

**Card 19**
Q: How do you measure if MCP server is worth converting to CLI?
A: Track: 1) Tokens consumed, 2) How often used, 3) How many tools used vs loaded. If high tokens + low usage = convert to CLI/scripts.

---

**Card 20**
Q: What command checks context consumption in Claude?
A: `/context` command shows current token usage and percentage of context window consumed.

---

### Advanced Patterns (Cards 21-30)

**Card 21**
Q: What is the single-purpose agent pattern?
A: Create agent focused on one specific task, execute, then delete. Avoids context accumulation, resets to 0 tokens, sidesteps engineering complexity.

---

**Card 22**
Q: How do you map conditions to files for progressive disclosure?
A: If condition X (e.g., "needs market search") → load file search.py. If condition Y → load file Y.py. Each condition maps to one file, only load when needed.

---

**Card 23**
Q: What is the CLI-first, MCP-later pattern?
A: Build CLI for direct use first. If need to scale to multiple agents or standardize, wrap CLI in MCP server. CLI methods call into MCP, not vice versa.

---

**Card 24**
Q: How does Anthropic recommend handling MCP context bloat?
A: Use progressive disclosure, wrap MCP functionality in CLI or scripts, use direct tool calls instead of loading full server context.

---

**Card 25**
Q: What is the garbage context principle?
A: Unused tools/context loaded into agent window = garbage. Reduces performance. "When you have less garbage context, your agent can perform better."

---

**Card 26**
Q: How do benchmarks compare MCP vs raw code approaches?
A: Zero quality degradation when using raw code (CLI/scripts) versus MCP servers. Performance identical, but context consumption vastly different.

---

**Card 27**
Q: What is the portability spectrum of approaches?
A: Least portable: MCP servers (protocol-specific). More: CLI (requires CLI access). More: Scripts (any file system). Most: Skills (Claude-specific but bundled).

---

**Card 28**
Q: How do you decide context budget allocation?
A: System prompts: 2.5%, Task context: varies, Tools: max 10%, Working context: 70%, Safety margin: 5%. Adjust based on task complexity.

---

**Card 29**
Q: What is the engineering investment spectrum?
A: Highest: MCP from scratch. Medium: CLI tools. Lower: File scripts. Lowest: Claude skills. Trade-off between investment and control.

---

**Card 30**
Q: How do prediction markets serve as information sources?
A: Markets reveal future sentiment through financial incentives. Probability changes = sentiment shifts. Volume spikes = conviction. Correlations = related events.

---

## Concept Mind Maps

### Map 1: MCP Server Alternatives Ecosystem

```
Context Window Optimization
├── Problem Identification
│   ├── MCP servers: 10,000+ tokens per server
│   ├── Multiple servers: 20%+ context consumed
│   ├── Impact: Reduced agent effectiveness
│   └── Root cause: Loading all tools upfront
│
├── Solution 1: CLI Tools
│   ├── Characteristics
│   │   ├── 50% context reduction
│   │   ├── Prompt-based tool discovery
│   │   └── Full control over functionality
│   ├── Implementation
│   │   ├── Build CLI with Click/Typer
│   │   ├── Create comprehensive help docs
│   │   ├── Write prime prompt for agents
│   │   └── Optional MCP wrapper
│   ├── Benefits
│   │   ├── Works for humans, teams, agents
│   │   ├── Easy to modify and extend
│   │   └── No protocol lock-in
│   └── Use Cases
│       ├── Custom tool development
│       ├── Team-wide tooling
│       └── When need specific control
│
├── Solution 2: File System Scripts
│   ├── Characteristics
│   │   ├── 90% context reduction
│   │   ├── Progressive disclosure pattern
│   │   ├── Single-file UV scripts
│   │   └── Conditional loading
│   ├── Implementation
│   │   ├── Create focused single-purpose scripts
│   │   ├── Use UV for dependencies
│   │   ├── Map conditions to files
│   │   └── Prime agent with loading logic
│   ├── Benefits
│   │   ├── Maximum context efficiency
│   │   ├── High portability
│   │   ├── No shared dependencies
│   │   └── Isolated functionality
│   └── Use Cases
│       ├── Multiple tool stacking
│       ├── Context-critical scenarios
│       └── Maximum portability needed
│
├── Solution 3: Claude Skills
│   ├── Characteristics
│   │   ├── 92%+ context reduction
│   │   ├── Automatic progressive disclosure
│   │   ├── No prime prompts needed
│   │   └── Claude ecosystem integration
│   ├── Implementation
│   │   ├── Create skill.md configuration
│   │   ├── Bundle related scripts
│   │   ├── Define automatic discovery rules
│   │   └── Deploy to Claude ecosystem
│   ├── Benefits
│   │   ├── Automatic tool discovery
│   │   ├── Lowest context overhead
│   │   ├── Built-in progressive disclosure
│   │   └── Easy to use
│   └── Trade-offs
│       ├── Vendor lock-in (Claude only)
│       ├── Less portable
│       └── Ecosystem dependency
│
├── Best Practices
│   ├── Prompt Engineering First
│   │   ├── Prompts execute before context loads
│   │   ├── Control what gets loaded
│   │   └── Foundation for context engineering
│   ├── Progressive Disclosure
│   │   ├── Load only what's needed
│   │   ├── Map conditions to files
│   │   └── Avoid front-loading
│   ├── Single-Purpose Agents
│   │   ├── Focus on one task
│   │   ├── Auto-delete when done
│   │   └── Sidestep context problems
│   ├── Context Monitoring
│   │   ├── Use /context command
│   │   ├── Alert at 15%, 20%, 25%
│   │   └── Track usage patterns
│   └── 80/15/5 Rule
│       ├── 80%: MCP for external tools
│       ├── 15%: CLI for control needs
│       └── 5%: Scripts/skills for critical context
│
└── Key Principles
    ├── Less garbage = better performance
    ├── Build CLI-first for flexibility
    ├── Progressive disclosure scales
    ├── Trade-offs not absolutes
    ├── Context is precious resource
    └── Measure before optimizing
```

---

### Map 2: Context Engineering Workflow

```
Agent Development Lifecycle
├── 1. Planning Phase
│   ├── Define task scope
│   ├── Estimate context needs
│   ├── Choose tool approach (MCP/CLI/Scripts/Skills)
│   ├── Set context budget
│   └── Plan progressive disclosure strategy
│
├── 2. Tool Selection
│   ├── External Tools → MCP servers (80%)
│   ├── Custom Tools → CLI-first approach
│   ├── High Context Scenarios → Scripts
│   ├── Claude-Only → Skills
│   └── Multi-Tool Stacking → Progressive Scripts
│
├── 3. Implementation
│   ├── MCP Approach
│   │   ├── Use existing servers
│   │   ├── Configure in mcp.json
│   │   └── Monitor context consumption
│   ├── CLI Approach
│   │   ├── Build CLI tool
│   │   ├── Write help documentation
│   │   ├── Create prime prompt
│   │   └── Optional MCP wrapper
│   ├── Script Approach
│   │   ├── Create single-file scripts
│   │   ├── Add UV dependencies
│   │   ├── Map conditions to files
│   │   └── Prime progressive disclosure
│   └── Skills Approach
│       ├── Define skill.md
│       ├── Bundle scripts
│       └── Deploy to ecosystem
│
├── 4. Optimization
│   ├── Monitor context usage (/context)
│   ├── Track tool usage patterns
│   ├── Identify unused tools
│   ├── Convert high-cost low-use to scripts
│   └── Implement progressive disclosure
│
├── 5. Maintenance
│   ├── Regular context audits
│   ├── Update prime prompts
│   ├── Refactor based on usage
│   ├── Migrate as needs change
│   └── Share learnings with team
│
└── 6. Scaling
    ├── Single agent → Multiple agents
    ├── CLI → MCP wrapper for standardization
    ├── Scripts → Skills for convenience
    ├── Document patterns
    └── Build reusable templates
```

---

### Map 3: Decision Tree for Tool Integration

```
New Tool Integration Needed
│
├─ Is it an external third-party tool?
│  ├─ YES → MCP server exists?
│  │  ├─ YES → Use MCP server (80% case)
│  │  └─ NO → Need customization?
│  │     ├─ NO → Build simple CLI
│  │     └─ YES → Build full CLI
│  │
│  └─ NO → Internal/custom tool
│     ├─ Context budget tight? (<10% available)
│     │  ├─ YES → Use file scripts with progressive disclosure
│     │  └─ NO → Build CLI tool
│     │
│     ├─ Team usage required?
│     │  ├─ YES → CLI approach (works for all)
│     │  └─ NO → Claude only?
│     │     ├─ YES → Consider skills
│     │     └─ NO → Scripts or CLI
│     │
│     └─ Multiple tools needed?
│        ├─ YES → Progressive disclosure with scripts
│        └─ NO → Single tool
│           ├─ Complex → CLI
│           └─ Simple → Script
│
Context Check: Will this push usage >20%?
├─ YES → Use progressive disclosure
├─ MAYBE → Monitor and optimize
└─ NO → Current approach OK

Future Scaling Needed?
├─ YES → Build CLI first, wrap MCP later
├─ MAYBE → CLI-first (easier to extend)
└─ NO → Simplest approach that works
```

---

## Cheat Sheets

### Cheat Sheet 1: Context Consumption Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT CONSUMPTION CHEAT SHEET                │
├─────────────────┬───────────┬──────────┬─────────┬──────────┤
│ Approach        │ Tokens    │ % of     │ Savings │ Use When │
│                 │           │ 200k     │         │          │
├─────────────────┼───────────┼──────────┼─────────┼──────────┤
│ MCP Server      │ 10,000    │ 5.0%     │ 0%      │ External │
│ (single)        │           │          │         │ tools    │
├─────────────────┼───────────┼──────────┼─────────┼──────────┤
│ MCP Servers     │ 20,000+   │ 10-20%   │ N/A     │ Avoid or │
│ (multiple)      │           │          │         │ optimize │
├─────────────────┼───────────┼──────────┼─────────┼──────────┤
│ CLI Tools       │ 5,600     │ 2.8%     │ 50%     │ Need     │
│                 │           │          │         │ control  │
├─────────────────┼───────────┼──────────┼─────────┼──────────┤
│ File Scripts    │ 2,000     │ 1.0%     │ 90%     │ Context  │
│ (progressive)   │           │          │         │ critical │
├─────────────────┼───────────┼──────────┼─────────┼──────────┤
│ Claude Skills   │ 1,500     │ 0.75%    │ 92%     │ Claude   │
│                 │           │          │         │ only     │
└─────────────────┴───────────┴──────────┴─────────┴──────────┘

THRESHOLDS:
├─ 0-10%   │ ✓ Safe - Normal operation
├─ 10-15%  │ ⚠ Caution - Monitor closely
├─ 15-20%  │ ⚠⚠ Warning - Optimize soon
├─ 20-25%  │ ⚠⚠⚠ Critical - Immediate action
└─ >25%    │ ❌ Danger - Severe performance impact

COMMAND: /context (check current usage)
```

---

### Cheat Sheet 2: Tool Selection Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                 TOOL SELECTION MATRIX                       │
├──────────────┬──────┬─────────┬──────────┬─────────┬────────┤
│ Factor       │ MCP  │ CLI     │ Scripts  │ Skills  │ Winner │
├──────────────┼──────┼─────────┼──────────┼─────────┼────────┤
│ Simplicity   │ ★★★★ │ ★★★     │ ★★       │ ★★★★★   │ Skills │
│ Control      │ ★    │ ★★★★★   │ ★★★★     │ ★★      │ CLI    │
│ Context Eff. │ ★    │ ★★★     │ ★★★★★    │ ★★★★★   │ Script │
│ Portability  │ ★★★  │ ★★★★    │ ★★★★★    │ ★       │ Script │
│ Team Usage   │ ★★   │ ★★★★★   │ ★★       │ ★       │ CLI    │
│ Speed to Dev │ ★★★★ │ ★★      │ ★★★      │ ★★★★    │ MCP    │
│ Flexibility  │ ★★   │ ★★★★★   │ ★★★★     │ ★★      │ CLI    │
│ Standards    │ ★★★★ │ ★★★     │ ★★       │ ★       │ MCP    │
└──────────────┴──────┴─────────┴──────────┴─────────┴────────┘

USAGE GUIDELINES (80/15/5 Rule):
├─ 80% → MCP Servers (external, standard integrations)
├─ 15% → CLI Tools (custom, team-wide, need control)
└─ 5%  → Scripts/Skills (context critical, Claude-only)

DECISION SHORTCUTS:
├─ "Need it now" → MCP
├─ "Team will use" → CLI
├─ "Stacking tools" → Scripts
├─ "Claude only" → Skills
└─ "Don't know yet" → CLI (most flexible)
```

---

### Cheat Sheet 3: Progressive Disclosure Patterns

```
┌─────────────────────────────────────────────────────────────┐
│           PROGRESSIVE DISCLOSURE PATTERNS                   │
└─────────────────────────────────────────────────────────────┘

PATTERN 1: Condition-to-File Mapping
─────────────────────────────────────
Condition: task_requires_market_search
  → Load: search.py

Condition: task_requires_market_details
  → Load: get_market.py

Condition: task_requires_trade_data
  → Load: get_trades.py

NOT LOADED: Everything else
SAVINGS: 60-90% depending on task


PATTERN 2: Progressive Prime Prompt
─────────────────────────────────────
"You have access to Kalshi market tools.
Available scripts:
- search.py: Search markets (load when: need to find markets)
- get_market.py: Get details (load when: have ticker, need info)
- get_trades.py: Trade data (load when: analyzing volume)
- get_orderbook.py: Orderbook (load when: analyzing liquidity)

IMPORTANT: Only read the script you need for current task.
Do NOT load all scripts upfront."


PATTERN 3: Tiered Tool Loading
─────────────────────────────────────
Tier 1 (Always): core_utils.py (500 tokens)
Tier 2 (Common): search.py, get_market.py (1000 tokens)
Tier 3 (Rare): get_trades.py, get_orderbook.py (2000 tokens)

Load tier based on task:
- Quick query: Tier 1 only
- Standard analysis: Tier 1 + 2
- Deep analysis: All tiers


PATTERN 4: Script Header Documentation
─────────────────────────────────────
"""
search.py - Search Kalshi prediction markets

USE WHEN: Need to find markets by keyword
DON'T USE WHEN: Already have market ticker

Dependencies: requests
Context Cost: ~400 tokens
"""

Agent reads header → decides if needed → loads or skips


IMPLEMENTATION TEMPLATE:
─────────────────────────────────────
# In prime prompt:
"Before loading any script, read its header docstring.
Only load if USE WHEN condition matches your current task.
Skip if DON'T USE WHEN applies."

# In each script:
"""
[Script name] - [One-line description]

USE WHEN: [Specific condition]
DON'T USE WHEN: [Specific condition]
Dependencies: [List]
Context Cost: [Estimate tokens]
"""
```

---

### Cheat Sheet 4: UV Single-File Script Template

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests",      # HTTP client
#   "click",         # CLI framework
#   "python-dotenv"  # Environment variables
# ]
# ///

"""
[Tool Name] - [One-line description]

USE WHEN: [Specific trigger condition]
DON'T USE WHEN: [Avoid condition]

Dependencies: Listed in header
Context Cost: ~[X] tokens
Author: [Name]
Updated: [Date]
"""

import click
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@click.group()
def cli():
    """[Tool description for help text]"""
    pass

@cli.command()
@click.option('--param', required=True, help='Parameter description')
def command_name(param):
    """Command description."""
    # Implementation
    api_key = os.getenv('API_KEY')

    try:
        # Your logic here
        result = make_api_call(param, api_key)
        click.echo(f"Result: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise

def make_api_call(param, api_key):
    """Helper function."""
    # Implementation
    pass

if __name__ == '__main__':
    cli()
```

**Usage:**
```bash
# Direct execution (UV handles dependencies)
./script.py command-name --param value

# Or
uv run script.py command-name --param value
```

---

### Cheat Sheet 5: Context Monitoring Commands

```bash
# ──────────────────────────────────────────────────────────
#             CONTEXT MONITORING COMMANDS
# ──────────────────────────────────────────────────────────

# Check current context usage
/context

# Example output interpretation:
# "Using 15,234 tokens of 200,000 (7.6%)"
#  ─────────┬──────────  ────┬────
#           │                └─> Percentage (< 15% = good)
#           └─> Consumed tokens


# Before loading MCP server
/context  # Baseline
# Load server
/context  # New reading
# Calculate: New - Baseline = Server cost


# Monitor during session
# Every 5-10 interactions:
/context
# Track trend: increasing, stable, or decreasing?


# Create context checkpoint
echo "/context output: $(date)" >> context_log.txt
/context >> context_log.txt


# Alert thresholds (set up monitoring):
# 0-15%:   ✓ Normal operation
# 15-20%:  ⚠ Start optimizing
# 20-25%:  ⚠⚠ Urgent optimization
# 25%+:    ❌ Critical - reduce immediately


# ──────────────────────────────────────────────────────────
#           OPTIMIZATION WORKFLOW
# ──────────────────────────────────────────────────────────

# Step 1: Identify context hogs
/context  # Before any tools
# Load tool 1
/context  # Check delta
# Load tool 2
/context  # Check delta
# ... repeat


# Step 2: Calculate savings potential
# Current: 20,000 tokens (10%)
# Convert to CLI: 10,000 tokens (5%) → 50% savings
# Convert to scripts: 2,000 tokens (1%) → 90% savings


# Step 3: Implement optimization
# - High-cost, low-use → Scripts
# - High-cost, frequent-use → CLI
# - Low-cost → Keep as MCP


# Step 4: Verify improvements
/context  # After optimization
# Compare to baseline
# Document savings
```

---

## Study Guides

### 5-Week Learning Path

#### Week 1: Foundations & Problem Understanding

**Day 1-2: Context Window Fundamentals**
- Learn what context windows are and why they matter
- Understand token counting and limits
- Study how MCP servers consume context
- Practice: Use /context command throughout a work session

**Day 3-4: Prompt Engineering Basics**
- Why prompts execute before context
- How to control context loading through prompts
- Progressive disclosure concepts
- Practice: Write prompts that minimize context loading

**Day 5-7: MCP Server Analysis**
- Deep dive into MCP architecture
- Measure context consumption of your current MCP servers
- Identify waste and inefficiencies
- Practice: Audit your MCP setup, create consumption report

**Weekend Project:**
Create a context monitoring system for your workflow

**Resources:**
- Anthropic MCP documentation
- Beyond MCP repository (github.com/disler/beyond-mcp)
- /context command reference

**Assessment:**
- Can you calculate context consumption percentage?
- Can you identify which MCP servers consume most context?
- Do you understand progressive disclosure concept?

---

#### Week 2: CLI Tools Approach

**Day 1-2: CLI Fundamentals**
- Click vs Typer framework comparison
- Building basic CLI tools
- Help documentation best practices
- Practice: Build simple CLI tool with --help

**Day 3-4: CLI for Agents**
- Creating prime prompts
- Teaching agents to use CLI tools
- Documentation agents can understand
- Practice: Write prime prompt for your CLI tool

**Day 5-7: MCP Wrapping**
- When and why to wrap CLI in MCP
- Implementation patterns
- Maintaining both interfaces
- Practice: Add MCP wrapper to your CLI tool

**Weekend Project:**
Convert one existing MCP server to CLI + optional MCP wrapper
Measure context savings

**Resources:**
- Click documentation
- Typer documentation
- Beyond MCP examples (2-cli-tools directory)

**Assessment:**
- Can you build CLI that works for humans and agents?
- Can you write effective prime prompts?
- Do you understand CLI-first, MCP-later pattern?

---

#### Week 3: File System Scripts & Progressive Disclosure

**Day 1-2: UV Dependency Manager**
- UV basics and installation
- Single-file script patterns
- Dependency declaration syntax
- Practice: Create UV single-file script

**Day 3-4: Progressive Disclosure Implementation**
- Mapping conditions to files
- Creating focused single-purpose scripts
- Prime prompts for progressive loading
- Practice: Split monolithic tool into progressive scripts

**Day 5-7: Advanced Patterns**
- Tiered tool loading
- Script header documentation
- Conditional loading logic
- Practice: Implement full progressive disclosure system

**Weekend Project:**
Build complete progressive disclosure tool set for one domain
(e.g., prediction markets, GitHub, file operations)
Measure 90% context savings

**Resources:**
- UV documentation (by Astral)
- Beyond MCP examples (3-file-system-scripts)
- Progressive disclosure patterns

**Assessment:**
- Can you create single-file UV scripts?
- Can you implement condition-to-file mapping?
- Do you achieve 80%+ context savings vs MCP?

---

#### Week 4: Claude Skills & Single-Purpose Agents

**Day 1-2: Claude Skills Architecture**
- Skills vs other approaches
- When to accept vendor lock-in
- Automatic progressive disclosure
- Practice: Study existing Claude skills

**Day 3-4: Building Skills**
- skill.md configuration
- Bundling scripts
- Deployment and testing
- Practice: Convert scripts to Claude skill

**Day 5-7: Single-Purpose Agents**
- Focused agent pattern
- Auto-delete mechanisms
- Context reset benefits
- Practice: Build agent that self-destructs after task

**Weekend Project:**
Create both a Claude skill and single-purpose agent
Compare with previous approaches
Document trade-offs

**Resources:**
- Claude skills documentation
- Beyond MCP examples (4-skills)
- Tactical Agent Coding course (if available)

**Assessment:**
- Can you build Claude skills?
- Can you create self-deleting agents?
- Do you understand when to use skills vs other approaches?

---

#### Week 5: Integration, Optimization & Real-World Application

**Day 1-2: Hybrid Architectures**
- Combining MCP, CLI, scripts, and skills
- Decision frameworks for tool selection
- Migration strategies
- Practice: Design hybrid system for your use case

**Day 3-4: Context Monitoring & Analytics**
- Building context monitoring agents
- Usage tracking and analysis
- Optimization recommendation systems
- Practice: Implement context monitor and analytics

**Day 5-7: Real-World Application**
- Apply to your actual projects
- Optimize existing workflows
- Share learnings with team
- Practice: Full workflow optimization

**Weekend Project:**
Complete end-to-end implementation:
- Context monitoring agent
- Hybrid tool architecture (MCP + CLI + scripts)
- Progressive disclosure for high-cost tools
- Documentation for team

**Resources:**
- All previous week materials
- Your own analytics and measurements
- Team feedback and requirements

**Assessment:**
- Can you design optimal tool architecture for any use case?
- Can you implement monitoring and continuous optimization?
- Can you teach these patterns to others?
- Have you achieved measurable context savings in real work?

---

### Final Capstone Project

**Build: Context-Optimized Multi-Agent System**

**Requirements:**
1. Implement at least 2 different approaches (MCP, CLI, scripts, or skills)
2. Include context monitoring agent
3. Demonstrate progressive disclosure
4. Achieve 30%+ context savings vs baseline MCP-only
5. Document architecture decisions and trade-offs
6. Create runbook for team adoption

**Deliverables:**
- Working system with all components
- Architecture documentation
- Context consumption analysis
- Performance benchmarks
- Team adoption guide
- Lessons learned report

**Success Criteria:**
- System operational and stable
- Measurable context savings
- Team can understand and use
- Scales to additional use cases
- Documentation enables others to replicate

---

## Quiz Questions

### Section 1: Foundational Knowledge

**Question 1:**
How much context does a typical MCP server consume before an agent begins working?
A) 1,000 tokens
B) 5,000 tokens
C) 10,000 tokens
D) 20,000 tokens

**Answer:** C) 10,000 tokens (approximately 5% of a 200k context window)

---

**Question 2:**
What percentage of context consumption is considered the warning threshold?
A) 5%
B) 10%
C) 15%
D) 25%

**Answer:** C) 15% (Caution at 10%, Warning at 15%, Critical at 20%)

---

**Question 3:**
According to the 80/15/5 rule, when should you use CLI tools?
A) 80% of the time
B) 15% of the time
C) 5% of the time
D) Never

**Answer:** B) 15% of the time (when you need specific control over tools)

---

**Question 4:**
What comes before context engineering in importance?
A) Model selection
B) Prompt engineering
C) Tool selection
D) Agent architecture

**Answer:** B) Prompt engineering (prompts execute before context loads)

---

**Question 5:**
What is progressive disclosure?
A) Loading all tools upfront for faster access
B) Loading tools conditionally based on agent needs
C) Disclosing API keys progressively
D) Gradually revealing agent capabilities

**Answer:** B) Loading tools conditionally based on agent needs

---

### Section 2: Implementation Details

**Question 6:**
What is the approximate context savings when using CLI tools vs MCP servers?
A) 25%
B) 50%
C) 75%
D) 90%

**Answer:** B) 50% (from 10,000 to ~5,600 tokens)

---

**Question 7:**
What is UV?
A) A Python testing framework
B) A dependency manager enabling single-file scripts
C) A CLI framework
D) A context monitoring tool

**Answer:** B) A dependency manager enabling single-file scripts (by Astral)

---

**Question 8:**
In a UV single-file script, where are dependencies declared?
A) In requirements.txt
B) In setup.py
C) In the script header between `# /// script` markers
D) In a separate config file

**Answer:** C) In the script header between `# /// script` markers

---

**Question 9:**
What is the CLI trifecta?
A) Three CLI frameworks: Click, Typer, and Argparse
B) CLI works for you, your team, and your agents
C) Three optimization levels: Basic, Intermediate, Advanced
D) Command, options, and arguments

**Answer:** B) CLI works for you, your team, and your agents

---

**Question 10:**
When should you build MCP wrapper for a CLI tool?
A) Immediately, always wrap CLI in MCP
B) Never, keep them separate
C) When scaling to multiple agents or need standardization
D) Only for external tools

**Answer:** C) When scaling to multiple agents or need standardization

---

### Section 3: Advanced Concepts

**Question 11:**
What is the primary trade-off of Claude skills?
A) High cost
B) Vendor lock-in
C) Poor performance
D) Complex setup

**Answer:** B) Vendor lock-in (Claude-specific, less portable)

---

**Question 12:**
How do single-purpose agents sidestep context engineering problems?
A) They use advanced algorithms
B) They use smaller models
C) They delete themselves after completion, resetting context
D) They don't use any tools

**Answer:** C) They delete themselves after completion, resetting context

---

**Question 13:**
What is info finance?
A) Financial APIs for agents
B) Using prediction markets to understand future incentives
C) Cryptocurrency trading strategies
D) Automated financial planning

**Answer:** B) Using prediction markets to understand future incentives (Vitalik Buterin concept)

---

**Question 14:**
What does "garbage context" refer to?
A) Deleted or corrupted data
B) Unused tools and information loaded into context window
C) Poorly formatted prompts
D) Error messages

**Answer:** B) Unused tools and information loaded into context window

---

**Question 15:**
According to benchmarks, what is the quality difference between MCP servers and raw code approaches?
A) MCP is 50% better
B) Raw code is 30% better
C) No quality degradation (equivalent)
D) Depends on use case

**Answer:** C) No quality degradation (equivalent performance)

---

### Section 4: Decision Making

**Question 16:**
When should you use file system scripts instead of CLI tools?
A) When building for humans
B) When context preservation is critical
C) When you need a standard protocol
D) When speed to development matters most

**Answer:** B) When context preservation is critical (90% savings)

---

**Question 17:**
What is the recommended first step when context consumption exceeds 20%?
A) Switch to a larger model
B) Delete some agents
C) Implement progressive disclosure or script-based alternatives
D) Ignore it, modern models can handle it

**Answer:** C) Implement progressive disclosure or script-based alternatives

---

**Question 18:**
When building a new custom tool, what should you build first?
A) MCP server
B) Claude skill
C) CLI tool
D) File system script

**Answer:** C) CLI tool (CLI-first approach for maximum flexibility)

---

**Question 19:**
What percentage of tool integrations should use MCP servers according to the video?
A) 50%
B) 65%
C) 80%
D) 95%

**Answer:** C) 80% (for external tools and standard integrations)

---

**Question 20:**
Multiple MCP servers consuming 20%+ of context indicates you should:
A) Upgrade to a larger context window model
B) Remove some MCP servers or convert to CLI/scripts
C) Use more powerful hardware
D) Reduce prompt length

**Answer:** B) Remove some MCP servers or convert to CLI/scripts

---

## Glossary of Terms

**Agent**: An AI system that can take actions on behalf of users, manipulate data, and use tools to accomplish tasks.

**CLI (Command-Line Interface)**: Text-based interface for interacting with software through commands, usable by humans, teams, and agents.

**Claude Skills**: Claude-native tool integration method with automatic progressive disclosure and bundled functionality.

**Context Engineering**: The practice of optimizing what information enters an agent's context window and when.

**Context Window**: The amount of text (measured in tokens) an AI model can process at one time. For example, 200,000 tokens.

**File System Scripts**: Single-purpose, isolated scripts that implement progressive disclosure for minimal context consumption.

**Garbage Context**: Unused tools, documentation, or information loaded into context that reduces agent performance.

**Info Finance**: Concept by Vitalik Buterin - using prediction markets to understand future incentives and sentiment before events occur.

**MCP (Model Context Protocol)**: Standard protocol for connecting AI agents to external tools and data sources.

**MCP Server**: Implementation of MCP protocol that exposes tools, resources, and prompts to agents.

**Prime Prompt**: Instructions written for agents explaining how to use CLI tools or scripts, part of progressive disclosure.

**Progressive Disclosure**: Pattern where tools and context are loaded conditionally based on agent needs rather than all upfront.

**Prompt Engineering**: Crafting prompts to control AI behavior and context loading; foundational skill that precedes context engineering.

**Single-Purpose Agent**: Focused agent built for one specific task that self-destructs after completion, resetting context.

**Token**: Unit of text measurement for AI models; roughly 0.75 words in English.

**UV**: Python dependency manager by Astral that enables single-file scripts with dependencies declared in header.

**80/15/5 Rule**: Tool selection guideline - 80% MCP servers, 15% CLI tools, 5% scripts/skills.

---

## Additional Learning Resources

### Primary Resources

1. **Beyond MCP Repository**
   - URL: github.com/disler/beyond-mcp
   - Contains: All four approaches with working examples
   - Focus: Kalshi prediction markets integration

2. **Anthropic Blog: Code Execution with MCP**
   - Official recommendations for progressive disclosure
   - Direct tool call patterns
   - Context optimization strategies

3. **Mario Zechner: "What if you don't need MCP?"**
   - Engineering perspective on MCP alternatives
   - CLI-first methodology
   - Real-world implementation experiences

### Tool Documentation

4. **UV by Astral**
   - Modern Python dependency manager
   - Single-file script capabilities
   - Fast, reliable, modern

5. **Click Framework**
   - Python CLI framework
   - Comprehensive, well-documented
   - Great for building agent-friendly CLIs

6. **Typer Framework**
   - Modern Python CLI framework
   - Built on Click
   - Type hints and automatic validation

### Prediction Markets

7. **Kalshi**
   - Regulated prediction market platform
   - Example integration in Beyond MCP
   - Info finance applications

8. **Polymarket**
   - Decentralized prediction markets
   - Alternative to Kalshi
   - Crypto-based

### Advanced Topics

9. **Vitalik Buterin on Info Finance**
   - Concept explanations
   - Use cases for prediction markets as information
   - Economic incentives

10. **Tactical Agent Coding Course**
    - Single-purpose agent patterns
    - Focused agent architectures
    - Production implementations

---

**Document Location**: /Users/ameno/dev/umbra-dev/technical-research/output/youtube-analysis/OIKTsVjTVJE/knowledge-artifacts.md
