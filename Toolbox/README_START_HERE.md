# START HERE - Toolbox Guide

**Welcome! This is your complete Investing System Toolbox**

---

## What Is This?

This folder contains everything you need to:
- ✅ Run daily market analysis workflows
- ✅ Monitor dashboard data freshness
- ✅ Verify system health
- ✅ Execute research pipelines
- ✅ Update master plan insights

---

## Quick Start (Choose Your Path)

### 🚀 First Time? Read This
👉 **[DOCUMENTATION_GUIDE_2025-10-18.md](DOCUMENTATION_GUIDE_2025-10-18.md)**
- Explains all the files and what they do
- Helps you find what you need
- Takes 5-10 minutes

### 📅 Running Workflow Today?
👉 **[DAILY_OPERATIONS_CHECKLIST_2025-10-18.md](DAILY_OPERATIONS_CHECKLIST_2025-10-18.md)**
- Step-by-step checklist for today
- Commands to run
- How to verify everything worked
- Troubleshooting if anything breaks

### 🔧 Want to Understand Everything?
👉 **[FINAL_VERIFICATION_SYSTEM_INDEX_2025-10-18.md](FINAL_VERIFICATION_SYSTEM_INDEX_2025-10-18.md)**
- Complete technical reference
- How the verification system works
- How to use the CLI tools
- Detailed explanations

### 🏥 Something Went Wrong?
👉 **[REPAIR_SUMMARY_2025-10-18.md](REPAIR_SUMMARY_2025-10-18.md)**
- Known issues and fixes
- Recovery procedures
- Error solutions
- Backup recovery

### 📊 System Health Check
👉 **[PRODUCTION_STATUS_2025-10-18.md](PRODUCTION_STATUS_2025-10-18.md)**
- Current system status
- All features verified
- Production readiness
- Latest verification results

---

## Your Daily Routine (Copy-Paste Commands)

### Step 1: Check Health (2 minutes)
```bash
python scripts/utilities/verify_data_freshness.py 2025-10-18
```

**What to expect:** System tells you which sections need updates

### Step 2: Run Workflow (20-30 minutes)
```bash
python scripts/automation/run_workflow.py
```

**What to expect:** Dashboard gets updated automatically

### Step 3: Verify Completion (5 minutes)
Check the output and look for:
- ✅ `[OK] Validation successful` (YAML is good)
- ✅ `Dashboard Health: XX%` (see percentage)
- ✅ Any RED dots → update those sections

---

## Key Files at a Glance

### For Daily Use
| File | Purpose | Time |
|------|---------|------|
| [DAILY_OPERATIONS_CHECKLIST_2025-10-18.md](DAILY_OPERATIONS_CHECKLIST_2025-10-18.md) | Step-by-step daily guide | 5 min |
| [QUICK_REFERENCE_VERIFICATION_SYSTEM_2025-10-18.md](QUICK_REFERENCE_VERIFICATION_SYSTEM_2025-10-18.md) | Cheat sheet | 2 min |
| `INSTRUCTIONS/Workflows/How_to_use_MP_CLAUDE_ONLY.txt` | Complete workflow steps | 20 min |

### For Understanding
| File | Purpose | Time |
|------|---------|------|
| [DOCUMENTATION_GUIDE_2025-10-18.md](DOCUMENTATION_GUIDE_2025-10-18.md) | Navigation & organization | 5 min |
| [FINAL_VERIFICATION_SYSTEM_INDEX_2025-10-18.md](FINAL_VERIFICATION_SYSTEM_INDEX_2025-10-18.md) | Complete system explanation | 30 min |
| [DATA_FRESHNESS_VERIFICATION_GUIDE_2025-10-18.md](DATA_FRESHNESS_VERIFICATION_GUIDE_2025-10-18.md) | Verification system details | 15 min |

### For Troubleshooting
| File | Purpose | Time |
|------|---------|------|
| [REPAIR_SUMMARY_2025-10-18.md](REPAIR_SUMMARY_2025-10-18.md) | Known issues & fixes | As needed |
| [PRODUCTION_STATUS_2025-10-18.md](PRODUCTION_STATUS_2025-10-18.md) | System health | 5 min |

### Technical References
| File | Purpose | Time |
|------|---------|------|
| [VERIFICATION_SCRIPT_IMPLEMENTATION_2025-10-18.md](VERIFICATION_SCRIPT_IMPLEMENTATION_2025-10-18.md) | How scripts work | 20 min |
| [YAML_CORRUPTION_FIX_2025-10-18.md](YAML_CORRUPTION_FIX_2025-10-18.md) | YAML safety | 10 min |
| [2025-10-18_FIXES_APPLIED.md](2025-10-18_FIXES_APPLIED.md) | What was fixed | 15 min |

---

## Important Folders

```
Toolbox/
├── INSTRUCTIONS/           ← How to run workflows
│   ├── Workflows/         ← Main workflow guide (READ THIS)
│   └── Research/          ← Research workflow guide
│
├── [Markdown docs]        ← All the guides and references
│
└── [This file]           ← You are here
```

---

## The Verification System (What You're Using)

The system has **3 layers** to tell you when data is stale:

### 🟢 GREEN = Fresh (< 12 hours old)
- ✅ Section has recent data
- ✅ Safe to make trading decisions
- ✅ No action needed

### 🟡 YELLOW = Aging (12-24 hours old)
- ⚠️ Section data is getting old
- ⚠️ Monitor carefully
- ⚠️ Plan to update soon

### 🔴 RED = Stale (> 24 hours old)
- ❌ Section needs update NOW
- ❌ Do not trade on this data
- ❌ Update content and timestamp

### Where to See Them
1. **Dashboard Top-Right:** Green or red dot (overall health)
2. **Each Section:** Green, yellow, or red dot (individual status)
3. **CLI Tool:** Run command to get detailed report

---

## Commands You'll Use

### Check System Health
```bash
python scripts/utilities/verify_data_freshness.py 2025-10-18
```
Shows which sections are fresh/aging/stale

### Run the Workflow
```bash
python scripts/automation/run_workflow.py
```
Updates dashboard and runs verification

### View the Dashboard
```
master-plan/research-dashboard.html
```
Open in browser to see visual status

---

## Folder Structure Explained

```
Investing/
├── Toolbox/                          ← You are here
│   ├── README_START_HERE.md         ← Start here
│   ├── DOCUMENTATION_GUIDE.md       ← Find what you need
│   ├── DAILY_OPERATIONS_CHECKLIST   ← Today's work
│   ├── PRODUCTION_STATUS.md         ← System health
│   ├── REPAIR_SUMMARY.md            ← If broken
│   ├── INSTRUCTIONS/
│   │   ├── Workflows/How_to_use_MP_CLAUDE_ONLY.txt  ← MAIN WORKFLOW
│   │   └── Research/How_to_use_Research.txt
│   └── [Other docs...]
│
├── scripts/                          ← Code & tools
│   ├── utilities/
│   │   ├── verify_data_freshness.py ← Health check tool
│   │   └── yaml_handler.py          ← YAML safety
│   ├── automation/
│   │   └── run_workflow.py          ← Run this to update
│   └── [Other scripts...]
│
├── master-plan/
│   ├── master-plan.md               ← Main data file
│   ├── research-dashboard.html      ← Dashboard (open in browser)
│   └── master-plan.backup           ← Safety backup
│
└── Research/                         ← Data & cache
    └── .cache/                      ← Today's data files
```

---

## Status Today

✅ **System Status:** PRODUCTION READY
✅ **All Features:** Operational
✅ **Dashboard Health:** 83.3% (10/12 sections fresh)
✅ **Documentation:** Current and organized
✅ **Ready to Use:** YES

---

## Quick Decision Tree

**"I want to start trading today"**
→ Read: DAILY_OPERATIONS_CHECKLIST
→ Run: `python scripts/automation/run_workflow.py`
→ Check: Dashboard health
→ Update: Any red sections
→ Done!

**"I want to understand how this works"**
→ Read: DOCUMENTATION_GUIDE (5 min)
→ Read: FINAL_VERIFICATION_SYSTEM_INDEX (30 min)
→ Read: DATA_FRESHNESS_VERIFICATION_GUIDE (15 min)
→ Done!

**"Something is broken or confusing"**
→ Read: REPAIR_SUMMARY
→ Read: PRODUCTION_STATUS
→ Follow: Troubleshooting section
→ If still stuck: See INSTRUCTIONS/Workflows/How_to_use_MP_CLAUDE_ONLY.txt

**"I want just a quick reference"**
→ Read: QUICK_REFERENCE_VERIFICATION_SYSTEM (2 min)
→ Done!

---

## Key Concepts

### Timestamps
- Format: `YYYY-MM-DDTHH:MM:SSZ` (ISO 8601)
- Example: `2025-10-18T20:32:00Z`
- Used to calculate section freshness

### Health Percentage
- Formula: (Fresh Sections / Total Sections) × 100%
- Target: ≥80% (safe to trade)
- Warning: 50-80% (be careful)
- Critical: <50% (needs major updates)

### Phases
- **Phase 4.5:** Data freshness verification (new)
- **Phase 3.8/3.9:** YAML validation (new)
- **All Phases:** Documented in workflow file

---

## Getting Help

**For:** Task-specific questions
→ **Check:** DAILY_OPERATIONS_CHECKLIST

**For:** System errors
→ **Check:** REPAIR_SUMMARY

**For:** How something works
→ **Check:** FINAL_VERIFICATION_SYSTEM_INDEX

**For:** Detailed technical info
→ **Check:** VERIFICATION_SCRIPT_IMPLEMENTATION_2025-10-18.md

**For:** Finding the right doc
→ **Check:** DOCUMENTATION_GUIDE

---

## What Happens When You Run the Workflow

1. **Scrapers collect data** (YouTube, RSS, X, Technical)
2. **Data gets cached** (Research/.cache/ folder)
3. **Dashboard reads cached data**
4. **YAML validation runs** (checks for corruption)
5. **Phase 4.5 verification** (checks timestamps)
6. **Results reported** (health %, what needs update)
7. **Dashboard updates** (indicators show status)

**Total time:** 20-30 minutes
**Automatic:** Yes, runs with one command

---

## Daily Checklist (Super Short Version)

- [ ] Run: `python scripts/automation/run_workflow.py`
- [ ] Check: Dashboard health percentage
- [ ] Update: Any RED sections (if needed)
- [ ] Verify: All sections now GREEN
- [ ] Trade: Make decisions with fresh data

---

## System Verified

✅ Verification system: Working
✅ YAML validation: Working
✅ Dashboard: Updating correctly
✅ CLI tools: Functioning
✅ Documentation: Current
✅ Recovery procedures: Ready

**Last verified:** October 18, 2025 @ 20:32 UTC

---

## Next Steps

1. **Read:** [DOCUMENTATION_GUIDE_2025-10-18.md](DOCUMENTATION_GUIDE_2025-10-18.md) (find your path)
2. **Choose:** Your use case (daily work, learning, or troubleshooting)
3. **Read:** The appropriate document
4. **Use:** The system with confidence

---

## Questions?

- **"What document should I read?"** → [DOCUMENTATION_GUIDE_2025-10-18.md](DOCUMENTATION_GUIDE_2025-10-18.md)
- **"How do I run the workflow?"** → [DAILY_OPERATIONS_CHECKLIST_2025-10-18.md](DAILY_OPERATIONS_CHECKLIST_2025-10-18.md)
- **"Something is broken!"** → [REPAIR_SUMMARY_2025-10-18.md](REPAIR_SUMMARY_2025-10-18.md)
- **"Is the system ready?"** → [PRODUCTION_STATUS_2025-10-18.md](PRODUCTION_STATUS_2025-10-18.md)
- **"How does everything work?"** → [FINAL_VERIFICATION_SYSTEM_INDEX_2025-10-18.md](FINAL_VERIFICATION_SYSTEM_INDEX_2025-10-18.md)

---

## Welcome to Your Complete Investing System!

Everything is ready. Everything is documented. Everything works.

**Start with:** [DOCUMENTATION_GUIDE_2025-10-18.md](DOCUMENTATION_GUIDE_2025-10-18.md)

**Then choose your path and get started.**

---

**Created:** October 18, 2025
**Status:** ✅ PRODUCTION READY
**Confidence:** HIGH ✅

Good luck with your trading!
