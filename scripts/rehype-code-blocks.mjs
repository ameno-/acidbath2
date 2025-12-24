/**
 * Rehype plugin to enhance code blocks with SSR structure
 *
 * Adds:
 * - Container wrapper with line count data
 * - Collapsible class for blocks > 15 lines
 * - Line numbers class
 * - Language detection from code class
 *
 * This enables:
 * - No layout shift (structure rendered SSR)
 * - SEO-friendly semantic HTML
 * - JS only handles interactivity
 */

import { visit } from 'unist-util-visit';
import { h } from 'hastscript';

const COLLAPSE_THRESHOLD = 15;
const PREVIEW_LINES = 8;

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

      // Determine if should collapse
      const shouldCollapse = lineCount > COLLAPSE_THRESHOLD;

      // Build container classes
      const containerClasses = ['code-block-container'];
      if (shouldCollapse) containerClasses.push('collapsible');
      containerClasses.push('with-line-numbers');

      // Create header if language exists
      const headerChildren = [];
      if (language) {
        headerChildren.push(
          h('div.code-block-header', [
            h('span.code-block-label', language.toUpperCase()),
            h('span.language-badge', language)
          ])
        );
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
        'data-max-preview': String(PREVIEW_LINES)
      }, containerChildren);

      // Wrap in outer wrapper
      const wrapper = h('div.code-block-wrapper', {
        'data-line-count': String(lineCount)
      }, [
        ...headerChildren,
        container
      ]);

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
