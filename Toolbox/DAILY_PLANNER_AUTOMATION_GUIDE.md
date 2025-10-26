# Daily Planner Automation Guide

## Overview

**Date**: October 26, 2025
**Status**: ACTIVE - Integrated into wingman_dash.py Phase 5
**Purpose**: Automatically prompt Claude AI to update Trading Signal recommendation and actionChecklist during daily workflow

---

## Problem Solved

Previously, these fields were **static** and never updated:
- `dashboard.dailyPlanner.recommendation` - Tactical guidance text
- `dashboard.dailyPlanner.actionChecklist` - Priority-tagged action items

**Why?** They weren't included in wingman_dash.py's Phase 5 section_mappings, so you never received update prompts.

**Solution**: Extended section_mappings to include these fields, so Phase 5 generates prompts telling you to update them.

---

## How It Works

### When You Run: `python scripts/automation/wingman_dash.py 2025-10-25`

**Phase 5 Output** (new lines):
```
📌 dashboard.dailyPlanner.recommendation
   ➜ Research Sources:
      • Research/.cache/2025-10-25_Market_Sentiment_Overview.md
      • Research/.cache/signals_2025-10-25.json

   Daily Planner Recommendation will receive tactical guidance (tier + context + action)

📌 dashboard.dailyPlanner.actionChecklist
   ➜ Research Sources:
      • Research/.cache/2025-10-25_Market_Sentiment_Overview.md
      • Research/.cache/signals_2025-10-25.json

   Daily Planner Action Checklist will receive tactical actions (high/critical/monitor)
```

### Detailed Prompts Saved To:
`Research/.cache/2025-10-25_ai_update_prompts.json`

---

## Your Workflow (Claude AI)

After wingman_dash Phase 5 completes:

### Step 1: Read the Prompts

Find the two new prompts in `ai_update_prompts.json`:
```json
{
  "section": "dashboard.dailyPlanner.recommendation",
  "status": "tactical_guidance",
  "writing_guidelines": {
    "format": "[TIER] tier (score/100). [Market context]. [Positioning guidance].",
    "example": "MODERATE tier (63.22/100). Post-CPI consolidation continues..."
  }
},
{
  "section": "dashboard.dailyPlanner.actionChecklist",
  "status": "tactical_actions",
  "schema": {
    "format": "YAML list of {text, priority}",
    "high": "Important actions (25-50% portfolio impact)",
    "critical": "Must-do actions (>50% portfolio impact)",
    "monitor": "Watch-list items (no immediate action)"
  }
}
```

### Step 2: Read Research Sources

**For recommendation:**
1. `Research/.cache/{date}_Market_Sentiment_Overview.md` - Market context + themes
2. `Research/.cache/signals_{date}.json` - Signal tier + score

**For actionChecklist:**
1. Same files as above

### Step 3: Generate Content

**RECOMMENDATION:**
```yaml
recommendation: |
  MODERATE tier (63.22/100). Post-CPI consolidation continues.
  Selective risk deployment appropriate with quality names showing
  strong technicals. Market breadth improving but still fragile—
  maintain hedges for volatility spikes.
```

**ACTION CHECKLIST:**
```yaml
actionChecklist:
  - text: "Selective risk deployment to quality names with strong technicals."
    priority: high
  - text: "Maintain hedges through week ahead given lingering volatility risks."
    priority: critical
  - text: "Monitor key support levels: SPX 6679, BTC $111.9K."
    priority: monitor
```

### Step 4: Update master-plan.md

Edit `master-plan/master-plan.md` in the `dashboard.dailyPlanner` section:

**Find:**
```yaml
dashboard:
  dailyPlanner:
    recommendation: "[OLD TEXT]"
    actionChecklist:
      - text: "[OLD ITEM]"
        priority: high
```

**Replace with:**
```yaml
dashboard:
  dailyPlanner:
    recommendation: "[NEW TEXT - from research synthesis]"
    actionChecklist:
      - text: "[NEW ACTION 1]"
        priority: high
      - text: "[NEW ACTION 2]"
        priority: critical
      - text: "[NEW ACTION 3]"
        priority: monitor
```

### Step 5: Update Timestamp

Update the parent timestamp (signals to dashboard that work is done):

```yaml
dashboard:
  dailyPlanner:
    # ...content above...
    prioritiesUpdated: '2025-10-26T06:15:00Z'  # ← Use current ISO 8601 time
```

---

## Writing Guidelines

### Recommendation Format

**Template**: `[TIER] tier (XX.XX/100). [Context]. [Guidance].`

**Example**:
> MODERATE tier (63.22/100). Post-CPI consolidation continues. Selective risk deployment appropriate with quality names showing strong technicals. Market breadth improving but still fragile—maintain hedges for volatility spikes.

**Rules:**
- Line 1: Tier + score
- Line 2: Market context (1-2 sentences)
- Line 3: Positioning guidance (1-2 sentences)
- Max 400 characters
- Professional, concise tone
- Include specific context: breadth, volatility, catalysts

### Action Checklist Format

**Schema:**
```yaml
actionChecklist:
  - text: "[ACTION TEXT]"
    priority: "high|critical|monitor"
```

**Priority Levels:**
- **critical**: Must-do defensive/offensive actions (>50% portfolio impact)
  - Examples: Reduce exposure, increase hedges, add positions, execute hedge
- **high**: Important actions aligned with signal tier (25-50% portfolio impact)
  - Examples: Watch for breadth improvement, prepare position sizes, set alerts
- **monitor**: Watch-list items, key levels to observe (no immediate action)
  - Examples: Monitor support levels, track economic catalysts, watch A/D ratio

**Example Checklist:**
```yaml
actionChecklist:
  - text: "Selective risk deployment to quality names with strong technicals."
    priority: high
  - text: "Maintain hedges through week ahead given lingering volatility risks."
    priority: critical
  - text: "Monitor key support levels: SPX 6679, BTC $111.9K."
    priority: monitor
```

---

## Signal Tier Context

Use the signal tier to determine recommendation tone:

**EXTREME (85-100)**:
- Tone: Very bullish, aggressive
- Recommendation: "Aggressive deployment in high-conviction setups. Scale into strength."
- Actions: High deployment, consider full long exposure, monitor for exhaustion

**STRONG (70-84)**:
- Tone: Bullish, confident
- Recommendation: "Active deployment in high-conviction setups. Monitor for exhaustion signals."
- Actions: Deploy capital, scale on dips, maintain discipline

**MODERATE (55-69)**:
- Tone: Cautiously bullish, selective
- Recommendation: "Selective risk deployment appropriate with quality names."
- Actions: Pick positions carefully, watch breadth, maintain hedges

**WEAK (40-54)**:
- Tone: Defensive, cautious
- Recommendation: "Defensive positioning - reduce exposure."
- Actions: Reduce exposure, move to quality, watch for improvement signals

**AVOID (<40)**:
- Tone: Very defensive, bearish
- Recommendation: "Reduce exposure significantly. Avoid new positions."
- Actions: Minimize exposure, stay defensive, wait for confirmation

---

## Example Workflow (Complete)

**Signal Data:**
```json
{
  "composite": 63.22,
  "tier": "MODERATE",
  "breakdown": {
    "trend": 28.21,
    "breadth": 18.45,
    "volatility": 11.2,
    "technical": 4.88,
    "seasonality": 0.48
  }
}
```

**Market Context** (from Market_Sentiment_Overview.md):
- Post-CPI consolidation
- Breadth divergence (SPX ATH but 80% of stocks below ATH)
- Fed decision Oct 29 is key catalyst
- Institutional accumulation vs retail fear
- Quality earnings holding up
- Tariff inflation risk building

**Your Generated Content:**

```yaml
recommendation: |
  MODERATE tier (63.22/100). Post-CPI consolidation continues.
  Selective risk deployment appropriate with quality names showing
  strong technicals. Market breadth improving but still fragile—
  maintain hedges for volatility spikes.

actionChecklist:
  - text: "Selective risk deployment to quality names with strong technicals."
    priority: high
  - text: "Maintain hedges through week ahead given lingering volatility risks."
    priority: critical
  - text: "Monitor key support levels: SPX 6679, BTC $111.9K."
    priority: monitor

prioritiesUpdated: '2025-10-26T06:15:00Z'
```

---

## Files Modified

| File | Change | Lines |
|------|--------|-------|
| `scripts/automation/wingman_dash.py` | Added recommendation + actionChecklist to section_mappings | 353-362 |
| `scripts/automation/wingman_dash.py` | Added dedicated prompt generation for both fields | 451-508 |

---

## Integration with Existing Workflow

✅ **Phase 1-4**: Automated (unchanged)
✅ **Phase 5**: Now includes recommendation + actionChecklist prompts (NEW)

This follows the same pattern as existing Phase 5 sections:
- Markets Intelligence
- Portfolio Recommendation
- Daily Planner Key Levels
- Technical Interpretations

---

## Quick Reference

### Data Sources
```
Market_Sentiment_Overview.md → Contains themes, catalysts, risk factors
signals_2025-10-25.json     → Contains signal tier + score
```

### Field Locations in master-plan.md
```yaml
dashboard:
  dailyPlanner:
    recommendation: "..."          # ← Edit here
    actionChecklist: [...]         # ← Edit here
    prioritiesUpdated: "..."       # ← Update timestamp here
```

### Console Output to Expect
```
📌 dashboard.dailyPlanner.recommendation
   Daily Planner Recommendation will receive tactical guidance...

📌 dashboard.dailyPlanner.actionChecklist
   Daily Planner Action Checklist will receive tactical actions...
```

---

## Validation Checklist

After updating both fields, verify:

- [ ] Recommendation format: `[TIER] tier (XX.XX/100). [Context]. [Guidance].`
- [ ] Recommendation ≤400 characters
- [ ] Action Checklist has 2-4 items
- [ ] Each item has `text` and `priority` (high/critical/monitor)
- [ ] Priorities match signal tier context
- [ ] Timestamp updated to current ISO 8601 time
- [ ] No syntax errors in YAML (can use `yamllint master-plan.md`)
- [ ] Run `verify_timestamps.py` confirms section is current

---

## Success Criteria

✅ wingman_dash Phase 5 generates prompts for these fields
✅ You (Claude) receive clear instructions each day
✅ Recommendation + actionChecklist updated fresh from research
✅ Timestamp reflects today's work
✅ Dashboard displays updated content

---

**Status**: Production Ready
**Last Updated**: October 26, 2025
**Next Review**: Daily during wingman_dash Phase 5

