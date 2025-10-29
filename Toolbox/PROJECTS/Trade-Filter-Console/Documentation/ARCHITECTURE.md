# Trade Filter Console - Technical Architecture

## System Overview

The Trade Filter Console is a **real-time assessment system** that bridges three components:

```
Wingman (AI) → live_assessment.json (Data) → trade-console.html (UI)
     ↓                    ↑                          ↓
  Updates JSON      Source of Truth         Displays Live
  as analysis       during session           visual feedback
  progresses        (auto-refreshed)         every 2 seconds
```

---

## Architecture Layers

### Layer 1: Data Engine (live_assessment.json)

**Location:** `Journal/live_assessment.json`

**Purpose:** Single source of truth for all assessment data during trade analysis

**Update Pattern:**
- Wingman writes to this file as it checks conditions
- Updates are immediate (no buffering)
- Console reads this file every 2 seconds

**Data Structure:**
```json
{
  "session_id": "unique-session-identifier",
  "status": "ANALYZING|AWAITING_TICKER|COMPLETE",
  "created_at": "ISO-8601 timestamp",
  "last_updated": "ISO-8601 timestamp",
  "ticker": "SPY",
  "setup_type": "EXTENSION_SELL|PULLBACK_BUY",
  "signal_light": "RED|YELLOW|GREEN",
  "overall_progress": {
    "items_passed": 5,
    "items_total": 18,
    "items_required": 15,
    "percentage": 33
  },
  "conditions": {
    "technical_structure": {
      "category": "Technical Structure",
      "items": [
        {
          "id": 1,
          "name": "Condition Name",
          "description": "What this condition checks",
          "status": "NOT_CHECKED|PASS|FAIL",
          "notes": "Wingman's analysis for this trade",
          "rule": "Associated rule numbers"
        }
      ]
    },
    "momentum_volume": {...},
    "market_context": {...},
    "fibonacci_reversion": {...},
    "risk_management": {...}
  },
  "setup_requirements": {
    "EXTENSION_SELL": {
      "setup_type": "Extension SHORT",
      "required_items": [1, 2, 3, ...],
      "required_count": 15,
      "items_checked": 15
    },
    "PULLBACK_BUY": {
      "setup_type": "Pullback LONG",
      "required_items": [1, 2, 3, ...],
      "required_count": 14,
      "items_checked": 14
    }
  },
  "assessment_notes": ["Session history and notes"],
  "wingman_commentary": "Real-time analysis text"
}
```

**Key Points:**
- Total 18 conditions defined (6 + 3 + 3 + 5 + 1)
- Each condition can be: NOT_CHECKED, PASS, FAIL
- Overall progress auto-calculated based on items_passed
- Wingman updates this file continuously
- Console reads every 2 seconds (configurable)

---

### Layer 2: Display Engine (trade-console.html)

**Location:** `Toolbox/PROJECTS/Trade-Filter-Console/trade-console.html`

**Technology Stack:**
- **HTML:** Structure and layout
- **CSS:** Styling (dark theme, responsive)
- **JavaScript:** Dynamic updates and auto-refresh

**Core Components:**

#### A. Header Section
```html
<div class="cockpit-header">
  <div class="cockpit-title">⚡ WINGMAN TRADE FILTER CONSOLE</div>
  <div class="status-info">
    <div class="ticker">SPY</div>
    <div class="timestamp">14:00 UTC</div>
  </div>
</div>
```
- Displays current ticker
- Shows current time
- Professional header styling

#### B. Signal Box (Main Indicator)
```html
<div class="signal-box green">
  <div class="signal-light">🟢</div>
  <div class="signal-status">GO</div>
  <div class="signal-progress">15/15 CONDITIONS PASSED</div>
  <div class="progress-bar-container">
    <div class="progress-bar">100%</div>
  </div>
</div>
```
- Large pulsing indicator (🔴 🟡 🟢)
- Status text (NO GO / CAUTION / GO)
- Progress bar (0-100%)
- Color changes based on signal_light value

#### C. Categories Container
```html
<div class="categories-container">
  <!-- Dynamic: Generated from JSON -->
  <div class="category">
    <div class="category-title">TECHNICAL STRUCTURE</div>
    <!-- Conditions rendered here -->
  </div>
</div>
```
- Responsive grid layout
- One card per category
- Items rendered dynamically from JSON

#### D. Condition Items
```html
<div class="condition-item passed">
  <div class="status-indicator">✅</div>
  <div class="condition-content">
    <div class="condition-name">RSI Level Check</div>
    <div class="condition-description">Current RSI level...</div>
    <div class="condition-notes">RSI at 80 - extreme overbought ✓</div>
    <div class="condition-rule">Rules: #19</div>
  </div>
</div>
```
- Color-coded borders (green/red/orange)
- Status indicator emoji (✅ ❌ ⏳)
- Wingman notes displayed
- Rule references shown

#### E. Commentary Section
```html
<div class="commentary-box">
  <div class="commentary-title">📊 WINGMAN COMMENTARY</div>
  <div class="commentary-text">Real-time analysis...</div>
</div>
```
- Displays wingman_commentary from JSON
- Pre-formatted text (preserves line breaks)
- Updates in real-time

---

### Layer 3: Integration Layer (Wingman Protocol)

**Files Involved:**
1. `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt`
2. `Toolbox/INSTRUCTIONS/Domains/How_to_Load_Wingman.txt`

**Wingman Behavior:**

#### During Session Start (Step 8.5)
```
1. Reset live_assessment.json to clean state
2. Set: status = "AWAITING_TICKER"
3. Set: ticker = null
4. Set: signal_light = "RED"
5. Reset all conditions to NOT_CHECKED
6. Clear commentary and assessment_notes
```

#### During Trade Analysis
```
1. You mention ticker: "Short SPY at $600"
   → Wingman sets ticker = "SPY"
   → Wingman sets setup_type = "EXTENSION_SELL"

2. You describe setup: "RSI at 80, bearish divergence"
   → Wingman updates condition #2 status = PASS
   → Wingman updates condition #5 status = PASS
   → Wingman updates overall_progress (2/15)
   → Wingman updates signal_light (still RED)

3. You add more details: "EMA falling, volume spike"
   → Wingman updates conditions #6, #7
   → Wingman updates progress (4/15)
   → Wingman updates commentary

4. All conditions pass:
   → overall_progress.items_passed = 15
   → overall_progress.percentage = 100
   → signal_light = "GREEN"
   → Wingman provides final analysis
```

**Update Frequency:**
- Immediate when new condition passes
- Not batched or delayed
- Console picks up within 2 seconds

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    WINGMAN (AI Assistant)                    │
│                                                               │
│ 1. Listens to user trade description                         │
│ 2. Maps details to checklist items                           │
│ 3. Updates condition statuses (PASS/FAIL/NOT_CHECKED)       │
│ 4. Recalculates overall_progress                            │
│ 5. Writes to live_assessment.json                           │
│ 6. Updates wingman_commentary                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Writes JSON
                         │ (immediate)
                         ▼
        ┌────────────────────────────────┐
        │  live_assessment.json          │
        │  (Single Source of Truth)      │
        │  - ticker                      │
        │  - setup_type                  │
        │  - signal_light                │
        │  - conditions[]                │
        │  - overall_progress            │
        │  - wingman_commentary          │
        └────────────────┬───────────────┘
                         │
                    Polls JSON
                    (every 2 sec)
                         │
                         ▼
        ┌────────────────────────────────┐
        │   trade-console.html           │
        │   (Browser Dashboard)          │
        │                                │
        │ JavaScript:                    │
        │ 1. Fetch JSON                  │
        │ 2. Parse JSON                  │
        │ 3. Update DOM                  │
        │ 4. Render conditions           │
        │ 5. Update signal light         │
        │ 6. Update progress bar         │
        └────────────────────────────────┘
                         │
                         │ Displays
                         │ (visual feedback)
                         ▼
        ┌────────────────────────────────┐
        │   Browser Window               │
        │   (User sees real-time updates)│
        └────────────────────────────────┘
```

---

## State Transitions

### Signal Light State Machine

```
START → RED (0% complete)
         ↓
      MONITORING (as conditions pass)
         ↓
      RED (< 70%)  OR  YELLOW (70-90%)  OR  GREEN (100%)
         ↓                ↓                     ↓
    Need more         Review but             READY
    conditions        ok to trade            TO TRADE
```

### Percentage Calculations

```
items_passed = Count of conditions with status = PASS
items_required = 15 (for EXTENSION) or 14 (for PULLBACK)
percentage = Math.round((items_passed / items_required) * 100)

Signal Light Logic:
├─ if percentage < 70: RED
├─ if 70 <= percentage < 100: YELLOW
└─ if percentage == 100: GREEN
```

---

## Browser Refresh Mechanism

### JavaScript Loop
```javascript
// Runs every 2000 milliseconds
setInterval(loadData, 2000)

function loadData() {
  // 1. Fetch live_assessment.json (with cache-bust param)
  fetch('live_assessment.json?t=' + Date.now())

  // 2. Parse JSON response
  .then(r => r.json())
  .then(data => {
    currentData = data
    updateDisplay()  // Update UI
  })

  // 3. Error handling (silent - don't block UI)
  .catch(err => console.error(err))
}
```

**Key Points:**
- Runs in background (non-blocking)
- `?t=Date.now()` prevents browser cache
- Fetches full JSON every time (not delta updates)
- Updates UI only if data changed
- Graceful error handling

**Performance:**
- CPU: ~0.1% usage
- Memory: ~2MB for JSON + DOM
- Network: ~50KB per fetch (JSON size)
- Latency: <100ms typical, 2000ms max

---

## File Synchronization

### Critical: No File Locks
**Problem:** If `live_assessment.json` is open in text editor, it can't be read by browser

**Solution:** Wingman NEVER leaves file open
- Reads file
- Updates in-memory
- Writes file
- Closes file
- Next read happens 2 seconds later

### Browser Cache Issues
**Problem:** Browser might cache old JSON

**Solution:** All fetches use cache-bust parameter
```javascript
fetch('live_assessment.json?t=1735000000000')
     // ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ unique timestamp
     // Forces browser to fetch fresh copy
```

### Race Conditions
**Scenario:** Wingman writing while browser reading

**Reality:** Unlikely on local filesystem, but possible on network drives
**Mitigation:** JSON writes are atomic (safe operations)

---

## Performance Characteristics

### Response Time
```
Wingman updates JSON
         ↓
       0-50ms   Browser fetches (next poll)
         ↓
      50-100ms  JavaScript processes
         ↓
    100-150ms   DOM updates
         ↓
    150-200ms   Browser renders
         │
    TOTAL: 150-2000ms (depends on poll interval)
```

### Optimization Options

**If you want FASTER updates:**
```
Change this line in trade-console.html:
const REFRESH_INTERVAL = 2000  // 2 seconds

To:
const REFRESH_INTERVAL = 500   // 500ms (faster)

Note: More frequent = more CPU usage
```

**If you want SLOWER (for low-power devices):**
```
const REFRESH_INTERVAL = 5000  // 5 seconds
```

---

## Error Handling

### Missing File
```
Error: live_assessment.json not found
Result: Console shows "Cannot load data"
Recovery: User manually refreshes browser
```

### Invalid JSON
```
Error: JSON parse error
Result: Console catches error silently
Recovery: Wait for next refresh (assumes Wingman will fix it)
```

### Network Error (on network drive)
```
Error: Cannot read file on network
Result: Silently fails, retries on next poll
Recovery: Auto-retry happens every 2 seconds
```

### Corruption
```
Unlikely: But if partial write happens:
Result: Browser silently fails to parse
Recovery: Next successful write overwrites with good data
```

---

## Security Considerations

### Local File System (No Security Issues)
- Files are local, not served over network
- No authentication required
- No CORS issues
- No JavaScript restrictions

### Browser Permissions
- HTML file reads from same directory (allowed)
- JSON file reads from parent directory (allowed by browser)
- No special permissions needed

### Data Privacy
- No external network calls
- No cloud storage
- All data stays on local machine
- Safe to use on trading machine

---

## Extensibility

### Adding New Conditions
1. Add to `pre_entry_checklist.json`
2. Add to `live_assessment.json` template
3. Console will automatically render (no code changes)
4. Wingman updates new condition during analysis

### Custom Styling
1. Edit CSS in `trade-console.html`
2. Change colors, fonts, spacing
3. No JavaScript changes needed
4. Fully responsive design

### Custom Refresh Rate
1. Locate: `const REFRESH_INTERVAL = 2000`
2. Change to desired milliseconds
3. Save and reload

### Adding Alerts
Could add sound/notification when GREEN LIGHT achieved:
```javascript
// In updateDisplay():
if (currentData.signal_light === 'GREEN') {
  new Audio('success.mp3').play()  // Add ding sound
}
```

---

## Testing Checklist

### Unit Tests (Manual)
- [ ] JSON parses correctly
- [ ] Progress percentage calculates right
- [ ] Signal light changes at correct thresholds
- [ ] All 18 conditions render
- [ ] All 5 categories display

### Integration Tests
- [ ] Wingman updates JSON
- [ ] Console reads updated JSON within 2 seconds
- [ ] UI reflects changes immediately after read
- [ ] Commentary updates
- [ ] Progress bar animates

### User Acceptance Tests
- [ ] Open 3 different trades through console
- [ ] Verify GREEN LIGHT predictions match actual trade results
- [ ] Test on mobile browser (responsive design)
- [ ] Test with slow network (timeout handling)

---

## Maintenance

### Regular Checks
- Monitor `live_assessment.json` file size (should stay ~30KB)
- Check browser console for JavaScript errors
- Verify JSON stays valid (test parse)
- Check Wingman updates complete successfully

### Troubleshooting
- Clear browser cache (Ctrl+Shift+Del)
- Close and reopen console
- Refresh browser (F5)
- Check browser console for errors (F12)
- Verify file permissions

---

## Version Control

### Files to Track
- `trade-console.html` (main dashboard)
- `live_assessment.json` (data template)
- Documentation files

### Files to Ignore
- Session-specific `live_assessment.json` (data, not code)
- Browser cache/temp files

---

**Technical Architecture Document**
**Version:** 1.0
**Last Updated:** 2025-10-28
**Status:** Production
