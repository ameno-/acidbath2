# Astro Blog Tutorial

## Project Structure
```
src/
├── pages/
│   ├── index.astro (Home)
│   ├── about.astro
│   ├── blog.astro
│   └── posts/
│       ├── post-1.md
│       ├── post-2.md
│       └── post-3.md
├── components/
├── layouts/
│   ├── BaseLayout.astro
│   └── MarkdownPostLayout.astro
└── styles/
    └── global.css
```

## Base Layout Pattern
```astro
---
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';
import '../styles/global.css';
const { pageTitle } = Astro.props;
---
<html lang="en">
  <head>
    <title>{pageTitle}</title>
  </head>
  <body>
    <Header />
    <h1>{pageTitle}</h1>
    <slot />
    <Footer />
  </body>
</html>
```

## Markdown Post Layout
```astro
---
import BaseLayout from './BaseLayout.astro';
const { frontmatter } = Astro.props;
---
<BaseLayout pageTitle={frontmatter.title}>
  <p>Published: {frontmatter.pubDate.toString().slice(0,10)}</p>
  <p>By: {frontmatter.author}</p>
  <img src={frontmatter.image.url} alt={frontmatter.image.alt} />
  <slot />
</BaseLayout>
```

## Dynamic Page Generation (Tags)
```astro
---
export async function getStaticPaths() {
  const allPosts = Object.values(
    import.meta.glob('../posts/*.md', { eager: true })
  );
  const uniqueTags = [
    ...new Set(allPosts.map((post: any) => post.frontmatter.tags).flat())
  ];

  return uniqueTags.map((tag) => {
    const filteredPosts = allPosts.filter((post: any) =>
      post.frontmatter.tags.includes(tag)
    );
    return {
      params: { tag },
      props: { posts: filteredPosts }
    };
  });
}
---
```

## Content Collections (Recommended for TypeScript)
Use `src/content/` directory with schema validation for type-safe content.
