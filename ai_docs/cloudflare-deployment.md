# Cloudflare Pages Deployment Guide

## Installation

```bash
npm install wrangler@latest --save-dev
```

## Configuration (wrangler.jsonc)

For static sites:
```json
{
  "name": "acidbath",
  "compatibility_date": "2024-12-15",
  "pages_build_output_dir": "./dist"
}
```

## Commands

Preview locally:
```bash
npx astro build && wrangler pages dev ./dist
```

Deploy:
```bash
npx astro build && wrangler pages deploy ./dist
```

## CI/CD via GitHub

1. Log into Cloudflare dashboard
2. Navigate to Workers & Pages
3. Select Create > Pages tab
4. Connect your repository with:
   - Framework preset: `Astro`
   - Build command: `npm run build`
   - Build output directory: `dist`
