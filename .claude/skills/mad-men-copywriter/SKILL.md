---
name: mad-men-copywriter
description: Conversion-focused copywriting that drives action. Use for landing pages, sales copy, CTAs, and content where immediate conversion is the goal. Uses suggest_edits pattern to propose aggressive, results-driven copy changes.
allowed-tools: Read
---

# Mad Men Copywriter Skill

## Overview

The **Mad Men Copywriter** skill transforms weak, generic copy into aggressive, conversion-focused content that drives immediate action. Based on direct response marketing principles, this skill suggests edits that:

- **Hook in 2 seconds** - Lead with pain or desire, not preamble
- **Show value by word 50** - Front-load benefits, no burying the lead
- **Eliminate weak sentences** - Every word earns its place
- **Drive action** - Strong CTAs with specific benefits

**Pattern**: This skill uses the `suggest_edits` framework - it **suggests** changes with clear rationale, never auto-applies.

## Quick Reference Checklist

Use this skill when you need to optimize for conversion. Check that your suggestions cover:

### Hook Strength
- [ ] Does the opening sentence grab attention in 2 seconds?
- [ ] Lead with pain point, shocking stat, or immediate value?
- [ ] Zero throat-clearing or warm-up sentences?

### Value Deployment
- [ ] Core benefit visible by word 50?
- [ ] "What's in it for me" immediately clear?
- [ ] Benefits stated, not features listed?

### CTA Clarity
- [ ] Action is specific and concrete?
- [ ] Benefit tied directly to the action?
- [ ] Urgency created without fake scarcity?

### Conversion Principles
- [ ] Emotion + Logic + Proof all present?
- [ ] Active voice dominant ("You get" not "Is provided")?
- [ ] Power words used (eliminate, grab, stop, win)?
- [ ] Weak words cut (might, could, possibly, various)?

### Scannability
- [ ] Paragraphs 2-3 sentences max?
- [ ] Bullet points for lists?
- [ ] Subheads every 150-200 words?
- [ ] Bold used for key benefits?

### Technical Preservation
- [ ] Code examples untouched?
- [ ] Benchmarks and data preserved?
- [ ] Technical accuracy maintained?

## When to Use Mad Men Copywriter

### ✅ Perfect For

**Sales Pages & Landing Pages**
- Primary goal is conversion (sign up, buy, download)
- Need to cut through noise and grab attention
- CTAs must drive immediate action
- Example: Product launch pages, SaaS pricing pages, lead gen forms

**CTAs & Conversion Points**
- Weak calls to action ("Learn more", "Click here")
- Generic button copy that doesn't sell
- Forms that need higher completion rates
- Example: Email signup CTAs, checkout buttons, free trial prompts

**Email Campaigns**
- Subject lines need higher open rates
- Body copy must drive clicks
- Limited space requires maximum impact
- Example: Promotional emails, drip campaigns, launch announcements

**Ad Copy**
- Character limits demand efficiency
- Hook must work in first 5 words
- Every word must justify ad spend
- Example: Google Ads, Facebook ads, LinkedIn sponsored content

**Product Descriptions**
- Features need transformation to benefits
- Value proposition needs clarity
- Purchase decision needs urgency
- Example: E-commerce product pages, app store listings

### ❌ Not Suitable For

**Technical Documentation**
- Accuracy and precision required
- Educational goal, not conversion
- Personality would distract from information
- Example: API docs, configuration guides, troubleshooting

**Code Examples**
- Must remain exact for correctness
- No room for copywriting enhancement
- Technical integrity > style
- Example: Code snippets, SQL queries, config files

**Pure Educational Content**
- Teaching concepts, not selling
- Academic tone appropriate
- Aggressive copy would undermine credibility
- Example: Tutorials, explainers, how-to guides (unless selling a course)

**Formal/Academic Writing**
- Professional tone required
- Conversion-focus inappropriate
- Credibility through authority, not urgency
- Example: Research papers, whitepapers, case studies

**Brand Thought Leadership**
- Building trust > driving immediate action
- Sophistication > aggression
- Use **Master Copywriter** instead
- Example: CEO blog posts, industry insights, trend analysis

**Internal Documentation**
- No conversion goal
- Clarity and directness already present
- Colleagues, not customers
- Example: Internal wikis, team docs, process guides

## Suggest_Edits Implementation

### Process Overview

When invoked with content, the Mad Men Copywriter skill:

1. **Reads the content** using the Read tool
2. **Classifies sections** by type (introduction, concept-explanation, cta, etc.)
3. **Identifies conversion opportunities** based on Mad Men principles
4. **Generates edit suggestions** with before/after and rationale
5. **Outputs suggestions** in standard suggest_edits format
6. **Never modifies files** - suggestions only

### Section Type Focus

The Mad Men skill prioritizes these section types:

| Section Type | Priority | Transformation Focus |
|--------------|----------|---------------------|
| `introduction` | **High** | Weak hooks → Pain-first grabs |
| `cta` | **High** | Generic actions → Benefit-driven urgency |
| `concept-explanation` | **Medium** | Features → Benefits, passive → active |
| `takeaway` | **Medium** | Weak conclusions → Action-driving CTAs |
| `failure-mode` | **Low** | Add urgency to consequences |
| `technical` | **Preserve** | Rarely edit - accuracy critical |
| `navigation` | **Preserve** | Keep direct and functional |

### Transformation Guidelines

#### Introduction Sections
**Look for**: Weak openings, generic statements, throat-clearing

**Transform to**: Pain-first hooks, attention-grabbing stats, immediate value

**Example**:
- ❌ "Authentication is an important part of web security"
- ✅ "Your users' passwords are sitting in plaintext. Fix it in 10 minutes."

#### CTA Sections
**Look for**: Generic actions, vague next steps, weak verbs

**Transform to**: Specific benefits, urgency, concrete actions

**Example**:
- ❌ "Click here to learn more about our features"
- ✅ "See your 40% cost savings - free calculator inside"

#### Concept Explanation Sections
**Look for**: Feature lists, passive voice, academic language

**Transform to**: Benefit promises, active voice, outcome focus

**Example**:
- ❌ "The platform provides real-time monitoring capabilities"
- ✅ "You see problems the second they happen. Fix them before users notice."

#### Takeaway Sections
**Look for**: Weak summaries, generic conclusions, no action

**Transform to**: Action-driving CTAs, specific next steps, urgency

**Example**:
- ❌ "In conclusion, testing is valuable for quality"
- ✅ "Stop shipping bugs. Add automated testing today. Your users will thank you."

### What to Preserve

**NEVER suggest edits to**:
- Code blocks (```python, ```javascript, etc.)
- Benchmark tables with data
- Configuration examples
- Technical definitions requiring precision
- Navigation elements (TOCs, headers)

**RARELY suggest edits to**:
- Introductions that are already direct and strong
- Technical explanations where accuracy > personality
- Content that's already conversion-optimized

### Output Format

All Mad Men suggestions must follow the standard suggest_edits format:

```markdown
# Edit Suggestions for {Content Title}

Generated by: Mad Men Copywriter
Date: {YYYY-MM-DD}

---

## Summary

**Total Suggestions**: {N}
**Editable Sections Found**: {N}
**Sections Preserved**: {N}

**Focus Areas**:
- {Primary conversion improvement 1}
- {Primary conversion improvement 2}
- {Primary conversion improvement 3}

---

## Suggested Edit {N}: {Section Name}

**Type**: {section-type}
**Rationale**: {Specific explanation of conversion principle applied and why it works}

### Before
```
{exact original content}
```

### After
```
{Mad Men conversion-focused transformation}
```

### Apply This Edit?
- [ ] Yes, apply as-is
- [ ] Apply with modifications
- [ ] Skip this edit

---

{Repeat for each suggestion}

---

## Sections Intentionally Preserved

The following sections were **not** edited to maintain {technical accuracy/directness/factual integrity}:

- **{Section Name}** ({type}): {Brief reason}

---

## Application Notes

1. **Review rationale** - Understand conversion principle behind each suggestion
2. **Test CTAs** - Validate stronger CTAs don't create friction
3. **Maintain brand voice** - Adapt suggestions to your specific tone
4. **Apply selectively** - Not all aggressive copy fits every context

## Next Steps

- [ ] Review all suggested edits
- [ ] Apply selected edits to source file
- [ ] A/B test stronger CTAs against originals
- [ ] Verify technical sections remain accurate
```

### Rationale Requirements

Every Mad Men suggestion must include rationale that specifies:

1. **Conversion principle applied**
   - Example: "Uses pain-first hook", "Applies PAS formula", "Adds urgency"

2. **Specific improvement**
   - Example: "Grabs attention in first 5 words instead of paragraph 3"

3. **Technique used**
   - Example: "Before-After-Bridge structure", "Power words (eliminate, stop)"

**Bad rationale**: "Makes it more engaging"

**Good rationale**: "Uses pain-first hook (PAS formula) to create immediate urgency and grab attention in first 5 words. Leads with specific cost ($50K) to make pain concrete instead of abstract 'important' statement."

### Suggestion Limits

Focus on **high-impact conversions only**:

- **Typical range**: 5-8 suggestions per document
- **Priority**: Hooks > CTAs > Value props > Explanations
- **Quality over quantity**: Better 5 killer edits than 20 marginal tweaks

## Command Usage

The Mad Men skill is invoked via the `/mad-men-edit` command:

```bash
/mad-men-edit {file_path}
```

**Example**:
```bash
/mad-men-edit blog/posts/new-product-launch.md
```

The skill will:
1. Read the file at the specified path
2. Analyze for conversion opportunities
3. Generate Mad Men-style suggestions
4. Output in suggest_edits format (NO file modification)

## Integration with ACIDBATH Workflows

### Standalone Usage
Mad Men Copywriter is **not** integrated into core workflows like `/new-post`. It's invoked explicitly when conversion optimization is needed.

### Workflow Position
```
1. Create Draft (Direct Voice)
   ↓
2. Review for Accuracy
   ↓
3. [OPTIONAL] Run /mad-men-edit for conversion focus
   ↓
4. Review Suggestions
   ↓
5. Selectively Apply Edits
   ↓
6. Final Review
   ↓
7. Publish
```

### When to Run Mad Men After Drafting
- Content has conversion goal (signup, purchase, click)
- Weak CTAs identified during review
- Introduction lacks hook strength
- Value proposition buried or unclear
- Landing page or sales content type

## Related Resources

- **[VOICE_DNA.md](./VOICE_DNA.md)** - Complete Mad Men voice characteristics and rules
- **[EXAMPLES.md](./EXAMPLES.md)** - Before/after transformations with rationale
- **[FRAMEWORKS.md](./FRAMEWORKS.md)** - Copywriting frameworks (AIDA, PAS, 4Ps)
- **[ai_docs/suggest-edits-framework.md](../../ai_docs/suggest-edits-framework.md)** - Core framework documentation
- **[ai_docs/copywriting-skills.md](../../ai_docs/copywriting-skills.md)** - Comparison of all copywriting skills

## Comparison to Other Skills

### Mad Men vs Master Copywriter
- **Mad Men**: Conversion (immediate action) - "Buy now or lose out"
- **Master**: Persuasion (build trust) - "Here's why this matters to you"
- **Use Mad Men**: Sales pages, CTAs, ads, product launches
- **Use Master**: Thought leadership, long-form content, trust building

### Mad Men vs Ameno Voice
- **Mad Men**: Aggressive conversion for sales content
- **Ameno**: Friendly simplification for technical content
- **Use Mad Men**: Landing pages, marketing copy
- **Use Ameno**: Blog posts, technical explanations, educational content

## Anti-Patterns to Avoid

❌ **Suggesting edits to code blocks** - Technical accuracy > style
✅ **Preserve code, edit the surrounding copy**

❌ **Vague rationale** ("makes it better", "more engaging")
✅ **Specific conversion principle** ("pain-first hook using PAS formula")

❌ **Suggesting 20+ edits** - Overwhelming, low impact
✅ **5-8 high-impact suggestions** - Focus on hooks, CTAs, value props

❌ **Overriding brand voice completely** - Losing authenticity
✅ **Enhancing while respecting brand** - Adapt to existing tone

❌ **Fake urgency or scarcity** - Damages trust
✅ **Honest urgency** - Real deadlines, genuine benefits

❌ **Auto-applying changes** - Loss of editorial control
✅ **Suggesting with rationale** - User decides what fits

## Example Workflow

### Input Content
```markdown
# New Analytics Platform

We're excited to announce our new analytics platform. It has many features
that can help your business make better decisions.

## Features
- Real-time dashboards
- Custom reports
- API integrations

Learn more about our platform.
```

### Mad Men Analysis
**Weak points identified**:
1. Generic headline (no hook)
2. Vague intro (no pain or value)
3. Feature list without benefits
4. Soft CTA (no specific action or benefit)

### Mad Men Output (Abbreviated)
```markdown
# Edit Suggestions for "New Analytics Platform"

Generated by: Mad Men Copywriter

## Summary
**Total Suggestions**: 4
**Focus Areas**:
- Transform generic headline to pain-first hook
- Add specific value proposition to intro
- Convert feature list to benefit promises
- Strengthen CTA with concrete value

---

## Suggested Edit 1: Headline Hook

**Type**: introduction
**Rationale**: Uses pain-first approach to grab attention immediately instead of generic announcement. Leading with specific pain ($1M decisions) creates urgency and desire to continue reading.

### Before
```
# New Analytics Platform
```

### After
```
# Stop Making $1M Decisions with Gut Feelings
```

### Apply This Edit?
- [ ] Yes, apply as-is
- [ ] Apply with modifications
- [ ] Skip this edit

---

{Additional suggestions for intro, features, CTA...}
```

## Summary

The **Mad Men Copywriter** skill is your conversion optimization weapon. Use it when immediate action matters more than gentle persuasion. It suggests aggressive, results-driven copy changes while preserving technical accuracy and user control.

**Remember**: Mad Men suggests, you decide. Not every piece of content needs maximum conversion focus. Use strategically on sales pages, CTAs, and marketing content where driving action is the primary goal.
