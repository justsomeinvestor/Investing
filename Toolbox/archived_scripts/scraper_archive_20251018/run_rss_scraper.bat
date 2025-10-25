@echo off
echo ================================================================
echo RSS Article Collector

echo ================================================================
echo.

echo Installing dependencies...
pip install feedparser > nul 2>&1

echo Starting RSS collector...
echo.
python rss_scraper.py

pause
