# Intraday Trading System - Complete Documentation

## Overview

This folder contains the complete intraday daytrading system for 5-min, 15-min, and 1-hour timeframe trades. It integrates with your existing Rules #0-20 and adds intraday-specific protocols.

---

## Files in This Folder

### 1. `intraday_signals.json` (Live Trading)
**Purpose:** Real-time tracking of active intraday setups

**What gets tracked:**
- Active signals pending entry (5-10 max at any time)
- Market context (VIX, ADD, $TICK, session time)
- Signal metadata (ticker, setup type, timeframe, confluences)
- Entry criteria validation (VWAP, RSI, volume, EMA, breadth)
- Multi-timeframe alignment score
- Risk management pre-sets (stop, target, position size)
- Pre-entry checklist status (Go/No-Go)

**How to use:**
1. During trading, you spot setup and say: "Wingman, log intraday signal: SPY VWAP reversion 5-min red arrow RSI 82 breadth weak"
2. Wingman parses and writes to this JSON
3. Dashboard auto-refreshes with new signal card
4. You review checklist, confluences, risk/reward
5. If Go signal = execute trade
6. When closed, say: "Close signal [ID]: [exit price] [outcome]"

**Data retention:** Current day's signals. Closed signals move to learning_database.json

---

### 2. `intraday_learning_database.json` (Historical Record)
**Purpose:** Long-term tracking of ALL intraday trades for pattern recognition

**What gets stored:**
- Complete trade records (entry/exit, P&L, bars held)
- Setup effectiveness by type (VWAP: 70% win rate, ORB: 60%, etc.)
- Confluence effectiveness (which combinations most predictive)
- Market regime performance (trending vs choppy vs volatile)
- Session performance (which times of day most profitable)
- Timeframe analysis (5-min vs 15-min vs 1-hour)
- Checklist compliance correlation

**How it grows:**
```
Day 1-5: 5-10 trades (data collection)
Day 6-10: 10-20 trades (patterns emerge)
Day 11-30: 30-50 trades (statistical reliability)
Month 2: 50-100 trades (confident edge identification)
Month 3+: 100+ trades (system optimization ready)
```

**How to use the data:**
- Weekly: Review win rate by setup type
- Monthly: Analyze by market regime, session time
- Quarterly: Calculate overall profitability, decide scaling

---

## Workflow: How to Log Intraday Trades

### Step 1: Signal Appears During Trading
You're watching 5-min chart, you see VWAP red arrow + divergence + breadth weakness.

### Step 2: Log to Wingman (Chat Interface)
```
"Wingman, log intraday signal: SPY VWAP reversion 5-min red arrow RSI 82 breadth weak"
```

### Step 3: Wingman Parses & Adds to JSON
- Extracts: SPY, VWAP reversion, 5-min, RSI 82, ADD negative
- Validates: 3+ confluences present? ✓
- Writes to: intraday_signals.json with timestamp
- Dashboard: Auto-refreshes with signal card

### Step 4: Review Pre-Entry Checklist
- Open intraday-command-center.html
- Check all 18 items
- If 17/18 checked = GO signal (green)
- If <15/18 = CAUTION or NO-GO (red)

### Step 5: Calculate Risk/Reward
- Entry: 684.50
- Stop: 685.50 (extension high)
- Position: 154 shares
- Risk: $154 (1% account)
- Target: 680.00 (50% pullback)
- Reward: $462 (3% account)
- R/R: 1:3 (excellent)

### Step 6: Execute Trade
- Place order
- Set stop-loss at $12.38
- Set target at $12.20
- Watch for entry confirmation

### Step 7: Trade Closed
Exit at stop hit or target reached. Say to Wingman:
```
"Close signal 20251029-001: 682.50 loss"
```

### Step 8: Wingman Records to Learning Database
- Moves signal to closed_signals
- Calculates P&L
- Updates learning_database.json
- Recalculates win rates for setup type
- Updates confluence effectiveness

---

## Integration with Existing Systems

### Your Existing Rules (Unmodified)
- **Rule #0:** Confluence Framework (use intraday confluences)
- **Rule #7, #9:** C+R Confirmation (apply to intraday timeframes)
- **Rule #19:** Divergence Confirmation (3-candle window for 5-min, standard for 15-min/1-hour)
- **Rule #20:** Fibonacci Reversion (core system for intraday + swing)

### New Intraday Rules (Added)
- **Rule #21:** Multi-Timeframe Confirmation (align 5-min, 15-min, 1-hour)
- **Rule #22:** Session-Specific Sizing (100%/100%/50%/100-125%/0% by time)
- **Rule #23:** Daily Loss Limit (stop trading at -2% = -$500)
- **Rule #24:** Pre-Entry Checklist (18 items, all must pass for Go signal)

### Andy Integration
- Morning: Load Andy's daily levels (from andy_intel_tracking.json)
- Intraday: Check if your setup aligns with Andy's called level
- If aligned: +1 confluence score
- EOD: Validate which Andy levels held for next session

### Main Dashboard
- Link from: command-center.html "INTRADAY CENTER" button
- Returns to: link back to command-center.html
- Separate P&L tracking (intraday ≠ swing)

---

## The 18-Item Pre-Entry Checklist

Every trade must pass this before entry:

```
SETUP IDENTIFICATION:
☐ 1. Primary setup type identified (VWAP/ORB/C+R/Fib)?
☐ 2. Secondary confluence(s) present (minimum 3 total)?
☐ 3. Multi-timeframe alignment confirmed?
☐ 4. Confluence count >= 3 (Go/No-Go signal)?

TECHNICAL VALIDATION:
☐ 5. Divergence confirmed within 3-candle window?
☐ 6. Volume >= 1.3x average on entry bar?
☐ 7. EMA filter passed (200 EMA aligned)?
☐ 8. VWAP status aligned with thesis (arrow color correct)?

RISK MANAGEMENT:
☐ 9. Stop price clearly defined (mechanical, no subjective)?
☐ 10. Risk amount calculated (<= 1% account = $231 max)?
☐ 11. Target price pre-set (before entry)?
☐ 12. Position size calculated from risk?

MARKET CONTEXT:
☐ 13. Session time favorable (not lunch chop)?
☐ 14. Breadth/ADD aligned (not counter-trend)?
☐ 15. VIX regime noted (adjust stops/size by regime)?
☐ 16. Andy levels checked (if available)?

FINAL CHECKS:
☐ 17. Checklist compliance rate calculated (all 16 above)?
☐ 18. Daily loss limit not exceeded?

GO SIGNAL: 17-18/18 = TRADE
CAUTION: 15-16/18 = SMALLER SIZE or PASS
NO-GO: <15/18 = DO NOT TRADE
```

---

## Signal Types Quick Reference

### VWAP Reversion (Best Setup Overall)
- **Timeframe:** 5-min or 15-min
- **Setup:** Price extends beyond VWAP, red/orange arrow
- **Entry:** At arrow trigger
- **Stop:** Extension high + 0.05%
- **Target:** VWAP centerline
- **Hold:** 1-3 bars
- **Win Rate:** 70%+
- **Best In:** Choppy markets (VIX 15-25)

### Opening Range Breakout (ORB)
- **Timeframe:** 5-min or 15-min (entry at 10:00 AM)
- **Setup:** First 30-min range, close + retest
- **Entry:** Retest of range break
- **Stop:** Opposite end of range
- **Target:** 2x range size
- **Hold:** 6-12 bars
- **Win Rate:** 60-65%
- **Best In:** Trending markets (VIX <20)

### Fibonacci Extension Fade
- **Timeframe:** 15-min or 1-hour
- **Setup:** Price extends to 127% or 168%
- **Entry:** At extension with divergence
- **Stop:** Extension high (tight!)
- **Target:** 50% pullback
- **Hold:** 12-20+ bars
- **Win Rate:** 65-70%
- **Best In:** All regimes

### C+R Confirmation
- **Timeframe:** 15-min or 1-hour
- **Setup:** Close below/above level, retest within 3-5 bars
- **Entry:** Retest entry
- **Stop:** Below/above retest level
- **Target:** Next structure
- **Hold:** 8-20+ bars
- **Win Rate:** 62%+
- **Best In:** Trending markets

---

## Session Times & Position Sizing

### 9:30-10:00 AM: OPENING RANGE
- **Volume:** Highest
- **Setup Quality:** High
- **Position Size:** 100% STANDARD
- **Best Setups:** ORB, opening retest
- **Note:** Let opening range fully form (9:45 minimum)

### 10:00 AM-11:30 AM: TREND DEVELOPMENT
- **Volume:** High
- **Setup Quality:** High
- **Position Size:** 100% STANDARD
- **Best Setups:** VWAP extensions, momentum follow
- **Note:** Strongest trending period

### 11:30 AM-2:00 PM: LUNCH CHOP
- **Volume:** Lowest
- **Setup Quality:** Poor
- **Position Size:** 50% REDUCED or SKIP
- **Best Setups:** AVOID (unless 6+ confluences)
- **Note:** Historically <50% win rate (skip if possible)

### 2:00-3:45 PM: POWER HOUR
- **Volume:** High
- **Setup Quality:** High
- **Position Size:** 100-125% (can increase)
- **Best Setups:** Pullbacks, structural bounces
- **Note:** Premium trading time (matched with morning)

### 3:45-4:00 PM: CLOSE
- **Volume:** Extreme
- **Setup Quality:** Poor
- **Position Size:** ZERO (exits only)
- **Best Setups:** None (Rule #5)
- **Note:** No new entries, manage existing positions only

---

## Learning Database Interpretation

### Weekly Analysis (Friday)
```
Last 5-10 trades this week:

VWAP Reversion:  2 wins / 1 loss = 67% ✓
ORB Breakout:    1 win / 2 loss = 33% ✗
C+R Confirmation: 3 wins / 1 loss = 75% ✓

ACTION: Focus on VWAP and C+R next week, reduce ORB
```

### Monthly Analysis (EOD last day of month)
```
Setup Type Performance (30 days):

VWAP Reversion:     14 wins / 6 loss = 70% ✓✓ (SCALE UP)
ORB Breakout:        8 wins / 7 loss = 53% ⚠ (REDUCE)
C+R Confirmation:   11 wins / 4 loss = 73% ✓✓ (SCALE UP)
Fibonacci Fade:      9 wins / 4 loss = 69% ✓✓ (STANDARD)

Confluence Effectiveness:
3 confluences:  12 wins / 8 loss = 60% (minimum threshold)
4 confluences:  18 wins / 7 loss = 72% (standard)
5+ confluences: 12 wins / 2 loss = 86% (premium) ✓✓✓

SESSION Performance:
Opening 9:30-10:00:  12 wins / 5 loss = 71% ✓
Trend 10:00-11:30:   18 wins / 7 loss = 72% ✓
Lunch 11:30-2:00:     3 wins / 6 loss = 33% ✗ AVOID
Power 2:00-3:45:     14 wins / 3 loss = 82% ✓✓ FOCUS
Close 3:45-4:00:      0 wins / 0 loss (exits only)

RECOMMENDATIONS:
1. Scale up VWAP + C+R (both 70%+)
2. Reduce ORB (below 60%)
3. Require 4+ confluences minimum (86% vs 60%)
4. AVOID lunch session (only 33% win rate)
5. FOCUS power hour (82% win rate)
```

---

## Rules for Using This System

### DO:
- ✅ Log EVERY signal (even losses)
- ✅ Follow pre-entry checklist 100% (no exceptions)
- ✅ Track confluences per trade
- ✅ Calculate win rate by setup type
- ✅ Adjust based on monthly performance data
- ✅ Avoid lunch chop (data shows <50% win rate)
- ✅ Scale up high-performing setups
- ✅ Update learning database daily

### DON'T:
- ❌ Backfill trades (only log live trades)
- ❌ Adjust stops once set (mechanical discipline)
- ❌ Trade without 3+ confluences (Rule #0)
- ❌ Skip the pre-entry checklist (non-negotiable)
- ❌ Trade in final 15 minutes (Rule #5)
- ❌ Exceed 1% risk per trade (Rule #23)
- ❌ Continue after daily loss limit (-$500, Rule #23)
- ❌ Ignore market regime changes

---

## Troubleshooting

### Problem: "No active signals showing"
**Solution:** Market may not have high-confluence setups. That's okay! Better to wait than trade bad setups.

### Problem: "Win rate below 50% on my best setup"
**Solution:** Either (1) setup needs more confluences, or (2) market regime changed. Review last 10 trades by regime.

### Problem: "I'm profitable but work is inconsistent"
**Solution:** Usually indicates mixed rule compliance. Check: Did you follow pre-entry checklist 100%? Did you avoid lunch chop?

### Problem: "Dashboard won't load signals"
**Solution:** (1) Check intraday_signals.json exists in this folder, (2) Restart browser, (3) Check browser console for errors

---

## Data Migration (End of Day)

**Automatic process:**
1. Any closed signals move from intraday_signals.json → intraday_learning_database.json
2. Learning database recalculates: win rate by setup, by confluence count, by session
3. Daily summary populated
4. New day: intraday_signals.json resets to empty (ready for new signals)

**Manual EOD Review:**
1. Export today's trades from learning_database.json
2. Calculate daily P/L, win rate, best setup
3. Journal: What worked? What failed? Why?
4. Plan tomorrow based on market regime

---

## Next Steps

1. **Today:** Start logging signals to intraday_signals.json
2. **This week:** Accumulate 5-10 trades with full data
3. **Next week:** First win rate calculations by setup type
4. **After 20 trades:** Statistical patterns emerge
5. **After 50 trades:** Confident edge identification
6. **After 100 trades:** System optimization, scaling decisions

---

## Questions & Support

**How do I start?**
→ Open intraday-command-center.html, wait for first setup, chat to Wingman to log signal

**How often should I check the dashboard?**
→ During market hours: Every 5-15 minutes (intraday timeframes are fast)
→ EOD: Review daily performance and update rules

**Can I do swing trades AND intraday?**
→ Yes! Keep them separate. Intraday capital ≠ swing capital. Your Trade #7 (swing) uses 29.7% account. Intraday uses 2-3% per trade.

**What if I have a bad day?**
→ Stop at -$500 daily loss limit (Rule #23). Closing program if necessary. Reset next day.

---

**System created:** 2025-10-29
**Status:** Ready for live trading
**Expected timeline:** 30 days to identify edge, 90 days to optimize
**Contact:** Chat to Wingman in the system for real-time updates
