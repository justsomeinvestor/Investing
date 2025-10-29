# Andy Intel Tracking System

## Overview

This folder contains systematic tracking of Andy's (lead trader) market insights, technical levels, trade ideas, and macro calls.

**Purpose:** Build an evidence-based profile of Andy's effectiveness as a confluence source for trading decisions (Rule #0 - Confluence Framework).

**Philosophy:** Andy is "more often right than wrong" (Pilot assessment). But we don't blind follow. We track, validate, and measure to determine exactly when Andy's input improves our edge vs when it's noise.

---

## Files in This Folder

### 1. `andy_intel_tracking.json` (Daily Tracking)

**What:** Complete daily record of Andy's calls from morning session.

**Contains:**
- Key levels (support/resistance) by ticker
- Trade ideas with entry/target/stop
- Sector themes (bullish/bearish bias)
- Macro catalysts and timing
- Earnings analysis
- Key insights
- Confluence alignment with Pilot's analysis
- Accuracy tracking (validations array)

**Updated:** Daily (usually around 09:00 ET after Andy's morning calls)

**Access:** Wingman reads this at session start (STEP 7.5 in loading sequence)

**Example Entry:**
```json
"SPX": {
  "support": [6858],
  "resistance": [6885, 6922, 6937],
  "pattern": "At next resistance, narrow mega-cap leadership",
  "context": "SPX at key resistance zone. Fed decision today = volatility driver.",
  "significance": "resistance",
  "catalyst": "FOMC decision 18:00 ET"
}
```

---

### 2. `andy_ticker_levels.json` (Quick Reference)

**What:** Condensed, searchable reference for Andy's most recent levels on each ticker.

**Why:** Fast lookup during trade analysis. "What's Andy's take on SPY?" → Check this file.

**Contains:**
- Most recent support/resistance per ticker
- Current bias (bullish/bearish/neutral)
- Key pattern
- Quick notes
- Last update date

**Auto-expires:** After 7 days without update (flagged for refresh)

**Access:** Wingman checks this when analyzing potential trades. Format: "Andy's recent levels on [TICKER]: Support [X], Resistance [Y]. Bias: [Z]."

**Example Ticker Entry:**
```json
"SPX": {
  "last_updated": "2025-10-29",
  "support": [6858],
  "resistance": [6885, 6922, 6937],
  "current_bias": "at_resistance",
  "key_pattern": "Narrow mega-cap leadership, breadth negative",
  "notes": "At next resistance 6937. Fed day volatility. Caution on breadth failure."
}
```

---

### 3. `andy_accuracy_history.json` (Long-term Validation)

**What:** Statistical database of Andy's accuracy over 20+ sessions/calls.

**Why:** Quantify whether Andy improves edge or adds noise. Data-driven confidence assessment.

**Contains:**
- Accuracy by category (technical levels, trade ideas, sector themes, macro, earnings)
- Hit rate calculations
- Session history log
- Overall confidence level
- Recommendation for weighting Andy in confluence framework

**Updated:** After each session EOD - validate morning calls against market outcomes

**Access:** Wingman reviews after 20+ calls for statistical assessment. "Is Andy >50% accurate? Which categories are reliable?"

**Example Category:**
```json
"technical_levels": {
  "total_calls": 0,
  "hits": 0,
  "misses": 0,
  "pending": 15,
  "hit_rate": null
}
```

---

## Daily Workflow

### Morning (Before Market Open)

1. **Capture Andy's Calls**
   - Pilot: Copy/paste Andy's morning commentary from chat
   - Wingman: Parses and structures into `andy_intel_tracking.json`
   - Time: ~09:00 ET (before open)

2. **Populate Quick Reference**
   - Wingman: Updates `andy_ticker_levels.json` with fresh levels
   - Wingman confirms: "Andy intel captured. [X] levels logged for [tickers]."

3. **Wingman Loading**
   - At session start, Wingman reads both files
   - Holds key levels in working memory for trade analysis

### During Trading Session

1. **Trade Analysis Integration**
   - Pilot identifies potential trade
   - Wingman checks `andy_ticker_levels.json`
   - Example: "Looking at SPY short at 688"
     - Wingman: "Andy's recent SPX levels: Resistance 6885, 6937. You're at key zone. +1 confluence alignment."
   - Pilot: Uses Andy's levels as one confluence factor (Rule #0)

2. **Pre-Entry Checklist**
   - Item 3 (Confluence): Include Andy's relevant call
   - Document in trade record

### End of Day

1. **Validate Morning Calls**
   - Check: Did SPX hit 6937 resistance? Did TLT reach 93.30? Did FOMC move markets as expected?
   - Wingman: Updates `accuracy_tracking.validations[]` in daily file

2. **Update Accuracy History**
   - Wingman calculates: Call hit, miss, or pending
   - Updates `andy_accuracy_history.json` category counts

3. **Prepare for Next Session**
   - Note: Which validations still pending (may extend 1-2 days)
   - Flag: Any surprising misses for investigation

### Monthly (After 20+ Sessions)

1. **Statistical Assessment**
   - Calculate overall hit rate by category
   - Determine confidence level
   - Update recommendation for Rule #0 weighting

2. **Adjust Confluence Weighting**
   - If Andy >60% accurate in category → STRONG confluence
   - If Andy 50-60% → MEDIUM confluence
   - If Andy <50% → WEAK confluence or deprecate

---

## How Andy Intel Integrates with Rule #0 (Confluence Framework)

### Rule #0 Overview
Never enter on single reason. Require MINIMUM 3+ independent confluences before any entry.

### Andy as Confluence Source

**When Andy Counts as +1 Confluence:**
1. Andy's call aligns with Pilot's independent analysis
2. Andy provides specific level (not vague "bullish")
3. Call is recent (within 1 trading session)
4. Call is in Andy's strength category (per accuracy history)
5. Pilot has independent thesis (never blind follow)

**When Andy Does NOT Count:**
- Pilot has no thesis of own (violates Rule #17 - external validation)
- Andy's call is general/vague ("market looks good")
- Call is stale (>2 days without reconfirmation)
- Call is in Andy's weak accuracy category
- Accuracy history shows <50% hit rate in that category

### Example Integration

**Scenario:** Pilot considering SPY short at 688

**Confluence Scorecard:**
1. ✅ Overbought RSI (Pilot's technical)
2. ✅ Failed opening price (Pilot's structure)
3. ✅ Retest zone (Pilot's technical)
4. ✅ Breadth divergence (Pilot's data)
5. ✅ Andy's SPX resistance at 6885 (Andy's technical) ← Andy confluence
6. ✅ FOMC catalyst (Macro)

**Result:** 6 confluences = HIGH CONVICTION ENTRY
- Andy contributes 1 confluence (if accuracy profile supports it)
- If Andy's technical levels historically accurate → weight heavily
- If Andy's accuracy unknown yet → count as medium confluence

---

## Tracking & Validation Examples

### Technical Level Validation

**Andy's Call:** "SPX resistance 6885"

**Validation Criteria:**
- Level reached within 1% (6877-6893) within 2 trading sessions = HIT
- Never reached = MISS
- Reached but no reaction = PARTIAL (level existed, not resistance)

**EOD Update:**
```json
{
  "call": "SPX resistance 6885",
  "outcome": "hit",
  "validation_date": "2025-10-30",
  "details": "SPX hit 6889 on Oct 30, pulled back from resistance zone"
}
```

---

### Trade Idea Validation

**Andy's Call:** "RUN fill 19.70, target 23.25"

**Validation Criteria:**
- Target hit 23.25 within 5 trading sessions = HIT
- Stop hit at 18.00 first = MISS
- Reaches 50%+ of target (21.88) = PARTIAL HIT

**EOD Update:**
```json
{
  "call": "RUN 19.70 → 23.25",
  "outcome": "partial_hit",
  "validation_date": "2025-11-03",
  "details": "RUN reached 21.90 on Nov 3, not full target. Positive execution."
}
```

---

### Sector Theme Validation

**Andy's Call:** "Mining is new growth sector - bullish"

**Validation Criteria:**
- Mining sector ETF (e.g., GDXJ) +1%+ within 2 sessions = HIT
- GDXJ -1%+ = MISS
- Flat/mixed = NEUTRAL (no credit)

**EOD Update:**
```json
{
  "call": "Mining sector bullish",
  "outcome": "hit",
  "validation_date": "2025-11-02",
  "details": "GDXJ +2.3% on Nov 1-2, validating sector strength"
}
```

---

## Statistical Targets

### Sample Size Minimums
- **Technical Levels:** 10+ validations before confidence assessment
- **Trade Ideas:** 8+ validations before confidence assessment
- **Sector Themes:** 5+ validations before confidence assessment
- **Overall:** 20+ validations before final accuracy recommendation

### Confidence Thresholds
- **High Confidence:** >60% hit rate across category + 10+ validations
- **Medium Confidence:** 50-60% hit rate + 5+ validations
- **Low Confidence:** <50% hit rate or <5 validations
- **Insufficient Data:** <3 validations in category

---

## Integration with Wingman Loading Sequence

### STEP 7.5E: Load Andy Intel Files
```
1. Read: Journal/andy-intel/andy_intel_tracking.json (today's calls)
2. Extract: key_levels, trade_ideas, sector_themes, macro_catalysts
3. Hold in memory: Andy's bias, key levels for major tickers
4. Note: accuracy tracking status
```

### STEP 7.5F: Load Andy Ticker Quick Reference
```
1. Read: Journal/andy-intel/andy_ticker_levels.json
2. Extract: Most recent levels per ticker, current bias, expiration status
3. Flag: Any tickers needing refresh (>7 days stale)
4. Use: For intraday confluence checks
```

### Display in Instrument Check
```
📡 LEAD TRADER INTEL (Andy)
├─ Last Update: [DATE TIME]
├─ Tracked Tickers: [COUNT]
├─ Accuracy Rate: [HIT_RATE]% ([CALLS] validated)
├─ Today's Key Levels:
│  ├─ SPX: R [6885, 6937], S [6858]
│  ├─ QQQ: R [637.75], S [633.65]
│  └─ AAPL: Distribution signal at [269.87]
└─ Integration: ✓ READY (confluence source)
```

---

## Best Practices

### 1. Never Blind Follow Andy
- Andy is a confluence SOURCE, not a decision
- Pilot must have independent thesis
- Use Andy to VALIDATE, not to initiate

### 2. Track Rigorously
- Update accuracy history EOD
- Don't skip validations (all calls must be tracked)
- Document "WHY" calls hit/missed (not just outcome)

### 3. Adjust Dynamically
- After 5+ validations per category: Adjust confidence level
- After 20+ total validations: Reassess Andy's contribution to edge
- If accuracy drops: Reduce weighting or deprecate

### 4. Use Data, Not Gut Feel
- "I think Andy is right" ≠ evidence
- "Andy has 65% accuracy in technical levels" = evidence
- Base confluence weighting on historical data

### 5. Communicate Clearly
- When using Andy in trade record: "Andy confluence: SPX 6885 resistance aligns with our technical setup"
- When validating: "Andy's 6885 resistance call HIT 10/30. Still tracking."
- When assessing: "Andy's technical levels currently 70% accurate (7/10 hits). STRONG confluence weighting justified."

---

## File Maintenance

### Daily
- Update `andy_intel_tracking.json` with morning calls
- Update `andy_ticker_levels.json` with fresh levels
- Validate yesterday's calls (update accuracy)

### Weekly (Friday EOD)
- Archive tickers >7 days old (move to historical)
- Update `andy_accuracy_history.json` session summary
- Flag any accuracy anomalies for investigation

### Monthly
- Statistical reassessment: Overall hit rate by category
- Confidence level recalibration
- Update Rule #0 weighting recommendation

---

## Questions to Ask

**When Loading for Session:**
- What are Andy's key levels for the markets I'm watching?
- Is Andy bullish or bearish on tickers I'm analyzing?
- Are there sector themes I should be aware of?

**During Trade Analysis:**
- Does Andy have levels on this ticker?
- Does Andy's bias align with or contradict my thesis?
- If aligned: +1 confluence. If contradictory: investigate why.

**End of Day:**
- Did Andy's calls validate?
- Which categories are winning? Which losing?
- Should I adjust my weighting of Andy's input?

**Monthly Assessment:**
- Is Andy >50% accurate overall?
- Which categories (levels/ideas/themes/macro/earnings) are his strengths?
- Should we increase/decrease reliance on Andy as confluence source?

---

## Contact & Updates

**Maintained by:** Wingman (AI Trading Partner)
**Created:** 2025-10-29
**Last Updated:** 2025-10-29
**Status:** ACTIVE (Daily tracking begins Oct 29)

---

## Navigation

- **Quick Reference:** Open `andy_ticker_levels.json` for pre-trade level checks
- **Daily Tracking:** Open `andy_intel_tracking.json` for complete daily record
- **Accuracy Stats:** Open `andy_accuracy_history.json` for long-term validation data
- **Wingman Loading:** See STEP 7.5 in `Toolbox/INSTRUCTIONS/Domains/How_to_Load_Wingman.txt`
- **Integration Guide:** See `Toolbox/INSTRUCTIONS/Domains/Andy_Integration_Guide.md`
