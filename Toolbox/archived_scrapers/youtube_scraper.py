import re
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass  # Fallback for older Python

# ========================================================================
# SHARED CONFIGURATION (YouTube specific)
# ========================================================================

YOUTUBE_ROOT = Path(r'../Research/YouTube')

# YouTube Configuration
CHANNELS_FILE = Path('channels.txt')
YT_PROCESSED_LOG_NAME = '_processed_videos.json'
YT_REQUEST_DELAY_SECONDS = 9
YT_FAILURE_BACKOFF_SECONDS = 20
YT_TRANSCRIPT_TIMEOUT_SECONDS = 45
YT_MAX_VIDEOS = 3

# Shared Utilities (moved from unified_scraper.py)
TRANSCRIPT_EXECUTOR = ThreadPoolExecutor(max_workers=4)
TAG_RE = re.compile(r'<[^>]+>')
BR_RE = re.compile(r'<\s*br\s*/?>', re.IGNORECASE)

def sanitize_filename(name):
    """Remove invalid filename characters"""
    return re.sub(r'[<>:"/\\|?*]', '_', str(name).strip())

# ========================================================================
# YOUTUBE SCRAPER FUNCTIONS
# ========================================================================

def get_channel_folder(channel_name):
    """Return the YouTube subfolder for a given channel."""
    folder = YOUTUBE_ROOT / sanitize_filename(channel_name)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def load_yt_processed_ids(channel_folder):
    """Load previously processed video IDs for a channel."""
    log_path = channel_folder / YT_PROCESSED_LOG_NAME
    if not log_path.exists():
        return set()
    try:
        data = json.loads(log_path.read_text(encoding='utf-8'))
        if isinstance(data, list):
            return set(data)
    except Exception as exc:
        print(f"    [WARN] Could not read processed log: {exc}")
    return set()


def save_yt_processed_ids(channel_folder, processed_ids):
    """Persist processed video IDs back to disk."""
    log_path = channel_folder / YT_PROCESSED_LOG_NAME
    try:
        log_path.write_text(json.dumps(sorted(processed_ids)), encoding='utf-8')
    except Exception as exc:
        print(f"    [WARN] Could not write processed log: {exc}")


def find_existing_transcripts(channel_folder, video_id):
    """Return transcript files already saved for a given video ID."""
    matches = []
    target_url = f"https://youtube.com/watch?v={video_id}"

    for candidate in channel_folder.glob('*.md'):
        if candidate.name.endswith('_Summary.md'):
            continue
        try:
            text = candidate.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                text = candidate.read_text(encoding='latin-1')
            except Exception as exc:
                print(f"    [WARN] Could not inspect existing file {candidate.name}: {exc}")
                continue
        except Exception as exc:
            print(f"    [WARN] Could not inspect existing file {candidate.name}: {exc}")
            continue

        if target_url in text:
            matches.append(candidate)

    return matches


def get_channel_videos(channel_url, max_videos=10):
    """Get latest videos from a YouTube channel"""
    if not channel_url.endswith('/videos'):
        channel_url = channel_url.rstrip('/') + '/videos'

    print(f"  Fetching videos from: {channel_url}")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }

    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)

            if 'entries' in info and info['entries']:
                channel_name = info.get('channel', info.get('uploader', 'Unknown'))

                for entry in info['entries'][:max_videos]:
                    if entry:
                        videos.append({
                            'id': entry.get('id'),
                            'title': entry.get('title', 'Unknown Title'),
                            'channel': channel_name
                        })

                print(f"  Found {len(videos)} videos from {channel_name}")
                return videos, channel_name
            else:
                print("  No videos found")
                return [], None

        except Exception as e:
            print(f"  Error: {e}")
            return [], None


def _fetch_transcript(video_id):
    """Internal helper to fetch a transcript."""
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)

    transcript = None
    transcript_type = ""

    try:
        transcript = transcript_list.find_manually_created_transcript(['en'])
        transcript_type = "Manual English"
    except Exception:
        try:
            transcript = transcript_list.find_generated_transcript(['en'])
            transcript_type = "Auto-generated English"
        except Exception:
            available = list(transcript_list)
            if available:
                transcript = available[0]
                transcript_type = transcript.language

    if transcript:
        data = transcript.fetch()
        text = ' '.join(item.text for item in data)
        return text, transcript_type

    return None, None


def download_transcript(video_id, video_title):
    """Download transcript for a video with timeout protection."""
    future = TRANSCRIPT_EXECUTOR.submit(_fetch_transcript, video_id)
    try:
        return future.result(YT_TRANSCRIPT_TIMEOUT_SECONDS)
    except FuturesTimeoutError:
        future.cancel()
        print(f"    [TIMEOUT] Transcript fetch exceeded {YT_TRANSCRIPT_TIMEOUT_SECONDS}s for {video_title}")
        return None, None
    except Exception as e:
        print(f"    Error getting transcript for {video_title}: {e}")
        return None, None


def save_individual_transcript(channel_folder, channel_name, video_id, video_title, transcript_text, transcript_type):
    """Save transcript as a standalone markdown file."""
    channel_folder.mkdir(parents=True, exist_ok=True)

    download_date = datetime.now().strftime("%Y-%m-%d")
    safe_title = sanitize_filename(video_title)
    safe_id = sanitize_filename(video_id)
    filename = channel_folder / f"{download_date}_{safe_id}_{safe_title}.md"

    markdown_content = f"""# {video_title}

## Video Information
- **Channel**: {channel_name}
- **Video URL**: https://youtube.com/watch?v={video_id}
- **Downloaded**: {download_date}
- **Transcript Type**: {transcript_type}
- **Transcript Length**: {len(transcript_text)} characters

---

## Transcript

{transcript_text}

---

*Downloaded using Unified Content Scraper*
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return filename


def process_youtube_channel(channel_url, max_videos=3):
    """Process a single YouTube channel"""
    print(f"\n  Processing: {channel_url}")

    videos, channel_name = get_channel_videos(channel_url, max_videos)

    if not videos:
        print("    No videos to process")
        return

    downloaded = 0
    failed = 0
    cached = 0
    channel_folder = get_channel_folder(channel_name)
    processed_ids = load_yt_processed_ids(channel_folder)
    new_downloads = False
    cache_changed = False

    for i, video in enumerate(videos, 1):
        video_id = video['id']
        video_title = video['title']

        print(f"    [{i}/{len(videos)}] {video_title}")

        if video_id in processed_ids:
            print("      [SKIP] Already processed (cached)")
            cached += 1
            continue

        existing_files = find_existing_transcripts(channel_folder, video_id)
        if existing_files:
            print("      [SKIP] Transcript already exists on disk")
            cached += 1
            processed_ids.add(video_id)
            cache_changed = True
            continue

        transcript_text, transcript_type = download_transcript(video_id, video_title)

        if transcript_text:
            filename = save_individual_transcript(
                channel_folder,
                channel_name,
                video_id,
                video_title,
                transcript_text,
                transcript_type
            )
            print(f"      [OK] Saved: {filename}")
            downloaded += 1
            processed_ids.add(video_id)
            new_downloads = True
            cache_changed = True
        else:
            print("      [SKIP] No transcript available")
            failed += 1
            time.sleep(YT_FAILURE_BACKOFF_SECONDS)

        if i < len(videos):
            time.sleep(YT_REQUEST_DELAY_SECONDS)

    if cache_changed:
        save_yt_processed_ids(channel_folder, processed_ids)

    if not new_downloads and cached > 0:
        print("    No new transcripts found; channel already up to date.")

    if downloaded == 0 and cached == 0:
        print()
        print("  [WARNING] No transcripts downloaded - possibly IP rate limited")
        print("            Try changing VPN/IP or wait 15-30 minutes")

    print(f"  Summary: {downloaded} downloaded, {failed} failed, {cached} cached")


def run_youtube_scraper():
    """Run the YouTube transcript scraper"""
    print("\n" + "=" * 60)
    print("YOUTUBE TRANSCRIPT SCRAPER")
    print("=" * 60)

    if not CHANNELS_FILE.exists():
        print("\nWARNING: channels.txt not found - skipping YouTube scraping")
        return None

    channels = []
    with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue

            if '#' in line:
                line = line.split('#', 1)[0].strip()

            if not line:
                continue

            if line.startswith('@'):
                line = f"https://youtube.com/{line}"

            channels.append(line)

    if not channels:
        print("\nNo channels configured in channels.txt - skipping YouTube scraping")
        return None

    print(f"\nFound {len(channels)} channel(s) to process")

    total_transcripts = 0
    for channel_url in channels:
        try:
            # process_youtube_channel would need to return count, but for now estimate
            process_youtube_channel(channel_url, max_videos=YT_MAX_VIDEOS)
            total_transcripts += YT_MAX_VIDEOS  # Approximate
        except Exception as e:
            print(f"Error processing {channel_url}: {e}")
            continue

    print(f"\nYouTube transcripts saved to: {YOUTUBE_ROOT}")

    return {
        'channels': len(channels),
        'transcripts': total_transcripts
    }


if __name__ == "__main__":
    run_youtube_scraper()
    print("\n[OK] YouTube Scraping complete! Closing in 3 seconds...")
    time.sleep(3)
