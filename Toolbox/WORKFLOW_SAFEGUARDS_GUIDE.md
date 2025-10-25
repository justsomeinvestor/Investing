# Workflow Safeguards Guide - 5 Critical Fixes

**Updated**: October 19, 2025
**Status**: Implemented in How_to_use_Research.txt
**Purpose**: Prevent workflow blocking failures discovered in 2025-10-19 session

---

## Overview

Research workflow discovered 5 critical gaps that could block future executions. This guide documents fixes and verification procedures.

---

## FIX #1: STEP 1 VERIFICATION CHECKPOINT

### **Problem**
No verification step after Step 1 to confirm required summaries exist before proceeding to Step 2. When providers missing (RSS, YouTube), workflow assumed all data present → cascading failures.

### **Solution**
Add explicit verification checkpoint after Step 1.5 (X Bookmarks completion).

### **Implementation**

**Location**: After Step 1.5, before Step 2

**Process**:
```
1. Use Glob pattern to check for REQUIRED summaries:

   a. Technical Summaries (REQUIRED - 4 files):
      Pattern: Research/Technicals/TradingView*/YYYY-MM-DD*Summary.md
      Files needed:
      - TradingView SPX Summary
      - TradingView BTC Summary
      - TradingView QQQ Summary
      - TradingView SOL Summary

   b. X Sentiments (REQUIRED - 2 files):
      Pattern: Research/X/YYYY-MM-DD_X_*.md
      Files needed:
      - X Crypto Summary
      - X Macro Summary

   c. Optional Providers (CAN SKIP):
      - RSS provider summaries (any pattern)
      - YouTube channel summaries (any pattern)
      - X Bookmarks summary (can be empty)

2. Decision Logic:
   - If ALL required present → proceed to Step 2
   - If ANY required missing → STOP and create them before Step 2
   - If optional missing → NOTE IT but PROCEED to Step 2

3. Document Results:
   - Record which optional providers missing
   - Note in final completion report
```

### **Verification Command**
```bash
# Check for 4 required technical summaries
find Research/Technicals -name "*YYYY-MM-DD*Summary.md" | wc -l
# Result: Should show 4 or more (4 required + optional)

# Check for 2 required X summaries
find Research/X -maxdepth 1 -name "*YYYY-MM-DD_X_*.md" | wc -l
# Result: Should show 2
```

### **What Happens If Missing**
- **If Technical summaries missing**: Step 4 (signals) will fail or give bad data → REQUIRED
- **If X summaries missing**: X sentiment analysis impossible → REQUIRED
- **If RSS/YouTube missing**: Technical + X overviews still possible → OPTIONAL
- **If Bookmarks empty**: Normal (no new bookmarks) → OPTIONAL

---

## FIX #2: TRADINGVIEW SUMMARY FORMAT REQUIREMENTS

### **Problem**
TradingView summaries had data but SummaryParser couldn't extract it. Parser looks for specific format patterns (e.g., "Price: 6747.50") but summaries had different formatting. Result: parser returned NONE → trend_score = 0 (broken).

### **Solution**
Enforce specific parseable format for all TradingView summaries.

### **Required Format**

**All TradingView summaries MUST include:**

```markdown
**Price:** [number]  OR  **Price:** $[number]
**50-DMA:** [number]
**200-DMA:** [number]
```

### **Valid Examples**

```markdown
# Valid Format
**Price:** 6747.50
**50-DMA:** 6705
**200-DMA:** 6450

# Also Valid
**Price:** $63500
**50-DMA:** 71000
**200-DMA:** 58500

# NOT VALID - Parser won't find these
**Current Price:** 6747.50  (should be "Price:")
**50-Day MA:** 6705         (should be "50-DMA:")
**200-Day MA:** 6450        (should be "200-DMA:")
Price: 6747.50              (missing ** formatting)
```

### **Why This Matters**
SummaryParser uses regex patterns to extract these values:
```python
# Pattern: "(?:trading|hovering|price)[:\s]+...(\d+\.?\d*)"
# Matches: "Price: 6747.50" ✅
# Matches: "Price: $6747.50" ✅
# Matches: "trading near 6747.50" ✅
# Doesn't match: "Current Price:" ❌

# Pattern: "50[-\s]?(?:day\s)?(?:EMA|SMA|MA|DMA)[:\s]*[\(\@]?\s*(\d+\.?\d*)"
# Matches: "50-DMA: 6705" ✅
# Matches: "50 DMA: 6705" ✅
# Matches: "50-day MA: 6705" ✅
# Doesn't match: "50-Day MA:" with space variation ❌
```

### **Verification Step**

After creating/updating technical summaries:

```bash
# Search for required patterns
grep -c "Price:" Research/Technicals/TradingView*/YYYY-MM-DD*Summary.md
# Result: Should find "Price:" in each file

grep -c "50-DMA:" Research/Technicals/TradingView*/YYYY-MM-DD*Summary.md
# Result: Should find "50-DMA:" in each file

grep -c "200-DMA:" Research/Technicals/TradingView*/YYYY-MM-DD*Summary.md
# Result: Should find "200-DMA:" in each file
```

### **What If Parser Still Fails**
- Verify format matches examples above
- Re-run signal calculator: `python scripts/processing/calculate_signals.py YYYY-MM-DD`
- If still NONE returned: Parser has deeper issue → fallback to FIX #5 (AI adjustment)

---

## FIX #3: STEP 2 RECOVERY (Don't Stop If Providers Missing)

### **Problem**
When Step 1 couldn't generate RSS or YouTube summaries (missing data), workflow assumed failure and stopped. No mechanism to skip providers and continue.

### **Solution**
Explicit skip logic: if provider data missing, skip that overview but continue workflow.

### **Step 2 Decision Tree**

```
Step 2.1: RSS Overview
├─ Check: RSS provider summaries exist? (Pattern: Research/RSS/*/YYYY-MM-DD*Summary.md)
├─ YES → Create RSS Overview
└─ NO → SKIP (don't create file, don't stop workflow)

Step 2.2: YouTube Overview
├─ Check: YouTube channel summaries exist? (Pattern: Research/YouTube/*/YYYY-MM-DD*Summary.md)
├─ YES → Create YouTube Overview
└─ NO → SKIP (don't create file, don't stop workflow)

Step 2.3: Technical Overview (ALWAYS CREATE)
├─ 7 technical summaries confirmed in Step 1 verification
└─ CREATE (synthesize from available technical providers)

Step 2.4: X/Twitter Overview (ALWAYS CREATE)
├─ X Crypto + Macro summaries confirmed in Step 1 verification
└─ CREATE (aggregate X sentiment data)

Step 2.5: Key Themes (CREATE WITH AVAILABLE DATA)
├─ Sources available: Technical Overview + X Overview + Market Data
├─ If RSS/YouTube missing: note in themes document
└─ CREATE (cross-reference available sources)

Result: Even without RSS/YouTube, Step 2 produces:
  - Technical Overview ✅
  - X Overview ✅
  - Key Themes ✅
  → Enough to proceed to Step 3 ✅
```

### **Implementation**

```python
# Pseudocode for Step 2 recovery

# Step 2.1
rss_files = glob(Research/RSS/*/YYYY-MM-DD*Summary.md)
if len(rss_files) > 0:
    create_rss_overview()
else:
    log("No RSS summaries found, skipping RSS Overview")
    # Continue to next step!

# Step 2.2
youtube_files = glob(Research/YouTube/*/YYYY-MM-DD*Summary.md)
if len(youtube_files) > 0:
    create_youtube_overview()
else:
    log("No YouTube summaries found, skipping YouTube Overview")
    # Continue to next step!

# Step 2.3 - ALWAYS RUN
technical_files = glob(Research/Technicals/TradingView*/YYYY-MM-DD*Summary.md)
# Must have 4 technical summaries from verification (Step 1)
create_technical_overview()  # MANDATORY

# Step 2.4 - ALWAYS RUN
x_files = glob(Research/X/YYYY-MM-DD_X_*.md)
# Must have 2 X summaries from verification (Step 1)
create_x_overview()  # MANDATORY

# Step 2.5 - Use available overviews
available_sources = []
if rss_overview_exists:
    available_sources.append("RSS")
if youtube_overview_exists:
    available_sources.append("YouTube")
available_sources.extend(["Technical", "X"])  # Always available
create_key_themes(available_sources)  # Create with what's available
```

### **Documentation**
In completion report, note:
- Which overviews created: ✅ Technical, ✅ X, ✅ Key Themes
- Which overviews skipped: ❌ RSS (no summaries), ❌ YouTube (no summaries)
- Result: Workflow continued successfully with available data

---

## FIX #4: EMPTY SCRAPER OUTPUTS (Distinguish Failure vs No Data)

### **Problem**
Bookmarks scraper produced `x_bookmarks_posts_20251019023018.json` with contents `[]` (empty array). No summary created. Unclear if this was failure or no-data situation.

### **Solution**
Distinguish between:
- **Empty data** = No new content on that date (NORMAL, continue)
- **Scraper crash** = Process failed (TRY ONCE MORE, then skip)

### **Decision Tree**

```
Check bookmarks JSON file: x_bookmarks_posts_YYYYMMDD*.json

File contains: []  (empty array)
├─ Interpretation: VALID OUTPUT - no new bookmarks on this date
├─ Action: Create summary noting "Zero new bookmarks collected"
├─ Workflow impact: NONE - proceed normally
└─ Reason: Bookmarks are OPTIONAL data source

File doesn't exist OR contains error
├─ Interpretation: LIKELY SCRAPER FAILED
├─ Action: Check scraper output logs
├─ Retry: Run once more → if fails again, skip
├─ Workflow impact: NOTE IT, but continue with available data
└─ Reason: Bookmarks are OPTIONAL; other data (X Crypto/Macro) still available

File contains valid posts
├─ Create summary from JSON data
├─ Normal processing continues
└─ No issues
```

### **Implementation**

```python
# Check bookmarks status

bookmarks_file = Research/X/Bookmarks/x_bookmarks_posts_YYYYMMDD*.json

with open(bookmarks_file) as f:
    data = json.load(f)

if data == []:
    # Empty array = no new bookmarks
    create_bookmarks_summary(
        content="Zero new bookmarks collected for YYYY-MM-DD. "
                "Scraper ran successfully but found no new bookmarked content."
    )
    log("Bookmarks: ZERO NEW (normal)")
    # Continue workflow

elif len(data) > 0:
    # Valid posts found
    create_bookmarks_summary_from_data(data)
    log("Bookmarks: VALID DATA")
    # Continue workflow

else:
    # Unexpected format
    log("Bookmarks: UNEXPECTED FORMAT - checking scraper logs")
    # This indicates scraper issue
```

### **For Other Scrapers (YouTube, RSS)**

If YouTube or RSS scraper fails:
- **First attempt**: Check error message, try ONE retry
- **If retry fails**: Skip that provider, document in report
- **Continue workflow**: Don't let one scraper block everything
- **Document**: Note which providers failed in completion report

---

## FIX #5: SIGNAL CALCULATION ROBUSTNESS (Handle Parser Failures)

### **Problem**
Signal calculator completed but trend = 0 (should be 10-20 for bullish market). Investigation revealed SummaryParser couldn't extract price/MA data from files. No process to check this or apply fallback.

### **Solution**
Add robustness check: If trend = 0, verify parser extraction, then apply AI adjustment if market contradicts.

### **Detection & Recovery Process**

```
Step 1: Check if trend score = 0
   └─ signals_YYYY-MM-DD.json shows "trend": 0

Step 2: Investigate why
   ├─ Check TradingView summaries for Format (Fix #2)
   │  └─ Look for: "Price:" + "50-DMA:" + "200-DMA:"
   │  └─ If missing → ADD THEM (see Fix #2)
   │
   ├─ Re-run signal calculator
   │  └─ If trend still 0 → Parser path issue (known issue #1)
   │
   └─ If format correct but parser fails → Proceed to Step 3

Step 3: Verify market evidence
   ├─ Open 2025-YYYY-MM-DD_market_data.md
   ├─ Check current price vs recent highs
   ├─ Check technical ratings (should see "Strong Buy" if market strong)
   └─ If price NEAR HIGHS + STRONG BUY + SUPPORT HOLDING → trend should NOT be 0

Step 4: Apply AI Adjustment (Per workflow Step 4, lines 498-530)
   ├─ Original score: 0
   ├─ Review evidence from Step 3
   ├─ Determine adjustment: +5 to +15 (per guidance)
   │  └─ +5 if weak bullish evidence
   │  └─ +10 if moderate bullish evidence
   │  └─ +15 if strong bullish evidence
   ├─ Update signals_YYYY-MM-DD.json:
   │  ├─ Change "trend": 0 → "trend": [adjusted_value]
   │  ├─ Update composite score: old - 0 + adjusted_value
   │  ├─ Update tier if composite crosses threshold
   │  └─ Add entry to ai_adjustments array with reasoning
   └─ Verify composite > 0 after adjustment

Step 5: Document & Continue
   ├─ File now has accurate signals
   ├─ Dashboard update can proceed
   └─ Note fix in completion report
```

### **Example: 2025-10-19 Adjustment**

```json
Original signals:
{
  "composite": 28.5,
  "tier": "WEAK",
  "breakdown": {
    "trend": 0,
    "breadth": 12.5,
    "volatility": 6,
    "technical": 5.0,
    "seasonality": 5.0
  },
  "ai_adjustments": []
}

Investigation found:
- Market data: SPX 6664 vs ATH 6745 (1.2% below = strong position)
- TradingView SPX: "Strong Buy" rating, 9 buy signals vs 3 sell
- Support: 6690-6727 consistently defended
- Conclusion: Bullish structure, trend should NOT be 0

Applied adjustment:
{
  "ai_adjustments": [
    {
      "component": "Trend",
      "original_score": 0,
      "adjusted_score": 15,
      "reasoning": "Parser failed to extract MA data. Manual review: SPX at 6664 vs ATH 6745 (strong position). TradingView shows Strong Buy with 9 buy signals. Bullish MA structure (price > 50-DMA > 200-DMA) confirmed in summary. Buyers defending 6690-6727 support. Evidence supports trend of +15."
    }
  ]
}

Updated signals:
- Trend: 0 → 15
- Composite: 28.5 → 43.5
- Tier: WEAK → MODERATE
- Result: Accurate signals ready for dashboard
```

### **When to Apply Adjustment**

Apply adjustment if:
- ✅ Trend = 0 (impossible score)
- ✅ Market evidence contradicts (price near high, strong buy rating, support holding)
- ✅ Parser format verified (has Price:/50-DMA:/200-DMA:)
- ✅ Still returned NONE (path issue, not format issue)

Don't apply if:
- ❌ Trend has reasonable value (5, 10, 15, etc.)
- ❌ Trend = 0 AND market is truly bearish
- ❌ Signal is biased/hype (no evidence in data)

---

## Implementation Checklist

For future research workflow runs, execute this checklist:

### **Before Step 2**
- [ ] Run Step 1 Verification Checkpoint (FIX #1)
- [ ] Verify 4 technical + 2 X summaries exist
- [ ] Document any optional providers missing

### **After Creating Technical Summaries**
- [ ] Verify TradingView format: Price, 50-DMA, 200-DMA (FIX #2)
- [ ] Search for "Price:" in summaries
- [ ] Search for "50-DMA:" in summaries
- [ ] Search for "200-DMA:" in summaries

### **During Step 2**
- [ ] Skip RSS if no summaries (don't create placeholder) (FIX #3)
- [ ] Skip YouTube if no summaries (don't create placeholder) (FIX #3)
- [ ] Always create Technical Overview (FIX #3)
- [ ] Always create X Overview (FIX #3)
- [ ] Create Key Themes from available sources (FIX #3)

### **After Signal Calculation**
- [ ] Check if trend = 0 (FIX #5)
- [ ] If yes, verify TradingView format (FIX #2)
- [ ] Review market data for trend contradiction
- [ ] If contradiction found, apply AI adjustment (FIX #5)
- [ ] Verify composite > 0 before proceeding

### **Scraper Issues**
- [ ] If bookmarks `[]` = document "Zero new" and continue (FIX #4)
- [ ] If other scraper fails: note it, skip provider, continue (FIX #4)

### **Final Report**
- [ ] Document all 5 fixes applied
- [ ] List any skipped providers
- [ ] Confirm all 14 critical files exist
- [ ] Verify signals quality (trend > 0)
- [ ] Ready for dashboard update

---

## Reference: Files Modified

1. **Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt**
   - Added "CRITICAL WORKFLOW SAFEGUARDS (Prevent Blocking Failures)" section
   - Added FIX #1 through FIX #5 with detailed explanations
   - Location: After line 20

---

## Questions & Troubleshooting

**Q: How do I know if a scraper failed vs produced empty data?**
A: Check output file:
- `[]` in JSON = empty data (normal, continue)
- File missing or error = failure (try once more, then skip)
- Text error in file = failure (document, skip provider)

**Q: What if all overviews are missing?**
A: This won't happen because Step 1 verification (FIX #1) guarantees minimum data. If Step 1 passes, you'll have at minimum:
- 4 technical summaries → can create Technical Overview
- 2 X summaries → can create X Overview
- Both → can create Key Themes

**Q: Can I skip the verification checkpoint?**
A: No. This is your guard against cascading failures. Takes 30 seconds, saves hours of debugging.

**Q: If trend stays 0 after fixing format, what do I do?**
A: Apply AI adjustment (FIX #5). Document parser issue. Continue workflow. Report to developer for deeper fix.

**Q: How do I know my AI adjustment is reasonable?**
A: Guidance from workflow:
- Max adjustment: ±15 points
- Justify with market evidence (price levels, technical indicators, support/resistance)
- Don't adjust based on bias or feelings
- Must contradict signal (e.g., trend=0 but market bullish)

---

**Document Version**: 1.0
**Status**: Production Ready ✅
**Last Updated**: October 19, 2025
