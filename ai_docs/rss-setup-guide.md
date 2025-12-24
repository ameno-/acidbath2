# RSS Platform Setup Guide

One-time setup instructions for RSS-based content syndication.

## Overview

Your blog's RSS feed automatically syndicates content to developer communities and newsletters without requiring API integrations. This guide covers the one-time setup for each platform.

**Your RSS Feed URL**: `https://blog.amenoacids.com/rss.xml`

## Platform Setup

### dev.to

dev.to can automatically import your blog posts as drafts, preserving your canonical URL for SEO.

#### Setup Steps

1. Go to [dev.to Settings > Extensions](https://dev.to/settings/extensions)
2. Scroll to **"Publishing to DEV from RSS"**
3. Enter your RSS feed URL: `https://blog.amenoacids.com/rss.xml`
4. Click **Save**

#### Configuration Options

| Option | Recommended Setting |
|--------|---------------------|
| Fetch articles from RSS | Enabled |
| Mark as canonical | Enabled (preserves SEO) |
| Import as drafts | Enabled (review before publishing) |

#### Verification

After setup, new blog posts will appear in your dev.to dashboard as drafts within 24 hours.

```bash
# Check your dev.to drafts
# Go to: https://dev.to/dashboard
```

#### Notes
- dev.to checks RSS feeds approximately every 24 hours
- Canonical URL is automatically set to your original blog post
- You can edit formatting before publishing the draft
- Tags from your RSS feed may need manual adjustment

---

### Hashnode

Hashnode supports RSS import to automatically create posts on your Hashnode publication.

#### Setup Steps

1. Go to your [Hashnode Dashboard](https://hashnode.com/dashboard)
2. Select your publication
3. Navigate to **Import** (in the sidebar)
4. Click **"Import from RSS"**
5. Enter your RSS feed URL: `https://blog.amenoacids.com/rss.xml`
6. Select import options:
   - Import as drafts (recommended)
   - Set canonical URL (enabled)
7. Click **Import**

#### Configuration Options

| Option | Recommended Setting |
|--------|---------------------|
| Import as | Drafts |
| Set canonical URL | Yes |
| Override if exists | No |

#### Verification

Check your Hashnode publication's drafts section for imported posts.

```bash
# Hashnode doesn't have a public API endpoint for drafts
# Check manually at: https://hashnode.com/draft
```

#### Notes
- Hashnode import is manual (not automatic polling)
- Re-run import periodically or when you publish new posts
- Consider using Hashnode's GitHub integration as an alternative
- Tags need to be added manually after import

---

### Buttondown (Newsletter)

Buttondown can automatically send RSS digest emails to your subscribers.

#### Setup Steps

1. Go to [Buttondown Settings](https://buttondown.email/settings)
2. Navigate to **Automations** or **RSS** section
3. Click **"Add RSS Feed"**
4. Enter your RSS feed URL: `https://blog.amenoacids.com/rss.xml`
5. Configure digest settings:
   - Frequency: Weekly (recommended)
   - Day: Sunday
   - Include full content or excerpt

#### Configuration Options

| Option | Recommended Setting |
|--------|---------------------|
| Frequency | Weekly |
| Send day | Sunday |
| Content | Excerpt with link |
| Subject line | "This Week on ACIDBATH" |

#### Verification

```bash
# Test your RSS feed is valid
curl -s https://blog.amenoacids.com/rss.xml | xmllint --noout - && echo "✓ Valid RSS"
```

Send a test digest to yourself before enabling for all subscribers.

#### Notes
- Subscribers receive automatic updates without any API integration
- You can still send manual newsletters for special announcements
- Digest emails include all new posts since the last digest
- Customize email template in Buttondown settings

---

## RSS Feed Verification

### Check Feed Validity

```bash
# Verify RSS feed is valid XML
curl -s https://blog.amenoacids.com/rss.xml | xmllint --noout - && echo "✓ Valid RSS"

# View latest items in feed
curl -s https://blog.amenoacids.com/rss.xml | grep -o '<title>[^<]*</title>' | head -10

# Check feed with online validator
# https://validator.w3.org/feed/check.cgi?url=https://blog.amenoacids.com/rss.xml
```

### Check Feed Content

```bash
# View full feed structure
curl -s https://blog.amenoacids.com/rss.xml | head -100

# Count items in feed
curl -s https://blog.amenoacids.com/rss.xml | grep -c '<item>'
```

### Astro RSS Configuration

Your Astro blog should have RSS configured in `astro.config.mjs`:

```javascript
import rss from '@astrojs/rss';

export async function GET(context) {
  return rss({
    title: 'ACIDBATH',
    description: 'AI Engineering Blog',
    site: context.site,
    items: await getCollection('blog').then(posts =>
      posts.map(post => ({
        title: post.data.title,
        pubDate: post.data.publishedDate,
        description: post.data.description,
        link: `/blog/${post.slug}/`,
      }))
    ),
  });
}
```

---

## Troubleshooting

### Feed Not Updating

| Symptom | Cause | Fix |
|---------|-------|-----|
| No new posts in feed | Build not deployed | Check Cloudflare Pages deployment |
| Old posts showing | Cache issue | Clear CDN cache or wait |
| Feed 404 | RSS not configured | Check `src/pages/rss.xml.js` exists |

### Import Not Working

| Platform | Issue | Fix |
|----------|-------|-----|
| dev.to | Posts not importing | Check feed URL in settings, wait 24h |
| Hashnode | Import fails | Try manual import, check feed validity |
| Buttondown | No digests sent | Check automation settings, verify subscribers exist |

### Canonical URL Issues

Ensure your RSS feed includes the full canonical URL for each post:

```xml
<item>
  <title>Post Title</title>
  <link>https://blog.amenoacids.com/blog/post-slug/</link>
  <!-- This link becomes the canonical URL -->
</item>
```

---

## Platform Comparison

| Feature | dev.to | Hashnode | Buttondown |
|---------|--------|----------|------------|
| Auto-polling | ✅ Every 24h | ❌ Manual | ✅ Configurable |
| Canonical URL | ✅ Automatic | ✅ Automatic | N/A |
| Draft mode | ✅ Optional | ✅ Optional | N/A |
| Tag import | ⚠️ Partial | ❌ Manual | N/A |
| Formatting | ⚠️ May need fixes | ✅ Good | ✅ Good |

---

## Maintenance

### Regular Tasks

| Task | Frequency | Description |
|------|-----------|-------------|
| Check dev.to drafts | After each post | Review and publish imported drafts |
| Run Hashnode import | After each post | Manually trigger RSS import |
| Review digest stats | Weekly | Check Buttondown analytics |

### After Publishing a New Blog Post

1. **Wait 24 hours** for dev.to auto-import
2. **Manually trigger** Hashnode RSS import
3. **Buttondown** will include in next scheduled digest
4. **Use Typefully** for immediate social media posting (see main workflow)

---

## Quick Reference

| Platform | Setup URL | RSS Feature |
|----------|-----------|-------------|
| dev.to | [dev.to/settings/extensions](https://dev.to/settings/extensions) | Auto-import |
| Hashnode | [hashnode.com/dashboard](https://hashnode.com/dashboard) → Import | Manual import |
| Buttondown | [buttondown.email/settings](https://buttondown.email/settings) | RSS digest |

**Your RSS Feed**: `https://blog.amenoacids.com/rss.xml`
