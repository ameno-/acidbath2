---
name: master-copywriter
description: Persuasion-focused copywriting that builds credibility and trust. Use for thought leadership, long-form content, brand building, and content where trust and authority matter more than immediate conversion. Uses suggest_edits pattern.
allowed-tools: Read
---

# Master Copywriter Skill

## Overview

The **Master Copywriter** skill transforms generic copy into persuasive, credibility-driven content that builds trust and authority. Based on persuasion psychology principles (especially Cialdini's influence principles), this skill suggests edits that:

- **Establish authority** before making claims
- **Use social proof** strategically
- **Tell stories** that illustrate benefits
- **Build credibility** through specificity and evidence
- **Persuade through trust** rather than urgency

**Pattern**: This skill uses the `suggest_edits` framework - it **suggests** changes with clear rationale, never auto-applies.

## Quick Reference Checklist

Use this skill when you need to persuade through credibility. Check that your suggestions cover:

### Authority Signals
- [ ] Credentials, expertise, or research cited?
- [ ] Expert opinions or authoritative sources referenced?
- [ ] Depth of knowledge demonstrated?

### Social Proof
- [ ] Testimonials or customer success stories present?
- [ ] Adoption stats or company logos mentioned?
- [ ] Specific names and numbers (not "many companies")?

### Storytelling
- [ ] Narrative used to illustrate key points?
- [ ] Before/after transformations shown?
- [ ] Customer journey or case study integrated?

### Evidence & Proof
- [ ] Claims backed with data or research?
- [ ] Specific numbers replace vague promises?
- [ ] Proof accessible (links to case studies, whitepapers)?

### Persuasion Psychology
- [ ] Reciprocity (value-first) present?
- [ ] Commitment & consistency applied?
- [ ] Authority and credibility established?

### Professional Tone
- [ ] Authoritative yet approachable?
- [ ] Professional but not corporate-speak?
- [ ] Confident without arrogance?

### Technical Preservation
- [ ] Code examples untouched?
- [ ] Benchmarks and data preserved?
- [ ] Technical accuracy maintained?

## When to Use Master Copywriter

### ✅ Perfect For

**Thought Leadership**
- CEO blog posts and vision pieces
- Industry trend analysis and predictions
- Expert opinion and commentary
- Establish yourself as authority in field

**Educational Content with Persuasion**
- Long-form guides that lead to product consideration
- Whitepapers that establish expertise
- In-depth case studies
- Tutorials that showcase capability and value

**Brand Building**
- About pages that build trust
- Company mission and values
- Team introductions that establish credibility
- Origin stories that create connection

**High-Trust Sales**
- Enterprise B2B sales materials
- High-ticket products ($1,000+)
- Professional services selling
- Long sales cycle content

**Authority Establishment**
- Expert positioning content
- Credential and experience highlighting
- Research and methodology presentation
- Differentiating through expertise

### ❌ Not Suitable For

**Quick Conversion Pages**
- Immediate "buy now" CTAs
- Low-ticket impulse purchases
- Short-form ads needing urgency
- Use **Mad Men Copywriter** instead

**Pure Technical Documentation**
- API docs, configuration guides
- Code examples and troubleshooting
- Developer documentation
- Technical accuracy > persuasion

**Simple Educational Content**
- How-to guides without product tie-in
- Explainers focused purely on teaching
- Academic or formal writing
- Use **Ameno Voice** for technical simplification

## Suggest_Edits Implementation

### Process Overview

When invoked, the Master Copywriter skill:

1. **Reads the content** using the Read tool
2. **Classifies sections** by type and persuasion opportunity
3. **Identifies credibility gaps** (missing proof, weak authority, unsupported claims)
4. **Generates edit suggestions** emphasizing trust-building
5. **Outputs suggestions** in standard suggest_edits format
6. **Never modifies files** - suggestions only

### Section Type Focus

| Section Type | Priority | Transformation Focus |
|--------------|----------|---------------------|
| `introduction` | **High** | Generic hooks → Authority-establishing openings |
| `concept-explanation` | **High** | Claims → Story-backed benefits |
| `takeaway` | **Medium** | Weak closes → Value-reinforcing conclusions |
| `cta` | **Medium** | Generic actions → Trust-aligned invitations |
| `failure-mode` | **Low** | Add credibility to warnings |
| `technical` | **Preserve** | Rarely edit - accuracy critical |
| `navigation` | **Preserve** | Keep direct and functional |

### Transformation Guidelines

#### Introduction Sections
**Look for**: Generic statements, unsupported claims, missing credibility

**Transform to**: Authority-backed openings with social proof or research

**Example**:
- ❌ "Project management is important for teams"
- ✅ "We studied 500 distributed teams to understand why 70% miss deadlines. The problem wasn't tools—it was context. Here's what the research revealed..."

#### Concept Explanation Sections
**Look for**: Feature lists, unsupported promises, missing proof

**Transform to**: Story-driven benefits with social proof

**Example**:
- ❌ "Our platform provides real-time analytics"
- ✅ "When Stripe needed to monitor 50M transactions/day, standard analytics weren't enough. They needed instant anomaly detection. Here's the real-time system we built for them..."

#### Takeaway Sections
**Look for**: Weak summaries, generic conclusions, no value reinforcement

**Transform to**: Authority-reinforcing closes with social proof

**Example**:
- ❌ "Try our platform to improve your workflow"
- ✅ "1,247 engineering teams chose us for mission-critical infrastructure. They trust us because downtime costs millions. If reliability matters to you like it matters to them, see our 99.99% uptime guarantee."

## Output Format

Standard suggest_edits format with Master Copywriter focus:

```markdown
# Edit Suggestions for {Content Title}

Generated by: Master Copywriter
Date: {YYYY-MM-DD}

---

## Summary

**Total Suggestions**: {N}
**Editable Sections Found**: {N}
**Sections Preserved**: {N}

**Focus Areas**:
- {Primary credibility improvement 1}
- {Primary persuasion improvement 2}
- {Primary authority-building improvement 3}

---

## Suggested Edit {N}: {Section Name}

**Type**: {section-type}
**Rationale**: {Persuasion principle + credibility mechanism + psychological impact}

### Before
```
{exact original content}
```

### After
```
{Master Copywriter transformation}
```

### Apply This Edit?
- [ ] Yes, apply as-is
- [ ] Apply with modifications
- [ ] Skip this edit
```

### Rationale Requirements

Every suggestion must specify:

1. **Persuasion principle used** (Cialdini, storytelling, etc.)
2. **How credibility is enhanced** (authority signal, social proof, data)
3. **Psychological mechanism** (why reader will find it more convincing)

**Bad rationale**: "Sounds more professional"
**Good rationale**: "Applies social proof principle by citing specific companies (Stripe, 1,247 users) and quantified results (99.99% uptime). Builds credibility through specificity rather than vague claims, leveraging reader's trust in known brands."

### Suggestion Limits

Focus on **credibility-building high-impact changes**:

- **Typical range**: 6-10 suggestions per document
- **Priority**: Authority > Social Proof > Story > Evidence
- **Quality over quantity**: Better 6 trust-building edits than 15 marginal tweaks

## Related Resources

- **[VOICE_DNA.md](./VOICE_DNA.md)** - Complete Master Copywriter voice characteristics
- **[EXAMPLES.md](./EXAMPLES.md)** - Before/after transformations
- **[FRAMEWORKS.md](./FRAMEWORKS.md)** - Persuasion frameworks (Cialdini, StoryBrand, etc.)
- **[ai_docs/suggest-edits-framework.md](../../ai_docs/suggest-edits-framework.md)** - Core framework documentation
- **[ai_docs/copywriting-skills.md](../../ai_docs/copywriting-skills.md)** - Comparison of all copywriting skills

## Summary

The **Master Copywriter** skill persuades through credibility, not pressure. Use it when trust-building and authority matter more than immediate conversion. It suggests sophisticated, evidence-backed copy changes while preserving technical accuracy and user control.

**Remember**: Master builds belief, Mad Men drives action. Choose based on whether your goal is long-term trust or short-term conversion.
