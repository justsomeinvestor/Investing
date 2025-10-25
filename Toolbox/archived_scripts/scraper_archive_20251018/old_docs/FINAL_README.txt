================================================================
YouTube Transcript Scraper - FINAL VERSION
================================================================

WHAT IT DOES:
------------
✓ Downloads transcripts from multiple YouTube channels
✓ Combines ALL transcripts into ONE FILE per channel
✓ Organizes by channel folders with timestamps
✓ Automatic rate-limit protection (3-second delays)

HOW TO USE:
----------
1. Edit "channels.txt" - Add your channels (one per line):
   @TomBilyeu
   @42Macro
   https://youtube.com/@ARKInvest2015

2. Double-click "run_scraper.bat"

3. Wait for it to finish

4. Find your files in: transcripts/[Channel Name]/

OUTPUT:
------
Each channel gets ONE combined markdown file:

transcripts/
├── Tom Bilyeu/
│   └── 2025-09-29_132723_Tom Bilyeu_ALL.md  ← ALL 10 transcripts
├── 42 Macro/
│   └── 2025-09-29_132755_42 Macro_ALL.md    ← ALL 10 transcripts
└── ARK Invest/
    └── 2025-09-29_133020_ARK Invest_ALL.md  ← ALL transcripts

FILE FORMAT:
-----------
# Channel Name - All Transcripts

**Downloaded**: 2025-09-29 13:27:23
**Total Videos**: 10

---

## 1. Video Title One
**Video URL**: https://youtube.com/watch?v=...
**Transcript Type**: Manual English
**Length**: 54457 characters

### Transcript
[Full text...]

---

## 2. Video Title Two
[Next transcript...]

---

[Continues for all videos]

RATE LIMITING:
-------------
✓ 3-second delay between videos (automatic)
✓ If you still see "IP blocked" errors:
  - Wait 15-30 minutes
  - Reduce max_videos in scrape_channels.py (line ~265)
  - Or run fewer channels at once

SETTINGS:
--------
To change videos per channel:
1. Open scrape_channels.py
2. Find: process_channel(channel_url, max_videos=10)
3. Change 10 to your number

TO INCREASE DELAY:
-----------------
1. Open scrape_channels.py  
2. Find: time.sleep(3)
3. Change 3 to 5 or more seconds

WHAT'S DIFFERENT FROM BEFORE:
-----------------------------
✗ OLD: Created separate file for each video (10 files per channel)
✓ NEW: Creates ONE file per channel with all transcripts combined

================================================================
