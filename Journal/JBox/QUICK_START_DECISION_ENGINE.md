# ⚡ Quick Start - Decision Engine

## 30-Second Setup

```bash
# 1. Open terminal
# 2. Navigate to scripts folder
cd C:\Users\Iccanui\Desktop\Investing\scripts

# 3. Start server
python server.py

# 4. Open browser
http://localhost:8888

# 5. Type ticker and press ENTER
```

Done! ✅

---

## How It Works

```
You type:  SPY
    ↓
Backend runs 5 analyses:
  • Technical Analysis (75/100)
  • Market Context (68/100)
  • Sentiment (70/100)
  • Volume (72/100)
  • Seasonality (65/100)
    ↓
Calculates probability: 71.5%
    ↓
Decision: BUY ✅
    ↓
Shows levels:
  Entry: $585.50
  Stop: $583.25
  Target: $591.75
  R:R: 1:2.1
```

---

## 5 Component Scores Explained

| Component | What It Measures | Example |
|-----------|------------------|---------|
| **TA** | Chart patterns, support/resistance, momentum | 75 = Strong uptrend |
| **Context** | SPY/QQQ/VIX market conditions | 68 = Market is mixed |
| **Sentiment** | News, fear, greed indicators | 70 = Optimistic |
| **Volume** | Trade volume confirmation | 72 = Volume confirms move |
| **Seasonality** | Time-based patterns (day/month/year) | 65 = Decent seasonality |

**Higher score = stronger signal**

---

## Understanding the Result

### BUY Signal (67-100%)
- Probability is high enough to trade
- Follow the entry/stop/target levels
- Risk/reward is favorable (usually 1:1.5 or better)

### WAIT Signal (50-67%)
- Market is mixed/uncertain
- Don't force a trade
- Wait for more clarity

### AVOID Signal (0-50%)
- Risk is too high vs potential reward
- Skip this trade
- Look for better setup

---

## Example Trade: NVDA at 54.2% (WAIT)

```
Signal: WAIT

Interpretation:
- Probability is 54.2% (just above 50%)
- This is borderline - could go either way
- Better setups available

What to do:
- Don't trade yet
- Wait for NVDA to either:
  a) Break above resistance with volume
  b) Drop with selling pressure
- Re-analyze when more clarity emerges

If forced to trade:
- Entry: $189.75
- Stop: $187.50 (acceptable loss of $2.25)
- Target: $195.00 (potential gain of $5.25)
- But risk/reward is only 1:1.85 (weak)
- Position size: 0 (engine doesn't suggest)
```

---

## Data Sources

### Current (Simulated)
- Signal: ✅ Works perfectly
- Numbers: Generated but realistic
- Use for: Testing, learning, system validation

### When Running Data Collector
```bash
python scripts/trading/data_collector.py
```
- Signal: Real market data
- Numbers: Live from Finnhub API
- Shows as `data_source: "cache"`

### Fallback (API Direct)
- Used when cache is empty
- Slightly slower (~3 seconds)
- But real market data

---

## Testing the System

### Quick Test
1. Type `SPY` → Press ENTER → Should show BUY
2. Type `TSLA` → Press ENTER → Should show different signal
3. Click **📊 Test NVDA** → Should show WAIT
4. Click **🎲 Random Ticker** → Analyzes random stock

### Expected Results
- **SPY**: BUY at ~71%
- **QQQ**: BUY at ~68%
- **NVDA**: WAIT at ~54%
- **TSLA**: AVOID at ~39%

(With simulated data - will differ with real data)

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Analyze Ticker | Type ticker + ENTER |
| Focus Input | Click input box |
| Clear Input | Click 🗑️ CLEAR or Ctrl+A, Delete |
| Close Analysis | Click ✕ CLOSE |
| Pin Analysis | Click 📌 PIN |

---

## What's Actually Running

### Backend (Python)
```
scripts/server.py
  ↓
  Serves HTML + API
  ↓
  Calls: analyze_ticker_v2.py
  ↓
  Runs decision engine
  ↓
  Returns JSON
```

### Frontend (JavaScript)
```
command-center.html
  ↓
  Gets your input
  ↓
  Calls: /api/analyze/<ticker>
  ↓
  Renders results
  ↓
  Shows on page
```

---

## Common Questions

**Q: Can I analyze any ticker?**
A: Yes! Enter any valid stock symbol. Currently using simulated data, but infrastructure is ready for real data.

**Q: Why does first analysis take 2-3 seconds?**
A: Engine running 5 different calculations. Subsequent analyses use caching.

**Q: Are these real results?**
A: Logic is real (actual decision engine from analyze_ticker_v2.py), data is simulated. Switch to real data once data collector runs.

**Q: Can I trade these signals?**
A: Not yet. First validate the system works for you, then enable real data, then paper trade to verify results.

**Q: What if I'm away from computer?**
A: Pin analysis (📌 PIN) to save it. Comes back when you reload page.

---

## Next Steps

1. ✅ Start server: `python scripts/server.py`
2. ✅ Open: `http://localhost:8888`
3. ✅ Try 5-10 different tickers
4. ✅ Compare signals with your own analysis
5. ✅ Read `DECISION_ENGINE_INTEGRATION.md` for deep dive
6. ⏭️ Enable real data when ready

---

## API for Power Users

### Analyze single ticker
```bash
curl http://localhost:8888/api/analyze/NVDA
```

### Analyze multiple tickers
```bash
curl -X POST http://localhost:8888/api/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["SPY", "QQQ", "NVDA"]}'
```

### Get market context
```bash
curl http://localhost:8888/api/market-context
```

---

## Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| "Connection Error" | Start server: `python scripts/server.py` |
| "Analysis Error" | Check ticker spelling (must be valid symbol) |
| Page won't load | Try `http://127.0.0.1:8888` instead of localhost |
| Results not showing | Check browser console (F12) for errors |

---

**Ready? Start here:**

```bash
python scripts/server.py
# Then go to: http://localhost:8888
```
