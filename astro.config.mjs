import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import rehypeMermaid from "rehype-mermaid";
import rehypeCodeBlocks from "./scripts/rehype-code-blocks.mjs";
import mdx from "@astrojs/mdx";
import react from "@astrojs/react";
import expressiveCode from "astro-expressive-code";
import { pluginCollapsibleSections } from "@expressive-code/plugin-collapsible-sections";

export default defineConfig({
  site: "https://blog.amenoacids.com",
  integrations: [
    expressiveCode({
      themes: ["github-dark", "github-light"],
      plugins: [pluginCollapsibleSections()],
      styleOverrides: {
        borderRadius: "0.5rem",
        uiFontFamily: "var(--font-family-sans)",
        codeFontFamily: "var(--font-family-mono)",
        borderColor: "var(--color-foreground-alt)",
        frames: {
          editorActiveTabIndicatorTopColor: "var(--color-accent-primary)",
          editorTabBarBackgroundColor: "var(--color-background-alt)",
        },
      },
    }),
    mdx(),
    react(),
  ],
  server: {
    port: process.env.WORKTREE_PORT_1 ? parseInt(process.env.WORKTREE_PORT_1) : 9103,
  },
  vite: {
    plugins: [tailwindcss()],
    server: {
      port: process.env.WORKTREE_PORT_2 ? parseInt(process.env.WORKTREE_PORT_2) : 9203,
    },
  },
  markdown: {
    syntaxHighlight: {
      type: "shiki",
      excludeLangs: ["mermaid"],
    },
    rehypePlugins: [
      rehypeCodeBlocks,
      [rehypeMermaid, { strategy: "pre-mermaid" }]
    ],
  },
});