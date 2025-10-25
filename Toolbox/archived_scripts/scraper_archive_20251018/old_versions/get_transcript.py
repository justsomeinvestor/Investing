#!/usr/bin/env python3
"""
Simple script to get the latest video transcript from a YouTube channel.
Usage: python get_transcript.py <channel_url>
"""

import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

def get_latest_video(channel_url):
    """Get the latest video from a YouTube channel."""
    print(f"Getting latest video from: {channel_url}")

    # Make sure we're looking at the videos page
    if not channel_url.endswith('/videos'):
        channel_url = channel_url.rstrip('/') + '/videos'

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Just get video list, don't extract full info
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)

            if 'entries' in info and info['entries']:
                latest = info['entries'][0]
                video_id = latest.get('id')
                title = latest.get('title', 'Unknown Title')

                print(f"Latest video: {title}")
                print(f"Video ID: {video_id}")

                return video_id, title
            else:
                print("No videos found")
                return None, None

        except Exception as e:
            print(f"Error: {e}")
            return None, None

def get_transcript(video_id, title):
    """Download transcript for a video."""
    print(f"Getting transcript for: {title}")

    try:
        # Get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try English first (manual, then auto-generated)
        transcript = None
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
            print("Using manual English transcript")
        except:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
                print("Using auto-generated English transcript")
            except:
                # Use first available
                available = list(transcript_list)
                if available:
                    transcript = available[0]
                    print(f"Using {transcript.language} transcript")

        if transcript:
            # Get the transcript text
            data = transcript.fetch()
            text = ' '.join([item['text'] for item in data])

            # Save to file
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            filename = f"{safe_title}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n")
                f.write(f"Video: https://youtube.com/watch?v={video_id}\n")
                f.write("-" * 50 + "\n\n")
                f.write(text)

            print(f"Saved transcript to: {filename}")
            print(f"Length: {len(text)} characters")
            return filename
        else:
            print("No transcript available")
            return None

    except Exception as e:
        print(f"Error getting transcript: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_transcript.py <channel_url>")
        print("Example: python get_transcript.py https://youtube.com/@channelname")
        return

    channel_url = sys.argv[1]

    # Get latest video
    video_id, title = get_latest_video(channel_url)

    if video_id:
        # Get transcript
        filename = get_transcript(video_id, title)
        if filename:
            print(f"\nDone! Transcript saved to {filename}")
        else:
            print("\nFailed to get transcript")
    else:
        print("Failed to get video")

if __name__ == "__main__":
    main()