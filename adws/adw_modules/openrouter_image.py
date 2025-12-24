"""OpenRouter Image Generation Module.

Provides image generation via OpenRouter API with Nano Banana
(Gemini 2.5 Flash Image Preview) as the primary model.

This module is designed to be:
- A fallback when other image generation APIs (like Gemini direct) hit quotas
- Extensible for other OpenRouter image models
- Simple to use with sensible defaults

Environment Variables:
    OPENROUTER_API_KEY: Required. Your OpenRouter API key.

Usage:
    from adw_modules.openrouter_image import generate_image, ImageConfig

    # Simple usage
    path = generate_image("A sunset over mountains", "output.png")

    # With configuration
    config = ImageConfig(aspect_ratio="16:9", output_path="banner.png")
    path = generate_image("A glass processor chip", config=config)
"""

import base64
import json
import os
import logging
import httpx
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, Union


# Module logger
logger = logging.getLogger(__name__)


class ImageModel(str, Enum):
    """Supported OpenRouter image generation models."""

    # Google Nano Banana models
    NANO_BANANA = "google/gemini-2.5-flash-image-preview"
    NANO_BANANA_PRO = "google/gemini-2.0-flash-image-generation"  # Gemini 3 Pro Image Preview

    # Black Forest Labs
    FLUX_MAX = "black-forest-labs/flux-2-max"
    FLUX_FLEX = "black-forest-labs/flux-2-flex"

    # OpenAI
    GPT5_IMAGE = "openai/gpt-5-image"
    GPT5_IMAGE_MINI = "openai/gpt-5-image-mini"


class AspectRatio(str, Enum):
    """Supported aspect ratios for Gemini image models."""

    SQUARE = "1:1"       # 1024x1024
    LANDSCAPE = "16:9"   # 1536x864
    PORTRAIT = "9:16"    # 864x1536
    WIDE = "21:9"        # 1536x672
    TALL = "9:21"        # 672x1536
    STANDARD_4_3 = "4:3" # 1024x768
    STANDARD_3_4 = "3:4" # 768x1024


class ImageSize(str, Enum):
    """Image size/resolution options."""

    SIZE_1K = "1K"  # Default, ~1024px
    SIZE_2K = "2K"  # ~2048px
    SIZE_4K = "4K"  # ~4096px


@dataclass
class ImageConfig:
    """Configuration for image generation."""

    model: ImageModel = ImageModel.NANO_BANANA
    aspect_ratio: AspectRatio = AspectRatio.LANDSCAPE
    image_size: ImageSize = ImageSize.SIZE_2K
    output_path: Optional[str] = None
    temperature: float = 1.0
    max_tokens: int = 8192

    # Additional model-specific options
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageResult:
    """Result from image generation."""

    success: bool
    file_path: Optional[str] = None
    base64_data: Optional[str] = None
    text_response: Optional[str] = None
    error: Optional[str] = None
    model_used: Optional[str] = None
    usage: Optional[Dict[str, int]] = None


class OpenRouterImageError(Exception):
    """Base exception for OpenRouter image generation errors."""
    pass


class APIKeyError(OpenRouterImageError):
    """Raised when API key is missing or invalid."""
    pass


class GenerationError(OpenRouterImageError):
    """Raised when image generation fails."""
    pass


class RateLimitError(OpenRouterImageError):
    """Raised when rate limit is exceeded."""
    pass


def get_api_key() -> str:
    """Get OpenRouter API key from environment.

    Returns:
        The API key string.

    Raises:
        APIKeyError: If OPENROUTER_API_KEY is not set.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise APIKeyError(
            "OPENROUTER_API_KEY environment variable not set. "
            "Get your key from https://openrouter.ai/keys"
        )
    return api_key


def _build_request_payload(
    prompt: str,
    config: ImageConfig
) -> Dict[str, Any]:
    """Build the API request payload.

    Args:
        prompt: The image generation prompt.
        config: Image configuration options.

    Returns:
        Dictionary containing the API request payload.
    """
    payload = {
        "model": config.model.value,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["image", "text"],
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
    }

    # Add image_config for Gemini models
    if config.model in (ImageModel.NANO_BANANA, ImageModel.NANO_BANANA_PRO):
        payload["image_config"] = {
            "aspect_ratio": config.aspect_ratio.value,
            "image_size": config.image_size.value,
        }

    # Add any extra parameters
    payload.update(config.extra_params)

    return payload


def _extract_image_from_response(response_data: Dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
    """Extract base64 image data and text from API response.

    Args:
        response_data: The parsed JSON response from the API.

    Returns:
        Tuple of (base64_image_data, text_response).
    """
    base64_data = None
    text_response = None

    choices = response_data.get("choices", [])
    if not choices:
        return None, None

    message = choices[0].get("message", {})

    # Extract text content
    content = message.get("content")
    if isinstance(content, str):
        text_response = content
    elif isinstance(content, list):
        # Content might be a list of parts
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "text":
                    text_response = part.get("text", "")
                elif part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:image"):
                        # Extract base64 from data URL
                        base64_data = url.split(",", 1)[1] if "," in url else url

    # Check for images array (Gemini format)
    images = message.get("images", [])
    if images and not base64_data:
        first_image = images[0]
        if isinstance(first_image, dict):
            url = first_image.get("image_url", {}).get("url", "")
            if url.startswith("data:image"):
                base64_data = url.split(",", 1)[1] if "," in url else url
        elif isinstance(first_image, str):
            # Direct base64 string
            if first_image.startswith("data:image"):
                base64_data = first_image.split(",", 1)[1] if "," in first_image else first_image
            else:
                base64_data = first_image

    return base64_data, text_response


def _save_image(base64_data: str, output_path: str) -> str:
    """Save base64 image data to file.

    Args:
        base64_data: Base64-encoded image data.
        output_path: Path to save the image.

    Returns:
        Absolute path to the saved file.
    """
    # Ensure output directory exists
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Decode and save
    image_bytes = base64.b64decode(base64_data)
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    logger.info(f"Image saved to: {output_path}")
    return output_path


def generate_image(
    prompt: str,
    output_path: Optional[str] = None,
    config: Optional[ImageConfig] = None,
    timeout: float = 120.0,
) -> ImageResult:
    """Generate an image using OpenRouter API.

    Args:
        prompt: Text prompt describing the image to generate.
        output_path: Optional path to save the image. If not provided,
            uses config.output_path or generates a temp file.
        config: Optional ImageConfig for customization.
        timeout: Request timeout in seconds.

    Returns:
        ImageResult with success status, file path, and metadata.

    Raises:
        APIKeyError: If OPENROUTER_API_KEY is not set.
        GenerationError: If image generation fails.
        RateLimitError: If rate limit is exceeded.

    Example:
        result = generate_image(
            "A photorealistic glass processor chip on beige background",
            output_path="banner.png",
            config=ImageConfig(aspect_ratio=AspectRatio.LANDSCAPE)
        )
        if result.success:
            print(f"Image saved to: {result.file_path}")
    """
    # Get API key
    api_key = get_api_key()

    # Set up config
    if config is None:
        config = ImageConfig()

    # Determine output path
    final_output_path = output_path or config.output_path
    if not final_output_path:
        # Generate temp filename
        import tempfile
        fd, final_output_path = tempfile.mkstemp(suffix=".png")
        os.close(fd)

    # Build request
    payload = _build_request_payload(prompt, config)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://acidbath.dev",
        "X-Title": "ACIDBATH Banner Generator",
    }

    logger.info(f"Generating image with {config.model.value}...")
    logger.debug(f"Prompt: {prompt[:100]}...")

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            # Handle rate limiting
            if response.status_code == 429:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("error", {}).get("message", "Rate limit exceeded")
                raise RateLimitError(f"Rate limit exceeded: {error_msg}")

            # Handle other errors
            if response.status_code != 200:
                error_msg = f"API error {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise GenerationError(error_msg)

            response_data = response.json()

    except httpx.TimeoutException:
        raise GenerationError(f"Request timed out after {timeout} seconds")
    except httpx.HTTPError as e:
        raise GenerationError(f"HTTP error: {e}")

    # Extract image data
    base64_data, text_response = _extract_image_from_response(response_data)

    if not base64_data:
        return ImageResult(
            success=False,
            error="No image data in response",
            text_response=text_response,
            model_used=config.model.value,
        )

    # Save image
    try:
        saved_path = _save_image(base64_data, final_output_path)
    except Exception as e:
        return ImageResult(
            success=False,
            error=f"Failed to save image: {e}",
            base64_data=base64_data,
            text_response=text_response,
            model_used=config.model.value,
        )

    # Extract usage info
    usage = response_data.get("usage", {})

    return ImageResult(
        success=True,
        file_path=saved_path,
        base64_data=base64_data,
        text_response=text_response,
        model_used=config.model.value,
        usage={
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        },
    )


async def generate_image_async(
    prompt: str,
    output_path: Optional[str] = None,
    config: Optional[ImageConfig] = None,
    timeout: float = 120.0,
) -> ImageResult:
    """Async version of generate_image.

    Args:
        prompt: Text prompt describing the image to generate.
        output_path: Optional path to save the image.
        config: Optional ImageConfig for customization.
        timeout: Request timeout in seconds.

    Returns:
        ImageResult with success status, file path, and metadata.
    """
    import asyncio

    # Get API key
    api_key = get_api_key()

    # Set up config
    if config is None:
        config = ImageConfig()

    # Determine output path
    final_output_path = output_path or config.output_path
    if not final_output_path:
        import tempfile
        fd, final_output_path = tempfile.mkstemp(suffix=".png")
        os.close(fd)

    # Build request
    payload = _build_request_payload(prompt, config)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://acidbath.dev",
        "X-Title": "ACIDBATH Banner Generator",
    }

    logger.info(f"Generating image async with {config.model.value}...")

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            if response.status_code == 429:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("error", {}).get("message", "Rate limit exceeded")
                raise RateLimitError(f"Rate limit exceeded: {error_msg}")

            if response.status_code != 200:
                raise GenerationError(f"API error {response.status_code}: {response.text}")

            response_data = response.json()

    except httpx.TimeoutException:
        raise GenerationError(f"Request timed out after {timeout} seconds")
    except httpx.HTTPError as e:
        raise GenerationError(f"HTTP error: {e}")

    # Extract and save (same as sync version)
    base64_data, text_response = _extract_image_from_response(response_data)

    if not base64_data:
        return ImageResult(
            success=False,
            error="No image data in response",
            text_response=text_response,
            model_used=config.model.value,
        )

    try:
        saved_path = _save_image(base64_data, final_output_path)
    except Exception as e:
        return ImageResult(
            success=False,
            error=f"Failed to save image: {e}",
            base64_data=base64_data,
            text_response=text_response,
            model_used=config.model.value,
        )

    usage = response_data.get("usage", {})

    return ImageResult(
        success=True,
        file_path=saved_path,
        base64_data=base64_data,
        text_response=text_response,
        model_used=config.model.value,
        usage={
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        },
    )


# Convenience function for banner generation with ACIDBATH defaults
def generate_banner(
    prompt: str,
    output_path: str,
    aspect_ratio: AspectRatio = AspectRatio.LANDSCAPE,
    model: ImageModel = ImageModel.NANO_BANANA,
) -> ImageResult:
    """Generate a blog banner with ACIDBATH defaults.

    Convenience wrapper with sensible defaults for blog banner generation:
    - 16:9 aspect ratio (2560x1440 target)
    - 2K resolution
    - Nano Banana model

    Args:
        prompt: Detailed banner prompt.
        output_path: Where to save the banner.
        aspect_ratio: Aspect ratio (default: 16:9 landscape).
        model: Image model to use.

    Returns:
        ImageResult with generation outcome.

    Example:
        result = generate_banner(
            prompt="A photorealistic glass AI processor chip...",
            output_path="public/assets/posts/my-post-banner.png"
        )
    """
    config = ImageConfig(
        model=model,
        aspect_ratio=aspect_ratio,
        image_size=ImageSize.SIZE_2K,
        temperature=1.0,
    )

    return generate_image(prompt, output_path, config)


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Generate images via OpenRouter API")
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("-o", "--output", default="generated_image.png", help="Output file path")
    parser.add_argument(
        "-m", "--model",
        choices=[m.value for m in ImageModel],
        default=ImageModel.NANO_BANANA.value,
        help="Model to use"
    )
    parser.add_argument(
        "-a", "--aspect-ratio",
        choices=[r.value for r in AspectRatio],
        default=AspectRatio.LANDSCAPE.value,
        help="Aspect ratio"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    # Find model and aspect ratio enums
    model = ImageModel(args.model)
    aspect_ratio = AspectRatio(args.aspect_ratio)

    config = ImageConfig(model=model, aspect_ratio=aspect_ratio)

    print(f"Generating image with {model.value}...")
    print(f"Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")

    try:
        result = generate_image(args.prompt, args.output, config)

        if result.success:
            print(f"\n✅ Image generated successfully!")
            print(f"   Path: {result.file_path}")
            if result.usage:
                print(f"   Tokens: {result.usage.get('total_tokens', 'N/A')}")
        else:
            print(f"\n❌ Generation failed: {result.error}")
            sys.exit(1)

    except APIKeyError as e:
        print(f"\n❌ API Key Error: {e}")
        sys.exit(1)
    except GenerationError as e:
        print(f"\n❌ Generation Error: {e}")
        sys.exit(1)
    except RateLimitError as e:
        print(f"\n❌ Rate Limit Error: {e}")
        sys.exit(1)
