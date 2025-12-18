# Tailwind CSS v4 with Astro (2025)

## Important: Use Vite Plugin (NOT @astrojs/tailwind)

The `@astrojs/tailwind` integration is deprecated. Use `@tailwindcss/vite` instead.

## Setup

### 1. Install Dependencies
```bash
npm install tailwindcss @tailwindcss/vite
```

### 2. Configure Astro (astro.config.mjs)
```js
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
});
```

### 3. Create Global CSS (src/styles/global.css)
```css
@import "tailwindcss";

/* Custom theme tokens */
@theme {
  --font-family-mono: "JetBrains Mono", monospace;
  --color-background: #fff;
  --color-text: #000;
}
```

### 4. Import in Layout
```astro
---
import '../styles/global.css';
---
```

## Tailwind v4 Changes

- CSS-first configuration
- Define tokens with `@theme`
- Add plugins via `@plugin`
- Import with `@import "tailwindcss"`
