# Options Data Fetcher

**Status**: ✅ Production Ready (yfinance) | 🛰️ Polygon spot assist enabled

## Overview

This system fetches options data 3-4 times daily for integration with your dashboard or other systems. It provides max pain, put/call ratios, IV percentiles, and key option levels for stocks like SPY, QQQ, NVDA.

## Quick Start

### Prerequisites
```bash
pip install pandas requests yfinance
```

### Basic Usage
```bash
# Fetch SPY, QQQ, NVDA data (spot via Polygon, chains via yfinance)
python options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 180

# Output: Research/.cache/optionsData.json (meta + tickers)
```

### Cron Job Setup (3×/day)
```cron
# 9:20 ET (pre-market), 12:05 ET (midday), 15:40 ET (into close)
20 9 * * 1-5 python /path/to/options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 180
05 12 * * 1-5 python /path/to/options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 180
40 15 * * 1-5 python /path/to/options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 180
```

## Data Output

The script writes to: `Research/.cache/optionsData.json`

### Sample Output Format
```json
{
  "date": "2025-10-16",
  "generatedAt": "2025-10-16T06:00:23",
  "source": "auto",
  "tickers": {
    "SPY": {
      "lastUpdated": "2025-10-16 05:47 ET",
      "currentPrice": 665.17,
      "maxPain": "$663",
      "putCallRatio": "1.07",
      "ivPercentile": "6%",
      "totalOI": "375,868",
      "expiration": "2025-10-16",
      "keyLevels": [
        {"strike": "663", "type": "Max Pain", "gamma": "N/A", "oi": "15K"},
        {"strike": "670", "type": "Call Wall", "gamma": "N/A", "oi": "18K"},
        {"strike": "655", "type": "Put Wall", "gamma": "N/A", "oi": "11K"}
      ],
      "source": "yfinance"
    },
    "QQQ": {
      "lastUpdated": "2025-10-16 05:47 ET",
      "currentPrice": 602.22,
      "maxPain": "$597",
      "putCallRatio": "1.23",
      "ivPercentile": "12%",
      "totalOI": "266,687",
      "expiration": "2025-10-16",
      "keyLevels": [
        {"strike": "597", "type": "Max Pain", "gamma": "N/A", "oi": "6K"},
        {"strike": "610", "type": "Call Wall", "gamma": "N/A", "oi": "11K"},
        {"strike": "580", "type": "Put Wall", "gamma": "N/A", "oi": "7K"}
      ],
      "source": "yfinance"
    }
  }
}
```

## Configuration Options

### Command Line Arguments
- `--tickers`: Space-separated list of ticker symbols (default: SPY QQQ)
- `--ttl-min`: Cache TTL in minutes (default: 180)
- `--provider`: `auto`, `polygon`, or `yfinance` (default: auto)

### Provider Selection
1. **Auto**: Uses Polygon equities for spot (if `POLYGON_API_KEY` set) and falls back to yfinance chains
2. **Polygon**: Uses Polygon for both spot and chains (requires options-enabled API key)
3. **yfinance**: Uses Yahoo Finance for chains; still leverages Polygon equities for spot if a key is present

## Current Working State

### ✅ What's Working
- **Hybrid Provider**: Polygon equities for spot + yfinance chains by default
- **Caching System**: Prevents redundant API calls
- **Rate Limiting**: Prevents API throttling
- **Error Handling**: Robust retry logic and fallbacks
- **Cron Ready**: Designed for 3-4x daily execution

### ⚠️ Known Limitations
- **yfinance Data Quality**: Limited open interest data, basic IV calculations
- **Polygon Options Snapshot**: Requires paid tier; otherwise chains fall back to yfinance

## Integration Guide

### For Dashboard Integration
1. **File Location**: Research/.cache/optionsData.json
2. **Update Frequency**: ~3 hours by default (--ttl-min configurable)
3. **Data Structure**: JSON meta wrapper with a 	ickers map for per-symbol metrics

### Environment Variables
```bash
# Recommended: enable Polygon equities for reliable spot prices
export POLYGON_API_KEY="your_polygon_key_here"
```

### Error Handling
The script outputs errors in the JSON structure:
```json
{
  "SPY": {
    "error": "Error description here"
  }
}
```

## Troubleshooting

### Common Issues

**1. "Yahoo API requires curl_cffi session"**
- ✅ **Fixed**: Removed requests session parameter from yfinance calls

**2. "Too Many Requests"**
- ✅ **Fixed**: Added rate limiting to prevent API throttling

**3. "403 Forbidden" (Polygon snapshot)**
- Check if your Polygon subscription includes options data
- Verify API key is valid and has proper permissions
- The script automatically falls back to yfinance chains when snapshots are unavailable

**4. Empty Open Interest Data**
- This is a limitation of yfinance's free data
- For complete OI data, Polygon API with proper subscription is recommended

### Testing
```bash
# Test with single ticker
python options_fetch_3x_daily.py --tickers SPY --ttl-min 1

# Force fresh data (ignore cache)
# Delete the .cache directory and run again

# Test different providers
python options_fetch_3x_daily.py --tickers SPY --provider yfinance
python options_fetch_3x_daily.py --tickers SPY --provider polygon
```

## File Structure
```
RnD/Options/
├── options_fetch_3x_daily.py    # Main script
├── test_polygon.py             # Polygon API test script
├── README.md                   # This file
└── OPTIONS_FETCH_README.md     # Original documentation

Research/.cache/
└── optionsData.json           # Output file
```

## Maintenance Notes

- **Dependencies**: pandas, requests, yfinance
- **Python Version**: 3.8+ recommended
- **Cache Location**: `Research/.cache/` (auto-created)
- **Log Output**: Check stdout for `[OK]` success messages

## Next Steps for Enhancement

1. **Polygon API Setup**: Resolve 403 errors for complete data
2. **Data Quality**: Enhance IV percentile calculations
3. **Additional Metrics**: Add gamma exposure, vanna, charm
4. **Web Interface**: Consider a simple web dashboard for monitoring

---

**Hand-off Ready**: This system is production-ready using yfinance. For enhanced data quality, resolve Polygon API permissions.</result>
</write_to_file>
