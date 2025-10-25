# Daily Journal Quick Reference

**Purpose:** Quick-access guide for end-of-day journaling workflow
**Time Commitment:** 5-10 minutes
**Created:** October 18, 2025

---

## 🚀 START HERE: End-of-Day Workflow (3 Steps)

### Step 1: Create Detailed Journal (via ChatGPT) - 3-5 min
Throughout your trading day, use ChatGPT with the Daily Journal Instructions. At EOD:
1. Say "Wrap it up" or "Generate EOD journal"
2. ChatGPT will ask for any missing data (cash balance, P/L YTD, trades, tomorrow prep)
3. Download the completed detailed journal
4. Save to `Journal/Inbox/YYYY-MM-DD_trading_journal.md`

**Reference:** [ChatGPT_Daily_Journal_Instructions.md](ChatGPT_Daily_Journal_Instructions.md)

---

### Step 2: Process & Move File - 1 min
Run the ingest script to move file to proper location:
```bash
python scripts/utilities/journal_ingest.py --date YYYY-MM-DD
```
This automatically:
- Moves file to `Journal/Log-Entries/YYYY-MM-DD_EOD_Wrap.md`
- Updates `Journal/account_state.json` with account data
- Ready for Journal.md integration

---

### Step 3: Add Summary to Journal.md - 2-3 min
The summary gets added to `Journal/Journal.md` at the TOP (newest first):

```markdown
**End of Day Review - YYYY-MM-DD (HH:MM PT)** - [Link to Detailed Journal](Log-Entries/YYYY-MM-DD_EOD_Wrap.md)

- **Market Action & Signal:** [Composite signal score, key price action, VIX, breadth]
- **Trades/P&L:** [All trades OR "No trades executed" + reason]
- **P&L / Balance:** Daily P&L **[+/-X.XX%]** or **$[amount]**
- **Account Summary:**
  - Cash & Sweep Vehicle: $XX,XXX.XX
  - OVERALL P/L YTD: $X,XXX.XX
- **Execution Review:** [What worked, mistakes, rules followed/broken, improvements]
- **Trend Watch & System Intel:** [Signal trend, narratives, breadth/vol context]
- **Tomorrow Prep:** [Key levels, catalysts, setups to stalk]
```

**Template Reference:** [Journal Entry Template.md](Journal Entry Template.md)

---

## ⏰ When to Update During Your Day

### Pre-Market (4:00-9:30 AM ET)
- Review yesterday's EOD entry in Journal.md
- Note overnight market moves
- Confirm today's setups

### Midday Check-in (11:00 AM - 1:00 PM ET)
- Log any trades taken (in ChatGPT context)
- Note if key levels triggered
- Brief status update

### End of Day (4:00-8:00 PM ET) - MANDATORY ✅
- Complete detailed journal with ChatGPT
- Run ingest script
- Add summary to Journal.md
- **Total time:** 5-10 minutes

---

## 💡 Example: Complete EOD Workflow

**5:00 PM PT - End of Trading Day:**

**With ChatGPT:** "Wrap it up for today"

**ChatGPT:** "Let me gather the required data. What is your:
1. Cash & Sweep Vehicle balance?
2. OVERALL P/L YTD?
3. Daily P&L?
4. Key levels for tomorrow?"

**You:** "Cash $23,105.83, P/L YTD $3,152.57, today +$100, watching ES 6,632-6,700"

**ChatGPT:** [Generates complete journal entry]

**5:05 PM:** Save to `Journal/Inbox/2025-10-17_trading_journal.md`

**5:06 PM:** Run:
```bash
python scripts/utilities/journal_ingest.py --date 2025-10-17
```

**5:08 PM:** File moved to `Journal/Log-Entries/2025-10-17_EOD_Wrap.md` and `account_state.json` updated

**5:10 PM:** Add summary to top of `Journal/Journal.md`:
```markdown
**End of Day Review - 2025-10-17 (17:00 PT)** - [Link to Detailed Journal](Log-Entries/2025-10-17_EOD_Wrap.md)

- **Market Action & Signal:** ES chop 6,650-6,700 box; signal 37/100 (WEAK)
- **Trades/P&L:** SOLZ tactical long +$100
- **P&L / Balance:** Daily P&L **+$100.00**
- **Account Summary:**
  - Cash & Sweep Vehicle: $23,105.83
  - OVERALL P/L YTD: $3,152.57
- **Execution Review:** Good discipline in chop, avoided overtrading
- **Trend Watch & System Intel:** Extreme breadth weakness (2/25), crypto liquidation context
- **Tomorrow Prep:** Mark ES levels: 6,632, 6,651, 6,687-6,692, 6,718-6,728
```

**Total time:** 5-7 minutes ✅

---

## ✅ Journaling Best Practices

**Do:**
- ✅ Be honest (especially about mistakes)
- ✅ Focus on process, not just P&L
- ✅ Note what you did RIGHT (reinforce wins)
- ✅ Keep entries brief (bullets, not paragraphs)
- ✅ Review weekly to spot patterns

**Don't:**
- ❌ Skip EOD entries (consistency matters)
- ❌ Write novels (use bullets only)
- ❌ Only journal losses (wins teach too)
- ❌ Blame externals (focus on controllables)
- ❌ Let journal fall behind (daily discipline)

---

## 📊 Review Schedule

**Daily (EOD):** What happened vs plan, key lesson

**Weekly (Friday PM):** Review 5 EOD entries, note patterns, update playbook

**Monthly:** Full scan, performance metrics (win rate, R multiples), rule updates

---

## 📁 File Locations Reference

| What | Where | Purpose |
|------|-------|---------|
| Daily instructions | [ChatGPT_Quick_Start.md](ChatGPT_Quick_Start.md) | Upload to ChatGPT |
| Detailed workflow | [ChatGPT_Daily_Journal_Instructions.md](ChatGPT_Daily_Journal_Instructions.md) | Complete EOD process |
| Entry template | [Journal Entry Template.md](Journal Entry Template.md) | Format reference |
| Journal index | `Journal/Journal.md` | Main summary log |
| Detailed entries | `Journal/Log-Entries/` | Full daily wraps |
| Account data | `Journal/account_state.json` | Current balance/P/L |
| Dashboard | `Journal/journal-dashboard.html` | Visual overview |

---

## 🔗 Data Flow

```
Trading Day
    ↓
ChatGPT Journal (detailed)
    ↓
Save to Inbox/
    ↓
Run journal_ingest.py
    ↓
Move to Log-Entries/ + Update account_state.json
    ↓
Add summary to Journal.md
    ↓
Dashboard reads Journal.md + account_state.json
    ↓
Visualized & Ready for Review
```

---

## ❓ Quick FAQ

**Q: Where do I upload the ChatGPT file?**
A: `Journal/Inbox/YYYY-MM-DD_trading_journal.md` - the script will move it to Log-Entries/

**Q: What if I can't get account data?**
A: Add placeholders with $0 and the script will ask you to update it. Better to have real numbers.

**Q: Do I need to manually move the file?**
A: No - `journal_ingest.py` script does it automatically

**Q: What gets parsed for the dashboard?**
A: Account Summary section (cash, P/L YTD) and Daily P&L - must use exact field names

**Q: Can I edit old entries?**
A: Yes, but keep them honest. Good for process improvements, not P&L manipulation.

**Q: When should I review patterns?**
A: Weekly is ideal, monthly at minimum. Look for recurring mistakes or winning setups.

---

## 🎯 Key Takeaways

1. **Journal is your edge** - Honest reflection builds pattern recognition
2. **Keep it brief** - Quality > Quantity (bullets, not paragraphs)
3. **Consistency matters** - Daily discipline > Perfect entries
4. **Review regularly** - Weekly to spot patterns, monthly for strategy updates
5. **Use for improvement** - Link insights back to your trading rules

---

## 📚 Need More Details?

- **How to use ChatGPT for journaling:** [ChatGPT_Daily_Journal_Instructions.md](ChatGPT_Daily_Journal_Instructions.md)
- **Quick ChatGPT reference:** [ChatGPT_Quick_Start.md](ChatGPT_Quick_Start.md)
- **Journal system overview:** [Journal/README.md](../../Journal/README.md)
- **Entry format spec:** [Journal Entry Template.md](Journal Entry Template.md)

---

**Last Updated:** October 18, 2025
**Status:** Clean, focused, actionable ✅
