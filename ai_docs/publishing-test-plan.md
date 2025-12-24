# Multi-Channel Publishing Test Plan

Simplified test plan for Typefully + RSS architecture.

## Architecture Overview

```
Blog Post → RSS Feed → dev.to, Hashnode, Buttondown (automatic)
         → /extract-content → Typefully → X, LinkedIn, Bluesky, Threads, Mastodon
```

**Only 2 API keys required:**
- `TYPEFULLY_API_KEY`
- `TYPEFULLY_SOCIAL_SET_ID`

---

## Environment Variables

### Required

| Variable | Description | How to Get |
|----------|-------------|------------|
| `TYPEFULLY_API_KEY` | API authentication | Typefully > Settings > API |
| `TYPEFULLY_SOCIAL_SET_ID` | Your account ID | See discovery command below |

### Discovery Command

```bash
# Get your social set ID
curl -s -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  https://api.typefully.com/v2/social-sets | jq '.results[0].id'
```

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `PUBLISH_MODE` | `staged` | `auto`, `staged`, or `dry-run` |
| `CANONICAL_URL_BASE` | - | Your blog's base URL |

---

## Test Plan

### Phase 1: Environment Validation

#### 1.1 Check Environment Variables

```bash
#!/bin/bash
echo "=== Typefully Configuration ==="
if [ -z "$TYPEFULLY_API_KEY" ]; then
    echo "❌ TYPEFULLY_API_KEY not set"
else
    echo "✓ TYPEFULLY_API_KEY is set"
fi

if [ -z "$TYPEFULLY_SOCIAL_SET_ID" ]; then
    echo "❌ TYPEFULLY_SOCIAL_SET_ID not set"
else
    echo "✓ TYPEFULLY_SOCIAL_SET_ID is set"
fi
```

#### 1.2 Test Typefully API Connection

```bash
# Test authentication
curl -s -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  https://api.typefully.com/v2/me | jq '.'

# Expected output:
# {
#   "id": 12345,
#   "email": "you@example.com",
#   "name": "Your Name"
# }
```

#### 1.3 Test Social Set Access

```bash
# Get social set details
curl -s -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/" | jq '.username'

# Expected: Your Twitter/X username
```

#### 1.4 Python Module Test

```bash
# Test Python client
uv run python adws/adw_modules/typefully_ops.py --test

# Expected output:
# ✓ Connected as: Your Name
# ✓ Social set: @yourusername
# ✓ Platforms: x, linkedin, bluesky, threads, mastodon
```

---

### Phase 2: RSS Feed Verification

#### 2.1 Check RSS Feed Exists

```bash
# Verify feed is accessible
curl -s -o /dev/null -w "%{http_code}" https://blog.amenoacids.com/rss.xml

# Expected: 200
```

#### 2.2 Validate RSS Format

```bash
# Check XML validity
curl -s https://blog.amenoacids.com/rss.xml | xmllint --noout - && echo "✓ Valid RSS XML"

# Expected: ✓ Valid RSS XML
```

#### 2.3 Check Feed Content

```bash
# View latest posts in feed
curl -s https://blog.amenoacids.com/rss.xml | grep -o '<title>[^<]*</title>' | head -5

# Expected: List of recent post titles
```

#### 2.4 Verify Canonical URLs

```bash
# Check that links are absolute URLs
curl -s https://blog.amenoacids.com/rss.xml | grep '<link>' | head -3

# Expected: Full URLs like https://blog.amenoacids.com/blog/post-slug/
```

---

### Phase 3: Content Extraction Test

#### 3.1 Run Extract-Content Command

```bash
# Extract content from a blog post
/extract-content src/content/blog/context-engineering.md
```

#### 3.2 Verify Output Files

```bash
# Check output directory
ls -la content/derivatives/context-engineering/

# Expected files:
# - twitter-thread.md
# - linkedin-post.md
# - bluesky-post.md
# - threads-post.md
# - mastodon-post.md
# - typefully-content.json
# - metadata.json
```

#### 3.3 Validate Typefully Content

```bash
# Check typefully-content.json structure
cat content/derivatives/context-engineering/typefully-content.json | jq 'keys'

# Expected: ["draft_title", "platforms", "tags"]

# Check platforms are configured
cat content/derivatives/context-engineering/typefully-content.json | jq '.platforms | keys'

# Expected: ["bluesky", "linkedin", "mastodon", "threads", "x"]
```

---

### Phase 4: Typefully Integration Test

#### 4.1 Create Test Draft (Not Published)

```bash
uv run python -c "
from adws.adw_modules.typefully_ops import TypefullyClient, TypefullyConfig

config = TypefullyConfig.from_env()
client = TypefullyClient(config)

# Create draft without publishing
result = client.create_draft(
    platforms={
        'x': {'enabled': True, 'posts': [{'text': '[TEST] Integration test - delete me'}]},
    },
    draft_title='[TEST] Delete this draft',
    publish_at=None  # Save as draft only
)

print(f'✓ Draft created: {result.private_url}')
print(f'✓ Draft ID: {result.id}')
print(f'✓ Status: {result.status}')
print()
print('ACTION: Go to Typefully and delete this test draft')
"
```

#### 4.2 Multi-Platform Draft Test

```bash
uv run python -c "
from adws.adw_modules.typefully_ops import TypefullyClient, TypefullyConfig

config = TypefullyConfig.from_env()
client = TypefullyClient(config)

# Create multi-platform draft
result = client.create_draft(
    platforms={
        'x': {
            'enabled': True,
            'posts': [
                {'text': '[TEST] Multi-platform test - Part 1'},
                {'text': '[TEST] Part 2 - delete this thread'},
            ]
        },
        'linkedin': {
            'enabled': True,
            'posts': [{'text': '[TEST] LinkedIn integration test. Please delete.'}]
        },
        'bluesky': {
            'enabled': True,
            'posts': [{'text': '[TEST] Bluesky integration test'}]
        },
    },
    draft_title='[TEST] Multi-platform integration test',
    tags=['test'],
    publish_at=None
)

print(f'✓ Multi-platform draft created')
print(f'✓ URL: {result.private_url}')
print(f'✓ Platforms: x (thread), linkedin, bluesky')
print()
print('ACTION: Review in Typefully UI, then delete')
"
```

#### 4.3 List Drafts Test

```bash
uv run python adws/adw_modules/typefully_ops.py --list-drafts

# Expected: List of your recent drafts
```

---

### Phase 5: End-to-End Test

#### 5.1 Full Workflow (Dry Run)

```bash
# 1. Extract content
/extract-content src/content/blog/context-engineering.md

# 2. Review generated content
cat content/derivatives/context-engineering/typefully-content.json | jq '.platforms.x.posts'

# 3. Create Typefully draft (dry run - not published)
uv run python -c "
import json
from adws.adw_modules.typefully_ops import TypefullyClient, TypefullyConfig

# Load extracted content
with open('content/derivatives/context-engineering/typefully-content.json') as f:
    content = json.load(f)

config = TypefullyConfig.from_env()
client = TypefullyClient(config)

# Create draft without publishing
result = client.create_draft(
    platforms=content['platforms'],
    draft_title=content.get('draft_title', 'Blog Post'),
    tags=content.get('tags', []),
    publish_at=None  # Draft only
)

print(f'✓ Draft created from extracted content')
print(f'✓ URL: {result.private_url}')
print(f'✓ Review in Typefully before publishing')
"
```

#### 5.2 Production Publish Test

**WARNING**: This will actually publish to your social accounts!

```bash
# Only run when ready to publish for real
uv run python -c "
from adws.adw_modules.typefully_ops import TypefullyClient, TypefullyConfig

config = TypefullyConfig.from_env()
client = TypefullyClient(config)

# Publish immediately
result = client.create_draft(
    platforms={
        'x': {'enabled': True, 'posts': [{'text': 'Hello from ACIDBATH! Testing new publishing pipeline.'}]},
    },
    draft_title='Production test',
    publish_at='now'  # PUBLISH IMMEDIATELY
)

print(f'✓ Published!')
print(f'✓ X URL: {result.x_published_url}')
"
```

---

## Troubleshooting

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `TYPEFULLY_API_KEY not set` | Missing env var | Export variable or add to .env |
| `401 Unauthorized` | Invalid API key | Regenerate in Typefully settings |
| `Social set not found` | Wrong ID | Run discovery command above |
| `429 Rate Limited` | Too many requests | Wait and retry |
| `MONETIZATION_ERROR` | Need Pro plan | Upgrade Typefully subscription |

### API Error Codes

| Code | Meaning |
|------|---------|
| `UNAUTHORIZED` | Invalid API key |
| `FORBIDDEN` | No permission for action |
| `NOT_FOUND` | Resource doesn't exist |
| `VALIDATION_ERROR` | Invalid request data |
| `RATE_LIMITED` | Too many requests |

---

## Validation Checklist

### Pre-Launch

- [ ] `TYPEFULLY_API_KEY` is set
- [ ] `TYPEFULLY_SOCIAL_SET_ID` is set
- [ ] Python module imports successfully
- [ ] API connection test passes
- [ ] RSS feed is valid and accessible
- [ ] Test draft creation works
- [ ] Test draft deletion works

### Post-Launch

- [ ] RSS platforms configured (dev.to, Hashnode, Buttondown)
- [ ] First real post published successfully
- [ ] All platform URLs verified
- [ ] Analytics tracking confirmed

---

## Quick Commands

```bash
# Validate environment
echo "API Key: ${TYPEFULLY_API_KEY:0:10}..." && echo "Social Set: $TYPEFULLY_SOCIAL_SET_ID"

# Test API
curl -s -H "Authorization: Bearer $TYPEFULLY_API_KEY" https://api.typefully.com/v2/me | jq '.name'

# Test Python module
uv run python adws/adw_modules/typefully_ops.py --test

# Check RSS feed
curl -s https://blog.amenoacids.com/rss.xml | xmllint --noout - && echo "✓ RSS OK"
```
