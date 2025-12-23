# Metaphor Frameworks

**WARNING: Use sparingly. Most concepts don't need metaphors.**

This library exists for genuinely complex concepts that benefit from extended metaphors developed collaboratively with the author. These are NOT quick analogies to reach for - they're frameworks developed over time and deployed consistently across related content.

---

## When to Use This Library

**Ask these questions first:**

1. Is the concept genuinely complex, or just unfamiliar?
2. Does the metaphor actually reduce cognitive load?
3. Has this metaphor been developed with the author?
4. Will this metaphor be used consistently across multiple posts?

If any answer is "no," don't use a metaphor. Simplify directly instead.

---

## Developed Frameworks

The following frameworks have been developed for specific complex concepts. They should be deployed consistently when those concepts appear.

### 1. Building a Bridge

**For**: Complex API integrations, system interconnections with multiple failure points

**When to use**: Only for multi-system integration scenarios where multiple connection points, load handling, and failure modes need explaining together.

**NOT for**: Simple API calls, single endpoints, basic request/response

| Technical Concept | Bridge Equivalent |
|-------------------|-------------------|
| API gateway | Bridge entrance checkpoint |
| Rate limiting | Load capacity |
| Retry logic | Detour routes |
| Circuit breaker | Structural safety cutoff |

### 2. Train System

**For**: Complex multi-stage pipelines with branching logic

**When to use**: Only for systems with multiple sequential stages, branching paths, and cargo that transforms as it moves through the system.

**NOT for**: Simple data flow, single-function transformations, basic I/O

| Technical Concept | Train Equivalent |
|-------------------|------------------|
| Pipeline stages | Stations |
| Data packet | Cargo car |
| Routing logic | Track switches |
| Backpressure | Track congestion |

### 3. Factory Assembly Line

**For**: Complex automation workflows with quality gates

**When to use**: Only for multi-stage automation with inspection points, parallel processing, and clear throughput bottlenecks.

**NOT for**: Simple scripts, single-step automation, basic loops

| Technical Concept | Factory Equivalent |
|-------------------|-------------------|
| Workflow stages | Work stations |
| Validation | Quality inspection |
| Parallelism | Multiple lines |
| Bottleneck | Slowest station |

---

## Frameworks NOT Yet Developed

The following are placeholder frameworks. They should NOT be used until developed collaboratively with the author for specific content needs:

- **Building a House** - For architecture/dependency discussions (needs development)
- **Power Grid** - For distribution/scaling (needs development)
- **Plumbing System** - For stream processing (needs development)

---

## How to Develop New Frameworks

When a genuinely complex concept needs a metaphor:

1. **Identify the complexity** - What makes this hard to explain directly?
2. **Propose to author** - Don't develop in isolation
3. **Map comprehensively** - Cover all aspects of the concept
4. **Test the mapping** - Does it reduce cognitive load?
5. **Define boundaries** - Where does the metaphor break down?
6. **Plan deployment** - Which posts will use this consistently?
7. **Add to this file** - Document for consistent future use

---

## Anti-Patterns

### Reaching for metaphors

**Bad**: "I need to explain context windows... let me check the metaphor library..."

This is backwards. If you're reaching for a metaphor, you probably don't need one.

### One-off analogies

**Bad**: Using "train cars" for context in one post, then "warehouse shelves" in another.

Metaphors should be consistent. If you use one, commit to it across related content.

### Decorating simple concepts

**Bad**: "Think of your context window like a cargo train with numbered cars..."

Context windows are already understandable. This adds cognitive load, not clarity.

---

## Remember

**Default: Don't use metaphors.**

This library exists for the rare cases where extended metaphors genuinely help. Most explanations are clearer without them.
