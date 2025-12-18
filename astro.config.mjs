import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://blog.amenoacids.com",
  vite: {
    plugins: [tailwindcss()],
  },
});
