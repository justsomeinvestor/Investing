#!/usr/bin/env python3
"""
Quick test script to verify transcript download works
"""

from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from datetime import datetime
import re
import os

def test_download():
    """Test downloading a transcript from a known good channel"""

    # Using 3Blue1Brown - known to have transcripts
    channel_url = "https://youtube.com/@3blue1brown/videos"

    print(f"Testing with: {channel_url}")
    print("-" * 50)

    # Get latest video
    print("Step 1: Getting latest video...")
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)

            if 'entries' in info and info['entries']:
                latest = info['entries'][0]
                video_id = latest.get('id')
                title = latest.get('title', 'Unknown Title')

                print(f"[OK] Found video: {title}")
                print(f"   Video ID: {video_id}")
                print()

                # Get transcript
                print("Step 2: Getting transcript...")
                ytt_api = YouTubeTranscriptApi()
                transcript_list = ytt_api.list(video_id)

                # Try to get English transcript
                transcript = None
                try:
                    transcript = transcript_list.find_manually_created_transcript(['en'])
                    print("[OK] Found manual English transcript")
                except:
                    try:
                        transcript = transcript_list.find_generated_transcript(['en'])
                        print("[OK] Found auto-generated English transcript")
                    except:
                        available = list(transcript_list)
                        if available:
                            transcript = available[0]
                            print(f"[OK] Found {transcript.language} transcript")

                if transcript:
                    data = transcript.fetch()
                    text = ' '.join([item.text for item in data])

                    print(f"   Length: {len(text)} characters")
                    print()

                    # Save to file
                    print("Step 3: Saving to file...")
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
                    filename = f"{timestamp}_{safe_title}.md"

                    markdown_content = f"""# {title}

## Video Information
- **Video URL**: https://youtube.com/watch?v={video_id}
- **Downloaded**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Transcript Length**: {len(text)} characters

---

## Transcript

{text}

---

*Downloaded using YouTube Transcript Downloader*
"""

                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)

                    print(f"[OK] Saved to: {filename}")
                    print()
                    print("=" * 50)
                    print("SUCCESS! Everything is working!")
                    print("=" * 50)

                    # Show preview
                    print()
                    print("Preview of transcript (first 200 chars):")
                    print(text[:200] + "...")

                    return True
                else:
                    print("[ERROR] No transcript available")
                    return False
            else:
                print("[ERROR] No videos found")
                return False

        except Exception as e:
            print(f"[ERROR] Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("YouTube Transcript Downloader - Test Script")
    print("=" * 50)
    print()

    success = test_download()

    print()
    if success:
        print("[OK] Test passed! The GUI should work perfectly.")
    else:
        print("[ERROR] Test failed. Check the error messages above.")

    input("\nPress Enter to exit...")