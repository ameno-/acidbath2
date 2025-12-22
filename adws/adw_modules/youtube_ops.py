"""YouTube content extraction using yt-dlp.

This module handles extraction of metadata, transcripts, and content
from YouTube videos, returning a unified ContentObject structure.
"""

import json
import os
import re
import subprocess
from typing import Optional, Dict, Any
from adws.adw_modules.data_types import ContentType, ContentObject


def extract_youtube_metadata(url: str) -> dict:
    """Extract metadata from YouTube video using yt-dlp.

    Args:
        url: YouTube video URL

    Returns:
        dict: Metadata with keys: video_id, title, duration, uploader, upload_date

    Raises:
        RuntimeError: If yt-dlp fails or video is unavailable
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", url],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp metadata extraction failed: {result.stderr}")

        metadata_json = json.loads(result.stdout)
        return {
            "video_id": metadata_json.get("id", ""),
            "title": metadata_json.get("title", ""),
            "duration": metadata_json.get("duration", 0),
            "uploader": metadata_json.get("uploader", ""),
            "upload_date": metadata_json.get("upload_date", ""),
        }
    except subprocess.TimeoutExpired:
        raise RuntimeError("yt-dlp timed out while extracting metadata")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse yt-dlp metadata JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during metadata extraction: {e}")


def download_transcript(url: str, output_dir: str) -> str:
    """Download transcript from YouTube video using yt-dlp.

    Args:
        url: YouTube video URL
        output_dir: Directory to save transcript file

    Returns:
        str: Path to saved transcript file

    Raises:
        RuntimeError: If transcript download fails
    """
    try:
        # Extract video ID for filename
        video_id_match = re.search(r"(?:v=|youtu\.be/)([^&\?]+)", url)
        if not video_id_match:
            raise RuntimeError("Could not extract video ID from URL")
        video_id = video_id_match.group(1)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Output file path
        transcript_path = os.path.join(output_dir, f"transcript_{video_id}.txt")

        # Try auto-generated subtitles first, fall back to manual if needed
        result = subprocess.run(
            [
                "yt-dlp",
                "--write-auto-sub",
                "--write-sub",
                "--skip-download",
                "--sub-format",
                "vtt",
                "--sub-langs",
                "en",
                "--output",
                os.path.join(output_dir, f"{video_id}"),
                url,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        # Find the downloaded .vtt file
        vtt_files = [
            f
            for f in os.listdir(output_dir)
            if f.startswith(video_id) and f.endswith(".vtt")
        ]

        if not vtt_files:
            raise RuntimeError(
                "No transcript/subtitles available for this video. "
                "yt-dlp output: " + result.stderr
            )

        vtt_path = os.path.join(output_dir, vtt_files[0])

        # Convert VTT to plain text
        with open(vtt_path, "r", encoding="utf-8") as vtt_file:
            vtt_content = vtt_file.read()

        # Remove VTT formatting (timestamps, cue identifiers, etc.)
        # Keep only the actual text content
        lines = vtt_content.split("\n")
        text_lines = []
        for line in lines:
            line = line.strip()
            # Skip WEBVTT header, timestamps, cue identifiers, and empty lines
            if (
                line
                and not line.startswith("WEBVTT")
                and not re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}", line)
                and not re.match(r"^\d+$", line)
                and "-->" not in line
            ):
                text_lines.append(line)

        transcript_text = "\n".join(text_lines)

        # Save as plain text
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        # Clean up VTT file
        os.remove(vtt_path)

        return transcript_path

    except subprocess.TimeoutExpired:
        raise RuntimeError("yt-dlp timed out while downloading transcript")
    except Exception as e:
        raise RuntimeError(f"Failed to download transcript: {e}")


def classify_youtube_content(metadata: dict, transcript: str) -> str:
    """Classify YouTube content as technical, educational, or general.

    Basic heuristic classification based on keywords in title and transcript.

    Args:
        metadata: Video metadata dict
        transcript: Transcript text

    Returns:
        str: Classification ("technical", "educational", or "general")
    """
    tech_keywords = [
        "programming",
        "code",
        "software",
        "python",
        "javascript",
        "api",
        "database",
        "algorithm",
        "tutorial",
        "developer",
        "engineering",
        "tech",
        "debug",
        "deploy",
    ]

    edu_keywords = [
        "learn",
        "course",
        "lesson",
        "teach",
        "education",
        "lecture",
        "study",
        "explain",
        "guide",
        "introduction",
        "beginner",
    ]

    # Combine title and transcript for analysis (limit transcript to first 1000 chars)
    content = (metadata.get("title", "") + " " + transcript[:1000]).lower()

    tech_count = sum(1 for kw in tech_keywords if kw in content)
    edu_count = sum(1 for kw in edu_keywords if kw in content)

    if tech_count >= 2:
        return "technical"
    elif edu_count >= 2:
        return "educational"
    else:
        return "general"


def extract_youtube_content(url: str, output_dir: str) -> ContentObject:
    """Extract complete content from YouTube video.

    Args:
        url: YouTube video URL
        output_dir: Directory for saving transcript files

    Returns:
        ContentObject: Unified content object with YouTube data

    Raises:
        RuntimeError: If extraction fails at any stage
    """
    # Extract metadata
    metadata = extract_youtube_metadata(url)

    # Download transcript
    transcript_path = download_transcript(url, output_dir)

    # Read transcript content
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    # Classify content
    classification = classify_youtube_content(metadata, transcript_text)
    metadata["classification"] = classification

    # Build ContentObject
    return ContentObject(
        type=ContentType.YOUTUBE,
        text=transcript_text,
        source=url,
        video_id=metadata["video_id"],
        transcript_path=transcript_path,
        url=url,
        title=metadata["title"],
        metadata=metadata,
    )
