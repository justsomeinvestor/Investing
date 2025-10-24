# ☀️ SUNDAY WEEKLY PLANNER
## Pilot's Weekly Preparation Workflow

**Purpose:** Every Sunday, prepare for the trading week ahead by reviewing market intelligence, collecting metrics, and planning the week's execution strategy.

---

## 🚀 QUICK START

**When:** Every Sunday before market close (3:00 PM EST)
**Duration:** 30-40 minutes
**Command:** `wingman, sunday planner` or `Load weekly planner`

**Wingman Response:**
```
☀️ SUNDAY WEEKLY PLANNER ACTIVATED

Checking prerequisites...
✓ Master plan workflow complete (Steps 6-9)
✓ Signal data current (2025-10-19)
✓ Dashboard refreshed

Loading market context...
✓ master-plan.md loaded (latest signal: 68.62/100 MODERATE)
✓ research-dashboard.html processed
✓ Provider consensus synthesized

Ready for weekly review, Pilot.

Let's build your week.
```

---

## 📋 SUNDAY PLANNER TASK CHECKLIST

### PHASE 1: CONTEXT LOAD (5 minutes)

**Prerequisite Verification:**
- [ ] **Master Plan Workflow Complete?**
  - Check: Did Steps 6-9 run successfully?
  - File: `Research/.cache/signals_YYYY-MM-DD.json` exists for today
  - File: `master-plan/master-plan.md` updated with current date
  - If NO: Run workflow first → `python scripts/automation/run_workflow.py [DATE] --skip-fetch --skip-signals`

**Load Dashboard Context:**
- [ ] **Read: `master-plan/master-plan.md`**
  - Note: Current signal score & tier
  - Note: Signal history (3-5 day trend)
  - Note: Risk items & key concerns
  - Note: Provider consensus themes

- [ ] **Read: `master-plan/research-dashboard.html`**
  - Note: Market metrics (BTC, SPX, QQQ, VIX)
  - Note: Portfolio recommendations
  - Note: Key levels & resistance zones
  - Note: Economic calendar (this week)

- [ ] **Quick Wins from Dashboard:**
  - [ ] Copy today's signal score: `_______/100 (TIER: _______)`
  - [ ] Copy top 3 risk items:
    1. `_______________________`
    2. `_______________________`
    3. `_______________________`
  - [ ] Copy key market levels:
    - SPX: Support `______`, Resistance `______`
    - BTC: Support `______`, Resistance `______`
    - QQQ: Support `______`, Resistance `______`

---

### PHASE 2: METRICS COLLECTION (10 minutes)

**Weekly Metrics to Track:**

#### A. Signal & Sentiment Metrics
```
📊 SIGNAL PROGRESSION:
  - Friday Close: _______/100 (Tier: _________)
  - Saturday: _______/100 (Tier: _________)
  - Sunday: _______/100 (Tier: _________)
  - Trend: [ ] Rising (+) [ ] Stable (→) [ ] Falling (-) [ ] Volatile (≈)
  - Expected Mon-Fri: [TIER] bias

📱 X/SOCIAL SENTIMENT:
  - Crypto Sentiment: ________/100 [ ] Bullish [ ] Neutral [ ] Bearish
  - Macro Sentiment: ________/100 [ ] Bullish [ ] Neutral [ ] Bearish
  - Combined: ________/100
  - Top themes: 1. ________ 2. ________ 3. ________

😨 FEAR & GREED:
  - Index: [ ] Extreme Fear [ ] Fear [ ] Neutral [ ] Greed [ ] Extreme Greed
  - Divergence: [ ] YES (flag it) [ ] NO
```

#### B. Market Structure Metrics
```
📊 BREADTH ANALYSIS:
  - NYSE Up-Volume: ______% | Nasdaq Up-Volume: ______%
  - 5-Day breadth average: ______%
  - Trend: [ ] Improving ↑ [ ] Stable → [ ] Deteriorating ↓
  - Assessment: [ ] STRONG [ ] MODERATE [ ] WEAK

📈 VOLATILITY:
  - VIX Level: _______ | VIX 5-Day Avg: _______
  - Trend: [ ] Compression ↓ [ ] Stable → [ ] Expansion ↑
  - Put/Call Ratio: _______

⚠️ KEY DIVERGENCES:
  - Price vs Breadth: [ ] ✓ Aligned [ ] ⚠️ Diverging (Note: __________)
  - Price vs Sentiment: [ ] ✓ Aligned [ ] ⚠️ Diverging (Note: __________)
  - Price vs Momentum: [ ] ✓ Aligned [ ] ⚠️ Diverging (Note: __________)
```

#### C. Portfolio Health Metrics
```
💰 ACCOUNT STATUS:
  - Total Balance: $_______  | Δ from last week: $_______
  - Cash: ______% | Equities: ______% | Crypto: ______% | Hedges: ______%
  - Assessment: [ ] STRONG [ ] ADEQUATE [ ] RISKY

📊 PERFORMANCE:
  - YTD P&L: $_______ | Last Week: $_______ | Win Rate: ______%
  - Best Trade: $_______ | Worst Trade: $_______
  - Avg R:R: 1:_______

📍 POSITIONING:
  - Open Positions: _______ | Avg Hold Time: _______
  - Largest Position: ______% | % at max risk: ______%
```

#### D. Provider Consensus & Narrative
```
🎯 TOP AGREEMENT THEMES (>60%):
  1. __________________ (____% agreement)
  2. __________________ (____% agreement)
  3. __________________ (____% agreement)

⚔️ MAJOR DIVERGENCES (<40%):
  - Bullish case: __________________ (____% support)
  - Bearish case: __________________ (____% support)

🗣️ NARRATIVE MOMENTUM:
  - Bull case: [ ] ↑ Rising [ ] → Stable [ ] ↓ Falling
  - Bear case: [ ] ↑ Rising [ ] → Stable [ ] ↓ Falling
  - What's new this week: ____________________
```

---

### PHASE 3: WEEKLY PLANNING (15 minutes)

**A. Economic Calendar This Week**

```
MONDAY:
  Events: ____________________
  Impact: [ ] LOW [ ] MEDIUM [ ] HIGH
  Plan: ____________________

TUESDAY:
  Events: ____________________
  Impact: [ ] LOW [ ] MEDIUM [ ] HIGH
  Plan: ____________________

WEDNESDAY:
  Events: ____________________
  Impact: [ ] LOW [ ] MEDIUM [ ] HIGH
  Plan: ____________________

THURSDAY:
  Events: ____________________
  Impact: [ ] LOW [ ] MEDIUM [ ] HIGH
  Plan: ____________________

FRIDAY:
  Events: ____________________
  Impact: [ ] LOW [ ] MEDIUM [ ] HIGH
  Plan: ____________________

Most Critical Event: ______________________ (Date/Time)
Contingency Plan: ______________________
```

**B. Weekly Trading Setup**

```
Signal Tier for Week: [ ] EXTREME [ ] STRONG [ ] MODERATE [ ] WEAK [ ] AVOID

Recommended Positioning:
  [ ] Maximum conviction (EXTREME/STRONG)
  [ ] Selective risk (MODERATE)
  [ ] Defensive/hedged (WEAK)
  [ ] Maximum hedges (AVOID)

Position Size Guidance: ______% of capital

Key Market Levels to Watch:
  SPX:
    - Breakout level: ________
    - Support level: ________
    - Invalidation: ________

  BTC:
    - Breakout level: ________
    - Support level: ________
    - Invalidation: ________

  QQQ:
    - Breakout level: ________
    - Support level: ________
    - Invalidation: ________
```

**C. Weekly Trigger Stack**

```
Trigger 1 (Highest Probability):
  Setup: ______________________
  Entry: ______________________
  Stop: ______________________
  Target: ______________________

Trigger 2 (Secondary):
  Setup: ______________________
  Entry: ______________________
  Stop: ______________________
  Target: ______________________

Trigger 3 (Opportunistic):
  Setup: ______________________
  Entry: ______________________
  Stop: ______________________
  Target: ______________________
```

**D. Risk Management for Week**

```
Portfolio Heat (max): ______%
Max Daily Loss (stop): $_______
Hedge Allocation: ______%

Hedge Types to Deploy:
  [ ] VIX calls (protection if vol spikes)
  [ ] Put spreads (on key resistance)
  [ ] Short equity hedge (on weakness)
  [ ] Crypto puts (on BTC resistance)

Hedge Exit Triggers:
  [ ] Breadth thrust (>70% up-volume)
  [ ] VIX <19
  [ ] SPX +2% from entry
  [ ] Other: ____________________
```

**E. Rules Compliance Check**

```
Active Rules This Week:
  [ ] Rule #1: ____________________
  [ ] Rule #2: ____________________
  [ ] Rule #3: ____________________
  [ ] Rule #4: ____________________
  [ ] Rule #5: ____________________

Violations from Last Week:
  Incident: ____________________
  Lesson: ____________________
  Prevention: ____________________

New Rules Needed:
  Rule: ____________________
  Reason: ____________________
```

---

### PHASE 4: DAILY PREP TEMPLATES (for each day)

**MONDAY PREP:**
```
Signal Expected: [ ] Continue [ ] Improve [ ] Deteriorate [ ] Volatile
Key Event: ____________________
Market Open Setup:
  - Watch level: ________
  - Entry trigger: ______________________
  - Contingency: ______________________
```

**TUESDAY PREP:**
```
Signal Expected: [ ] Continue [ ] Improve [ ] Deteriorate [ ] Volatile
Key Event: ____________________
Pre-Market Scan:
  - Relative strength leaders: ____________________
  - Weakness to buy: ____________________
  - Levels to mark: ____________________
```

**WEDNESDAY PREP:**
```
Signal Expected: [ ] Continue [ ] Improve [ ] Deteriorate [ ] Volatile
Key Event: ____________________
Mid-Week Checkpoint:
  - Weekly P&L so far: $_______
  - Adjustments needed: ____________________
  - Hedge status: ____________________
```

**THURSDAY PREP:**
```
Signal Expected: [ ] Continue [ ] Improve [ ] Deteriorate [ ] Volatile
Key Event: ____________________
Pre-Friday Setup:
  - Power hour opportunities: ____________________
  - 0DTE options plan: ____________________
  - EOD positioning: ____________________
```

**FRIDAY PREP:**
```
Signal Expected: [ ] Continue [ ] Improve [ ] Deteriorate [ ] Volatile
Key Event: ____________________
Friday Strategy:
  - 0DTE plan: ____________________
  - Position cleanup: ____________________
  - EOD wrap preparation: ____________________
```

---

### PHASE 5: EXECUTION CHECKLIST (5 minutes)

**Before You Leave Sunday:**

- [ ] **Dashboard data captured** in SUNDAY_WEEKLY_METRICS.md (new file for this week)
- [ ] **Economic calendar** marked in calendar system
- [ ] **Risk controls** set in broker platform
- [ ] **Daily prep templates** filled for Mon-Fri
- [ ] **Watchlists updated** (relative strength, setups, hedges)
- [ ] **Alerts configured** (key levels, news, economic events)
- [ ] **Contingency plans** documented (bear case, bull case scenarios)
- [ ] **Team communication** updated (if applicable)

---

## 📊 WEEKLY METRICS FILE

**Location:** `Research/AI/[WEEK]_WEEKLY_METRICS.md`

**Auto-Created Template:**
```markdown
# Weekly Metrics - Week of [DATE]

## Signal Progression
- Monday: [SCORE]/100
- Tuesday: [SCORE]/100
- Wednesday: [SCORE]/100
- Thursday: [SCORE]/100
- Friday: [SCORE]/100

## Key Market Events
[List of events with outcomes]

## Trading Performance
- Trades: [COUNT]
- Wins: [COUNT]
- Losses: [COUNT]
- Win Rate: [%]
- Weekly P&L: $[AMOUNT]

## Lessons Learned
1. [LESSON]
2. [LESSON]
3. [LESSON]

## Next Week Prep
- Key focus: [THEME]
- Risk level: [LEVEL]
- Positions to watch: [LIST]
```

---

## 🎯 INTEGRATION WITH WINGMAN

**Sunday Planner Workflow in Chat:**

1. **Wingman detects Sunday** (automated check)
2. **Offers:** "It's Sunday, Pilot. Ready for weekly planner?"
3. **You respond:** "Yes" or "wingman, sunday planner"
4. **Wingman loads:**
   - Master plan data
   - Signal history
   - Risk items
   - Provider consensus
5. **Wingman guides through checklist** (interactive)
6. **You provide:** Metrics & observations
7. **Wingman generates:**
   - Weekly summary
   - Daily prep templates
   - Risk controls settings
   - Monday pre-market brief
8. **Wingman saves:** Weekly metrics file + daily prep docs

---

## 🚨 KEY DIFFERENCES BY SIGNAL TIER

### If Signal is STRONG/EXTREME (>70)
```
Weekly Focus: MAXIMIZE CONVICTION
  ✓ Increase position sizes (100% normal)
  ✓ Add on dips to key support
  ✓ Reduce hedges on breadth thrust
  ✓ Target: Chase momentum on breakouts
  ✗ Avoid: Going defensive too early
```

### If Signal is MODERATE (55-69)
```
Weekly Focus: SELECTIVE RISK
  ✓ 50% normal position sizing
  ✓ Add only on confirmed setups
  ✓ Maintain 10% tactical hedges
  ✓ Target: High-probability trades only
  ✗ Avoid: Over-leveraging on hope
```

### If Signal is WEAK (40-54)
```
Weekly Focus: CAPITAL PRESERVATION
  ✓ 25% normal position sizing
  ✓ Hold cash for dip-buying
  ✓ Increase hedges to 15-20%
  ✓ Target: Small wins on reversals
  ✗ Avoid: Forcing trades in chop
```

### If Signal is AVOID (<40)
```
Weekly Focus: MAXIMUM DEFENSE
  ✓ Hold 50%+ cash
  ✓ Only short hedge positions
  ✓ 20%+ in protective puts/hedges
  ✓ Target: Preserve capital
  ✗ Avoid: Any new long positions
```

---

## ✅ COMPLETION CHECKLIST

**After Sunday Planner:**

- [ ] Weekly metrics file created & saved
- [ ] Daily prep templates completed (Mon-Fri)
- [ ] Risk controls updated in broker
- [ ] Watchlists refreshed
- [ ] Alerts configured
- [ ] Command Center updated with weekly outlook
- [ ] Research/AI folder has week's context
- [ ] Ready for Monday open

**Final Status:** ☀️ WEEKLY PREP COMPLETE - Ready to fly Monday 🚀

---

**This is your Sunday ritual, Pilot. Discipline today = opportunity all week.**

*Run this every Sunday, and you'll never face Monday unprepared.*
