# The Monospace Web - Design System

By Oskar Wickström (MIT License)

## Design Philosophy
- Monospace-first typography with JetBrains Mono
- Line-height-based vertical rhythm system
- Character-based grid alignment
- Dark/light mode support

## CSS Variables
```css
:root {
  --font-family: "JetBrains Mono", monospace;
  --line-height: 1.20rem;
  --border-thickness: 2px;
  --text-color: #000;
  --text-color-alt: #666;
  --background-color: #fff;
  --background-color-alt: #eee;
  --font-weight-normal: 500;
  --font-weight-medium: 600;
  --font-weight-bold: 800;
}

@media (prefers-color-scheme: dark) {
  :root {
    --text-color: #fff;
    --text-color-alt: #aaa;
    --background-color: #000;
    --background-color-alt: #111;
  }
}
```

## Key Patterns

### Typography
- Font size: 16px (14px on mobile <480px)
- Tabular and lining numerals for alignment
- Headings: uppercase, bold weight

### Layout
- Body max-width: 80ch
- Padding: 2ch (1ch on mobile)
- Sibling spacing: `* + * { margin-top: var(--line-height) }`

### Components
- Tables: border-collapse with calculated padding
- Details/Summary: custom markers (▶/▼)
- Forms: consistent height (2 * line-height)
- Lists: tree structure visualization
- Grid: auto-detecting columns via :has()

## Complete CSS
See: https://github.com/owickstrom/the-monospace-web/blob/main/src/index.css
