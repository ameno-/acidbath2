# Feature: Copywriting Skills Framework

## Metadata
adw_id: `e71e0fb5`
prompt: `Issue #19 - Improve copywriting: Create new copywriting skills (Mad Men Copywriter and Master Copywriter) for strategic use on posts/content. Migrate existing "Ameno voice" skill out of core blog workflows. Create suggest_edits framework for personality injection. Add comprehensive test coverage.`

## Feature Description

This feature creates a new copywriting skills framework to diversify ACIDBATH's writing style. It introduces two high-impact copywriting skills (Mad Men Copywriter and Master Copywriter) while migrating the existing "Ameno voice" skill into a standalone, non-integrated tool for selective personality injection.

The key innovation is the `suggest_edits` framework - a new editing pattern that generates targeted edit suggestions rather than automatically applying changes. This preserves editorial control while allowing strategic personality injection across different writing styles.

## User Story

As a content creator for ACIDBATH,
I want access to multiple specialized copywriting skills that can suggest strategic edits to my content,
So that I can selectively apply different writing personalities (Mad Men conversion-focused, Master Copywriter persuasion-focused, or Ameno technical-friendly) based on the content type and target audience, without losing control over the final voice.

## Problem Statement

ACIDBATH currently has only one voice style (Ameno voice) which is:
1. **Tightly integrated** into blog post workflows (`/new-post`, `/ameno-finalize`)
2. **Automatically applied** during content creation/finalization
3. **Single-purpose** - focused on simplifying technical concepts with personality
4. **Lacks diversity** - cannot adapt to different content types (landing pages, sales copy, social media, different blog post styles)

This creates several issues:
- **Limited flexibility**: Cannot switch writing styles for different content types
- **Loss of control**: Automatic application doesn't allow selective personality injection
- **No test coverage**: Changes to voice implementation risk breaking existing content
- **Tight coupling**: Ameno voice is embedded in core workflows, making it hard to evolve independently

## Solution Statement

Create a **multi-voice copywriting framework** with three distinct skills:

1. **Mad Men Copywriter** - Conversion-focused, aggressive sales copy (from issue description)
2. **Master Copywriter** - Persuasion-focused, sophisticated marketing copy (planned)
3. **Ameno Voice** - Technical simplification with personality (existing, migrated)

All skills use a new **`suggest_edits` pattern**:
- Generate edit suggestions with before/after comparisons
- Provide rationale for each suggested change
- Allow users to selectively apply edits
- Never automatically modify content

This decouples copywriting from workflows, adds test coverage, and preserves editorial control.

## Relevant Files

### Existing Files to Modify

- **`.claude/commands/new-post.md`** - Remove Ameno voice integration from post creation workflow
- **`.claude/commands/ameno-finalize.md`** - Convert to suggest_edits pattern instead of auto-apply
- **`ai_docs/ameno-voice-style.md`** - Update to reflect suggest_edits pattern
- **`.claude/skills/ameno-voice/SKILL.md`** - Update to use suggest_edits framework
- **`.claude/skills/ameno-voice/EXAMPLES.md`** - Add suggest_edits examples
- **`README.md`** - Update Skills & Commands section with new copywriting framework

### New Files

#### Copywriting Skills

- **`.claude/skills/mad-men-copywriter/SKILL.md`** - Mad Men skill definition with suggest_edits pattern
- **`.claude/skills/mad-men-copywriter/VOICE_DNA.md`** - Mad Men voice characteristics and rules
- **`.claude/skills/mad-men-copywriter/EXAMPLES.md`** - Before/after transformations with rationale
- **`.claude/skills/mad-men-copywriter/FRAMEWORKS.md`** - Copywriting frameworks (AIDA, PAS, etc.)
- **`.claude/skills/master-copywriter/SKILL.md`** - Master Copywriter skill definition
- **`.claude/skills/master-copywriter/VOICE_DNA.md`** - Master Copywriter voice characteristics
- **`.claude/skills/master-copywriter/EXAMPLES.md`** - Before/after examples
- **`.claude/skills/master-copywriter/FRAMEWORKS.md`** - Persuasion frameworks

#### Commands

- **`.claude/commands/mad-men-edit.md`** - Command to invoke Mad Men copywriting skill
- **`.claude/commands/master-copy-edit.md`** - Command to invoke Master Copywriter skill

#### Framework Documentation

- **`ai_docs/suggest-edits-framework.md`** - Core framework documentation
- **`ai_docs/copywriting-skills.md`** - Overview of all copywriting skills and when to use each

#### Tests

- **`tests/skills/test_copywriting_skills.py`** - Test suite for all copywriting skills
- **`tests/skills/test_suggest_edits_framework.py`** - Test suite for suggest_edits pattern
- **`tests/skills/fixtures/sample_content.md`** - Test content samples
- **`tests/skills/fixtures/expected_edits.json`** - Expected edit suggestion formats

#### Sample Content for PR

- **`samples/copywriting-demos/mad-men-demo.md`** - Sample Mad Men edits on actual content
- **`samples/copywriting-demos/master-copy-demo.md`** - Sample Master Copywriter edits
- **`samples/copywriting-demos/ameno-demo.md`** - Sample Ameno voice edits (migrated pattern)

## Implementation Plan

### Phase 1: Foundation - Suggest Edits Framework

Create the core `suggest_edits` framework that all copywriting skills will use. This establishes the pattern before implementing individual skills.

**Key components:**
- Edit suggestion data structure (before/after, rationale, section type)
- Output format specification (markdown with clear visual separation)
- Framework documentation with implementation guidelines

### Phase 2: Core Implementation - Copywriting Skills

Implement the three copywriting skills using the suggest_edits framework:

1. **Mad Men Copywriter** - From issue description, conversion-focused
2. **Master Copywriter** - Persuasion-focused, sophisticated
3. **Ameno Voice** - Migrate existing skill to new pattern

Each skill includes:
- SKILL.md with frontmatter and suggest_edits instructions
- VOICE_DNA.md defining personality, tone, and rules
- EXAMPLES.md with before/after transformations
- FRAMEWORKS.md with applicable copywriting/persuasion patterns

### Phase 3: Integration

1. **Decouple Ameno voice** from `/new-post` and `/ameno-finalize` workflows
2. **Update commands** to use suggest_edits pattern
3. **Add sample content** demonstrating each skill's output
4. **Comprehensive test coverage** for all skills and framework
5. **Documentation updates** in README and ai_docs

## Step by Step Tasks

### Group A: Foundation - Suggest Edits Framework [parallel: false, model: sonnet]

Sequential foundation work that establishes the core framework.

#### Step A.1: Create Suggest Edits Framework Documentation

- Create `ai_docs/suggest-edits-framework.md` with:
  - Framework purpose and philosophy (suggest, don't auto-apply)
  - Edit suggestion data structure specification
  - Output format specification (markdown template)
  - Implementation guidelines for skill creators
  - Example suggest_edits flow from start to finish
- Define standard edit suggestion format:
  ```markdown
  ## Suggested Edit {N}: {Section Name}

  **Type**: {concept-explanation|failure-mode|takeaway|introduction|cta}
  **Rationale**: {Why this edit improves the content}

  ### Before
  ```
  {original content}
  ```

  ### After
  ```
  {suggested content}
  ```

  ### Apply This Edit?
  - [ ] Yes, apply as-is
  - [ ] Apply with modifications
  - [ ] Skip this edit
  ```

#### Step A.2: Create Test Infrastructure

- Create `tests/skills/` directory structure
- Create `tests/skills/fixtures/` directory
- Create `tests/skills/fixtures/sample_content.md` with diverse content types:
  - Technical introduction (should stay direct)
  - Concept explanation (candidate for personality)
  - Code example (should stay clean)
  - Failure mode section (candidate for conversational honesty)
  - Benchmark table (should stay factual)
  - Takeaway section (candidate for memorable style)
- Create `tests/skills/fixtures/expected_edits.json` defining expected edit structure

#### Step A.3: Create Framework Test Suite

- Create `tests/skills/test_suggest_edits_framework.py` with tests for:
  - Edit suggestion format validation
  - Required fields presence (type, rationale, before, after)
  - Output markdown structure
  - No auto-modification verification (framework should NEVER write files)
  - Clear visual separation between suggestions
  - Proper section type classification

### Group B: Core Implementation - Mad Men Copywriter Skill [parallel: false, depends: A, model: auto]

Implement the Mad Men Copywriter skill based on the issue description.

#### Step B.1: Extract and Formalize Mad Men Prompt

- Create `.claude/skills/mad-men-copywriter/` directory
- Create `VOICE_DNA.md` based on issue description prompt:
  - Context: "Write copy that fucking sells"
  - Role: Senior copywriter, 15+ years, conversion-focused
  - Response guidelines (hook in 2 seconds, lead with pain, etc.)
  - Information collection (Product, Audience, Platform, Desired Action, USP)
  - Constraints (specs, scannability, platform rules, emotion+logic+proof)
  - Output requirements (Headline, Subheadline, Body, CTA, A/B variant)
- Adapt the raw prompt into structured voice characteristics:
  - Primary trait: Conversion obsession (every word must sell)
  - Tone: Aggressive, direct, no-nonsense
  - Techniques: Pain-first, value by word 50, eliminate weak sentences
  - Vocabulary: Action verbs, power words, no hedging
  - Anti-patterns: Fluff, passive voice, "cute" over clear

#### Step B.2: Create Mad Men Skill Definition

- Create `.claude/skills/mad-men-copywriter/SKILL.md` with:
  - YAML frontmatter:
    ```yaml
    ---
    name: mad-men-copywriter
    description: Conversion-focused copywriting that drives action. Use for landing pages, sales copy, CTAs, and content where immediate conversion is the goal. Uses suggest_edits pattern to propose aggressive, results-driven copy changes.
    allowed-tools: Read
    ---
    ```
  - Quick reference checklist (hook strength, pain deployment, CTA clarity)
  - When to use Mad Men voice (sales pages, conversion-focused content)
  - When NOT to use (technical docs, educational content, code examples)
  - Suggest_edits implementation instructions
  - Link to VOICE_DNA.md and EXAMPLES.md

#### Step B.3: Create Mad Men Frameworks and Examples

- Create `.claude/skills/mad-men-copywriter/FRAMEWORKS.md`:
  - AIDA (Attention, Interest, Desire, Action)
  - PAS (Problem, Agitate, Solution)
  - 4Ps (Picture, Promise, Prove, Push)
  - Before-After-Bridge
  - Each framework includes:
    - When to use
    - Structure template
    - Mad Men adaptation (how to apply conversion focus)
- Create `.claude/skills/mad-men-copywriter/EXAMPLES.md`:
  - 5-7 before/after transformations showing:
    - Weak headline → Conversion-focused headline
    - Generic intro → Pain-first intro
    - Soft CTA → Aggressive CTA
    - Feature list → Benefit-driven copy
    - Technical explanation → Results-focused explanation
  - Each example includes rationale explaining the edit

#### Step B.4: Create Mad Men Command

- Create `.claude/commands/mad-men-edit.md`:
  - Usage: `/mad-men-edit {file_path}`
  - Process:
    1. Read the content file
    2. Analyze for conversion opportunities
    3. Generate edit suggestions using suggest_edits pattern
    4. Focus on: headlines, CTAs, value propositions, pain points
  - Output format specification (markdown with edit suggestions)
  - Anti-pattern checks (ensure tech sections stay direct)

### Group C: Core Implementation - Master Copywriter Skill [parallel: true, depends: A, model: auto]

Implement Master Copywriter skill in parallel with Ameno migration (independent work).

#### Step C.1: Design Master Copywriter Voice DNA

- Create `.claude/skills/master-copywriter/` directory
- Create `VOICE_DNA.md` defining Master Copywriter characteristics:
  - Context: Persuasion-focused, sophisticated marketing copy
  - Role: Master copywriter with deep psychology knowledge
  - Primary trait: Persuasion through credibility and trust
  - Tone: Authoritative yet approachable, professional but warm
  - Techniques: Storytelling, social proof, authority building, reciprocity
  - Vocabulary: Precise language, power of specificity, strategic repetition
  - Differentiation from Mad Men:
    - Mad Men: Aggressive conversion → "Buy now or lose out"
    - Master: Persuasive credibility → "Here's why this matters to you"

#### Step C.2: Create Master Copywriter Skill Definition

- Create `.claude/skills/master-copywriter/SKILL.md` with:
  - YAML frontmatter:
    ```yaml
    ---
    name: master-copywriter
    description: Persuasion-focused copywriting that builds credibility and trust. Use for thought leadership, long-form content, brand building, and content where trust and authority matter more than immediate conversion. Uses suggest_edits pattern.
    allowed-tools: Read
    ---
    ```
  - Quick reference checklist (credibility signals, story structure, proof points)
  - When to use Master Copywriter (thought leadership, educational content with persuasion)
  - When NOT to use (pure technical docs, quick conversion pages)
  - Suggest_edits implementation instructions

#### Step C.3: Create Master Copywriter Frameworks and Examples

- Create `.claude/skills/master-copywriter/FRAMEWORKS.md`:
  - Hero's Journey (for narrative content)
  - Cialdini's 6 Principles (Reciprocity, Commitment, Social Proof, Authority, Liking, Scarcity)
  - StoryBrand Framework (Character, Problem, Guide, Plan, Call, Success, Avoid Failure)
  - Inverted Pyramid (Lead with most important, add supporting details)
- Create `.claude/skills/master-copywriter/EXAMPLES.md`:
  - 5-7 before/after transformations showing:
    - Generic intro → Story-driven intro
    - Claim without proof → Claim with social proof
    - Technical feature → Benefit with authority backing
    - Weak case study → Compelling narrative
    - Flat conclusion → Inspirational call to value

#### Step C.4: Create Master Copywriter Command

- Create `.claude/commands/master-copy-edit.md`:
  - Usage: `/master-copy-edit {file_path}`
  - Process focused on persuasion elements
  - Output format using suggest_edits pattern

### Group D: Core Implementation - Ameno Voice Migration [parallel: true, depends: A, model: auto]

Migrate existing Ameno voice to suggest_edits pattern (parallel with Master Copywriter).

#### Step D.1: Update Ameno Voice Skill for Suggest Edits

- Update `.claude/skills/ameno-voice/SKILL.md`:
  - Add suggest_edits pattern instructions
  - Remove auto-apply language
  - Add section on generating edit suggestions with rationale
  - Update example flow to show suggestion format
  - Add checklist for evaluating suggested edits

#### Step D.2: Update Ameno Voice Examples

- Update `.claude/skills/ameno-voice/EXAMPLES.md`:
  - Convert all examples to suggest_edits format
  - Add rationale for each example
  - Show section type classification (concept-explanation, failure-mode, etc.)
  - Include examples of sections that should NOT be edited

#### Step D.3: Decouple Ameno from New Post Workflow

- Update `.claude/commands/new-post.md`:
  - Remove Ameno voice application from creation process
  - Keep ACIDBATH direct voice as default
  - Add note about optional finalization with `/ameno-finalize` AFTER drafting
  - Clarify workflow: Create (direct) → Review → Optionally apply voice

#### Step D.4: Update Ameno Finalize Command

- Update `.claude/commands/ameno-finalize.md`:
  - Convert from auto-apply to suggest_edits pattern
  - Process:
    1. Read the post
    2. Classify sections by type
    3. Generate edit suggestions for appropriate sections
    4. Output suggestions with rationale
  - Remove file writing - only output suggestions
  - Update output format to match suggest_edits framework

### Group E: Testing and Validation [parallel: false, depends: B, C, D, model: sonnet]

Comprehensive test coverage for all skills and framework.

#### Step E.1: Create Copywriting Skills Test Suite

- Create `tests/skills/test_copywriting_skills.py`:
  - Test for Mad Men Copywriter:
    - Validates edit suggestions focus on conversion
    - Checks for pain-first hooks
    - Verifies aggressive CTAs
    - Ensures no auto-modification
  - Test for Master Copywriter:
    - Validates persuasion techniques
    - Checks for credibility signals
    - Verifies story elements where appropriate
    - Ensures no auto-modification
  - Test for Ameno Voice:
    - Validates simplification without metaphor overuse
    - Checks section type classification
    - Verifies direct sections remain unchanged
    - Ensures no auto-modification

#### Step E.2: Create Integration Tests

- Add integration tests to `tests/skills/test_copywriting_skills.py`:
  - Test all three skills on the same content piece
  - Verify each produces different, appropriate suggestions
  - Validate output format consistency across skills
  - Test edge cases:
    - Content with no edit opportunities (should say so)
    - Pure code content (should skip or suggest minimal edits)
    - Mixed content types (should classify sections correctly)

#### Step E.3: Add Regression Tests

- Create regression test suite:
  - Use existing published blog posts as fixtures
  - Run all three skills on published content
  - Verify suggestions align with skill philosophy
  - Ensure no breaking changes to suggest_edits format
  - Test with `uv run adws/run_tests.py -m copywriting_skills`

### Group F: Documentation and Samples [parallel: true, depends: E, model: auto]

Create comprehensive documentation and sample content.

#### Step F.1: Create Copywriting Overview Documentation

- Create `ai_docs/copywriting-skills.md`:
  - Overview of the copywriting skills framework
  - Comparison table of three skills:
    | Skill | Focus | When to Use | Tone | Primary Technique |
    |-------|-------|-------------|------|-------------------|
    | Mad Men | Conversion | Sales pages, CTAs | Aggressive | Pain → Solution → Action |
    | Master | Persuasion | Thought leadership | Authoritative | Credibility → Trust → Decision |
    | Ameno | Simplification | Technical content | Technical-friendly | Direct → Clarity → Memorable |
  - Decision tree: "Which skill should I use?"
  - Integration with ACIDBATH editorial philosophy
  - How suggest_edits preserves editorial control

#### Step F.2: Create Sample Demonstrations

- Create `samples/copywriting-demos/` directory
- Create `samples/copywriting-demos/mad-men-demo.md`:
  - Take a real blog post section (landing page style content)
  - Show Mad Men suggested edits
  - Include before/after for 5-7 edits
  - Show rationale for each
  - Demonstrate conversion-focus
- Create `samples/copywriting-demos/master-copy-demo.md`:
  - Take a real blog post (thought leadership style)
  - Show Master Copywriter suggested edits
  - Include before/after for 5-7 edits
  - Show persuasion techniques applied
- Create `samples/copywriting-demos/ameno-demo.md`:
  - Take a technical blog post
  - Show Ameno voice suggested edits
  - Demonstrate simplification without metaphor abuse
  - Show sections correctly left unchanged

#### Step F.3: Update README Documentation

- Update `README.md`:
  - Add Copywriting Skills Framework section under Skills & Commands
  - List all three skills with descriptions
  - Add usage examples for each command
  - Update workflow diagram to show optional copywriting step
  - Link to `ai_docs/copywriting-skills.md` and `ai_docs/suggest-edits-framework.md`

#### Step F.4: Update AI Documentation

- Update `ai_docs/ameno-voice-style.md`:
  - Add section on suggest_edits pattern
  - Update workflow position (now optional, suggestion-based)
  - Clarify relationship with other copywriting skills
  - Update integration points

## Testing Strategy

### Unit Tests

**Framework Tests** (`tests/skills/test_suggest_edits_framework.py`):
- Edit suggestion format validation
- Required fields presence
- Output structure verification
- No-modification guarantee

**Skill Tests** (`tests/skills/test_copywriting_skills.py`):
- Mad Men Copywriter:
  - Conversion-focused edit detection
  - Pain-first hook validation
  - CTA aggressiveness check
  - Technical section preservation
- Master Copywriter:
  - Persuasion technique detection
  - Credibility signal validation
  - Story element presence
  - Authority building check
- Ameno Voice:
  - Simplification without metaphor abuse
  - Section type classification accuracy
  - Direct section preservation
  - Rationale clarity

**Integration Tests**:
- Run all three skills on same content
- Verify different, appropriate suggestions
- Format consistency across skills
- Edge case handling

### Edge Cases

1. **Empty or minimal content**: Skills should gracefully handle and suggest no edits or minimal changes
2. **Pure code content**: Should skip or suggest only minimal, relevant edits
3. **Already optimized content**: Should recognize and suggest few/no changes
4. **Mixed content types**: Should correctly classify sections and apply appropriate edits
5. **Content with inline code/technical terms**: Should preserve technical accuracy
6. **Lists and tables**: Should handle structured content appropriately
7. **Long-form content (5000+ words)**: Should not suggest excessive edits (suggest only high-impact changes)
8. **Content with existing personality**: Should recognize and enhance, not override

## Acceptance Criteria

### Framework Acceptance

- [ ] `suggest_edits` framework documentation is comprehensive and includes implementation guide
- [ ] Framework guarantees no auto-modification (all skills only suggest, never write)
- [ ] Edit suggestion format is consistent across all skills
- [ ] Framework has test coverage with clear validation

### Mad Men Copywriter Acceptance

- [ ] Mad Men skill produces conversion-focused suggestions
- [ ] Suggestions include clear rationale linked to conversion goals
- [ ] Skill correctly identifies sections suitable for aggressive copy
- [ ] Skill preserves technical/code sections without conversion-speak
- [ ] VOICE_DNA accurately captures the prompt from issue #19
- [ ] Examples demonstrate clear before/after with measurable improvement

### Master Copywriter Acceptance

- [ ] Master Copywriter skill produces persuasion-focused suggestions
- [ ] Suggestions include credibility-building and trust signals
- [ ] Skill correctly identifies sections suitable for authority building
- [ ] Skill differs meaningfully from Mad Men (persuasion vs conversion)
- [ ] Examples demonstrate sophisticated, trust-building copy

### Ameno Voice Migration Acceptance

- [ ] Ameno voice skill uses suggest_edits pattern (no auto-apply)
- [ ] `/ameno-finalize` command outputs suggestions, doesn't modify files
- [ ] `/new-post` workflow no longer auto-applies Ameno voice
- [ ] Existing Ameno voice characteristics preserved in new pattern
- [ ] Migration doesn't break existing content or workflows

### Testing Acceptance

- [ ] All skills have comprehensive test coverage
- [ ] Framework has dedicated test suite
- [ ] Integration tests cover multi-skill scenarios
- [ ] Edge cases are tested and handled gracefully
- [ ] Tests can be run with `uv run adws/run_tests.py -m copywriting_skills`
- [ ] All tests pass in CI

### Documentation Acceptance

- [ ] `ai_docs/suggest-edits-framework.md` is complete and clear
- [ ] `ai_docs/copywriting-skills.md` provides clear skill comparison
- [ ] Each skill has complete VOICE_DNA, EXAMPLES, and FRAMEWORKS files
- [ ] README updated with copywriting framework section
- [ ] Sample demos show each skill in action

### Sample Content Acceptance

- [ ] Three sample demonstrations created (Mad Men, Master, Ameno)
- [ ] Each sample includes 5-7 edit suggestions with rationale
- [ ] Samples demonstrate real-world usage on actual content
- [ ] Samples are included in PR comments for review

## Validation Commands

Execute these commands to validate the feature is complete:

### Framework Validation
```bash
# Verify framework documentation exists
ls -la ai_docs/suggest-edits-framework.md

# Verify framework tests exist and pass
uv run pytest tests/skills/test_suggest_edits_framework.py -v
```

### Skills Validation
```bash
# Verify all skill files exist
ls -la .claude/skills/mad-men-copywriter/
ls -la .claude/skills/master-copywriter/
ls -la .claude/skills/ameno-voice/

# Verify all commands exist
ls -la .claude/commands/mad-men-edit.md
ls -la .claude/commands/master-copy-edit.md
ls -la .claude/commands/ameno-finalize.md

# Verify skills tests pass
uv run pytest tests/skills/test_copywriting_skills.py -v
```

### Integration Validation
```bash
# Run all copywriting tests
uv run adws/run_tests.py -m copywriting_skills

# Verify no auto-modification (should only output suggestions)
# This should be a manual test - run each command and verify no files changed
```

### Documentation Validation
```bash
# Verify all documentation exists
ls -la ai_docs/copywriting-skills.md
ls -la samples/copywriting-demos/

# Verify README updated (manual check for copywriting section)
grep -n "Copywriting Skills" README.md
```

### Sample Content Validation
```bash
# Verify sample demos exist
ls -la samples/copywriting-demos/mad-men-demo.md
ls -la samples/copywriting-demos/master-copy-demo.md
ls -la samples/copywriting-demos/ameno-demo.md

# Count edit suggestions in each demo (should be 5-7 each)
grep -c "## Suggested Edit" samples/copywriting-demos/mad-men-demo.md
grep -c "## Suggested Edit" samples/copywriting-demos/master-copy-demo.md
grep -c "## Suggested Edit" samples/copywriting-demos/ameno-demo.md
```

### Ameno Migration Validation
```bash
# Verify new-post.md doesn't auto-apply Ameno
grep -i "ameno" .claude/commands/new-post.md | grep -v "optional\|after\|finalize"
# Should return no matches (no auto-application)

# Verify ameno-finalize uses suggest_edits
grep -i "suggest_edits\|suggestions" .claude/commands/ameno-finalize.md
# Should find references to suggestion pattern
```

### End-to-End Validation

**Manual test workflow**:
1. Create test content file with mixed sections (intro, concept, code, failure, takeaway)
2. Run `/mad-men-edit {file}` - verify conversion-focused suggestions, no file changes
3. Run `/master-copy-edit {file}` - verify persuasion-focused suggestions, different from Mad Men
4. Run `/ameno-finalize {file}` - verify simplification suggestions, different from others
5. Verify all three produce valid suggest_edits format
6. Verify original file remains unchanged

## Notes

### Implementation Priority

The issue requests "work in parallel loops until task is fully complete." Here's the parallel execution strategy:

**Sequential (must be done in order)**:
- Group A (Foundation) must complete before any skills work
- Group E (Testing) requires Groups B, C, D to be complete
- Group F (Documentation) can start after testing passes

**Parallel (can be done simultaneously)**:
- Group B (Mad Men), Group C (Master Copywriter), and Group D (Ameno Migration) are independent
- Within Group F, all four steps can be done in parallel

### Key Design Decisions

1. **suggest_edits pattern**: Chosen over auto-apply to preserve editorial control. This is critical for a multi-voice system where different skills might suggest conflicting changes.

2. **Three skills instead of two**: The issue mentions Mad Men and Master Copywriter, but preserving Ameno voice (migrated to new pattern) creates a complete framework covering conversion → persuasion → simplification.

3. **No workflow integration**: Deliberately keeping copywriting skills as standalone commands rather than integrating them into `/new-post` or other workflows. This prevents coupling and allows strategic, selective use.

4. **Comprehensive VOICE_DNA files**: Each skill has a dedicated DNA file to formalize personality, tone, and rules. This makes skills maintainable and extensible.

5. **Framework-first approach**: Building suggest_edits framework before skills ensures consistency and reduces duplication.

### Future Considerations

- **Additional skills**: Framework is extensible for future copywriting personalities (Technical Writer, Story Seller, etc.)
- **Combination patterns**: Could create commands that apply multiple skills sequentially (e.g., Ameno for simplification, then Mad Men for CTAs)
- **A/B testing support**: Could extend suggest_edits to generate variant suggestions for testing
- **Metrics integration**: Could track which suggested edits lead to better engagement/conversion

### Dependencies

**Python packages** (add with `uv add` if needed):
- `pytest` - Already available, used for tests
- `pytest-cov` - Already available, for coverage
- No new packages required

**Existing patterns to follow**:
- Skill structure: Follow `.claude/skills/ameno-voice/` pattern
- Test structure: Follow `adws/run_tests.py` pattern
- Documentation: Follow `ai_docs/ameno-voice-style.md` style

### PR Comment Content

When creating PR, include in comments:

**Sample Mad Men Edit** (1-2 examples from `samples/copywriting-demos/mad-men-demo.md`)
**Sample Master Copywriter Edit** (1-2 examples from `samples/copywriting-demos/master-copy-demo.md`)
**Sample Ameno Edit** (1-2 examples from `samples/copywriting-demos/ameno-demo.md`)

This gives reviewers immediate visibility into each skill's output quality and differentiation.
