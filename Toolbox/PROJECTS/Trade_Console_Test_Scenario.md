# Trade Filter Console - Test Scenario

## Overview
This document demonstrates the Trade Filter Console system in action with a real scenario. It shows how Wingman updates the console in real-time as a trade is analyzed.

---

## Test Scenario: SPY Short at Extension

### Initial State (Before Analysis)
**User opens:** `Journal/trade-console.html`
**Console displays:**
- Signal Light: 🔴 RED (NO GO)
- Progress: 0/15 conditions (0%)
- All conditions: ⏳ NOT_CHECKED

**Live Assessment JSON state:**
```json
{
  "status": "AWAITING_TICKER",
  "ticker": null,
  "signal_light": "RED",
  "setup_type": null,
  "overall_progress": { "items_passed": 0, "items_total": 0, "items_required": 15, "percentage": 0 }
}
```

---

## Step-by-Step Analysis Flow

### Message 1: User mentions the ticker and direction
**User:** "What about shorting SPY? Price just broke below $595."

**Wingman:**
- Detects: SPY short = EXTENSION_SELL setup
- Opens assessment session
- Updates live_assessment.json:
  ```json
  {
    "ticker": "SPY",
    "setup_type": "EXTENSION_SELL",
    "signal_light": "RED",
    "overall_progress": { "items_required": 15 }
  }
  ```

**Console updates:**
- Ticker: SPY (displayed at top)
- Signal: Still 🔴 RED (waiting for conditions to pass)

**Wingman Output:**
```
Copy that. SPY short at $595.

Let me analyze the setup against our 15-condition extension short checklist.
Initializing threat assessment...

[Console is now active - open trade-console.html to watch real-time updates]
```

---

### Message 2: User confirms the Close+Retest breakdown
**User:** "Price closed below $595 yesterday, and retested at $598 this morning before selling off. Clear breakdown."

**Wingman:**
- Checks Item #1: C+R Confirmation
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "technical_structure": {
        "items": [
          {
            "id": 1,
            "name": "C+R Confirmation",
            "status": "PASS",
            "notes": "Price closed below $595, retested $598, confirmed breakdown ✓"
          }
        ]
      }
    },
    "overall_progress": { "items_passed": 1, "percentage": 7 }
  }
  ```

**Console updates in real-time:**
- ✅ C+R Confirmation lights up green
- Progress bar: 1/15 (7%) - starts moving
- Signal: Still 🔴 RED (need more conditions)

**Wingman Output:**
```
✓ C+R Confirmation: Close below $595, retest at $598, breakdown confirmed.
  [1/15 conditions passing]
```

---

### Message 3: User mentions RSI and divergence
**User:** "RSI is at 83 - overbought. And I notice price made a higher high this morning but the RSI didn't confirm it. Classic bearish divergence."

**Wingman:**
- Checks Item #2: RSI Level Check
- Checks Item #5: Divergence Present
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "technical_structure": {
        "items": [
          { "id": 2, "name": "RSI Level Check", "status": "PASS", "notes": "RSI 83, overbought territory" },
          { "id": 5, "name": "Divergence Present?", "status": "PASS", "notes": "Price higher high, RSI lower - bearish divergence confirmed" }
        ]
      }
    },
    "overall_progress": { "items_passed": 3, "percentage": 20 }
  }
  ```

**Console updates in real-time:**
- ✅ RSI Level Check lights up
- ✅ Divergence Present lights up
- Progress bar: 3/15 (20%)
- Signal: Still 🔴 RED (need 70% threshold for yellow)

**Wingman Output:**
```
✓ RSI Level Check: RSI at 83, extreme overbought. Divergence risk confirmed.
✓ Divergence: Price higher high, RSI lower. Bearish momentum failure. 3-candle confirmation rule applies.
  [3/15 conditions passing]
```

---

### Message 4: User mentions volume
**User:** "Entry bar volume is 1.4 million shares, well above the 20-bar average of 900k. Strong conviction."

**Wingman:**
- Checks Item #7: Volume ≥ 1.3× 20-bar avg
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "momentum_volume": {
        "items": [
          { "id": 7, "name": "Volume ≥ 1.3× 20-bar avg", "status": "PASS", "notes": "1.4M entry bar vs 900k avg = 1.56x average ✓" }
        ]
      }
    },
    "overall_progress": { "items_passed": 4, "percentage": 27 }
  }
  ```

**Console updates in real-time:**
- ✅ Volume lights up
- Progress bar: 4/15 (27%)
- Signal: Still 🔴 RED

**Wingman Output:**
```
✓ Volume: 1.4M shares on entry bar, 1.56x the 20-bar average. Conviction confirmed.
  [4/15 conditions passing]
```

---

### Message 5: User mentions EMA and market context
**User:** "5-min 200 EMA is rolling over - falling nicely. And signal tier is STRONG (73/100) - we're aligned with system."

**Wingman:**
- Checks Item #6: EMA Filter
- Checks Item #9: Signal Tier ≥ MODERATE
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "momentum_volume": {
        "items": [
          { "id": 6, "name": "EMA Filter", "status": "PASS", "notes": "5-min 200 EMA falling - short direction confirmed" }
        ]
      },
      "market_context": {
        "items": [
          { "id": 9, "name": "Signal Tier ≥ MODERATE", "status": "PASS", "notes": "Signal STRONG (73/100) - fully aligned with system ✓" }
        ]
      }
    },
    "overall_progress": { "items_passed": 6, "percentage": 40 }
  }
  ```

**Console updates in real-time:**
- ✅ EMA Filter lights up
- ✅ Signal Tier lights up
- Progress bar: 6/15 (40%)
- Signal: Still 🔴 RED (but getting closer to 70%)

**Wingman Output:**
```
✓ EMA Filter: 5-min 200 EMA falling. Short aligned with trend momentum.
✓ Signal Tier: STRONG (73/100). Fully aligned with system. ✓
  [6/15 conditions passing]
```

---

### Message 6: User mentions Fibonacci extensions
**User:** "Price extended to exactly 127% of the prior pullback move. That's a textbook extension level."

**Wingman:**
- Checks Item #4: 127%/168% Extension Area
- Checks Item #13: At 127%-168% Extension (from Rule #20)
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "technical_structure": {
        "items": [
          { "id": 4, "name": "127% / 168% Extension Area", "status": "PASS", "notes": "Price at 127% extension of prior move - reversal zone ✓" }
        ]
      },
      "fibonacci_reversion": {
        "items": [
          { "id": 13, "name": "At 127%-168% Extension?", "status": "PASS", "notes": "Exactly 127% Fib extension - prime reversal area" }
        ]
      }
    },
    "overall_progress": { "items_passed": 8, "percentage": 53 }
  }
  ```

**Console updates in real-time:**
- ✅ 127%/168% Extension Area lights up
- ✅ At 127%-168% Extension lights up
- Progress bar: 8/15 (53%)
- Signal: 🔴 Still RED but now clearly progressing

**Wingman Output:**
```
✓ Fib Extensions: Price at 127% extension - textbook reversal zone.
✓ Rule #20 Extension: Fibonacci reversion framework triggered.
  [8/15 conditions passing - Over halfway there]
```

---

### Message 7: User confirms VWAP signal
**User:** "VWAP script just gave me a yellow arrow - mean reversion signal. Price extending above the bands."

**Wingman:**
- Checks Item #5b: VWAP Extension Trigger
- Checks Item #15: VWAP Yellow/Orange/Red Arrow
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "technical_structure": {
        "items": [
          { "id": "5b", "name": "VWAP Extension Trigger", "status": "PASS", "notes": "VWAP yellow arrow signal - mean reversion opportunity ✓" }
        ]
      },
      "fibonacci_reversion": {
        "items": [
          { "id": 15, "name": "VWAP Yellow/Orange/Red Arrow?", "status": "PASS", "notes": "Yellow arrow on VWAP script - Rule #20 signal ✓" }
        ]
      }
    },
    "overall_progress": { "items_passed": 10, "percentage": 67 }
  }
  ```

**Console updates in real-time:**
- ✅ VWAP Extension Trigger lights up
- ✅ VWAP Yellow Arrow lights up
- Progress bar: 10/15 (67%)
- Signal: Still 🔴 RED (just below 70% for yellow)

**Wingman Output:**
```
✓ VWAP Mean Reversion: Yellow arrow signal. Price extended above bands. Rule #20 engaged.
✓ VWAP Arrow: Official mean reversion trigger confirmed.
  [10/15 conditions passing - Almost there!]
```

---

### Message 8: User confirms remaining technical conditions
**User:** "ADD line is clearly rolling over - declining. Daily trend is still down. No strong breadth. And volatility is expanding - good for reversals."

**Wingman:**
- Checks Item #8: ADD Confirmation
- Checks Item #10: Higher TF Alignment
- Checks Item #11: Volatility Pattern
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "momentum_volume": {
        "items": [
          { "id": 8, "name": "ADD Confirmation", "status": "PASS", "notes": "Advance-Decline declining - breadth not confirming rally" }
        ]
      },
      "market_context": {
        "items": [
          { "id": 10, "name": "Higher TF Alignment", "status": "PASS", "notes": "Daily still in downtrend. Aligned with short bias" },
          { "id": 11, "name": "Volatility Pattern", "status": "PASS", "notes": "Volatility expanding - good for reversal moves" }
        ]
      }
    },
    "overall_progress": { "items_passed": 13, "percentage": 87 }
  }
  ```

**Console updates in real-time:**
- ✅ ADD Confirmation lights up
- ✅ Higher TF Alignment lights up
- ✅ Volatility Pattern lights up
- Progress bar: 13/15 (87%)
- **Signal: 🟡 YELLOW LIGHT** (caution - missing 2 conditions)

**Wingman Output:**
```
✓ ADD Confirmation: Declining. Breadth not confirming.
✓ Higher TF Alignment: Daily downtrend continues. Aligned.
✓ Volatility Pattern: Expanding volatility - good for reversals.
  [13/15 conditions passing]

🟡 YELLOW LIGHT: Almost there. Missing 2 conditions from Fibonacci reversion framework.
What about items #14 and #16-17?
```

---

### Message 9: User confirms bearish divergence and pullback levels
**User:** "The divergence definitely confirmed over 3 candles - price kept going up but momentum didn't. Clear failure. And if we short here, the 50% pullback would be around $580 - that's exactly at the weekly pivot."

**Wingman:**
- Checks Item #14: Bearish Divergence Confirmed (within Rule #19 3-candle window)
- Checks Item #16: 50%-61.8% Pullback Identified
- Checks Item #17: Hard Level Confluence Present
- Updates live_assessment.json:
  ```json
  {
    "conditions": {
      "fibonacci_reversion": {
        "items": [
          { "id": 14, "name": "Bearish Divergence Confirmed?", "status": "PASS", "notes": "3+ candles confirmed - momentum failure validated ✓" },
          { "id": 16, "name": "50%-61.8% Pullback Identified?", "status": "PASS", "notes": "50% pullback = $580 level identified" },
          { "id": 17, "name": "Hard Level Confluence Present?", "status": "PASS", "notes": "$580 = weekly pivot. Hard level confirmed ✓" }
        ]
      }
    },
    "overall_progress": { "items_passed": 16, "items_required": 15, "percentage": 107 }
  }
  ```

**Console updates in real-time:**
- ✅ Bearish Divergence Confirmed lights up
- ✅ 50% Pullback Identified lights up
- ✅ Hard Level Confluence lights up
- Progress bar: **15/15 (100%)** - **COMPLETE**
- **Signal: 🟢 GREEN LIGHT** (GO)

**Wingman Output:**
```
✓ Bearish Divergence: 3+ candles confirmed. Momentum failure validated.
✓ Pullback Level: 50% reversion = $580. Weekly pivot confluence.

═══════════════════════════════════════════════════════════════════
🟢 GREEN LIGHT - ALL 15/15 CONDITIONS PASS
═══════════════════════════════════════════════════════════════════

Setup Summary:
  • Close+retest breakdown: ✓
  • RSI overbought with divergence: ✓
  • Strong volume (1.56x avg): ✓
  • EMA falling: ✓
  • Signal STRONG (73/100): ✓
  • Price at 127% Fib extension: ✓
  • VWAP yellow arrow: ✓
  • ADD declining: ✓
  • Daily aligned: ✓
  • Volatility expanding: ✓
  • Divergence confirmed (Rule #19): ✓
  • Pullback target at $580 (weekly pivot): ✓

Risk Calculation:
  • Entry: $595.00
  • Stop: $597.50 (ATR-based, above high)
  • Risk: $2.50 per share = $250 total... wait

Wingman Check: Risk is exactly $250. That's the daily loss limit.
For 1% ($231), position size would be 92 shares.

Clear to enter SPY short 92 @ $595?
```

---

## Console Display at Completion

**Main Signal Box:**
```
🟢 GREEN LIGHT - GO

15/15 CONDITIONS PASSED (100%)
═════════════════════════════

ALL CONDITIONS READY FOR ENTRY
```

**Condition Categories (All Green):**

**Technical Structure:**
- ✅ C+R Confirmation: Close below $595, retest $598, confirmed breakdown
- ✅ RSI Level Check: RSI 83, extreme overbought
- ✅ 50% Fib Pullback: $580 level identified
- ✅ 127%/168% Extension: Price at 127% extension
- ✅ Divergence: Price higher, RSI lower - bearish
- ✅ VWAP Trigger: Yellow arrow signal

**Momentum & Volume:**
- ✅ EMA Filter: 5-min 200 EMA falling
- ✅ Volume: 1.4M shares, 1.56x average
- ✅ ADD Confirmation: Declining

**Market Context:**
- ✅ Signal Tier: STRONG (73/100)
- ✅ Higher TF Alignment: Daily downtrend
- ✅ Volatility: Expanding

**Fibonacci Reversion (Rule #20):**
- ✅ At 127% Extension: Yes, textbook level
- ✅ Bearish Divergence: Confirmed (3+ candles)
- ✅ VWAP Arrow: Yellow triggered
- ✅ 50% Pullback: $580 identified
- ✅ Hard Level: Weekly pivot at $580

**Risk Management:**
- ✅ Risk: $231 (1% account)

**Wingman Commentary:**
```
All 15/15 conditions pass for extension short.

Setup quality: EXCELLENT
• Multi-confluence reversal at extension zone
• Bearish divergence with Rule #19 3-candle confirmation
• Fib extension (127%) + VWAP mean reversion alignment
• Risk/reward well-defined ($580 pullback target)
• Position sizing: 92 shares @ $595, stop $597.50
• Risk: $231 (1% account)

GREEN LIGHT - Clear to enter SPY short.
```

---

## Key Learning Points from This Test

1. **Real-Time Updates**: Console updated with each piece of analysis, showing progress in real-time
2. **Condition Checking**: Conditions light up as they're confirmed, creating visual confidence
3. **Clear Signal**: When 15/15 pass, signal changes from RED → YELLOW → GREEN with clear indicator
4. **Risk Calculation**: Wingman automatically calculates position size based on ATR and risk rules
5. **Commentary**: Clear English explanation of what each condition means and why it matters
6. **Rule Integration**: Console tied to specific rules (#7, #9, #18, #19, #20, etc.)
7. **Entry Readiness**: User has complete visual confirmation before entering trade

---

## Next Session: Closing the Loop

When user exits the trade, Wingman would:
1. Record the exit in positions.json
2. Calculate actual P/L
3. Compare actual performance vs. the "GREEN LIGHT" prediction
4. Log compliance metrics
5. Note any lessons learned

This creates a feedback loop: Better setups → Better GREEN LIGHT signal → Higher win rates → Better discipline

---

## Files Involved in This System

- **live_assessment.json** - Updated by Wingman throughout analysis (every message)
- **trade-console.html** - Displays updates in real-time (refreshes every 2 seconds)
- **pre_entry_checklist.json** - Source of truth for condition definitions
- **Journal_Trading_Partner_Protocol.txt** - Wingman behavior rules
- **How_to_Load_Wingman.txt** - Console initialization step

System is fully operational. Ready to use.
