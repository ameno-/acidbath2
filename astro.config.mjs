import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import rehypeMermaid from "rehype-mermaid";
import rehypeCodeBlocks from "./scripts/rehype-code-blocks.mjs";
import mdx from "@astrojs/mdx";

export default defineConfig({
  site: "https://blog.amenoacids.com",
  integrations: [mdx()],
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
