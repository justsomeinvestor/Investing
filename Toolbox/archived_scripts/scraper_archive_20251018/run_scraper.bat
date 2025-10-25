@echo off
echo ================================================================
echo YouTube Transcript Batch Scraper
echo ================================================================
echo.

echo Installing dependencies...
pip install youtube-transcript-api yt-dlp > nul 2>&1

echo Starting scraper...
echo.
python scrape_channels.py

pause