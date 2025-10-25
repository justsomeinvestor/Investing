# YouTube Transcript Scraper

Professional-grade YouTube transcript downloader for investment research.

## Quick Start

1. **Configure channels**: Edit `channels.txt` (8 high-quality channels pre-configured)
2. **Run scraper**: Double-click `run_scraper.bat`
3. **Access transcripts**: `output\YouTube\[Channel Name]\`

## Features

- Downloads the last 3 videos per channel
- Saves transcripts as timestamped markdown files
- Organizes output by channel folder
- Waits 3 seconds between requests by default (helps avoid rate limits)
- Honors weighted channel prioritization (weights 6-10 enabled by default)

## Output Structure

```
output\
|-- 42 Macro\
|   |-- 2025-09-29_143022_Video_Title_1.md
|   |-- 2025-09-29_143025_Video_Title_2.md
|   |-- 2025-09-29_143028_Video_Title_3.md
|-- Fundstrat Capital\
|-- Unchained Crypto\
|-- ...
```


## Active Channels (Weight 6-10)

| Channel | Weight | Category | Focus |
|---------|--------|----------|-------|
| @42Macro | 10 | Macro | Data-driven macro for timing risk cycles |
| @FundstratCapital | 9 | Macro | Veteran strategist Tom Lee |
| @UnchainedCrypto | 8 | Crypto | No-hype crypto reporting |
| @intothecryptoverse | 8 | On-Chain | Quant crypto cycles |
| @RaoulPalTJM | 7 | Macro | Macro/Exponential Age theses |
| @Bankless | 7 | Policy | Regulatory/infrastructure coverage |
| @Bg2Pod | 7 | Macro | High-signal tech/macro from operators |
| @ChedsTrading | 6 | TA | Solid TA pedagogy |

## Configuration

### Change number of videos per channel
Edit `scrape_channels.py` line 274:
```python
process_channel(channel_url, max_videos=3)  # Change 3 to desired number
```

### Add/remove channels
Edit `channels.txt`:
- Uncomment lines (remove `#`) to enable channels
- Add new channels: `@ChannelHandle  # Weight X - Category - Description`

### Adjust rate limiting
Edit `scrape_channels.py` line 206:
```python
time.sleep(3)  # Change 3 to more seconds if needed
```

## Rate Limiting

- **3-second delay** between videos (automatic)
- If you see "IP blocked" errors:
  - Change VPN/IP address
  - Wait 15-30 minutes
  - Reduce videos per channel
  - Use residential VPN (not datacenter)

## Requirements

- Python 3.6+
- youtube-transcript-api (auto-installed)
- yt-dlp (auto-installed)

## Files

| File | Purpose |
|------|---------|
| `run_scraper.bat` | Main launcher (double-click to run) |
| `scrape_channels.py` | Core scraper logic |
| `channels.txt` | Channel configuration with weights |
| `requirements.txt` | Python dependencies |
| `_archive/` | Backup of old versions |

## RSS Article Collector

- **Configure feeds**: Update `rss_feeds.json` to add sources or toggle the provided placeholders (Benzinga and Forex Factory are disabled until valid URLs are supplied).
- **Run collector**: Double-click `run_rss_scraper.bat` to fetch the latest articles; dependencies install automatically.
- **Output location**: Articles are saved under `output\RSS\<Provider>` with filenames like `YYYY-MM-DD_<Feed>_<Title>.md` plus a `_processed_articles.json` cache per provider.
- **Workflow**: Use the new markdown files to refresh provider summaries (`YYYY-MM-DD_<Provider>_Summary.md`) exactly like the YouTube transcript process.

## Troubleshooting

**No transcripts downloaded?**
- Change VPN IP address
- Wait 15-30 minutes between runs
- Check if channel has transcripts enabled

**Rate limited?**
- Increase delay in code (line 206)
- Reduce max_videos (line 274)
- Use residential VPN

**Channel not found?**
- Verify channel handle is correct
- Add `/videos` to URL manually
- Check channel exists on YouTube

## Archive

Old versions, GUI, and documentation are in `_archive/` folder.

---

*Last updated: 2025-09-29*

