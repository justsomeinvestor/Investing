# EOD Wrap Handler — Wingman Automation [UPDATED]

**Purpose:** When Pilot says "wingman, eod wrap [notes]", this handler executes a complete 7-step end-of-day automation process.

**Status:** ✅ FULLY AUTOMATED - Single command executes all steps (no manual work)

---

## 🔄 EOD Wrap Process

### Step 1: Collect Session Data
- Read today's session summary: `Research/AI/[DATE]_SESSION_SUMMARY.md`
- Parse all trades from session chat
- Calculate daily P&L
- Extract market observations and setups

### Step 2: Generate Journal Entry
Create: `Journal/Log-Entries/[DATE]_EOD_Wrap.md`

**Template Structure:**
```
# Daily Trading Journal — [DATE]

## Summary
- Net P/L (realized): $[X]
- Trades: [N]
- Overall Read: [Brief assessment]

## Trades
### [N] [TICKER] — [DIRECTION]
- Entry: [PRICE] @ [TIME]
- Exit: [PRICE] @ [TIME]
- P&L: $[X] ([%])
- Notes: [Setup, thesis, execution notes]

## Market Structure & Levels
[Key levels, setups, and observations]

## Psychology & Process
[Trader mindset, discipline, patterns observed]

## Lessons & Playbook Updates
[Rules violations, new insights, adjustments needed]

## Next Session Plan
[Prep checklist for tomorrow]
```

### Step 3: Update Command Center
- Update `Journal/COMMAND_CENTER.md`:
  - Today's P&L in status section
  - Latest trade in "Last Trade" panel
  - Update recent trade history (last 5)
  - Refresh market signal if available
  - Update YTD P&L

### Step 4: Update Account State
- Read from `.session_state.json` (trades recorded during session)
- Calculate realized P&L from all trades
- Update `Journal/account_state.json`:
  - New total_balance
  - Updated ytd_pl
  - Mark last_updated timestamp
  - Set data_freshness: "FRESH"

### Step 5: Update Session Summary
- Finalize `Research/AI/[DATE]_SESSION_SUMMARY.md`:
  - Fill in trades executed
  - Complete session statistics
  - Add execution review
  - Note rules compliance

### Step 6: Log Entry to Journal Index
- Update `Journal/Journal.md`:
  - Add today's entry to top of "Journal Entries (Newest First)"
  - Include summary line with key metrics
  - Link to detailed entry

### Step 7: Prepare for Next Session
- Reset `.session_state.json`:
  - Clear recent_trades array
  - Keep active rules
  - Preserve account balance
  - Set ready for next session

---

## 📋 EOD Wrap Output

**Files Updated:**
1. ✓ `Research/AI/[DATE]_SESSION_SUMMARY.md` — Finalized
2. ✓ `Journal/Log-Entries/[DATE]_EOD_Wrap.md` — Created
3. ✓ `Journal/COMMAND_CENTER.md` — Updated with today's data
4. ✓ `Journal/account_state.json` — P&L and balance updated
5. ✓ `Journal/Journal.md` — New entry logged
6. ✓ `.session_state.json` — Reset for next session

**Confirmation Message:**
```
✓ EOD COMPLETE

Daily Summary:
├─ Trades: [N]
├─ P&L: $[X] ([%])
├─ Execution: [Quality assessment]
├─ Account: $[NEW_BALANCE]
└─ YTD: $[YTD_PL]

Journal Updated. Ready for tomorrow.
```

---

## 🎯 Live Trade Recording Format

During the session, trades are recorded as:

**Format:** `[TICKER] [DIRECTION] [SIZE] @ [ENTRY], stop [STOP], target [TARGET]`

**Example:** `NVDA long 100 @ 189.50, stop 188, target 192`

**Wingman Response:**
1. Threat Assessment (Signal, Cash, R:R, Rules)
2. Ask: "Proceed with entry?"
3. On YES: Record to session state + confirm
4. On exit: Close position + calc P&L + update balance

---

## 📊 Session State Format

`.session_state.json` tracks live trades:

```json
{
  "session_id": "SESSION_20251019_121337",
  "trades": [
    {
      "ticker": "NVDA",
      "direction": "long",
      "size": 100,
      "entry_price": 189.50,
      "entry_time": "09:15",
      "exit_price": 191.20,
      "exit_time": "11:45",
      "stop": 188.00,
      "target": 192.00,
      "realized_pnl": 170.00,
      "status": "closed"
    }
  ],
  "daily_pnl": 170.00,
  "trades_count": 1
}
```

---

## 🚀 Ready for Next Session

After EOD wrap:
- All data persisted
- Account balance updated
- New session can start fresh
- All historical data preserved in Journal

**Next session workflow:**
1. "Load Wingman" → Loads all yesterday's data
2. Market signal refreshes
3. Ready to trade

---

**This handler automates the journey from live trading → formatted journal → command center → next session.**
