# Bug: Side-nav sub-heading highlighting

## Metadata
issue_number: `5`
adw_id: `github`
issue_json: `{"number": "5", "title": "Side-nav sub-heading highlighting", "body": "There is a bug with the side-nav. \nhttps://blog.amenoacids.com/blog/directory-watchers/#race-conditions-incomplete-writes\n\n<img width=\"1073\" height=\"851\" alt=\"Image\" src=\"https://github.com/user-attachments/assets/046323f0-efb4-4514-b958-96a944ff71bf\" />\n\nIt doesn't show the sub-heading that is currently selected.\n\nMake sure that the side-nav, content visible on page, and URL remain in sync and always highlight the right content."}`

## Bug Description
The Table of Contents (TOC) sidebar on blog posts fails to highlight sub-headings (h3 elements) when they are currently visible on the page. The URL hash correctly updates to reflect the current section (e.g., `#race-conditions-incomplete-writes`), but the corresponding TOC link does not receive the `.active` class and visual highlighting. This creates a disconnect between what the user is viewing, what the URL indicates, and what the TOC shows as active.

**Symptoms:**
- URL hash updates correctly when scrolling to sections
- TOC links work correctly when clicked
- But TOC active state does not update to match visible content
- Both h2 and h3 headings are affected

**Expected Behavior:**
- When scrolling to any heading (h2 or h3), the corresponding TOC link should be highlighted with the `.active` class
- The TOC active state should always match the currently visible heading
- URL hash, visible content, and TOC highlighting should remain synchronized at all times

**Actual Behavior:**
- TOC highlighting does not update when sections become visible through scrolling
- The URL correctly shows the section hash (e.g., `#race-conditions-incomplete-writes`)
- But the TOC link for that section does not get the `.active` class styling

## Problem Statement
Fix the IntersectionObserver implementation in TableOfContents.astro to correctly detect and highlight the currently visible heading in the TOC sidebar, ensuring synchronization between URL hash, visible content, and TOC active state.

## Solution Statement
The IntersectionObserver in `TableOfContents.astro` currently has insufficient logic to reliably track which heading is actually visible. The root cause is the IntersectionObserver configuration and logic:

1. **Inadequate rootMargin**: The `rootMargin: '-10% 0px -70% 0px'` creates a narrow viewport band that may miss headings when they're in view but outside this band
2. **No URL hash synchronization**: The observer doesn't sync with URL hash changes from manual scrolling or direct navigation
3. **Race condition on page load**: The script may run before all headings are fully rendered in the DOM

The fix involves:
- Adjusting the IntersectionObserver rootMargin to use a more reliable detection zone
- Adding URL hash change listeners to sync TOC state with browser navigation
- Implementing a more robust heading visibility detection algorithm that picks the topmost visible heading
- Adding initialization logic that sets the correct active state on page load based on the URL hash

## Steps to Reproduce
1. Navigate to https://blog.amenoacids.com/blog/directory-watchers/
2. Scroll to the "Race Conditions: Incomplete Writes" section (or any h3 sub-heading)
3. Observe that the URL updates to `#race-conditions-incomplete-writes`
4. Look at the TOC sidebar on the left
5. Note that the "Race Conditions: Incomplete Writes" link is NOT highlighted with active styling
6. Compare with the URL hash - there's a mismatch

Alternative reproduction:
1. Navigate directly to https://blog.amenoacids.com/blog/directory-watchers/#race-conditions-incomplete-writes
2. Observe that the TOC does not highlight the corresponding section on initial page load

## Root Cause Analysis
The issue lies in the `TableOfContents.astro` component's IntersectionObserver implementation (lines 36-95).

**Primary Issues:**

1. **Narrow IntersectionObserver viewport** (line 75):
   ```typescript
   rootMargin: '-10% 0px -70% 0px'
   ```
   This creates a band from 10% below the top to 30% from the top of the viewport. Headings outside this narrow band won't trigger intersection events, leading to missed updates.

2. **No URL hash synchronization**:
   - When the page loads with a hash (e.g., `#race-conditions-incomplete-writes`), there's no logic to set the initial active state based on the URL
   - When users navigate via browser back/forward or direct hash changes, the TOC doesn't update

3. **Timing issues on initialization** (lines 89-94):
   - The script waits for `DOMContentLoaded` or runs immediately, but doesn't account for Astro's client-side navigation events
   - On Astro page transitions, the observer may not reinitialize correctly

4. **Incomplete active state logic** (lines 64-70):
   - Only toggles `.active` on the link element
   - The parent `li` gets `.is-active` class, but this only happens when IntersectionObserver fires
   - No fallback mechanism when IntersectionObserver misses an intersection

**Secondary Issues:**
- The IntersectionObserver threshold `[0, 0.5, 1]` requires significant portions of the heading to be visible, which may not trigger for small headings or quick scrolling
- No debouncing or throttling, potentially causing performance issues with rapid scroll events

## Relevant Files
Use these files to fix the bug:

- **`/Users/ameno/dev/acidbath2/trees/github/src/components/TableOfContents.astro`** (PRIMARY)
  - Lines 36-95: IntersectionObserver implementation with flawed rootMargin and no URL hash sync
  - Lines 50-78: Observer callback that needs improved visibility detection logic
  - Lines 89-94: Initialization that needs URL hash handling on page load

- **`/Users/ameno/dev/acidbath2/trees/github/src/layouts/BlogPostLayout.astro`** (SECONDARY - for testing)
  - Lines 432-527: TOC sidebar styles including `.toc-link.active` (line 498-502) and `.toc-item.is-active` (line 504-507)
  - Used to verify that active styles are correctly applied after the fix

### New Files
None - this is a bug fix to existing functionality

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Analyze Current Behavior
- Read the TableOfContents.astro file completely to understand the current implementation
- Identify all intersection observer configuration parameters and their effects
- Document the current active state update logic and its failure modes

### 2. Implement URL Hash Synchronization
- Add a `hashchange` event listener to detect URL hash changes from browser navigation
- Add initialization logic to set active state based on URL hash on page load
- Ensure the active state updates when users navigate via browser back/forward buttons

### 3. Fix IntersectionObserver Configuration
- Adjust `rootMargin` to use a more reliable detection zone (e.g., `-20% 0px -20% 0px` for a centered viewport band)
- Modify the threshold values to trigger more reliably for headings of various sizes
- Consider changing the logic to detect the heading closest to the top of the viewport rather than requiring full intersection

### 4. Improve Active State Logic
- Implement a more robust algorithm to determine which heading should be considered "active"
- Add logic to find the topmost visible heading when multiple headings are in view
- Ensure the active class is applied consistently to both the link and parent li elements

### 5. Add Fallback Mechanisms
- Implement a scroll event listener as a fallback when IntersectionObserver misses updates
- Add debouncing to prevent performance issues with rapid scrolling
- Ensure the TOC updates even if IntersectionObserver fails to fire

### 6. Test All Scenarios
- Test scrolling through the blog post to verify TOC updates correctly
- Test direct navigation to a hash URL (e.g., `#race-conditions-incomplete-writes`)
- Test browser back/forward navigation
- Test clicking TOC links
- Test on different viewport sizes to ensure responsive behavior
- Verify that h2 and h3 headings both highlight correctly

### 7. Verify Synchronization
- Confirm that URL hash, visible content, and TOC active state remain in sync
- Test rapid scrolling to ensure no race conditions or missed updates
- Verify behavior on page load, navigation, and scroll events

### 8. Clean Up and Optimize
- Remove any unnecessary code or comments
- Ensure the script is properly scoped and doesn't leak global variables
- Verify that cleanup functions properly disconnect observers on navigation
- Add code comments explaining the fix for future maintainers

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

```bash
# Start the development server
npm run dev

# Manual testing checklist (no automated tests for this visual/interaction bug):
# 1. Navigate to http://localhost:4321/blog/directory-watchers/
# 2. Scroll slowly through the article
#    ✓ TOC should highlight each section as it becomes visible
# 3. Navigate to http://localhost:4321/blog/directory-watchers/#race-conditions-incomplete-writes
#    ✓ TOC should highlight "Race Conditions: Incomplete Writes" on page load
# 4. Click a TOC link
#    ✓ Should navigate to section and maintain highlighting
# 5. Use browser back button
#    ✓ TOC should update to reflect previous section
# 6. Test on multiple blog posts to ensure no regressions
# 7. Verify responsive behavior on different viewport sizes

# Build and preview production bundle to ensure no build errors
npm run build
npm run preview

# Run existing tests to ensure no regressions
npm run test
```

## Notes
- This is purely a client-side JavaScript/TypeScript fix - no backend or build changes needed
- The fix should not require any changes to CSS styles - the `.active` and `.is-active` classes are already properly styled
- Focus on making the IntersectionObserver more reliable and adding URL hash synchronization as the primary fix
- Consider progressive enhancement: the TOC should remain functional even if JavaScript fails
- The same TableOfContents component is used across all blog posts, so the fix will apply site-wide
- Test with both h2 and h3 headings since the bug affects both depth levels
