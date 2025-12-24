#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.27.0",
# ]
# ///
"""
Typefully API operations for multi-platform social media publishing.

Typefully provides a unified API for posting to:
- X (Twitter) - posts and threads
- LinkedIn - professional posts
- Bluesky - decentralized social
- Threads - Meta's Twitter alternative
- Mastodon - Fediverse publishing

Usage:
    from adw_modules.typefully_ops import TypefullyClient, TypefullyConfig

    config = TypefullyConfig.from_env()
    client = TypefullyClient(config)

    # Create and publish a draft
    draft = client.create_draft(
        platforms={
            "x": {"enabled": True, "posts": [{"text": "Hello world!"}]},
            "linkedin": {"enabled": True, "posts": [{"text": "Hello LinkedIn!"}]}
        },
        publish_at="now"
    )
"""

from __future__ import annotations

import os
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal
from enum import Enum

import httpx


class PublishMode(str, Enum):
    """When to publish the draft."""
    DRAFT = "draft"  # Save as draft only
    NOW = "now"  # Publish immediately
    NEXT_SLOT = "next-free-slot"  # Use Typefully's smart scheduling
    SCHEDULED = "scheduled"  # Schedule for specific time


class DraftStatus(str, Enum):
    """Status of a draft."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    ERROR = "error"


@dataclass
class TypefullyConfig:
    """Configuration for Typefully API client."""

    api_key: str
    social_set_id: int
    base_url: str = "https://api.typefully.com"
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "TypefullyConfig":
        """Create config from environment variables."""
        api_key = os.environ.get("TYPEFULLY_API_KEY")
        if not api_key:
            raise ValueError("TYPEFULLY_API_KEY environment variable not set")

        social_set_id = os.environ.get("TYPEFULLY_SOCIAL_SET_ID")
        if not social_set_id:
            raise ValueError("TYPEFULLY_SOCIAL_SET_ID environment variable not set")

        return cls(
            api_key=api_key,
            social_set_id=int(social_set_id),
            base_url=os.environ.get("TYPEFULLY_BASE_URL", "https://api.typefully.com"),
        )


@dataclass
class PlatformContent:
    """Content for a single platform."""

    enabled: bool = True
    posts: list[dict[str, Any]] = field(default_factory=list)
    settings: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "enabled": self.enabled,
            "posts": self.posts,
        }
        if self.settings:
            result["settings"] = self.settings
        return result


@dataclass
class DraftResult:
    """Result of a draft creation or update."""

    id: int
    social_set_id: int
    status: DraftStatus
    private_url: str
    share_url: str | None = None
    scheduled_date: datetime | None = None
    published_at: datetime | None = None

    # Platform-specific published URLs
    x_published_url: str | None = None
    linkedin_published_url: str | None = None
    bluesky_published_url: str | None = None
    threads_published_url: str | None = None
    mastodon_published_url: str | None = None

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "DraftResult":
        """Parse from API response."""
        return cls(
            id=data["id"],
            social_set_id=data["social_set_id"],
            status=DraftStatus(data["status"]),
            private_url=data["private_url"],
            share_url=data.get("share_url"),
            scheduled_date=_parse_datetime(data.get("scheduled_date")),
            published_at=_parse_datetime(data.get("published_at")),
            x_published_url=data.get("x_published_url"),
            linkedin_published_url=data.get("linkedin_published_url"),
            bluesky_published_url=data.get("bluesky_published_url"),
            threads_published_url=data.get("threads_published_url"),
            mastodon_published_url=data.get("mastodon_published_url"),
        )

    def get_published_urls(self) -> dict[str, str]:
        """Get all published URLs as a dict."""
        urls = {}
        if self.x_published_url:
            urls["x"] = self.x_published_url
        if self.linkedin_published_url:
            urls["linkedin"] = self.linkedin_published_url
        if self.bluesky_published_url:
            urls["bluesky"] = self.bluesky_published_url
        if self.threads_published_url:
            urls["threads"] = self.threads_published_url
        if self.mastodon_published_url:
            urls["mastodon"] = self.mastodon_published_url
        return urls


def _parse_datetime(value: str | None) -> datetime | None:
    """Parse ISO 8601 datetime string."""
    if not value:
        return None
    # Handle both Z and timezone offset formats
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


class TypefullyError(Exception):
    """Base exception for Typefully API errors."""

    def __init__(self, code: str, message: str, details: list[dict] | None = None):
        self.code = code
        self.message = message
        self.details = details or []
        super().__init__(f"{code}: {message}")


class TypefullyClient:
    """Client for Typefully API v2.

    Handles authentication, rate limiting, and error handling for
    Typefully's social media publishing API.
    """

    def __init__(self, config: TypefullyConfig):
        self.config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=config.timeout,
        )

    def __enter__(self) -> "TypefullyClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle API response and raise appropriate errors."""
        if response.status_code == 429:
            raise TypefullyError("RATE_LIMITED", "Rate limit exceeded. Try again later.")

        try:
            data = response.json()
        except json.JSONDecodeError:
            response.raise_for_status()
            return {}

        if not response.is_success:
            error = data.get("error", {})
            raise TypefullyError(
                code=error.get("code", "UNKNOWN"),
                message=error.get("message", response.text),
                details=error.get("details"),
            )

        return data

    # ========================================
    # User Endpoints
    # ========================================

    def get_me(self) -> dict[str, Any]:
        """Get the current authenticated user.

        Returns:
            User profile data including id, email, name.
        """
        response = self._client.get("/v2/me")
        return self._handle_response(response)

    # ========================================
    # Social Set Endpoints
    # ========================================

    def list_social_sets(self, limit: int = 10, offset: int = 0) -> dict[str, Any]:
        """List all social sets (accounts) accessible to the user.

        Args:
            limit: Max items per page (max 50)
            offset: Items to skip

        Returns:
            Paginated list of social sets.
        """
        response = self._client.get(
            "/v2/social-sets",
            params={"limit": min(limit, 50), "offset": offset},
        )
        return self._handle_response(response)

    def get_social_set(self, social_set_id: int | None = None) -> dict[str, Any]:
        """Get detailed info about a social set including connected platforms.

        Args:
            social_set_id: ID of social set (defaults to config.social_set_id)

        Returns:
            Social set details with platform configurations.
        """
        set_id = social_set_id or self.config.social_set_id
        response = self._client.get(f"/v2/social-sets/{set_id}/")
        return self._handle_response(response)

    # ========================================
    # Draft Endpoints
    # ========================================

    def list_drafts(
        self,
        status: DraftStatus | None = None,
        tags: list[str] | None = None,
        order_by: str = "-updated_at",
        limit: int = 10,
        offset: int = 0,
        social_set_id: int | None = None,
    ) -> dict[str, Any]:
        """List drafts for a social set.

        Args:
            status: Filter by draft status
            tags: Filter by tag slugs
            order_by: Sort order (created_at, -created_at, updated_at, etc.)
            limit: Max items per page
            offset: Items to skip
            social_set_id: Social set ID (defaults to config)

        Returns:
            Paginated list of drafts.
        """
        set_id = social_set_id or self.config.social_set_id
        params: dict[str, Any] = {
            "limit": min(limit, 50),
            "offset": offset,
            "order_by": order_by,
        }
        if status:
            params["status"] = status.value
        if tags:
            params["tag"] = tags

        response = self._client.get(f"/v2/social-sets/{set_id}/drafts", params=params)
        return self._handle_response(response)

    def create_draft(
        self,
        platforms: dict[str, dict[str, Any]],
        draft_title: str | None = None,
        tags: list[str] | None = None,
        share: bool = False,
        publish_at: str | datetime | None = None,
        social_set_id: int | None = None,
    ) -> DraftResult:
        """Create a new draft with platform-specific content.

        Args:
            platforms: Platform configurations, e.g.:
                {
                    "x": {"enabled": True, "posts": [{"text": "Tweet"}]},
                    "linkedin": {"enabled": True, "posts": [{"text": "Post"}]},
                }
            draft_title: Internal title for organization (not published)
            tags: List of tag slugs to apply
            share: Generate a public share URL
            publish_at: When to publish:
                - None: Save as draft
                - "now": Publish immediately
                - "next-free-slot": Use smart scheduling
                - datetime: Schedule for specific time
            social_set_id: Social set ID (defaults to config)

        Returns:
            DraftResult with draft ID, status, and URLs.
        """
        set_id = social_set_id or self.config.social_set_id

        body: dict[str, Any] = {"platforms": platforms}

        if draft_title:
            body["draft_title"] = draft_title
        if tags:
            body["tags"] = tags
        if share:
            body["share"] = True
        if publish_at:
            if isinstance(publish_at, datetime):
                body["publish_at"] = publish_at.isoformat()
            else:
                body["publish_at"] = publish_at

        response = self._client.post(f"/v2/social-sets/{set_id}/drafts", json=body)
        data = self._handle_response(response)
        return DraftResult.from_response(data)

    def get_draft(
        self,
        draft_id: int,
        social_set_id: int | None = None,
    ) -> DraftResult:
        """Get a draft by ID.

        Args:
            draft_id: The draft ID
            social_set_id: Social set ID (defaults to config)

        Returns:
            DraftResult with full draft details.
        """
        set_id = social_set_id or self.config.social_set_id
        response = self._client.get(f"/v2/social-sets/{set_id}/drafts/{draft_id}")
        data = self._handle_response(response)
        return DraftResult.from_response(data)

    def update_draft(
        self,
        draft_id: int,
        platforms: dict[str, dict[str, Any]] | None = None,
        draft_title: str | None = None,
        tags: list[str] | None = None,
        publish_at: str | datetime | None = None,
        social_set_id: int | None = None,
    ) -> DraftResult:
        """Update an existing draft.

        Cannot update published drafts.

        Args:
            draft_id: The draft ID to update
            platforms: New platform configurations
            draft_title: New title
            tags: New tags (replaces existing)
            publish_at: Schedule/publish options
            social_set_id: Social set ID (defaults to config)

        Returns:
            Updated DraftResult.
        """
        set_id = social_set_id or self.config.social_set_id

        body: dict[str, Any] = {}
        if platforms:
            body["platforms"] = platforms
        if draft_title is not None:
            body["draft_title"] = draft_title
        if tags is not None:
            body["tags"] = tags
        if publish_at:
            if isinstance(publish_at, datetime):
                body["publish_at"] = publish_at.isoformat()
            else:
                body["publish_at"] = publish_at

        response = self._client.patch(
            f"/v2/social-sets/{set_id}/drafts/{draft_id}",
            json=body,
        )
        data = self._handle_response(response)
        return DraftResult.from_response(data)

    def delete_draft(
        self,
        draft_id: int,
        social_set_id: int | None = None,
    ) -> None:
        """Delete a draft.

        Args:
            draft_id: The draft ID to delete
            social_set_id: Social set ID (defaults to config)
        """
        set_id = social_set_id or self.config.social_set_id
        response = self._client.delete(f"/v2/social-sets/{set_id}/drafts/{draft_id}")
        self._handle_response(response)

    def publish_draft(
        self,
        draft_id: int,
        social_set_id: int | None = None,
    ) -> DraftResult:
        """Immediately publish a draft to all enabled platforms.

        Args:
            draft_id: The draft ID to publish
            social_set_id: Social set ID (defaults to config)

        Returns:
            DraftResult with published URLs.
        """
        set_id = social_set_id or self.config.social_set_id
        response = self._client.post(
            f"/v2/social-sets/{set_id}/drafts/{draft_id}/publish"
        )
        data = self._handle_response(response)
        return DraftResult.from_response(data)

    # ========================================
    # Tag Endpoints
    # ========================================

    def list_tags(self, social_set_id: int | None = None) -> list[dict[str, Any]]:
        """List all tags for a social set.

        Args:
            social_set_id: Social set ID (defaults to config)

        Returns:
            List of tags with id, name, slug.
        """
        set_id = social_set_id or self.config.social_set_id
        response = self._client.get(f"/v2/social-sets/{set_id}/tags")
        data = self._handle_response(response)
        return data.get("results", [])

    def create_tag(
        self,
        name: str,
        social_set_id: int | None = None,
    ) -> dict[str, Any]:
        """Create a new tag.

        Args:
            name: Tag name (will be slugified)
            social_set_id: Social set ID (defaults to config)

        Returns:
            Created tag with id, name, slug.
        """
        set_id = social_set_id or self.config.social_set_id
        response = self._client.post(
            f"/v2/social-sets/{set_id}/tags",
            json={"name": name},
        )
        return self._handle_response(response)

    # ========================================
    # Convenience Methods
    # ========================================

    def publish_to_all_platforms(
        self,
        x_content: list[str] | None = None,
        linkedin_content: str | None = None,
        bluesky_content: str | None = None,
        threads_content: str | None = None,
        mastodon_content: str | None = None,
        draft_title: str | None = None,
        tags: list[str] | None = None,
        publish_now: bool = True,
    ) -> DraftResult:
        """Convenience method to publish content to multiple platforms at once.

        Args:
            x_content: List of tweets (for thread) or single tweet
            linkedin_content: LinkedIn post text
            bluesky_content: Bluesky post text
            threads_content: Threads post text
            mastodon_content: Mastodon post text
            draft_title: Internal title for organization
            tags: Tag slugs to apply
            publish_now: If True, publish immediately; if False, save as draft

        Returns:
            DraftResult with status and published URLs.
        """
        platforms: dict[str, dict[str, Any]] = {}

        if x_content:
            posts = [{"text": t} for t in x_content] if isinstance(x_content, list) else [{"text": x_content}]
            platforms["x"] = {"enabled": True, "posts": posts}

        if linkedin_content:
            platforms["linkedin"] = {"enabled": True, "posts": [{"text": linkedin_content}]}

        if bluesky_content:
            platforms["bluesky"] = {"enabled": True, "posts": [{"text": bluesky_content}]}

        if threads_content:
            platforms["threads"] = {"enabled": True, "posts": [{"text": threads_content}]}

        if mastodon_content:
            platforms["mastodon"] = {"enabled": True, "posts": [{"text": mastodon_content}]}

        if not platforms:
            raise ValueError("At least one platform content must be provided")

        return self.create_draft(
            platforms=platforms,
            draft_title=draft_title,
            tags=tags,
            publish_at="now" if publish_now else None,
        )


# ========================================
# CLI for testing
# ========================================

def main():
    """Test Typefully API connection."""
    import argparse

    parser = argparse.ArgumentParser(description="Test Typefully API")
    parser.add_argument("--test", action="store_true", help="Run connection test")
    parser.add_argument("--list-drafts", action="store_true", help="List drafts")
    args = parser.parse_args()

    try:
        config = TypefullyConfig.from_env()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nSet these environment variables:")
        print("  TYPEFULLY_API_KEY=your_api_key")
        print("  TYPEFULLY_SOCIAL_SET_ID=your_social_set_id")
        return 1

    with TypefullyClient(config) as client:
        if args.test:
            try:
                user = client.get_me()
                print(f"✓ Connected as: {user.get('name', user.get('email', 'Unknown'))}")

                social_set = client.get_social_set()
                print(f"✓ Social set: @{social_set.get('username', 'unknown')}")

                # List available platforms
                platforms = []
                for p in ["x", "linkedin", "bluesky", "threads", "mastodon"]:
                    if social_set.get(p):
                        platforms.append(p)
                print(f"✓ Platforms: {', '.join(platforms)}")

            except TypefullyError as e:
                print(f"✗ API Error: {e}")
                return 1

        elif args.list_drafts:
            try:
                result = client.list_drafts(limit=5)
                drafts = result.get("results", [])
                print(f"Found {result.get('count', 0)} drafts (showing {len(drafts)}):")
                for draft in drafts:
                    status = draft.get("status", "unknown")
                    preview = draft.get("preview", "")[:50]
                    print(f"  [{status}] {preview}...")
            except TypefullyError as e:
                print(f"Error: {e}")
                return 1

        else:
            parser.print_help()

    return 0


if __name__ == "__main__":
    exit(main())
