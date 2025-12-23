# Feature: ACIDBATH Design System Integration

## Metadata
adw_id: `be401aa9`
prompt: `Review uploaded zip for complete design system and components to improve. Plan and implement all your work in parallel. Integrate the tenants of this design system into ACIDBATH and the content strategy. Migrate and integrate css and style changes. Write test to verify improvements. Create required new components and replace existing implementations with new components.`

## Feature Description
This feature integrates a comprehensive design system into ACIDBATH featuring acid-green theming, enhanced typography, and four key UI components (CodeBlock, Callout, Collapse, TableOfContents). The design system prioritizes readability through fluid typography scaling, semantic color coding, collapsible content sections, and interactive navigation. This transforms dense technical articles into layered, scannable content while maintaining the blog's practitioner-focused aesthetic.

The integration updates global CSS with design tokens, replaces existing components with enhanced versions, creates two new components (Callout and Collapse), and ensures all changes align with ACIDBATH's editorial philosophy.

## User Story
As a **senior engineer reading ACIDBATH posts**
I want to **easily scan long-form technical content with clear visual hierarchy**
So that **I can quickly navigate to relevant sections and understand code examples without overwhelming walls of text**

## Problem Statement
Current ACIDBATH posts suffer from:
1. **Dense code blocks** with no collapsing for lengthy examples, forcing excessive scrolling
2. **Flat visual hierarchy** lacking semantic callouts for warnings, insights, or key takeaways
3. **Limited content organization** without collapsible sections for supplementary material
4. **Basic table of contents** without hierarchical grouping or scroll progress indicators
5. **Inconsistent typography scaling** across devices without fluid responsive design
6. **Limited semantic color usage** beyond basic accent colors

These issues reduce scannability and increase cognitive load for senior engineers seeking specific information.

## Solution Statement
Implement the ACIDBATH design system through:

1. **Enhanced global CSS**: Fluid typography with `clamp()` functions, expanded design tokens (8 font sizes, modular spacing, semantic colors), and acid-green theming (`#39ff14`)

2. **Upgraded CodeBlock component**: Auto-collapse for blocks >15 lines, line numbers, syntax highlighting with acid-green theme, copy-to-clipboard, filename/language badges, and fade gradient for collapsed state

3. **New Callout component**: Seven semantic types (quote, info, warning, danger, success, insight, data) with distinct icons, colored borders, and visual hierarchy

4. **New Collapse component**: Collapsible sections with three variants (default, compact, prominent), animated chevron, and preview text support

5. **Enhanced TableOfContents**: Hierarchical H2/H3 grouping, scroll progress indicator, active section tracking with auto-expansion, "show more" functionality, and sticky positioning

6. **Comprehensive testing**: Playwright tests verifying component functionality, visual regression, accessibility, and responsive behavior

## Relevant Files

### Existing Files to Modify

- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/styles/global.css`** - Replace with design system CSS tokens, fluid typography, and semantic color scheme
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/CodeBlock.astro`** - Enhance with collapsibility, line numbers, syntax highlighting, and design system styling
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/TableOfContents.astro`** - Upgrade with hierarchical grouping, scroll progress, and expanded/collapsed states
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/layouts/BlogPostLayout.astro`** - Update to integrate new components and design system styles
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/layouts/BaseLayout.astro`** - Add design system font imports (Inter, JetBrains Mono)
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/README.md`** - Document design system integration and component usage

### New Files

- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/Callout.astro`** - Seven-variant semantic callout component
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/Collapse.astro`** - Collapsible section component with variants
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/tests/design-system.spec.ts`** - Component functionality tests
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/tests/design-system-visual.spec.ts`** - Visual regression tests
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/ai_docs/design-system.md`** - Design system reference documentation
- **`/Users/ameno/dev/acidbath2/trees/be401aa9/src/content/blog/design-system-showcase.md`** - Example post demonstrating all components

## Implementation Plan

### Phase 1: Foundation
Establish design system CSS foundation with typography, color tokens, and spacing scales. This creates the visual language that all components depend on.

### Phase 2: Core Implementation
Build and enhance all four components in parallel using the design system foundation. Each component is independent and can be developed concurrently.

### Phase 3: Integration & Testing
Integrate components into blog layouts, create showcase content, write comprehensive tests, and validate the implementation meets ACIDBATH editorial standards.

## Step by Step Tasks

### Group A: Design System Foundation [parallel: false, model: sonnet]
Sequential setup establishing CSS foundation and documentation that other groups depend on.

#### Step A.1: Update Global CSS with Design System
- Replace `/Users/ameno/dev/acidbath2/trees/be401aa9/src/styles/global.css` with design system tokens
- Implement fluid typography using `clamp()` for responsive scaling (8 sizes: xs to 4xl)
- Add modular spacing scale (--space-1 through --space-16)
- Define semantic color palette (accent: #39ff14, backgrounds: #0a0a0a to #1a1a1a, semantic: warning/info/success/danger)
- Configure border radius tokens (4px to full rounded)
- Set transition speeds (fast: 0.1s, base: 0.15s, slow: 0.3s)
- Preserve existing Tailwind v4 integration and monospace typography

#### Step A.2: Update BaseLayout with Font Imports
- Modify `/Users/ameno/dev/acidbath2/trees/be401aa9/src/layouts/BaseLayout.astro`
- Add Google Fonts imports for Inter and JetBrains Mono
- Configure font-display: swap for performance
- Update font-family CSS variables to reference new fonts

#### Step A.3: Create Design System Documentation
- Write `/Users/ameno/dev/acidbath2/trees/be401aa9/ai_docs/design-system.md`
- Document color tokens, typography scale, spacing system
- Include component usage examples and props interfaces
- Define when to use each callout variant
- Add guidelines for collapsible content organization
- Document design system alignment with ACIDBATH editorial tenets

### Group B: Component Development [parallel: true, depends: A, model: auto]
Independent component builds that can execute concurrently after foundation is ready.

#### Step B.1: Create Callout Component
- Create `/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/Callout.astro`
- Implement seven semantic variants: quote, info, warning, danger, success, insight, data
- Add variant-specific icons, colored left borders (2-4px), and semi-transparent backgrounds
- Style quote variant with oversized opening quote and italic text
- Configure insight variant with gradient background and featured treatment
- Support title prop override and author prop for quotes
- Use design system color tokens and spacing
- Add TypeScript interface for props (type: required, title: optional, author: optional)

#### Step B.2: Create Collapse Component
- Create `/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/Collapse.astro`
- Build using native HTML `<details>` element with custom styling
- Implement three variants: default (neutral), compact (reduced padding), prominent (acid green accent)
- Add animated chevron rotation (90° on expand)
- Support title (required), preview text (optional), defaultOpen (optional) props
- Add hover states with background transitions
- Style expandable/collapse text hints
- Configure nested CodeBlock margin handling
- Use design system tokens for colors, spacing, transitions

#### Step B.3: Enhance CodeBlock Component
- Modify `/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/CodeBlock.astro`
- Add collapsible functionality with auto-trigger for >15 lines
- Implement line numbers with toggle support
- Create language badge display in header
- Add filename prop and header display
- Build fade gradient overlay for collapsed state (8-line preview)
- Support highlightLines prop for marking important lines
- Enhance copy-to-clipboard with improved feedback
- Configure maxPreviewLines prop (default: 8)
- Add defaultExpanded prop for initial state control
- Style with acid-green syntax theme (keywords: #39ff14, strings: warm orange, comments: muted green)
- Preserve existing copy button functionality

#### Step B.4: Enhance TableOfContents Component
- Modify `/Users/ameno/dev/acidbath2/trees/be401aa9/src/components/TableOfContents.astro`
- Implement hierarchical H2/H3 grouping using collapsible `<details>` elements
- Add scroll progress bar (dynamic width based on reading position)
- Display section count in header (e.g., "8 sections")
- Build "show more" functionality with maxTopLevel prop (default: 8)
- Enhance active section highlighting with parent auto-expansion
- Improve scroll spy with better viewport detection
- Add smooth scroll behavior with history state management
- Style with acid-green active indicators and hover states
- Maintain existing sticky positioning and accessibility features

### Group C: Layout Integration [parallel: false, depends: B, model: sonnet]
Sequential integration work incorporating all components into blog infrastructure.

#### Step C.1: Update BlogPostLayout Integration
- Modify `/Users/ameno/dev/acidbath2/trees/be401aa9/src/layouts/BlogPostLayout.astro`
- Import new Callout and Collapse components
- Update component import paths
- Verify TableOfContents and CodeBlock integration with enhanced versions
- Ensure grid layout accommodates new component widths
- Test responsive behavior with all components
- Validate design system CSS applies globally

#### Step C.2: Create Design System Showcase Post
- Write `/Users/ameno/dev/acidbath2/trees/be401aa9/src/content/blog/design-system-showcase.md`
- Demonstrate all seven Callout variants with real content
- Include collapsible CodeBlock examples (short and long)
- Show all three Collapse variants with nested content
- Display enhanced TableOfContents with hierarchical sections
- Use realistic ACIDBATH-style technical content
- Add metadata matching ACIDBATH post structure
- Include TLDR and Key Takeaways sections

#### Step C.3: Update README with Design System Documentation
- Modify `/Users/ameno/dev/acidbath2/trees/be401aa9/README.md`
- Add "Design System" section describing integration
- Document component usage with code examples
- Link to ai_docs/design-system.md for detailed reference
- Update "Project Structure" to include design system components
- Add component props reference table

### Group D: Testing & Validation [parallel: true, depends: C, model: auto]
Comprehensive test suites validating component functionality and visual quality.

#### Step D.1: Create Component Functionality Tests
- Write `/Users/ameno/dev/acidbath2/trees/be401aa9/tests/design-system.spec.ts`
- Test CodeBlock collapsibility (auto and manual)
- Verify copy-to-clipboard functionality
- Test Callout rendering for all seven variants
- Validate Collapse expand/collapse interaction
- Test TableOfContents hierarchical grouping and scroll spy
- Verify "show more" functionality in TOC
- Test component props handling (required and optional)
- Validate accessibility (ARIA labels, keyboard navigation)

#### Step D.2: Create Visual Regression Tests
- Write `/Users/ameno/dev/acidbath2/trees/be401aa9/tests/design-system-visual.spec.ts`
- Capture screenshots of all Callout variants
- Test CodeBlock in collapsed and expanded states
- Verify Collapse component variants visually
- Test responsive behavior at mobile, tablet, desktop widths
- Validate color contrast ratios meet WCAG AA standards
- Test dark mode consistency across components
- Verify acid-green accent consistency

#### Step D.3: Integration Testing with Real Content
- Test design-system-showcase.md post rendering
- Verify all components render correctly in blog context
- Test component interaction (nested components)
- Validate performance (no layout shifts, smooth animations)
- Test Mermaid diagram compatibility with new CSS
- Verify existing posts still render correctly
- Test build process (npm run build succeeds)

### Group E: Documentation & Quality Assurance [parallel: false, depends: D, model: opus]
Final validation ensuring implementation meets ACIDBATH editorial standards.

#### Step E.1: Editorial Quality Check
- Review design-system-showcase.md against ACIDBATH tenets
- Verify POC Rule: all components have working examples
- Check Numbers Test: specific measurements documented
- Validate Production Lens: edge cases and limitations documented
- Ensure Senior Engineer Filter: content valuable for experienced developers
- Confirm Honest Failure Requirement: component limitations documented
- Add "Try It Now" section with actionable next steps

#### Step E.2: Performance Validation
- Run Playwright performance tests
- Verify no increase in bundle size >10%
- Test Core Web Vitals (LCP, CLS, FID) meet targets
- Validate font loading doesn't block render
- Test animation performance (60fps)
- Check accessibility audit scores

#### Step E.3: Final Integration Validation
- Build project: `npm run build`
- Preview production build: `npm run preview`
- Run full test suite: `npm run test`
- Verify all tests pass
- Test on mobile Safari, Chrome, Firefox
- Validate responsive design at 320px, 768px, 1024px, 1440px
- Check console for errors or warnings
- Verify llms.txt generation includes new content

## Testing Strategy

### Unit Tests
1. **CodeBlock Component**:
   - Auto-collapse triggers at 15 lines
   - Line numbers display correctly
   - Copy button copies code to clipboard
   - Collapse/expand animation works smoothly
   - Language badge renders for supported languages
   - Filename displays when provided

2. **Callout Component**:
   - All seven variants render with correct styling
   - Icons display for each variant
   - Title override works
   - Author attribution renders for quote variant
   - Nested content (code, links) renders correctly

3. **Collapse Component**:
   - All three variants render correctly
   - Chevron animates on expand/collapse
   - defaultOpen prop controls initial state
   - Preview text displays when provided
   - Nested components render properly

4. **TableOfContents Component**:
   - H2/H3 hierarchical grouping works
   - Scroll progress bar updates on scroll
   - Active section highlighting accurate
   - "Show more" hides extra sections
   - Smooth scroll navigation works
   - Parent expands when child is active

### Integration Tests
1. All components render in BlogPostLayout
2. Design system CSS applies globally
3. Components work together (nested usage)
4. Responsive behavior at breakpoints (320px, 768px, 1024px, 1440px)
5. Mermaid diagrams compatible with new styles
6. Existing posts render without errors
7. Build process completes successfully

### Edge Cases
1. **CodeBlock**:
   - Empty code block
   - Single-line code (no collapse)
   - Code with 15 lines exactly (boundary)
   - Very long lines (horizontal scroll)
   - Special characters in code (escaping)
   - Code without language specified

2. **Callout**:
   - Quote without author
   - Callout with long title
   - Nested callouts
   - Callout with only whitespace content

3. **Collapse**:
   - Collapse with no content
   - Deeply nested collapses
   - Collapse containing large images
   - Multiple collapses in sequence

4. **TableOfContents**:
   - Post with only H2s (no H3s)
   - Post with only H3s (no H2s)
   - Post with >20 sections
   - Sections with special characters in slugs
   - Empty heading text

### Accessibility Tests
1. ARIA labels on interactive elements
2. Keyboard navigation (tab, enter, space)
3. Focus indicators visible
4. Color contrast ratios ≥4.5:1 (WCAG AA)
5. Screen reader compatibility
6. Semantic HTML structure
7. Skip links for navigation

### Performance Tests
1. Bundle size increase <10%
2. LCP (Largest Contentful Paint) <2.5s
3. CLS (Cumulative Layout Shift) <0.1
4. FID (First Input Delay) <100ms
5. Font loading strategy (font-display: swap)
6. Animation frame rate ≥60fps
7. No blocking resources

## Acceptance Criteria

1. **Design System Integration**:
   - [ ] Global CSS replaced with design system tokens
   - [ ] Fluid typography scales from 0.75rem to 3.5rem
   - [ ] Acid-green color scheme (#39ff14) consistently applied
   - [ ] Modular spacing scale implemented
   - [ ] Semantic colors defined and used

2. **Component Implementation**:
   - [ ] Callout component supports all 7 variants
   - [ ] Collapse component has 3 variants working
   - [ ] CodeBlock auto-collapses for >15 lines
   - [ ] TableOfContents groups H2/H3 hierarchically
   - [ ] All components use design system tokens

3. **Visual Quality**:
   - [ ] Typography readable across all devices
   - [ ] Color contrast meets WCAG AA standards
   - [ ] Components visually consistent with ACIDBATH brand
   - [ ] Animations smooth at 60fps
   - [ ] Responsive behavior at all breakpoints

4. **Functionality**:
   - [ ] All interactive features work (collapse, copy, scroll spy)
   - [ ] Keyboard navigation functional
   - [ ] Screen reader accessible
   - [ ] No console errors or warnings
   - [ ] Existing posts render without issues

5. **Testing**:
   - [ ] All Playwright tests pass
   - [ ] Visual regression tests baseline captured
   - [ ] Accessibility audit scores ≥95
   - [ ] Performance tests meet targets
   - [ ] Integration tests validate component interaction

6. **Documentation**:
   - [ ] ai_docs/design-system.md complete
   - [ ] README.md updated with design system section
   - [ ] Showcase post demonstrates all components
   - [ ] Component props documented with TypeScript interfaces
   - [ ] Usage examples provided

7. **Editorial Standards**:
   - [ ] Showcase post passes all 6 ACIDBATH tenets
   - [ ] Design system enhances scannability
   - [ ] Components support senior engineer workflow
   - [ ] No reduction in content quality or depth

## Validation Commands

Execute these commands to validate the feature is complete:

**Build & Preview**:
```bash
# Build the project (includes llms.txt generation)
npm run build

# Preview production build
npm run preview
```

**Run Tests**:
```bash
# Run all Playwright tests
npm run test

# Run design system specific tests
npx playwright test design-system

# Run visual regression tests
npx playwright test design-system-visual

# Generate test report
npm run test:report
```

**Component Validation**:
```bash
# Verify CodeBlock component exists and is valid
cat src/components/CodeBlock.astro | grep -A 5 "collapsible"

# Verify Callout component exists
test -f src/components/Callout.astro && echo "Callout component exists"

# Verify Collapse component exists
test -f src/components/Collapse.astro && echo "Collapse component exists"

# Verify TableOfContents enhancements
cat src/components/TableOfContents.astro | grep -A 3 "hierarchical"
```

**CSS Validation**:
```bash
# Check design system tokens exist
grep -E "(--accent-primary|--text-xs|--space-1)" src/styles/global.css

# Verify fluid typography
grep "clamp(" src/styles/global.css | wc -l
```

**Content Validation**:
```bash
# Verify showcase post exists
test -f src/content/blog/design-system-showcase.md && echo "Showcase post exists"

# Verify documentation exists
test -f ai_docs/design-system.md && echo "Design system docs exist"

# Check README updated
grep -i "design system" README.md
```

**Accessibility Validation**:
```bash
# Run accessibility-focused tests
npx playwright test --grep "accessibility"

# Check ARIA labels in components
grep -r "aria-label" src/components/
```

**Performance Validation**:
```bash
# Run performance tests
npm run test:perf

# Check bundle size
npm run build && du -sh dist/
```

**Integration Validation**:
```bash
# Start dev server and verify no errors
npm run dev &
sleep 5
curl -s http://localhost:4321 | grep -i "error" && echo "Errors found!" || echo "No errors"
pkill -f "astro dev"
```

## Notes

### Design System Alignment with ACIDBATH Tenets

The design system enhances ACIDBATH's editorial philosophy:

1. **POC Rule**: Components provide copy-paste examples senior engineers can use immediately
2. **Numbers Test**: Specific measurements (15-line collapse threshold, 8-line preview, 60fps animations) replace vague "improvements"
3. **Production Lens**: Documentation includes edge cases, browser compatibility, and performance impact
4. **Senior Engineer Filter**: Sophisticated features (scroll spy, hierarchical TOC) serve experienced developers
5. **Honest Failure Requirement**: Component limitations documented (e.g., CodeBlock syntax highlighting requires language prop)
6. **Try It Now**: Showcase post provides actionable examples

### Browser Compatibility

- **Modern browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **CSS features**: `clamp()`, `@layer`, CSS Grid, Intersection Observer
- **Fallbacks**: Native `<details>` element, progressive enhancement for animations

### Performance Considerations

- **Font loading**: `font-display: swap` prevents FOIT (Flash of Invisible Text)
- **Code splitting**: Components lazy-loaded via Astro islands
- **Animation**: CSS transforms (GPU-accelerated) over layout properties
- **Bundle size**: Target <10% increase from design system CSS

### Future Enhancements

- **Search integration**: Pagefind styling to match design system
- **RSS feed styling**: Apply typography to feed content
- **Print styles**: Optimized layout for PDF export
- **Color scheme variants**: Electric blue (#00d4ff) or sunset orange (#ff6b35) alternatives
- **Component library expansion**: Chart components, Timeline, Progress indicators

### Dependencies

No new npm packages required. All components built using:
- **Astro**: Native component framework
- **Tailwind v4**: Existing styling infrastructure
- **TypeScript**: Type safety for props
- **Playwright**: Testing framework (already installed)

### Migration Path

For existing ACIDBATH posts:
1. Automatic: Typography and color improvements apply globally
2. Manual: Add Callout components to emphasize key points
3. Manual: Wrap long code examples in enhanced CodeBlock
4. Manual: Use Collapse for supplementary content
5. Optional: Enhanced TOC requires no changes (auto-generated)

### Content Strategy Impact

Design system supports content pipeline:
- **Blog posts**: Enhanced scannability improves engagement metrics
- **Twitter threads**: Callout components translate to visual emphasis
- **LinkedIn posts**: Design system maintains professional aesthetic
- **Newsletter**: Typography improvements enhance email readability

All derivative content generation workflows remain compatible.
