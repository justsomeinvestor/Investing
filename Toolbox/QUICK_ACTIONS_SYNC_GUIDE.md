# Quick Actions Sync Guide

**Created**: October 23, 2025
**Script**: `scripts/utilities/sync_quick_actions.py`
**Status**: Production Ready - Integrated with wingman_dash workflow

---

## Overview

The Quick Actions section displays 4 actionable insights on the dashboard based on current market conditions:

1. **RISK** - Position sizing guidance based on signal composite score
2. **HEDGE** - Contrarian opportunities based on fear & greed readings
3. **WATCH** - Upcoming economic catalysts to monitor
4. **PLAN** - Portfolio allocation strategy based on signal tier

The sync_quick_actions.py script automatically generates these actions using:
- Signal composite data (from `Research/.cache/signals_{date}.json`)
- Market data (from `Research/.cache/{date}_market_data.json`)
- Rule-based logic tied to signal thresholds

---

## Quick Actions Structure

Each action has 5 fields:

```yaml
quickActions:
  - type: RISK | HEDGE | WATCH | PLAN
    title: "Descriptive title"
    value: "Key metric or indicator"
    description: "Detailed guidance (2-3 sentences)"
    urgency: CRITICAL | HIGH | MEDIUM | LOW
```

### Example (Signal 58/100 - MODERATE)

```yaml
quickActionsUpdated: '2025-10-23T18:19:43Z'
quickActions:
  - type: RISK
    title: Selective Risk - Moderate Environment
    value: 'Signal Score: 58.0/100 (MODERATE)'
    description: Signal at MODERATE (58.0/100). Trend=18.0, breadth=15.0 suggest selective opportunities.
      Maintain 30-40% exposure in quality names with strong technicals. Avoid speculation until signal >60.
    urgency: HIGH

  - type: HEDGE
    title: Fear Reading - Contrarian Watch
    value: Crypto Fear & Greed 27 • BTC $109,799
    description: Fear reading (F&G 27) approaching contrarian zone. BTC $109,799 needs to hold support.
      Watch for extreme fear <25 or signal improvement. Maintain hedges through uncertainty.
    urgency: HIGH

  - type: WATCH
    title: Upcoming Economic Catalysts
    value: Monitor key macro events
    description: 'Watch for: (1) Fed meetings, (2) CPI/PPI data, (3) Jobs reports, (4) Major earnings,
      (5) Geopolitical events. Check economic calendar daily for precise timing.'
    urgency: MEDIUM

  - type: PLAN
    title: Balanced Risk Management
    value: 40-50% exposure
    description: 'Signal 58.0/100 (MODERATE) allows selective deployment. Position: 30-35% quality equities,
      15-20% crypto infrastructure, 10% hedges, 35-40% cash. Quality bias non-negotiable.'
    urgency: HIGH
```

---

## Action Generation Logic

### 1. RISK Action (Signal-Based)

**Signal < 30 (AVOID)**:
- Urgency: CRITICAL
- Title: "Extreme Caution - High Risk Environment"
- Guidance: 10-15% exposure max, 75-85% cash

**Signal 30-40 (WEAK)**:
- Urgency: CRITICAL
- Title: "High Caution - Weak Environment"
- Guidance: 20-25% exposure, 40-50% cash, 15-20% hedges

**Signal 40-60 (MODERATE)**:
- Urgency: HIGH
- Title: "Selective Risk - Moderate Environment"
- Guidance: 30-40% exposure in quality names, avoid speculation

**Signal > 60 (STRONG)**:
- Urgency: MEDIUM
- Title: "Risk Deployment Window Open"
- Guidance: 50-60% exposure, maintain discipline

### 2. HEDGE Action (Fear & Greed Based)

**F&G < 25 (Extreme Fear)**:
- Urgency: HIGH
- Title: "Extreme Fear - Contrarian Setup Forming"
- Guidance: Watch for capitulation, reduce hedges if support holds

**F&G 25-40 (Fear)**:
- Urgency: HIGH
- Title: "Fear Reading - Contrarian Watch"
- Guidance: Maintain hedges, watch for extreme fear or signal improvement

**F&G 40-75 (Neutral)**:
- Urgency: MEDIUM
- Title: "Neutral Sentiment - Maintain Hedges"
- Guidance: No edge, maintain 10-15% hedge allocation

**F&G > 75 (Extreme Greed)**:
- Urgency: CRITICAL
- Title: "Extreme Greed - Add Hedges"
- Guidance: Top forming, add hedges (puts, inverse ETFs), reduce exposure 20-30%

### 3. WATCH Action (Catalysts)

**Always Present**:
- Urgency: MEDIUM
- Title: "Upcoming Economic Catalysts"
- Guidance: Fed meetings, CPI/PPI, jobs reports, earnings, geopolitical events
- Note: This is generic guidance - ideally would pull from economic calendar

### 4. PLAN Action (Position Sizing)

**Signal < 30 (AVOID)**:
- Urgency: CRITICAL
- Value: "10-15% exposure max"
- Position: 10-15% defensive, 5-10% crypto IF must, 75-85% cash

**Signal 30-40 (WEAK)**:
- Urgency: CRITICAL
- Value: "20-30% exposure"
- Position: 20-25% quality equities, 10-15% crypto, 15-20% hedges, 40-50% cash

**Signal 40-60 (MODERATE)**:
- Urgency: HIGH
- Value: "40-50% exposure"
- Position: 30-35% equities, 15-20% crypto, 10% hedges, 35-40% cash

**Signal > 60 (STRONG)**:
- Urgency: MEDIUM
- Value: "60-70% exposure"
- Position: 50-55% equities, 20-25% crypto, 5-10% hedges, 20-25% cash

---

## Data Sources

### Required Files

1. **signals_{date}.json** - Signal composite data
   - Path: `Research/.cache/signals_{date}.json`
   - Required fields: `composite`, `tier`, `breakdown`
   - Example: `{"composite": 58.0, "tier": "MODERATE", "breakdown": {"trend": 18, "breadth": 15}}`

2. **{date}_market_data.json** - Market data
   - Path: `Research/.cache/{date}_market_data.json`
   - Required fields: `fear_greed.crypto`, `crypto.bitcoin.usd`
   - Example: `{"fear_greed": {"crypto": 27}, "crypto": {"bitcoin": {"usd": 109799}}}`

### Fallback Behavior

If data files are missing, script uses conservative defaults:
- Signal: 50.0 (MODERATE)
- Fear & Greed: 50 (Neutral)
- BTC Price: $100,000

---

## Usage

### Standalone Execution

```bash
# From repo root
python scripts/utilities/sync_quick_actions.py 2025-10-23
```

**Output:**
```
======================================================================
⚡ QUICK ACTIONS SYNCHRONIZATION
======================================================================
Date: 2025-10-23

[1/5] Loading signals data...
   ✓ Loaded signals: 58.0/100 (MODERATE)
[2/5] Loading market data...
   ✓ Loaded market data: F&G Crypto=27, BTC=$109,799
[3/5] Loading master plan...
   ✓ Loaded master plan
[4/5] Generating Quick Actions...
   ✓ Generated 4 quick actions
      - RISK: HIGH
      - HEDGE: HIGH
      - WATCH: MEDIUM
      - PLAN: HIGH
[5/5] Saving master plan...
   ✓ Saved master plan with updated quickActions

======================================================================
✅ QUICK ACTIONS SYNC COMPLETE
======================================================================
```

### Integrated with Wingman Dash

The script is automatically called during Phase 2 of wingman_dash.py:

```bash
python scripts/automation/wingman_dash.py 2025-10-23
```

**Wingman Dash Phase 2 includes:**
1. social_tab_sync
2. technicals_tab_sync
3. news_tab_sync
4. daily_planner_sync
5. markets_intelligence_update
6. **quick_actions_sync** ← NEW

---

## Integration Points

### wingman_dash.py (Line 79)

```python
self.sync_scripts = [
    ("social_tab_sync", self.repo_root / "scripts" / "utilities" / "sync_social_tab.py"),
    ("technicals_tab_sync", self.repo_root / "scripts" / "utilities" / "sync_technicals_tab.py"),
    ("news_tab_sync", self.repo_root / "scripts" / "utilities" / "sync_news_tab.py"),
    ("daily_planner_sync", self.repo_root / "scripts" / "utilities" / "sync_daily_planner.py"),
    ("markets_intelligence_update", self.repo_root / "scripts" / "automation" / "update_markets_intelligence.py"),
    ("quick_actions_sync", self.repo_root / "scripts" / "utilities" / "sync_quick_actions.py"),  # Added Oct 23
]
```

### master-plan.md Structure

```yaml
dashboard:
  quickActionsUpdated: '2025-10-23T18:19:43Z'
  quickActions:
    - type: RISK
      title: ...
      value: ...
      description: ...
      urgency: ...
    - type: HEDGE
      ...
    - type: WATCH
      ...
    - type: PLAN
      ...
```

---

## Benefits

✅ **Automated Updates**: No manual editing required - runs automatically with wingman_dash
✅ **Rule-Based Logic**: Consistent action recommendations based on signal thresholds
✅ **Timestamp Tracking**: quickActionsUpdated shows when last synced (eliminates red dots)
✅ **Data-Driven**: Uses latest signal composite and market data
✅ **Modular Design**: Easy to extend with additional action types or logic
✅ **Fallback Safety**: Uses conservative defaults if data files missing

---

## Customization

### Adding New Action Types

1. Add new action type to `quick_actions` list in `sync_quick_actions()` method
2. Create generation method (e.g., `generate_execution_action()`)
3. Update this documentation with new action logic

### Modifying Thresholds

Edit the threshold values in generation methods:

```python
def generate_risk_action(self, composite: float, ...):
    if composite < 30:  # Change threshold here
        urgency = "CRITICAL"
        # ...
```

### Integrating Economic Calendar

Replace generic WATCH action with calendar-driven events:

```python
def generate_watch_action(self) -> Dict[str, Any]:
    # Load economic calendar from Research/.cache/economic_calendar.json
    calendar = self.load_economic_calendar()
    next_event = calendar.get_next_major_event()

    return {
        'type': 'WATCH',
        'title': f'{next_event["name"]} - {next_event["date"]}',
        'value': next_event["impact"],
        'description': next_event["details"],
        'urgency': 'HIGH' if next_event["impact"] == "CRITICAL" else 'MEDIUM'
    }
```

---

## Troubleshooting

### Script Fails to Load Signals

**Error**: `⚠ Signals file not found`

**Solution**: Run wingman recon/prep first to generate signal data:
```bash
python scripts/automation/wingman_recon.py 2025-10-23
python scripts/automation/wingman_prep.py 2025-10-23
```

### Script Fails to Load Market Data

**Error**: `⚠ Market data file not found`

**Solution**: Ensure market data is generated during recon phase. Script will use fallback values if missing.

### YAML Write Errors

**Error**: `yaml.YAMLError: Invalid YAML`

**Solution**: MasterPlanYAML handler validates before writing. Check that data structure matches expected format. Review yaml_handler.py validation logic.

### Quick Actions Not Updating in Dashboard

**Issue**: Timestamp changes but content doesn't match new data

**Solution**: Check that master-plan.md file structure matches expected path `dashboard.quickActions`. Verify YAML handler is accessing correct nested keys.

---

## Future Enhancements

1. **Economic Calendar Integration**: Pull next 3-5 days of catalysts for WATCH action
2. **Provider Consensus**: Integrate macro provider recommendations into actions
3. **X Sentiment Signals**: Use social sentiment extremes for HEDGE contrarian signals
4. **Historical Performance**: Track action accuracy and adjust thresholds over time
5. **Multi-Asset Actions**: Expand beyond BTC to include ETH, SOL, SPY, QQQ levels

---

## Testing

### Unit Test Quick Actions Generation

```python
# Test RISK action generation
syncer = QuickActionsSyncer('2025-10-23')
syncer.signals_data = {'composite': 58.0, 'tier': 'MODERATE', 'breakdown': {'trend': 18, 'breadth': 15, 'volatility': 13}}
risk_action = syncer.generate_risk_action(58.0, 'MODERATE', 18, 15, 13)

assert risk_action['type'] == 'RISK'
assert risk_action['urgency'] == 'HIGH'
assert '30-40% exposure' in risk_action['description']
```

### Integration Test with Wingman Dash

```bash
# Run full wingman_dash workflow
python scripts/automation/wingman_dash.py 2025-10-23

# Verify quickActions section updated
grep -A 20 "quickActionsUpdated" master-plan/master-plan.md
```

---

## Version History

**v1.0.0** (October 23, 2025)
- Initial release
- 4 action types: RISK, HEDGE, WATCH, PLAN
- Rule-based generation from signal + market data
- Integrated with wingman_dash Phase 2

---

**Status**: Production Ready
**Maintenance**: Update thresholds as signal system evolves
**Contact**: See main project README for support
