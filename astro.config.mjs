import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import rehypeMermaid from "rehype-mermaid";

export default defineConfig({
  site: "https://blog.amenoacids.com",
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    syntaxHighlight: {
      type: "shiki",
      excludeLangs: ["mermaid"],
    },
    rehypePlugins: [[rehypeMermaid, { strategy: "pre-mermaid" }]],
  },
});
