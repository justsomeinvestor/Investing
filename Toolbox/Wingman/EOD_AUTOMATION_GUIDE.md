# End-of-Day Automation Guide - Wingman System

**Date Created:** 2025-10-27
**Status:** ✅ PRODUCTION - Fully automated 7-step EOD process
**Audience:** Pilot (user) operating Wingman trading system

---

## 🎯 Quick Start: Execute EOD Wrap

At end of trading day (after markets close), simply say:

```
wingman, eod wrap

[Optional: Add your execution notes, observations, or lessons learned]
```

That's it. Wingman handles all 7 steps automatically (~30 seconds, zero manual work).

---

## 📋 The 7-Step EOD Wrap Process

When you call "wingman, eod wrap", the system executes this complete sequence:

### **Step 1: Collect Session Data**
Wingman reads all your closed positions from today and calculates:
- Total trades executed
- Realized P&L from all trades
- Win/loss count
- Daily performance metrics

### **Step 2: Generate Journal Entry**
Creates `Journal/Log-Entries/2025-10-27_EOD_Wrap.md` with:
- Trade-by-trade breakdown (entry, exit, P&L, duration)
- Account summary (balance, YTD P/L)
- Your execution review (notes you provided)
- Next session preparation section

### **Step 3: Update Command Center**
Refreshes `Journal/COMMAND_CENTER.md`:
- Account balance (latest)
- YTD P/L (cumulative)
- Today's trade count & results
- Last updated timestamp

### **Step 4: Update Account State**
Persists to `Journal/account_state.json`:
- New account balance (after today's P&L)
- Updated YTD P/L
- Data freshness mark
- Last updated date

### **Step 5: Finalize Session Summary**
Updates `Research/AI/2025-10-27_SESSION_SUMMARY.md`:
- Trades executed list
- Session statistics table
- EOD finalization timestamp

### **Step 6: Update Journal Index**
Adds today's entry to `Journal/Journal.md`:
- Newest entry at top (newest-first format)
- One-line summary with key metrics
- Link to detailed entry

### **Step 7: Reset Session State**
Prepares `.session_state.json` for next session:
- Clears open/closed position arrays
- Keeps all your rules and settings
- Preserves account balance
- Sets status to READY

---

## 💻 Command Syntax

### Basic Usage
```
wingman, eod wrap
```
Executes EOD with generic execution notes.

### With Execution Notes
```
wingman, eod wrap

Good discipline day - stayed patient during chop, only took high-probability setups.
Avoided two trades that didn't meet criteria. Ready for tomorrow.
```
Your notes get included in the journal entry for future reference.

### Expected Response
```
✓ EOD WRAP COMPLETE - 2025-10-27

Status: COMPLETE
Trades Executed: 1
Daily P&L: +$100.00
Account Balance: $23,205.83
YTD P/L: +$3,252.57

Execution Log:
  📍 STEP 1: Collecting session data...
  📍 STEP 2: Generating journal entry...
     Created: 2025-10-27_EOD_Wrap.md
  📍 STEP 3: Updating Command Center...
     Command Center updated
  📍 STEP 4: Updating account state...
     Account state saved
  📍 STEP 5: Finalizing session summary...
     Session summary finalized
  📍 STEP 6: Updating Journal index...
     Journal.md updated
  📍 STEP 7: Resetting session state...
     Session state reset for tomorrow

Journal updated. Dashboard refreshed. Ready for next session.
```

---

## 📊 What Gets Updated

| Component | File | Updates |
|-----------|------|---------|
| **Journal Entry** | `Log-Entries/2025-10-27_EOD_Wrap.md` | CREATED |
| **Command Center** | `COMMAND_CENTER.md` | Account balance, YTD, trades |
| **Account State** | `account_state.json` | Balance & YTD P/L |
| **Journal Index** | `Journal.md` | Today's summary (top) |
| **Session Summary** | `Research/AI/2025-10-27_SESSION_SUMMARY.md` | Trades & stats |
| **Session State** | `.session_state.json` | Reset for next day |

---

## 🔄 Complete Workflow: Before & After

### ❌ Before (Manual ChatGPT Workflow)
1. Chat with ChatGPT all day
2. Say "wrap it up" at end of day
3. Provide account data manually
4. Download markdown file from ChatGPT
5. Save to Journal/Inbox/
6. Run: `python scripts/utilities/journal_ingest.py --date 2025-10-27`
7. Manually edit Journal/Journal.md
8. Manually update Command Center
9. **Time: 10-15 minutes of manual work**

### ✅ After (Wingman Automation)
1. Trade with Wingman all day (trades auto-recorded)
2. Say **"wingman, eod wrap"** at end of day
3. All 7 steps execute automatically
4. **Time: ~30 seconds, zero manual work**

---

## 📁 File Locations & What They Contain

### Trading Journal
- **Location:** `Journal/Log-Entries/2025-10-27_EOD_Wrap.md`
- **Content:** Complete daily journal with trades, P&L, execution notes
- **Created:** Daily during EOD wrap
- **Kept:** Permanently (historical archive)

### Command Center Dashboard
- **Location:** `Journal/COMMAND_CENTER.md`
- **Content:** Your trading HQ dashboard with current account status
- **Updated:** Daily during EOD wrap
- **Used By:** Wingman for mission briefs and status checks

### Account State (Truth File)
- **Location:** `Journal/account_state.json`
- **Content:** Current balance, YTD P/L, constraints, position allocation
- **Updated:** Daily during EOD wrap (after trades)
- **Used By:** All systems for cash validation, position sizing, P&L calc

### Positions & Trades Database
- **Location:** `Journal/positions.json`
- **Content:** Open & closed positions with entry/exit/P&L details
- **Updated:** Real-time as trades execute
- **Used By:** EOD orchestrator to calculate daily P&L

### Session State (Live Tracking)
- **Location:** `Journal/.session_state.json`
- **Content:** Current session ID, account summary, market signals, rules
- **Updated:** Real-time as trades execute + reset at EOD
- **Used By:** Wingman for threat assessment, status checks

### Journal Index
- **Location:** `Journal/Journal.md`
- **Content:** Newest-first index of all daily EOD entries (newest at top)
- **Updated:** Daily during EOD wrap
- **Used By:** Quick reference, scanning recent performance

### Session Summary
- **Location:** `Research/AI/2025-10-27_SESSION_SUMMARY.md`
- **Content:** Session context, trades, observations, statistics
- **Updated:** Real-time during session + finalized at EOD
- **Used By:** Session tracking, market intelligence

---

## ✅ Verification: How to Check It Worked

After running "wingman, eod wrap", verify these:

### ✓ Check 1: Journal Entry Created
- File exists: `Journal/Log-Entries/2025-10-27_EOD_Wrap.md`
- Contains: Today's trades with entry/exit/P&L
- Timestamp: Today's date

### ✓ Check 2: Command Center Updated
- Open: `Journal/COMMAND_CENTER.md`
- Find account section, verify:
  - Account Balance matches your broker
  - YTD P/L is correct

### ✓ Check 3: Account State Updated
- Open: `Journal/account_state.json`
- Check:
  - `total_balance` = correct amount
  - `ytd_pl` = matches account_state.json
  - `last_updated` = today's date

### ✓ Check 4: Journal Index Updated
- Open: `Journal/Journal.md`
- Top entry should be today's date with link to Log-Entries entry
- Should show today's P&L and trade count

### ✓ Check 5: Session State Reset
- Open: `Journal/.session_state.json`
- Check:
  - `status` = "READY"
  - `positions.open_count` = 0
  - `recent_trades` = empty array

All good? You're ready for tomorrow!

---

## 🚀 Common Use Cases

### Use Case 1: Good Trading Day
```
wingman, eod wrap

Strong setup execution today. Caught the SPX dip with tight stop, managed
to exit before the rebound. Rules followed perfectly. Confidence high for tomorrow.
```
→ Wingman records your wins and execution quality for pattern recognition.

### Use Case 2: Flat/Break-Even Day
```
wingman, eod wrap

Stayed disciplined - signal was weak so held cash. Avoided three tempting trades
that didn't meet trigger stack. Good risk management.
```
→ Wingman tracks your rule compliance even on no-trade days.

### Use Case 3: Loss Day
```
wingman, eod wrap

Two losses today: (1) Violated Rule #3 chop discipline - entered without close+retest.
(2) Early exit on winner - need more patience on targets. Will review playbook tomorrow.
```
→ Wingman records lessons learned and rule violations for improvement.

### Use Case 4: End of Week Review
At end of Friday:
```
wingman, eod wrap

Solid week - three green days, two flat. Best setup was the Tuesday dip catch.
Need to work on: (1) Not fading in low breadth, (2) Better position sizing
in sideways markets. Win rate 67%, P/L positive. Good week overall.
```
→ Wingman creates end-of-week summary for pattern analysis.

---

## 🔧 Technical Details

### What System Components Are Involved?

1. **EODWrapOrchestrator** (`scripts/journal/eod_wrap_automation.py`)
   - Master orchestrator that runs all 7 steps
   - Handles file I/O, data validation, error logging

2. **WingmanCommander** (`scripts/journal/wingman_commander.py`)
   - Calls the orchestrator
   - Formats the final report for you

3. **SupportingModules:**
   - `state_manager.py` - Position & account tracking
   - `entry_builder.py` - Journal entry formatting
   - (These are called by the orchestrator)

### Error Handling

If any step fails:
- ❌ Error is logged and reported
- ⚠️ Remaining steps still execute
- 📋 You get a detailed report of what failed
- ✓ You can re-run "wingman, eod wrap" to fix it

Example error handling:
```
⚠️ EOD WRAP COMPLETE - 2025-10-27 [WITH ERRORS]

Status: ERRORS ENCOUNTERED
...
Execution Log:
  📍 STEP 1: Collecting session data...
  ❌ ERROR: No trades found for 2025-10-27
  ...
```

---

## 📞 Troubleshooting

### Problem: "wingman, eod wrap" doesn't work
**Solution:** Make sure:
1. You have trades recorded in `Journal/positions.json`
2. EODWrapOrchestrator script is in `scripts/journal/`
3. Wingman system is loaded ("Load Wingman" first)

### Problem: Account balance didn't update
**Solution:**
1. Check that positions.json has closed trades for today
2. Verify account_state.json had starting balance
3. Run "wingman, eod wrap" again

### Problem: Journal entry not created
**Solution:**
1. Check `Journal/Log-Entries/` directory exists
2. Verify you have write permissions
3. Check error message in execution log

---

## 🎯 Key Takeaways

✅ **One Command:** `wingman, eod wrap` handles all 7 steps
✅ **Fully Automatic:** No manual file moving, editing, or copying
✅ **Real-Time:** All trades recorded during session
✅ **Comprehensive:** Journal, Command Center, account state, all updated
✅ **Consistent:** Same format, same process, every day
✅ **Ready for Tomorrow:** Session state reset and ready to go

---

## 📚 Related Documentation

- [EOD_WRAP_HANDLER.md](../../Journal/JBox/EOD_WRAP_HANDLER.md) - Technical details
- [COMMAND_CENTER.md](../../Journal/COMMAND_CENTER.md) - Your trading dashboard
- [How_to_Load_Wingman.txt](../INSTRUCTIONS/Domains/How_to_Load_Wingman.txt) - Wingman initialization
- [Journal_Trading_Partner_Protocol.txt](../INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt) - Wingman core rules

---

**Last Updated:** 2025-10-27
**Status:** ✅ PRODUCTION READY
**Maintained By:** Wingman (Claude Code)

