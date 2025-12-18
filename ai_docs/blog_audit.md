# ACIDBATH Blog Post Audit

Generated: December 2025

This audit evaluates all existing blog posts against the ACIDBATH tenets and identifies required changes.

---

## Executive Summary

**Critical Issues:**
- All 6 posts are under the 2,000-2,500 word target
- 4 of 6 posts have hype-speak titles that violate ACIDBATH voice guidelines
- Metadata files contain fear-mongering and clickbait phrases
- Most posts lack explicit failure mode documentation

**Word Count Analysis:**

| Post | Current | Target | Gap |
|------|---------|--------|-----|
| 01 - Prompts Are The New Code | 1,487 | 2,000 | -513 |
| 02 - Context Window Bleeding | 1,509 | 2,000 | -491 |
| 03 - Sub-Agents Wrong | 1,671 | 2,000 | -329 |
| 04 - Chat UI Is Dead | 1,686 | 2,000 | -314 |
| 05 - Agent Endgame | 1,869 | 2,000 | -131 |
| 06 - 55k Files | 1,594 | 2,000 | -406 |

---

## Post-by-Post Audit

### Post 01: The Prompt Is The New Code

**Current Title:** "Prompts Are the New Code: The 7-Level Framework That's Making Traditional Programming Obsolete"

**Tenet Violations:**
| Tenet | Status | Issue |
|-------|--------|-------|
| POC Rule | ✅ PASS | Has working analyze.md template |
| Numbers Test | ⚠️ WEAK | Claims "20 hours of work" but no specific benchmark |
| Production Lens | ⚠️ WEAK | Limited real-world gotchas |
| Senior Engineer Filter | ✅ PASS | Valuable content |
| Honest Failure Requirement | ❌ FAIL | No failure modes documented |
| Try It Now | ✅ PASS | Clear action item |
| Voice/Style | ❌ FAIL | Title contains "Making Traditional Programming Obsolete" (hype) |

**Metadata Issues:**
- `"emotionalHooks": ["Fear of obsolescence", "FOMO on paradigm shift"]` - manipulative
- `"controversialClaims": ["Engineers will be obsolete in 2 years"]` - fear-mongering
- `"title"`: contains "Making Traditional Programming Obsolete" - hype-speak

**Required Changes:**
1. **Retitle**: "Workflow Prompts: The Pattern That Makes AI Engineering Predictable"
2. **Add 500+ words** covering:
   - When workflow prompts fail (overly complex tasks, ambiguous requirements)
   - Token cost comparison (workflow vs ad-hoc)
   - Real benchmark: time saved on actual project
3. **Remove all "obsolete" language from metadata**
4. **Add explicit limitations section**

---

### Post 02: Your Context Window Is Bleeding

**Current Title:** "Your Context Window Is Bleeding: Why MCP Servers Are a Bandaid on a Bullet Wound"

**Tenet Violations:**
| Tenet | Status | Issue |
|-------|--------|-------|
| POC Rule | ✅ PASS | Has UV script examples |
| Numbers Test | ✅ PASS | 95% reduction, token counts |
| Production Lens | ⚠️ WEAK | Limited production considerations |
| Senior Engineer Filter | ✅ PASS | Valuable optimization content |
| Honest Failure Requirement | ❌ FAIL | No failure modes for progressive disclosure |
| Try It Now | ✅ PASS | Clear action item |
| Voice/Style | ❌ FAIL | "Bandaid on a Bullet Wound" is sensationalist |

**Metadata Issues:**
- `"subtitle": "20% of your context was gone before you typed a single character"` - acceptable
- Title contains "Bandaid on a Bullet Wound" - sensationalist medical metaphor

**Required Changes:**
1. **Retitle**: "Progressive Disclosure: Cutting Context Consumption by 95%"
2. **Add 500+ words** covering:
   - When progressive disclosure fails (tools used every time anyway)
   - Setup overhead vs savings calculation
   - Maintenance burden of managing script directory
3. **Add section on measuring your actual baseline before optimizing**

---

### Post 03: Sub-Agents Are Researchers, Not Implementers

**Current Title:** "You're Using Sub-Agents Wrong: 90% of Developers Are Sabotaging Their AI Workflows"

**Tenet Violations:**
| Tenet | Status | Issue |
|-------|--------|-------|
| POC Rule | ✅ PASS | Has context.md and researcher.md templates |
| Numbers Test | ✅ PASS | 80% token reduction |
| Production Lens | ✅ PASS | Good coverage of context isolation problem |
| Senior Engineer Filter | ✅ PASS | Valuable delegation pattern |
| Honest Failure Requirement | ⚠️ WEAK | Mentions failure but not explicit scenarios |
| Try It Now | ✅ PASS | Clear action item |
| Voice/Style | ❌ FAIL | "90% of Developers Are Sabotaging" is clickbait |

**Metadata Issues:**
- `"title": "You're Using Sub-Agents Wrong: 90% of Developers Are Sabotaging"` - clickbait percentage claim
- No source for the "90%" claim

**Required Changes:**
1. **Retitle**: "Sub-Agents for Research: The File-Based Pattern That Works"
2. **Add 300+ words** covering:
   - When research delegation fails (simple tasks, time-sensitive work)
   - Overhead of context file management
   - Cost comparison: sub-agent research vs manual research
3. **Remove unsubstantiated "90%" claim**

---

### Post 04: Beyond the Chat Box

**Current Title:** "Chat UI Is Dead: Why Agentic Drop Zones Are the Future of AI Automation"

**Tenet Violations:**
| Tenet | Status | Issue |
|-------|--------|-------|
| POC Rule | ✅ PASS | Has complete drop_watcher.py |
| Numbers Test | ⚠️ WEAK | "2 hours → 2 minutes" but no specific validation |
| Production Lens | ⚠️ WEAK | Limited error handling discussion |
| Senior Engineer Filter | ✅ PASS | Valuable automation pattern |
| Honest Failure Requirement | ❌ FAIL | No failure modes |
| Try It Now | ✅ PASS | Clear action item |
| Voice/Style | ❌ FAIL | "Chat UI Is Dead" is sensationalist |

**Metadata Issues:**
- `"title": "Chat UI Is Dead"` - sensationalist, false (chat UI is not dead)
- `"callToAction": "Keep chatting. Or start dropping."` - acceptable

**Required Changes:**
1. **Retitle**: "Directory Watchers: File-Based AI Automation That Scales"
2. **Add 300+ words** covering:
   - When drop zones fail (files that need context, multi-file inputs)
   - Error handling and monitoring
   - File system race conditions
   - Maintenance overhead
3. **Add production deployment considerations**

---

### Post 05: Custom Agents Are The Endgame

**Current Title:** "The Agent Endgame: Stop Renting Default Agents and Start Building Your Own"

**Tenet Violations:**
| Tenet | Status | Issue |
|-------|--------|-------|
| POC Rule | ✅ PASS | Has pong, calculator, code review agents |
| Numbers Test | ✅ PASS | Model cost comparison table |
| Production Lens | ⚠️ WEAK | Mentions security but not detailed |
| Senior Engineer Filter | ✅ PASS | Valuable SDK patterns |
| Honest Failure Requirement | ⚠️ WEAK | Limited failure discussion |
| Try It Now | ✅ PASS | Clear action item |
| Voice/Style | ✅ PASS | Title is direct but not hype |

**Metadata Issues:**
- Title is acceptable ("Stop Renting Default Agents" is strong but not hype)

**Required Changes:**
1. **Keep title** (acceptable)
2. **Add 200+ words** covering:
   - When custom agents fail (over-engineering, maintenance burden)
   - Cost of building vs using defaults
   - Testing and validation challenges
3. **Expand security considerations section**

---

### Post 06: 55,000 Files in 5 Minutes

**Current Title:** "55,000 Files in 5 Minutes: How to Make AI Coding Agents Actually Work on Large Codebases"

**Tenet Violations:**
| Tenet | Status | Issue |
|-------|--------|-------|
| POC Rule | ⚠️ WEAK | Configuration shown but no complete script |
| Numbers Test | ✅ PASS | 36x, 28x, 23x improvements with $ amounts |
| Production Lens | ⚠️ WEAK | Limited setup complexity discussion |
| Senior Engineer Filter | ✅ PASS | Valuable large codebase content |
| Honest Failure Requirement | ❌ FAIL | No failure modes |
| Try It Now | ✅ PASS | Clear action item |
| Voice/Style | ✅ PASS | Title is specific and factual |

**Metadata Issues:**
- `"provocative": "Using AI coding tools without proper setup is like eating spaghetti with a spoon"` - acceptable analogy

**Required Changes:**
1. **Keep title** (acceptable - specific numbers, not hype)
2. **Add 400+ words** covering:
   - When semantic search fails (non-standard languages, generated code)
   - Setup complexity and time investment
   - Language support limitations
   - Indexing time and resource requirements
3. **Add complete working example script**

---

## Metadata Cleanup Required

### Files to Update:

1. **`01-prompts-are-the-new-code/metadata.json`**
   - Remove `emotionalHooks` section
   - Remove `controversialClaims` section
   - Update title to remove "Obsolete"
   - Update SEO fields

2. **`02-context-window-bleeding/metadata.json`**
   - Update title to remove "Bandaid on a Bullet Wound"
   - Update SEO fields

3. **`03-subagents-wrong/metadata.json`**
   - Update title to remove "90% of Developers Are Sabotaging"
   - Remove unsubstantiated percentage claims

4. **`04-chat-ui-is-dead/metadata.json`**
   - Update title to remove "Chat UI Is Dead"
   - Update subtitle

5. **`05-agent-endgame/metadata.json`** - Minor updates only

6. **`06-55k-files-5-minutes/metadata.json`** - Minor updates only

---

## Implementation Priority

### Phase 1: Critical Rewrites (High Impact)

1. **Post 01** - Foundation post, sets tone for entire blog
2. **Post 02** - High-value optimization content, needs failure modes
3. **Post 03** - Core delegation pattern, needs title fix

### Phase 2: Enhancement (Medium Impact)

4. **Post 04** - Good content, needs title fix and failure modes
5. **Post 06** - Strong numbers, needs POC enhancement

### Phase 3: Polish (Lower Priority)

6. **Post 05** - Already closest to tenets, minor additions

---

## Combination Opportunities

**Considered but NOT recommended:**

While some posts share themes, each addresses a distinct pattern:
- Post 01 (workflow prompts) ≠ Post 05 (custom SDK agents) - different abstraction levels
- Post 02 (context optimization) ≠ Post 03 (sub-agent delegation) - different solutions
- Post 04 (drop zones) ≠ Post 06 (semantic search) - different problem domains

**Recommendation:** Keep posts separate but strengthen cross-references between them.

---

## Revised Title Proposals

| Current | Proposed |
|---------|----------|
| Prompts Are the New Code: The 7-Level Framework That's Making Traditional Programming Obsolete | **Workflow Prompts: The Pattern That Makes AI Engineering Predictable** |
| Your Context Window Is Bleeding: Why MCP Servers Are a Bandaid on a Bullet Wound | **Progressive Disclosure: Cutting Context Consumption by 95%** |
| You're Using Sub-Agents Wrong: 90% of Developers Are Sabotaging Their AI Workflows | **Sub-Agents for Research: The File-Based Context Pattern** |
| Chat UI Is Dead: Why Agentic Drop Zones Are the Future of AI Automation | **Directory Watchers: File-Based AI Automation That Scales** |
| The Agent Endgame: Stop Renting Default Agents and Start Building Your Own | **Custom Agents Are The Endgame** (keep) |
| 55,000 Files in 5 Minutes: How to Make AI Coding Agents Actually Work on Large Codebases | **55,000 Files in 5 Minutes** (keep, already strong) |

---

## Success Criteria

After rewrites, each post must:

- [ ] Hit 2,000-2,500 word count
- [ ] Pass all 6 tenets without violations
- [ ] Have title following Problem-Solution or specific number format
- [ ] Include explicit "What Doesn't Work" or "Limitations" section
- [ ] Have metadata free of hype-speak and fear-mongering
- [ ] Include at least one specific, verifiable benchmark
