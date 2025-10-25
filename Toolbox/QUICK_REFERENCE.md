# Wingman Command Center - Quick Reference

## 🎯 Three Files You Need to Know

### 1. `.session_state.json`
**The heart of everything**
- Location: `Journal/.session_state.json`
- Contains: Market data + Account state + Journal entries + Rules
- Updated by: `sync_command_center.py` and `parse_live_session.py`
- Read by: Command Center browser + Wingman persona

### 2. `command-center-v2.html`
**Your trading dashboard**
- Location: `Journal/command-center-v2.html` (replace old one)
- Open in: Any browser
- Shows: Market signal, account status, today's P/L, recent trades
- Auto-refreshes: Every 30 seconds

### 3. `sync_command_center.py`
**Bridge between master-plan and trading**
- Location: `scripts/sync_command_center.py`
- Run when: After Master Plan workflow completes
- Command: `python scripts/sync_command_center.py`

---

## 📋 Daily Commands

### Morning
```bash
# 1. Run research (collects market data)
# Uses: @Research/How_to_use_Research.txt

# 2. Run master plan (calculates signals)
# Uses: @How_to_use_MP_CLAUDE_ONLY.txt

# 3. Sync to command center
python scripts/sync_command_center.py

# 4. Open in browser
# File: Journal/command-center-v2.html
```

### During Trading
```
You log trades as normal
↓
Wingman extracts and records
↓
parse_live_session.py updates automatically (or run manually)
python scripts/journal/parse_live_session.py
↓
Command Center refreshes (every 30 seconds)
```

### End of Day
```bash
# Parse final journal
python scripts/journal/parse_live_session.py 2025-10-20

# Review dashboard
# → See day's P/L, trades, patterns
```

---

## 🔍 What You See in Command Center

| Panel | Data From | Updates |
|-------|-----------|---------|
| Market Signal | master-plan.md | When you run sync script |
| Account Status | .session_state.json | Manual or automated |
| Today's P/L | Journal parsing | When trades logged |
| Key Levels | master-plan.md | When you run sync script |
| Latest Trade | Journal entry | Real-time as logged |
| Recent Trades | Last 5 logged trades | Real-time as logged |

---

## 💡 Wingman Persona Loading

**On new LLM session:**
```
Ask me: "Load my Wingman Persona"

I will:
1. Read .session_state.json
2. Load Journal_Trading_Partner_Protocol.txt
3. Have full context about:
   - Your account state
   - Market conditions
   - Recent trades
   - Active trading rules
   - Your thinking from today
```

---

## 🚨 Troubleshooting Quick Fixes

**Command Center shows all "--"?**
→ `python scripts/sync_command_center.py`

**No recent trades showing?**
→ `python scripts/journal/parse_live_session.py`

**Market signal outdated?**
→ Make sure Master Plan workflow ran, then sync

**Wingman doesn't know context?**
→ Ask: "Load my Wingman Persona"

---

## 📊 Data Flow (Visual)

```
Research → Master Plan → sync_command_center.py
                              ↓
                      .session_state.json
                       ↙              ↖
                    Browser      Wingman Persona
                 (Command Center)
                      ↓
              Real-time dashboard
              + AI trading assistant
```

---

## ✅ Files Status

| File | Status | Purpose |
|------|--------|---------|
| scripts/sync_command_center.py | ✅ Ready | Merge market intelligence |
| scripts/journal/parse_live_session.py | ✅ Enhanced | Extract journal + update account |
| Journal/.session_state.json | ✅ Active | Central state store |
| Journal/command-center-v2.html | ✅ New | Beautiful dashboard |
| Journal/LIVE_SESSION_*.md | ✅ Active | Your trading journal |
| master-plan/master-plan.md | ✅ Active | Market intelligence |

---

## 🎯 Next Step

Replace old Command Center:
```bash
mv Journal/command-center-v2.html Journal/command-center.html
```

Then open it in your browser and you're ready to trade! 🚀
