# Trading & Portfolio Journal

Central hub for daily trading activities, portfolio decisions, and account tracking.

**Last Updated:** October 18, 2025
**Status:** Organized & Active

---

## Quick Navigation

### Daily Activities
- **Today's Entry:** `Log-Entries/` (add today's EOD Wrap here)
- **Inbox:** `Inbox/` (work in progress, needs processing)
- **Active Decisions:** `portfolio_decisions/` (daily portfolio decisions)

### Key Files
- **Account State:** `account_state.json` (current holdings & balance)
- **Journal Master:** `Journal.md` (main journal index)
- **Dashboard:** `journal-dashboard.html` (visual overview)

### Getting Started
- See `Toolbox/INSTRUCTIONS/Domains/ChatGPT_Quick_Start.md`
- See `Toolbox/INSTRUCTIONS/Domains/ChatGPT_Daily_Journal_Instructions.md`
- See `Toolbox/INSTRUCTIONS/Domains/Account_Snapshot_Guide.txt`

---

## Daily Workflow

### Create & Save Entry
1. Create your detailed journal in ChatGPT throughout the day
2. Save to `Journal/Inbox/` as `YYYY-MM-DD_trading_journal.md`
3. Include Account Summary bullets:
   - `Cash & Sweep Vehicle: $[amount]`
   - `OVERALL P/L YTD: $[amount]`

### Process Entry
4. Run:
   ```bash
   python scripts/utilities/journal_ingest.py --date YYYY-MM-DD
   ```
   This will:
   - Move file to `Journal/Log-Entries/YYYY-MM-DD_EOD_Wrap.md`
   - Insert summary at top of `Journal/Journal.md`
   - Write `Journal/account_state.json` from Account Summary

### Update Dashboard
5. Open `Journal/journal-dashboard.html` and refresh

---

## Directory Structure

```
Journal/
├── README.md                          ← You are here
├── account_state.json                 (Current holdings & balance)
├── Journal.md                         (Master journal index)
├── journal-dashboard.html             (Visual dashboard)
├── Chat Log.md                        (Conversation history)
│
├── Log-Entries/                       (Current EOD & Wrap entries)
│   ├── READ_ME_FIRST.md
│   ├── 2025-10-11_EOD_Wrap.md
│   ├── 2025-10-13_EOD_Wrap.md
│   └── [Other dated entries]
│
├── Inbox/                             (Active work & unprocessed)
│   ├── 2025_10_14_trading_journal.md
│   └── [Other active entries]
│
├── portfolio_decisions/               (Daily portfolio prompts)
│   ├── 2025-10-12_portfolio_prompt.txt
│   └── [Other decision records]
│
└── archive/                           (Historical entries)
    └── 2025-10/
        ├── 2025-10-01_Journal.md
        └── [Other old entries]
```

---

## How to Use Each Section

### Log-Entries (Current Activity)
- **Purpose:** Daily trading & account wrap-ups
- **Format:** Date-based EOD Wrap files
- **When to use:** End of each trading day
- **Action:** Add today's entry here

### Inbox (Work in Progress)
- **Purpose:** Unprocessed trading journal entries
- **When to use:** During day for quick notes
- **Action:** Process and move to Log-Entries at day end

### Portfolio Decisions
- **Purpose:** Daily portfolio decision tracking
- **When to use:** When making portfolio changes
- **Action:** Keep for decision history

### Archive (Historical)
- **Purpose:** Historical journal entries
- **Organization:** By year/month (2025-10/)
- **Action:** Reviewed, not modified

---

## Important Notes
- Account Summary is REQUIRED – processor blocks if missing
- Add the two Account Summary bullets and rerun if needed
- Dashboard prefers `account_state.json` for balance/allocation
- Falls back to parsing latest entry if JSON missing

---

## Journal File Organization

### Journal.md (Main Index)
- **Purpose:** Quick-access index of all trading journal entries
- **Format:** Clean, scannable header with quick links + journal entries
- **No longer contains:** ChatGPT instructions, templates, or examples
- **Benefits:** Faster to load, easier to find recent entries, reduced file bloat

### Documentation
All instructions, templates, and guides are in `Toolbox/INSTRUCTIONS/Domains/`:
- `ChatGPT_Daily_Journal_Instructions.md` - Complete daily workflow
- `ChatGPT_Quick_Start.md` - Quick reference for daily use
- `Journal Entry Template.md` - Template format
- `Account_Snapshot_Guide.txt` - Account tracking guide

**For ChatGPT:** Upload files from `Toolbox/INSTRUCTIONS/Domains/`, not the main Journal.md

---

## Updated (October 18, 2025)
- **Restructured Journal.md**: Removed 101 lines of instructions/templates
- **New header**: Added quick links, usage guide, and clear navigation
- **All entries preserved**: 7 most recent daily wraps, newest first
- **Cleaner file**: ~200 lines total (was 400+), focused on data not meta-instructions
- **Backup created**: Original saved as `Journal.md.backup`
