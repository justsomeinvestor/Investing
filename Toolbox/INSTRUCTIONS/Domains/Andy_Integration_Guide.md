# Andy Integration Guide - Lead Trader Confluence System

## Table of Contents

1. [Overview](#overview)
2. [Philosophy](#philosophy)
3. [System Architecture](#system-architecture)
4. [Daily Workflow](#daily-workflow)
5. [Trade Integration](#trade-integration)
6. [Accuracy Tracking](#accuracy-tracking)
7. [Confluence Weighting](#confluence-weighting)
8. [Best Practices](#best-practices)

---

## Overview

### What This System Is

A **systematic, data-driven approach** to integrate lead trader Andy's market insights into Pilot's trading decisions through the confluence framework (Rule #0).

### Why This System Exists

- Andy is "more often right than wrong" (Pilot assessment)
- But blind following = Rule #17 violation (external validation without verification)
- Solution: Track Andy's calls, validate against outcomes, measure contribution to edge
- After 20+ sessions: Know exactly when Andy's input improves vs hurts trading

### What It's NOT

- NOT a system to blind follow Andy
- NOT a replacement for Pilot's independent analysis
- NOT optional (tracking is mandatory)
- NOT a prediction machine (probabilistic assessment only)

---

## Philosophy

### Core Principle

> Andy is one **confluence source among 7 possible sources**. We validate, measure, and weight based on evidence—not emotion or blind trust.

### Three Levels of Confidence

| Level | Criteria | Use | Example |
|-------|----------|-----|---------|
| **STRONG** | >60% accuracy + 10+ validations | Weight 2x in confluence | Andy's technical levels (60% accuracy) |
| **MEDIUM** | 50-60% accuracy + 5+ validations | Weight 1x in confluence | Andy's sector themes (building data) |
| **WEAK** | <50% accuracy or <5 validations | Weight 0.5x or deprecate | Andy's macro calls (insufficient data yet) |

### Data-Driven Decision Making

```
Session 1-5:   "Andy seems right a lot" (INSUFFICIENT DATA)
                ↓
Session 6-10:  "Andy is 55% accurate on levels, 70% on trades" (EMERGING PATTERN)
                ↓
Session 11-20: "Andy's technical levels = 65% accuracy = STRONG confluence" (CONFIDENCE)
                ↓
Session 21+:   Adjust weighting based on category-specific accuracy
```

---

## System Architecture

### File Structure

```
Journal/andy-intel/
├── README.md                      # System documentation
├── andy_intel_tracking.json       # Daily call tracking (v2.0)
├── andy_ticker_levels.json        # Quick reference (fast lookup)
├── andy_accuracy_history.json     # Long-term validation database
└── archive/                       # Historical data (>7 days old)
    └── YYYY-MM/
        └── andy_intel_YYYY-MM-DD.json
```

### File Purposes

#### 1. `andy_intel_tracking.json` (Daily Tracking)

**Updated:** Daily (~09:00 ET after Andy's morning calls)

**Contains:**
- Key levels (support/resistance) by ticker
- Trade ideas (entry/target/stop)
- Sector themes (bullish/bearish)
- Macro catalysts (FOMC, earnings, etc.)
- Earnings analysis
- Confluence alignment with Pilot
- Accuracy tracking (pending validations)

**Accessed:** At Wingman load (STEP 8.7)

**Example Entry:**
```json
"SPX": {
  "support": [6858],
  "resistance": [6885, 6922, 6937],
  "pattern": "At next resistance, narrow mega-cap leadership",
  "significance": "resistance",
  "catalyst": "FOMC 18:00 ET today"
}
```

---

#### 2. `andy_ticker_levels.json` (Quick Reference)

**Updated:** Daily (after andy_intel_tracking.json)

**Contains:**
- Most recent support/resistance per ticker
- Current bias (bullish/bearish/neutral)
- Key pattern
- Last update date (expires after 7 days)

**Accessed:** During trade analysis (intraday)

**Purpose:** Fast lookup. "What's Andy's take on SPX?" → Check this file.

**Example:**
```json
"SPX": {
  "support": [6858],
  "resistance": [6885, 6922, 6937],
  "current_bias": "at_resistance",
  "key_pattern": "Narrow leadership, breadth negative",
  "notes": "Fed day volatility. Caution on breadth failure."
}
```

---

#### 3. `andy_accuracy_history.json` (Long-term Database)

**Updated:** EOD after validating morning calls

**Contains:**
- Accuracy by category (levels/ideas/themes/macro/earnings)
- Hit rate calculations
- Session history
- Overall confidence level
- Recommendation for weighting

**Accessed:** After 20+ calls for statistical assessment

**Purpose:** Determine which Andy call types are reliable.

**Example:**
```json
"technical_levels": {
  "total_calls": 10,
  "hits": 6,
  "misses": 4,
  "hit_rate": 0.60,
  "confidence": "medium"
}
```

---

### Data Flow

```
Morning (09:00 ET)
├─ Andy's calls captured
├─ Wingman structures into andy_intel_tracking.json
├─ Wingman syncs to andy_ticker_levels.json
└─ Wingman loads at session start (STEP 8.7)

During Trading (09:30-16:00 ET)
├─ Pilot identifies potential trade
├─ Wingman checks andy_ticker_levels.json for Andy's levels
├─ If aligned: +1 confluence
└─ Pilot includes Andy in confluence scorecard

EOD (After Market Close)
├─ Wingman validates morning calls vs market outcomes
├─ Wingman updates accuracy_tracking in daily file
├─ Wingman updates andy_accuracy_history.json
└─ Session complete

Monthly (After 20+ Validations)
├─ Statistical assessment: Which categories are accurate?
├─ Confidence recalibration: Adjust weighting
└─ Update Rule #0 guidance: How to use Andy going forward
```

---

## Daily Workflow

### Morning Session (Before 10:00 AM ET)

#### Step 1: Capture Andy's Calls
```
Pilot action: Copy/paste Andy's morning chat commentary
              or summarize key calls

Example:
"SPX resistance 6885, 6937 next. QQQ hitting 637.75 resistance.
AAPL double top at 269.87 (distribution signal). NVDA rejected
212.19. Mining sector bullish (CCJ, UEC). FOMC at 18:00 ET today."
```

#### Step 2: Wingman Structures Data
```
Wingman action: Parse and input into andy_intel_tracking.json

SPX section:
  - support: [6858]
  - resistance: [6885, 6922, 6937]
  - pattern: "At next resistance"
  - catalyst: "FOMC 18:00 ET"

QQQ section:
  - support: [633.65]
  - resistance: [637.75]
  - pattern: "Hitting resistance"

... (continue for all tickers)
```

#### Step 3: Create Quick Reference
```
Wingman action: Sync to andy_ticker_levels.json

SPX → Quick lookup entry updated
QQQ → Quick lookup entry updated
AAPL → Quick lookup entry updated
NVDA → Quick lookup entry updated
CCJ → Quick lookup entry updated

Confirmation: "✅ Andy intel captured. 25 levels logged for 15 tickers."
```

#### Step 4: Load at Session Start
```
Wingman (STEP 8.7): Read both files, hold in memory

Ready for: "When Pilot analyzes SPX short, check andy_ticker_levels
for SPX bias. If aligned with Pilot's thesis: +1 confluence."
```

---

### During Trading (9:30 AM - 4:00 PM ET)

#### Scenario: Pilot Identifies Potential Trade

**Pilot:** "Looking at SPY short at 688. Overbought RSI, failed opening, retest zone."

**Wingman Process:**
1. Check andy_ticker_levels.json for SPX/SPY entries
2. Find: Andy SPX resistance 6885, 6937. Current bias: "at_resistance"
3. Assess alignment: Pilot's breakdown = Andy's resistance zone
4. Update live_trade_tracker.json confluence scorecard
5. Provide context: "Andy's recent SPX resistance at 6885, 6937. Your thesis aligns with key zone. +1 confluence."

**Pilot Decision:** Includes Andy's levels in pre-entry checklist

**Record:** In trades_ledger.json, document Andy confluence contribution

---

### End of Day (After 4:00 PM ET)

#### Step 1: Validate Morning Calls
```
Wingman process:

Andy called: "SPX resistance 6885, 6937"
Market result: SPX hit 6889 on Oct 30 (HIT) + pulled back (resistance confirmed)
Record: "call": "SPX resistance 6885", "outcome": "hit", "validation_date": "2025-10-30"

Andy called: "NVDA rejected 212.19"
Market result: NVDA traded 211.85-213.10, pullback happened (HIT)
Record: Call validated

Andy called: "TLT target 93.30"
Market result: TLT closed 92.40 (MISS - didn't reach target)
Record: "call": "TLT 93.30", "outcome": "miss", "validation_date": "2025-10-30"

... (validate all calls)
```

#### Step 2: Update Accuracy Database
```
Wingman updates andy_accuracy_history.json:

technical_levels:
  - total_calls: 15
  - hits: 9 (hit %)
  - misses: 6 (miss %)
  - hit_rate: 60% = MEDIUM confidence

trade_ideas:
  - total_calls: 8
  - hits: 6
  - misses: 2
  - hit_rate: 75% = HIGH confidence

... (all categories)
```

#### Step 3: Summary & Prep
```
Wingman output: "Andy EOD Summary:
- Technical levels: 9/15 hit (60%)
- Trade ideas: 6/8 hit (75%)
- Sector themes: 3/5 validated
- Overall: 18/28 calls hit (64% accuracy)
- Status: Building database. 12 more calls to 20-call confidence threshold."
```

---

## Trade Integration

### Pre-Entry Checklist (Rule #0 Integration)

**When Pilot identifies trade:**

#### Confluence Scorecard Example

```
TRADE: SPY short @ 688

Confluences:
1. ✅ Overbought RSI (Technical - Pilot's analysis)
2. ✅ Failed opening price (Structure - Pilot's analysis)
3. ✅ Retest zone (Technical - Pilot's analysis)
4. ✅ Breadth divergence (Market data - Pilot's data)
5. ✅ Andy SPX 6885 resistance (Lead trader - Andy's call)
6. ✅ FOMC catalyst (Macro - Andy's context)

Total: 6 confluences = HIGH CONVICTION ENTRY

Andy's contribution: +1 confluence (technical levels align with thesis)
Andy confidence: 60% (from accuracy history) = MEDIUM weighting
```

---

### How Andy Becomes Confluence

#### Condition 1: Technical Alignment
```
Pilot's analysis: SPY breaking below 687.23 (opening price)
Andy's levels: SPX resistance 6885, 6937 (equivalent to SPY 688+)

Result: Pilot's short entry @ 688 = respecting Andy's resistance zone
Confluence: +1 (aligned)
```

#### Condition 2: Specificity
```
Andy says: "SPX bullish" ❌ VAGUE (no confluence value)
Andy says: "SPX resistance 6885" ✅ SPECIFIC (can validate, has confluence value)

Rule: Only count Andy calls that are SPECIFIC price levels or trade ideas.
```

#### Condition 3: Recency
```
Andy called SPX 6885 resistance on Oct 29
Pilot analyzing on Oct 29 same day: ✅ FRESH (counts)
Pilot analyzing on Oct 31 (2 days later): ⚠️ STALE (reconfirm or discount)
Pilot analyzing on Nov 5 (1 week later): ❌ EXPIRED (don't count)
```

#### Condition 4: Andy's Category Accuracy
```
From andy_accuracy_history.json:

technical_levels: 60% accuracy → MEDIUM weighting
If SPX 6885 resistance = technical level call:
  Confluence count: +1 × 0.6 (weighted) = +0.6 confluence

trade_ideas: 75% accuracy → HIGH weighting
If Andy's RUN 19.70 → 23.25 = trade idea:
  Confluence count: +1 × 0.75 (weighted) = +0.75 confluence
```

#### Condition 5: Pilot's Independent Thesis (MANDATORY)
```
❌ WRONG: "I'm shorting SPY because Andy said so"
          (No independent thesis - violates Rule #17)

✅ RIGHT: "I'm shorting SPY because: (1) Overbought RSI,
          (2) Failed opening, (3) Retest zone.
          Andy's SPX resistance aligns with this thesis,
          so +1 confluence."
          (Independent thesis + Andy alignment)
```

---

## Accuracy Tracking

### Validation Criteria by Category

#### Technical Levels

**Definition:** Support/resistance calls. e.g., "SPX resistance 6885"

**Validation Criteria:**
- ✅ **HIT** = Level reached ±1% within 2 trading sessions
- ❌ **MISS** = Never reached within 2 sessions
- ⚠️ **PARTIAL** = Reached but no reaction (level existed, not true resistance)

**Example:**
```
Andy: "SPX resistance 6885"
Oct 30 Result: SPX hit 6889, pulled back = HIT (within 1%, confirmed resistance)
Record: {"call": "SPX resistance 6885", "outcome": "hit", "date": "2025-10-30"}
```

---

#### Trade Ideas

**Definition:** Entry/exit calls with targets. e.g., "RUN 19.70 target 23.25"

**Validation Criteria:**
- ✅ **HIT** = Target reached within stated timeframe
- ❌ **MISS** = Stop hit first, or target not reached in timeframe
- ⚠️ **PARTIAL** = Reached 50%+ of target (partial credit)

**Example:**
```
Andy: "RUN fill 19.70, target 23.25"
Nov 3 Result: RUN reached 21.90 (not full target) = PARTIAL HIT (81% of target)
Record: {"call": "RUN target 23.25", "outcome": "partial_hit", "percent": 0.81, "date": "2025-11-03"}
```

---

#### Sector Themes

**Definition:** Directional sector calls. e.g., "Mining is new growth sector"

**Validation Criteria:**
- ✅ **HIT** = Sector ETF moves predicted direction >1% within 2 sessions
- ❌ **MISS** = Opposite direction >1%
- ⚠️ **NEUTRAL** = Flat or mixed (no credit)

**Example:**
```
Andy: "Mining sector bullish" (Sector theme)
Oct 31 - Nov 1 Result: GDXJ +2.3% = HIT (bullish direction confirmed)
Record: {"call": "Mining bullish", "outcome": "hit", "metric": "GDXJ +2.3%", "date": "2025-11-01"}
```

---

#### Macro Catalysts

**Definition:** Event impact calls. e.g., "FOMC dovish = relief rally"

**Validation Criteria:**
- ✅ **HIT** = Market moves in predicted direction/magnitude
- ❌ **MISS** = Opposite direction or no move
- ⚠️ **PARTIAL** = Correct direction but smaller magnitude

**Example:**
```
Andy: "FOMC dovish cut expected, will trigger relief rally"
Oct 29 18:00 ET Result: Fed cut rates (dovish) + SPX +1.8% (relief rally) = HIT
Record: {"call": "FOMC dovish relief rally", "outcome": "hit", "result": "SPX +1.8%", "date": "2025-10-29"}
```

---

#### Earnings Analysis

**Definition:** Post-earnings setup calls. e.g., "CLS bullish on Oct 31 earnings"

**Validation Criteria:**
- ✅ **HIT** = Stock moves in predicted direction post-earnings by expected magnitude
- ❌ **MISS** = Opposite direction or unexpected magnitude
- ⚠️ **PARTIAL** = Correct direction, smaller move than expected

**Example:**
```
Andy: "CLS bullish on Oct 31 earnings. Target 341-344."
Nov 1 Result (post-earnings): CLS +2.5% to 343 range = HIT (target reached, bullish validated)
Record: {"call": "CLS bullish earnings", "outcome": "hit", "target": "341-344", "result": 343, "date": "2025-11-01"}
```

---

### Accuracy Calculation

#### Per-Category Accuracy

```
Formula: Hit Rate = Hits / (Hits + Misses)

Example - Technical Levels:
- Total calls: 15
- Hits: 9
- Misses: 6
- Hit Rate: 9 / 15 = 60%

Interpretation:
- 60% = MEDIUM confidence
- Can use as +1 confluence, but with reduced weight
```

#### Overall Accuracy

```
Formula: Overall Hit Rate = Total Hits / (Total Hits + Misses)

Example - All Categories Combined:
- Total calls: 40
- Total hits: 24
- Total misses: 16
- Overall Hit Rate: 24 / 40 = 60%

Interpretation:
- 60% = Slightly above random
- Andy is better than coin flip
- Specific categories may vary (some 70%, some 50%)
```

#### Confidence Thresholds

| Accuracy | Sample Size | Confidence | Recommendation |
|----------|-------------|-----------|-----------------|
| >60% | 10+ | HIGH | Weight 2x in confluence |
| 50-60% | 5+ | MEDIUM | Weight 1x in confluence |
| <50% | 5+ | LOW | Weight 0.5x or deprecate |
| <5 calls | Any | INSUFFICIENT | Track, don't use yet |

---

## Confluence Weighting

### Static Weighting (Pre-data)

Before accuracy data, weight all Andy calls at 1x (equal to other sources):

```
CONFLUENCE SCORECARD (Before 20 validations):

1. Overbought RSI (Technical - Pilot)         × 1.0 = 1.0
2. Failed opening (Structure - Pilot)         × 1.0 = 1.0
3. Retest zone (Technical - Pilot)            × 1.0 = 1.0
4. Andy SPX resistance (Lead trader - Andy)   × 1.0 = 1.0
5. FOMC catalyst (Macro - Andy)               × 1.0 = 1.0

Total Confluence Score: 5.0
```

---

### Dynamic Weighting (Post-data, After 20 Validations)

After 20+ calls validated, weight based on accuracy:

```
CONFLUENCE SCORECARD (After accuracy profile built):

1. Overbought RSI (Technical - Pilot)              × 1.0 = 1.0
2. Failed opening (Structure - Pilot)              × 1.0 = 1.0
3. Retest zone (Technical - Pilot)                 × 1.0 = 1.0
4. Andy SPX resistance (Technical level - Andy)    × 0.6 = 0.6
   (Andy technical levels = 60% accuracy)
5. FOMC catalyst (Macro - Combo)                   × 1.0 = 1.0

Total Confluence Score: 4.6 confluences
(Equivalent to 4.6/5 or 92% of full confluence)
```

---

### When to Adjust Weighting

#### Increase Weighting (>60% Accuracy)
```
Scenario: Andy's technical levels = 70% accurate over 10+ calls

Action:
  - Increase weighting to 1.5x
  - Example: Andy confluence = 1.5 points (vs 1.0 for other sources)
  - Use in confluence scorecard: 1.0 × 1.5 = 1.5 points

Rationale: Andy is better than random, has demonstrated edge in this category
```

#### Maintain Weighting (50-60% Accuracy)
```
Scenario: Andy's sector themes = 55% accurate

Action:
  - Keep weighting at 1.0x
  - Example: Andy confluence = 1.0 point (equal to other sources)
  - Use in confluence scorecard: 1.0 × 1.0 = 1.0 point

Rationale: Andy at coin-flip level. Useful as confirmation, not as lead signal
```

#### Decrease Weighting (<50% Accuracy)
```
Scenario: Andy's macro calls = 40% accurate over 10+ calls

Action:
  - Decrease weighting to 0.5x or 0.0x (deprecate)
  - Example: Andy confluence = 0.5 points (quarter-weight)
  - Or: Don't count Andy macro calls at all

Rationale: Andy below random in this category. Better to ignore than be misled
```

---

## Best Practices

### DO ✅

1. **DO: Require Independent Thesis First**
   ```
   Pilot: "I see overbought RSI, failed opening retest, breadth divergence.
           Andy's SPX resistance aligns with this setup."
   Result: Andy confluence counts.
   ```

2. **DO: Validate Every Call**
   ```
   Morning: Andy calls SPX 6885 resistance
   EOD: Check if SPX tested 6885. If yes = HIT. If no = MISS.
   Record: Both outcomes (don't cherry-pick wins).
   ```

3. **DO: Track Systematically**
   ```
   Update accuracy_history.json after EVERY session.
   Don't wait for "perfect" sample—start small, add over time.
   ```

4. **DO: Adjust Based on Data**
   ```
   After 20 calls: "Andy is 65% accurate on levels, 50% on themes.
   Weight levels heavily, themes lightly."
   ```

5. **DO: Communicate Openly**
   ```
   "This trade: 6 confluences total. Andy provides 1 (weighted 0.6
   based on 60% accuracy history). So really 5.6 effective confluences."
   ```

---

### DON'T ❌

1. **DON'T: Blind Follow Andy**
   ```
   Wrong: "Andy says SPX 6885 resistance, so I'm shorting SPY"
   Right: "Andy's SPX 6885 aligns with my technical setup, so +1 confluence"
   ```

2. **DON'T: Cherry-Pick Wins**
   ```
   Wrong: Record Andy's hits, ignore misses
   Right: Record BOTH hits and misses objectively
   ```

3. **DON'T: Use Stale Data**
   ```
   Wrong: "Andy called SPX 6885 last week, still using it today"
   Right: "Andy's call is 7 days old. Need reconfirmation or discard"
   ```

4. **DON'T: Count Vague Calls**
   ```
   Wrong: Andy says "market looks bullish" → +1 confluence
   Right: Andy says "SPX resistance 6885" → +1 confluence (if specific)
   ```

5. **DON'T: Ignore Low Accuracy**
   ```
   Wrong: Keep weighting Andy equally despite 30% accuracy
   Right: "Andy is 30% accurate on earnings. Stop counting these calls."
   ```

---

### Common Pitfalls

#### Pitfall 1: "Andy is right a lot, so always follow him"
```
Problem: Confirmation bias. Remembering hits, forgetting misses.
Solution: Systematic tracking. Numbers don't lie.
```

#### Pitfall 2: "This time is different, Andy's really right"
```
Problem: Emotional weighting. One good call ≠ pattern.
Solution: Need 20+ calls minimum before confidence assessment.
```

#### Pitfall 3: "Andy said so, but I'll trade opposite"
```
Problem: Contrarianitis. Assuming Andy is always wrong to be contrarian.
Solution: Use data. If Andy is 60% accurate, trade with him 60% of time.
```

#### Pitfall 4: "Let me adjust accuracy calculation to make Andy look better"
```
Problem: Cherry-picking. Changing validation rules mid-stream.
Solution: Define rules FIRST, then apply consistently to all calls.
```

#### Pitfall 5: "I don't have time to validate every call"
```
Problem: Lazy tracking. Defeats purpose of system.
Solution: EOD validation = 10-15 min effort. Non-negotiable.
```

---

## Quick Reference

### File Access Points

| Need | File | Action |
|------|------|--------|
| **Today's levels** | andy_ticker_levels.json | Quick lookup during trade |
| **Complete daily record** | andy_intel_tracking.json | Reference during session |
| **Historical accuracy** | andy_accuracy_history.json | Monthly assessment |
| **System documentation** | README.md (in andy-intel/) | Understand system |

---

### Decision Trees

#### "Should I count this as Andy confluence?"

```
Does Pilot have independent thesis?
├─ YES → Is Andy's call specific (not vague)?
│   ├─ YES → Is call recent (within 1-2 days)?
│   │   ├─ YES → Does Andy have accuracy data in this category?
│   │   │   ├─ YES → Use accuracy % as weight
│   │   │   └─ NO → Use 1.0x weight (default)
│   │   └─ NO → Discard (stale)
│   └─ NO → Discard (too vague)
└─ NO → Discard (violates Rule #17)
```

---

#### "Is this Andy call validated?"

```
Andy's call: [SPECIFIC LEVEL/IDEA]
Check market outcome: Did predicted event occur?
├─ YES, at expected magnitude → HIT (update accuracy up)
├─ YES, at 50%+ magnitude → PARTIAL HIT (partial credit)
├─ NO, opposite direction → MISS (update accuracy down)
├─ NO, no move → MISS (update accuracy down)
└─ PENDING (>2 days, still waiting) → PENDING (don't count yet)

Record result in andy_accuracy_history.json
```

---

### Monthly Review Checklist

- [ ] Review andy_accuracy_history.json accuracy by category
- [ ] Calculate overall hit rate: Hits / (Hits + Misses)
- [ ] Identify strongest category (highest accuracy)
- [ ] Identify weakest category (lowest accuracy)
- [ ] Update confluence weighting recommendations
- [ ] Communicate to Pilot: "Andy is X% accurate, weighting Y"
- [ ] Plan for next 20 calls: Track specific categories

---

## FAQ

**Q: What if Andy is 50% accurate?**
A: That's coin-flip level. You can use his calls, but don't over-weight them. Use 1.0x or 0.5x weighting. Equal contributor, not stronger.

**Q: Should I trade opposite Andy if he's wrong 50% of the time?**
A: No. That's overthinking. Just use him as one confluence source. If he's 50%, he's neutral, not inverse.

**Q: Can I use old Andy levels (>7 days)?**
A: Technically yes, but reconfirm first. Markets change. "Support 6858 from 5 days ago" might not be support today.

**Q: What if Andy is 80% accurate?**
A: Excellent. Use 1.5x or 2x weighting. But still require Pilot's independent thesis first. Never blind follow.

**Q: When do I start using Andy for confluence?**
A: Immediately. Start tracking now. Weighting can be adjusted after data builds (20+ calls). But tracking from day 1.

**Q: Can I skip tracking if I "feel" Andy is right?**
A: No. Feelings are unreliable. Systematic tracking is mandatory, not optional.

**Q: Should I tell Pilot about accuracy changes?**
A: Yes. "Andy's technical levels are now 65% accurate. Weighting increased to 1.5x in confluence framework."

---

## Updates & Revisions

| Date | Version | Change |
|------|---------|--------|
| 2025-10-29 | v1.0 | Initial system creation. 25 calls captured. Tracking begins. |
| TBD | v1.1 | After 20 calls: Statistical assessment, weighting recommendations |
| TBD | v2.0 | After 100+ calls: Category-specific deep analysis |

---

## Final Note

This system works best when:
1. **Tracked rigorously** (every call validated EOD)
2. **Applied objectively** (weighting based on data, not gut)
3. **Updated regularly** (accuracy recalculated monthly)
4. **Communicated clearly** (Pilot knows why Andy is weighted X)

Andy is your trading partner's voice in the system. Respect that by treating his contributions with the same rigor you use for your own analysis.

---

**Location:** `Toolbox/INSTRUCTIONS/Domains/Andy_Integration_Guide.md`
**Maintained by:** Wingman (AI Trading Partner)
**Status:** ACTIVE (October 29, 2025 forward)
