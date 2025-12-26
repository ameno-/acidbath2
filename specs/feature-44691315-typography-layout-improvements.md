# Feature: Typography and Layout Improvements

## Metadata
adw_id: `44691315`
prompt: `Review both documents and implement changes on all blog posts and pages. Make sure all pages still work. Make sure to update the content creation and review workflows to ensure they respect new typography. Update tests. Perform work in parallel as much as possible. Complete every step and deliver a fully working solution. If CI fails, fix errors and all tests pass`

## Feature Description
This feature implements comprehensive typography and layout improvements across the entire ACIDBATH blog based on two expert-level design documents. The improvements focus on: (1) upgrading the font stack to best-in-class options (JetBrains Mono + Inter/Geist), (2) implementing production-ready typography specifications optimized for dark themes, (3) enhancing code blocks with Expressive Code, (4) improving callout components with six semantic variants, (5) optimizing image handling with Astro's built-in pipeline, and (6) implementing proper layout patterns centered on the 65-character line width.

The changes will be applied to all existing blog posts, page templates, component library, content creation workflows, review processes, and test suites to ensure system-wide consistency and compliance with WCAG accessibility standards.

## User Story
As a blog reader
I want improved typography and layout that maximizes readability on dark backgrounds
So that I can efficiently scan, navigate, and consume dense technical content without eye strain

As a content creator
I want automated workflows that respect the new typography system
So that I can maintain consistent quality across all blog posts without manual intervention

As a developer
I want comprehensive tests validating the design system
So that I can confidently make changes without breaking accessibility or visual consistency

## Problem Statement
The current ACIDBATH blog has foundational design system elements but lacks:
1. **Optimal font choices** - Not using best-in-class fonts specifically designed for dark themes and technical content
2. **Dark theme optimization** - Typography specifications don't account for halation, contrast requirements, and increased letter-spacing needs
3. **Advanced code presentation** - Missing features like Expressive Code for collapsible sections, file tabs, diff notation
4. **Semantic callout variants** - Only 7 variants instead of industry-standard 6 (note, tip, info, warning, danger, quote)
5. **Image optimization** - Not leveraging Astro's full image pipeline capabilities
6. **Layout refinement** - Not implementing research-backed 65ch line width and proper two-column patterns
7. **Workflow integration** - Content creation and review workflows don't enforce new typography standards
8. **Test coverage** - Tests don't validate new typography specifications and accessibility requirements

## Solution Statement
Implement a comprehensive typography and layout upgrade that:
1. Migrates font stack to JetBrains Mono (code) + Inter (prose) with proper self-hosted loading via Fontsource
2. Applies production-ready typography specifications (18-20px body, 1.6 line-height, 60-70ch line length, WCAG AA 4.5:1 contrast)
3. Integrates Expressive Code for advanced code block features (collapsible sections, file tabs, diff highlighting)
4. Standardizes callout components to 6 semantic variants (note, tip, info, warning, danger, quote) with proper dark mode support
5. Enhances image handling using Astro's Picture component with WebP/AVIF formats
6. Implements proper layout patterns with 65ch content column and sticky sidebar TOC
7. Updates all content creation workflows (`/new-post`, `/ai-audit`, `/ameno-finalize`) to enforce typography standards
8. Expands test suite to validate typography specs, accessibility, and visual consistency

## Relevant Files

### Typography & Font Loading
- **src/styles/global.css** - Core typography tokens, font-family declarations, fluid clamp() scales, dark theme color system
- **src/layouts/BaseLayout.astro** - Font preloading, Fontsource imports, root HTML configuration
- **package.json** - Add `@fontsource-variable/inter` and `@fontsource/jetbrains-mono` dependencies

### Components
- **src/components/Callout.astro** - Refactor to 6 semantic variants with proper icons, dark mode backgrounds, WCAG contrast
- **src/components/Collapse.astro** - Update variant styling to match new typography specs
- **src/components/TableOfContents.astro** - Verify sticky positioning, scrollbar styling, 65ch alignment
- **src/components/CodeEnhancer.astro** - May be replaced/enhanced by Expressive Code integration

### Layouts
- **src/layouts/BlogPostLayout.astro** - Implement 65ch content column, two-column grid, update prose wrapper classes
- **src/layouts/BaseLayout.astro** - Update max-width calculations, responsive breakpoints

### Blog Posts (Apply typography to all)
- **src/content/blog/agent-architecture.md**
- **src/content/blog/claude-skills-deep-dive.md**
- **src/content/blog/context-engineering.md**
- **src/content/blog/directory-watchers.md**
- **src/content/blog/document-generation-skills.md**
- **src/content/blog/single-file-scripts.md**
- **src/content/blog/workflow-prompts.md**

### Content Workflows
- **.claude/commands/new-post.md** - Update frontmatter template, section scaffolding to include typography guidelines
- **.claude/commands/ai-audit.md** - Add typography compliance checks to audit criteria
- **.claude/commands/ameno-finalize.md** - Add typography review step for voice edits
- **ai_docs/design-system.md** - Update with new typography specs, component variants, font stack

### Tests
- **tests/design-system.spec.ts** - Add typography specs validation, font loading tests, WCAG contrast tests
- **tests/design-system-visual.spec.ts** - Update visual regression baselines for new typography
- **tests/blog-posts.spec.ts** - Verify all posts render correctly with new layout

### New Files

#### Configuration
- **astro.config.mjs** - Add Expressive Code integration with dual-theme support, collapsible plugin
- **src/env.d.ts** - TypeScript definitions for Fontsource imports (if needed)

#### Documentation
- **ai_docs/typography-specs.md** - Detailed typography specifications reference document
- **ai_docs/font-loading-guide.md** - Fontsource setup, preloading strategies, performance guidelines

## Implementation Plan

### Phase 1: Foundation - Font Stack & Core Typography
Establish the font loading infrastructure and update core typography tokens. This phase sets the foundation for all subsequent changes by implementing the JetBrains Mono + Inter font stack with proper self-hosting, updating CSS custom properties for fluid typography, and ensuring WCAG contrast compliance.

### Phase 2: Core Implementation - Components & Layout
Upgrade all components and layouts to use the new typography system. This includes integrating Expressive Code for advanced code blocks, refactoring Callout components to 6 semantic variants, implementing the 65ch content column layout pattern, and enhancing image handling with Astro's Picture component.

### Phase 3: Integration - Content Migration & Workflows
Apply the typography system across all existing content and integrate it into content creation/review workflows. This involves updating all blog posts to use new components, modifying content creation commands to enforce typography standards, updating the design system documentation, and expanding the test suite to validate typography compliance.

## Step by Step Tasks

### Group A: Foundation - Font Stack & Typography Tokens [parallel: false, model: sonnet]
Sequential setup of font loading and core typography system that other groups depend on.

#### Step A.1: Install Font Dependencies
- Run `npm install @fontsource-variable/inter @fontsource/jetbrains-mono --save`
- Verify package.json updated with correct versions
- Run `npm install` to ensure clean install

#### Step A.2: Configure Font Loading in BaseLayout
- Import Fontsource fonts in `src/layouts/BaseLayout.astro`
- Add preload links for WOFF2 files with crossorigin attribute
- Configure font-display: swap for zero CLS
- Set up font-feature-settings for ligatures (code) and optical sizing (Inter)

#### Step A.3: Update Typography Tokens in global.css
- Update `--font-family-sans` to use Inter variable font with system fallbacks
- Update `--font-family-mono` to use JetBrains Mono with monospace fallbacks
- Implement body font size: 18-20px (update --text-base to clamp(1.125rem, 1rem + 0.5vw, 1.25rem))
- Update line-height to 1.6 for body text
- Add letter-spacing: +0.5-1.5% for body text on dark backgrounds
- Verify all fluid typography clamp() values match spec ranges
- Update code block font to 85-90% of body size (14-16px effective)
- Set code line-height to 1.4-1.5

#### Step A.4: Implement WCAG Contrast Compliance
- Update foreground color to #E0E0E0 (off-white, not pure white) for 13.5:1 contrast
- Update background to #121212 (not pure black) to prevent halation
- Verify muted-foreground (#A0A0A0) achieves 4.5:1 contrast minimum
- Update code block background to achieve 3:1 contrast vs page background
- Document all contrast ratios in ai_docs/typography-specs.md

#### Step A.5: Update Root HTML Configuration
- Set body max-width to 65ch (research-backed optimal line length)
- Update responsive breakpoints for two-column layout (1100px+)
- Configure font-optical-sizing: auto for Inter variable font
- Enable font-variant-numeric: tabular-nums lining-nums for consistent number rendering

### Group B: Expressive Code Integration [parallel: false, depends: A, model: sonnet]
Install and configure Expressive Code for advanced code block features.

#### Step B.1: Install Expressive Code
- Run `npm install astro-expressive-code @expressive-code/plugin-collapsible-sections --save`
- Verify package.json dependencies

#### Step B.2: Configure Expressive Code in astro.config.mjs
- Import `astroExpressiveCode` and `pluginCollapsibleSections`
- Configure dual-theme support: github-dark + github-light
- Enable collapsible sections plugin
- Set borderRadius: 0.5rem to match design system
- Configure styleOverrides for acid-green accent integration

#### Step B.3: Test Expressive Code Features
- Create test markdown with file tabs using `title="filename.js"` meta-string
- Test line highlighting with `{1-3,5}` syntax
- Test diff highlighting with `// [!code ++]` and `// [!code --]` comments
- Test collapsible sections with `collapse={1-10}` syntax
- Verify copy button functionality

#### Step B.4: Migrate Existing Code Blocks
- Audit all blog posts for code blocks > 15 lines
- Add `collapse` meta-strings to long code examples
- Add `title` attributes for filename context
- Test rendering on all posts

### Group C: Component Refactoring [parallel: true, depends: A, model: auto]
Upgrade components to match new typography and design standards. These tasks can run in parallel as they're independent.

#### Step C.1: Refactor Callout Component to 6 Semantic Variants
- Update Callout.astro to support: note, tip, info, warning, danger, quote (remove success, insight, data)
- Map Lucide icons: Info (note), Lightbulb (tip), TriangleAlert (warning), OctagonAlert (danger), Quote (quote)
- Implement proper dark mode backgrounds: bg-blue-950/50, bg-purple-950/50, bg-amber-950/50, bg-red-950/50, bg-slate-900/50
- Verify border colors match semantic meaning: blue-900, purple-900, amber-900, red-900, slate-300
- Add border-l-4 for quote variant (left border emphasis)
- Update TypeScript interface: `type: 'note' | 'tip' | 'info' | 'warning' | 'danger' | 'quote'`
- Test all variants render correctly with dark mode

#### Step C.2: Update Collapse Component Styling
- Verify compact, default, and prominent variants match new typography specs
- Update padding to use --space-* tokens
- Ensure chevron rotation animation works (90deg on open)
- Test nested CodeBlock margin handling with Expressive Code
- Verify defaultOpen prop behavior

#### Step C.3: Enhance TableOfContents Component
- Verify sticky positioning with `top: var(--spacing-line)`
- Update scrollbar styling for dark theme (4px width, acid-green thumb)
- Ensure 65ch content alignment in two-column layout
- Test progress bar animation on scroll
- Verify active section highlighting with acid-green
- Test "Show More" functionality for >8 sections

#### Step C.4: Implement Picture Component for Images
- Create ImageWrapper.astro component using Astro's Picture
- Configure formats: ['avif', 'webp'] for modern browsers
- Add lazy loading by default
- Implement proper alt text validation
- Test responsive image sizing
- Add click-to-zoom using medium-zoom pattern (optional enhancement)

### Group D: Layout Implementation [parallel: false, depends: A, C, model: sonnet]
Update layouts to implement 65ch line width and two-column patterns.

#### Step D.1: Update BlogPostLayout Two-Column Grid
- Implement CSS Grid: `grid-template-columns: 220px 1fr`
- Set content column to `max-width: 65ch` (not 80ch)
- Configure gap: 3rem between TOC and content
- Update media query breakpoint: `@media (min-width: 1100px)`
- Test sticky TOC positioning
- Verify mobile layout (single column, TOC hidden)

#### Step D.2: Update BaseLayout Max-Width
- Update body max-width to `65ch` for single-column pages
- For two-column layouts: `width: calc(65ch + 220px + 3rem)`
- Update responsive padding: 3ch desktop, 2ch tablet, 1ch mobile
- Test on all breakpoints (320px, 768px, 1100px, 1440px)

#### Step D.3: Implement Prose Wrapper Styling
- Create prose wrapper classes for blog content
- Apply line-length max of 65ch strictly
- Configure heading line-height: 1.2-1.3
- Set paragraph line-height: 1.6
- Add proper word-break and hyphens: auto
- Test long URLs and code snippets don't break layout

### Group E: Content Migration [parallel: true, depends: B, C, model: auto]
Update all existing blog posts to use new components and typography. These can run in parallel.

#### Step E.1: Migrate agent-architecture.md
- Update Callout components to new variants (note/tip/info/warning/danger/quote)
- Add Expressive Code meta-strings to long code blocks
- Verify all headings follow hierarchy (no skipped levels)
- Test rendering and TOC generation

#### Step E.2: Migrate claude-skills-deep-dive.md
- Update Callout components to new variants
- Add Expressive Code meta-strings to long code blocks
- Verify all headings follow hierarchy
- Test rendering and TOC generation

#### Step E.3: Migrate context-engineering.md
- Update Callout components to new variants
- Add Expressive Code meta-strings to long code blocks
- Verify all headings follow hierarchy
- Test rendering and TOC generation

#### Step E.4: Migrate directory-watchers.md
- Update Callout components to new variants
- Add Expressive Code meta-strings to long code blocks
- Verify all headings follow hierarchy
- Test rendering and TOC generation

#### Step E.5: Migrate document-generation-skills.md
- Update Callout components to new variants
- Add Expressive Code meta-strings to long code blocks
- Verify all headings follow hierarchy
- Test rendering and TOC generation

#### Step E.6: Migrate single-file-scripts.md
- Update Callout components to new variants
- Add Expressive Code meta-strings to long code blocks
- Verify all headings follow hierarchy
- Test rendering and TOC generation

#### Step E.7: Migrate workflow-prompts.md
- Update Callout components to new variants
- Add Expressive Code meta-strings to long code blocks
- Verify all headings follow hierarchy
- Test rendering and TOC generation

### Group F: Workflow Updates [parallel: true, depends: A, C, model: auto]
Update content creation and review workflows to enforce new typography standards.

#### Step F.1: Update new-post.md Command
- Add typography guidelines to post creation template
- Update frontmatter template with line-length guidance
- Add callout variant usage examples (6 semantic types)
- Include Expressive Code syntax examples
- Document 65ch line length requirement
- Add WCAG contrast requirement reminders

#### Step F.2: Update ai-audit.md Command
- Add typography compliance checks: font sizes, line-heights, line lengths
- Verify callout variants are semantically correct (no deprecated types)
- Check code blocks >15 lines have collapse meta-strings
- Validate heading hierarchy (no skipped levels)
- Verify WCAG contrast on custom colors
- Check image alt text presence

#### Step F.3: Update ameno-finalize.md Command
- Add typography review step before voice edits
- Ensure edits don't break line length (65ch)
- Verify callout variants remain semantically appropriate after edits
- Check that simplification doesn't remove critical code block context

#### Step F.4: Update design-system.md Documentation
- Document new font stack: JetBrains Mono + Inter with Fontsource
- Update typography specifications table with new values
- Document 6 callout variants (remove success, insight, data)
- Add Expressive Code usage examples
- Update component props for new variants
- Document WCAG contrast ratios achieved
- Add migration guide for deprecated callout types

### Group G: Test Suite Expansion [parallel: false, depends: B, C, E, model: sonnet]
Expand tests to validate new typography system and ensure all posts work correctly.

#### Step G.1: Add Typography Specification Tests
- Test body font size is 18-20px (clamp range)
- Test line-height is 1.6 for body text
- Test line-height is 1.2-1.3 for headings
- Test code font size is 85-90% of body
- Test code line-height is 1.4-1.5
- Test content max-width is 65ch
- Test letter-spacing is present on body text

#### Step G.2: Add Font Loading Tests
- Test Inter variable font loads successfully
- Test JetBrains Mono loads successfully
- Test font-display: swap prevents FOIT
- Test preload links exist for WOFF2 files
- Test font-feature-settings applied correctly

#### Step G.3: Add WCAG Contrast Tests
- Test foreground/background achieves 4.5:1 minimum (target: 13.5:1)
- Test muted-foreground achieves 4.5:1 minimum
- Test all callout variants achieve 4.5:1 contrast
- Test code block background achieves 3:1 vs page background
- Test syntax highlighting colors achieve 4.5:1

#### Step G.4: Add Callout Component Tests
- Test all 6 variants render: note, tip, info, warning, danger, quote
- Test deprecated variants (success, insight, data) show warnings or errors
- Test icons render correctly for each variant
- Test dark mode backgrounds applied correctly
- Test quote variant has border-l-4

#### Step G.5: Add Expressive Code Tests
- Test copy button functionality
- Test collapsible sections expand/collapse
- Test file tabs display correctly
- Test diff highlighting renders
- Test line highlighting works
- Test theme switching (light/dark)

#### Step G.6: Add Layout Tests
- Test two-column grid on desktop (>1100px)
- Test single column on mobile (<1100px)
- Test content column max-width is 65ch
- Test TOC sticky positioning
- Test responsive breakpoints: 320px, 768px, 1100px, 1440px

#### Step G.7: Test All Blog Posts Render
- Test agent-architecture.md renders without errors
- Test claude-skills-deep-dive.md renders without errors
- Test context-engineering.md renders without errors
- Test directory-watchers.md renders without errors
- Test document-generation-skills.md renders without errors
- Test single-file-scripts.md renders without errors
- Test workflow-prompts.md renders without errors
- Verify TOC generates correctly for each post
- Verify no console errors on any post

### Group H: Build & CI Validation [parallel: false, depends: G, model: opus]
Final validation that everything works in production build and CI passes.

#### Step H.1: Run Full Build
- Execute `npm run build`
- Verify no TypeScript errors
- Verify no Astro build errors
- Check bundle size hasn't increased >10%
- Verify all pages generate successfully

#### Step H.2: Run Full Test Suite
- Execute `npm run test`
- Verify all design-system tests pass
- Verify all blog-post tests pass
- Verify all visual regression tests pass
- Check test coverage hasn't decreased

#### Step H.3: Manual Visual Inspection
- Preview build with `npm run preview`
- Inspect each blog post visually
- Verify font loading (no FOUT/FOIT)
- Test responsive breakpoints manually
- Verify callout colors in dark mode
- Test Expressive Code features
- Verify TOC scroll behavior
- Check reading experience at 65ch

#### Step H.4: Fix Any CI Failures
- If tests fail, identify root cause
- Fix failing tests or implementation
- Re-run build and tests until all pass
- Document any edge cases discovered

## Testing Strategy

### Unit Tests
- **Typography Specs**: Validate all typography tokens match specifications (font-size, line-height, letter-spacing, max-width)
- **Font Loading**: Verify Fontsource imports, preload links, font-display settings
- **WCAG Contrast**: Test all color combinations achieve 4.5:1 minimum for text, 3:1 for UI elements
- **Callout Variants**: Ensure all 6 semantic variants render with correct icons, colors, backgrounds
- **Expressive Code**: Validate copy button, collapsible sections, file tabs, diff highlighting, line highlighting
- **Layout Grid**: Test two-column layout on desktop, single column on mobile, 65ch max-width enforcement

### Integration Tests
- **Blog Post Rendering**: Each of the 7 blog posts must render without errors, generate correct TOC, display all components
- **Component Interactions**: Test Callout inside Collapse, CodeBlock auto-collapse, TOC active tracking
- **Responsive Behavior**: Verify layout adapts correctly at 320px, 768px, 1100px, 1440px breakpoints

### Visual Regression Tests
- **Typography Consistency**: Screenshot comparison of before/after for each blog post
- **Dark Mode**: Verify all components render correctly in dark theme
- **Component Variants**: Visual validation of all Callout variants, Collapse variants

### Accessibility Tests
- **ARIA Labels**: Verify all interactive elements have proper labels
- **Keyboard Navigation**: Test all collapsible elements, TOC links, code copy buttons
- **Screen Reader**: Ensure proper semantic HTML structure, heading hierarchy

## Edge Cases

1. **Long Code Blocks**: Code blocks with 100+ lines should collapse properly with Expressive Code
2. **Deep Heading Nesting**: Posts with H4/H5/H6 should still generate correct TOC (test edge case)
3. **Very Long Words**: URLs or code tokens that exceed 65ch should break properly without layout overflow
4. **Missing Font Fallback**: If Fontsource fails to load, system fonts should render without layout shift
5. **Deprecated Callout Types**: Posts using old callout variants (success, insight, data) should show warnings or migrate gracefully
6. **Mobile TOC**: On mobile, TOC should hide gracefully without breaking layout
7. **Zero/One Section**: Posts with <2 headings should not break TOC component
8. **Special Characters**: Heading text with special chars should generate valid slugs for TOC links
9. **Image Loading Failures**: Missing images should not break layout or cause hydration errors
10. **Syntax Highlighting Edge Cases**: Obscure languages or invalid code should not crash Expressive Code

## Acceptance Criteria

### Typography & Fonts
- [ ] Inter variable font loads successfully via Fontsource with zero CLS
- [ ] JetBrains Mono loads successfully via Fontsource with zero CLS
- [ ] Body font size is 18-20px (clamp range validated)
- [ ] Body line-height is 1.6
- [ ] Code font size is 14-16px (85-90% of body)
- [ ] Code line-height is 1.4-1.5
- [ ] Content max-width is 65ch on all blog posts
- [ ] Letter-spacing is +0.5-1.5% on body text

### WCAG Contrast
- [ ] Foreground (#E0E0E0) vs Background (#121212) achieves 13.5:1 contrast
- [ ] Muted foreground (#A0A0A0) achieves 4.5:1 contrast minimum
- [ ] All callout variants achieve 4.5:1 contrast on text
- [ ] Code block background achieves 3:1 contrast vs page background
- [ ] All syntax highlighting colors achieve 4.5:1 contrast

### Components
- [ ] Callout component supports exactly 6 variants: note, tip, info, warning, danger, quote
- [ ] All callout variants render with correct Lucide icons
- [ ] Quote variant has border-l-4 styling
- [ ] Callout dark mode backgrounds use proper opacity (bg-*-950/50)
- [ ] Expressive Code integrates successfully with copy button, collapsible sections, file tabs
- [ ] Code blocks >15 lines auto-collapse with Expressive Code
- [ ] Collapse component maintains 3 variants: default, compact, prominent
- [ ] TableOfContents displays correctly with sticky positioning

### Layout
- [ ] Desktop (>1100px) displays two-column grid: 220px TOC + 65ch content
- [ ] Mobile (<1100px) displays single column with hidden TOC
- [ ] Content column strictly enforces 65ch max-width
- [ ] TOC remains sticky during scroll
- [ ] Responsive breakpoints work: 320px, 768px, 1100px, 1440px

### Content Migration
- [ ] All 7 blog posts render without errors
- [ ] All blog posts use new callout variants (no deprecated types)
- [ ] Long code blocks have Expressive Code meta-strings
- [ ] All posts generate correct TOC
- [ ] No console errors on any blog post page

### Workflows
- [ ] `/new-post` command includes new typography guidelines
- [ ] `/ai-audit` command checks typography compliance
- [ ] `/ameno-finalize` command includes typography review step
- [ ] `ai_docs/design-system.md` documents new font stack, callout variants, specs

### Tests
- [ ] All typography specification tests pass
- [ ] All font loading tests pass
- [ ] All WCAG contrast tests pass
- [ ] All callout component tests pass (6 variants)
- [ ] All Expressive Code tests pass
- [ ] All layout tests pass
- [ ] All blog post rendering tests pass
- [ ] Visual regression tests pass

### Build & CI
- [ ] `npm run build` completes without errors
- [ ] `npm run test` passes all tests
- [ ] Bundle size increase is <10%
- [ ] No TypeScript errors
- [ ] No Astro build errors
- [ ] Preview build looks correct visually

## Validation Commands

Execute these commands to validate the feature is complete:

### Build Validation
```bash
npm run build
```
Expected: Build completes successfully, no errors, all pages generated

### Test Validation
```bash
npm run test
```
Expected: All tests pass, including new typography and component tests

### Type Check
```bash
npm run astro check
```
Expected: No TypeScript errors

### Font Loading Check
```bash
ls -la node_modules/@fontsource-variable/inter/
ls -la node_modules/@fontsource/jetbrains-mono/
```
Expected: Both packages installed with WOFF2 files present

### Preview Build
```bash
npm run preview
```
Expected: Server starts, visit http://localhost:4321 and manually verify:
- Fonts load correctly (Inter for prose, JetBrains Mono for code)
- All blog posts render without errors
- Callout components show 6 variants with correct styling
- Code blocks have Expressive Code features (copy, collapse, tabs)
- Layout is 65ch on desktop with sticky TOC
- Mobile layout is single column

### Contrast Validation
Use browser DevTools to inspect computed colors and verify:
```
Foreground: #E0E0E0 on Background: #121212
Use https://webaim.org/resources/contrastchecker/ to verify 13.5:1 ratio
```

### Component Audit
```bash
grep -r "type=\"success\"" src/content/blog/
grep -r "type=\"insight\"" src/content/blog/
grep -r "type=\"data\"" src/content/blog/
```
Expected: No results (deprecated callout types removed)

### Code Block Audit
```bash
grep -r "```" src/content/blog/ | wc -l
```
Expected: Count code blocks, verify long ones (>15 lines) have collapse meta-strings

## Notes

### Dependencies
- **@fontsource-variable/inter** - Variable font for prose, optimized for dark themes, 405KB
- **@fontsource/jetbrains-mono** - Monospace font for code, 142 ligatures, excellent character differentiation
- **astro-expressive-code** - Advanced code block features, VS Code syntax highlighting
- **@expressive-code/plugin-collapsible-sections** - Enables code block collapsing
- **lucide-react** - Icon library for callout semantic variants (already installed)

### Performance Considerations
- Variable fonts reduce payload by 40% vs multiple static weights
- Self-hosted fonts (Fontsource) eliminate third-party requests
- Preload WOFF2 files for critical fonts to prevent FOUT
- Expressive Code adds ~50KB to bundle but eliminates custom code block JS
- AVIF/WebP image formats reduce image payload by 30-50%

### Browser Compatibility
- Minimum: Chrome 90+, Firefox 88+, Safari 14+ (for clamp() support)
- Expressive Code works in all modern browsers
- Fontsource variable fonts work in all modern browsers
- Fallback to system fonts if Fontsource fails (graceful degradation)

### Migration Path for Deprecated Callouts
- `success` → `tip` (positive suggestion) or `info` (neutral information)
- `insight` → `note` (key takeaway) or `tip` (actionable insight)
- `data` → `info` (data presentation) or `note` (key metric)

### Future Enhancements (Out of Scope)
- Click-to-zoom for images using react-medium-image-zoom
- Video embeds with astro-embed for lazy-loaded YouTube/Vimeo
- Mermaid/D2 diagram integration with astro-mermaid
- Search integration with Pagefind
- Print styles for PDF export
- Reading progress indicator
- Estimated reading time per section
