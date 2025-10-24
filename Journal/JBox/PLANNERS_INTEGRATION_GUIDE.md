# Planners Integration Guide
## Research Dashboard → Weekly/Daily Planning Hub

---

## 🎯 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│  master-plan/research-dashboard.html                    │
│  (Central Intelligence Hub)                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PLANNERS TAB (was "Daily Planner")                     │
│  ├─ WEEKLY PLANNER Section                             │
│  │  └─ Reads: Research/AI/[WEEK]_WEEKLY_METRICS.md    │
│  │  └─ Updated: Every Sunday before market close       │
│  │  └─ Contains: Signal forecast, trigger stack,       │
│  │              risk controls, economic calendar       │
│  │                                                     │
│  └─ DAILY PLANNER Section                              │
│     └─ Reads: Research/AI/[DATE]_DAILY_METRICS.md      │
│     └─ Updated: Each market day (9:00 AM ET)           │
│     └─ Contains: Today's priorities, key levels,       │
│                  today's setups from weekly stack      │
│                                                         │
└─────────────────────────────────────────────────────────┘
         ↓                          ↓
   [Weekly Data]              [Daily Data]
         ↓                          ↓
    Collected by:              Updated by:
    Sunday Planner              Daily Ops
    (Wingman prompt)            (Before market)
         ↓                          ↓
    Generated weekly             Generated daily
    metrics file                metrics file
```

---

## 📁 FILE STRUCTURE

### Weekly Metrics (Every Sunday)
```
Research/AI/2025-10-19_WEEKLY_METRICS.md
├─ Signal progression (Fri-Sat-Sun)
├─ Sentiment analysis
├─ Market structure (breadth, VIX, divergences)
├─ Portfolio health snapshot
├─ Provider consensus themes
├─ Economic calendar for week
├─ Risk assessment
├─ Weekly trigger stack (3 setups)
├─ Daily positioning guide (Mon-Fri)
└─ Next Sunday's prep notes
```

### Daily Metrics (Every Trading Day)
```
Research/AI/2025-10-20_DAILY_METRICS.md
├─ Market signal & context
├─ Inherited from weekly plan
├─ Today's 3 priorities (from weekly stack)
├─ Key market levels (filtered from weekly)
├─ Economic calendar (today only)
├─ Risk management for today
├─ Pre-market checklist
├─ Trade execution log
└─ EOD summary & tomorrow prep
```

---

## 🔄 DATA FLOW

### SUNDAY WORKFLOW
```
1. Wingman Prompt: "Load Sunday planner"
   ↓
2. Wingman runs through metrics checklist (PHASE 2 of SUNDAY_WEEKLY_PLANNER.md)
   ├─ Signal progression (Fri-Sat-Sun)
   ├─ Sentiment metrics
   ├─ Breadth/VIX/divergences
   ├─ Portfolio health
   ├─ Provider consensus
   └─ Economic calendar
   ↓
3. You provide: Filled checklist + trading setups
   ↓
4. Wingman generates: 2025-10-19_WEEKLY_METRICS.md
   ├─ Formatted metrics
   ├─ Weekly trigger stack
   ├─ Risk controls
   ├─ Daily positioning guide (Mon-Fri)
   └─ Saves to Research/AI/
   ↓
5. Dashboard READS file + displays in "Weekly Planner" section
   ↓
6. **READY:** Research dashboard now has week's context loaded
```

### DAILY WORKFLOW (Monday-Friday)
```
1. Market Open: Dashboard auto-loads daily metrics file
   ↓
2. Daily Metrics file (2025-10-20_DAILY_METRICS.md) contains:
   ├─ Today's 3 priorities (PULLED from weekly stack)
   ├─ Today's levels (FILTERED from weekly levels)
   ├─ Today's economic events
   ├─ Pre-market checklist
   └─ Link to weekly context above
   ↓
3. You trade: Follow today's plan, execute triggers
   ↓
4. Dashboard updates: Trade log auto-fills as you trade
   ↓
5. EOD: Fill summary section + review against weekly plan
   ↓
6. **READY:** Next day's daily metrics loaded (repeats)
```

---

## 📊 RESEARCH DASHBOARD INTEGRATION

### Tab Structure (UPDATED)

```
Tabs:
├─ Overview (unchanged)
├─ Provider Insights (unchanged)
├─ Signal Data (unchanged)
├─ Risk Monitor (unchanged)
├─ Planners ← NEW COMBINED TAB
│  ├─ Weekly Planner Section
│  │  ├─ Signal Forecast (Mon-Fri)
│  │  ├─ Economic Calendar (Week View)
│  │  ├─ Weekly Trigger Stack (3 setups)
│  │  ├─ Portfolio Positioning Guide
│  │  ├─ Risk Controls & Hedges
│  │  └─ Key Levels (Weekly)
│  │
│  └─ Daily Planner Section
│     ├─ Today's Context (from weekly)
│     ├─ Today's Priorities (3 trades)
│     ├─ Today's Levels (filtered)
│     ├─ Economic Calendar (Today)
│     ├─ Trade Execution Log
│     └─ Pre-Market Checklist
│
├─ Options Intelligence (unchanged)
├─ Calendar (unchanged)
└─ AI Interpretation (unchanged)
```

### Weekly Planner Display
```
┌─────────────────────────────────────────────────────┐
│ WEEKLY PLANNER                                      │
│ Week of Oct 13-17 | Updated: Sun Oct 19, 3:30 PM  │
├─────────────────────────────────────────────────────┤
│                                                     │
│ SIGNAL FORECAST                                    │
│ ┌─────────────────────────────────────────────────┐│
│ │ Friday: 36.21/100 (WEAK)                        ││
│ │ Saturday: 37.04/100 (WEAK)                      ││
│ │ Sunday: 43.50/100 (MODERATE)                    ││
│ │ Trend: RISING ↑                                 ││
│ │ Expected Mon-Fri: MODERATE tier (volatile)      ││
│ └─────────────────────────────────────────────────┘│
│                                                     │
│ WEEKLY TRIGGER STACK                               │
│ ┌──────────────────┬──────────────────┐           │
│ │ Trigger #1       │ Breadth Thrust   │           │
│ │ Probability: 40% │ Buy ES 6,710     │           │
│ │ R:R: 1:2.5       │ Target: 6,800    │           │
│ ├──────────────────┼──────────────────┤           │
│ │ Trigger #2       │ Bottom Bounce    │           │
│ │ Probability: 55% │ Long ES 6,700    │           │
│ │ R:R: 1:1.5       │ Target: 6,760    │           │
│ ├──────────────────┼──────────────────┤           │
│ │ Trigger #3       │ Fade Strength    │           │
│ │ Probability: 45% │ Short ES 6,720   │           │
│ │ R:R: 1:2.0       │ Target: 6,630    │           │
│ └──────────────────┴──────────────────┘           │
│                                                     │
│ RISK CONTROLS                                      │
│ • Max Portfolio Heat: 30%                          │
│ • Daily Loss Limit: $200                           │
│ • Hedge Allocation: 15-20%                         │
│ • Key Risk: Liquidation tail, breadth divergence   │
│                                                     │
│ ECONOMIC CALENDAR (WEEK)                           │
│ Mon: No events | Tue: Pending homes (10 AM)        │
│ Wed: NEW HOME SALES (10 AM) | Thu: Durable (8:30AM)│
│ Fri: PCE INFLATION (8:30 AM) ← CRITICAL            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Daily Planner Display
```
┌─────────────────────────────────────────────────────┐
│ DAILY PLANNER                                       │
│ Monday, October 20, 2025 | Updated: 9:00 AM ET    │
├─────────────────────────────────────────────────────┤
│                                                     │
│ TODAY'S CONTEXT (from Weekly Plan)                  │
│ Week Tier: MODERATE | Max Risk: 30% | Max Loss: $X │
│                                                     │
│ TODAY'S 3 PRIORITIES                                │
│ ┌─────────────────────────────────────────────────┐│
│ │ Priority #1: BREADTH THRUST (40% probability)   ││
│ │ Watch: ES 6,710 (20-DMA) - entry on breadth >25%││
│ │ Stop: 6,697 (8-DMA) | Target: 6,800 | R:R 1:2.5 ││
│ │ Status: WATCHING                                 ││
│ │                                                  ││
│ │ Priority #2: BOTTOM BOUNCE (55% probability)    ││
│ │ Watch: ES 6,700 support - entry on close >6,700 ││
│ │ Stop: 6,665 | Target: 6,760 | R:R 1:1.5         ││
│ │ Status: WATCHING                                 ││
│ │                                                  ││
│ │ Priority #3: FADE STRENGTH (45% probability)    ││
│ │ Watch: ES 6,720-6,750 resistance zone           ││
│ │ Short entry if divergence forms                  ││
│ │ Target: 6,630 | R:R 1:2.0                       ││
│ │ Status: WATCHING (mid-week play)                 ││
│ └─────────────────────────────────────────────────┘│
│                                                     │
│ TODAY'S KEY LEVELS                                  │
│ SPX: 6,650 (support) | 6,700 (key level) | 6,730 │
│ BTC: $100K (critical) | $106,850 (200-DMA)        │
│ QQQ: 597 (support) | 601.20 (resistance)          │
│                                                     │
│ TODAY'S EVENTS                                      │
│ No major economic releases today                    │
│ Focus: Breadth data for direction signal            │
│                                                     │
│ PRE-MARKET CHECKLIST                                │
│ ☐ Futures checked | ☐ Watchlists loaded            │
│ ☐ Alerts configured | ☐ Levels marked              │
│ ☐ Mindset: SELECTIVE/CAUTIOUS                      │
│                                                     │
│ TRADE LOG (Real-time updates)                       │
│ [Trades will appear here as you execute them]      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔗 FILE LINKING

### Sunday Weekly Planner Generates:
```markdown
File: Research/AI/2025-10-19_WEEKLY_METRICS.md

This file contains:
- Weekly signal forecast
- Economic calendar (full week)
- Trigger stack with 3 setups
- Portfolio positioning guide (Mon-Fri daily breakdown)
- Risk controls and hedges
- Key market levels (weekly view)
- Status: "Last updated: Sunday Oct 19, 3:30 PM"
```

### Daily Metrics File (Created Each Day):
```markdown
File: Research/AI/2025-10-20_DAILY_METRICS.md

This file contains:
- Today's context (pulled from weekly above)
- Today's 3 priorities (from weekly trigger stack)
- Today's key levels (filtered from weekly)
- Today's economic calendar (just today)
- Pre-market checklist
- Trade execution log (updates live)
- Status: "Last updated: Monday Oct 20, 9:00 AM"
```

### Both Files Read Into Dashboard:
```javascript
// Pseudo-code for dashboard integration
fetch('Research/AI/2025-10-19_WEEKLY_METRICS.md')
  .then(data => displayWeeklyPlanner(data))

fetch('Research/AI/2025-10-20_DAILY_METRICS.md')
  .then(data => displayDailyPlanner(data))
```

---

## 📋 WORKFLOW COMMANDS

### To Create Weekly Metrics (Sunday):
```
You: "wingman, sunday planner"

Wingman: [Runs through SUNDAY_WEEKLY_PLANNER.md checklist]
         [Collects your metrics inputs]
         [Generates 2025-10-19_WEEKLY_METRICS.md]
         [Saves to Research/AI/]
         [Updates dashboard]

You're Set: Weekly planner loaded into dashboard
```

### To Create Daily Metrics (Each Day):
```
You: "wingman, daily planner"

Wingman: [Pulls context from this week's WEEKLY_METRICS.md]
         [Creates today's priorities from weekly stack]
         [Generates 2025-10-20_DAILY_METRICS.md]
         [Saves to Research/AI/]
         [Updates dashboard]

You're Set: Daily planner loaded for today's trading
```

### To View Planners Tab:
```
Action: Open master-plan/research-dashboard.html
Click: "Planners" tab
See: Weekly Planner section (top)
     Daily Planner section (below)
     Both auto-refresh from markdown files
```

---

## 🎯 KEY INTEGRATION POINTS

1. **Weekly Context Drives Daily Execution**
   - Daily planner inherits weekly trigger stack
   - Daily priorities are filtered from weekly setups
   - Risk controls cascade (weekly max → daily limits)

2. **Data Persistence**
   - Weekly metrics saved as markdown file
   - Daily metrics saved as markdown file
   - Dashboard reads both, displays in unified view

3. **Real-Time Updates**
   - Daily planner updates as trades execute
   - Trade log populates live
   - P&L calculations update automatically

4. **Cross-Reference**
   - Daily planner links to weekly context
   - Weekly planner links to daily execution
   - All data trails back to master metrics

---

## 📊 METRICS COLLECTED & DISPLAYED

### Weekly Metrics (Collected Sunday)
```
✓ Signal progression (3-day trend)
✓ Sentiment analysis (social + media)
✓ Market structure (breadth, VIX, divergences)
✓ Portfolio health (balance, P&L, positioning)
✓ Provider consensus (themes, divergences)
✓ Economic calendar (week view)
✓ Risk assessment (heat, hedges, tail risks)
✓ Trigger stack (3 weekly setups)
✓ Daily positioning guide (Mon-Fri)
✓ Rules compliance check
```

### Daily Metrics (Generated Each Day)
```
✓ Today's signal & inherited context
✓ Today's 3 priorities (from weekly)
✓ Today's key levels (filtered)
✓ Today's economic calendar
✓ Pre-market checklist
✓ Trade execution log (live update)
✓ Risk controls for today
✓ EOD summary template
✓ Tomorrow's prep
```

---

## 🚀 YOUR OPERATIONAL FLOW

```
SUNDAY
└─ "wingman, sunday planner"
   └─ Weekly metrics collected + saved
   └─ Dashboard loads weekly planner tab
   └─ Review: trigger stack, risk controls, calendar
   └─ Ready for week

MONDAY-FRIDAY
├─ Market open: "wingman, daily planner"
│  └─ Daily metrics created (from weekly context)
│  └─ Dashboard loads daily planner tab
│  └─ Review: today's 3 priorities, levels, events
│  ├─ Trade execution: Update trade log in real-time
│  └─ EOD: Fill summary, review against weekly plan

NEXT SUNDAY
└─ Repeat: "wingman, sunday planner"
   └─ New weekly metrics collected
   └─ Dashboard resets for next week
   └─ Previous week's data persists in Research/AI/
```

---

## ✅ IMPLEMENTATION CHECKLIST

**Already Created:**
- [x] SUNDAY_WEEKLY_PLANNER.md (with enhanced metrics)
- [x] DAILY_PLANNER_TEMPLATE.md (template for daily files)
- [x] 2025-10-19_WEEKLY_METRICS.md (example weekly file)

**Next Steps:**
- [ ] Integrate Planners tab into research-dashboard.html
- [ ] Add data binding to read weekly/daily metrics files
- [ ] Create display sections for weekly + daily planners
- [ ] Test: Load dashboard, check both planner sections
- [ ] Create daily metrics file for tomorrow (2025-10-20_DAILY_METRICS.md)

---

**This integration transforms the research dashboard into your unified planning & execution hub.**

*Every Sunday, you plan the week. Every day, you execute that plan. The dashboard displays both.*

🚀 **Ready to integrate, Pilot.**
