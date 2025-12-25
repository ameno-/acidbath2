# Content-to-Asset Mapping

Decision tree logic for mapping blog post content to appropriate asset types and styles. This file extends the banner skill's content-style mapping to include asset type selection, enabling intelligent recommendations for all design assets.

---

## Overview

The content analysis process examines post metadata, title, tags, and context to recommend:
1. **Asset Type**: Which type of asset to generate (Banner, Callout, Divider, Diagram, DataCard)
2. **Style**: Which style variant within that asset type best suits the content
3. **Priority**: When multiple assets are suggested, which to generate first

---

## Asset Type Selection Logic

### Primary Asset Type: Banner

**Every blog post needs a banner**. The banner asset type is always recommended for new posts.

**Scoring**: Banner gets automatic +10 base score for any new post creation context.

### Secondary Asset Types: Context-Dependent

Additional asset types are recommended based on content characteristics:

| Content Characteristic | Recommended Asset Type | Scoring Logic |
|------------------------|------------------------|---------------|
| Contains metrics, benchmarks, performance data | **DataCard** | +3 per metric mentioned |
| Long post (5000+ words, 5+ sections) | **Divider** | +2 per major section beyond 3 |
| Explains process, workflow, or system | **Diagram** | +3 if workflow keywords present |
| Has key insights, warnings, or takeaways | **Callout** | +2 per insight/warning indicator |
| Multiple quantitative comparisons | **DataCard** (multiple) | +2 per comparison pair |
| Complex concept requiring visual aid | **Diagram** | +3 if abstract concept keywords |

---

## Banner Style Selection Logic

When Banner asset type is selected, apply the following scoring to recommend a style:

### Initial Scores

```python
banner_scores = {
    "glass_object": 0,
    "isometric": 0,
    "blueprint": 0,
    "dramatic": 0,
    "glitch": 1  # Universal baseline fallback
}
```

### Category Matching (+3 points)

| Content Category | Recommended Banner Style | Points |
|------------------|-------------------------|--------|
| "AI Engineering" | Glass Object Technical | +3 |
| "Technical Analysis" or "Deep Dive" | Technical Blueprint | +3 |
| "AI Development" | Simple Isometric Diagram | +3 |
| "Opinion" or "Commentary" | Dramatic Announcement | +3 |

### Tag Matching (+2 points each, max +6)

**Architecture Tags** → Glass Object +2
- `architecture`, `framework`, `SDK`, `system design`, `infrastructure`

**Workflow Tags** → Isometric +2
- `workflow`, `automation`, `process`, `sub-agents`, `pipeline`

**Performance Tags** → Blueprint +2
- `performance`, `optimization`, `benchmark`, `cost`, `token`, `efficiency`

**Opinion Tags** → Dramatic +2
- `opinion`, `paradigm`, `controversial`, `future`, `prediction`

### Title Sentiment (+1 to +2 points)

**Provocative Keywords** → Dramatic +2
- "wrong", "dead", "obsolete", "endgame", "obsolete", "is dead"

**Data Indicators** → Blueprint +2
- Numbers in title ("55,000", "36x", "95%")
- Metric patterns ("X faster", "Y% improvement")

**System Keywords** → Glass Object +1
- "architecture", "framework", "system", "platform"

**Process Keywords** → Isometric +1
- "workflow", "build", "using", "how to", "process"

### Formatting Metadata (+0.5 to +2 points)

**Tone Metadata**:
- `tone: "provocative"` → Dramatic +2
- `tone: "technical"` → Blueprint +1, Glass Object +1
- `tone: "instructional"` → Isometric +1

**Content Flags**:
- `hasDiagrams: true` → Isometric +1
- `hasMetrics: true` → Blueprint +1
- `isOpinion: true` → Dramatic +2

### Ranking

- **Primary Recommendation**: Highest score
- **Alternative 1**: Second highest
- **Alternative 2**: Third highest or Enhanced Glitch (universal fallback)

---

## Callout Style Selection Logic

When Callout asset type is selected, apply the following scoring:

### Initial Scores

```python
callout_scores = {
    "insight_highlight": 0,
    "warning_alert": 0,
    "data_spotlight": 0,
    "tech_detail": 1  # Universal baseline
}
```

### Content Context Matching (+3 points)

| Context Indicator | Recommended Callout Style | Points |
|-------------------|--------------------------|--------|
| "key insight", "takeaway", "important" | Insight Highlight | +3 |
| "warning", "gotcha", "edge case", "caution" | Warning Alert | +3 |
| Contains specific metric or number | Data Spotlight | +3 |
| Technical concept or system component | Tech Detail | +3 |

### Tone Matching (+2 points)

**Positive/Success Tone** → Insight Highlight +2
- "success", "achievement", "discovery", "breakthrough"

**Warning/Caution Tone** → Warning Alert +2
- "avoid", "mistake", "failure", "problem", "issue"

**Quantitative Tone** → Data Spotlight +2
- Numbers, percentages, measurements present

**Technical Tone** → Tech Detail +2
- Technical jargon, architecture terms

### Placement Context (+1 point)

**Mid-article emphasis** → Insight Highlight +1
**Before risky section** → Warning Alert +1
**After benchmark/test** → Data Spotlight +1
**Explaining component** → Tech Detail +1

---

## Divider Style Selection Logic

When Divider asset type is selected, apply the following scoring:

### Initial Scores

```python
divider_scores = {
    "minimal_line": 2,  # Default for most contexts
    "tech_pattern": 0,
    "glitch_break": 0
}
```

### Content Tone Matching (+2 points)

| Tone Characteristic | Recommended Divider Style | Points |
|---------------------|---------------------------|--------|
| Clean, technical, professional | Minimal Line | +2 |
| Deeply technical, architecture-focused | Tech Pattern | +2 |
| Edgy, modern, disruptive | Glitch Break | +2 |

### Section Transition Type (+1 point)

**Subtle transition** (related topics) → Minimal Line +1
**Major topic shift** (architecture → implementation) → Tech Pattern +1
**Paradigm shift** (old approach → new approach) → Glitch Break +1

### Post Theme Matching (+1 point)

**Minimalist posts** → Minimal Line +1
**Technical deep-dives** → Tech Pattern +1
**Provocative opinion** → Glitch Break +1

---

## Diagram Style Selection Logic

When Diagram asset type is selected, apply the following scoring:

### Initial Scores

```python
diagram_scores = {
    "two_element_flow": 1,  # Safest default
    "three_element_process": 0,
    "abstract_representation": 0
}
```

### Concept Complexity Matching (+3 points)

| Concept Type | Recommended Diagram Style | Points |
|--------------|---------------------------|--------|
| Simple relationship (A → B) | Two-Element Flow | +3 |
| Process with 3 stages (A → B → C) | Three-Element Process | +3 |
| Abstract concept or metaphor | Abstract Representation | +3 |

### Keyword Matching (+2 points)

**Flow Keywords** → Two-Element Flow +2
- "input", "output", "from", "to", "transform"

**Process Keywords** → Three-Element Process +2
- "steps", "stages", "phases", "pipeline", "workflow"

**Abstract Keywords** → Abstract Representation +2
- "concept", "idea", "metaphor", "represents", "symbolizes"

### CRITICAL: Complexity Check (Override)

If content suggests >3 elements:
- **Override all scores** → Abstract Representation = 10
- **Warn user**: "Nano Banana limitation: Diagram simplified to abstract representation"

---

## DataCard Style Selection Logic

When DataCard asset type is selected, apply the following scoring:

### Initial Scores

```python
datacard_scores = {
    "metric_hero": 1,  # Default for single metrics
    "comparison_card": 0,
    "progress_indicator": 0
}
```

### Metric Type Matching (+3 points)

| Metric Characteristic | Recommended DataCard Style | Points |
|-----------------------|----------------------------|--------|
| Single impressive number | Metric Hero | +3 |
| Before/after comparison | Comparison Card | +3 |
| Improvement or progression | Progress Indicator | +3 |

### Context Matching (+2 points)

**Bold claim** ("36x faster") → Metric Hero +2
**Optimization result** (before vs after) → Comparison Card +2
**Goal achievement** ("95% complete") → Progress Indicator +2

### Metric Format (+1 point)

**Percentage** → Progress Indicator +1
**Multiplier** ("10x", "50x") → Metric Hero +1
**Two values** → Comparison Card +1

---

## Multi-Asset Recommendations

### When to Suggest Multiple Assets

**Performance Analysis Posts**:
```
Recommended Assets:
1. Banner (blueprint style) - Header
2. DataCard (metric hero) - "36x faster" highlight
3. DataCard (comparison) - Before/after comparison
4. Divider (tech pattern) - Between analysis sections
```

**Architecture Explanation Posts**:
```
Recommended Assets:
1. Banner (glass object or isometric) - Header
2. Diagram (two-element or three-element) - System overview
3. Callout (insight highlight) - Key design decision
4. Divider (minimal line) - Section breaks
```

**Tutorial/How-To Posts**:
```
Recommended Assets:
1. Banner (isometric style) - Header
2. Diagram (three-element process) - Step-by-step flow
3. Callout (warning alert) - Common pitfalls
4. Callout (tech detail) - Important configuration
```

**Provocative Opinion Posts**:
```
Recommended Assets:
1. Banner (dramatic style) - Bold header
2. Callout (insight highlight) - Key arguments (2-3)
3. Divider (glitch break) - Major topic shifts
```

### Asset Priority Order

When recommending multiple assets, suggest generation in this priority:

1. **Banner** - Always first (header image needed immediately)
2. **DataCard** - Second (if metrics present, visual impact high)
3. **Diagram** - Third (if concept explanations needed)
4. **Callout** - Fourth (for emphasizing key points)
5. **Divider** - Last (section breaks, least critical)

---

## Content Analysis Examples

### Example 1: "55,000 Files in 5 Minutes" Post

**Content Characteristics**:
- Category: "Technical Deep Dive"
- Tags: `performance`, `optimization`, `benchmark`, `AI coding agents`
- Title: Contains numbers ("55,000", "5 Minutes")
- Tone: Data-driven, quantitative

**Asset Recommendations**:
1. **Banner** - Technical Blueprint (Score: 8)
   - Category match: Technical Deep Dive → Blueprint +3
   - Tag match: performance, optimization, benchmark → Blueprint +6 (max)
   - Title data indicators → Blueprint +2

2. **DataCard** - Metric Hero (Score: 6)
   - Single impressive metric: "55,000 files in 5 minutes"
   - Performance improvement context

3. **DataCard** - Comparison Card (Score: 5)
   - Before/after comparison (3 hours vs 5 minutes)

**Recommended Generation Order**: Banner → DataCard (metric hero) → DataCard (comparison)

---

### Example 2: "You're Using Sub-Agents Wrong" Post

**Content Characteristics**:
- Category: "AI Development"
- Tags: `sub-agents`, `workflow optimization`, `context management`
- Title: Provocative ("Wrong")
- Tone: Instructional with opinion

**Asset Recommendations**:
1. **Banner** - Simple Isometric Diagram (Score: 7)
   - Category match: AI Development → Isometric +3
   - Tag match: workflow, sub-agents → Isometric +4

2. **Diagram** - Three-Element Process (Score: 6)
   - Explains correct pattern (Research → Context → Implementation)
   - Workflow concept

3. **Callout** - Warning Alert (Score: 5)
   - Highlighting common mistakes
   - "Wrong" approach warnings

**Recommended Generation Order**: Banner → Diagram → Callout (warning)

---

### Example 3: "The Agent Endgame" Post

**Content Characteristics**:
- Category: "AI Engineering"
- Tags: `custom agents`, `agent engineering`, `system prompts`, `architecture`
- Title: Provocative ("Endgame")
- Tone: Advanced, architectural

**Asset Recommendations**:
1. **Banner** - Glass Object Technical (Score: 8)
   - Category match: AI Engineering → Glass Object +3
   - Tag match: architecture, agent engineering → Glass Object +4
   - System keywords in title → Glass Object +1

2. **Callout** - Insight Highlight (Score: 5)
   - Key architectural insights
   - Advanced concepts emphasized

**Recommended Generation Order**: Banner → Callout (insight)

---

### Example 4: "Context Window Bleeding: Token Analysis" Post

**Content Characteristics**:
- Category: "Technical Analysis"
- Tags: `context optimization`, `token consumption`, `performance`, `MCP servers`
- Title: Contains technical term ("Context Window Bleeding")
- Tone: Technical, data-focused

**Asset Recommendations**:
1. **Banner** - Technical Blueprint (Score: 9)
   - Category match: Technical Analysis → Blueprint +3
   - Tag match: performance, token consumption → Blueprint +4
   - Title technical focus → Blueprint +2

2. **DataCard** - Metric Hero (Score: 6)
   - "20% overhead" metric visualization
   - Token consumption numbers

3. **Diagram** - Abstract Representation (Score: 4)
   - Context window as visual metaphor
   - "Bleeding" concept abstracted

**Recommended Generation Order**: Banner → DataCard → Diagram

---

## Override Patterns

### User Manual Override

Users can always override recommendations with command flags:

```bash
# Override asset type
/generate-design-asset --asset-type callout "Content"

# Override both asset type and style
/generate-design-asset --asset-type banner --style glass_object "Title"

# Auto-accept primary recommendation
/generate-design-asset --slug post-slug --auto
```

### Fallback Patterns

If content analysis provides insufficient data:

**Banner Asset**: Default to **Enhanced Glitch Corruption** (universal fallback)
**Callout Asset**: Default to **Tech Detail** (universal, works for most contexts)
**Divider Asset**: Default to **Minimal Line** (clean, unobtrusive)
**Diagram Asset**: Default to **Abstract Representation** (safest for unclear concepts)
**DataCard Asset**: Default to **Metric Hero** (single metric presentation)

---

## Scoring Summary Table

### Banner Styles

| Style | Category Match | Tag Match | Title Sentiment | Tone Match | Typical Total |
|-------|---------------|-----------|----------------|------------|---------------|
| Glass Object Technical | AI Engineering (+3) | Architecture (+2-6) | System keywords (+1) | Technical (+1) | 7-11 |
| Simple Isometric Diagram | AI Development (+3) | Workflow (+2-6) | Process keywords (+1) | Instructional (+1) | 7-11 |
| Technical Blueprint | Technical Analysis (+3) | Performance (+2-6) | Data indicators (+2) | Technical (+1) | 8-12 |
| Dramatic Announcement | Opinion (+3) | Opinion tags (+2-6) | Provocative (+2) | Provocative (+2) | 9-13 |
| Enhanced Glitch | (Universal fallback) | - | - | - | 1 (baseline) |

### Callout Styles

| Style | Context Match | Tone Match | Placement | Typical Total |
|-------|---------------|------------|-----------|---------------|
| Insight Highlight | Key insight (+3) | Positive (+2) | Mid-article (+1) | 6 |
| Warning Alert | Warning/gotcha (+3) | Caution (+2) | Before risky section (+1) | 6 |
| Data Spotlight | Metric present (+3) | Quantitative (+2) | After benchmark (+1) | 6 |
| Tech Detail | Technical concept (+3) | Technical (+2) | Explaining component (+1) | 6 |

### Divider Styles

| Style | Tone Match | Transition Type | Theme Match | Typical Total |
|-------|------------|----------------|-------------|---------------|
| Minimal Line | Professional (+2) | Subtle (+1) | Minimalist (+1) | 4-6 |
| Tech Pattern | Technical (+2) | Major shift (+1) | Deep-dive (+1) | 4-6 |
| Glitch Break | Disruptive (+2) | Paradigm shift (+1) | Provocative (+1) | 4-6 |

### Diagram Styles

| Style | Concept Match | Keyword Match | Complexity Check | Typical Total |
|-------|---------------|---------------|------------------|---------------|
| Two-Element Flow | A → B (+3) | Flow keywords (+2) | 2 elements | 6 |
| Three-Element Process | A → B → C (+3) | Process keywords (+2) | 3 elements | 6 |
| Abstract Representation | Metaphor (+3) | Abstract keywords (+2) | >3 elements (override) | 6-10 |

### DataCard Styles

| Style | Metric Type | Context Match | Format | Typical Total |
|-------|-------------|---------------|--------|---------------|
| Metric Hero | Single number (+3) | Bold claim (+2) | Multiplier (+1) | 6 |
| Comparison Card | Before/after (+3) | Optimization (+2) | Two values (+1) | 6 |
| Progress Indicator | Improvement (+3) | Goal achievement (+2) | Percentage (+1) | 6 |

---

## Decision Flow Diagram (Conceptual)

```
Post Content
    ↓
Content Analysis
    ├── Extract category
    ├── Parse tags
    ├── Analyze title
    └── Identify tone
    ↓
Asset Type Selection
    ├── Banner (always +10 for new posts)
    ├── DataCard (if metrics present)
    ├── Diagram (if workflow/concept explanation)
    ├── Callout (if insights/warnings)
    └── Divider (if long post, 5+ sections)
    ↓
Style Scoring (per asset type)
    ├── Category matching
    ├── Tag matching
    ├── Title sentiment
    └── Formatting metadata
    ↓
Rank Styles (highest to lowest)
    ↓
Present Recommendations
    ├── Primary (highest score)
    ├── Alternative 1 (second highest)
    └── Alternative 2 (third or fallback)
    ↓
User Selection or Auto-Accept
    ↓
Generate Asset
```

---

## Version History

- **v1.0** (2025-12-24): Initial content-to-asset mapping with decision tree logic for all 5 asset types, scoring systems, and multi-asset recommendations
