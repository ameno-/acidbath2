# Content-to-Style Mapping Rules

Intelligent decision framework for recommending banner styles based on post metadata, content analysis, and thematic elements. This document defines the mapping logic from blog post characteristics to optimal banner style choices.

---

## Mapping Decision Tree

```
START: Analyze Post Metadata
│
├─ Check Category
│  ├─ "AI Engineering" → Evaluate Tags
│  ├─ "Technical Analysis" → Technical Blueprint (primary)
│  ├─ "AI Development" → Glass Object Technical or Isometric
│  └─ "Technical Deep Dive" → Technical Blueprint (primary)
│
├─ Check Tags (if category unclear)
│  ├─ Contains ["architecture", "framework", "SDK", "system design"]
│  │  → Glass Object Technical (primary)
│  │  → Isometric Technical Diagram (alternative)
│  │
│  ├─ Contains ["workflow", "automation", "process", "sub-agents", "orchestration"]
│  │  → Isometric Technical Diagram (primary)
│  │  → Glass Object Technical (alternative)
│  │
│  ├─ Contains ["performance", "optimization", "benchmark", "cost", "token", "context"]
│  │  → Technical Blueprint (primary)
│  │  → Isometric Technical Diagram (alternative)
│  │
│  ├─ Contains ["opinion", "paradigm", "future", "obsolete", "wrong", "dead"]
│  │  → Newspaper Front Page (primary)
│  │  → Enhanced Glitch Corruption (alternative)
│  │
│  └─ Contains ["tutorial", "guide", "how-to", "practical", "implementation"]
│     → Isometric Technical Diagram (primary)
│     → Glass Object Technical (alternative)
│
├─ Analyze Title Sentiment
│  ├─ Provocative/Controversial (contains "wrong", "dead", "obsolete", "secret", "endgame")
│  │  → Newspaper Front Page (boost priority)
│  │
│  ├─ Data-driven (contains numbers, percentages, metrics, "X hours", "Y files")
│  │  → Technical Blueprint (boost priority)
│  │
│  ├─ System-focused (contains "architecture", "system", "framework", "agent")
│  │  → Glass Object Technical or Isometric (boost priority)
│  │
│  └─ Process-focused (contains "workflow", "pattern", "using", "build")
│     → Isometric Technical Diagram (boost priority)
│
└─ Check Formatting Metadata (if available)
   ├─ hasDiagrams: true → Isometric Technical Diagram
   ├─ tone: "provocative" → Newspaper Front Page
   ├─ tone: "direct, technical" → Technical Blueprint or Glass Object
   └─ style: "polarizing, emotionally engaging" → Newspaper Front Page
```

---

## Category-Based Primary Recommendations

### AI Engineering
**Default**: Glass Object Technical
**Reasoning**: Represents sophisticated technical systems and frameworks
**Override If**:
- Contains workflow tags → Isometric Technical Diagram
- Contains performance tags → Technical Blueprint
- Tone is provocative → Newspaper Front Page

### Technical Analysis
**Default**: Technical Blueprint
**Reasoning**: Emphasizes data, metrics, and rigorous analysis
**Override If**:
- Focus is on architecture → Glass Object Technical
- Focus is on workflow/process → Isometric Technical Diagram
- Contains controversial claims → Newspaper Front Page

### AI Development
**Default**: Isometric Technical Diagram
**Reasoning**: Shows development workflows and implementation patterns
**Override If**:
- Focus is on architecture/framework → Glass Object Technical
- Focus is on performance → Technical Blueprint
- Highly opinionated → Newspaper Front Page

### (No Category or General)
**Default**: Enhanced Glitch Corruption
**Reasoning**: Universal style works for all content
**Override If**: Tags or title provide clear direction from decision tree

---

## Tag-Based Style Mapping

### Architecture & Systems Tags
**Triggers**: `architecture`, `framework`, `SDK`, `system design`, `infrastructure`, `platform`, `agent systems`

**Primary Style**: Glass Object Technical
**Alternative Style**: Isometric Technical Diagram

**Example Mappings**:
- "The Agent Endgame: Build Custom Agents" → Glass Object Technical
  - Object: Glass AI processor or custom agent component
  - Rationale: Represents sophisticated custom agent architecture

- "API Architecture for LLM Systems" → Glass Object Technical
  - Object: Glass server rack or API gateway
  - Rationale: Architectural foundation visualization

### Workflow & Process Tags
**Triggers**: `workflow`, `automation`, `process`, `sub-agents`, `orchestration`, `pipeline`, `agent patterns`, `integration`

**Primary Style**: Isometric Technical Diagram
**Alternative Style**: Glass Object Technical

**Example Mappings**:
- "You're Using Sub-Agents Wrong" → Isometric Technical Diagram
  - System: Multi-agent research workflow with file-based context
  - Rationale: Shows relationship between agents and data flow

- "Agentic Drop Zones: File-Based Automation" → Isometric Technical Diagram
  - System: Directory watcher pipeline with agent orchestration
  - Rationale: Visualizes automation workflow spatially

### Performance & Optimization Tags
**Triggers**: `performance`, `optimization`, `benchmark`, `cost`, `token`, `context`, `scalability`, `efficiency`

**Primary Style**: Technical Blueprint
**Alternative Style**: Isometric Technical Diagram

**Example Mappings**:
- "55,000 Files in 5 Minutes" → Technical Blueprint
  - Subject: Performance comparison schematic with metrics
  - Rationale: Data-driven benchmark visualization

- "Context Window Bleeding: Token Consumption" → Technical Blueprint
  - Subject: Context allocation diagram with measurements
  - Rationale: Quantitative analysis of resource usage

### Opinion & Paradigm Shift Tags
**Triggers**: `opinion`, `paradigm`, `future`, `controversial`, `bold claims`, `mindset shift`, `industry commentary`

**Primary Style**: Newspaper Front Page
**Alternative Style**: Enhanced Glitch Corruption

**Example Mappings**:
- "Prompts Are the New Code" → Newspaper Front Page
  - Headline: "Prompts Are the New Code: Programming Is Obsolete"
  - Photo: Engineer at terminal with prompt-focused workflow
  - Rationale: Provocative paradigm shift announcement

- "Chat UI Is Dead" → Newspaper Front Page
  - Headline: "Chat UI Is Dead: Agentic Drop Zones Are the Future"
  - Photo: File system automation replacing chat interface
  - Rationale: Bold claim challenging status quo

### Tutorial & Practical Tags
**Triggers**: `tutorial`, `guide`, `how-to`, `practical`, `implementation`, `walkthrough`, `getting started`

**Primary Style**: Isometric Technical Diagram
**Alternative Style**: Glass Object Technical

**Example Mappings**:
- "How to Build Custom Claude Agents" → Isometric Technical Diagram
  - System: Agent development workflow from system prompt to deployment
  - Rationale: Step-by-step process visualization

- "Practical Context Engineering Guide" → Isometric Technical Diagram
  - System: Context optimization pipeline with techniques
  - Rationale: Shows methodology spatially

---

## Title Sentiment Analysis

### Provocative Indicators
**Keywords**: `wrong`, `dead`, `obsolete`, `secret`, `endgame`, `truth`, `uncomfortable`, `sabotaging`, `fail`, `disaster`

**Style Boost**: Newspaper Front Page (+2 priority)
**Reasoning**: Provocative language signals controversial take or paradigm challenge

**Examples**:
- "You're Using X Wrong" → Strong newspaper signal
- "X Is Dead" → Strong newspaper signal
- "The X Endgame" → Moderate newspaper signal (can also be architecture)
- "X: The Uncomfortable Truth" → Strong newspaper signal

### Data-Driven Indicators
**Patterns**: Numbers (`55,000 files`, `90% of developers`, `3 hours → 5 minutes`, `28x improvement`), percentages, metrics, comparisons

**Style Boost**: Technical Blueprint (+2 priority)
**Reasoning**: Quantitative claims require schematic visualization with metrics

**Examples**:
- "55,000 Files in 5 Minutes" → Strong blueprint signal
- "90% Reduction in Token Usage" → Strong blueprint signal
- "3 Proven Alternatives: 50-92% Savings" → Strong blueprint signal

### System-Focused Indicators
**Keywords**: `architecture`, `system`, `framework`, `agent`, `infrastructure`, `platform`, `SDK`

**Style Boost**: Glass Object Technical (+1 priority)
**Reasoning**: System-level thinking aligns with architectural visualization

**Examples**:
- "The Agent Endgame" → Moderate glass signal
- "Custom Agent Architecture" → Strong glass signal
- "Framework Design for X" → Strong glass signal

### Process-Focused Indicators
**Keywords**: `workflow`, `pattern`, `using`, `build`, `implement`, `create`, `orchestrate`

**Style Boost**: Isometric Technical Diagram (+1 priority)
**Reasoning**: Process language indicates sequential or spatial relationships

**Examples**:
- "Agent Orchestration Patterns" → Strong isometric signal
- "Building Autonomous Workflows" → Strong isometric signal
- "How to Implement X" → Moderate isometric signal

---

## Formatting Metadata Analysis

When post metadata includes `formatting` object:

### `hasDiagrams: true`
**Style Boost**: Isometric Technical Diagram (+1 priority)
**Reasoning**: Post already contains diagrams; banner should match visual language

### `tone: "provocative"` or `"polarizing"`
**Style Boost**: Newspaper Front Page (+2 priority)
**Reasoning**: Provocative tone needs visually provocative style

### `tone: "direct, technical"` or `"precise"`
**Style Boost**: Technical Blueprint or Glass Object Technical (+1 priority)
**Reasoning**: Clean, technical tone matches precise visual styles

### `style: "emotionally engaging"` or `"controversial"`
**Style Boost**: Newspaper Front Page (+2 priority)
**Reasoning**: Emotional engagement pairs with dramatic newspaper presentation

### `hasCodeBlocks: true` (with no other strong signals)
**Style Boost**: Technical Blueprint or Isometric (+0.5 priority)
**Reasoning**: Technical implementation content benefits from technical visual style

---

## Multi-Style Recommendation Strategy

Always provide 3 options when presenting to user:
1. **Primary Recommendation**: Highest-scoring style from decision tree
2. **Alternative 1**: Second-highest scoring style (provides contrast/choice)
3. **Alternative 2**: Wildcard—either Enhanced Glitch (universal) or style based on secondary analysis

### Scoring System

Start with base scores:
- Glass Object Technical: 0
- Isometric Technical Diagram: 0
- Technical Blueprint: 0
- Newspaper Front Page: 0
- Enhanced Glitch Corruption: 1 (universal baseline)

Apply boosts from:
- Category match: +3 points
- Tag match: +2 points per matching tag (max +6)
- Title sentiment: +1 to +2 points
- Formatting metadata: +0.5 to +2 points

**Highest score wins primary recommendation.**
**Second-highest wins alternative 1.**
**Enhanced Glitch or third-highest wins alternative 2.**

---

## Override Patterns

### When to Ignore Recommendations

1. **User Explicitly Specifies Style**: Always honor user choice
2. **Post Has Existing Banner**: Offer to keep current style or upgrade
3. **Brand Guidelines**: If ACIDBATH establishes brand rules, apply those first
4. **Seasonal/Event Content**: Special occasions may override standard mapping
5. **A/B Testing**: May override for testing purposes

### Edge Case Handling

**Post with Conflicting Signals** (e.g., technical deep-dive with provocative title):
- Score both directions
- Present higher-scoring as primary
- Include conflicting style as alternative with explanation
- Example: "Performance Analysis with Controversial Claims" → Blueprint (primary, data-driven) + Newspaper (alternative, provocative angle)

**Post with Minimal Metadata** (only title, no tags/category):
- Rely heavily on title sentiment analysis
- Default to Enhanced Glitch if still unclear
- Prompt user for content type clarification
- Example: Single-word title "Agents" → Ask user or default to Glass Object (general AI topic)

**Post with Many Tags** (5+ tags spanning multiple categories):
- Weight more specific tags higher (e.g., "agent architecture" > "AI")
- Look for tag clusters (3+ related tags in same category)
- Use title as tiebreaker
- Example: Post tagged with workflow, performance, and architecture tags → Check title for dominant theme

---

## Concrete Examples with Reasoning

### Example 1: "Prompts Are the New Code"
**Metadata**:
- Category: "AI Engineering"
- Tags: `Prompt Engineering`, `AI Agents`, `Engineering Productivity`, `Paradigm Shift`
- Tone: `provocative`
- Style: `polarizing, emotionally engaging`

**Decision Process**:
1. Category "AI Engineering" → Base: Glass Object (+3)
2. Tag "Paradigm Shift" → Newspaper Front Page (+2)
3. Tone "provocative" → Newspaper Front Page (+2)
4. Style "polarizing, emotionally engaging" → Newspaper Front Page (+2)
5. Title contains paradigm language → Newspaper Front Page (+2)

**Scores**:
- Glass Object: 3
- Newspaper Front Page: 8
- Enhanced Glitch: 1

**Recommendation**:
- **Primary**: Newspaper Front Page
- **Alternative 1**: Glass Object Technical (represents sophisticated engineering angle)
- **Alternative 2**: Enhanced Glitch Corruption

**Rationale**: Strong provocative signals overwhelm category baseline. Paradigm shift content demands dramatic presentation.

---

### Example 2: "55,000 Files in 5 Minutes"
**Metadata**:
- Category: "Technical Deep Dive"
- Tags: `Performance Optimization`, `MCP Servers`, `Code Refactoring`, `Developer Tools`
- Tone: `direct, technical`
- Title contains: Multiple metrics (55,000 files, 5 minutes)

**Decision Process**:
1. Category "Technical Deep Dive" → Technical Blueprint (+3)
2. Tag "Performance Optimization" → Technical Blueprint (+2)
3. Tag "MCP Servers" → Isometric (+2)
4. Tone "direct, technical" → Blueprint/Glass (+1 to Blueprint)
5. Title has data-driven metrics → Technical Blueprint (+2)

**Scores**:
- Technical Blueprint: 8
- Isometric Diagram: 2
- Glass Object: 1
- Enhanced Glitch: 1

**Recommendation**:
- **Primary**: Technical Blueprint
- **Alternative 1**: Isometric Technical Diagram (workflow angle)
- **Alternative 2**: Enhanced Glitch Corruption

**Rationale**: Heavy performance and metrics focus. Blueprint style showcases quantitative comparisons effectively.

---

### Example 3: "You're Using Sub-Agents Wrong"
**Metadata**:
- Category: "AI Development"
- Tags: `sub agents`, `ai coding`, `context management`, `workflow optimization`, `ai architecture`
- Title sentiment: Provocative ("Wrong")

**Decision Process**:
1. Category "AI Development" → Isometric (+3)
2. Tag "sub agents" → Isometric (+2)
3. Tag "workflow optimization" → Isometric (+2)
4. Tag "ai architecture" → Glass Object (+2)
5. Title "Wrong" → Newspaper Front Page (+2)
6. Tag "context management" → Isometric (+2)

**Scores**:
- Isometric Diagram: 9
- Newspaper Front Page: 2
- Glass Object: 2
- Enhanced Glitch: 1

**Recommendation**:
- **Primary**: Isometric Technical Diagram
- **Alternative 1**: Newspaper Front Page (provocative angle)
- **Alternative 2**: Glass Object Technical (architecture angle)

**Rationale**: Despite provocative title, overwhelming workflow/process tags indicate spatial visualization is more important. Isometric shows research-vs-implementation pattern effectively.

---

### Example 4: "The Agent Endgame"
**Metadata**:
- Category: "AI Engineering"
- Tags: `agent engineering`, `custom agents`, `claude code sdk agents`, `system prompts`
- Difficulty: `advanced`
- Title: Contains "Endgame" (provocative + system-focused)

**Decision Process**:
1. Category "AI Engineering" → Glass Object (+3)
2. Tag "agent engineering" → Glass Object (+2)
3. Tag "custom agents" → Glass Object (+2)
4. Tag "system prompts" → Glass Object (+2)
5. Title "Endgame" → Newspaper (+1, weaker signal here)
6. Difficulty "advanced" → Glass Object (+1)

**Scores**:
- Glass Object: 10
- Newspaper Front Page: 1
- Enhanced Glitch: 1

**Recommendation**:
- **Primary**: Glass Object Technical
- **Alternative 1**: Isometric Technical Diagram (agent workflow)
- **Alternative 2**: Newspaper Front Page ("Endgame" angle)

**Rationale**: Strong architecture and custom engineering focus. Glass style represents sophisticated, production-grade agent systems.

---

### Example 5: "Chat UI Is Dead"
**Metadata**:
- Category: "AI Engineering"
- Tags: `agentic drop zones`, `ai workflow automation`, `beyond chat ui`, `file-based automation`
- Tone: `Polarizing, Direct`
- Title: Provocative ("Is Dead")

**Decision Process**:
1. Category "AI Engineering" → Glass Object (+3)
2. Tag "ai workflow automation" → Isometric (+2)
3. Tag "file-based automation" → Isometric (+2)
4. Tone "Polarizing, Direct" → Newspaper (+2)
5. Title "Is Dead" → Newspaper (+2)
6. Tag "beyond chat ui" → Isometric (+2)

**Scores**:
- Isometric Diagram: 6
- Newspaper Front Page: 4
- Glass Object: 3
- Enhanced Glitch: 1

**Recommendation**:
- **Primary**: Isometric Technical Diagram (close call)
- **Alternative 1**: Newspaper Front Page (provocative angle)
- **Alternative 2**: Glass Object Technical (architecture angle)

**Rationale**: Very close scoring. Workflow automation tags slightly edge out provocative tone. Both styles would work—present both as equal recommendations.

---

## Implementation Pseudocode

```python
def recommend_banner_style(post_metadata):
    scores = {
        "glass_object": 0,
        "isometric": 0,
        "blueprint": 0,
        "newspaper": 0,
        "glitch": 1  # Universal baseline
    }

    # Category analysis
    category = post_metadata.get("category", "").lower()
    if "ai engineering" in category:
        scores["glass_object"] += 3
    elif "technical analysis" in category or "deep dive" in category:
        scores["blueprint"] += 3
    elif "ai development" in category:
        scores["isometric"] += 3

    # Tag analysis
    tags = [tag.lower() for tag in post_metadata.get("tags", [])]

    architecture_tags = ["architecture", "framework", "sdk", "system design", "infrastructure"]
    workflow_tags = ["workflow", "automation", "process", "sub-agents", "orchestration", "pipeline"]
    performance_tags = ["performance", "optimization", "benchmark", "cost", "token", "context"]
    opinion_tags = ["opinion", "paradigm", "future", "controversial", "mindset shift"]

    for tag in tags:
        if any(arch_tag in tag for arch_tag in architecture_tags):
            scores["glass_object"] += 2
        if any(work_tag in tag for work_tag in workflow_tags):
            scores["isometric"] += 2
        if any(perf_tag in tag for perf_tag in performance_tags):
            scores["blueprint"] += 2
        if any(op_tag in tag for op_tag in opinion_tags):
            scores["newspaper"] += 2

    # Title sentiment analysis
    title = post_metadata.get("title", "").lower()
    provocative_keywords = ["wrong", "dead", "obsolete", "endgame", "truth", "sabotag"]
    data_keywords = ["files", "minutes", "hours", "x ", "% ", "percent", "improvement"]

    if any(keyword in title for keyword in provocative_keywords):
        scores["newspaper"] += 2
    if any(keyword in title for keyword in data_keywords):
        scores["blueprint"] += 2

    # Formatting metadata
    formatting = post_metadata.get("formatting", {})
    tone = formatting.get("tone", "").lower()

    if "provocative" in tone or "polarizing" in tone:
        scores["newspaper"] += 2
    elif "technical" in tone or "direct" in tone:
        scores["blueprint"] += 1
        scores["glass_object"] += 1

    if formatting.get("hasDiagrams", False):
        scores["isometric"] += 1

    # Sort and return top 3
    sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return {
        "primary": sorted_styles[0][0],
        "alternative_1": sorted_styles[1][0],
        "alternative_2": sorted_styles[2][0],
        "scores": scores,
        "reasoning": generate_reasoning(post_metadata, scores, sorted_styles)
    }
```

---

## Migration Guide: Old vs. New Mapping

### Old Behavior (Pre-Style Library)
Single glitch style for all posts. No content awareness. No recommendations.

### New Behavior (Post-Style Library)
Content-aware recommendations with 3 options. Intelligent mapping based on metadata.

**For Existing Posts**:
1. Re-analyze metadata using new mapping rules
2. Suggest appropriate style from library
3. Offer to regenerate with new style or keep existing glitch banner
4. Allow user to choose upgrade or preserve current

**Example Migration**:
- **Post**: "Prompts Are the New Code"
- **Old Banner**: Generic glitch art
- **New Recommendation**: Newspaper Front Page (provocative headline)
- **User Choice**: Regenerate with newspaper style or keep existing glitch

---

## Testing the Mapping

### Validation Dataset
Use existing 6 blog posts as test cases:

1. ✅ "Prompts Are the New Code" → Newspaper Front Page
2. ✅ "Context Window Bleeding" → Technical Blueprint
3. ✅ "You're Using Sub-Agents Wrong" → Isometric Technical Diagram
4. ✅ "Chat UI Is Dead" → Isometric (primary) / Newspaper (close alternative)
5. ✅ "The Agent Endgame" → Glass Object Technical
6. ✅ "55,000 Files in 5 Minutes" → Technical Blueprint

All 6 posts should map to appropriate styles based on decision tree logic.

### Edge Case Tests
- **Post with no tags**: Should default to Enhanced Glitch, prompt for clarification
- **Post with conflicting tags** (workflow + opinion): Should score both, present as alternatives
- **Single-word title**: Should rely on category or ask user
- **All tags equal weight**: Should use title sentiment as tiebreaker

---

## Version History

- **v1.0** (2025-12-23): Initial mapping rules with decision tree, tag analysis, scoring system, and validation examples
