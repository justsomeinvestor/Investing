# Technical Implementation Guide: Technicals Tab Automation

**Version**: 1.0
**Date**: October 25, 2025
**Scope**: Research Dashboard Technicals Tab Automation Architecture

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Data Flow Diagram](#data-flow-diagram)
3. [How Key Levels are Calculated](#how-key-levels-are-calculated)
4. [How VIX Regime is Determined](#how-vix-regime-is-determined)
5. [Extending the Automation](#extending-the-automation)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Verification Checklist](#verification-checklist)

---

## Architecture Overview

The Technicals Tab automation consists of **4 layers**:

```
Layer 1: Data Collection
├─ Web Scraping (Selenium)
├─ API Calls (Finnhub, CoinGecko)
└─ Light HTML Scraping

Layer 2: Processing & Calculation
├─ P/C Ratio extraction
├─ Key levels calculation
├─ VIX regime determination
└─ Support/Resistance calculation

Layer 3: Caching
├─ JSON cache files (daily)
├─ YAML backup structures
└─ Historical archives

Layer 4: Dashboard Sync
├─ Master plan YAML update
├─ Timestamp management
├─ Graceful degradation (preserve manual data)
└─ Error detection & validation
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              WORKFLOW EXECUTION                             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1.5: FETCH TECHNICAL DATA                            │
│ (scripts/processing/fetch_technical_data.py)               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [1/6] fetch_spy_options()                                 │
│  └─→ Run: scripts/scrapers/scrape_options_data.py SPY      │
│      ├─ Barchart P/C ratios + IV percentile                │
│      ├─ Barchart max pain chart page                       │
│      └─ Calculate key levels from OI data                  │
│      └─ Output: JSON with all fields + keyLevels array     │
│                                                              │
│  [2/6] fetch_qqq_options()                                 │
│  └─→ Run: scripts/scrapers/scrape_options_data.py QQQ      │
│      ├─ Same process as SPY                                │
│      └─ Output: QQQ options data + keyLevels               │
│                                                              │
│  [3/6] fetch_spx_levels() → PLACEHOLDER (not yet automated)│
│  [4/6] fetch_btc_levels() → PLACEHOLDER (not yet automated)│
│  [5/6] fetch_market_breadth() → PLACEHOLDER                │
│  [6/6] fetch_vix_structure()                               │
│  └─→ Calculate regime from current VIX (from market_data)  │
│      ├─ < 15 = low, 15-20 = normal                        │
│      ├─ 20-30 = elevated, > 30 = high                      │
│      └─ Output: VIX regime in JSON                         │
│                                                              │
│  Result: Research/.cache/2025-10-25_technical_data.json    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3.9: SYNC TECHNICALS TAB                             │
│ (scripts/utilities/sync_technicals_tab.py)                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [1] Load technical_data.json (fresh data)                 │
│  [2] Load market_data.json (for SPY price)                 │
│  [3] Load master-plan.md (for manual data preservation)    │
│  [4] Update optionsData section                            │
│      ├─ Sync SPY/QQQ max pain, P/C, IV, volume flow       │
│      ├─ Sync key levels (or preserve if scraper empty)     │
│      └─ Update lastUpdated timestamps                      │
│  [5] Validate data completeness                            │
│      ├─ Check max pain not null                            │
│      ├─ Check key levels not empty                         │
│      └─ Display errors or success message                  │
│  [6] Update aiInterpretation.updatedAt                     │
│  [7] Save master-plan.md with backup                       │
│                                                              │
│  Result: master-plan/master-plan.md (updated)              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ DASHBOARD RENDERING                                         │
│ (master-plan/research-dashboard.html)                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Read YAML front matter from master-plan.md                │
│  ├─ Extract tabs.technicals.optionsData                    │
│  ├─ Extract tabs.technicals.closeProbability               │
│  ├─ Extract tabs.technicals.aiInterpretation               │
│  └─ Render UI with fresh data                              │
│                                                              │
│  User sees: Current max pain, key levels, VIX regime       │
│            All data auto-updated, always fresh             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## How Key Levels are Calculated

**Location**: `scripts/scrapers/scrape_options_data.py` → `calculate_key_levels()` method

### Calculation Logic

```python
1. GET BASE DATA:
   - Max pain (from max-pain-chart scraping)
   - Put OI (total put open interest)
   - Call OI (total call open interest)

2. DETERMINE TICKER ZONE SIZE:
   if ticker == 'SPY':
       zone_size = 0.01  # 1% zones
   else:  # QQQ
       zone_size = 0.015  # 1.5% zones

3. CREATE KEY LEVELS ARRAY:

   Level 1: MAX PAIN (anchor point)
   ├─ Strike: max_pain value
   ├─ Type: "Max Pain"
   ├─ Sentiment: "neutral"
   └─ Reason: "Peak open interest"

   Level 2: CALL WALLS (if call_oi > put_oi)
   ├─ Strike: max_pain × (1 + zone_size × 2)  [+2% above]
   ├─ Type: "Call Wall"
   ├─ Sentiment: "bullish"
   └─ Reason: "Call OI cluster"

   Level 3: GAMMA NEUTRAL (middle ground)
   ├─ Strike: max_pain × (1 + zone_size × 1)  [+1% above]
   ├─ Type: "Gamma Neutral"
   ├─ Sentiment: "neutral"
   └─ Reason: "High gamma exposure zone"

   Level 4: PUT WALLS (if put_oi > call_oi)
   ├─ Strike: max_pain × (1 - zone_size × 2)  [-2% below]
   ├─ Type: "Put Wall"
   ├─ Sentiment: "bearish"
   └─ Reason: "Put OI cluster"

4. OUTPUT:
   keyLevels = [
       {"strike": "670", "type": "Max Pain", "sentiment": "neutral", ...},
       {"strike": "676.7", "type": "Gamma Neutral", "sentiment": "neutral", ...},
       {"strike": "656.6", "type": "Put Wall", "sentiment": "bearish", ...}
   ]
```

### Example Walkthrough (SPY on Oct 25, 2025)

```
Data Inputs:
  - max_pain: $670.00
  - put_oi: 11,995,973
  - call_oi: 4,506,384
  - zone_size: 0.01 (SPY)

Sentiment Determination:
  - put_oi (11.9M) > call_oi (4.5M)
  - Ratio: 2.66:1 → BEARISH bias

Calculation:
  - max_pain = 670.00
  - call_wall = 670 × 1.02 = 683.40
  - gamma_neutral = 670 × 1.01 = 676.70
  - put_wall = 670 × 0.98 = 656.60

Output:
  ✓ Max Pain: $670.00
  ✓ Gamma Neutral: $676.70 (neutral)
  ✓ Put Wall: $656.60 (bearish - high put OI)
```

### Integration Points

- **Called by**: `scrape_all()` method after max pain is determined
- **Uses data from**: Barchart options metrics (P/C ratio, OI data)
- **Outputs to**: `self.data['keyLevels']` array
- **Validation**: Checks max pain exists before calculating
- **Error handling**: Returns empty array if max pain fails

---

## How VIX Regime is Determined

**Location**: `scripts/processing/fetch_technical_data.py` → `fetch_vix_structure()` method

### Regime Classification

```python
Current VIX Calculation:
  - Reads current VIX price from market_data.json (Finnhub API)

Classification Logic:
  if vix_current < 15:
      vol_regime = "low"          # Complacency period
                                   # Good time to sell volatility
  elif vix_current < 20:
      vol_regime = "normal"        # Healthy market
                                   # Normal trading conditions
  elif vix_current < 30:
      vol_regime = "elevated"      # Caution period
                                   # Risk-off sentiment emerging
  else:
      vol_regime = "high"          # Panic/crisis mode
                                   # Extremely negative sentiment
```

### Thresholds Explained

| Regime | VIX Level | Market Condition | Trader Action |
|---|---|---|---|
| **Low** | < 15 | Complacency, rallying | Sell volatility, caution on long exposure |
| **Normal** | 15-20 | Healthy, balanced | Standard trading conditions |
| **Elevated** | 20-30 | Risk increasing | Reduce leverage, increase hedges |
| **High** | > 30 | Panic/crisis | Defensive positioning, opportunities |

### Example Values

```
Historical VIX Readings:
  - 12.5 → "low" (COVID vaccine optimism, 2020)
  - 18.2 → "normal" (typical market)
  - 27.3 → "elevated" (Fed rate hike expectations)
  - 42.8 → "high" (COVID crash, March 2020)
```

### Integration Points

- **Called by**: `fetch_all()` after market data available
- **Uses data from**: Current VIX price (from Finnhub in market_data.json)
- **Outputs to**: `vix_structure['vol_regime']` field
- **Dashboard display**: Shows current regime in UI (helps traders understand volatility context)

---

## Extending the Automation

### Adding New Data Source (e.g., Adding Support/Resistance Levels)

**Template**: Create a new fetch function

```python
# File: scripts/processing/fetch_technical_data.py

def fetch_support_resistance_levels(self):
    """Calculate support and resistance from recent price action"""
    print("[7/6] Calculating support/resistance levels...")

    try:
        # 1. Get price data (could be from API or scraping)
        # 2. Calculate pivot points, Fibonacci levels, etc.
        # 3. Return structured data

        return {
            'asset': 'SPY',
            'pivot': 670.50,
            'support_1': 665.20,
            'support_2': 660.00,
            'resistance_1': 675.80,
            'resistance_2': 680.50,
            'source': 'calculated',
            'fetchedAt': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
        return self.get_empty_levels_data('SPY')
```

### Adding to Data Collection Flow

```python
# In fetch_all() method:
data = {
    'date': self.date_str,
    'timestamp': datetime.now().isoformat(),
    'spy_options': self.fetch_spy_options(),
    'qqq_options': self.fetch_qqq_options(),
    'support_resistance': self.fetch_support_resistance_levels(),  # NEW
    'spx_levels': self.fetch_spx_levels(),
    'btc_levels': self.fetch_btc_levels(),
    'market_breadth': self.fetch_market_breadth(),
    'vix_structure': self.fetch_vix_structure()
}
```

### Syncing to Dashboard

```python
# File: scripts/utilities/sync_technicals_tab.py

def update_support_resistance(self, tech_tab: Dict[str, Any]):
    """Sync support/resistance levels to technicals tab"""
    if 'supportResistance' not in tech_tab:
        tech_tab['supportResistance'] = {}

    # Map technical_data fields to master_plan structure
    sr_data = self.technical_data.get('support_resistance', {})
    if sr_data and sr_data.get('pivot'):
        tech_tab['supportResistance'] = {
            'pivot': sr_data.get('pivot'),
            'support1': sr_data.get('support_1'),
            'support2': sr_data.get('support_2'),
            'resistance1': sr_data.get('resistance_1'),
            'resistance2': sr_data.get('resistance_2'),
            'lastUpdated': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        print(f"      ✓ Updated support/resistance levels")
```

### Best Practices for Extensions

1. **Use consistent naming** (snake_case for Python, camelCase for JSON)
2. **Include error handling** (try/except with fallback empty data)
3. **Add timestamps** (track when data was fetched)
4. **Validate required fields** (check data before using)
5. **Provide clear output** (print progress statements)
6. **Test independently** (run function standalone before integrating)

---

## Troubleshooting Guide

### Problem: Dashboard Shows Stale Data

**Symptom**: Technicals tab shows Oct 24 data when today is Oct 25

**Diagnosis Steps**:
```bash
1. Check workflow ran:
   $ ls -la Research/.cache/2025-10-25_technical_data.json

2. Check scraper output:
   $ python scripts/scrapers/scrape_options_data.py SPY | tail -50

3. Check sync script ran:
   $ grep "Technicals tab" Research/.cache/*_workflow_log.txt

4. Check master plan was updated:
   $ grep "2025-10-25T" master-plan/master-plan.md | tail -5
```

**Solutions** (in order of likelihood):
- Workflow didn't run → Check cron/scheduler
- Scraper failed → Check internet connection and Barchart website
- Sync failed → Check permissions on master-plan.md
- Data is there but timestamp is wrong → Run sync script manually

### Problem: "KEY LEVELS DATA MISSING" Warning

**Symptom**: Workflow shows warning about empty key levels

**Root Causes**:
1. Max pain scraping failed
2. Key levels calculation returned empty array
3. Cache file corrupted (see BUG_FIX document)

**Fix**:
```bash
1. Test scraper directly:
   $ python scripts/scrapers/scrape_options_data.py SPY

2. Verify output contains keyLevels array:
   $ python scripts/scrapers/scrape_options_data.py SPY | jq '.keyLevels'

3. If empty, check Barchart website is accessible:
   $ curl -s https://www.barchart.com/etfs-funds/quotes/SPY/max-pain-chart | head -20

4. If website has changed, update scraper regex patterns
```

### Problem: Validation Errors on Sync

**Symptom**: Sync script shows "STALE DATA RISK" messages

**Meaning**: One of the critical data fields is missing or null

**Fields Being Validated**:
- `spy_options.maxPain` ← Must not be null
- `qqq_options.maxPain` ← Must not be null
- `spy_options.keyLevels` ← Must not be empty array
- `qqq_options.keyLevels` ← Must not be empty array

**Solutions**:
1. Check technical_data.json file exists and is valid
2. Re-run scraper for affected ticker
3. Check error messages in workflow log
4. For empty key levels, check max pain exists first

### Problem: Manual Data Getting Overwritten

**Symptom**: Manually edited key levels are replaced with stale data

**Prevention**: Sync script preserves manual data if scraper returns empty

```python
# This is the behavior in update_options_data():
if scraper_data.get('keyLevels'):
    entry['keyLevels'] = scraper_data['keyLevels']  # Use new data
elif existing_data.get('keyLevels'):
    entry['keyLevels'] = existing_data['keyLevels']  # Keep manual
```

**If data still gets overwritten**:
1. Check if scraper is returning empty array `[]`
2. Manually restore from .backup file
3. Report as bug in GitHub issues

---

## Verification Checklist

### Daily Verification (After Workflow Runs)

- [ ] Check technical_data.json exists: `ls Research/.cache/*technical_data.json`
- [ ] Verify max pain is current: `grep -A 1 '"maxPain"' Research/.cache/2025-10-25_technical_data.json`
- [ ] Verify key levels populated: `grep -c '"type": "Max Pain"' Research/.cache/2025-10-25_technical_data.json`
- [ ] Check master plan updated: `grep "2025-10-25T" master-plan/master-plan.md | wc -l`
- [ ] Verify no stale data warnings in workflow log
- [ ] Check dashboard displays correct data in browser

### Weekly Verification

- [ ] All 5 data sources working (SPY, QQQ, VIX, SPX placeholder, BTC placeholder)
- [ ] No error messages in past 7 days of logs
- [ ] Historical data being properly archived
- [ ] Backup files being created on every sync

### Monthly Verification

- [ ] Review API rate limit usage (Finnhub, CoinGecko)
- [ ] Check for any deprecated website changes (Barchart, ChartExchange)
- [ ] Analyze stale data incident frequency
- [ ] Review performance metrics (speed of data collection)

---

## Performance Optimization

### Current Performance

```
Phase 1.5 (Fetch Technical Data):  ~2-3 minutes
  ├─ SPY scraping:    ~40 seconds (Selenium overhead)
  ├─ QQQ scraping:    ~40 seconds (Selenium overhead)
  ├─ VIX calculation: <1 second
  └─ Cache save:      <1 second

Phase 3.9 (Sync Technicals Tab): ~0.5 seconds
  ├─ Load files:      <0.1 seconds
  ├─ Sync data:       <0.2 seconds
  └─ Save & backup:   <0.2 seconds

Total: ~2-3 minutes (dominated by Selenium waits)
```

### Optimization Opportunities

1. **Parallel scraping**: Run SPY and QQQ scrapes simultaneously
2. **Headless browser**: Use headless Chrome to reduce overhead
3. **Browser reuse**: Share one browser instance across tickers
4. **Connection pooling**: Reuse HTTP connections
5. **Caching**: Cache Barchart page DOM between scrapings

### Recommended for Next Iteration

- Implement parallel scraping (could cut Phase 1.5 in half)
- Add headless mode (slight performance improvement)
- Consider alternative to Selenium for max pain data

---

## Key Concepts Recap

1. **Max Pain**: Strike price where option losses are maximized at expiration
2. **Key Levels**: Support/resistance zones calculated from option gamma exposure
3. **Put Wall**: High concentration of put open interest below current price (support)
4. **Call Wall**: High concentration of call open interest above current price (resistance)
5. **VIX Regime**: Volatility environment classification (helps risk management)
6. **Graceful Degradation**: Preserving manual data when automation fails

---

**Next Steps**: Implement Tasks 2-7 using this guide as reference
**Questions**: See Troubleshooting Guide section
**Updates**: Review monthly for API changes and performance improvements
