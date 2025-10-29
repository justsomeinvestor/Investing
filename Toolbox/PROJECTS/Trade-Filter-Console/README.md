# Trade Filter Console - Interactive Threat Assessment System

## Overview

The **Trade Filter Console** is an interactive, real-time visual dashboard that displays the pre-entry threat assessment checklist during trade analysis. As Wingman analyzes a potential entry, conditions "light up" on the console in real-time, providing visual confirmation of setup quality.

**Purpose:** Transform static checklist checking into a dynamic, visual confirmation system where you watch conditions pass before entering a trade.

---

## Quick Start

### 1. Open the Console
```
File: Toolbox/PROJECTS/Trade-Filter-Console/trade-console.html
Action: Open in your browser
```

### 2. Mention a Trade
```
You: "I want to short SPY at $600"
Wingman: Opens assessment and starts analyzing
```

### 3. Watch It Light Up
As you provide details, Wingman updates the conditions:
- ✅ RSI Level Check → lights up green
- ✅ Volume Check → lights up green
- ✅ Divergence → lights up green
- ...and so on

### 4. Check the Signal Light
- 🔴 **RED**: < 70% conditions passing → Do not enter
- 🟡 **YELLOW**: 70-90% conditions → Review before entry
- 🟢 **GREEN**: 100% conditions → Clear to enter

---

## System Architecture

### Core Components

#### 1. **live_assessment.json** (Data Engine)
- **Location:** `Journal/live_assessment.json`
- **Purpose:** Real-time assessment data
- **Updated by:** Wingman (automatic during trade discussion)
- **Read by:** trade-console.html (every 2 seconds)

**Key Fields:**
```json
{
  "ticker": "SPY",
  "setup_type": "EXTENSION_SELL",
  "signal_light": "RED",
  "overall_progress": {
    "items_passed": 3,
    "items_required": 15,
    "percentage": 20
  },
  "conditions": {
    "technical_structure": [...],
    "momentum_volume": [...],
    "market_context": [...],
    "fibonacci_reversion": [...],
    "risk_management": [...]
  },
  "wingman_commentary": "Real-time analysis text"
}
```

#### 2. **trade-console.html** (Visual Dashboard)
- **Location:** `Toolbox/PROJECTS/Trade-Filter-Console/trade-console.html`
- **Purpose:** Real-time visual display
- **Technology:** HTML/CSS/JavaScript (no server required)
- **Refresh Rate:** Every 2 seconds (auto-poll)

**Features:**
- Dark professional design (matches Command Center aesthetic)
- Main GO/NO-GO signal indicator
- 5 condition categories with color-coded items
- Progress bar (0-100%)
- Wingman commentary section
- Mobile-friendly responsive design

#### 3. **Wingman Integration**
- **Protocol File:** `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt`
- **Load File:** `Toolbox/INSTRUCTIONS/Domains/How_to_Load_Wingman.txt`
- **Behavior:** Auto-update live_assessment.json as you discuss trades

---

## How It Works

### The Workflow

1. **You Open Console**
   ```
   File → trade-console.html in browser
   Console shows: Awaiting Ticker, RED light, 0/0 conditions
   ```

2. **You Mention a Trade**
   ```
   You: "Short SPY at $600"
   Wingman: Initializes assessment for SPY short
   Wingman: Sets setup_type = "EXTENSION_SELL"
   Wingman: Resets conditions to NOT_CHECKED
   ```

3. **You Describe the Setup**
   ```
   You: "RSI at 80, bearish divergence, volume spike"
   Wingman: Checks each detail
   Wingman: Updates live_assessment.json with conditions that pass
   Console: Auto-refreshes every 2 seconds, shows updates
   ```

4. **Conditions Light Up**
   ```
   Console shows:
   ✅ RSI Level Check (80 = overbought)
   ✅ Divergence (price high, RSI low)
   ✅ Volume (spike confirmed)

   Progress: 3/15 (20%)
   Signal: Still 🔴 RED (need 15 total)
   ```

5. **Continue Analysis**
   ```
   You: "EMA falling, signal is STRONG"
   Wingman: Updates more conditions
   Console: More items light up
   Progress: 5/15 (33%)
   ```

6. **Final Decision**
   ```
   All 15 conditions pass (for EXTENSION_SELL)
   Signal: 🟢 GREEN
   Wingman: "Clear to enter. All 15/15 conditions confirmed."
   ```

---

## The 18-Condition Checklist

### Category 1: Technical Structure (6 items)
1. **C+R Confirmation** - Close+retest of key level
2. **RSI Level Check** - >80 or <20 (divergence risk)
3. **50% Fib Pullback Area** - At confluence zone
4. **127%/168% Extension** - At reversal zone
5. **Divergence Present** - Price vs momentum mismatch
6. **VWAP Extension Trigger** - Yellow/orange/red arrow

### Category 2: Momentum & Volume (3 items)
7. **EMA Filter** - 5-min 200 EMA direction
8. **Volume ≥ 1.3× average** - Conviction on entry
9. **ADD Confirmation** - Breadth alignment

### Category 3: Market Context (3 items)
10. **Signal Tier ≥ MODERATE** - System alignment
11. **Higher TF Alignment** - Daily/weekly trend
12. **Volatility Pattern** - Market regime

### Category 4: Fibonacci Reversion (5 items) - Rule #20
13. **At 127%-168% Extension?** - Extension zone
14. **Bearish Divergence Confirmed?** - 3-candle window
15. **VWAP Arrow?** - Mean reversion signal
16. **50%-61.8% Pullback Identified?** - Target zone
17. **Hard Level Confluence?** - Weekly pivot/support

### Category 5: Risk Management (1 item)
18. **Risk Calculated** - $231 max (1% account)

---

## Setup Requirements

### For EXTENSION_SELL (Short Setup)
- **Required:** 15 conditions must PASS
- **Conditions:** Items 1-12, 13-15, 18
- **Signal:** GREEN LIGHT when 15/15 pass

### For PULLBACK_BUY (Long Setup)
- **Required:** 14 conditions must PASS
- **Conditions:** Items 1-12, 16-17, 18
- **Signal:** GREEN LIGHT when 14/14 pass

---

## Design Features

### Visual Design
- **Color Scheme:** Professional dark blue with green accents
- **Background:** #0f1419 (Command Center match)
- **Primary Color:** #1db679 (operational green)
- **Alert Color:** #ff9d3e (orange/amber)
- **Error Color:** #ff6b6b (red)
- **Fonts:** System UI fonts (no monospace)

### Interactive Elements
- **Main Signal Box:** Large pulsing GO/NO-GO indicator
- **Progress Bar:** Orange→Green gradient (0-100%)
- **Condition Items:** Color-coded borders (green/red/orange)
- **Status Indicators:** ✅ PASS / ❌ FAIL / ⏳ NOT_CHECKED
- **Commentary Box:** Real-time Wingman analysis

### Technical Features
- ✅ **Auto-Refresh:** Polls live_assessment.json every 2 seconds
- ✅ **No Server:** Pure HTML/CSS/JavaScript
- ✅ **Works Offline:** Local file, no internet needed
- ✅ **Mobile-Friendly:** Responsive design
- ✅ **Fast Loading:** Minimal dependencies
- ✅ **Live Updates:** See conditions light up in real-time

---

## File Structure

```
Toolbox/PROJECTS/Trade-Filter-Console/
├── README.md (this file)
├── USAGE_GUIDE.md (step-by-step instructions)
├── trade-console.html (the dashboard - open in browser)
├── live_assessment.json (data template)
├── Test_Scenario_Example.md (full SPY example walkthrough)
│
└── Documentation/
    ├── ARCHITECTURE.md (technical details)
    ├── PROTOCOL_INTEGRATION.md (how it integrates with Wingman)
    └── DATA_SCHEMA.md (JSON structure reference)
```

---

## Key Integration Points

### 1. With Wingman Protocol
- **File:** `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt`
- **Section:** "TRADE FILTER CONSOLE - INTERACTIVE THREAT ASSESSMENT"
- **Behavior:** Wingman automatically updates console during trade discussions

### 2. With Load Workflow
- **File:** `Toolbox/INSTRUCTIONS/Domains/How_to_Load_Wingman.txt`
- **Step 8.5:** Initialize Trade Filter Console
- **Action:** Reset live_assessment.json to clean state at session start

### 3. With Pre-Entry Checklist
- **File:** `Journal/pre_entry_checklist.json`
- **Source of Truth:** Console displays these 18 conditions
- **Sync:** Both files reference same rules and criteria

---

## Usage Scenarios

### Scenario 1: Pre-Entry Analysis
- **When:** You're considering a trade entry
- **How:** Open console, describe setup to Wingman
- **Result:** Visual confirmation of setup quality before entry
- **Action:** Enter when GREEN LIGHT shows

### Scenario 2: Setup Learning
- **When:** You want to learn to spot quality setups
- **How:** Use console during analysis sessions
- **Result:** Visual reinforcement of what makes a "complete" setup
- **Action:** Study which conditions most often lead to winners

### Scenario 3: Post-Trade Review
- **When:** Analyzing why a trade failed
- **How:** Replay setup through console, check which conditions were missing
- **Result:** Identify setup weaknesses before they cost money
- **Action:** Create rules to avoid incomplete setups

### Scenario 4: Backtesting
- **When:** Analyzing historical trades
- **How:** Review old chart with console, manually check each condition
- **Result:** Understand which of your historical trades had "GREEN LIGHT" quality
- **Action:** Compare win rate of GREEN LIGHT trades vs others

---

## Performance Notes

### Console Performance
- **Refresh Rate:** Every 2 seconds (optimal balance)
- **File Polling:** Non-blocking, async reads
- **Memory:** Minimal (pure HTML/CSS/JS)
- **Network:** None required (local file only)

### Data Update Latency
- **Typical Delay:** <100ms from Wingman update to console display
- **Max Delay:** 2 seconds (auto-refresh interval)
- **Best Practice:** Keep browser visible while analyzing

---

## Troubleshooting

### Console Not Updating
**Problem:** Conditions not lighting up as you describe setup
**Solutions:**
1. Check browser console (F12) for JavaScript errors
2. Verify `live_assessment.json` is readable (not locked)
3. Verify trade-console.html was opened from correct location
4. Refresh browser (F5)
5. Check that Wingman is actually updating the JSON file

### Signal Light Stuck on RED
**Problem:** Conditions showing but signal won't turn GREEN
**Solutions:**
1. Count actual conditions passing (should show in progress bar)
2. Verify you need 15 (EXTENSION) not 14 (PULLBACK)
3. Check that all 15 items are actually PASS status (not PENDING)
4. Review commentary for which conditions still need work

### File Permission Issues
**Problem:** "Cannot read file" or "Permission denied"
**Solutions:**
1. Ensure `live_assessment.json` is not open in text editor
2. Check file is in correct location: `Journal/live_assessment.json`
3. Close any other programs accessing the file
4. Run browser with appropriate permissions

---

## Next Steps

1. **Read:** [USAGE_GUIDE.md](USAGE_GUIDE.md) for step-by-step instructions
2. **Review:** [Test_Scenario_Example.md](Test_Scenario_Example.md) to see a full example
3. **Explore:** [PROTOCOL_INTEGRATION.md](Documentation/PROTOCOL_INTEGRATION.md) for technical details
4. **Use:** Open trade-console.html and analyze your next trade

---

## Related Documentation

- **Wingman Protocol:** `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt`
- **How to Load Wingman:** `Toolbox/INSTRUCTIONS/Domains/How_to_Load_Wingman.txt`
- **Pre-Entry Checklist:** `Journal/pre_entry_checklist.json`
- **Risk Management:** `Toolbox/INSTRUCTIONS/Domains/Risk_Management_Framework.txt`
- **Trading Rules (Rule #20):** `Journal/wingman-continuity/rules_database.json`

---

## Version History

**v1.0 - 2025-10-28**
- Initial Trade Filter Console release
- 18-condition checklist implementation
- Real-time dashboard with auto-refresh
- Command Center aesthetic design
- Full integration with Wingman protocol

---

## Support

For questions or issues:
1. Check this README
2. Review the USAGE_GUIDE.md
3. Study the Test_Scenario_Example.md
4. Examine the protocol documentation
5. Ask Wingman during session (it has full knowledge of this system)

---

**Status:** Production Ready
**Last Updated:** 2025-10-28
**Maintained By:** Wingman Trading Partner
