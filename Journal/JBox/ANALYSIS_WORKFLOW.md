# Analysis Workflow - Complete Guide

**Updated:** 2025-10-19
**Status:** Ready to integrate with backend

---

## Complete Analysis Workflow

### 1. User Initiates Analysis

**In Conversation:**
```
"wingman, analyze SPY"
```

### 2. Backend Processing

**The system should:**
1. Run `analyze_ticker_v2.py` with ticker='SPY'
2. Generate analysis result (JSON)
3. Send result to frontend

### 3. Frontend Display

**JavaScript function receives:**
```javascript
displayAnalysis({
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
    "reasoning": "Strong technical setup..."
})
```

**Panel automatically:**
1. Shows and populates all fields
2. Color-codes the display
3. Auto-scrolls into view
4. Ready for user interaction

### 4. User Options

**Option A: Review & Close**
```
1. Review analysis on screen
2. Click CLOSE button
3. Panel hides
4. Ready for next analysis
```

**Option B: Keep Reference (PIN)**
```
1. Review analysis
2. Click PIN button
3. Button turns green: "📌 PINNED"
4. Analysis locked in place
5. Can request new analysis
6. Can compare multiple
```

**Option C: Compare Multiple**
```
1. "wingman, analyze SPY" → displayed
2. Click PIN
3. "wingman, analyze QQQ" → displayed next/below
4. Now see both side-by-side
5. Can PIN both
6. Can close individually
```

### 5. Persistence Across Sessions

**When user closes browser:**
```
Pinned analysis stays in browser storage
```

**When user reopens site next day:**
```
Pinned analysis automatically restores
Can still refer to yesterday's analysis
```

**To clear:**
```
Click PIN button to unpin
Close button becomes active
Click CLOSE to remove
```

---

## Integration Points

### Backend → Frontend Communication

**Required JSON Structure:**
```json
{
    "ticker": "string",
    "signal": "BUY|WAIT|AVOID",
    "probability_score": "number (0-100)",
    "confidence": "string",
    "data_source": "cache|live_api|simulated",
    "component_scores": {
        "technical_analysis": "number",
        "market_context": "number",
        "sentiment": "number",
        "volume": "number",
        "seasonality": "number"
    },
    "levels": {
        "entry": "number",
        "stop": "number",
        "target": "number",
        "r_r_ratio": "number"
    },
    "position_sizing": {
        "shares": "number"
    },
    "reasoning": "string"
}
```

### Frontend Function Signature

```javascript
function displayAnalysis(analysisData) {
    // Called when backend returns analysis result
    // Populates panel with data
    // Shows/auto-scrolls panel
    // Resets pin state
}

function togglePinAnalysis() {
    // Called when PIN button clicked
    // Toggles pin state
    // Saves to localStorage if pinning
    // Changes button appearance
}

function closeAnalysis() {
    // Called when CLOSE button clicked
    // Checks if pinned (prevent if so)
    // Hides panel
}

function restorePinnedAnalysis() {
    // Called on page load
    // Checks localStorage
    // Restores pinned analysis if found
}
```

---

## Status Feedback System (To be added)

### Planned Status Bar (in header)

**Status Fields:**
- Data Collector: RUNNING / STOPPED
- Cache Status: FULL / EMPTY / STALE
- Last Update: timestamp
- Tickers Tracked: count (e.g., "5")
- API Usage: calls used (e.g., "12 / 60")
- Analysis Status: READY / ANALYZING / ERROR

### How Status Updates

**When collector starts:**
```javascript
updateStatus({
    collector: 'RUNNING',
    cache: 'STALE',
    tickers: 2,
    lastUpdate: null
})
```

**After collection completes:**
```javascript
updateStatus({
    collector: 'RUNNING',
    cache: 'FRESH',
    tickers: 2,
    lastUpdate: '14:30:00',
    apiUsage: '12 / 60'
})
```

**When analysis runs:**
```javascript
updateStatus({
    analysis: 'ANALYZING'
})
// Then after complete:
updateStatus({
    analysis: 'READY'
})
```

---

## Example Workflows

### Morning Session

**Time: 09:00**
```
User: "wingman, start collector"
Status: Collector → RUNNING
User: "wingman, signal"
Result: BUY signal displayed
```

**Time: 09:05**
```
Status: Cache → FRESH (just updated)
User: "wingman, analyze SPY"
Result: SPY analysis displayed
User: Clicks PIN
Result: SPY analysis locked in place
```

**Time: 09:10**
```
User: "wingman, analyze QQQ"
Result: QQQ analysis displayed (SPY still pinned above)
User: Clicks PIN on QQQ too
Result: Both analyses locked in place for comparison
```

**Time: 16:00**
```
User: "wingman, stop collector"
Status: Collector → STOPPED
User: "wingman, eod wrap"
Result: EOD summary displayed
User: Closes unpin analyses
```

### Afternoon Session (Multi-Day)

**Time: Next Day 09:00**
```
User: Opens command center
Result: Yesterday's pinned analyses automatically restored
User: Reviews previous analyses
User: "wingman, start collector"
Status: Collector → RUNNING
User: "wingman, analyze NVDA"
Result: New NVDA analysis displayed (old analyses still pinned above for reference)
```

---

## Visual Layout

### Panel Arrangement

```
┌─────────────────────────────────────────────────────────┐
│ 📊 Live Analysis Result        [📌 PIN] [✕ CLOSE]       │
├─────────────────────────────────────────────────────────┤
│ Ticker: SPY    │  Signal: BUY    │  Probability: 71.5%  │
├─────────────────────────────────────────────────────────┤
│           Component Breakdown (5-column grid)            │
│  TA: 80  │  Context: 55  │  Sentiment: 40  │  ...      │
├─────────────────────────────────────────────────────────┤
│ Entry: $425.30  │  Stop: $423.50  │  Target: $429.80   │
│                 R:R: 1:2.1                              │
├─────────────────────────────────────────────────────────┤
│ Reasoning: [Full analysis narrative]                    │
├─────────────────────────────────────────────────────────┤
│ Data: cache | Confidence: GOOD | Position: 255 shares  │
└─────────────────────────────────────────────────────────┘
```

### Color Coding

| Element | Color | Meaning |
|---------|-------|---------|
| Ticker | Cyan | Informational |
| Signal | Green/Yellow/Red | BUY/WAIT/AVOID |
| Entry | Cyan | Entry price |
| Stop | Red | Stop loss |
| Target | Green | Take profit |
| R:R | Orange | Risk:reward ratio |
| PIN Button (active) | Green | Pinned |
| PIN Button (default) | Yellow | Ready to pin |

---

## User Stories

### Story 1: Quick Check
```
"wingman, analyze NVDA"
→ [Review panel]
→ [Click CLOSE]
→ [Panel hides]
Done: Takes 10 seconds
```

### Story 2: Setup Reference
```
"wingman, analyze QQQ"
→ [Review panel]
→ [Click PIN]
→ "wingman, analyze AAPL"
→ [Compare both on screen]
→ [Click CLOSE on AAPL]
→ [Keep QQQ pinned for trading]
Done: Can trade with reference
```

### Story 3: Multi-Day Analysis
```
Day 1: "wingman, analyze SPY" → PIN
Day 2: Browser opens → SPY analysis restored
→ "wingman, analyze TSLA"
→ Now see both Day 1 SPY and new TSLA analysis
→ Can remove Day 1 SPY when done
Done: Historical reference across sessions
```

---

## Technical Notes

### localStorage Keys
- `lastAnalysis` - Stores full pinned panel HTML

### Functions in command-center.html
- `displayAnalysis(data)` - Shows analysis result
- `togglePinAnalysis()` - PIN/UNPIN functionality
- `closeAnalysis()` - Hide panel
- `restorePinnedAnalysis()` - Auto-restore on load

### Browser Requirements
- localStorage support (all modern browsers)
- JavaScript enabled
- Responsive CSS grid layout

---

## Next Steps

1. **Backend Integration**: Modify Wingman persona to call `displayAnalysis()` when analysis completes
2. **Status Bar**: Add status feedback header showing collector/cache/API status
3. **History**: Optional - add timestamp to each pinned analysis
4. **Export**: Optional - export pinned analyses to PDF

---

See Also:
- [command-center.html](command-center.html) - Live implementation
- [DYNAMIC_ANALYSIS_GUIDE.md](DYNAMIC_ANALYSIS_GUIDE.md) - User guide
- [QUICK_COMMANDS_GUIDE.html](QUICK_COMMANDS_GUIDE.html) - Command reference
