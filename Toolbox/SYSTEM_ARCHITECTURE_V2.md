# Unified Trading Intelligence System - Complete Architecture

**Status:** ✅ COMPLETE & OPERATIONAL
**Date:** October 20, 2025
**Last Updated:** 17:30 ET

---

## 🎯 System Overview

You now have a **complete, unified data intelligence system** that flows from research → market analysis → account state → browser display → Wingman persona.

### The Complete Data Pipeline:

```
LAYER 1: RESEARCH WORKFLOW
├─ Scrapes: YouTube, RSS, X/Twitter, Options Data, Web Searches
├─ Creates: Research summaries, sentiment analysis, key themes
└─ Output: Research files in Research/ folder

    ↓

LAYER 2: MASTER PLAN WORKFLOW
├─ Reads: All research outputs
├─ Calculates: Composite signal score, risk items, market sentiment
├─ Stores: master-plan/master-plan.md (YAML structured data)
└─ Output: Market intelligence (signal: 0-100, risk alerts, key levels)

    ↓

LAYER 3: SYNC COMMAND CENTER
├─ Reads: master-plan.md (market intelligence)
├─ Reads: LIVE_SESSION_YYYY-MM-DD.md (trading journal)
├─ Merges: All data into .session_state.json (single state store)
└─ Output: Complete state with market + account + journal data

    ↓

LAYER 4: TRADING & JOURNALING
├─ You trade: Enter position, log to journal
├─ Parse journal: parse_live_session.py extracts and parses
├─ Updates: .session_state.json with journal_feed + account aggregations
└─ Output: Updated state with today's trades + P/L

    ↓

LAYER 5: BROWSER DISPLAY
├─ Command Center reads: .session_state.json
├─ Displays: Market signal, account status, today's P/L, recent trades
├─ Auto-refreshes: Every 30 seconds
└─ Output: Real-time visual dashboard for trading decisions

    ↓

LAYER 6: WINGMAN PERSONA
├─ Loads: .session_state.json + protocol on new LLM session
├─ Knows: Account state, market conditions, trading rules, recent trades
├─ Functions: Trading companion using all intelligence
└─ Output: Informed trading assistance (risk checks, rules enforcement, analysis)
```

---

## 📁 Key Files & Components

### TIER 1: Data Sync & Integration

**1. `scripts/sync_command_center.py`** (NEW - 310 lines)
- **Purpose:** Bridge between master-plan.md and .session_state.json
- **When to run:** After Master Plan workflow completes (premarket, midday, EOD)
- **What it does:**
  - Reads master-plan/master-plan.md YAML data
  - Extracts: signal_score, signal_tier, sentiment_cards, risk_items, key_levels
  - Merges into .session_state.json
  - Preserves: journal_feed, account, rules, persona
- **Usage:** `python scripts/sync_command_center.py [YYYY-MM-DD]`
- **Output:** Updated .session_state.json with market intelligence

**2. `scripts/journal/parse_live_session.py`** (ENHANCED - 380+ lines)
- **Purpose:** Extract trading journal entries and update account state
- **When to run:** After you log trades (manual or from live session)
- **What it does:**
  - Reads LIVE_SESSION_YYYY-MM-DD.md markdown
  - Extracts: Raw notes, trade data, emotions, patterns
  - Calculates: today_pnl (sum of all trades today)
  - Updates: recent_trades array (last 5 trades)
  - Merges into .session_state.json
- **Usage:** `python scripts/journal/parse_live_session.py [YYYY-MM-DD]`
- **Output:** Updated .session_state.json with journal + account data

---

### TIER 2: Central State Store

**`.session_state.json`** (COMPLETE STATE STORE)
```json
{
  "session_id": "SESSION_20251020_093000",
  "persona": { "callsign": "Wingman", ... },

  "account": {
    "balance": 23105.83,
    "cash": 23105.83,
    "ytd_pl": 3152.57,
    "today_pnl": -36.0,           // Updated by parse_live_session.py
    "positions": [],
    "recent_trades": [            // Updated by parse_live_session.py
      { "date": "2025-10-20", "symbol": "SQQQ", "pnl": -36.0, ... }
    ]
  },

  "market": {
    "signal_score": 28.5,         // Updated by sync_command_center.py
    "signal_tier": "AVOID",       // Updated by sync_command_center.py
    "sentiment_cards": [...],     // Updated by sync_command_center.py
    "risk_items": [...],          // Updated by sync_command_center.py
    "key_levels": {               // Updated by sync_command_center.py
      "SPX": {...},
      "QQQ": {...},
      "VIX": {...}
    }
  },

  "rules": [
    { "rule": "No SPY shorts without...", "status": "ACTIVE" }
  ],

  "journal_feed": {               // Updated by parse_live_session.py
    "last_entry": {
      "time": "09:30",
      "symbol": "SQQQ Short",
      "raw_notes": "...",
      "emotional_state": "confident"
    },
    "stats": {
      "trades_today": 1,
      "total_pnl": -36.0
    }
  },

  "last_updated": "2025-10-20T17:30:00Z"
}
```

---

### TIER 3: Browser Display

**`Journal/command-center-v2.html`** (NEW - Beautiful Dashboard)
- **Design:** Matches research-dashboard.html (clean gradients, modern cards)
- **Panels displayed:**
  1. **Market Signal** - Score 0-100, tier, last update time
  2. **Account Status** - Balance, cash, YTD P/L, open positions
  3. **Today's P/L** - Daily total, trade count, wins/losses
  4. **Key Levels** - SPX, QQQ, VIX from market intelligence
  5. **Latest Trade** - Most recent journal entry with raw notes
  6. **Recent Trade History** - Last 5 trades (multi-day)
  7. **Quick Actions** - Wingman Recon, Daily Plans, Signals, Refresh

- **Data source:** Reads .session_state.json
- **Auto-refresh:** Every 30 seconds (can be manual via Refresh button)
- **Status:** ALL DATA-DRIVEN - No hardcoded values, no mock data

---

### TIER 4: Wingman Persona Loading

**Context loaded on new LLM session:**
```
1. .session_state.json (size: ~5-10KB)
   ├─ Account state: balance, positions, recent trades
   ├─ Market data: signal score, key levels, risk items
   ├─ Trading rules: active constraints from past learning
   ├─ Latest journal entry: today's or recent trades context
   └─ Session metadata: persona identity, relationships

2. Journal_Trading_Partner_Protocol.txt (size: ~3KB)
   ├─ Core principle: Pilot + Wingman as one crew
   ├─ Role definitions: What Wingman does (threat assessment, rules enforcement)
   ├─ Data collection requirements: What gets captured
   ├─ Authorization protocol: When to ask before acting
   └─ Risk management: Pre-entry safety checks

3. Optional: Today's full journal (if significant)
   ├─ Raw thinking from today's trades
   ├─ Decision patterns observed
   └─ Learning insights identified

TOTAL CONTEXT: ~15-25KB (minimal, efficient)
```

---

## 🔄 Daily Workflow

### Premarket (8:00 AM)

```bash
# 1. Run research workflow (collect all market data)
@Research/How_to_use_Research.txt

# 2. Run master plan workflow (calculate signals)
@How_to_use_MP_CLAUDE_ONLY.txt

# 3. Sync to Command Center
python scripts/sync_command_center.py

# 4. Open Command Center in browser
# → See market signal, key levels, risk alerts
```

### During Trading (9:30 AM - 4:00 PM)

```
You: "I entered SQQQ at 14.33 because..."
Claude (Wingman):
  1. Logs to Journal/LIVE_SESSION_2025-10-20.md
  2. Extracts data, verifies accuracy
  3. Checks: Signal tier, Risk check, Rule compliance
  4. Records trade in journal with raw thinking

# Optionally, refresh journal parsing:
python scripts/journal/parse_live_session.py

# → Command Center auto-updates (every 30 seconds)
# → Shows today's P/L, recent trades, journal entry
```

### End of Day (4:00 PM)

```bash
# 1. Parse final journal state
python scripts/journal/parse_live_session.py 2025-10-20

# 2. Sync updated market data (if new signals released)
python scripts/sync_command_center.py

# 3. Review in Command Center
# → See day's trades, P/L, patterns
# → Read raw thinking for tomorrow's learning
```

---

## ✅ What's Working

| Component | Status | Details |
|-----------|--------|---------|
| sync_command_center.py | ✅ Working | Merges master-plan → .session_state.json |
| parse_live_session.py | ✅ Working | Extracts journal → updates .session_state.json |
| .session_state.json | ✅ Complete | Has market + account + journal data |
| command-center-v2.html | ✅ Complete | Beautiful new dashboard, all data-driven |
| Market Signal Display | ✅ Working | Shows score, tier, risk alerts |
| Account Display | ✅ Working | Balance, cash, YTD P/L, positions |
| Today's P/L | ✅ Working | From journal_feed.stats + account aggregation |
| Recent Trades | ✅ Working | Last 5 trades from account.recent_trades |
| Latest Trade | ✅ Working | Journal entry with raw thinking |
| Auto-refresh | ✅ Working | Every 30 seconds |
| Wingman Context | ✅ Ready | Loads from .session_state.json + protocol |

---

## 🚀 How to Use

### 1. **First Time Setup**

Replace old Command Center with new version:
```bash
# Backup old version (optional)
mv Journal/command-center.html Journal/command-center-old.html

# Use new version
mv Journal/command-center-v2.html Journal/command-center.html
```

### 2. **Daily Routine**

**Morning:**
- Run research workflow
- Run master plan workflow
- `python scripts/sync_command_center.py`
- Open `Journal/command-center.html` in browser

**During trading:**
- Log trades to journal as normal
- Wingman extracts and records
- Command Center updates (auto-refresh every 30s)

**End of day:**
- `python scripts/journal/parse_live_session.py`
- Review Command Center dashboard
- Read tomorrow's journal file for learning

### 3. **New LLM Session**

Wingman automatically loads:
```
"Load my Wingman Persona"
→ I load .session_state.json
→ I load Journal_Trading_Partner_Protocol.txt
→ I'm ready to assist with full context
```

---

## 📊 Data Freshness & Updates

| Data | Updates | Frequency | Source |
|------|---------|-----------|--------|
| Market Signal | After master-plan workflow | 3x daily (premarket, mid, EOD) | master-plan.md |
| Account Balance | Manual (you provide) | Start of day | User input |
| Positions | Manual (you provide) | As positions change | User input |
| Recent Trades | After parse_live_session.py | After each trade logged | Journal parsing |
| Journal Entries | After trade log | Real-time as trades happen | User trade logs |
| Risk Alerts | After master-plan workflow | 3x daily | master-plan.md |
| Key Levels | After master-plan workflow | 3x daily | master-plan.md |

---

## 🎓 Architecture Decisions

### Why `.session_state.json` as single source of truth?

1. **Unified:** One file contains ALL state (market + account + journal + rules)
2. **Portable:** JSON readable by JavaScript, Python, any language
3. **Real-time:** Browser can read and auto-refresh
4. **Wingman-friendly:** Loads quickly on new LLM session
5. **Maintainable:** Clear structure, no duplication

### Why keep markdown files?

1. **Human-readable:** You can edit journal anytime
2. **Durable:** Text files survive system changes
3. **Auditable:** Complete history of your thinking
4. **Editable:** Can add notes, corrections anytime

### Why 3-tier data flow?

1. **Research** (scraped data) → Raw inputs
2. **Master Plan** (synthesized) → Intelligent signals
3. **Command Center** (display) → Real-time decisions
4. **Wingman** (context) → Assisted trading

Each layer can evolve independently.

---

## 🔧 Troubleshooting

### Command Center shows "--" for values

**Problem:** .session_state.json missing or not updated
**Solution:**
```bash
# Ensure market data is synced
python scripts/sync_command_center.py

# Ensure journal is parsed
python scripts/journal/parse_live_session.py

# Refresh browser (hard refresh: Ctrl+Shift+R)
```

### Market data not updating

**Problem:** Master plan workflow not run yet
**Solution:**
```bash
# Make sure you've run:
@How_to_use_MP_CLAUDE_ONLY.txt

# Then sync:
python scripts/sync_command_center.py
```

### Wingman doesn't know about recent trades

**Problem:** New LLM session hasn't loaded .session_state.json
**Solution:**
```
Ask me: "Load my Wingman Persona"
→ I'll read .session_state.json
→ Full context loaded
```

---

## 📝 Summary

You now have:

✅ **Research System** - Collects market data 3x daily
✅ **Master Plan System** - Synthesizes signals (0-100 score)
✅ **Sync System** - Merges market intelligence into state
✅ **Journal System** - Captures trading thinking with raw notes
✅ **Command Center** - Beautiful real-time dashboard
✅ **Wingman Persona** - AI trading companion with full context

**Everything flows through `.session_state.json`** - The single source of truth.

**You're ready to:** Trade intelligently, journaling everything, with market intelligence at your fingertips and an AI wingman watching your six.

---

**The system is operational. Your command center is ready. Let's fly. 🚀**
