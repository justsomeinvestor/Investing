================================================================
YouTube Transcript Downloader - WORKING VERSION
================================================================

QUICK START:
-----------
1. Double-click "run_gui.bat"
2. Enter a YouTube channel URL (e.g., @TomBilyeu)
3. Click "Download Latest Transcript"
4. Done! The transcript will be saved as a timestamped markdown file.

FEATURES:
---------
- Automatically gets the latest video from any YouTube channel
- Downloads transcript (manual or auto-generated)
- Saves as timestamped markdown files with metadata
- Format: YYYY-MM-DD_HHMMSS_Video_Title.md

OUTPUT FORMAT:
-------------
Each transcript is saved as a markdown file containing:
- Video title
- Video URL
- Download timestamp
- Transcript length
- Full transcript text

EXAMPLES OF CHANNELS TO TRY:
----------------------------
@TomBilyeu
@3Blue1Brown
@TED
@CrashCourse
@Computerphile

REQUIREMENTS:
------------
- Python 3.6 or higher
- The batch file automatically installs required packages:
  * youtube-transcript-api
  * yt-dlp

TROUBLESHOOTING:
---------------
If a video doesn't have transcripts:
- Try a different channel
- Educational channels usually have transcripts
- Some creators disable transcripts on their videos

FILES:
-----
run_gui.bat          - Double-click this to start!
transcript_gui.py    - The main GUI application
test_transcript.py   - Test script to verify everything works
get_transcript.py    - Command-line version (advanced)

================================================================
Everything has been tested and is working perfectly!
================================================================