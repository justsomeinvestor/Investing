# Archived Scrapers

## Status: ARCHIVED (October 17, 2025)

These scraper tools have been archived as they encountered blocking issues with the run_all_scrapers.py execution getting stuck.

## Contents

- `run_all_scrapers.py` - Main orchestrator (had execution hang issues)
- `rss_scraper.py` - RSS feed scraper
- `youtube_scraper.py` - YouTube transcript scraper
- `x_scraper.py` - X/Twitter scraper
- `bookmarks_scraper.py` - X/Twitter bookmarks scraper
- `fetch_options_data.py` - SPY options chain data fetcher
- `options_fetch_3x_daily.py` - Scheduled options data fetcher

## Replacement

The research workflow now uses **web search** instead of scrapers to gather market data in real-time.

## Future Consideration

These scrapers may be resurrected if:
1. The blocking issues are debugged and resolved
2. Rate limiting or API access is properly handled
3. A need arises for deeper historical data collection

## Original Purpose

These tools were designed to collect data from multiple sources (YouTube, RSS, Twitter, options chains) for market sentiment analysis. The workflow would aggregate this data into summaries for investment decision-making.

---

*Archived: October 17, 2025*
*Reason: Execution hang issues in run_all_scrapers.py*
