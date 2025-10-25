# Trading Command Center - Complete Project Plan

## 1. System Overview

**Project Name:** AI-Powered Trading Command Center with Real-Time Intelligence Engine

**Core Vision:** Transform daily trading conversations into a persistent, intelligent command center where Wingman (AI trading partner) provides rule-based analysis, real-time signals, and automated decision support.

**Architecture Pattern:** "Matrix Upload" - Morning data collection → Processing → Wingman persona loads with full context → Real-time intelligence engine ready for trade analysis.

---

## 2. System Components

### 2.1 Command Center Dashboard
**Purpose:** Real-time operational hub for trading decisions
- **Status:** ✅ BUILT
- **Files:**
  - `Journal/COMMAND_CENTER.md` - Markdown reference guide
  - `Journal/command-center.html` - Interactive visual dashboard
- **Key Features:**
  - Account instruments display (balance, cash, YTD P/L)
  - Live market signal panel (score, tier, breadth, sentiment)
  - Key levels (ES, SPX, QQQ, BTC)
  - Today's P&L tracking
  - Active rules display
  - Trade entry template
  - Quick commands grid
- **Theme:** Dark blue/cyan military command center (#0a0e27 primary, #00d4ff accent)
- **Font Sizes:** h1 42px, panel headers 20px, text 16-15px (optimized for readability)

### 2.2 Prospecting Workflow
**Purpose:** Convert daily conversations into trading journal entries
- **Status:** ✅ BUILT
- **Files:**
  - `Research/AI/2025-10-19_SESSION_SUMMARY.md` - Daily prospecting canvas
  - `Journal/PROSPECTING_WORKFLOW.md` - Complete daily operations guide
  - `Journal/EOD_WRAP_HANDLER.md` - Automated journal generation process
- **Key Pattern:** Trade format `[TICKER] [DIRECTION] [SIZE] @ [PRICE], stop [X], target [Y]`
- **EOD Automation:** Wingman wraps session → generates journal entry → updates Command Center → logs to index → resets for next session

### 2.3 Weekly Planner System
**Purpose:** Structured preparation ritual (Sundays, ~40 minutes)
- **Status:** ✅ BUILT
- **Files:**
  - `Journal/SUNDAY_WEEKLY_PLANNER.md` - Complete ritual with 5 phases
  - `Research/AI/2025-10-19_WEEKLY_METRICS.md` - Example metrics collection
- **Phases:**
  1. Context Load (5 min) - Verify master plan, load dashboard
  2. Metrics Collection (10 min) - Signal, sentiment, breadth, portfolio health
  3. Weekly Planning (15 min) - Economic calendar, setup, triggers, risk mgmt
  4. Daily Prep Templates (Mon-Fri) - Individual day setup
  5. Execution Checklist
- **Output:** Trigger stack with probability scoring (3 setups per week)

### 2.4 Daily Planner System
**Purpose:** Daily execution plan derived from weekly foundation
- **Status:** ✅ BUILT (template created)
- **Files:**
  - `Journal/DAILY_PLANNER_TEMPLATE.md` - Template structure
  - `Research/AI/[DATE]_DAILY_METRICS.md` - Created fresh each trading day
- **Data Flow:** Weekly metrics → filter to today's priorities → daily execution plan
- **Key Sections:** Market signal, priorities, key levels, risk mgmt, checklist, trade log

### 2.5 Dashboard Integration (Planners Tab)
**Purpose:** Display weekly + daily plans in research-dashboard.html
- **Status:** ⏳ PENDING
- **Files:**
  - `master-plan/research-dashboard.html` - Needs "Planners" tab renovation
- **Requirements:**
  - Rename "Daily Planner" tab to "Planners"
  - Add Weekly Planner section (reads `Research/AI/[WEEK]_WEEKLY_METRICS.md`)
  - Add Daily Planner section (reads `Research/AI/[DATE]_DAILY_METRICS.md`)
  - Implement markdown file binding for auto-load

### 2.6 Trading Rules System
**Purpose:** Centralized rule repository for trade decision-making
- **Status:** ❌ NOT BUILT
- **Target Location:** `Toolbox/Rules/`
- **Files to Create:**
  - `CMT_Level_2_TA_Rules.md` - Technical analysis standards (chart patterns, trend, momentum, volume, support/resistance)
  - `Seasonality_Database.md` - Yearly, presidential, decadal, monthly, weekly patterns
  - `Probability_Scoring_Framework.md` - Weighting: 40% TA, 25% market context, 15% sentiment, 10% volume, 10% seasonality
  - `Risk_Management_Rules.md` - Position sizing, stop logic, R:R requirements, account protection
- **Integration:** Loaded into Wingman persona at session start

### 2.7 Real-Time Analysis Engine
**Purpose:** Instant ticker analysis with CMT rules, sentiment, and probability scoring
- **Status:** ❌ NOT BUILT
- **Target Location:** `scripts/trading/`
- **Implementation:**
  - **Input:** Ticker symbol (e.g., "NVDA")
  - **Process:**
    1. Fetch live price (Yahoo Finance API)
    2. Pull SPY/QQQ context (breadth, correlation from master plan)
    3. Check X sentiment (loaded from morning scrape)
    4. Apply CMT TA rules
    5. Web search for catalysts/news
    6. Calculate probability score (weighted formula)
  - **Output:** BUY/WAIT/AVOID + thesis + entry/stop/target
  - **Integration:** Callable from Wingman persona

### 2.8 Wingman Persona System
**Purpose:** AI trading partner with full market context loaded
- **Status:** ⏳ PARTIAL (persona exists, Matrix upload not implemented)
- **Matrix Upload Contents:**
  - `account_state.json` (balance, positions, YTD)
  - `.session_state.json` (active rules)
  - `master-plan/master-plan.md` (today's signal analysis)
  - `master-plan/research-dashboard.html` (current metrics)
  - `Research/AI/[WEEK]_WEEKLY_METRICS.md` (weekly plan)
  - `Research/AI/[DATE]_DAILY_METRICS.md` (daily plan)
  - `Toolbox/Rules/CMT_Level_2_TA_Rules.md` (TA rules)
  - `Toolbox/Rules/Seasonality_Database.md` (patterns)
  - `Toolbox/Rules/Probability_Scoring_Framework.md` (weights)
  - Latest X sentiment data
  - Provider consensus narratives
- **Load Trigger:** "Load Wingman" command at session start
- **Verification:** "✓ Full context ingested. Ready to analyze tickers."

---

## 3. Data Flow Architecture

### 3.1 Morning Ritual (Complete Sequence)

```
Step 1: Data Collection
├─ Run: @Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt
├─ Collects: X sentiment, RSS feeds, YouTube transcripts, web search
└─ Output: Raw intelligence data

Step 2: Data Processing & Dashboard Update
├─ Run: @Toolbox/INSTRUCTIONS/Workflows/How_to_use_MP_CLAUDE_ONLY.txt
├─ Processes: Raw data + AI interpretation
├─ Updates: master-plan/master-plan.md (signal analysis)
└─ Updates: master-plan/research-dashboard.html (all metrics)

Step 3: Matrix Upload (Wingman Persona Load)
├─ Command: "Load Wingman"
├─ Ingests: All data files + rules + account state
├─ Indexes: CMT rules, seasonality data, probability weights
├─ Caches: X sentiment, master plan metrics
└─ Confirms: "✓ Full context ingested. Ready to analyze tickers."

Step 4: Real-Time Trading Intelligence
├─ User Input: "What about NVDA here?"
├─ Wingman Process:
│  ├─ Fetches: Live price (Yahoo Finance)
│  ├─ References: SPY/QQQ context (loaded master plan)
│  ├─ Applies: CMT TA rules (loaded from Toolbox/Rules/)
│  ├─ Checks: X sentiment (loaded from morning scrape)
│  ├─ Searches: News/catalysts (web search)
│  └─ Calculates: Probability score (weighted formula)
└─ Output: BUY/WAIT/AVOID + thesis + levels
```

### 3.2 Daily Trading Workflow

```
Morning (Pre-Market)
├─ Run morning ritual (steps 1-3 above)
├─ Load daily plan: Research/AI/[DATE]_DAILY_METRICS.md
└─ Review: Today's 3 priorities from weekly stack

During Market Hours
├─ Monitor: Market signal, key levels, economic calendar
├─ Execute: Trade ideas → log to session summary
├─ Each trade:
│  ├─ Format: [TICKER] [DIRECTION] [SIZE] @ [PRICE], stop [X], target [Y]
│  ├─ Wingman: Threat assessment → confirmation → execution → P&L tracking
│  └─ Record: To Research/AI/2025-10-19_SESSION_SUMMARY.md
└─ Adjust: Rules compliance, risk management

End of Day (EOD)
├─ User: "eod wrap"
├─ Wingman:
│  ├─ Collects: All session data + trades
│  ├─ Generates: Journal entry (formatted)
│  ├─ Updates: Journal/Journal.md (append entry)
│  ├─ Updates: Command Center (reset for next session)
│  ├─ Logs: To index
│  └─ Resets: .session_state.json for next day
└─ Ready: For next session
```

### 3.3 Weekly Ritual (Sundays)

```
Sunday Morning (~40 minutes)
├─ Phase 1: Context Load (5 min)
│  ├─ Verify: Master plan workflow run
│  ├─ Load: master-plan.md + research-dashboard.html
│  └─ Review: Week context
├─ Phase 2: Metrics Collection (10 min)
│  ├─ Signal progression (trend: rising/stable/falling/volatile)
│  ├─ Sentiment analysis (bullish/neutral/bearish)
│  ├─ Market structure (breadth, VIX, divergences)
│  ├─ Portfolio health (cash %, YTD, constraints)
│  └─ Provider consensus (major narratives)
├─ Phase 3: Weekly Planning (15 min)
│  ├─ Economic calendar (key events this week)
│  ├─ Setup identification (3 trading ideas)
│  ├─ Trigger stack (entry, stop, target, R:R, probability)
│  ├─ Risk management (position sizing, max loss)
│  └─ Rules compliance (verify active rules)
├─ Phase 4: Daily Prep Templates (5 min)
│  └─ Create Mon-Fri daily planner templates
└─ Phase 5: Execution Checklist (5 min)
   └─ Verify all components ready for Monday

Output: Research/AI/[WEEK]_WEEKLY_METRICS.md (saved for daily reference)
```

---

## 4. File Structure

```
Investing/
├── Toolbox/
│   ├── Rules/                          [TO BUILD]
│   │   ├── CMT_Level_2_TA_Rules.md
│   │   ├── Seasonality_Database.md
│   │   ├── Probability_Scoring_Framework.md
│   │   └── Risk_Management_Rules.md
│   ├── INSTRUCTIONS/
│   │   ├── Research/How_to_use_Research.txt
│   │   └── Workflows/How_to_use_MP_CLAUDE_ONLY.txt
│   ├── PROJECT_PLAN.md                 [THIS FILE]
│   ├── PROJECT_CHANGELOG.md            [TO CREATE]
│   ├── IMPLEMENTATION_STATUS.md         [TO CREATE]
│   └── HANDOFF_GUIDE.md                [TO CREATE]
├── Journal/
│   ├── COMMAND_CENTER.md               [BUILT]
│   ├── command-center.html             [BUILT]
│   ├── PROSPECTING_WORKFLOW.md         [BUILT]
│   ├── EOD_WRAP_HANDLER.md             [BUILT]
│   ├── SUNDAY_WEEKLY_PLANNER.md        [BUILT]
│   ├── PLANNERS_INTEGRATION_GUIDE.md   [BUILT]
│   ├── Journal.md                      [HISTORICAL]
│   └── [DATE]_Journal_Entry.md         [DAILY OUTPUT]
├── Research/
│   ├── AI/
│   │   ├── [DATE]_SESSION_SUMMARY.md   [DAILY]
│   │   ├── [DATE]_DAILY_METRICS.md     [DAILY]
│   │   ├── [WEEK]_WEEKLY_METRICS.md    [WEEKLY - SUNDAY]
│   │   ├── DAILY_PLANNER_TEMPLATE.md   [TEMPLATE]
│   │   └── [HISTORICAL ENTRIES]
│   └── X/
│       └── [SENTIMENT DATA]
├── master-plan/
│   ├── master-plan.md                  [DAILY - UPDATED BY WORKFLOW]
│   ├── research-dashboard.html         [DAILY - UPDATED BY WORKFLOW]
│   └── [PLANNERS TAB TO BE INTEGRATED]
├── scripts/                            [TO BUILD]
│   └── trading/
│       ├── analyze_ticker.py           [REAL-TIME ANALYSIS ENGINE]
│       └── matrix_upload.py            [WINGMAN CONTEXT LOADER]
└── account_state.json                  [ACCOUNT STATE - LOADED BY WINGMAN]
```

---

## 5. Technical Specifications

### 5.1 Probability Scoring Formula

```
SCORE = (TA_WEIGHT * ta_score)
       + (CONTEXT_WEIGHT * context_score)
       + (SENTIMENT_WEIGHT * sentiment_score)
       + (VOLUME_WEIGHT * volume_score)
       + (SEASONALITY_WEIGHT * seasonality_score)

Where:
- TA_WEIGHT = 0.40 (CMT Level 2 technical analysis)
- CONTEXT_WEIGHT = 0.25 (SPY/QQQ breadth, market structure)
- SENTIMENT_WEIGHT = 0.15 (X sentiment, provider consensus)
- VOLUME_WEIGHT = 0.10 (volume profile, OI for options)
- SEASONALITY_WEIGHT = 0.10 (monthly, yearly, presidential patterns)

Output Scale: 0-100
- 0-33: AVOID (bearish setup)
- 34-66: WAIT (neutral/uncertain)
- 67-100: BUY (bullish setup)
```

### 5.2 TA Rules Framework (CMT Level 2)

**Categories:**
- Chart Patterns (head & shoulders, triangles, channels, flags)
- Trend Analysis (HMA, moving averages, trend lines)
- Momentum (RSI, MACD, divergences)
- Volume Analysis (OBV, volume profile, volume by price)
- Support/Resistance (key levels, breakout zones, pivot points)

**Standards:**
- Multiple timeframe confirmation (1hr, 4hr, daily, weekly)
- Divergence detection (bullish/bearish)
- Breadth alignment with index (SPY/QQQ relative strength)
- Seasonal correlation checking

### 5.3 Data Sources & APIs

**Live Data:**
- Yahoo Finance API (free tier - stock prices, options data)
- Alternative: AlphaVantage (if more features needed)

**Sentiment Data:**
- X scraper (owned by user, existing system)
- Manual news search (catalysts, earnings, economic events)

**Market Context:**
- Master plan file (breadth, signal, sentiment from morning scrape)
- SPY/QQQ levels (live from Yahoo Finance)
- Breadth indicators (cached from morning data)

**Seasonality:**
- Web search for historical patterns
- Stored in `Toolbox/Rules/Seasonality_Database.md`
- Patterns: Monthly averages, yearly cycles, presidential cycles, decadal patterns

### 5.4 Integration Points

**Wingman Persona Commands:**
- `Load Wingman` → Initialize Matrix upload
- `analyze [TICKER]` → Run real-time analysis engine
- `eod wrap` → Generate journal entry + update dashboard
- `rules` → Display all active CMT rules
- `signal` → Display current market signal score
- `portfolio` → Show account state + YTD metrics

**Dashboard Commands:**
- View: Command Center (operational hub)
- View: Planners (weekly + daily execution)
- View: Research Dashboard (master plan + all metrics)
- Execute: Trade entry (log to session summary)

---

## 6. Implementation Checklist

### Phase 1: ✅ COMPLETE - Dashboard & Workflow Foundation
- [x] Command Center Dashboard (HTML + Markdown)
- [x] Prospecting Workflow (session summary + EOD handler)
- [x] Sunday Weekly Planner (ritual with metrics collection)
- [x] Daily Planner Template (daily execution blueprint)
- [x] Integration Guide (architecture documentation)
- [x] Example Weekly Metrics (data structure reference)

### Phase 2: ⏳ PENDING - Rules & Real-Time Engine
- [ ] CMT Level 2 TA Rules (technical analysis standards)
- [ ] Seasonality Database (historical patterns)
- [ ] Probability Scoring Framework (weighting system)
- [ ] Risk Management Rules (position sizing, stops)
- [ ] Real-Time Analysis Engine (Python script)
- [ ] Matrix Upload System (Wingman context loader)
- [ ] Planners Tab Integration (dashboard enhancement)

### Phase 3: ⏳ PENDING - Testing & Refinement
- [ ] Unit tests for probability scoring formula
- [ ] Integration tests for real-time engine
- [ ] Manual testing with live tickers
- [ ] Dashboard responsiveness verification
- [ ] Rule application verification on sample trades
- [ ] Performance testing (API response times)

---

## 7. Success Criteria

✅ **System is production-ready when:**
1. All Phase 1 files created and validated (DONE)
2. Rules system built and indexed (PENDING)
3. Real-time analysis engine returns accurate scores (PENDING)
4. Matrix upload loads all context into Wingman (PENDING)
5. Dashboard Planners tab displays weekly/daily metrics (PENDING)
6. Manual testing confirms all workflows function (PENDING)
7. Handoff documentation complete and verified (IN PROGRESS)

---

## 8. Technical Notes

- **Architecture Pattern:** Command Center (hub) → Workflows (automation) → Rules Engine (decision support) → Wingman (intelligence layer)
- **Data Persistence:** All state stored in markdown files (human-readable, git-friendly)
- **Real-Time Updates:** Dashboard refreshes from master-plan files (updated by morning ritual)
- **Context Preservation:** Matrix upload ensures LLM context never drifts from established rules
- **Error Handling:** All file reads/writes validated; missing files generate clear error messages
- **Scalability:** System designed to handle multiple trade ideas simultaneously; can expand ticker universe

---

## 9. Dependencies & Prerequisites

- Python 3.8+ (for real-time analysis engine)
- Yahoo Finance API (free tier access)
- X sentiment scraper (existing user system)
- Master plan workflow automation (existing user system)
- Markdown parsing library (Python markdown module)
- Git repository (recommended for version control)

---

## 10. Future Enhancements

- Options analysis integration (IV rank, put/call ratios, OI concentration)
- Backtesting framework (validate CMT rules against historical data)
- Trade journaling with post-trade analysis
- Machine learning probability weighting (trained on user's historical trades)
- Multi-timeframe analysis automation
- Alert system for key level breaks
- Portfolio risk management automation (heat maps, correlation analysis)
