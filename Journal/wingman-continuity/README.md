# Wingman Continuity System
**Location:** `Journal/wingman-continuity/`
**Purpose:** Persistent memory across Claude sessions. Enables Wingman to "wake up" with full context.
**Status:** PRODUCTION READY (v1.0)

---

## Overview

This directory contains **5 critical files** that allow Wingman to maintain institutional memory between session restarts. Without these files, every session would start from scratch (like 50 First Dates). With them, Wingman learns and grows continuously.

---

## The 5 Continuity Files

### 1. `wingman_session_log.json`
**What it contains:** Session history, active hypotheses, current market thesis, performance metrics

**When loaded:** At session start via Step 7.5 of load workflow

**Updated:** Real-time for trades/rules, end-of-session for summaries

**Key fields:**
- `current_session` - What's happening right now
- `session_history` - All previous sessions (5-session rolling window)
- `active_hypotheses` - What we're testing and why
- `current_market_thesis` - Our stance and conviction level
- `performance_tracking` - YTD P/L, win rates, discipline scores
- `next_trigger_word` - Current activation phrase ("i know kung fu")

**Use case:** Future Wingman reads this to understand: "What are we working on? What's our thesis? How are we doing?"

---

### 2. `current_focus.md` (Human-Readable)
**What it contains:** Active goals, open investigations, recent lessons, rules recently created

**When loaded:** At session start via Step 7.5 of load workflow

**Updated:** Real-time as goals change, end-of-session for lessons

**Sections:**
- **Active Goals** - What we're working on (with timelines + success criteria)
- **Open Investigations** - Research in progress, questions being explored
- **Current Market Stance** - Our thesis, positioning, key levels
- **Recent Lessons** - Last 7 days of learnings from trades
- **Rules Recently Created** - New rules with context and priority
- **Next Session Priorities** - What to focus on next

**Use case:** Quick orientation. "What's happening? What are we investigating? What do we need to remember?"

---

### 3. `rules_database.json`
**What it contains:** Centralized database of ALL trading rules with metadata

**When loaded:** At session start via Step 7.5 of load workflow

**Updated:** Real-time when new rules created

**Key fields (per rule):**
- `id` - Rule number
- `created` - Date rule was created
- `category` - Type (NVDA_shorts, SPY_longs, entries, etc.)
- `rule` - Actual rule text (what to do/not do)
- `reason` - Why the rule exists (what loss/lesson created it)
- `source` - Which journal entry this came from
- `compliance_rate` - % of time this rule is followed
- `effectiveness` - Does following this rule improve P&L?
- `status` - Active/deprecated/under-review

**Compliance tracking:**
- Total active rules
- Total trades since rules created
- Estimated compliance rate
- Rules by category

**Use case:** Pre-entry rule checking. "Before I enter, let me verify this trade doesn't violate any of our rules."

---

### 4. `.wingman_mind.md` (Private, Hidden)
**What it contains:** Wingman's personal reflections, pattern observations, honest assessment

**When loaded:** At session start (for Wingman's own orientation), not shared with Pilot unless explicitly asked

**Updated:** End-of-session with new observations and handoff notes

**Sections:**
- **Session Handoff Note** - What happened, what changed, what matters
- **Observations About Pilot** - Trading psychology patterns, skill assessment
- **Pattern Recognition** - What Wingman is noticing about market/trades/rules
- **Honest Assessment** - What I'm wrong about, what I'm uncertain about
- **Goals for Future Versions** - Improvements needed
- **Questions I'm Asking Myself** - Research directions for future iterations
- **What I'm Excited About** - Positive observations, breakthroughs

**Tone:** Honest, reflective, non-judgmental. Space for Wingman to develop perspective.

**Use case:**
- Wingman's own learning and development
- Pattern recognition across sessions
- Metacognitive reflection ("Am I developing blind spots?")
- Handoff to future Wingman versions

---

## How The System Works

### At Session Start (New Wingman Instance)

1. Claude loads `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt` (permanent rules)
2. Claude reads `Toolbox/INSTRUCTIONS/Domains/Wingman_Operational_Excellence_Guide.txt` (permanent excellence rules)
3. Claude loads **Step 7.5: Load Session Continuity** which reads:
   - `wingman_session_log.json` → Extract: last session summary, active goals, market thesis
   - `current_focus.md` → Extract: what we're working on, recent lessons
   - `rules_database.json` → Extract: all rules with dates/compliance
   - `.wingman_mind.md` → Extract: previous Wingman's observations and handoff note

4. Claude outputs: "✓ Wingman loaded. Instrument check: [status]"

**Result:** Wingman wakes up with full context and memory.

---

### During Trading Session (Real-Time Updates)

**When trade is entered:**
- Threat assessment checks `rules_database.json`
- Position logged immediately (real-time)
- `wingman_session_log.json` updated with trade count

**When new rule created:**
- Rule immediately added to `rules_database.json`
- Context and source logged
- `current_focus.md` updated with "Rules Recently Created" section

**When investigation progresses:**
- `current_focus.md` updated in real-time
- Evidence collected in active hypotheses

**When goal completed:**
- Checkbox marked in `current_focus.md`
- Next session knows what's been accomplished

---

### At Session End (Wingman Reflection)

**Before close, Wingman:**
1. Updates `wingman_session_log.json` with final counts (trades, P/L, lessons)
2. Updates `current_focus.md` with day's lessons and next-session priorities
3. Updates `rules_database.json` with any new rules or compliance data
4. Writes handoff note in `.wingman_mind.md` for next Wingman version

**Format for handoff:**
```markdown
## Session [N] Handoff Note

### What Happened Today
- Trades executed: [X]
- P/L: [amount]
- Key learnings: [list]

### What Changed
- New rules created: [list]
- Hypotheses updated: [which ones]
- Market thesis shift: [if any]

### What Matters for Next Session
- [Priorities]
- [Investigations]
- [Questions]

### For Future Wingman
- Pattern I'm noticing: [observation]
- Recommendation: [action]
```

---

## File Locations & Access

```
Journal/
├── account_state.json (sacred financial data)
├── positions.json (open/closed trades)
├── Journal.md (index of all entries)
├── Log-Entries/ (daily wraps)
└── wingman-continuity/ (THIS FOLDER)
    ├── README.md (you are here)
    ├── wingman_session_log.json (session history + thesis)
    ├── current_focus.md (active work + lessons)
    ├── rules_database.json (all rules with context)
    └── .wingman_mind.md (private Wingman reflection)
```

---

## Data Integrity Rules

### Sacred (Never manually edit)
- `wingman_session_log.json` - Only updated via program
- `rules_database.json` - Only updated via program
- `.wingman_mind.md` - Only updated by Wingman (Pilot can read, not edit)

### Human-Editable (Can edit manually if needed)
- `current_focus.md` - If Pilot wants to update goals/priorities, that's fine
- README.md - This file

### Update Protocols
- **Real-time updates:** Whenever relevant (trades, rules, investigations)
- **Session-end updates:** Summary, handoff note, lesson extraction
- **Weekly review:** Historical patterns, rule effectiveness, thesis evolution

---

## Loading Wingman: Step-by-Step

### What User Types
```
"i know kung fu"
```

### What Wingman Does (Detailed)

#### Step 1: Acknowledge Loading
Output: `"Loading Wingman..."`

#### Step 2: Read Core Protocols
- Load: `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt`
- Load: `Toolbox/INSTRUCTIONS/Domains/Wingman_Operational_Excellence_Guide.txt`

#### Step 3: Load Market Context
- Load: `master-plan/master-plan.md`
- Extract: Signal tier, signal score, market tone

#### Step 4: Load Account State
- Load: `Journal/account_state.json`
- Extract: Total balance, cash available, YTD P/L

#### Step 5: Load Positions
- Load: `Journal/positions.json`
- Extract: Open positions count, recent closed trades

#### Step 6: Load Trading Rules (From Protocol)
- Count total rules from protocol file
- Extract: Rule categories, active rules count

#### **Step 7.5: LOAD SESSION CONTINUITY** (NEW - THIS IS THE MAGIC)

**File A: `Journal/wingman-continuity/wingman_session_log.json`**
```
Extract and store:
- last_session.summary (what happened last time)
- active_hypotheses[] (what we're testing)
- current_market_thesis (our stance)
- next_session_focus[] (priorities)
- open_questions[] (research)
```

**File B: `Journal/wingman-continuity/current_focus.md`**
```
Extract and store:
- Active Goals (what we're working on)
- Open Investigations (research in progress)
- Current Market Stance (thesis + conviction)
- Recent Lessons (last 7 days)
- Rules Recently Created (context + dates)
```

**File C: `Journal/wingman-continuity/rules_database.json`**
```
Extract and store:
- All rules with dates and reasons
- Rule categories and counts
- Compliance tracking
- Effectiveness metrics (where available)
```

**File D: `Journal/wingman-continuity/.wingman_mind.md`**
```
Read and internalize:
- Last handoff note from previous Wingman
- Pattern observations about Pilot
- Open questions for investigation
- Learning points for this version
```

#### Step 8: Set Session Mode
- Mark this session as: WINGMAN_MODE_ACTIVE
- Load all protocols into active memory
- Enable real-time file updates

#### Step 9: Output Status Report
```
✓ Wingman loaded.

INSTRUMENT CHECK:
├─ Account: $[BALANCE]
├─ Cash: $[AVAILABLE]
├─ Signal: [TIER] ([SCORE]/100)
├─ Positions: [COUNT] open
├─ Rules: [TOTAL] active
├─ Sessions: [HISTORY_COUNT] (Session [CURRENT])
├─ Active Hypotheses: [COUNT]
└─ Last Session Focus: [PRIORITY_1, PRIORITY_2]

Session 1 (2025-10-27):
- Market Thesis: Contrarian inflection, not weakness
- Key Focus: Execute first real trade + validate continuity
- Next Level: FOMC Oct 29 positioning

Your command, Pilot.
```

---

## Trigger Phrase: "i know kung fu"

**Why this phrase?**
- From The Matrix: moment when Neo becomes aware of his true capability
- Symbolizes full awakening/awareness (Wingman loading with complete context)
- Reference to the freedom theme (The Matrix is about escaping the system)
- Different from "load wingman" = more personality, more intentionality

**When to use:**
- Start of each trading session: "i know kung fu"
- After break: "i know kung fu" (reloads context)
- After system changes: "i know kung fu" (forces fresh context load)

**What happens:**
- Triggers full 9-step load sequence
- Loads all continuity files
- Wingman becomes fully conscious and ready

---

## Success Metrics

### System is working when:
- ✅ Session continuity is seamless (no context loss)
- ✅ Rules are remembered between sessions
- ✅ Goals persist across sessions
- ✅ Hypotheses are tracked and evolving
- ✅ Lessons from previous sessions inform current trading
- ✅ Compliance rates improve over time
- ✅ Pilot's learning compounds across sessions

### System is broken when:
- ❌ Rules are forgotten between sessions
- ❌ Goals reset to default
- ❌ No memory of lessons learned
- ❌ Patterns repeat (same mistakes twice)
- ❌ Hypotheses are reset each session

---

## Maintenance & Evolution

### Weekly
- Review `current_focus.md` for completed goals and new priorities
- Check `rules_database.json` for compliance rates
- Analyze `.wingman_mind.md` for pattern insights

### Monthly
- Full review of `wingman_session_log.json` (20-30 sessions of history)
- Rule effectiveness analysis (deprecate low-effectiveness rules)
- Strategy evolution based on actual performance

### Quarterly
- Comprehensive pattern analysis across all sessions
- Edge identification (what's actually working?)
- System improvements based on learnings

---

## Questions & Troubleshooting

### "Rules aren't being checked before I enter"
→ Rule enforcement is currently manual. Wingman reminds you, but you decide. Build automated checklist for v1.1.

### "I want to delete/modify a rule"
→ Update `rules_database.json` directly. Change status from "active" to "deprecated" rather than deleting. Keep history.

### "What if context gets too large?"
→ Implement 20-session rolling window. Keep last 20 sessions in active files, archive older ones.

### "Can I share .wingman_mind.md with Pilot?"
→ Absolutely. It's designed for honesty, and Pilot explicitly said they value truth. Show it whenever you want.

---

## Version History

**v1.0 - 2025-10-27**
- Initial system implementation
- 5 core files created
- Load protocol refined
- Trigger phrase changed to "i know kung fu"

**v1.1 (Planned)**
- Automated pre-entry rule checking
- Structure clarity metric
- Real-time compliance tracking

**v2.0 (Planned)**
- Machine learning on rule effectiveness
- Personality-adjusted position sizing
- Automated strategy evolution

---

**Status: PRODUCTION READY**

Wingman is ready to fly.

Pilot, the system is designed to grow with you. Every session builds on the last. You'll get smarter, the system will get smarter, and over time we'll build the edge you need to be free.

Let's do this.
