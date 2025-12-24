# Typefully API v2 Reference

API documentation for Typefully integration in ACIDBATH multi-channel publishing.

## Overview

Typefully is a social media scheduling and publishing platform that provides a unified API for posting to multiple social platforms.

**Base URL**: `https://api.typefully.com`

**Supported Platforms**:
- X (Twitter) - posts and threads
- LinkedIn - professional posts
- Bluesky - decentralized social
- Threads - Meta's Twitter alternative
- Mastodon - Fediverse publishing

## Authentication

All requests require a Bearer token:

```
Authorization: Bearer YOUR_API_KEY
```

Generate your API key from Typefully Settings > API.

**Note**: API access requires Typefully Pro subscription.

## Endpoints

### User

#### Get Current User
```
GET /v2/me
```

Returns the authenticated user's profile.

**Response**:
```json
{
  "id": 12345,
  "email": "user@example.com",
  "name": "John Doe"
}
```

### Social Sets

A "social set" represents a connected social media account or group of accounts.

#### List Social Sets
```
GET /v2/social-sets
```

**Query Parameters**:
- `limit` (int, max 50): Items per page
- `offset` (int): Items to skip

**Response**:
```json
{
  "results": [
    {
      "id": 67890,
      "username": "acidbath",
      "name": "ACIDBATH",
      "profile_image_url": "https://...",
      "team": null
    }
  ],
  "count": 1,
  "limit": 10,
  "offset": 0,
  "next": null,
  "previous": null
}
```

#### Get Social Set Details
```
GET /v2/social-sets/{social_set_id}/
```

Returns configured platforms (X, LinkedIn, Bluesky, etc.) for the social set.

### Drafts

#### List Drafts
```
GET /v2/social-sets/{social_set_id}/drafts
```

**Query Parameters**:
- `status`: `draft` | `published` | `scheduled` | `error` | `publishing`
- `tag`: Filter by tag slug(s)
- `order_by`: `created_at` | `-created_at` | `updated_at` | `-updated_at` | `scheduled_date` | `-scheduled_date` | `published_at` | `-published_at`
- `limit`, `offset`: Pagination

#### Create Draft
```
POST /v2/social-sets/{social_set_id}/drafts
```

**Request Body**:
```json
{
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [
        {"text": "First tweet of thread"},
        {"text": "Second tweet..."}
      ]
    },
    "linkedin": {
      "enabled": true,
      "posts": [
        {"text": "LinkedIn post content (up to 3000 chars)"}
      ]
    },
    "bluesky": {
      "enabled": true,
      "posts": [
        {"text": "Bluesky post (300 chars max)"}
      ]
    },
    "threads": {
      "enabled": true,
      "posts": [
        {"text": "Threads post (500 chars)"}
      ]
    },
    "mastodon": {
      "enabled": true,
      "posts": [
        {"text": "Mastodon toot (500 chars default)"}
      ]
    }
  },
  "draft_title": "Blog Post Promotion",
  "tags": ["blog", "promotion"],
  "share": false,
  "publish_at": "now"
}
```

**`publish_at` Options**:
- `null` - Save as draft only
- `"now"` - Publish immediately
- `"next-free-slot"` - Use Typefully's smart scheduling
- ISO 8601 datetime - Schedule for specific time: `"2025-01-20T14:00:00Z"`

**Response**:
```json
{
  "id": 12345,
  "social_set_id": 67890,
  "status": "scheduled",
  "scheduled_date": "2025-01-20T14:00:00Z",
  "private_url": "https://typefully.com/?d=12345&a=67890",
  "share_url": null,
  "platforms": {...}
}
```

#### Update Draft
```
PATCH /v2/social-sets/{social_set_id}/drafts/{draft_id}
```

Same body format as create. Cannot update published drafts.

#### Delete Draft
```
DELETE /v2/social-sets/{social_set_id}/drafts/{draft_id}
```

#### Publish Draft
```
POST /v2/social-sets/{social_set_id}/drafts/{draft_id}/publish
```

Immediately publishes a draft to all enabled platforms.

### Tags

#### List Tags
```
GET /v2/social-sets/{social_set_id}/tags
```

#### Create Tag
```
POST /v2/social-sets/{social_set_id}/tags
```

**Request Body**:
```json
{
  "name": "Blog Posts"
}
```

### Media

#### Upload Media
```
POST /v2/social-sets/{social_set_id}/media
```

Upload images/videos. Returns `media_id` to use in posts.

## Platform Content Formats

### X (Twitter)

```json
{
  "x": {
    "enabled": true,
    "posts": [
      {"text": "Tweet 1 (280 chars max)", "media_ids": ["uuid1"]},
      {"text": "Tweet 2 of thread"}
    ],
    "settings": {
      "reply_to_url": "https://x.com/user/status/123"
    }
  }
}
```

- Max 25 posts per thread
- 280 characters per tweet
- Optional: reply to existing tweet

### LinkedIn

```json
{
  "linkedin": {
    "enabled": true,
    "posts": [
      {"text": "Post content (up to 3000 chars)"}
    ]
  }
}
```

- Single post only (no threads)
- Up to 3000 characters

### Bluesky

```json
{
  "bluesky": {
    "enabled": true,
    "posts": [
      {"text": "Bluesky post (300 chars)"}
    ]
  }
}
```

- 300 character limit per post
- Max 25 posts in thread

### Threads

```json
{
  "threads": {
    "enabled": true,
    "posts": [
      {"text": "Threads post (500 chars)"}
    ]
  }
}
```

- 500 character limit
- Max 25 posts in thread

### Mastodon

```json
{
  "mastodon": {
    "enabled": true,
    "posts": [
      {"text": "Mastodon toot (500 chars default, instance-specific)"}
    ]
  }
}
```

- 500 character default (varies by instance)
- Max 25 posts in thread

## Draft Status Values

| Status | Description |
|--------|-------------|
| `draft` | Saved but not scheduled |
| `scheduled` | Queued for publishing |
| `publishing` | Currently being posted |
| `published` | Successfully posted to all platforms |
| `error` | Publishing failed |

## Response Fields for Published Drafts

After publishing, the response includes:

```json
{
  "status": "published",
  "published_at": "2025-01-20T14:00:05Z",
  "x_published_url": "https://x.com/username/status/123",
  "x_post_published_at": "2025-01-20T14:00:05Z",
  "linkedin_published_url": "https://linkedin.com/feed/update/urn:li:share:123",
  "linkedin_post_published_at": "2025-01-20T14:00:08Z",
  "bluesky_published_url": "https://bsky.app/profile/user.bsky.social/post/abc",
  "bluesky_post_published_at": "2025-01-20T14:00:10Z",
  "threads_published_url": "https://threads.net/@user/post/ABC",
  "threads_post_published_at": "2025-01-20T14:00:12Z",
  "mastodon_published_url": "https://mastodon.social/@user/123",
  "mastodon_post_published_at": "2025-01-20T14:00:15Z"
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [
      {
        "field": "platforms.x.posts.0.text",
        "message": "Must not be empty."
      }
    ]
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing API key |
| `FORBIDDEN` | 403 | No permission for this action |
| `INSUFFICIENT_ACCESS_LEVEL` | 403 | Need higher access level |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `VALIDATION_ERROR` | 400/422 | Invalid request data |
| `MONETIZATION_ERROR` | 402 | Requires paid plan |
| `RATE_LIMITED` | 429 | Too many requests |

## Rate Limiting

- Rate limits apply per-user and per-social-set
- When exceeded, receive `429 Too Many Requests`
- Use exponential backoff for retries
- Check `Retry-After` header when available

## Best Practices

1. **Use tags** to organize drafts by content type (blog, promotion, etc.)
2. **Prefer `next-free-slot`** for auto-scheduling to optimal times
3. **Create drafts first**, then publish - allows preview in Typefully UI
4. **Handle partial failures** - some platforms may succeed while others fail
5. **Store draft IDs** to track publishing status

## Example: Publish Blog Post to All Platforms

```python
import httpx

client = httpx.Client(
    base_url="https://api.typefully.com",
    headers={"Authorization": f"Bearer {api_key}"}
)

# Create and immediately publish
response = client.post(
    f"/v2/social-sets/{social_set_id}/drafts",
    json={
        "platforms": {
            "x": {
                "enabled": True,
                "posts": [
                    {"text": "New blog post: Context Engineering Deep Dive"},
                    {"text": "Key insight: Progressive disclosure cuts token usage 95%"},
                    {"text": "Full post: https://blog.example.com/context-engineering"}
                ]
            },
            "linkedin": {
                "enabled": True,
                "posts": [{"text": "I wrote about context engineering..."}]
            },
            "bluesky": {
                "enabled": True,
                "posts": [{"text": "New post on context engineering!"}]
            }
        },
        "draft_title": "Context Engineering Blog Post",
        "tags": ["blog"],
        "publish_at": "now"
    }
)

draft = response.json()
print(f"Published to X: {draft.get('x_published_url')}")
print(f"Published to LinkedIn: {draft.get('linkedin_published_url')}")
```

## Comparison: Typefully vs Direct APIs

| Aspect | Typefully | Direct Platform APIs |
|--------|-----------|---------------------|
| Auth | Single API key | OAuth per platform |
| Rate limits | Managed by Typefully | Per-platform limits |
| Thread support | Built-in | Manual implementation |
| Scheduling | Smart scheduling | Custom cron logic |
| Analytics | Included | Separate integration |
| Maintenance | Typefully handles | You maintain |
| Cost | Pro subscription | Free (with limits) |
