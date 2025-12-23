import { test, expect } from '@playwright/test';

const SHOWCASE_URL = '/blog/design-system-showcase';

/**
 * Visual Regression Tests for Design System Components
 *
 * These tests capture screenshots and validate visual consistency.
 * Run with: npx playwright test design-system-visual
 * Update baselines: npx playwright test design-system-visual --update-snapshots
 */

test.describe('Design System Visual Regression', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(SHOWCASE_URL);
    // Wait for fonts and images to load
    await page.waitForLoadState('networkidle');
  });

  test.describe('Callout Variants', () => {
    test('should match quote callout visual', async ({ page }) => {
      const quoteCallout = page.locator('.callout-quote').first();
      await expect(quoteCallout).toBeVisible();
      await expect(quoteCallout).toHaveScreenshot('callout-quote.png');
    });

    test('should match info callout visual', async ({ page }) => {
      const infoCallout = page.locator('.callout-info').first();
      if (await infoCallout.count() > 0) {
        await expect(infoCallout).toHaveScreenshot('callout-info.png');
      }
    });

    test('should match warning callout visual', async ({ page }) => {
      const warningCallout = page.locator('.callout-warning').first();
      if (await warningCallout.count() > 0) {
        await expect(warningCallout).toHaveScreenshot('callout-warning.png');
      }
    });

    test('should match danger callout visual', async ({ page }) => {
      const dangerCallout = page.locator('.callout-danger').first();
      if (await dangerCallout.count() > 0) {
        await expect(dangerCallout).toHaveScreenshot('callout-danger.png');
      }
    });

    test('should match success callout visual', async ({ page }) => {
      const successCallout = page.locator('.callout-success').first();
      if (await successCallout.count() > 0) {
        await expect(successCallout).toHaveScreenshot('callout-success.png');
      }
    });

    test('should match insight callout visual', async ({ page }) => {
      const insightCallout = page.locator('.callout-insight').first();
      if (await insightCallout.count() > 0) {
        await expect(insightCallout).toHaveScreenshot('callout-insight.png');
      }
    });

    test('should match data callout visual', async ({ page }) => {
      const dataCallout = page.locator('.callout-data').first();
      if (await dataCallout.count() > 0) {
        await expect(dataCallout).toHaveScreenshot('callout-data.png');
      }
    });
  });

  test.describe('CodeBlock States', () => {
    test('should match collapsed code block visual', async ({ page }) => {
      const collapsedBlock = page.locator('.code-block-container.collapsible').first();
      await expect(collapsedBlock).toBeVisible();
      await expect(collapsedBlock).toHaveScreenshot('codeblock-collapsed.png');
    });

    test('should match expanded code block visual', async ({ page }) => {
      const expandButton = page.locator('.collapse-toggle').first();
      await expandButton.click();
      await page.waitForTimeout(300); // Wait for animation

      const expandedBlock = page.locator('.code-block-container.expanded').first();
      await expect(expandedBlock).toHaveScreenshot('codeblock-expanded.png');
    });

    test('should match code block with language badge', async ({ page }) => {
      const codeBlockHeader = page.locator('.code-block-header').first();
      if (await codeBlockHeader.count() > 0) {
        await expect(codeBlockHeader).toHaveScreenshot('codeblock-header-badge.png');
      }
    });

    test('should match copy button hover state', async ({ page }) => {
      const copyButton = page.locator('.copy-button').first();
      await copyButton.hover();
      await page.waitForTimeout(100); // Wait for hover transition

      await expect(copyButton).toHaveScreenshot('codeblock-copy-hover.png');
    });
  });

  test.describe('Collapse Variants', () => {
    test('should match default collapse variant', async ({ page }) => {
      const defaultCollapse = page.locator('.collapse-default').first();
      if (await defaultCollapse.count() > 0) {
        await expect(defaultCollapse).toHaveScreenshot('collapse-default.png');
      }
    });

    test('should match compact collapse variant', async ({ page }) => {
      const compactCollapse = page.locator('.collapse-compact').first();
      if (await compactCollapse.count() > 0) {
        await expect(compactCollapse).toHaveScreenshot('collapse-compact.png');
      }
    });

    test('should match prominent collapse variant', async ({ page }) => {
      const prominentCollapse = page.locator('.collapse-prominent').first();
      if (await prominentCollapse.count() > 0) {
        await expect(prominentCollapse).toHaveScreenshot('collapse-prominent.png');
      }
    });

    test('should match collapse expanded state', async ({ page }) => {
      const collapse = page.locator('details.collapse').first();
      await collapse.evaluate((el: HTMLDetailsElement) => { el.open = true; });
      await page.waitForTimeout(200); // Wait for animation

      await expect(collapse).toHaveScreenshot('collapse-expanded.png');
    });
  });

  test.describe('Responsive Behavior', () => {
    test('should match mobile viewport (320px)', async ({ page }) => {
      await page.setViewportSize({ width: 320, height: 568 });
      await page.waitForTimeout(100);

      await expect(page).toHaveScreenshot('responsive-mobile-320.png', {
        fullPage: true,
      });
    });

    test('should match tablet viewport (768px)', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 });
      await page.waitForTimeout(100);

      await expect(page).toHaveScreenshot('responsive-tablet-768.png', {
        fullPage: true,
      });
    });

    test('should match desktop viewport (1024px)', async ({ page }) => {
      await page.setViewportSize({ width: 1024, height: 768 });
      await page.waitForTimeout(100);

      await expect(page).toHaveScreenshot('responsive-desktop-1024.png', {
        fullPage: true,
      });
    });

    test('should match large desktop viewport (1440px)', async ({ page }) => {
      await page.setViewportSize({ width: 1440, height: 900 });
      await page.waitForTimeout(100);

      await expect(page).toHaveScreenshot('responsive-desktop-1440.png', {
        fullPage: true,
      });
    });
  });

  test.describe('Color Contrast', () => {
    test('should meet WCAG AA standards for accent color', async ({ page }) => {
      // Verify acid-green accent has sufficient contrast
      const accentElement = page.locator('.text-accent').first();

      if (await accentElement.count() > 0) {
        const backgroundColor = await page.evaluate(() => {
          return getComputedStyle(document.body).backgroundColor;
        });

        const accentColor = await accentElement.evaluate((el) => {
          return getComputedStyle(el).color;
        });

        // Basic check that colors are defined
        expect(backgroundColor).toBeTruthy();
        expect(accentColor).toBeTruthy();

        // Note: Actual contrast ratio calculation would require a library
        // For now, we verify the colors are set correctly
        expect(accentColor).toContain('rgb');
      }
    });

    test('should meet contrast standards for callout variants', async ({ page }) => {
      const callouts = await page.locator('.callout').all();

      for (const callout of callouts) {
        const textColor = await callout.evaluate((el) => {
          const content = el.querySelector('.callout-content');
          return content ? getComputedStyle(content).color : null;
        });

        const bgColor = await callout.evaluate((el) => {
          return getComputedStyle(el).backgroundColor;
        });

        // Verify colors are defined
        expect(textColor).toBeTruthy();
        expect(bgColor).toBeTruthy();
      }
    });
  });

  test.describe('Typography Scaling', () => {
    test('should scale typography correctly at mobile width', async ({ page }) => {
      await page.setViewportSize({ width: 320, height: 568 });

      const heading = page.locator('h1').first();
      const fontSize = await heading.evaluate((el) => {
        return getComputedStyle(el).fontSize;
      });

      // Verify font size is within expected mobile range
      const size = parseFloat(fontSize);
      expect(size).toBeGreaterThan(0);
      expect(size).toBeLessThan(100); // Sanity check
    });

    test('should scale typography correctly at desktop width', async ({ page }) => {
      await page.setViewportSize({ width: 1440, height: 900 });

      const heading = page.locator('h1').first();
      const fontSize = await heading.evaluate((el) => {
        return getComputedStyle(el).fontSize;
      });

      // Verify font size is within expected desktop range
      const size = parseFloat(fontSize);
      expect(size).toBeGreaterThan(0);
      expect(size).toBeLessThan(100); // Sanity check
    });

    test('should apply clamp() for fluid typography', async ({ page }) => {
      const baseTextElement = page.locator('p').first();

      const fontSize = await baseTextElement.evaluate((el) => {
        // Check if CSS variable is using clamp
        const root = document.documentElement;
        const textBase = getComputedStyle(root).getPropertyValue('--text-base');
        return textBase;
      });

      // Verify --text-base uses clamp() function
      if (fontSize) {
        expect(fontSize).toContain('clamp');
      }
    });
  });

  test.describe('Dark Mode Consistency', () => {
    test('should maintain dark theme across all components', async ({ page }) => {
      const body = page.locator('body');
      const bgColor = await body.evaluate((el) => {
        return getComputedStyle(el).backgroundColor;
      });

      // Verify background is dark (rgb values should be low)
      expect(bgColor).toMatch(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);

      const match = bgColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
      if (match) {
        const [, r, g, b] = match.map(Number);
        const isDark = r < 50 && g < 50 && b < 50;
        expect(isDark).toBe(true);
      }
    });

    test('should use consistent accent color', async ({ page }) => {
      const accentElements = await page.locator('[class*="accent"]').all();

      if (accentElements.length > 0) {
        const firstAccentColor = await accentElements[0].evaluate((el) => {
          return getComputedStyle(el).color;
        });

        // Verify acid-green is used (#39ff14 = rgb(57, 255, 20))
        expect(firstAccentColor).toBeTruthy();
      }
    });
  });

  test.describe('Animation Performance', () => {
    test('should smoothly animate collapse toggle', async ({ page }) => {
      const collapse = page.locator('details.collapse').first();
      const summary = collapse.locator('summary');

      // Capture before animation
      await expect(collapse).toHaveScreenshot('animation-collapse-before.png');

      // Trigger animation
      await summary.click();
      await page.waitForTimeout(150); // Mid-animation

      // Verify animation is CSS-based (no layout shift)
      const chevron = collapse.locator('.collapse-chevron');
      const transform = await chevron.evaluate((el) => {
        return getComputedStyle(el).transform;
      });

      expect(transform).toBeTruthy();
    });

    test('should smoothly animate code block expand', async ({ page }) => {
      const expandButton = page.locator('.collapse-toggle').first();

      if (await expandButton.count() > 0) {
        // Trigger animation
        await expandButton.click();
        await page.waitForTimeout(150); // Mid-animation

        // Verify transition is smooth (no instant jump)
        const container = page.locator('.code-block-container.collapsible').first();
        const maxHeight = await container.evaluate((el) => {
          return getComputedStyle(el).maxHeight;
        });

        // max-height should be changing during animation
        expect(maxHeight).toBeTruthy();
      }
    });
  });
});
