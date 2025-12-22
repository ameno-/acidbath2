import { test, expect, type Page } from '@playwright/test';

/**
 * ACIDBATH Blog Post Regression Tests
 *
 * These tests enforce content strategy standards for SEO, accessibility,
 * content quality, and performance. Run on every blog post to ensure
 * search ranking and user experience quality.
 */

// Blog post slugs to test - add new posts here
const BLOG_POSTS = [
  'workflow-prompts',
  'context-engineering',
  'agent-architecture',
  'directory-watchers',
  'document-generation-skills',
];

// Content strategy constants
const MIN_DESCRIPTION_LENGTH = 50;
const MAX_DESCRIPTION_LENGTH = 160;
const MIN_TITLE_LENGTH = 20;
const MAX_TITLE_LENGTH = 70;
const MIN_WORD_COUNT = 1500;
const BANNED_PHRASES = [
  'game-changer',
  'revolutionary',
  'cutting-edge',
  'next-generation',
  'paradigm shift',
  'synergy',
  'leverage',
  'disrupt',
];

// ============================================================================
// SEO TESTS
// ============================================================================

test.describe('SEO Requirements', () => {
  for (const slug of BLOG_POSTS) {
    test.describe(`Post: ${slug}`, () => {
      test('has valid meta title', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const title = await page.title();
        expect(title).toBeTruthy();
        expect(title.length).toBeGreaterThanOrEqual(MIN_TITLE_LENGTH);
        expect(title.length).toBeLessThanOrEqual(MAX_TITLE_LENGTH + 20); // Allow for site name suffix
        expect(title).not.toContain('undefined');
        expect(title).not.toContain('null');
      });

      test('has valid meta description', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const description = await page.getAttribute('meta[name="description"]', 'content');
        expect(description).toBeTruthy();
        expect(description!.length).toBeGreaterThanOrEqual(MIN_DESCRIPTION_LENGTH);
        expect(description!.length).toBeLessThanOrEqual(MAX_DESCRIPTION_LENGTH);
      });

      test('has canonical URL', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        // Check for canonical link or og:url
        const canonical = await page.getAttribute('link[rel="canonical"]', 'href');
        const ogUrl = await page.getAttribute('meta[property="og:url"]', 'content');

        expect(canonical || ogUrl).toBeTruthy();
      });

      test('has JSON-LD structured data', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const jsonLd = await page.locator('script[type="application/ld+json"]').textContent();
        expect(jsonLd).toBeTruthy();

        const data = JSON.parse(jsonLd!);
        expect(data['@context']).toBe('https://schema.org');
        expect(data['@type']).toBe('TechArticle');
        expect(data.headline).toBeTruthy();
        expect(data.description).toBeTruthy();
        expect(data.author).toBeTruthy();
        expect(data.datePublished).toBeTruthy();
      });

      test('has AI-specific meta tags', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        // At minimum, check for AI content link
        const aiContentLink = await page.getAttribute('link[rel="ai-content"]', 'href');
        expect(aiContentLink).toBe('/llms.txt');

        // Optional but valuable: AI summary meta tag
        const aiSummary = await page.getAttribute('meta[name="ai-summary"]', 'content');
        // Not all posts may have tldr, so just check if present it's not empty
        if (aiSummary) {
          expect(aiSummary.length).toBeGreaterThan(20);
        }
      });

      test('has proper heading hierarchy', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        // Should have exactly one H1
        const h1Count = await page.locator('h1').count();
        expect(h1Count).toBe(1);

        // H1 should not be empty
        const h1Text = await page.locator('h1').first().textContent();
        expect(h1Text?.trim()).toBeTruthy();

        // Should have H2s for content structure
        const h2Count = await page.locator('article h2, .prose h2').count();
        expect(h2Count).toBeGreaterThanOrEqual(1);
      });

      test('has keywords in JSON-LD', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const jsonLd = await page.locator('script[type="application/ld+json"]').textContent();
        const data = JSON.parse(jsonLd!);

        expect(data.keywords).toBeTruthy();
        expect(data.keywords.length).toBeGreaterThan(0);
      });
    });
  }
});

// ============================================================================
// CONTENT STRUCTURE TESTS
// ============================================================================

test.describe('Content Structure', () => {
  for (const slug of BLOG_POSTS) {
    test.describe(`Post: ${slug}`, () => {
      test('has publication date displayed', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const timeElement = await page.locator('time[datetime]').first();
        await expect(timeElement).toBeVisible();

        const datetime = await timeElement.getAttribute('datetime');
        expect(datetime).toMatch(/^\d{4}-\d{2}-\d{2}/);
      });

      test('has author attribution', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const pageContent = await page.textContent('body');
        expect(pageContent).toMatch(/acidbath|ACIDBATH/i);
      });

      test('has reading time indicator', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const readingTime = await page.locator('.badge-time, [class*="reading-time"]').first();
        await expect(readingTime).toBeVisible();

        const text = await readingTime.textContent();
        expect(text).toMatch(/\d+\s*min/i);
      });

      test('has tags displayed', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const tags = await page.locator('.tags .tag, .tag').first();
        await expect(tags).toBeVisible();
      });

      test('tags are clickable links', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const tagLink = await page.locator('.tags a.tag').first();
        const href = await tagLink.getAttribute('href');
        expect(href).toMatch(/^\/tags\//);
      });

      test('has sufficient content length', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const proseContent = await page.locator('.prose').textContent();
        const wordCount = proseContent?.split(/\s+/).filter(w => w.length > 0).length || 0;

        expect(wordCount).toBeGreaterThanOrEqual(MIN_WORD_COUNT);
      });

      test('does not contain banned marketing phrases', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const content = await page.locator('.prose').textContent();
        const lowerContent = content?.toLowerCase() || '';

        for (const phrase of BANNED_PHRASES) {
          expect(lowerContent).not.toContain(phrase.toLowerCase());
        }
      });

      test('has code blocks if technical post', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        // Technical posts should have code examples
        const codeBlocks = await page.locator('pre code, .astro-code').count();
        expect(codeBlocks).toBeGreaterThanOrEqual(1);
      });
    });
  }
});

// ============================================================================
// LINK VALIDATION TESTS
// ============================================================================

test.describe('Link Validation', () => {
  for (const slug of BLOG_POSTS) {
    test(`Post: ${slug} - internal links are valid`, async ({ page }) => {
      await page.goto(`/blog/${slug}`);

      const internalLinks = await page.locator('a[href^="/"]').all();

      for (const link of internalLinks.slice(0, 10)) { // Limit to first 10 for speed
        const href = await link.getAttribute('href');
        if (href && !href.includes('#')) {
          const response = await page.request.get(href);
          expect(response.status(), `Link ${href} should be valid`).toBeLessThan(400);
        }
      }
    });

    test(`Post: ${slug} - external links have proper attributes`, async ({ page }) => {
      await page.goto(`/blog/${slug}`);

      const externalLinks = await page.locator('a[href^="http"]').all();

      for (const link of externalLinks) {
        const href = await link.getAttribute('href');
        // External links should ideally have rel="noopener" for security
        // This is a soft check - log but don't fail
        const rel = await link.getAttribute('rel');
        if (!rel?.includes('noopener')) {
          console.warn(`External link ${href} missing rel="noopener"`);
        }
      }

      // Just verify external links exist and are https
      for (const link of externalLinks) {
        const href = await link.getAttribute('href');
        if (href && !href.startsWith('https://localhost')) {
          expect(href).toMatch(/^https:\/\//);
        }
      }
    });

    test(`Post: ${slug} - anchor links point to existing sections`, async ({ page }) => {
      await page.goto(`/blog/${slug}`);

      const anchorLinks = await page.locator('a[href^="#"]').all();

      for (const link of anchorLinks) {
        const href = await link.getAttribute('href');
        if (href && href !== '#') {
          const targetId = href.slice(1);
          // Use page.evaluate to check if element exists (handles special chars in IDs)
          const exists = await page.evaluate((id) => {
            return document.getElementById(id) !== null;
          }, targetId);
          expect(exists, `Anchor ${href} should point to existing element`).toBe(true);
        }
      }
    });
  }
});

// ============================================================================
// ASSET LOADING TESTS
// ============================================================================

test.describe('Asset Loading', () => {
  for (const slug of BLOG_POSTS) {
    test.describe(`Post: ${slug}`, () => {
      test('images load successfully', async ({ page }) => {
        const failedImages: string[] = [];

        page.on('response', response => {
          if (response.request().resourceType() === 'image') {
            if (response.status() >= 400) {
              failedImages.push(response.url());
            }
          }
        });

        await page.goto(`/blog/${slug}`);
        await page.waitForLoadState('networkidle');

        expect(failedImages, `Failed images: ${failedImages.join(', ')}`).toHaveLength(0);
      });

      test('images have alt text', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const images = await page.locator('article img, .prose img').all();

        for (const img of images) {
          const alt = await img.getAttribute('alt');
          const src = await img.getAttribute('src');
          expect(alt, `Image ${src} should have alt text`).toBeTruthy();
        }
      });

      test('mermaid diagrams render (if present)', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        // Wait for potential mermaid rendering
        await page.waitForTimeout(1000);

        const mermaidContainers = await page.locator('.mermaid').all();

        for (const container of mermaidContainers) {
          // Mermaid should render SVG inside the container
          const svg = await container.locator('svg').count();
          expect(svg, 'Mermaid diagram should render as SVG').toBeGreaterThan(0);
        }
      });

      test('banner image loads if present', async ({ page }) => {
        await page.goto(`/blog/${slug}`);

        const banner = await page.locator('.post-banner img, .post-banner-img').first();

        if (await banner.count() > 0) {
          await expect(banner).toBeVisible();

          // Check natural dimensions to verify image loaded
          const naturalWidth = await banner.evaluate((img: HTMLImageElement) => img.naturalWidth);
          expect(naturalWidth).toBeGreaterThan(0);
        }
      });
    });
  }
});

// ============================================================================
// PERFORMANCE TESTS
// ============================================================================

test.describe('Performance', () => {
  for (const slug of BLOG_POSTS) {
    test(`Post: ${slug} - page loads within performance budget`, async ({ page }) => {
      const startTime = Date.now();

      await page.goto(`/blog/${slug}`, { waitUntil: 'domcontentloaded' });

      const domContentLoaded = Date.now() - startTime;
      expect(domContentLoaded, 'DOM should load within 3s').toBeLessThan(3000);

      await page.waitForLoadState('load');
      const fullLoad = Date.now() - startTime;
      expect(fullLoad, 'Full page should load within 5s').toBeLessThan(5000);
    });

    test(`Post: ${slug} - Core Web Vitals metrics`, async ({ page }) => {
      await page.goto(`/blog/${slug}`);

      // Largest Contentful Paint (LCP) - should be < 2.5s for "good"
      const lcp = await page.evaluate(() => {
        return new Promise<number>((resolve) => {
          new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            const lastEntry = entries[entries.length - 1];
            resolve(lastEntry.startTime);
          }).observe({ type: 'largest-contentful-paint', buffered: true });

          // Fallback timeout
          setTimeout(() => resolve(0), 5000);
        });
      });

      if (lcp > 0) {
        expect(lcp, 'LCP should be under 2.5s for good score').toBeLessThan(2500);
      }

      // Cumulative Layout Shift (CLS) - should be < 0.1 for "good"
      const cls = await page.evaluate(() => {
        return new Promise<number>((resolve) => {
          let clsValue = 0;
          new PerformanceObserver((entryList) => {
            for (const entry of entryList.getEntries()) {
              if (!(entry as any).hadRecentInput) {
                clsValue += (entry as any).value;
              }
            }
          }).observe({ type: 'layout-shift', buffered: true });

          setTimeout(() => resolve(clsValue), 3000);
        });
      });

      expect(cls, 'CLS should be under 0.1 for good score').toBeLessThan(0.1);
    });

    test(`Post: ${slug} - no render-blocking resources in critical path`, async ({ page }) => {
      await page.goto(`/blog/${slug}`);

      // Check that main content is visible quickly
      const h1 = page.locator('h1').first();
      await expect(h1).toBeVisible({ timeout: 2000 });

      // Check prose content is visible
      const prose = page.locator('.prose').first();
      await expect(prose).toBeVisible({ timeout: 3000 });
    });
  }
});

// ============================================================================
// TABLE OF CONTENTS TESTS
// ============================================================================

test.describe('Table of Contents', () => {
  for (const slug of BLOG_POSTS) {
    test(`Post: ${slug} - TOC exists and links work`, async ({ page }) => {
      // Set viewport to desktop to see TOC
      await page.setViewportSize({ width: 1200, height: 800 });
      await page.goto(`/blog/${slug}`);

      const toc = page.locator('.toc-sidebar, .toc-nav');

      if (await toc.count() > 0) {
        const tocLinks = await page.locator('.toc-link').all();

        // TOC should have links
        expect(tocLinks.length).toBeGreaterThan(0);

        // First TOC link should scroll to section when clicked
        if (tocLinks.length > 0) {
          const href = await tocLinks[0].getAttribute('href');
          expect(href).toMatch(/^#/);
        }
      }
    });
  }
});

// ============================================================================
// ACCESSIBILITY TESTS
// ============================================================================

test.describe('Accessibility Basics', () => {
  for (const slug of BLOG_POSTS) {
    test(`Post: ${slug} - has proper document structure`, async ({ page }) => {
      await page.goto(`/blog/${slug}`);

      // Check lang attribute
      const lang = await page.getAttribute('html', 'lang');
      expect(lang).toBe('en');

      // Check viewport meta
      const viewport = await page.getAttribute('meta[name="viewport"]', 'content');
      expect(viewport).toContain('width=device-width');
    });

    test(`Post: ${slug} - interactive elements are focusable`, async ({ page }) => {
      await page.goto(`/blog/${slug}`);

      // All links should be focusable
      const links = await page.locator('a[href]').all();
      for (const link of links.slice(0, 5)) {
        const tabIndex = await link.getAttribute('tabindex');
        expect(tabIndex).not.toBe('-1');
      }
    });
  }
});

// ============================================================================
// LLMS.TXT TESTS
// ============================================================================

test.describe('AI Content Accessibility', () => {
  test('llms.txt exists and is valid', async ({ page }) => {
    const response = await page.request.get('/llms.txt');
    expect(response.status()).toBe(200);

    const content = await response.text();
    expect(content).toContain('ACIDBATH');
    expect(content.length).toBeGreaterThan(100);
  });

  test('llms-full.txt exists and contains post content', async ({ page }) => {
    const response = await page.request.get('/llms-full.txt');
    expect(response.status()).toBe(200);

    const content = await response.text();

    // Should contain content from all posts
    for (const slug of BLOG_POSTS) {
      const slugWords = slug.replace(/-/g, ' ');
      // At least the slug concept should appear
      expect(content.toLowerCase()).toContain(slugWords.split(' ')[0]);
    }
  });
});
