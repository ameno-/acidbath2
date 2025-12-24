/**
 * Rehype plugin to enhance code blocks with SSR structure
 *
 * Adds:
 * - Container wrapper with line count data
 * - Collapsible class for blocks > 15 lines
 * - Line numbers class
 * - Language detection from code class
 * - GitHub source links (header + SEO footer)
 *
 * GitHub Link Format:
 * Use meta string: ```python github=https://github.com/user/repo/blob/main/file.py#L1-L50
 * Or first-line comment: # github: https://github.com/...
 *
 * This enables:
 * - No layout shift (structure rendered SSR)
 * - SEO-friendly semantic HTML with source links
 * - JS only handles interactivity
 */

import { visit } from 'unist-util-visit';
import { h } from 'hastscript';

const COLLAPSE_THRESHOLD = 15;
const PREVIEW_LINES = 8;
const GITHUB_REGEX = /github[=:]\s*(https:\/\/github\.com\/[^\s]+)/i;
const GITHUB_COMMENT_REGEX = /^#\s*github:\s*(https:\/\/github\.com\/[^\s]+)/im;
const GITHUB_HTML_COMMENT_REGEX = /<!--\s*github:\s*(https:\/\/github\.com\/[^\s]+)\s*-->/im;
const GITHUB_SLASHSLASH_COMMENT_REGEX = /^\/\/\s*github:\s*(https:\/\/github\.com\/[^\s]+)/im;

/**
 * Extract GitHub URL from meta string or first-line comment
 */
function extractGitHubUrl(metaString, codeContent) {
  // Try meta string first (e.g., ```python github=https://...)
  if (metaString) {
    const match = metaString.match(GITHUB_REGEX);
    if (match) return match[1];
  }

  // Try first-line comment (e.g., # github: https://...)
  const commentMatch = codeContent.match(GITHUB_COMMENT_REGEX);
  if (commentMatch) return commentMatch[1];

  // Try HTML comment (e.g., <!-- github: https://... -->)
  const htmlCommentMatch = codeContent.match(GITHUB_HTML_COMMENT_REGEX);
  if (htmlCommentMatch) return htmlCommentMatch[1];

  // Try // comment (e.g., // github: https://... for JS/JSON/etc)
  const slashCommentMatch = codeContent.match(GITHUB_SLASHSLASH_COMMENT_REGEX);
  if (slashCommentMatch) return slashCommentMatch[1];

  return null;
}

/**
 * Parse GitHub URL to extract file path and line range
 */
function parseGitHubUrl(url) {
  if (!url) return null;

  try {
    const parsed = new URL(url);
    const pathParts = parsed.pathname.split('/');
    // Format: /user/repo/blob/branch/path/to/file.ext
    const user = pathParts[1];
    const repo = pathParts[2];
    const filePath = pathParts.slice(5).join('/');
    const lineRange = parsed.hash; // e.g., #L1-L50

    return {
      url,
      user,
      repo,
      filePath,
      lineRange,
      displayText: filePath + (lineRange || '')
    };
  } catch {
    return null;
  }
}

export default function rehypeCodeBlocks() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      // Find <pre> elements containing <code>
      if (node.tagName !== 'pre') return;
      if (!parent || index === undefined) return;

      const codeNode = node.children?.find(
        child => child.type === 'element' && child.tagName === 'code'
      );

      if (!codeNode) return;

      // Skip mermaid blocks
      const codeClasses = codeNode.properties?.className || [];
      if (codeClasses.some(c => c.includes('mermaid'))) return;

      // Extract language from class (e.g., 'language-python' -> 'python')
      const langClass = codeClasses.find(c => c.startsWith('language-'));
      const language = langClass ? langClass.replace('language-', '') : '';

      // Count lines in code content
      const codeContent = getTextContent(codeNode);
      const lineCount = (codeContent.match(/\n/g) || []).length + 1;

      // Extract GitHub URL from meta or comment
      // Shiki/Astro stores meta in different places depending on version
      const metaString = node.properties?.metastring
        || node.properties?.dataMetastring
        || node.data?.meta
        || codeNode.properties?.metastring
        || codeNode.data?.meta
        || '';
      const githubUrl = extractGitHubUrl(metaString, codeContent);
      const githubInfo = parseGitHubUrl(githubUrl);

      // Determine if should collapse
      const shouldCollapse = lineCount > COLLAPSE_THRESHOLD;

      // Build container classes
      const containerClasses = ['code-block-container'];
      if (shouldCollapse) containerClasses.push('collapsible');
      containerClasses.push('with-line-numbers');
      if (githubInfo) containerClasses.push('has-github-link');

      // Create header with language and optional GitHub link
      const headerChildren = [];
      const headerElements = [];

      if (language) {
        headerElements.push(h('span.code-block-label', language.toUpperCase()));
        headerElements.push(h('span.language-badge', language));
      }

      // Add GitHub link to header
      if (githubInfo) {
        headerElements.push(
          h('a.github-header-link', {
            href: githubInfo.url,
            target: '_blank',
            rel: 'noopener noreferrer',
            title: `View source on GitHub: ${githubInfo.displayText}`
          }, [
            h('span.github-icon', '↗'),
            h('span.github-text', 'GitHub')
          ])
        );
      }

      if (headerElements.length > 0) {
        headerChildren.push(h('div.code-block-header', headerElements));
      }

      // Create copy button (SSR structure, JS adds functionality)
      const copyButton = h('button.copy-button', {
        'aria-label': 'Copy code',
        type: 'button'
      }, [
        h('span.copy-icon', 'Copy'),
        h('span.copied-icon', 'Copied!')
      ]);

      // Create collapse toggle if needed
      const collapseToggle = shouldCollapse ? h('button.collapse-toggle', {
        'aria-label': 'Toggle code visibility',
        type: 'button'
      }, [
        h('span.expand-text', `Expand (${lineCount} lines)`),
        h('span.collapse-text', 'Collapse')
      ]) : null;

      // Create fade overlay for collapsed blocks
      const fadeOverlay = shouldCollapse ?
        h('div.code-fade', { 'aria-hidden': 'true' }) : null;

      // Build container children
      const containerChildren = [
        copyButton,
        collapseToggle,
        h('div.code-content', [node]),
        fadeOverlay
      ].filter(Boolean);

      // Create container
      const container = h('div', {
        className: containerClasses,
        'data-language': language,
        'data-line-count': String(lineCount),
        'data-max-preview': String(PREVIEW_LINES),
        'data-github-url': githubUrl || undefined
      }, containerChildren);

      // Create SEO-friendly footer link for GitHub (crawlers love explicit links)
      const githubFooter = githubInfo ? h('div.code-block-footer', [
        h('a.github-source-link', {
          href: githubInfo.url,
          target: '_blank',
          rel: 'noopener noreferrer'
        }, [
          h('span.github-arrow', '→'),
          h('span', ` View full source: ${githubInfo.displayText}`)
        ])
      ]) : null;

      // Wrap in outer wrapper
      const wrapper = h('div.code-block-wrapper', {
        'data-line-count': String(lineCount),
        'data-has-github': githubInfo ? 'true' : undefined
      }, [
        ...headerChildren,
        container,
        githubFooter
      ].filter(Boolean));

      // Replace the original pre with our wrapper
      parent.children[index] = wrapper;
    });
  };
}

/**
 * Extract text content from a hast node
 */
function getTextContent(node) {
  if (node.type === 'text') {
    return node.value;
  }
  if (node.children) {
    return node.children.map(getTextContent).join('');
  }
  return '';
}
