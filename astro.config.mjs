import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import rehypeMermaid from "rehype-mermaid";

export default defineConfig({
  site: "https://blog.amenoacids.com",
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
    rehypePlugins: [[rehypeMermaid, { strategy: "pre-mermaid" }]],
  },
});
