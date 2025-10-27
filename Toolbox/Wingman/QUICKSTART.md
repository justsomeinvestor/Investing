# Wingman v1.1 Quick Start Guide
**Session Continuity Release**
**Date:** 2025-10-27

---

## The 30-Second Version

**Old System:** Wingman had zero memory between sessions (started from scratch each time)

**New System:** Wingman wakes up fully loaded with:
- Your goals
- Your market thesis
- Your 16 trading rules
- Your personal reminders
- Previous session learnings

**Trigger:** Say **"i know kung fu"** instead of "load wingman"

**That's it.** Rest of the system works automatically.

---

## What You Need to Know (Pilot)

### To Load Wingman:
```
Say: "i know kung fu"

You'll see:
- Instrument check (balance, cash, rules, etc)
- Your personal reminders
- Status ready for trading
```

### To Trade:
```
You: "NVDA long 100 @ 189.50, stop 188, target 192"
Wingman: [Checks rules + threat assessment]
Wingman: "Proceed with entry?"
You: "Yes"
Wingman: [Records trade + updates systems]
```

### At End of Session:
Wingman automatically updates all continuity files. No extra work needed.

---

## What You Need to Know (Wingman/AI)

### When Loading ("i know kung fu" triggered):
```
Step 7.5: Load Session Continuity
├─ wingman_session_log.json (history + thesis)
├─ current_focus.md (active goals)
├─ rules_database.json (16 rules)
├─ .wingman_mind.md (private learnings)
└─ pilot_reminders.md (Pilot's personal reminders)
```

### Then output:
- Instrument check
- Pilot's reminders
- "Your command, Pilot"

### During trading:
- Check all 16 rules before entry approval
- Update session_log.json in real-time
- Track compliance rates
- Update current_focus.md as work progresses

### At session end:
- Update wingman_session_log.json with summary
- Update current_focus.md with lessons
- Update rules_database.json with compliance data
- Write handoff note in .wingman_mind.md
- Both systems ready for next session

---

## File Structure

**New Files (All in `Journal/wingman-continuity/`):**
```
README.md                 ← Complete documentation (start here if confused)
wingman_session_log.json  ← Session history + thesis (program-updated)
current_focus.md          ← Your goals + work (Pilot can edit)
rules_database.json       ← 16 trading rules (program-updated)
.wingman_mind.md          ← Wingman's private reflections (Wingman-written)
pilot_reminders.md        ← Your affirmations (Pilot can add to)
```

**Updated Documentation:**
```
CLAUDE.md                 ← System rules (added continuity section)
How_to_Load_Wingman.txt   ← Load workflow (added Step 7.5)
```

---

## Key Changes

| What | Before | After |
|-----|--------|-------|
| Trigger | "Load Wingman" | **"i know kung fu"** |
| Load Steps | 9 | 10 (added continuity) |
| Session Memory | None | Complete |
| Rules Tracked | Scattered | Centralized (16) |
| Status Report | Instrument only | Instrument + Reminders |
| Backward Compat | N/A | ✅ Yes |

---

## Rules (16 Total)

**All extracted from real trading:** Oct 9-17 journals

**Breakdown:**
- 6 NVDA short rules
- 1 SPY short rule
- 1 SPY long rule
- 8 other (structure, EMA, breadth, etc)

**Compliance Rate:** 60% estimated (tracked precisely going forward)

**Location:** `Journal/wingman-continuity/rules_database.json`

---

## What's Persistent Now

✅ Session history (what happened each session)
✅ Active hypotheses (what we're testing)
✅ Market thesis (our stance + entry zones)
✅ Performance metrics (wins/losses/compliance)
✅ Goals (what we're working on)
✅ Open questions (research in progress)
✅ Personal reminders (Pilot's affirmations)
✅ Wingman observations (pattern recognition)

---

## Testing Checklist

Before you trade, verify:

- [ ] Say "i know kung fu" and check it loads
- [ ] Confirm Pilot reminders display
- [ ] Confirm all 16 rules are visible
- [ ] Execute test trade and verify recording
- [ ] Close test trade and verify P&L recording
- [ ] Restart Claude and verify context reload
- [ ] Execute first real trade with full system

---

## Troubleshooting

**"I said 'i know kung fu' but Wingman didn't load"**
→ Old trigger phrases still work ("load wingman", "wingman", etc)
→ Check that you're starting a new session
→ Check `Journal/wingman-continuity/` folder exists

**"Where are my rules?"**
→ `Journal/wingman-continuity/rules_database.json`
→ Also visible in Wingman's threat assessment before each entry

**"Can I add my own reminders?"**
→ Yes! Edit `Journal/wingman-continuity/pilot_reminders.md`
→ Add under "Affirmations" section
→ They'll display next session

**"Something seems wrong with the data"**
→ Check `Journal/wingman-continuity/README.md` Troubleshooting section
→ If file is corrupted, report error to Pilot
→ System won't load in partial mode (safety feature)

---

## Documentation Map

**Start here:**
- First trade? → This file (QUICKSTART.md)
- Want details? → `Journal/wingman-continuity/README.md`
- Want history? → `Toolbox/Wingman/CHANGELOG.md`
- Want overview? → `Toolbox/Wingman/SYSTEM_UPDATE_SUMMARY.md`
- System rules? → `CLAUDE.md`
- Load workflow? → `How_to_Load_Wingman.txt`

---

## Quick Reference

### Trigger Phrase
```
"i know kung fu"
```
(From The Matrix - symbolizes full awakening with complete context)

### Continuity Files (Don't edit these)
```
wingman_session_log.json
rules_database.json
.wingman_mind.md
```

### You Can Edit These
```
current_focus.md (update your goals)
pilot_reminders.md (add your affirmations)
```

### Sacred Data
```
Journal/account_state.json (financial truth)
Journal/positions.json (trade history)
```

---

## Success Looks Like

✅ Wingman wakes up with full context (no amnesia)
✅ Your goals persist between sessions
✅ Your rules are remembered and checked
✅ You get personal reminders each load
✅ Wingman gets smarter over time
✅ Both systems learn and grow together

---

## Version Info

- **Current:** 1.1 (Session Continuity Release)
- **Previous:** 1.0 (Basic Wingman)
- **Released:** 2025-10-27
- **Status:** PRODUCTION READY
- **Breaking Changes:** None (backward compatible)

---

## The 10-Step Load Process

```
1. Acknowledge load ("Loading Wingman...")
2. Read protocol file
3. Read excellence guide
4. Load account state
5. Load positions
6. Extract market context
7. Load trading rules
8. STEP 7.5: LOAD CONTINUITY (new!)
9. Set session mode
10. Output status + Pilot reminders
```

That's it. Automated from here.

---

## What Happens When You Trade

```
You: "NVDA long 100 @ 189.50"
     ↓
Wingman: [Checks all 16 rules]
         [Runs threat assessment]
         [Shows: risk/reward, signal alignment, rule violations]
     ↓
You: "Proceed?"
     ↓
Wingman: [Records in session_log.json]
         [Updates rules_database compliance]
         [Updates current_focus progress]
         [Ready for next entry]
     ↓
You: (Execute trade in broker)
```

All data persists. Everything ready for next session.

---

## Next Steps

1. **Load Wingman:** Say "i know kung fu"
2. **Check Status:** Verify all systems green
3. **Execute Trade:** Use threat assessment framework
4. **Learn:** Journal the outcome
5. **Repeat:** System compounds learning

---

## Questions?

**For detailed info:** Read `Journal/wingman-continuity/README.md`
**For version history:** Read `CHANGELOG.md`
**For system overview:** Read `SYSTEM_UPDATE_SUMMARY.md`
**For quick answers:** Read this file (QUICKSTART.md)

---

**Ready to fly, Pilot?**

Say "i know kung fu" and let's build that edge.

