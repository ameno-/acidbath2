#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyttsx3",
# ]
# ///
"""
Generate audio summary MP3 from text using pyttsx3
"""

import pyttsx3
import sys
import os

def generate_audio(text, output_file):
    """Generate MP3 from text using pyttsx3"""
    try:
        # Initialize TTS engine
        engine = pyttsx3.init()

        # Configure engine settings
        engine.setProperty('rate', 150)    # Speech rate (words per minute)
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

        print("🎙️  Audio Summary Generator")
        print("=" * 40)
        print(f"📝 Text length: {len(text)} characters")
        print(f"📁 Output file: {output_file}")
        print("🔊 Generating audio...")

        # Save to file
        engine.save_to_file(text, output_file)
        engine.runAndWait()

        print(f"✅ Audio file created: {output_file}")

        # Verify file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📊 File size: {file_size / 1024:.1f} KB")
            return True
        else:
            print("❌ Error: Output file was not created")
            return False

    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Read the summary text from file
    try:
        with open("audio-summary.txt", "r") as f:
            text = f.read()

        success = generate_audio(text, "audio-summary.mp3")
        sys.exit(0 if success else 1)
    except FileNotFoundError:
        print("❌ Error: audio-summary.txt not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
