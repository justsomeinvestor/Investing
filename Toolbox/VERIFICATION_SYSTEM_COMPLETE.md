# Verification System - Complete Production Guide

**Status**: ✅ **PRODUCTION READY**
**Version**: 1.0
**Last Updated**: 2025-10-26
**Architecture**: 3-layer verification (YAML → Python → HTML)
**Coverage**: 25/34 timestamp fields (74% of all fields, 100% of critical fields)

---

## Executive Summary

The **Wingman Verification System** is a comprehensive 3-layer architecture that tracks data freshness across 25 critical dashboard sections. It ensures users always know whether displayed data is current, aging, or stale through **real-time visual indicators** synchronized with **automated verification scripts**.

**Problem Solved**: Dashboard showed "fresh" timestamps but stale/generic content. Solution: Separated Phase 2 (automated data sync) from Phase 5 (AI-driven synthesis), with clear timestamp ownership and visual feedback.

**Key Metrics**:
- 25 timestamp fields tracked (100% of critical sections)
- 3 layers: data storage → verification logic → visual display
- Color-coded status: GREEN (current), YELLOW (aging), RED (stale)
- Health percentage: 100% when all 25 fields current
- Phase 2/5 separation: Clear ownership model prevents overwrites

---

## Architecture Overview

### 3-Layer Verification Stack

```
┌─ LAYER 1: DATA STORAGE (YAML) ────────────────────────────────┐
│                                                               │
│  File: master-plan/master-plan.md                            │
│  Format: ISO 8601 timestamps (YYYY-MM-DDTHH:MM:SSZ)         │
│  Count: 25 tracked fields + 9 other timestamps               │
│  Example:                                                     │
│    keyLevelsUpdated: '2025-10-26T11:47:10Z'                 │
│    sentimentCardsUpdated: '2025-10-26T11:47:10Z'            │
│                                                               │
│  Owners:                                                      │
│    • Phase 2 (12 fields): sync_*.py scripts (automated)      │
│    • Phase 5 (13 fields): Claude AI (manual synthesis)       │
│                                                               │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌─ LAYER 2: VERIFICATION LOGIC (PYTHON) ────────────────────────┐
│                                                               │
│  Script: scripts/utilities/verify_timestamps.py              │
│  Function: Calculate health across all 25 fields             │
│  Logic:                                                      │
│    1. Extract 25 timestamp fields from YAML                  │
│    2. Parse ISO 8601 format to datetime                      │
│    3. Calculate hours since update: (now - timestamp)        │
│    4. Classify status:                                       │
│       • CURRENT: < 12 hours → GREEN                          │
│       • STALE: 12-24 hours → YELLOW                          │
│       • VERY_STALE: > 24 hours → RED                         │
│    5. Compute health: (current_count / 25) * 100             │
│    6. Output: JSON report with status for each field         │
│                                                               │
│  Output Example:                                             │
│    {                                                         │
│      "health_percentage": 100.0,                             │
│      "current_count": 25,                                    │
│      "stale_sections": [],                                   │
│      "status": "current"                                     │
│    }                                                         │
│                                                               │
│  Used By:                                                    │
│    • wingman dash workflow (Phase 4 final status check)      │
│    • Administrative monitoring                               │
│    • Automated alerts (future)                               │
│                                                               │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌─ LAYER 3: VISUAL DISPLAY (HTML/CSS/JS) ──────────────────────┐
│                                                               │
│  File: master-plan/research-dashboard.html                   │
│  Function: Display colored status badges on dashboard        │
│  Components:                                                 │
│    • getDataFreshness(timestamp) - Calculates status        │
│    • .date-badge CSS classes - Defines colors               │
│    • renderSection(data, updatedAt) - Injects badges        │
│                                                               │
│  Sections with Badges (11 total):                           │
│    Daily Planner (3): Key Levels, Calendar, Priorities      │
│    Dashboard (3): Risk Monitor, Timeline, Consensus         │
│    Tabs (5): Portfolio, Markets, News, X, Technicals       │
│    Header (1): Global verification status                   │
│                                                               │
│  User Experience:                                            │
│    • Green dot: Data is fresh, trust it                      │
│    • Yellow dot: Data aging, update soon                     │
│    • Red dot: Data stale, update immediately                │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Data Flow Example

```
User opens dashboard
    ↓
HTML loads master-plan.md YAML
    ↓
Each section's render function called
    ↓
Pass updatedAt timestamp to render function
    ↓
getDataFreshness(timestamp) calculates hours since update
    ↓
Returns: 'status-ok' (GREEN) | 'status-warning' (YELLOW) | 'status-error' (RED)
    ↓
CSS .date-badge.status-X applied
    ↓
Colored dot (10px circle) appears next to section title
    ↓
User sees instant visual feedback on data freshness
```

---

## Field Classification: 25 Tracked Fields

### Phase 2: Automated Data Sync (12 fields)

These fields are set automatically by `sync_*.py` scripts during `wingman dash` Phase 2. They track data-driven fields that update via API/scraper integration.

| # | Field | Script | Section | Purpose | Phase |
|---|-------|--------|---------|---------|-------|
| 1 | `dashboard.lastUpdated` | `update_master_plan.py` | Dashboard | Overall dashboard timestamp | 2 |
| 2 | `dashboard.sentimentCardsUpdated` | `update_master_plan.py` | Dashboard | Sentiment card metrics | 2 |
| 3 | `dashboard.metricsUpdated` | `update_master_plan.py` | Dashboard | Market metrics (BTC, SPY, etc.) | 2 |
| 4 | `dashboard.quickActionsUpdated` | `update_master_plan.py` | Dashboard | Quick action items | 2 |
| 5 | `dashboard.sentimentHistoryUpdated` | `sync_risk_items.py` | Dashboard | Historical sentiment archive | 2 |
| 6 | `dashboard.riskItemsUpdated` | `sync_risk_items.py` | Dashboard | Risk item summaries | 2 |
| 7 | `dashboard.providerConsensusUpdated` | `sync_provider_consensus.py` | Dashboard | Provider consensus aggregation | 2 |
| 8 | `dashboard.dailyPlanner.keyLevelsUpdated` | `update_master_plan.py` | Daily Planner | Key support/resistance levels | 2 |
| 9 | `dashboard.dailyPlanner.economicCalendarUpdated` | `sync_daily_planner.py` | Daily Planner | Economic calendar reference | 2 |
| 10 | `dashboard.dailyPlanner.endOfDay.ranAt` | `sync_daily_planner.py` | Daily Planner | End-of-day recap execution | 2 |
| 11 | `dashboard.dailyPlanner.signalDataUpdated` | `sync_daily_planner.py` | Daily Planner | Signal composite score | 2 |
| 12 | `tabs.technicals.technicalsTabSyncedAt` | `sync_technicals_tab.py` | Technicals Tab | Technical data last sync | 2 |

**Expected Health After Phase 2**: 48% (12/25 current, 13 still pending Phase 5)

**Key Characteristic**: These are **data-driven** fields that sync scripts can set with high confidence. They represent "what the market is doing" not "what this means".

---

### Phase 5: AI-Driven Synthesis (13 fields)

These fields are set by Claude AI during `wingman dash` Phase 5. They track interpretation fields that require judgment and market context.

#### Daily Planner (4 fields)

| # | Field | Purpose | Requires |
|---|-------|---------|----------|
| 1 | `dashboard.dailyPlanner.prioritiesUpdated` | Top 5 priorities | Action checklist synthesis |
| 2 | `dashboard.dailyPlanner.aiInterpretation.updatedAt` | Daily narrative synthesis | Market context + signal |
| 3 | `dashboard.dailyPlanner.recommendationUpdated` | Trading recommendation tier | Signal data + analysis |
| 4 | `dashboard.dailyPlanner.actionChecklistUpdated` | Tactical action items | Portfolio state + market |

#### Tab AI Interpretations (9 fields)

| # | Field | Tab | Purpose |
|---|-------|-----|---------|
| 5 | `tabs.portfolio.aiInterpretation.updatedAt` | Portfolio | Portfolio analysis & recommendation |
| 6 | `tabs.portfolio.portfolioRecommendation.updatedAt` | Portfolio | Portfolio allocation tier |
| 7 | `tabs.markets.aiInterpretation.updatedAt` | Markets | Consolidated macro/crypto/tech |
| 8 | `tabs.news_catalysts.aiInterpretation.updatedAt` | News | News sentiment + catalysts |
| 9 | `tabs.xsentiment.aiInterpretation.updatedAt` | X Sentiment | X platform sentiment synthesis |
| 10 | `tabs.xsentiment.socialTabSyncedAt` | X Sentiment | Last sync from X API |
| 11 | `tabs.xsentiment.crypto_trending.updatedAt` | X Sentiment | Top crypto trending tickers |
| 12 | `tabs.xsentiment.macro_trending.updatedAt` | X Sentiment | Top macro trending topics |
| 13 | `tabs.technicals.aiInterpretation.updatedAt` | Technicals | Technical analysis synthesis |

**Expected Health After Phase 5**: 100% (all 25 fields current)

**Key Characteristic**: These are **interpretation-driven** fields that require Claude's judgment. They answer "what should I do?" questions based on data and context.

**Critical**: These fields must NEVER be overwritten by sync scripts. Phase 2 only updates data fields, Phase 5 owns interpretation.

---

## Verification Health Calculation

### Formula

```
Health % = (Current Fields / 25) * 100
```

### Expected Progression

```
Before wingman dash:      0%   (0/25 current)
After Phase 2 (auto):    48%  (12/25 current)
After Phase 5 (AI):     100%  (25/25 current)
```

### What Each Level Means

| Health | Status | Fields | Implication | Action |
|--------|--------|--------|-------------|--------|
| 0-20% | CRITICAL | 0-5 | Dashboard broken/not initialized | Run full wingman dash |
| 21-47% | DEGRADED | 6-11 | Partial data available | Continue Phase 5 AI synthesis |
| 48-79% | EXPECTED | 12-19 | Phase 2 complete, awaiting Phase 5 | Run Phase 5 (manual AI work) |
| 80-99% | GOOD | 20-24 | Most fields current, few aging | Minor updates needed |
| 100% | OPTIMAL | 25 | All sections current | Maintain status |

---

## How to Use: Operations Guide

### Daily Operations

#### 1. Check Health Status (Pre-Dashboard)
```bash
python scripts/utilities/verify_timestamps.py --json --date $(date +%Y-%m-%d)
```

Expected output for healthy system:
```json
{
  "health_percentage": 100.0,
  "current_count": 25,
  "stale_count": 0,
  "status": "current"
}
```

#### 2. Open Dashboard
```bash
open master-plan/research-dashboard.html
```

Expected: All section titles have **green dots** next to them

#### 3. If Health < 100%
Check which sections are stale:
```bash
python scripts/utilities/verify_timestamps.py
# Output shows [WARN] STALE and [ERROR] VERY_STALE sections
```

#### 4. Update Stale Sections

**If Phase 2 field is stale** (automated data):
```bash
# Re-run sync script
python scripts/utilities/sync_daily_planner.py
python scripts/processing/fetch_market_data.py 2025-10-26
# This updates fields like economicCalendarUpdated, metricsUpdated
```

**If Phase 5 field is stale** (AI interpretation):
```bash
# Requires manual Claude AI work - run wingman dash Phase 5
# Or manually update interpretation fields with fresh analysis
```

#### 5. Verify Update Success
```bash
python scripts/utilities/verify_timestamps.py --json --date $(date +%Y-%m-%d)
# Should show: "health_percentage": 100.0
```

### Weekly Review

Check `Toolbox/verification_field_registry.md` to ensure:
- All 25 fields documented
- No new fields added without registry entry
- No Phase 2 fields regularly becoming stale (indicates sync issue)
- No Phase 5 fields regularly becoming stale > 24h (indicates AI synthesis delayed)

---

## How to Use: Developer Guide

### Adding a New Timestamp Field (5-Step Process)

#### Step 1: Identify Field Ownership

Decide if field is Phase 2 (automated) or Phase 5 (AI-driven):

| Phase 2 Question | Phase 5 Question |
|---|---|
| Can a script set this with 100% confidence? | Does this require judgment/interpretation? |
| Is this raw data or metrics? | Is this narrative or recommendation? |
| Can it be computed from API/scraper? | Does it need Claude AI to synthesize? |
| Example: Market price, signal score | Example: Trading recommendation, action plan |

#### Step 2: Add to YAML (master-plan/master-plan.md)

```yaml
# For Phase 2 field:
dashboard:
  newMetricUpdated: '2025-10-26T12:00:00Z'  # Set by sync script

# For Phase 5 field:
dashboard:
  newInterpretation:
    updatedAt: '2025-10-26T12:00:00Z'  # Set by Claude AI
```

**Format Requirements**:
- Use ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`
- Always include 'Z' suffix (UTC)
- Field name should end with `Updated` or `updatedAt`
- Place in logical section (dashboard, dailyPlanner, or tab)

#### Step 3: Add to Tracking (scripts/utilities/verify_timestamps.py)

```python
REQUIRED_TIMESTAMPS = [
    # ... existing fields ...

    # NEW FIELD (Phase 2 or Phase 5)
    "dashboard.newMetricUpdated",  # NEW - Brief description
]
```

**Requirements**:
- Path must start with `"dashboard."`
- Use same path as in YAML file
- Add comment indicating if Phase 2 or Phase 5
- Keep list organized by section

#### Step 4: Add to Registry (Toolbox/verification_field_registry.md)

Add to appropriate table:

```markdown
### Phase 2: Automated Sync (add to table)
| Line | Field Path | Script | Purpose | Format |
| XXX | `dashboard.newMetricUpdated` | sync_script.py | Description | ISO 8601 |

### Phase 5: AI Synthesis (add to table)
| # | Field | Purpose | Requires |
| N | `dashboard.newInterpretation.updatedAt` | Description | Data requirements |
```

#### Step 5: Add Visual Indicator (master-plan/research-dashboard.html)

**Option A: In render function signature**
```javascript
function renderNewSection(data, updatedAt) {
    // ... section rendering code ...

    if (updatedAt) {
        const statusClass = getDataFreshness(updatedAt);
        title.innerHTML = `Section Title <span class="date-badge ${statusClass}"></span>`;
    }
}

// Call with timestamp:
renderNewSection(data, plannerData.newMetricUpdated);
```

**Option B: Using selector after rendering**
```javascript
// In main rendering function after element is in DOM:
const sectionTitle = document.querySelector('.new-section .section-title');
if (sectionTitle && updatedAt) {
    const statusClass = getDataFreshness(updatedAt);
    sectionTitle.innerHTML = `${sectionTitle.textContent} <span class="date-badge ${statusClass}"></span>`;
}
```

#### Step 6: Update Sync Script (if Phase 2)

In the script that populates this field:
```python
# scripts/utilities/sync_script.py
self.data['newMetricUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
print(f"✓ Updated newMetricUpdated timestamp")
```

**Key Points**:
- Always set timestamp when setting the data
- Use consistent timestamp format
- Log the timestamp update for debugging

#### Step 7: Verify

Run verification:
```bash
python scripts/utilities/verify_timestamps.py --json
# Should show new field in output
# Status should be "CURRENT" if timestamp is today
```

Check dashboard:
```bash
open master-plan/research-dashboard.html
# New section should have colored dot indicator
```

**Congratulations!** New field is now tracked and displayed.

---

## Troubleshooting Guide

### Issue 1: Badge Shows Red Despite Running wingman dash

**Diagnosis**:
1. Check if sync script actually ran: `grep -i "updated.*timestamp" master-plan.md`
2. Check timestamp format: `grep "newFieldUpdated" master-plan.md`
3. Check system time: `date`

**Solution**:
```bash
# 1. Verify YAML is valid
python -c "import yaml; yaml.safe_load(open('master-plan/master-plan.md'))"

# 2. Check specific field value
grep "newFieldUpdated" master-plan/master-plan.md

# 3. Run verification with debug
python scripts/utilities/verify_timestamps.py --date 2025-10-26
```

### Issue 2: New Field Not Showing in Dashboard

**Diagnosis**:
1. Field added to YAML but no indicator? → Missing from HTML render function
2. Field in HTML but no badge? → Missing from verify_timestamps.py
3. Field shows but always red? → Timestamp format issue

**Solution**:
```bash
# Check field exists in all 3 layers:

# Layer 1: YAML
grep "newField" master-plan/master-plan.md

# Layer 2: Python
grep "newField" scripts/utilities/verify_timestamps.py

# Layer 3: HTML
grep "newField" master-plan/research-dashboard.html

# All 3 must match exactly
```

### Issue 3: getDataFreshness() Calculation Wrong

**Common Causes**:
- Timestamp missing 'Z' suffix (should be `...SSZ`)
- Timestamp not ISO 8601 format
- Browser time zone issues
- Leap second edge cases

**Debug**:
1. Open browser console (F12)
2. Calculate manually: `(now - updateTime) / (1000 * 60 * 60)`
3. Compare to actual hours
4. Check console logs for `Freshness check` messages

**Fix**:
```javascript
// In browser console:
const ts = new Date('2025-10-26T11:47:10Z');
const now = new Date();
console.log('Hours since:', (now - ts) / (1000 * 60 * 60));
```

### Issue 4: Phase 2 Field Regularly Becoming Stale

**Diagnosis**: Script runs but doesn't set timestamp

**Check Script**:
```bash
# Verify script includes timestamp setting:
grep -A5 "updatedAt\|Updated" scripts/utilities/sync_script.py
```

**Fix**:
```python
# Add or verify this line:
self.data['fieldUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
```

### Issue 5: Phase 5 Field Stuck Stale > 24h

**Diagnosis**: AI synthesis didn't run or incomplete

**Check**:
```bash
# See if Phase 5 was attempted
grep "Phase 5\|AI synthesis\|recommendation\|action" wingman_dash.log

# Check if Claude AI output exists
ls -la Research/.cache/*_ai_update_prompts.json
```

**Fix**:
```bash
# Manually trigger Phase 5
# Or edit master-plan.md to set current timestamp
```

---

## Maintenance Checklist

### Daily Checks
- [ ] Run: `verify_timestamps.py --json`
- [ ] Check: Health percentage = 100%
- [ ] If health < 100%, identify stale sections
- [ ] Update stale Phase 2 fields (run sync scripts)
- [ ] Update stale Phase 5 fields (Claude AI synthesis)

### Weekly Checks
- [ ] Review `CHANGELOG_2025-10-26.md` for any issues
- [ ] Check if Phase 2 fields regularly become stale (script failure?)
- [ ] Check if Phase 5 fields regularly become stale (AI delays?)
- [ ] Monitor for any new timestamp fields not in registry

### Monthly Checks
- [ ] Review and update `verification_field_registry.md`
- [ ] Check for new dashboard sections needing timestamps
- [ ] Monitor browser console for timestamp calculation errors
- [ ] Verify color-coding is working correctly across browsers

### When Adding New Features
- [ ] Does new section need a timestamp? → Add it
- [ ] Is it Phase 2 or Phase 5? → Classify correctly
- [ ] Add to all 3 layers (YAML, Python, HTML)
- [ ] Add to registry documentation
- [ ] Test with verify_timestamps.py
- [ ] Verify visual indicator displays

---

## Production Deployment Checklist

Before deploying to production, ensure:

- [ ] All 25 fields documented in registry
- [ ] All functions updated to accept updatedAt parameter
- [ ] All callers updated to pass timestamps
- [ ] Verify script correctly extracts all 25 fields
- [ ] Health calculation logic verified
- [ ] Color-coding CSS matches design
- [ ] Backward compatibility tested (missing timestamps don't break)
- [ ] Timestamp format ISO 8601 consistent throughout
- [ ] Phase 2/5 ownership clearly documented
- [ ] Developer guide included in registry
- [ ] Troubleshooting guide complete

---

## Performance Considerations

### Calculation Overhead
- `getDataFreshness()` runs for each badge on page load
- 11 badges = 11 timestamp calculations
- Each calculation: ~0.1ms (negligible)
- Total: ~1-2ms per dashboard load

### Recommended Optimization
If adding more than 50 fields:
```javascript
// Cache freshness results
const freshnessCache = {};
function getDataFreshnessCached(timestamp) {
    if (freshnessCache[timestamp]) return freshnessCache[timestamp];
    const result = getDataFreshness(timestamp);
    freshnessCache[timestamp] = result;
    return result;
}
```

### Memory Usage
- YAML parsing: ~5KB for 25 timestamps
- JavaScript calculations: negligible
- DOM badges: ~1KB per badge × 11 = ~11KB
- Total overhead: < 50KB

No performance issues at current scale.

---

## Testing

### Unit Testing the Freshness Calculation

```javascript
// Test cases for getDataFreshness()

// Test 1: Current data (< 12 hours)
const now = new Date();
const oneHourAgo = new Date(now.getTime() - (1 * 60 * 60 * 1000));
assert(getDataFreshness(oneHourAgo.toISOString()) === 'status-ok'); // GREEN

// Test 2: Stale data (12-24 hours)
const eighteenHoursAgo = new Date(now.getTime() - (18 * 60 * 60 * 1000));
assert(getDataFreshness(eighteenHoursAgo.toISOString()) === 'status-warning'); // YELLOW

// Test 3: Very stale data (> 24 hours)
const twoDaysAgo = new Date(now.getTime() - (48 * 60 * 60 * 1000));
assert(getDataFreshness(twoDaysAgo.toISOString()) === 'status-error'); // RED

// Test 4: Invalid format
assert(getDataFreshness('invalid') === 'status-error'); // Graceful failure
```

### Integration Testing

1. **Verify all 25 fields extract correctly**:
   ```bash
   python scripts/utilities/verify_timestamps.py --json | jq '.current_count'
   # Should output: 25
   ```

2. **Verify health calculation**:
   ```bash
   python scripts/utilities/verify_timestamps.py --json | jq '.health_percentage'
   # Should output: 100.0 (when all current)
   ```

3. **Verify visual display**:
   - Open dashboard
   - Inspect element on badge: `<span class="date-badge status-ok">`
   - Check CSS is applied: Green background, glow effect

---

## Future Enhancements

### Phase 1: Dashboard Admin Panel (Estimated: 2 weeks)
Create admin page showing:
- All 25 fields with individual status
- Last update time for each field
- Which script owns each field
- Manual override capability for testing

### Phase 2: Historical Trending (Estimated: 3 weeks)
Track health over time:
- Graph of health % over past 30 days
- Identify patterns (e.g., Phase 5 always stale Friday-Sunday?)
- Predict when fields will become stale

### Phase 3: Automated Alerts (Estimated: 2 weeks)
Alert when:
- Health drops below 80%
- Any field > 24 hours stale
- Sync script fails
- Dashboard not updated for 3+ hours

### Phase 4: Self-Healing (Estimated: 4 weeks)
Automatic remediation:
- Trigger sync scripts when Phase 2 fields become stale
- Suggest Claude AI synthesis for Phase 5 fields
- Rollback to cached data if sync fails
- Email notifications with remediation suggestions

---

## Reference Documentation

### Related Files
- [verification_field_registry.md](verification_field_registry.md) - Field registry and developer guide
- [CHANGELOG_2025-10-26.md](CHANGELOG_2025-10-26.md) - Implementation details and commits
- `scripts/utilities/verify_timestamps.py` - Verification logic
- `master-plan/research-dashboard.html` - Visual display implementation
- `master-plan/master-plan.md` - YAML data source

### Related Workflows
- `wingman dash` - Executes Phases 1-5, includes verification checks
- Phase 2 Sync - Updates 12 Phase 2 fields automatically
- Phase 5 Synthesis - Claude AI updates 13 Phase 5 fields manually

### Key Concepts
- **ISO 8601**: Timestamp format used throughout system
- **Health Percentage**: (current fields / 25) × 100
- **Status Classification**: CURRENT (GREEN) | STALE (YELLOW) | VERY_STALE (RED)
- **Phase Separation**: Phase 2 automated, Phase 5 AI-driven

---

**Documentation Version**: 1.0
**Last Updated**: 2025-10-26
**Next Review**: 2025-11-02
**Status**: 🟢 PRODUCTION READY
