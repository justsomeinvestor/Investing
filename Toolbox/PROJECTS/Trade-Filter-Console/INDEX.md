# Trade Filter Console - Project Index

## 📁 Project Location
```
Toolbox/PROJECTS/Trade-Filter-Console/
```

## 🎯 Quick Navigation

### 🚀 Getting Started
1. **First Time?** → Start with [README.md](README.md)
2. **Ready to Use?** → Follow [USAGE_GUIDE.md](USAGE_GUIDE.md)
3. **Want to See It in Action?** → Study [Test_Scenario_Example.md](Test_Scenario_Example.md)

### 🔧 Technical Details
4. **How Does It Work?** → Read [Documentation/ARCHITECTURE.md](Documentation/ARCHITECTURE.md)
5. **What Files Are Where?** → See [FILE_STRUCTURE.md](Documentation/FILE_STRUCTURE.md) (below)
6. **How Does It Integrate?** → Check [Documentation/PROTOCOL_INTEGRATION.md](Documentation/PROTOCOL_INTEGRATION.md)

### 📊 The Console Files
- **Dashboard:** `trade-console.html` - Open this in browser
- **Data:** `live_assessment.json` - Lives in Journal/ folder
- **Backup:** `live_assessment.json` - Template copy in this project folder

---

## 📋 Files in This Project

### Core Files
| File | Purpose | Action |
|------|---------|--------|
| `trade-console.html` | Visual dashboard | **Open in browser** |
| `live_assessment.json` | Data template | Reference only |
| `Test_Scenario_Example.md` | Full SPY example walkthrough | **Read first time** |

### Documentation
| File | Purpose | Read When |
|------|---------|-----------|
| `README.md` | Complete overview | You want full context |
| `USAGE_GUIDE.md` | Step-by-step instructions | You're using it live |
| `INDEX.md` | This file - navigation | You're lost |

### Technical (in Documentation/ folder)
| File | Purpose | Read When |
|------|---------|-----------|
| `ARCHITECTURE.md` | How everything works | You're debugging |
| `PROTOCOL_INTEGRATION.md` | Wingman integration | You're modifying |
| `DATA_SCHEMA.md` | JSON structure | You're coding |

---

## 🎯 Common Tasks

### Task 1: I want to use the console right now
1. Open: `trade-console.html` in your browser
2. Follow: [USAGE_GUIDE.md](USAGE_GUIDE.md) steps 1-6
3. Describe your trade to Wingman
4. Watch conditions light up

**Time required:** 5 minutes setup

---

### Task 2: I want to understand how it works
1. Read: [README.md](README.md) - Overview
2. Read: [Test_Scenario_Example.md](Test_Scenario_Example.md) - Real example
3. Read: [Documentation/ARCHITECTURE.md](Documentation/ARCHITECTURE.md) - Technical

**Time required:** 20 minutes

---

### Task 3: I want to modify the console design
1. Open: `trade-console.html` in code editor
2. Edit: `<style>` section (CSS)
3. Save and refresh browser
4. See changes immediately

**Time required:** 30 minutes (depending on changes)

---

### Task 4: I want to change the refresh rate
1. Open: `trade-console.html` in code editor
2. Find: `const REFRESH_INTERVAL = 2000`
3. Change: to desired milliseconds (e.g., 1000 = 1 second)
4. Save and reload browser

**Time required:** 2 minutes

---

### Task 5: I'm debugging an issue
1. Check: [README.md](README.md) "Troubleshooting" section
2. Check: [USAGE_GUIDE.md](USAGE_GUIDE.md) "Troubleshooting Checklist"
3. Check: Browser console (F12) for errors
4. Read: [Documentation/ARCHITECTURE.md](Documentation/ARCHITECTURE.md) for technical details

**Time required:** 10-30 minutes

---

## 🔗 Related Documentation (Outside This Folder)

### Wingman Protocol Files
- `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt` - Core Wingman behavior
- `Toolbox/INSTRUCTIONS/Domains/How_to_Load_Wingman.txt` - Loading workflow

### Trading Rules & Data
- `Journal/pre_entry_checklist.json` - Source of truth for conditions
- `Journal/live_assessment.json` - Active session data
- `Journal/wingman-continuity/rules_database.json` - All trading rules

### Reference Materials
- `Toolbox/INSTRUCTIONS/Domains/Risk_Management_Framework.txt` - Risk rules
- `Toolbox/INSTRUCTIONS/Domains/Wingman_Operational_Excellence_Guide.txt` - Wingman rules

---

## 📊 The 18 Condition Checklist

### Category 1: Technical Structure (6)
1. C+R Confirmation
2. RSI Level Check
3. 50% Fib Pullback Area
4. 127%/168% Extension Area
5. Divergence Present?
6. VWAP Extension Trigger (5b)

### Category 2: Momentum & Volume (3)
7. EMA Filter
8. Volume ≥ 1.3× Average
9. ADD Confirmation

### Category 3: Market Context (3)
10. Signal Tier ≥ MODERATE
11. Higher TF Alignment
12. Volatility Pattern

### Category 4: Fibonacci Reversion - Rule #20 (5)
13. At 127%-168% Extension?
14. Bearish Divergence Confirmed?
15. VWAP Yellow/Orange/Red Arrow?
16. 50%-61.8% Pullback Identified?
17. Hard Level Confluence Present?

### Category 5: Risk Management (1)
18. Risk Calculated ($231 max)

---

## 🚦 Signal Light Reference

| Light | Percentage | Meaning | Action |
|-------|-----------|---------|--------|
| 🔴 RED | < 70% | Not ready | Do not enter |
| 🟡 YELLOW | 70-90% | Caution | Review before entry |
| 🟢 GREEN | 100% | Ready | Clear to enter |

---

## 🎓 Learning Path

### Beginner Path (First Time Using Console)
1. Open [README.md](README.md) - 5 min read
2. Review [Test_Scenario_Example.md](Test_Scenario_Example.md) - 10 min read
3. Follow [USAGE_GUIDE.md](USAGE_GUIDE.md) - 2 min reference
4. Open `trade-console.html` in browser
5. Analyze your first trade
6. **Estimated time:** 30 minutes total

### Intermediate Path (Want to Understand Better)
1. Complete Beginner Path
2. Read [Documentation/ARCHITECTURE.md](Documentation/ARCHITECTURE.md) - 15 min
3. Use console on 10+ trades
4. Track which GREEN setups win
5. Refine your understanding based on results
6. **Estimated time:** 2-3 trading sessions

### Advanced Path (Want to Modify/Maintain)
1. Complete Intermediate Path
2. Read [Documentation/PROTOCOL_INTEGRATION.md](Documentation/PROTOCOL_INTEGRATION.md) - 20 min
3. Read [Documentation/DATA_SCHEMA.md](Documentation/DATA_SCHEMA.md) - 15 min
4. Study `trade-console.html` code
5. Make custom modifications
6. **Estimated time:** 1-2 hours

---

## 🔧 Maintenance Tasks

### Daily
- Open console at market open
- Use for trade analysis
- Console auto-resets between trades

### Weekly
- Track GREEN vs YELLOW vs RED results
- Note any setup patterns
- Check if console behavior meets expectations

### Monthly
- Review this documentation
- Check if conditions need refinement
- Plan any custom modifications

---

## 📞 Quick Reference by Use Case

### "I want to analyze a trade right now"
→ Open `trade-console.html`, follow [USAGE_GUIDE.md](USAGE_GUIDE.md)

### "I don't know what to do"
→ Read [README.md](README.md) Overview section

### "The console isn't updating"
→ See [README.md](README.md) Troubleshooting section

### "I want to understand how Wingman updates the console"
→ Read [Documentation/PROTOCOL_INTEGRATION.md](Documentation/PROTOCOL_INTEGRATION.md)

### "I want to understand the JSON format"
→ Read [Documentation/DATA_SCHEMA.md](Documentation/DATA_SCHEMA.md)

### "I want to modify the design"
→ Edit `<style>` in `trade-console.html`, see [USAGE_GUIDE.md](USAGE_GUIDE.md) Keyboard Shortcuts

### "I want to make it update faster"
→ Change `REFRESH_INTERVAL` in `trade-console.html` (see [Documentation/ARCHITECTURE.md](Documentation/ARCHITECTURE.md))

### "I want to see a real example"
→ Read [Test_Scenario_Example.md](Test_Scenario_Example.md)

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 10+ |
| Total Documentation | ~50KB |
| Total Code | ~200KB (HTML + CSS + JS) |
| Total Data | ~30KB (JSON) |
| Conditions Tracked | 18 |
| Categories | 5 |
| Setup Types | 2 (EXTENSION_SELL, PULLBACK_BUY) |
| Development Time | ~6 hours |
| Status | Production Ready |

---

## 🎯 Success Metrics

You'll know the console is working when:

1. ✅ You can open it and see all conditions
2. ✅ Wingman updates conditions as you describe trade
3. ✅ Signal light changes from RED → YELLOW → GREEN
4. ✅ GREEN LIGHT setups have higher win rate than random trades
5. ✅ You feel more confident in your entries
6. ✅ You can identify missing conditions faster
7. ✅ Your compliance improves (fewer rule violations)

---

## 📝 Document Versions

| Document | Version | Last Updated | Status |
|----------|---------|--------------|--------|
| README.md | 1.0 | 2025-10-28 | Production |
| USAGE_GUIDE.md | 1.0 | 2025-10-28 | Production |
| ARCHITECTURE.md | 1.0 | 2025-10-28 | Production |
| PROTOCOL_INTEGRATION.md | 1.0 | 2025-10-28 | Production |
| DATA_SCHEMA.md | 1.0 | 2025-10-28 | Production |
| trade-console.html | 1.0 | 2025-10-28 | Production |
| live_assessment.json | 1.0 | 2025-10-28 | Production |

---

## 🚀 Getting Help

### Step 1: Check the Docs
- Is it in this INDEX? → Check linked section
- General questions? → Read README.md
- Using it live? → Check USAGE_GUIDE.md
- Technical issue? → Check ARCHITECTURE.md

### Step 2: Common Issues
- Console not updating? → Troubleshooting section
- Don't understand? → Read Test_Scenario_Example.md
- Need different colors? → USAGE_GUIDE.md → Keyboard Shortcuts

### Step 3: Ask Wingman
- Say: "How do I use the trade filter console?"
- Wingman has full knowledge of this system
- It will guide you through any issue

---

## 📌 Pro Tips

1. **Bookmark the console:** `Toolbox/PROJECTS/Trade-Filter-Console/trade-console.html`
2. **Use second monitor:** Console on one screen, charts on other
3. **Keep it open:** Throughout your trading session
4. **Trust the checklist:** GREEN LIGHT = enter with confidence
5. **Track results:** Note which GREEN setups are winners
6. **Refine over time:** After 50+ trades, you'll see patterns
7. **Read commentary:** Wingman's notes help you learn

---

**Project Index - Trade Filter Console**
**Version:** 1.0
**Last Updated:** 2025-10-28
**Status:** Ready to Use

🚀 **You're all set. Open `trade-console.html` and start analyzing!**
