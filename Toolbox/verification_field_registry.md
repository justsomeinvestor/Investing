# Verification Field Registry

**Last Updated:** 2025-10-26
**Coverage:** 28/34 timestamp fields (82% of all fields, 100% of critical fields)
**Health Status:** 100% (28/28 current)

---

## Overview

Complete registry of all timestamp fields tracked by Wingman's verification system. This document defines which fields are tracked, who owns them (Phase 2 automated or Phase 5 AI), and what they represent.

### Quick Stats
- **Total fields in master-plan.md:** 34
- **Fields tracked by verify_timestamps.py:** 28
- **Phase 2 owned (automated):** 15 (added contrarian detector tracking)
- **Phase 5 owned (AI synthesis):** 13
- **Expected health after Phase 2:** 54% (15/28 current)
- **Expected health after Phase 5:** 100% (28/28 current)

---

## Field Classification

### Phase 2: Automated Sync (Owned by sync scripts)

These fields are set automatically during wingman dash Phase 2 (data synchronization). Updated by various sync_*.py scripts.

| Line | Field Path | Script | Purpose | Format |
|------|-----------|--------|---------|--------|
| 6 | `dashboard.lastUpdated` | `update_master_plan.py` | Overall dashboard timestamp | ISO 8601 |
| 7 | `dashboard.sentimentCardsUpdated` | `update_master_plan.py` | Sentiment card metrics | ISO 8601 |
| 29 | `dashboard.metricsUpdated` | `update_master_plan.py` | Market metrics (BTC, SPY, etc.) | ISO 8601 |
| 87 | `dashboard.riskItemsUpdated` | `sync_risk_items.py` | Risk item summaries | ISO 8601 |
| 1109 | `dashboard.quickActionsUpdated` | `update_master_plan.py` | Quick action items | ISO 8601 |
| 1135 | `dashboard.providerConsensusUpdated` | `sync_provider_consensus.py` | Provider consensus roll-up | ISO 8601 |
| 1189 | `dashboard.dailyPlanner.prioritiesUpdated` | `sync_daily_planner.py` | DEPRECATED - no longer set | N/A |
| 1203 | `dashboard.dailyPlanner.keyLevelsUpdated` | `update_master_plan.py` | Key support/resistance levels | ISO 8601 |
| 1228 | `dashboard.dailyPlanner.signalDataUpdated` | `sync_daily_planner.py` | Signal composite score | ISO 8601 |
| 1220 | `dashboard.dailyPlanner.economicCalendarUpdated` | `sync_daily_planner.py` | Economic calendar reference | ISO 8601 |
| 1276 | `dashboard.dailyPlanner.endOfDay.ranAt` | `sync_daily_planner.py` | End-of-day execution timestamp | ISO 8601 |
| 46 | `dashboard.sentimentHistoryUpdated` | (STALE - needs update) | Historical sentiment archive | ISO 8601 |

**Expected Stale After Phase 2:**
- `dashboard.sentimentHistoryUpdated`
- `dashboard.riskItemsUpdated`
- `dashboard.providerConsensusUpdated`
- Tab-specific fields (awaiting Phase 5)

---

### Phase 5: AI Synthesis (Owned by Claude AI)

These fields are set by Claude during Phase 5 (AI interpretation synthesis). These interpret market data and provide tactical guidance.

#### Daily Planner (4 fields)

| Line | Field Path | Purpose | Requires |
|------|-----------|---------|----------|
| 1152 | `dashboard.dailyPlanner.aiInterpretation.updatedAt` | Daily narrative synthesis | Market context + signal |
| 1233 | `dashboard.dailyPlanner.recommendationUpdated` | Trading recommendation tier | Signal data + market analysis |
| 1245 | `dashboard.dailyPlanner.actionChecklistUpdated` | Tactical action items | Portfolio + market state |
| 1181 | `dashboard.dailyPlanner.prioritiesUpdated` | Top 5 priorities (NEW) | actionChecklist source |

#### Portfolio Tab (2 fields)

| Line | Field Path | Purpose | Requires |
|------|-----------|---------|----------|
| 106 | `tabs.portfolio.aiInterpretation.updatedAt` | Portfolio analysis & recommendation | Allocation + signal |
| 106 | `tabs.portfolio.portfolioRecommendation.updatedAt` | Portfolio allocation tier | Risk/reward analysis |

#### Markets Intelligence Tab (1 field)

| Line | Field Path | Purpose | Requires |
|------|-----------|---------|----------|
| 157 | `tabs.markets.aiInterpretation.updatedAt` | Consolidated macro/crypto/tech analysis | Research + provider data |

#### News & Catalysts Tab (1 field)

| Line | Field Path | Purpose | Requires |
|------|-----------|---------|----------|
| 450 | `tabs.news_catalysts.aiInterpretation.updatedAt` | News sentiment + catalyst analysis | News scraping + filtering |

#### X Sentiment Tab (4 fields)

| Line | Field Path | Purpose | Requires |
|------|-----------|---------|----------|
| 369 | `tabs.xsentiment.aiInterpretation.updatedAt` | X platform sentiment synthesis | Twitter API + sentiment calc |
| 369 | `tabs.xsentiment.socialTabSyncedAt` | Last sync from X API | API data availability |
| 1010 | `tabs.xsentiment.crypto_trending.updatedAt` | Top crypto trending tickers | X search + mentions |
| 1010 | `tabs.xsentiment.macro_trending.updatedAt` | Top macro trending topics | X search + mentions |
| 643 | `tabs.xsentiment.contrarian_detector.updatedAt` | Contrarian analysis & opportunity detection | Sentiment score calculation |

#### Technicals Tab (4 fields - Phase 2)

| Line | Field Path | Purpose | Requires |
|------|-----------|---------|----------|
| 896 | `tabs.technicals.aiInterpretation.updatedAt` | Technical analysis synthesis | Chart data + pattern detection |
| 896 | `tabs.technicals.technicalsTabSyncedAt` | Last technical data sync | Data source availability |
| 1030 | `tabs.technicals.tradingSignalScore.updatedAt` | Trading signal score freshness | Market signal calculation |
| 1122+ | `tabs.technicals.unusualActivity.updatedAt` | Unusual options activity detection | P/C ratio spikes, IV extremes, etc. |

---

## Verification Health Matrix

### Expected Health After Each Phase

```
Pre-Dash:     0%  (0/25 current)
Phase 2:     48%  (12/25 current) ← Automated sync complete
Phase 5:    100%  (25/25 current) ← AI synthesis complete
```

### Current Status (2025-10-26 Post-Phase-2)

```
✅ CURRENT (20/25):
  - dashboard.lastUpdated
  - dashboard.sentimentCardsUpdated
  - dashboard.metricsUpdated
  - dashboard.quickActionsUpdated
  - dashboard.dailyPlanner.keyLevelsUpdated
  - dashboard.dailyPlanner.signalDataUpdated
  - dashboard.dailyPlanner.economicCalendarUpdated
  - dashboard.dailyPlanner.aiInterpretation.updatedAt
  - dashboard.dailyPlanner.endOfDay.ranAt
  - dashboard.dailyPlanner.recommendationUpdated
  - dashboard.dailyPlanner.actionChecklistUpdated
  - tabs.portfolio.aiInterpretation.updatedAt
  - tabs.portfolio.portfolioRecommendation.updatedAt
  - tabs.markets.aiInterpretation.updatedAt
  - tabs.news_catalysts.aiInterpretation.updatedAt
  - tabs.xsentiment.aiInterpretation.updatedAt
  - tabs.xsentiment.socialTabSyncedAt
  - tabs.technicals.aiInterpretation.updatedAt
  - tabs.technicals.technicalsTabSyncedAt
  - (1 more field - see stale list)

⚠️  STALE (5/25, expected):
  - dashboard.sentimentHistoryUpdated (yesterday)
  - dashboard.riskItemsUpdated (yesterday)
  - dashboard.providerConsensusUpdated (yesterday)
  - tabs.xsentiment.crypto_trending.updatedAt (yesterday)
  - tabs.xsentiment.macro_trending.updatedAt (yesterday)

❌ VERY_STALE: 0
❌ MISSING: 0
```

### Stale Fields Explanation

The 5 stale fields are **expected** at this stage (post-Phase-2, pre-Phase-5):
- **Risk items:** Require AI synthesis to identify & summarize (Phase 5)
- **Provider consensus:** Requires consolidation of provider opinions (Phase 5)
- **Trending tickers:** Require X sentiment processing (Phase 5)
- **Historical sentiment:** Updates after Phase 5 completes

These will transition to "current" during Phase 5 AI synthesis.

---

## How to Use This Registry

### For Developers

1. **Adding a new timestamp field:**
   - Add field to master-plan.md
   - Add path to `REQUIRED_TIMESTAMPS` in verify_timestamps.py
   - Add entry to this registry
   - Update sync script if Phase 2 (automated)

2. **Checking field ownership:**
   - Phase 2 field? Update `sync_daily_planner.py` or other sync script
   - Phase 5 field? Update Claude AI Phase 5 code

3. **Debugging stale sections:**
   - Run: `python scripts/utilities/verify_timestamps.py --json --date 2025-10-26`
   - Compare `stale_sections` with this registry's Phase 2 vs Phase 5 lists
   - If Phase 2 field is stale → check sync script
   - If Phase 5 field is stale → check Claude AI synthesis

### For Operations (wingman dash execution)

1. **After Phase 2 (automated sync):** Expect ~48% health (12/25 fields current)
2. **After Phase 5 (AI synthesis):** Expect 100% health (25/25 fields current)
3. **Dashboard will show:** Green dots (current) for completed sections, yellow/red for stale

---

## Fields Not Tracked (8 fields)

The following 34 - 26 = 8 fields exist but are not tracked. These are lower-priority or sub-field timestamps:

| Field | Reason | Tier |
|-------|--------|------|
| `dashboard.sentimentHistoryUpdated` | Historical archive - low priority | Low |
| Per-provider `lastUpdated` (e.g., "42 Macro lastUpdated") | Too granular, handled at tab level | Low |
| Economic calendar sub-section timestamps | Delegated to parent section | Low |
| Chart-level technical timestamps | Per-chart tracking not critical | Low |
| Metadata fields (footer lastUpdated) | Covered by dashboard.lastUpdated | Meta |
| Other sub-section timestamps | Handled by parent field | Low |

These can be added to `REQUIRED_TIMESTAMPS` in future iterations if more granular tracking is needed.

---

## Phase 2 vs Phase 5 Separation of Concerns

### Why This Separation Exists

**Problem:** Automated sync scripts were overwriting AI-driven content with generic templates, causing dashboard to show "fresh" but stale interpretations.

**Solution:** Clear ownership model:
- **Phase 2 (Automated):** Updates only data-driven fields (signal scores, metrics, calendars)
- **Phase 5 (AI):** Updates only interpretation fields (narratives, recommendations, action items)

### Benefits

1. **No conflicts:** Sync scripts never overwrite AI work
2. **Clear responsibility:** Each phase owns its fields
3. **Faster debugging:** Stale field → know which phase to check
4. **Extensible:** New fields clearly assigned to correct phase

---

## Visual Indicators Implementation

### Dashboard Status Display

All 25 tracked timestamp fields now have **visual date-badge indicators** (colored dots) in the dashboard:

**Color Coding:**
- 🟢 **GREEN** (`status-ok`): Updated within last 12 hours - CURRENT
- 🟡 **YELLOW** (`status-warning`): Updated 12-24 hours ago - STALE (but expected for AI sections)
- 🔴 **RED** (`status-error`): Updated 2+ days ago - VERY_STALE (requires action)

**Sections with Visual Indicators:**
- ✅ Daily Planner: Key Levels, Economic Calendar, Today's Priorities (next to section titles)
- ✅ Dashboard: Risk Monitor, Sentiment Timeline, Provider Consensus (next to section titles)
- ✅ Tab AI Briefings: Portfolio, Markets, News, X Sentiment, Technicals (in AI header)
- ✅ Dashboard Header: Global verification status indicator (top right)

**Implementation:**
- Indicators added via `getDataFreshness(timestamp)` function
- Styled with CSS classes: `.date-badge.status-ok/warning/error`
- Hover tooltips show freshness details
- Synchronized with `verify_timestamps.py` status classifications

---

## Maintenance

### Regular Updates

- [x] Reviewed: 2025-10-26 (initial creation)
- [x] Updated: 2025-10-26 (added visual indicators)
- [ ] Next review: 2025-11-02 (post 1 week)
- [ ] When: After any new timestamp field is added
- [ ] By: Dev + AI engineer

### Common Updates

- **Adding Phase 2 field:** Update sync script + this registry
- **Adding Phase 5 field:** Update Claude AI code + this registry
- **Field deprecation:** Mark as DEPRECATED with reason + replacement

---

## Troubleshooting

### "Health stuck at 80% after Phase 2"
✅ **Expected!** The 5 stale fields require Phase 5 AI synthesis. This is normal.

### "New field not being tracked"
❌ **Action:** Add to `REQUIRED_TIMESTAMPS` in verify_timestamps.py + update this registry

### "Field says stale but just updated"
❌ **Action:** Check timestamp format (must be ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`)

### "Dashboard shows error dots despite fresh timestamps"
❌ **Action:** Check YAML validity: `python -m yaml master-plan/master-plan.md`

---

**End of Registry**

Generated: 2025-10-26
Version: 1.0
Author: Claude Wingman AI
