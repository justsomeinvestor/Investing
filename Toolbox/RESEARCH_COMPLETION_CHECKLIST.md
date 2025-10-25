# Research Workflow Completion Checklist

**Purpose**: Daily verification checklist to ensure research workflow completes successfully
**Usage**: Run through this checklist after each daily research workflow
**Date Updated**: October 19, 2025
**Version**: 1.0

---

## PRE-WORKFLOW: Setup & Planning

### **Date & Preparation**
- [ ] Today's date determined (YYYY-MM-DD format)
- [ ] All dates in commands replaced with today's date
- [ ] TodoWrite tool initialized to track 6 steps
- [ ] Workspace verified (correct directory)

### **Review Recent Fixes**
- [ ] Read WORKFLOW_SAFEGUARDS_GUIDE.md (5 critical fixes)
- [ ] Understand FIX #1: Step 1 verification checkpoint
- [ ] Understand FIX #2: TradingView format requirements
- [ ] Understand FIX #3: Step 2 recovery (skip missing providers)
- [ ] Understand FIX #4: Empty scraper output handling
- [ ] Understand FIX #5: Signal robustness (trend=0 check)

---

## STEP 0: Data Collection (5-10 minutes)

### **0A: Automated Scrapers**
- [ ] Ran: `python scripts/automation/run_all_scrapers.py`
- [ ] Expected output:
  - [ ] X/Twitter scraper completed (lists, posts)
  - [ ] Bookmarks scraper completed
  - [ ] X data archival completed
  - [ ] Technical data scraper completed (SPY/QQQ options)
- [ ] Output files exist:
  - [ ] `Research/.cache/YYYY-MM-DD_technical_data.json` exists (has size >0)

### **0B: Web Searches for Market Data**
- [ ] Executed 8 web searches in parallel
- [ ] Created: `Research/.cache/YYYY-MM-DD_market_data.md`
- [ ] File contains:
  - [ ] SPY/SPX current price
  - [ ] Volatility metrics (VIX)
  - [ ] Technical levels (support/resistance)
  - [ ] Options flow insights
  - [ ] Hedge fund positioning
  - [ ] Fed/economic policy notes

**If issues**:
- [ ] Bookmarks empty (`[]`)? → NORMAL, create summary noting "Zero new bookmarks"
- [ ] Technical scraper failed? → Try retry once, document, proceed with available data
- [ ] Web searches timeout? → Retry failed searches, use partial results if needed

---

## STEP 1: Individual Provider Summaries (30-45 minutes)

### **✅ FIX #1: VERIFICATION CHECKPOINT (BEFORE Step 2)**

**Required Files Check** - Use Glob:

```
Pattern: Research/Technicals/TradingView*/YYYY-MM-DD*Summary.md
Expected: Find 4 files
- [ ] TradingView SPX Summary (✅ found)
- [ ] TradingView BTC Summary (✅ found)
- [ ] TradingView QQQ Summary (✅ found)
- [ ] TradingView SOL Summary (✅ found)

Pattern: Research/X/YYYY-MM-DD_X_*.md
Expected: Find 2 files
- [ ] X Crypto Summary (✅ found)
- [ ] X Macro Summary (✅ found)
```

**Optional Files Check**:

```
Pattern: Research/RSS/*/YYYY-MM-DD*Summary.md
Expected: 0 or more files
- [ ] RSS provider summaries (if any exist, note count: ___)

Pattern: Research/YouTube/*/YYYY-MM-DD*Summary.md
Expected: 0 or more files
- [ ] YouTube channel summaries (if any exist, note count: ___)

Pattern: Research/X/Bookmarks/YYYY-MM-DD*Summary.md
Expected: 0 or 1 file
- [ ] X Bookmarks summary (if empty JSON exists, create "Zero new" summary)
```

**Decision Logic**:
- [ ] If ALL REQUIRED (4 tech + 2 X) found → ✅ PROCEED TO STEP 2
- [ ] If ANY REQUIRED missing → ❌ STOP, create them now, then proceed
- [ ] If OPTIONAL missing → ⚠️ NOTE IT, but still proceed to Step 2

**If REQUIRED Files Missing**:
- [ ] Identify which summaries missing
- [ ] Create them using web search data or market data
- [ ] Document what sources used
- [ ] Add to completion report

---

## STEP 2: Category Overviews (45-60 minutes)

### **✅ FIX #3: Skip Missing Providers, Don't Stop Workflow**

### **Step 2.1: RSS Overview**
- [ ] Check: RSS provider summaries exist? (Pattern: `Research/RSS/*/YYYY-MM-DD*Summary.md`)
  - [ ] YES → Create `Research/RSS/YYYY-MM-DD_RSS_Overview.md` ✅
  - [ ] NO → Skip (don't create placeholder) and continue ⚠️
- [ ] If created, verify file has content (>500 characters)

### **Step 2.2: YouTube Overview**
- [ ] Check: YouTube summaries exist? (Pattern: `Research/YouTube/*/YYYY-MM-DD*Summary.md`)
  - [ ] YES → Create `Research/YouTube/YYYY-MM-DD_YouTube_Overview.md` ✅
  - [ ] NO → Skip (don't create placeholder) and continue ⚠️
- [ ] If created, verify file has content (>500 characters)

### **Step 2.3: Technical Overview** (✅ ALWAYS CREATE)
- [ ] Synthesized all 7 technical summaries:
  - [ ] TradingView SPX
  - [ ] TradingView BTC
  - [ ] TradingView QQQ
  - [ ] TradingView SOL
  - [ ] Fear & Greed Index
  - [ ] Market Breadth
  - [ ] Volatility Metrics
- [ ] Created: `Research/Technicals/YYYY-MM-DD_Technical_Overview.md`
- [ ] File has content (>2000 characters)
- [ ] Includes sections:
  - [ ] Cross-asset landscape
  - [ ] Key levels by asset
  - [ ] Risk assessment matrix
  - [ ] Trading implications

### **Step 2.4: X/Twitter Overview** (✅ ALWAYS CREATE)
- [ ] Aggregated data:
  - [ ] X Crypto Summary
  - [ ] X Macro Summary
  - [ ] X Bookmarks status (zero new? note it)
- [ ] Created: `Research/X/YYYY-MM-DD_X_Overview.md`
- [ ] File has content (>1500 characters)
- [ ] Includes sections:
  - [ ] Crypto sentiment analysis
  - [ ] Macro sentiment analysis
  - [ ] Conflicting narratives
  - [ ] Opportunities identified

### **Step 2.5: Key Themes Document** (CREATE WITH AVAILABLE DATA)
- [ ] Identified cross-provider consensus themes (appear in 3+ sources)
- [ ] Created: `Research/.cache/YYYY-MM-DD_key_themes.md`
- [ ] File has content (>2000 characters)
- [ ] Includes sections:
  - [ ] Cross-provider consensus (bullish + bearish narratives)
  - [ ] Divergences & disagreements
  - [ ] Catalyst calendar
  - [ ] Risk assessment summary

### **✅ FIX #2: TradingView Format Verification**

After creating Technical Overview, verify format in TradingView summaries:

```
- [ ] TradingView SPX contains: "Price:", "50-DMA:", "200-DMA:"
- [ ] TradingView BTC contains: "Price:", "50-DMA:", "200-DMA:"
- [ ] TradingView QQQ contains: "Price:", "50-DMA:", "200-DMA:"
- [ ] TradingView SOL contains: "Price:", "50-DMA:", "200-DMA:"
```

Command to verify:
```bash
grep -l "Price:" Research/Technicals/TradingView*/YYYY-MM-DD*Summary.md
# Result: Should find files
```

---

## STEP 3: Market Sentiment Overview (30-45 minutes)

### **CRITICAL FILE - BLOCKS DASHBOARD IF MISSING**

- [ ] Read all category overviews created in Step 2:
  - [ ] Technical Overview (MANDATORY - should exist)
  - [ ] X Overview (MANDATORY - should exist)
  - [ ] RSS Overview (optional - may not exist)
  - [ ] YouTube Overview (optional - may not exist)
  - [ ] Key Themes (MANDATORY - should exist)

- [ ] Created: `Research/.cache/YYYY-MM-DD_Market_Sentiment_Overview.md`
  - [ ] File exists ✅
  - [ ] File has content (>3000 characters)

- [ ] Includes all required sections:
  - [ ] Executive Summary (2-3 sentences)
  - [ ] Cross-Provider Consensus (bulls vs bears)
  - [ ] Key Levels to Watch (SPX, BTC, QQQ with support/resistance)
  - [ ] Major Catalysts This Week
  - [ ] Aggregate Sentiment Score (0-100)
  - [ ] Risk Level Assessment (LOW/MEDIUM/HIGH)

- [ ] Quality checks:
  - [ ] Sentiment score assigned (0-100 range)
  - [ ] Risk level clearly stated
  - [ ] References to category overviews visible
  - [ ] Trading implications included

**If file missing**: ❌ CANNOT PROCEED TO DASHBOARD - create now

---

## STEP 4: Calculate Trading Signals (10-15 minutes)

### **Run Signal Calculator**
- [ ] Executed: `python scripts/processing/calculate_signals.py YYYY-MM-DD`
- [ ] Output file created: `Research/.cache/signals_YYYY-MM-DD.json`
- [ ] File has valid JSON structure (no syntax errors)

### **✅ FIX #5: Signal Robustness - Check for Component = 0**

Open signals file and check:

```json
"breakdown": {
  "trend": 0,        ← CHECK THIS FIRST
  "breadth": X,
  "volatility": X,
  "technical": X,
  "seasonality": X
}
```

- [ ] Trend score is NOT 0 → ✅ PASS, proceed normally
- [ ] Trend score = 0 → ⚠️ INVESTIGATE (see below)

### **If Trend = 0: Investigation Steps**

1. [ ] Verify TradingView format (FIX #2):
   - [ ] All TradingView summaries have "Price:", "50-DMA:", "200-DMA:"?
   - [ ] YES → Re-run signal calculator: `python scripts/processing/calculate_signals.py YYYY-MM-DD`
   - [ ] If still 0 → Parser issue confirmed, proceed to step 2

2. [ ] Review market evidence from `Research/.cache/YYYY-MM-DD_market_data.md`:
   - [ ] Current price vs recent highs (is market near ATH?)
   - [ ] Technical rating (is it "Strong Buy"?)
   - [ ] Support levels (are they being defended?)
   - [ ] Overall sentiment (bullish or bearish?)

3. [ ] If market IS bullish but trend = 0:
   - [ ] Apply AI Adjustment (FIX #5):
     - [ ] Set trend: 0 → 15 (or 10 if only mildly bullish)
     - [ ] Update composite score: original + 15
     - [ ] Update tier if composite crosses threshold
     - [ ] Add entry to ai_adjustments array with reasoning

4. [ ] If market is truly bearish:
   - [ ] Trend = 0 may be correct
   - [ ] Do NOT apply adjustment
   - [ ] Document why in completion report

### **Verification Checklist**

- [ ] Composite score between 0-100 ✅
- [ ] Tier assigned (WEAK/MODERATE/STRONG/EXTREME) ✅
- [ ] All component scores present ✅
- [ ] X sentiment scores extracted ✅
- [ ] JSON is valid (no syntax errors) ✅
- [ ] AI adjustments documented (if any applied) ✅

---

## STEP 5: Finalize & Verify (15-20 minutes)

### **File Existence Verification (14 CRITICAL FILES)**

Use Glob or find commands to verify:

```
1. [ ] Research/.cache/YYYY-MM-DD_market_data.md (Step 0B)
2. [ ] Research/.cache/YYYY-MM-DD_technical_data.json (Step 0A)
3. [ ] Research/Technicals/TradingView SPX/YYYY-MM-DD_TradingView SPX_Summary.md (Step 1.3)
4. [ ] Research/Technicals/TradingView BTC/YYYY-MM-DD_TradingView BTC_Summary.md (Step 1.3)
5. [ ] Research/Technicals/TradingView QQQ/YYYY-MM-DD_TradingView QQQ_Summary.md (Step 1.3)
6. [ ] Research/Technicals/TradingView SOL/YYYY-MM-DD_TradingView SOL_Summary.md (Step 1.3)
7. [ ] Research/X/YYYY-MM-DD_X_Crypto_Summary.md (Step 1.4)
8. [ ] Research/X/YYYY-MM-DD_X_Macro_Summary.md (Step 1.4)
9. [ ] Research/X/Bookmarks/YYYY-MM-DD_X_Bookmarks_Summary.md (Step 1.5)
10. [ ] Research/Technicals/YYYY-MM-DD_Technical_Overview.md (Step 2.3)
11. [ ] Research/X/YYYY-MM-DD_X_Overview.md (Step 2.4)
12. [ ] Research/.cache/YYYY-MM-DD_key_themes.md (Step 2.5)
13. [ ] Research/.cache/YYYY-MM-DD_Market_Sentiment_Overview.md (Step 3) ← CRITICAL
14. [ ] Research/.cache/signals_YYYY-MM-DD.json (Step 4)
```

**Count Result**: _____ / 14 files found

- [ ] 14/14 files present → ✅ COMPLETE, proceed to dashboard
- [ ] <14 files → ⚠️ IDENTIFY MISSING, create if possible, or document

### **Signal Quality Final Check**

- [ ] Composite score > 0 ✅
- [ ] Tier assigned ✅
- [ ] No component = 0 (except if market truly bearish) ✅
- [ ] AI adjustments documented if applied ✅

### **Issues Encountered Documentation**

Record any issues that occurred:

```
Issue 1: ________________________________
Resolution: ________________________________
Status: [ ] Fixed  [ ] Workaround Applied  [ ] Noted for developer

Issue 2: ________________________________
Resolution: ________________________________
Status: [ ] Fixed  [ ] Workaround Applied  [ ] Noted for developer
```

---

## FINAL COMPLETION REPORT

### **Template to Fill Out**

```
🎯 RESEARCH WORKFLOW COMPLETE FOR [DATE]

✅ STEP 0: Data Collection
  - Automated technical data collected: YES/NO
  - Market data gathered via web search: YES/NO

✅ STEP 1: Provider Summaries (___/14 required files)
  - TradingView SPX Summary: YES/NO
  - TradingView BTC Summary: YES/NO
  - TradingView QQQ Summary: YES/NO
  - TradingView SOL Summary: YES/NO
  - X Crypto Sentiment Summary: YES/NO
  - X Macro Sentiment Summary: YES/NO
  - X Bookmarks Summary: YES/NO (notes: ________)

✅ STEP 2: Category Overviews
  - RSS Overview: YES/NO (optional)
  - YouTube Overview: YES/NO (optional)
  - Technical Overview: YES/NO
  - X/Twitter Overview: YES/NO
  - Key Themes identified: YES/NO

✅ STEP 3: Market Sentiment Overview
  - Executive summary created: YES/NO
  - Sentiment score assigned (0-100): ___
  - Risk level assessed: LOW/MEDIUM/HIGH

✅ STEP 4: Trading Signals
  - Composite score calculated: ___/100
  - Tier assigned: WEAK/MODERATE/STRONG/EXTREME
  - Trend score checked (not 0): YES/NO
  - AI adjustments applied (if needed): YES/NO

📊 Output Files Created: ___/14 critical files

⚠️ Issues Encountered: NONE / (list): ___________

🚀 Status: ✅ WORKFLOW COMPLETE - READY FOR DASHBOARD UPDATE
```

### **Next Step**
```
[ ] All checks passed → Proceed to Master Plan workflow
    Command: @master-plan/How_to_use_MP_CLAUDE_ONLY.txt

[ ] Issues found → Document in completion report, note workarounds
    Dashboard can still update with available data
```

---

## Quick Reference: Troubleshooting

### **If Step X fails...**

**Step 0 (Scrapers)**
- [ ] Bookmarks empty → NORMAL, create "Zero new" summary
- [ ] Tech scraper failed → Try once more, then skip & proceed
- [ ] Web search timeout → Retry failed searches, use partial data

**Step 1 (Summaries)**
- [ ] Missing 4 required technical → CREATE NOW before Step 2
- [ ] Missing 2 required X summaries → CREATE NOW before Step 2
- [ ] Missing RSS/YouTube → OK, skip & proceed to Step 2

**Step 2 (Overviews)**
- [ ] RSS overview failing → Skip (optional)
- [ ] YouTube overview failing → Skip (optional)
- [ ] Technical overview failing → ERROR, investigate
- [ ] X overview failing → ERROR, investigate

**Step 3 (Market Sentiment)**
- [ ] Cannot create → ERROR, check Step 2 overviews exist
- [ ] This file CRITICAL for dashboard

**Step 4 (Signals)**
- [ ] Trend = 0 → Check TradingView format, apply AI adjustment if bullish market
- [ ] Other component = 0 → Normal, not error
- [ ] Composite = 0 → ERROR, all components broken

---

## Document Information

**Checklist Version**: 1.0
**Last Updated**: October 19, 2025
**Status**: Production Ready ✅
**Suggested Review**: Use this checklist for every daily research workflow
