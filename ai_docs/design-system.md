# ACIDBATH Design System

## Overview

The ACIDBATH design system establishes a comprehensive visual language for technical blog content, prioritizing scannability, readability, and semantic clarity. Built on fluid typography, acid-green theming, and modular spacing, it transforms dense technical articles into layered, navigable content for senior engineers.

## Design Principles

1. **Scannability First**: Visual hierarchy enables rapid information triage
2. **Semantic Clarity**: Color coding communicates content type instantly
3. **Responsive Typography**: Fluid scaling maintains readability across devices
4. **Layered Information**: Collapsible sections reduce cognitive overload
5. **Practitioner Aesthetic**: Monospace-first, terminal-inspired design

## Typography

### Font Families

```css
--font-family-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-family-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
```

**Primary**: JetBrains Mono for body text (preserves ACIDBATH monospace heritage)
**Secondary**: Inter for UI components and long-form prose sections

### Fluid Typography Scale

Uses `clamp()` for responsive scaling without media queries:

| Token | Min Size | Preferred | Max Size | Use Case |
|-------|----------|-----------|----------|----------|
| `--text-xs` | 0.75rem | 0.7rem + 0.25vw | 0.875rem | Metadata, timestamps |
| `--text-sm` | 0.875rem | 0.8rem + 0.375vw | 1rem | Captions, labels |
| `--text-base` | 1rem | 0.95rem + 0.25vw | 1.125rem | Body text |
| `--text-lg` | 1.125rem | 1rem + 0.625vw | 1.5rem | Subheadings |
| `--text-xl` | 1.25rem | 1.1rem + 0.75vw | 1.875rem | H3 headings |
| `--text-2xl` | 1.5rem | 1.3rem + 1vw | 2.25rem | H2 headings |
| `--text-3xl` | 1.875rem | 1.6rem + 1.375vw | 3rem | H1 headings |
| `--text-4xl` | 2.25rem | 1.9rem + 1.75vw | 3.5rem | Hero text |

**Viewport Range**: 320px (mobile) → 1440px (desktop)

## Color Palette

### Backgrounds

```css
--color-background: #0a0a0a;        /* Primary background */
--color-background-alt: #1a1a1a;    /* Secondary surfaces */
--color-background-hover: #252525;  /* Interactive hover states */
--color-background-code: #111111;   /* Code block backgrounds */
```

### Foreground

```css
--color-foreground: #ffffff;        /* Primary text */
--color-foreground-alt: #888888;    /* Secondary text */
--color-foreground-muted: #666666;  /* Disabled/muted text */
```

### Accent (Acid Green)

```css
--color-accent-primary: #39ff14;    /* Primary brand color */
--color-accent-secondary: #2ee60f;  /* Hover/active states */
--color-accent-muted: #1a8008;      /* Subtle accents */
```

**Contrast Ratio**: 12.3:1 against `#0a0a0a` (WCAG AAA)

### Semantic Colors

| Type | Foreground | Background | Use Case |
|------|------------|------------|----------|
| Note | `#6b7280` | `rgba(107, 114, 128, 0.1)` | Supplementary info |
| Tip | `#39ff14` | `rgba(57, 255, 20, 0.1)` | Helpful suggestions |
| Info | `#2196f3` | `rgba(33, 150, 243, 0.1)` | Reference material |
| Warning | `#ff9800` | `rgba(255, 152, 0, 0.1)` | Cautions, gotchas |
| Danger | `#f44336` | `rgba(244, 67, 54, 0.1)` | Errors, critical warnings |
| Quote | `#888888` | `rgba(136, 136, 136, 0.1)` | Testimonials, citations |

## Spacing

### Modular Scale

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

**Base Unit**: 0.25rem (4px) for 8px grid alignment

## Components

### CodeBlock (Expressive Code)

Code presentation powered by Astro Expressive Code integration. Features automatic collapsing, syntax highlighting, and copy functionality.

**Expressive Code Features**:
- Automatic syntax highlighting for 100+ languages
- Copy-to-clipboard button
- Line highlighting with `{1,3-5}` syntax
- File tabs with `// filename.js` comments
- Diff highlighting with `+`/`-` prefixes
- Collapsible sections with `collapse={lines}` meta-string

**Collapse Meta-String**:
```markdown
```python collapse={12-50}
# Lines 1-11 visible
# Lines 12-50 collapsed by default
```
```

**Auto-collapse Behavior**: Blocks >15 lines auto-collapse

**Line Highlighting**:
```markdown
```typescript {2,5-7}
// Line 2 and lines 5-7 will be highlighted
```
```

**File Tabs**:
```markdown
```typescript
// src/utils/helpers.ts
export function helper() {}
```
```

**Visual Features**:
- Acid-green syntax theme matching ACIDBATH aesthetic
- JetBrains Mono font (85-90% of body size)
- Copy button with "Copied!" feedback
- Expand/collapse toggle for long blocks
- Line numbers (optional)

### Callout

Semantic callouts for emphasizing content by type.

**Props Interface**:
```typescript
interface Props {
  type: 'note' | 'tip' | 'info' | 'warning' | 'danger' | 'quote';
  title?: string;
  author?: string; // Quote variant only
}
```

**Variant Guide (6 Semantic Variants)**:

| Type | Border Color | Icon | When to Use |
|------|--------------|------|-------------|
| `note` | `#6b7280` | 📝 | Supplementary information |
| `tip` | `#39ff14` | 💡 | Helpful suggestions, pro tips |
| `info` | `#2196f3` | ℹ️ | Reference material, links |
| `warning` | `#ff9800` | ⚠️ | Gotchas, edge cases |
| `danger` | `#f44336` | ⛔ | Critical failures, errors |
| `quote` | `#888888` | " | Testimonials, external quotes |

**Deprecated Variants** (migrate to new types):
- `success` → Use `tip` or `note`
- `insight` → Use `tip` or `note`
- `data` → Use `info` or `note`

**Usage**:
```astro
<Callout type="warning" title="Performance Gotcha">
This approach causes N+1 queries at scale.
</Callout>

<Callout type="quote" author="Ameno">
Production is the only real testing environment.
</Callout>
```

**Visual Treatment**:
- Quote: Oversized opening quote, italic text, 2px left border
- Insight: Gradient background, featured treatment, 4px left border
- Others: Semi-transparent background, 2px left border, variant-specific icon

### Collapse

Collapsible sections for supplementary content.

**Props Interface**:
```typescript
interface Props {
  title: string;
  preview?: string;
  variant?: 'default' | 'compact' | 'prominent'; // Default: 'default'
  defaultOpen?: boolean; // Default: false
}
```

**Variants**:
- **Default**: Neutral styling, standard padding
- **Compact**: Reduced padding for inline usage
- **Prominent**: Acid-green accent, featured treatment

**Usage**:
```astro
<Collapse title="Deep Dive: Algorithm Analysis" variant="prominent">
  <CodeBlock code={complexAlgorithm} language="python" />
  <p>Detailed explanation...</p>
</Collapse>
```

**Visual Features**:
- Animated chevron (90° rotation on expand)
- Preview text in collapsed state
- Hover background transition
- Nested CodeBlock margin handling

### TableOfContents

Hierarchical navigation with scroll progress and active tracking.

**Props Interface**:
```typescript
interface Props {
  headings: Array<{
    depth: number;
    slug: string;
    text: string;
  }>;
  maxTopLevel?: number; // Default: 8
}
```

**Features**:
- **Hierarchical Grouping**: H2 sections with collapsible H3 subsections
- **Scroll Progress**: Dynamic width bar based on reading position
- **Active Tracking**: Auto-expands parent when child is active
- **Show More**: Hides sections beyond `maxTopLevel` threshold
- **Smooth Scroll**: History state management for browser back/forward

**Usage**:
```astro
<TableOfContents headings={headings} maxTopLevel={10} />
```

**Visual Indicators**:
- Acid-green highlight for active section
- Section count in header (e.g., "8 sections")
- Progress bar updates on scroll
- Sticky positioning for persistent access

## Design System Alignment with ACIDBATH Tenets

### 1. POC Rule
All components provide copy-paste examples that work immediately. No theoretical concepts without implementation.

### 2. Numbers Test
Specific measurements throughout:
- 15-line collapse threshold (not "long code")
- 8-line preview window (not "brief excerpt")
- 60fps animation target (not "smooth")
- 4.5:1 color contrast minimum (not "readable")

### 3. Production Lens
Edge cases documented:
- CodeBlock syntax highlighting requires `language` prop
- Collapse component uses `<details>` (limited IE support)
- Fluid typography requires modern CSS (Chrome 90+, Firefox 88+, Safari 14+)

### 4. Senior Engineer Filter
Sophisticated features for experienced developers:
- Scroll spy with intersection observer
- CSS Grid for complex layouts
- TypeScript interfaces for type safety
- Performance considerations (font loading, animation)

### 5. Honest Failure Requirement
Component limitations acknowledged:
- No server-side syntax highlighting (client-side only)
- Nested Collapse components have depth limitations
- TableOfContents requires JavaScript for scroll spy

### 6. Try It Now
All examples are copy-paste ready with realistic data.

## Browser Compatibility

**Minimum Versions**:
- Chrome 90+ (clamp() support)
- Firefox 88+ (clamp() support)
- Safari 14+ (clamp() support)
- Edge 90+ (Chromium-based)

**Fallback Strategy**:
- Native `<details>` element (progressive enhancement)
- CSS Grid with flexbox fallback (automatic)
- Intersection Observer polyfill not required (graceful degradation)

## Performance Guidelines

### Font Loading (Fontsource)

Fonts are loaded via Fontsource npm packages (self-hosted, bundled automatically):

```typescript
// In BaseLayout.astro or similar
import '@fontsource-variable/inter';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/500.css';
```

**Benefits over CDN**:
- Zero external network requests
- Bundled with site assets
- Better Core Web Vitals (no extra DNS lookup)
- Works offline

**Strategy**: `font-display: swap` configured in Fontsource prevents FOIT (Flash of Invisible Text)

### Animation
- Use CSS `transform` (GPU-accelerated) over `left`/`top`
- Target 60fps for all transitions
- Prefer `transition` over `animation` for simple state changes

### Bundle Size
- Design system CSS: ~8KB gzipped
- No JavaScript dependencies for base components
- Astro islands for interactive features (lazy-loaded)

## Migration Guide

For existing ACIDBATH posts:

### Automatic Improvements
- Typography and color tokens apply globally via CSS cascade
- Enhanced link hover states (acid-green)
- Improved code block backgrounds

### Manual Enhancements
1. **Add Callouts**: Wrap key points in semantic callouts
   ```astro
   <Callout type="insight">
   This reduced query time from 2.3s to 47ms in production.
   </Callout>
   ```

2. **Collapse Long Code**: Wrap >15 line examples
   ```astro
   <CodeBlock code={longExample} language="python" />
   ```

3. **Use Collapse for Appendices**:
   ```astro
   <Collapse title="Full Benchmark Results">
   [Detailed tables...]
   </Collapse>
   ```

### No Changes Required
- TableOfContents (auto-generated from headings)
- Typography scaling (fluid by default)
- Color scheme (updated via CSS variables)

## Future Enhancements

**Planned**:
- Search integration (Pagefind styling)
- Print styles (PDF export optimization)
- Chart components (metrics visualization)
- Timeline component (project narratives)

**Under Consideration**:
- Color scheme variants (electric blue, sunset orange)
- Syntax theme customization
- Component animation preferences
- Accessibility preference detection (prefers-reduced-motion)

## Dependencies

**Core Packages**:
- Astro (component framework)
- Tailwind v4 (styling foundation)
- TypeScript (type safety)
- Playwright (testing)
- astro-expressive-code (code blocks)
- @fontsource-variable/inter (body font)
- @fontsource/jetbrains-mono (code font)

## Maintenance

### Updating Design Tokens
Modify `/src/styles/global.css` `@theme` block. All components reference CSS variables.

### Adding Semantic Colors
1. Define in `@theme` (foreground + background variant)
2. Add Callout variant in `/src/components/Callout.astro`
3. Document in this file

### Component Versioning
Breaking changes require:
- TypeScript interface updates
- Documentation updates
- Migration guide additions
- Test suite updates

## Support

**Documentation**: This file + README.md Design System section
**Examples**: `/src/content/blog/design-system-showcase.md`
**Tests**: `/tests/design-system.spec.ts` + `/tests/design-system-visual.spec.ts`
