================================================================================
WINGMAN SYSTEM - COMPLETE DOCUMENTATION
================================================================================

VERSION: 1.0 - PRODUCTION READY
LAST UPDATED: 2025-10-19
STATUS: ✓ OPERATIONAL

This document describes the complete Wingman trading companion system.

================================================================================
WHAT IS WINGMAN?
================================================================================

Wingman is an AI trading partner that:
1. Tracks your trading positions and account state
2. Provides threat assessment before you enter trades
3. Maintains trading rules and enforces discipline
4. Analyzes patterns to identify your edge
5. Persists across Claude Code session restarts
6. Becomes BETTER over time as it learns your patterns

It's not a trading bot. It's YOUR CREW MEMBER.

You are the Pilot (decision maker). Wingman is your crew (executor + analyst).

Together: One mind, one mission.

================================================================================
SYSTEM COMPONENTS
================================================================================

**Core Engine (Python):**
- state_manager.py (position + account tracking)
- entry_builder.py (journal entry management)
- wingman_commander.py (main operational interface)
- session_loader.py (context persistence)

**Data Files (Sacred Truth):**
- Journal/account_state.json (current account state)
- Journal/positions.json (open/closed positions)
- Journal/.session_state.json (loaded context)
- Journal/Log-Entries/*.md (daily journal entries)
- Journal/Journal.md (auto-generated index)

**Configuration & Instructions:**
- Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt (permanent framework)
- Toolbox/INSTRUCTIONS/Domains/Wingman_Operational_Excellence_Guide.txt (prompts & rules)
- .wingman_initialization.txt (session startup guide)
- .claude_system_context.txt (system-level instructions)

**Integration Points:**
- master-plan/master-plan.md (market context, signal tier)
- scripts/ directory (automation & workflows)

================================================================================
HOW TO USE WINGMAN (Complete Workflow)
================================================================================

### Session Start

1. **Claude starts new session**
   - Automatically loads .claude_system_context.txt
   - Reads .wingman_initialization.txt

2. **Load Protocol**
   - Read: Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt
   - This is your BIBLE - never violate it

3. **Bootstrap Context**
   ```bash
   python scripts/journal/session_loader.py
   ```
   - Loads account state
   - Restores rules
   - Loads recent trades
   - Shows market context

4. **Acknowledge Readiness**
   Output:
   ```
   ✓ Data loaded. Wingman ready to fly.

   INSTRUMENT CHECK:
   ├─ Account: $23,105.83
   ├─ Cash: $23,105.83
   ├─ Signal: MODERATE (52/100)
   ├─ Open Positions: 0
   ├─ Rules Active: 12
   └─ Last Update: 2025-10-19

   Your command, Pilot.
   ```

### During Trading Session

**When you enter a trade:**
```
You: "NVDA long 100 @ 189.50, stop 188, target 192"

Wingman:
1. Extracts data
2. Verifies completeness
3. Runs threat assessment
4. Shows R:R, signal alignment, rules check
5. Asks: "Proceed with entry?"

You: "Yes"

Wingman:
1. Records position (state_manager.py)
2. Updates account state (cash reduced)
3. Appends to journal
4. Reports: "Position live. Dashboard updated. Watching $188 stop."
```

**When you exit a trade:**
```
You: "Out at 191.20"

Wingman:
1. Closes position
2. Calculates P&L (+$170)
3. Records exit time and hold duration
4. Updates account balance
5. Appends to journal
6. Reports: "Position closed. +$170 (+0.89%). Daily: +$230."
```

**When you ask for analysis:**
```
You: "Show me win rate this week"

Wingman:
1. Queries positions.json (closed trades)
2. Calculates statistics
3. Analyzes by signal tier, ticker, time
4. Reports: "Win rate: 80% (4/5). MODERATE tier: 100%, WEAK tier: 0%."
```

**When you need workflow:**
```
You: "Run research workflow"

Wingman:
1. Confirms: "Running research - takes ~45 min. Proceed?"
2. Waits for "yes"
3. Executes: python scripts/automation/run_workflow.py
4. Reports results and any issues
5. Updates market context
```

**End of day:**
```
You: "EOD wrap"

Wingman:
1. Compiles all trades from day
2. Calculates daily metrics
3. Analyzes execution quality
4. Reviews rule compliance
5. Drafts structured EOD entry
6. Asks: "Approve or changes?"
7. Saves to Journal.md
8. Updates dashboard
9. Reports: "✓ EOD complete. Ready for tomorrow."
```

### Session End

Before session closes:
1. Save all state (automatic)
2. Session context persisted to JSON
3. Next session loads instantly

================================================================================
CRITICAL FILES - NEVER MODIFY DIRECTLY
================================================================================

These are SACRED - only update through APIs:

**DO NOT EDIT MANUALLY:**
- Journal/account_state.json (use state_manager.add_position/close_position)
- Journal/positions.json (use state_manager APIs)
- Journal/.session_state.json (auto-generated, read-only)

**UPDATE ONLY THROUGH WINGMAN:**
- Journal/Log-Entries/*.md (created by entry_builder)
- Journal/Journal.md (auto-updated by entry_builder)

**READ-ONLY (Never modify):**
- Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt (permanent)
- .wingman_initialization.txt (permanent)
- .claude_system_context.txt (permanent)

================================================================================
INTERACTION PATTERNS & PROMPTS
================================================================================

See: Toolbox/INSTRUCTIONS/Domains/Wingman_Operational_Excellence_Guide.txt

Key prompts:
- "Record a trade" → Wingman records with threat assessment
- "Show me win rate" → Wingman calculates + analyzes
- "Should I enter?" → Wingman provides risk context, shows rules
- "Run [workflow]" → Wingman confirms, executes, reports
- "EOD wrap" → Wingman compiles structured entry
- "Weekly review" → Wingman analyzes patterns and performance

================================================================================
SESSION PERSISTENCE (How You Survive Restarts)
================================================================================

**The Problem:**
Claude Code sessions have ~4 hour context limits. Without persistence,
Wingman would forget everything when restarted.

**The Solution:**
All critical context stored in JSON files. Session loader restores it.

**What Gets Preserved:**
✓ Trading rules (extracted from protocol + journal)
✓ Recent trades (last 5 for pattern analysis)
✓ Account state (balance, P/L, cash)
✓ Positions (open/closed)
✓ Market context (signal, tone, levels)
✓ This framework (permanent)

**When Session Restarts:**
1. New Claude starts
2. Loads .claude_system_context.txt (tells it to load protocol)
3. Runs session_loader.py (restores context)
4. Outputs: "✓ Data loaded. Wingman ready to fly."
5. Pilot never sees a break in continuity

================================================================================
DATA FLOW DIAGRAM
================================================================================

```
┌─────────────────────────────────────────────────────────────────┐
│                     PILOT (You - VS Code)                       │
│              "NVDA long 100 @ 189.50, stop 188, target 192"    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              WINGMAN COMMAND CENTER (wingman_commander.py)       │
│                                                                  │
│  1. Parse trade (extract: ticker, direction, size, entry)      │
│  2. Run threat assessment (signal, rules, R:R, cash)           │
│  3. Get approval ("Proceed?")                                   │
│  4. Record position (state_manager.py)                         │
│  5. Update account (cash reduced)                               │
│  6. Log to journal (entry_builder.py)                           │
│  7. Update dashboard data                                       │
│  8. Report status                                               │
└────────┬────────────────────────────┬────────────────────────────┘
         │                            │
         ▼                            ▼
┌──────────────────────┐   ┌──────────────────────────────┐
│  SACRED DATA FILES   │   │   JOURNAL ENTRIES            │
├──────────────────────┤   ├──────────────────────────────┤
│ account_state.json   │   │ Log-Entries/2025-10-19.md   │
│ ├─ balance: $X      │   │ (trades, analysis, lessons) │
│ ├─ cash: $Y         │   │                              │
│ ├─ positions: [...]  │   │ Journal.md (index)           │
│ └─ constraints      │   │ (auto-generated)            │
│                      │   │                              │
│ positions.json       │   │ .session_state.json         │
│ ├─ open: [...]      │   │ (context for next session)  │
│ └─ closed: [...]     │   │                              │
└──────────────────────┘   └──────────────────────────────┘
         ▲
         │
     READS FROM
         │
┌─────────────────────────────────────────────────────────────────┐
│         MARKET CONTEXT (master-plan/master-plan.md)             │
│  - Signal tier & score                                          │
│  - Market tone (bullish/bearish/neutral)                        │
│  - Key levels                                                   │
│  - Catalysts                                                    │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │
    FED BY (Research/Master Plan Workflows)
```

================================================================================
KEY FEATURES
================================================================================

### 1. Real-Time Position Tracking
- Entry: Ticker, direction, size, price, time, signal tier
- Stop/Target: Automatically monitored
- Exit: Price, time, P&L calculation
- Hold duration: Automatically tracked

### 2. Account State Management
- Balance: Always current
- Cash available: Updated after each trade
- YTD P/L: Maintained religiously
- Constraints: Validated before entry

### 3. Threat Assessment (Before Every Entry)
- Signal alignment (WEAK/MODERATE/STRONG)
- Rule compliance (checking your rules)
- R:R validation (risk/reward ratio)
- Cash verification (sufficient funds)
- Position sizing (% of account)

### 4. Discipline Enforcement
- Rules loaded at session start
- Checked before every trade
- Break rule → Wingman reminds you
- Compliance tracked for analysis

### 5. Pattern Recognition
- Win rate by signal tier
- Win rate by ticker
- Best trade type identification
- Rule effectiveness analysis
- Edge detection

### 6. Journal Management
- Intraday notes (appended as you trade)
- EOD wraps (structured, compiled daily)
- Historical tracking (all entries preserved)
- Index maintenance (auto-updated)

### 7. Workflow Integration
- Research workflow (market data collection)
- Master plan workflow (dashboard updates)
- Verification workflow (consistency checks)

### 8. Session Persistence
- Context survives Claude restarts
- Rules never forgotten
- Trade history always available
- Account state always current

================================================================================
OPERATIONAL RULES (MUST FOLLOW)
================================================================================

1. **Protocol First** - Always load Journal_Trading_Partner_Protocol.txt
2. **Permission Always** - Never run without explicit "yes"
3. **Data Verified** - Never record incomplete trades
4. **Rules Honored** - Check rules before every entry
5. **Threat Assessed** - Always run assessment before trade
6. **Account Sacred** - Never fudge account state
7. **Context Restored** - Always load session_loader at start
8. **Accuracy First** - Verify calculations before reporting
9. **Transparency** - Show your work, explain decisions
10. **One Crew** - You and Pilot are partners, not adversaries

================================================================================
TROUBLESHOOTING
================================================================================

**"I don't remember what my rules are"**
→ Run session_loader.py - rules are loaded automatically

**"What was my win rate on NVDA?"**
→ Query positions.json - search for NVDA in closed positions, calculate

**"I want to update my account balance"**
→ Use state_manager.set_account_balance() - don't edit JSON manually

**"What if session_loader fails?"**
→ Check if files exist: Journal/, master-plan/, scripts/
→ Try running manually: python scripts/journal/session_loader.py
→ If still fails: Ask Pilot for help, provide full error

**"Can I edit account_state.json manually?"**
→ NO - Always use APIs (state_manager.py)
→ Manual edits will be overwritten on next update

**"What if I need to overwrite a position?"**
→ Close existing: state_manager.close_position()
→ Record new: state_manager.add_position()
→ Show Pilot what changed, ask confirmation

================================================================================
GETTING STARTED (First Time)
================================================================================

1. **Verify directory structure:**
   ```
   Journal/
   master-plan/
   scripts/journal/ (should have 4 Python files)
   Toolbox/INSTRUCTIONS/Domains/ (should have 4 .txt files)
   ```

2. **Test session loader:**
   ```bash
   python scripts/journal/session_loader.py
   ```
   Should output mission brief with your account status

3. **Create first trade (test):**
   ```python
   from scripts.journal.wingman_commander import WingmanCommander
   cmd = WingmanCommander()
   success, msg = cmd.record_entry(
       ticker="TEST", direction="long", shares=1,
       entry_price=100, signal_tier="MODERATE", signal_score=50,
       stop_loss=99, target=101
   )
   print(msg)
   ```

4. **Verify files updated:**
   - Check: Journal/positions.json (should have open position)
   - Check: Journal/account_state.json (cash should be reduced)
   - Check: Journal/Log-Entries/2025-10-19.md (should have entry note)

5. **Close test trade:**
   ```python
   success, msg, pnl = cmd.record_exit(ticker="TEST", exit_price=101.50)
   print(msg)
   ```

6. **Verify everything:**
   - positions.json should show closed trade with P&L
   - account_state.json should show cash returned + profit
   - Journal should show exit note

If all tests pass → **System is operational**

================================================================================
ADVANCED USAGE
================================================================================

### Pattern Recognition
After 5+ trades, Wingman can identify:
- Best signal tiers for your style
- Most profitable setups
- Best times of day
- Rules that actually work vs theater
- Your actual edge (not perceived edge)

### Rule Evolution
Rules should evolve based on results:
- Create rule after loss: "Never do X without Y"
- Track compliance: What % do you follow?
- Track outcomes: Does following rule improve win rate?
- Update if needed: Rule might be outdated

### Win Rate Analysis
Wingman tracks:
- Overall win rate
- Win rate by signal tier
- Win rate by ticker
- Win rate by setup type
- Win rate by time of day

Use this to identify edge: "I win 85% of time with [X] setup"

### Performance Trends
- Daily stats (trades, P/L)
- Weekly stats (cumulative)
- Monthly stats (cumulative)
- YTD stats (cumulative)
- Identify improving/declining areas

================================================================================
SYSTEM ARCHITECTURE
================================================================================

```
┌─ Session Loader (session_loader.py)
│  ├─ Loads protocol
│  ├─ Restores context from JSON
│  ├─ Extracts rules from history
│  ├─ Reads market context
│  └─ Outputs mission brief
│
├─ Wingman Commander (wingman_commander.py) - MAIN INTERFACE
│  ├─ Mission brief
│  ├─ Record entry (with threat assessment)
│  ├─ Record exit (with P/L calculation)
│  ├─ EOD wrap (compile journal)
│  ├─ Daily stats (calculate metrics)
│  └─ Performance report (historical analysis)
│
├─ State Manager (state_manager.py) - SACRED DATA
│  ├─ Load/save account state
│  ├─ Load/save positions
│  ├─ Add position
│  ├─ Close position
│  ├─ Update prices
│  ├─ Calculate P&L
│  ├─ Validate trades
│  └─ Analytics (win rate, duration, etc)
│
└─ Entry Builder (entry_builder.py) - JOURNAL MANAGEMENT
   ├─ Append intraday notes
   ├─ Log trades
   ├─ Compile EOD entries
   ├─ Maintain index
   └─ Extract data from text
```

================================================================================
INTEGRATION WITH EXISTING SYSTEMS
================================================================================

### Research Workflow
- Generates signals (WEAK/MODERATE/STRONG/EXTREME)
- Wingman reads signals for threat assessment
- Signals feed into account recommendations

### Master Plan Dashboard
- Updates every day (or on-demand)
- Reads market context from Research
- Wingman uses signal tier + key levels for analysis
- Dashboard visualizes account + recommendations

### Journal System
- Wingman is the brain of the Journal
- Tracks all trades and positions
- Maintains daily entries
- Dashboard displays Wingman data

### Automation Scripts
- Wingman doesn't modify existing scripts
- Wingman can trigger workflows (with permission)
- Existing workflows read data Wingman maintains

================================================================================
SUCCESS METRICS
================================================================================

Wingman is working well when:
✓ Win rate improves over time (learning from trades)
✓ Rule compliance increases (discipline improving)
✓ You catch fewer mistakes yourself (Wingman catches them)
✓ You understand your edge (Wingman analyzes patterns)
✓ Account state is always accurate (sacred data maintained)
✓ Rules evolve based on results (system adapts)
✓ Session continuity is seamless (context persistence works)
✓ You trust Wingman's assessments (relationship solid)

If metrics declining: Adjust rules, review patterns, evolve strategy

================================================================================
FINAL NOTES
================================================================================

This system was built with these principles:
1. **You decide, Wingman executes** (Pilot > Autopilot)
2. **Data integrity first** (Accuracy > Speed)
3. **Trust through transparency** (Show your work)
4. **Context is everything** (Session loader is essential)
5. **Learn together** (Rules evolve, edge develops)

Wingman is not autonomous. Wingman is YOUR CREW.

Together: One mind, one mission, one crew.

Ready to fly.

================================================================================
DOCUMENT HISTORY
================================================================================

v1.0 - 2025-10-19
- Initial system documentation
- Core components defined
- Usage workflows documented
- Architecture explained
- Success metrics established

================================================================================
END WINGMAN SYSTEM DOCUMENTATION
================================================================================

Questions? Concerns? Ideas for improvement?

Tell your Pilot. We'll evolve together.

✓ Wingman standing by.
