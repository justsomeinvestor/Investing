# Dynamic Analysis Panel - Command Center Guide

**Updated:** 2025-10-19
**Feature:** Live analysis results display with pin-to-persist functionality

---

## Overview

The Command Center now features a **Dynamic Analysis Panel** that:
- ✅ Displays analysis results in real-time
- ✅ Shows all components (TA, context, sentiment, volume, seasonality)
- ✅ Displays entry/stop/target levels
- ✅ PIN results to keep them on screen
- ✅ Persists pinned analyses across page reloads (localStorage)
- ✅ Auto-scrolls to analysis when results arrive

---

## How It Works

### 1. Running an Analysis

**In Conversation with Wingman:**
```
"wingman, analyze SPY"
```

**Result:**
- Analysis completes
- Dynamic panel appears (if not already visible)
- All data fills in automatically
- Panel auto-scrolls into view

### 2. Panel Contents

The analysis panel displays:

**Header Section:**
- Ticker name (large, blue)
- Signal (BUY/WAIT/AVOID - green if BUY)
- Probability score (0-100)

**Component Breakdown:**
- Technical Analysis (TA)
- Market Context
- Sentiment
- Volume
- Seasonality

**Trade Levels:**
- Entry price (blue)
- Stop price (red)
- Target price (green)
- Risk:Reward ratio (yellow)

**Additional Info:**
- Full reasoning/analysis narrative
- Data source (cache/live_api/simulated)
- Confidence level
- Position size (shares)

### 3. PIN Button - Keep Results On Screen

**Click PIN Button:**
- Button turns green: "📌 PINNED"
- Analysis saved to browser storage
- Result persists across page reloads
- Close button becomes inactive (protected)

**To Unpin:**
- Click PIN button again (turns back to yellow: "📌 PIN")
- Analysis can now be closed
- Storage is cleared

### 4. CLOSE Button

**Click CLOSE Button:**
- If NOT pinned: Panel closes/hides
- If pinned: Alert appears "Analysis is pinned. Click PIN to unpin before closing."

---

## Use Cases

### Scenario 1: Quick Analysis
```
User: "wingman, analyze NVDA"
→ Panel displays with NVDA analysis
→ User reviews
→ User closes (not needed after)
```

### Scenario 2: Compare Multiple Tickers
```
User: "wingman, analyze NVDA"
→ Panel shows NVDA
User: PIN analysis
→ Analysis stays on screen
User: "wingman, analyze TSLA"
→ New analysis displayed below/beside
User: Compare both visually
```

### Scenario 3: Reference During Trading
```
User: "wingman, analyze SPY"
→ PIN analysis
→ SPY setup stays visible all session
→ Refer back while trading
→ Close at end of day
```

### Scenario 4: Multi-Day Reference
```
User: "wingman, analyze QQQ" (Monday)
→ PIN analysis
→ Browser closes
User: Reopens site (Tuesday)
→ PINNED analysis still there!
→ Can refer back to Monday's analysis
```

---

## Technical Details

### Functions Available

**displayAnalysis(analysisData)**
- Called when analysis completes
- Populates all panel fields
- Shows the panel
- Auto-scrolls to it
- Resets pin state

**togglePinAnalysis()**
- Toggles pin on/off
- Changes button color
- Saves/clears localStorage
- Protects/unprotects close button

**closeAnalysis()**
- Hides panel if not pinned
- Prevents close if pinned (shows alert)

**restorePinnedAnalysis()**
- Runs on page load
- Checks localStorage for saved analysis
- Restores if found
- Re-attaches button handlers

### Data Storage

**localStorage Key:** `lastAnalysis`

**Stored Data:** Full panel HTML
- Includes all filled-in values
- Includes button states
- Survives browser restart
- Survives domain reload

**Cleared When:**
- User unpins analysis
- User clicks close on unpinned result
- localStorage manually cleared

---

## Visual Design

**Color Scheme:**
- Panel border: Green (#00ff41) when showing
- Ticker: Cyan (#00d4ff)
- Signal (BUY): Green (#00ff41)
- Probability: Orange (#ff6b35)
- Entry: Cyan (#00d4ff)
- Stop: Red (#ff0055)
- Target: Green (#00ff41)
- R:R: Orange (#ffb700)

**Layout:**
- Top: Header with PIN/CLOSE buttons
- Grid 1: Ticker | Signal | Probability
- Grid 2: Component scores (5 columns)
- Grid 3: Entry | Stop | Target | R:R
- Bottom: Reasoning + metadata

---

## Integration with Analysis Command

**How Results Get to Panel:**

1. User says: "wingman, analyze SPY"
2. Backend runs analysis
3. Returns JSON result
4. Frontend calls: `displayAnalysis(analysisResult)`
5. Panel populates and shows

**Expected JSON Format:**
```json
{
  "ticker": "SPY",
  "signal": "BUY",
  "probability_score": 71.5,
  "confidence": "GOOD",
  "data_source": "cache",
  "component_scores": {
    "technical_analysis": 80.0,
    "market_context": 55.0,
    "sentiment": 40.0,
    "volume": 50.0,
    "seasonality": 55.0
  },
  "levels": {
    "entry": 425.30,
    "stop": 423.50,
    "target": 429.80,
    "r_r_ratio": 2.1
  },
  "position_sizing": {
    "shares": 255
  },
  "reasoning": "Full reasoning text here..."
}
```

---

## Browser Compatibility

- Works on Chrome/Firefox/Safari/Edge
- Requires localStorage support (all modern browsers)
- Responsive design (adapts to mobile)

---

## Tips & Tricks

**Multiple Analyses:**
- Each new analysis OVERWRITES the previous (unless pinned)
- PIN before getting new analysis if you want to compare
- Can analyze different tickers one by one and PIN each

**Long Analysis Session:**
- PIN your best setups throughout the day
- Close others to keep dashboard clean
- Review all pinned analyses at end of day

**Archive Results:**
- PIN analysis before page refresh
- Analysis persists in localStorage
- Perfect for review next session

---

## Troubleshooting

**Panel not showing?**
- Check if it's been closed without data
- Refresh page to reset
- Run new analysis

**PIN not working?**
- Try clicking PIN again
- Check browser console for JS errors
- Clear localStorage and try again

**Analysis shows old data?**
- Unpin current analysis
- Run fresh analysis
- Confirm data source is "cache" or "live_api"

---

## Future Enhancements (Phase 3.2+)

- [ ] Export pinned analyses to PDF
- [ ] Multiple simultaneous analyses (tabs)
- [ ] Analysis history with timestamps
- [ ] Comparison view for side-by-side
- [ ] Alert when analysis meets criteria
- [ ] Custom pin notes/annotations

---

## See Also

- [QUICK_COMMANDS_GUIDE.html](QUICK_COMMANDS_GUIDE.html) - Full command reference
- [COMMAND_CENTER.md](COMMAND_CENTER.md) - System overview
- [command-center.html](command-center.html) - Live implementation
