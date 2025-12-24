import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import rehypeMermaid from "rehype-mermaid";
import rehypeCodeBlocks from "./scripts/rehype-code-blocks.mjs";
import mdx from "@astrojs/mdx";

export default defineConfig({
  site: "https://blog.amenoacids.com",
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
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
