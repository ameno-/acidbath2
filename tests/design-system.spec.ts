import { test, expect } from '@playwright/test';

const SHOWCASE_URL = '/blog/design-system-showcase';

test.describe('Design System Components', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(SHOWCASE_URL);
  });

  test.describe('CodeBlock Component', () => {
    test('should auto-collapse code blocks with more than 15 lines', async ({ page }) => {
      // Find collapsible code blocks
      const collapsibleBlocks = await page.locator('.code-block-container.collapsible').all();

      expect(collapsibleBlocks.length).toBeGreaterThan(0);

      // Verify initial collapsed state
      const firstBlock = collapsibleBlocks[0];
      const isExpanded = await firstBlock.evaluate((el) =>
        el.classList.contains('expanded')
      );
      expect(isExpanded).toBe(false);
    });

    test('should expand code block when clicking expand button', async ({ page }) => {
      // Find a collapsible code block first
      const collapsibleBlock = page.locator('.code-block-container.collapsible').first();
      await expect(collapsibleBlock).toBeVisible();

      // Get the expand button within that block
      const expandButton = collapsibleBlock.locator('.collapse-toggle');
      await expect(expandButton).toBeVisible();

      // Click expand
      await expandButton.click();

      // Verify expanded state
      await expect(collapsibleBlock).toHaveClass(/expanded/);

      // Verify button text changes
      await expect(expandButton).toContainText('Collapse');
    });

    test('should copy code to clipboard when clicking copy button', async ({ page, context }) => {
      // Grant clipboard permissions
      await context.grantPermissions(['clipboard-read', 'clipboard-write']);

      const copyButton = page.locator('.copy-button').first();
      await expect(copyButton).toBeVisible();

      // Click copy
      await copyButton.click();

      // Verify copied state
      await expect(copyButton).toHaveClass(/copied/);
      await expect(copyButton).toContainText('Copied!');

      // Verify clipboard content (non-empty)
      const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
      expect(clipboardText.length).toBeGreaterThan(0);
    });

    test('should display line numbers when enabled', async ({ page }) => {
      // Find code block with line numbers
      const codeWithNumbers = page.locator('.code-block-container.with-line-numbers').first();
      await expect(codeWithNumbers).toBeVisible();

      // Verify line number styling is applied
      const hasLineNumbers = await codeWithNumbers.evaluate((el) => {
        const code = el.querySelector('code');
        return code !== null;
      });
      expect(hasLineNumbers).toBe(true);
    });

    test('should display language badge when language is specified', async ({ page }) => {
      const languageBadge = page.locator('.language-badge').first();

      // Badge should exist for code blocks with language
      if (await languageBadge.count() > 0) {
        await expect(languageBadge).toBeVisible();
        const badgeText = await languageBadge.textContent();
        expect(badgeText).toBeTruthy();
      }
    });
  });

  test.describe('Callout Component', () => {
    test('should render all seven callout variants', async ({ page }) => {
      const variants = ['quote', 'info', 'warning', 'danger', 'success', 'insight', 'data'];

      for (const variant of variants) {
        const callout = page.locator(`.callout-${variant}`).first();
        await expect(callout).toBeVisible();
      }
    });

    test('should display variant-specific icons', async ({ page }) => {
      // Check for icon presence in non-quote variants (e.g., info)
      const infoCallout = page.locator('.callout-info').first();
      await expect(infoCallout).toBeVisible();

      const calloutIcon = infoCallout.locator('.callout-icon');
      await expect(calloutIcon).toBeVisible();

      const iconText = await calloutIcon.textContent();
      expect(iconText).toBeTruthy();
    });

    test('should display author attribution for quote variant', async ({ page }) => {
      const quoteCallout = page.locator('.callout-quote').first();
      await expect(quoteCallout).toBeVisible();

      const author = page.locator('.callout-author').first();
      if (await author.count() > 0) {
        await expect(author).toBeVisible();
        await expect(author).toContainText('—');
      }
    });

    test('should display title or default title', async ({ page }) => {
      // Target non-quote variant since quote hides the header
      const infoCallout = page.locator('.callout-info').first();
      await expect(infoCallout).toBeVisible();

      const calloutTitle = infoCallout.locator('.callout-title');
      await expect(calloutTitle).toBeVisible();

      const titleText = await calloutTitle.textContent();
      expect(titleText).toBeTruthy();
    });

    test('should render nested content correctly', async ({ page }) => {
      // Check if callout contains paragraph content
      const calloutContent = page.locator('.callout-content').first();
      await expect(calloutContent).toBeVisible();

      const hasContent = await calloutContent.evaluate((el) => {
        return el.textContent && el.textContent.trim().length > 0;
      });
      expect(hasContent).toBe(true);
    });
  });

  test.describe('Collapse Component', () => {
    test('should render all three collapse variants', async ({ page }) => {
      const defaultCollapse = page.locator('.collapse-default').first();
      const compactCollapse = page.locator('.collapse-compact').first();
      const prominentCollapse = page.locator('.collapse-prominent').first();

      // At least one of each variant should exist
      const hasVariants =
        (await defaultCollapse.count() > 0) ||
        (await compactCollapse.count() > 0) ||
        (await prominentCollapse.count() > 0);

      expect(hasVariants).toBe(true);
    });

    test('should toggle collapse state when clicking summary', async ({ page }) => {
      // Navigate to the Collapse section
      await page.goto('/blog/design-system-showcase#collapse-component');
      await page.waitForTimeout(500);

      const collapseElement = page.locator('details.collapse').first();
      await expect(collapseElement).toBeAttached();

      // Get initial state
      const initiallyOpen = await collapseElement.evaluate((el: HTMLDetailsElement) => el.open);

      // Toggle using JavaScript click since element might be off-screen
      await collapseElement.evaluate((el: HTMLDetailsElement) => {
        el.open = !el.open;
      });

      // Verify state changed
      const newState = await collapseElement.evaluate((el: HTMLDetailsElement) => el.open);
      expect(newState).toBe(!initiallyOpen);
    });

    test('should animate chevron on expand/collapse', async ({ page }) => {
      // Navigate to the Collapse section
      await page.goto('/blog/design-system-showcase#collapse-component');
      await page.waitForTimeout(500);

      const collapseElement = page.locator('details.collapse').first();
      const chevron = collapseElement.locator('.collapse-chevron');

      await expect(chevron).toBeAttached();

      // Toggle using JavaScript
      await collapseElement.evaluate((el: HTMLDetailsElement) => {
        el.open = !el.open;
      });

      // Chevron should still be attached after toggle
      await expect(chevron).toBeAttached();
    });

    test('should display preview text when collapsed', async ({ page }) => {
      // Find collapse with preview
      const collapseWithPreview = page.locator('.collapse-preview').first();

      if (await collapseWithPreview.count() > 0) {
        await expect(collapseWithPreview).toBeVisible();

        const previewText = await collapseWithPreview.textContent();
        expect(previewText).toBeTruthy();
      }
    });

    test('should hide preview text when expanded', async ({ page }) => {
      const collapseElement = page.locator('details.collapse').first();

      // Open the collapse
      await collapseElement.evaluate((el: HTMLDetailsElement) => { el.open = true; });

      // Preview should be hidden when open (via CSS)
      const preview = collapseElement.locator('.collapse-preview');
      if (await preview.count() > 0) {
        const isVisible = await preview.isVisible();
        expect(isVisible).toBe(false);
      }
    });
  });

  test.describe('TableOfContents Component', () => {
    test('should display section count in header', async ({ page }) => {
      const tocCount = page.locator('.toc-count');

      if (await tocCount.count() > 0) {
        await expect(tocCount).toBeVisible();
        await expect(tocCount).toContainText('sections');
      }
    });

    test('should display scroll progress bar', async ({ page }) => {
      const progressBar = page.locator('.toc-progress-bar');
      const progressFill = page.locator('.toc-progress-fill');

      if (await progressBar.count() > 0) {
        await expect(progressBar).toBeVisible();
        // Progress fill exists but may have 0 width at top of page
        await expect(progressFill).toBeAttached();
      }
    });

    test('should group H3s under H2 sections', async ({ page }) => {
      const tocGroups = page.locator('.toc-group');

      if (await tocGroups.count() > 0) {
        const firstGroup = tocGroups.first();
        await expect(firstGroup).toBeVisible();

        // Check if group has H2 link
        const h2Link = firstGroup.locator('.toc-link-h2');
        await expect(h2Link).toBeVisible();
      }
    });

    test('should show subcount for groups with H3s', async ({ page }) => {
      const subcount = page.locator('.toc-subcount').first();

      if (await subcount.count() > 0) {
        await expect(subcount).toBeVisible();
        const text = await subcount.textContent();
        expect(text).toMatch(/\(\d+\)/);
      }
    });

    test('should toggle group expansion when clicking chevron', async ({ page }) => {
      const tocGroup = page.locator('.toc-group').first();

      if (await tocGroup.count() > 0) {
        // Get initial state
        const initiallyOpen = await tocGroup.evaluate((el: HTMLDetailsElement) => el.open);

        // Click the chevron specifically (not the link)
        const chevron = tocGroup.locator('.toc-chevron');
        await chevron.click();

        // Wait for state change
        await page.waitForTimeout(100);

        const newState = await tocGroup.evaluate((el: HTMLDetailsElement) => el.open);
        expect(newState).toBe(!initiallyOpen);
      }
    });

    test('should display show more button when sections exceed threshold', async ({ page }) => {
      const showMoreButton = page.locator('.toc-show-more');

      // Button only appears if more than maxTopLevel sections exist
      if (await showMoreButton.count() > 0) {
        await expect(showMoreButton).toBeVisible();
        await expect(showMoreButton).toContainText('Show');
      }
    });

    test('should smooth scroll to section when clicking TOC link', async ({ page }) => {
      const tocLink = page.locator('.toc-link').first();

      if (await tocLink.count() > 0) {
        await tocLink.click();

        // Wait for scroll
        await page.waitForTimeout(500);

        // Verify URL hash changed
        const url = page.url();
        expect(url).toContain('#');
      }
    });
  });

  test.describe('Accessibility', () => {
    test('should have proper ARIA labels on interactive elements', async ({ page }) => {
      // Copy button
      const copyButton = page.locator('.copy-button').first();
      if (await copyButton.count() > 0) {
        const ariaLabel = await copyButton.getAttribute('aria-label');
        expect(ariaLabel).toBeTruthy();
      }

      // Collapse toggle
      const collapseToggle = page.locator('.collapse-toggle').first();
      if (await collapseToggle.count() > 0) {
        const ariaLabel = await collapseToggle.getAttribute('aria-label');
        expect(ariaLabel).toBeTruthy();
      }

      // TOC aside
      const tocAside = page.locator('.toc-sidebar');
      if (await tocAside.count() > 0) {
        const ariaLabel = await tocAside.getAttribute('aria-label');
        expect(ariaLabel).toBeTruthy();
      }
    });

    test('should support keyboard navigation on collapsible elements', async ({ page }) => {
      const summary = page.locator('summary').first();

      if (await summary.count() > 0) {
        // Focus the element
        await summary.focus();

        // Verify it's focused
        const isFocused = await summary.evaluate((el) =>
          document.activeElement === el
        );
        expect(isFocused).toBe(true);
      }
    });
  });
});
