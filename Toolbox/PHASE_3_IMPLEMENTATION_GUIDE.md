# Phase 3 Implementation Guide: Background Data Collector

**Status:** READY TO BUILD
**Date:** 2025-10-19
**Lead AI:** Claude (Haiku 4.5)
**Estimated Time:** ~9 hours
**Priority:** HIGH (Blocks Phase 3.2+)

---

## 📋 Complete Implementation Checklist

### Files to Create (6 NEW files)

- [ ] `scripts/trading/data_collector.py` (2 hours)
- [ ] `scripts/trading/api_sources.py` (1.5 hours)
- [ ] `scripts/trading/ticker_manager.py` (1 hour)
- [ ] `scripts/trading/cache_manager.py` (1 hour)
- [ ] `config/api_keys.json` (5 min - secret storage)
- [ ] `data/watchlist.json` (5 min - initial watchlist)

### Files to Modify (2 files)

- [ ] `Journal/command-center.html` (+1.5 hours - add control panel)
- [ ] `scripts/trading/analyze_ticker.py` (+1 hour - cache integration)

### Testing & Documentation (2 hours)

- [ ] Unit tests for each module
- [ ] Integration testing
- [ ] Error handling verification
- [ ] Documentation updates

---

## 🔧 Detailed Module Specifications

### Module 1: `api_sources.py` (1.5 hours)

**Purpose:** Handle all API calls and scraping to Finnhub

**Dependencies:**
- `requests` (HTTP library)
- `json` (built-in)
- `logging` (built-in)
- Optional: `beautifulsoup4` (for Yahoo Finance scraping fallback)

**Key Functions:**

```python
class FinnhubAPI:
    def __init__(self, api_key: str)
    def get_quote(self, ticker: str) -> Dict
        # Fetch: price, change, volume

    def get_candles(self, ticker: str, days: int = 100) -> pd.DataFrame
        # Fetch: OHLCV history

    def get_technical_indicators(self, ticker: str) -> Dict
        # Fetch: Pre-calculated indicators (if available)

class YahooFinanceScraper:
    def scrape_quote(self, ticker: str) -> Dict
        # Fallback if Finnhub fails

    def scrape_candles(self, ticker: str) -> pd.DataFrame
        # Historical data fallback
```

**Rate Limit Handling:**
- Track call count per minute
- Warn when approaching 60 calls/min limit
- Queue requests if needed
- Log API usage

**Error Handling:**
- Invalid ticker → Return None
- API down → Log error, try fallback
- Rate limited → Queue and retry
- No internet → Use stale cache

---

### Module 2: `cache_manager.py` (1 hour)

**Purpose:** Store and retrieve cached market data

**Data Structure:**
- Location: `data/cache/[TICKER].json`
- TTL: 5 minutes
- Format: Standardized JSON (see SESSION_TRACKER.md for format)

**Key Functions:**

```python
class CacheManager:
    def __init__(self, cache_dir: str = 'data/cache')

    def save(self, ticker: str, data: Dict) -> bool
        # Save ticker data to JSON file
        # Timestamp automatically added

    def get(self, ticker: str) -> Optional[Dict]
        # Retrieve ticker data from cache
        # Returns None if not cached

    def is_stale(self, ticker: str, ttl: int = 300) -> bool
        # Check if cached data is older than TTL (seconds)

    def clear(self, ticker: str = None) -> bool
        # Clear specific ticker or all cache

    def get_all(self) -> Dict[str, Dict]
        # Return all cached data for all tickers

    def get_cache_status(self) -> Dict
        # Return: {entries: N, total_size: bytes, oldest: datetime}
```

**File Format:** (already defined in documentation)

---

### Module 3: `ticker_manager.py` (1 hour)

**Purpose:** Manage user's watchlist (add/remove tickers)

**Data Structure:**
- Location: `data/watchlist.json`
- Default: `["SPY", "QQQ"]` (always tracked)

**Key Functions:**

```python
class TickerManager:
    def __init__(self, watchlist_file: str = 'data/watchlist.json')

    def load(self) -> List[str]
        # Load watchlist from JSON

    def save(self) -> bool
        # Persist watchlist to JSON

    def add_ticker(self, ticker: str) -> bool
        # Add ticker to watchlist
        # Returns False if already exists or invalid

    def remove_ticker(self, ticker: str) -> bool
        # Remove ticker (except SPY/QQQ - protected)
        # Returns False if protected or not found

    def is_tracked(self, ticker: str) -> bool
        # Check if ticker in watchlist

    def get_watchlist(self) -> List[str]
        # Return current watchlist

    def validate_ticker(self, ticker: str) -> bool
        # Validate ticker format (alphanumeric, 1-5 chars)
```

**File Format:**
```json
{
  "watchlist": ["SPY", "QQQ", "NVDA", "TSLA"],
  "protected": ["SPY", "QQQ"],
  "last_updated": "2025-10-19T16:00:00"
}
```

---

### Module 4: `data_collector.py` (2 hours)

**Purpose:** Background service that collects market data continuously

**Architecture:**
- Runs as daemon/background process
- Reads watchlist every cycle
- Fetches data from Finnhub
- Calculates indicators
- Caches results
- Logs activity

**Key Functions:**

```python
class DataCollector:
    def __init__(self, api_key: str, update_interval: int = 300)
        # interval = 5 minutes

    def start(self) -> bool
        # Begin background collection loop

    def stop(self) -> bool
        # Gracefully stop collection

    def is_running(self) -> bool
        # Check if service is active

    def _collection_loop(self)
        # Main loop: fetch → calculate → cache → sleep

    def _fetch_and_process(self, ticker: str) -> Dict
        # For single ticker:
        # 1. Fetch from Finnhub
        # 2. Calculate RSI, MACD, OBV, MAs
        # 3. Detect S/R levels
        # 4. Cache result

    def get_status(self) -> Dict
        # Return: {running: bool, last_run: datetime, next_run: datetime,
        #          tickers_tracked: N, cache_entries: N}
```

**Process Flow:**
```
1. Load watchlist (SPY, QQQ + user-added)
2. For each ticker:
   a. Fetch from Finnhub (quote + candles)
   b. Calculate indicators:
      - RSI (14-period)
      - MACD (12/26/9)
      - OBV
      - EMA 20/50/200
   c. Detect support/resistance (peaks/troughs)
   d. Cache to JSON
   e. Log activity
3. Write status to collector_status.json
4. Sleep 5 minutes
5. Repeat from step 1
```

**Error Handling:**
- If Finnhub fails → Try Yahoo Finance scraping
- If both fail → Keep running, use stale cache
- If watchlist file missing → Use default (SPY, QQQ)
- If cache write fails → Log and continue

**Logging:**
- Log file: `logs/data_collector.log`
- Include: timestamp, action, status, errors
- Rotate logs daily

---

### Module 5: Updates to `analyze_ticker.py` (1 hour)

**Changes:**
- Import cache_manager
- Check if collector is running
- Try cache first (if not stale)
- Fall back to fresh fetch if needed
- Pass market context from cache (SPY/QQQ status, VIX)

**New Flow:**
```python
def analyze(ticker: str):
    # 1. Try to get from cache
    cached = cache_manager.get(ticker)

    if cached and not cache_manager.is_stale(ticker):
        # Use cached data (FAST)
        context = build_from_cache(cached)
        context['source'] = 'cache'
    else:
        # Fetch fresh
        context = fetch_fresh(ticker)
        context['source'] = 'live'

    # 2. Get market context from cache
    context['spy'] = cache_manager.get('SPY')
    context['qqq'] = cache_manager.get('QQQ')
    context['vix'] = get_vix_from_cache()

    # 3. Continue with decision logic
    ta_score = calculate_ta_score(context)
    ...
```

---

### Module 6: Command Center UI Updates (1.5 hours)

**New Panel: "Data Collector Control"**

HTML Structure:
```html
<div class="data-collector-panel">
  <h3>📡 Data Collector Control</h3>

  <div class="status-row">
    <span class="status-indicator" id="collector-status">●</span>
    <span id="collector-info">STOPPED</span>
  </div>

  <div class="button-row">
    <button id="btn-start">START</button>
    <button id="btn-stop">STOP</button>
    <button id="btn-restart">RESTART</button>
  </div>

  <div class="ticker-section">
    <h4>Tracked Tickers (Always: SPY, QQQ)</h4>
    <div id="ticker-list"></div>
  </div>

  <div class="add-ticker-row">
    <input type="text" id="new-ticker" placeholder="Add ticker">
    <button id="btn-add">ADD</button>
  </div>
</div>
```

**JavaScript Functions:**
```javascript
function startCollector()
  // Send start signal to backend

function stopCollector()
  // Send stop signal to backend

function addTicker()
  // Get input, validate, send to backend

function removeTicker(ticker)
  // Remove from watchlist, update UI

function updateStatus()
  // Poll backend for status, update UI

function displayTickers()
  // Populate ticker list with prices
```

**Backend Integration:**
- Need Flask/FastAPI endpoint for:
  - GET `/api/collector/status`
  - POST `/api/collector/start`
  - POST `/api/collector/stop`
  - POST `/api/collector/ticker/add`
  - POST `/api/collector/ticker/remove`

---

### Module 7: API Keys & Configuration (5 min)

**File: `config/api_keys.json`**
```json
{
  "finnhub": "cvb0g99r01qgjh3v2pcgcvb0g99r01qgjh3v2pd0",
  "created": "2025-10-19",
  "note": "Keep this file secure - contains API keys"
}
```

**File: `data/watchlist.json`**
```json
{
  "watchlist": ["SPY", "QQQ"],
  "protected": ["SPY", "QQQ"],
  "last_updated": "2025-10-19T16:00:00"
}
```

---

## 🧪 Testing Plan

### Unit Tests Required

```python
# test_api_sources.py
- test_get_quote_valid_ticker()
- test_get_quote_invalid_ticker()
- test_get_candles_sufficient_data()
- test_api_error_handling()
- test_rate_limit_handling()

# test_cache_manager.py
- test_save_and_retrieve()
- test_is_stale_ttl()
- test_clear_specific_ticker()
- test_clear_all()

# test_ticker_manager.py
- test_add_ticker()
- test_remove_ticker_fails_for_protected()
- test_validate_ticker_format()
- test_load_save_persistence()

# test_data_collector.py
- test_collector_starts()
- test_collector_stops()
- test_collection_cycle()
- test_error_recovery()
```

### Integration Tests

```python
# test_integration.py
- test_collector_to_cache_flow()
- test_cache_to_engine_flow()
- test_command_center_controls()
- test_ticker_add_remove_in_running_service()
```

### Manual Testing Checklist

- [ ] Start collector, verify every 5 minutes it updates
- [ ] Add NVDA ticker, verify it gets tracked
- [ ] Remove NVDA ticker, verify it stops being tracked
- [ ] Try to remove SPY (should fail)
- [ ] Stop collector gracefully
- [ ] Restart collector, verify cache persists
- [ ] Run analysis with collector running (uses cache)
- [ ] Run analysis with collector stopped (fetches live)
- [ ] Verify Finnhub API rate limits not hit
- [ ] Verify error handling (kill internet, restart service, etc.)

---

## 📊 File Dependencies

```
data_collector.py
├── api_sources.py (fetch data)
├── cache_manager.py (store data)
└── ticker_manager.py (get watchlist)

analyze_ticker.py
├── cache_manager.py (read cache)
└── api_sources.py (live fetch fallback)

command-center.html
└── Backend API endpoints (start/stop/add/remove)

Backend API (need to add)
├── data_collector.py (control service)
├── ticker_manager.py (manage tickers)
└── cache_manager.py (get status)
```

---

## ⏱️ Time Breakdown

| Task | Time | Notes |
|------|------|-------|
| api_sources.py | 1.5h | Finnhub API + Yahoo scraper fallback |
| cache_manager.py | 1h | JSON caching, TTL handling |
| ticker_manager.py | 1h | Watchlist management |
| data_collector.py | 2h | Main background service |
| Command Center UI | 1.5h | HTML + JavaScript controls |
| analyze_ticker.py updates | 1h | Cache integration |
| Testing | 2h | Unit + integration tests |
| Documentation | 0.5h | Comments, docstrings |
| **TOTAL** | **~9h** | Ready for production |

---

## ✅ Success Criteria

- [x] Architecture designed and documented
- [ ] All 6 modules created and tested
- [ ] Command Center UI has working START/STOP/ADD/REMOVE buttons
- [ ] Finnhub API integration works (60 calls/min rate limit respected)
- [ ] JSON cache persists between sessions
- [ ] Background service runs independently for 8 hours+
- [ ] Decision engine reads from cache and returns instant results
- [ ] Manual testing passes all 10 checklist items
- [ ] Error handling verified (API down, invalid ticker, etc.)
- [ ] Documentation complete for next AI handoff

---

## 🚀 Ready to Build

All design decisions made. All dependencies identified. All specifications written.

**Next step:** Implement all 6 modules in order listed above.

**Estimated completion:** ~9 hours of focused development

**Then:** Proceed to Phase 3.2 (TA Calculator) with real data flowing

---

**Document created:** 2025-10-19
**Ready for implementation:** YES ✅
**Handoff quality:** HIGH (detailed specs + success criteria)
