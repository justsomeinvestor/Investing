# 🎯 WINGMAN COMMAND CENTER

**Pilot & Wingman Operational Dashboard**

---

## 🚨 LIVE STATUS

### Account Instruments
```
┌─────────────────────────────────────┐
│ OPERATIONAL STATUS: READY           │
├─────────────────────────────────────┤
│ Account Balance:    $23,105.83      │
│ Available Cash:     $23,105.83 (✓)  │
│ YTD P/L:            +$3,152.57      │
│ Open Positions:     0                │
│ Alert Status:       GREEN            │
└─────────────────────────────────────┘
```

### Market Signal & Threat Level
```
┌─────────────────────────────────────┐
│ COMPOSITE SIGNAL:   43.5/100        │
│ Tier:               MODERATE ⚠️      │
├─────────────────────────────────────┤
│ Breadth:            WEAK (2.0/25)    │
│ Volatility:         ELEVATED (VIX~) │
│ Sentiment:          NEUTRAL          │
│ Deployment Ready:   ✗ (Wait signal)  │
│ Risk Posture:       CAUTIOUS         │
└─────────────────────────────────────┘
```

---

## 🎮 COMMAND INTERFACE

### Active Mission: [AWAITING ORDERS]

**Last Entry:**
- Date: 2025-10-20
- Trade: SQQQ long (defensive hedge)
- P&L: Profitable ✓
- Status: Closed

**Session Started:** 2025-10-19 19:13 UTC
**Wingman Status:** OPERATIONAL ✓

---

## 📊 MARKET INTELLIGENCE

### Key Levels (Last Updated: 2025-10-17)

**Indices:**
| Level | Value | Status |
|-------|-------|--------|
| ES | 6,650–6,700 | ⏸️ Chop Box |
| SPX Target | 6,660 | 📍 Watch |
| QQQ Resistance | 601.20 | 📍 Watch |

**Crypto:**
| Asset | Level | Status |
|-------|-------|--------|
| BTC | ~106,850 | 📍 200-DMA |
| IBIT | $59–60 | 📍 Support |

**Individual Equities:**
| Ticker | Range | Status |
|--------|-------|--------|
| NVDA | 185–192 | ⏸️ Consolidating |
| TSLA | 425–440 | ⏸️ Range |
| AAPL | 245–251 | ⏸️ Chop |
| SMH | 345.85–348.20 | 📍 Resistance |

**Commodities:**
| Asset | Level | Status |
|-------|-------|--------|
| Gold (/GC) | 4,263–4,330 | 📍 Correcting |

---

## 📋 TRADING COMMAND LOG

### Current Session: 2025-10-19

**No active trades. Ready for deployment.**

**Recent Trade History (Last 5):**
1. **SQQQ** — Long (10-20) | Profitable ✓ (Defensive hedge)
2. **SOLZ** — Long (10-17) | +$100 ✓
3. **NVDA** — Short (10-13) | -$100 ✗
4. **SPXU** — Long (10-15) | +$181 ✓
5. **SPY Short** — Via SPXU (10-14) | -$15 ✗

---

## ⚙️ ACTIVE RULES & PROTOCOLS

### Trading Rules (Enforced by Wingman)

**Rule #1: Trigger Stack Requirement**
- Status: ✅ ACTIVE (created 2025-10-14)
- Mandate: No SPY shorts without full trigger stack
- Criteria:
  - ✓ C+R confirmation required
  - ✓ Falling 200 EMA required
  - ✓ Negative breadth confirmation required
- Violation Alert: WINGMAN BLOCKS

**Rule #2: Position Sizing**
- Status: ✅ ACTIVE
- Mandate: First position max 0.25R until breadth confirms
- Violation Alert: WINGMAN BLOCKS

**Rule #3: Chop Discipline**
- Status: ✅ ACTIVE (created 2025-10-17)
- Mandate: In chop/triangle (6,650–6,700 ES box), plan fade vs. breakout criteria before entry
- Violation Alert: WINGMAN ASSESSMENT & CONFIRMATION

**Rule #4: DMA Respect**
- Status: ✅ ACTIVE (created 2025-10-17)
- Mandate: 8-DMA and 20-DMA are tactical stop/target rails in triangular structure
- Violation Alert: WINGMAN HIGHLIGHTS RISK

**Rule #5: No Early Exits on Reversals**
- Status: ✅ ACTIVE (created 2025-10-09)
- Mandate: Wait for 5-min close confirmation before panic-exiting shorts
- Violation Alert: WINGMAN REMINDS

---

## 🛡️ THREAT ASSESSMENT TEMPLATE

**[Use this before EVERY entry]**

```
THREAT ASSESSMENT — [TICKER] — [DIRECTION]

Signal Alignment:
  ├─ Market Signal: [43.5/100] → [TIER]
  ├─ Breadth: [2.0/25] → [STATUS]
  └─ Your Trade Fits: [ ] YES [ ] NO

Risk Assessment:
  ├─ Cash Available: $23,105.83 → [SUFFICIENT?]
  ├─ Position Size: [___%]
  ├─ R:R Ratio: [1:__] → [ACCEPTABLE?]
  └─ Max Risk: $[___]

Rule Compliance:
  ├─ Rule #1 (Trigger Stack): [ ] PASS [ ] FAIL
  ├─ Rule #2 (Sizing): [ ] PASS [ ] FAIL
  ├─ Rule #3 (Chop Discipline): [ ] PASS [ ] FAIL
  ├─ Rule #4 (DMA Respect): [ ] PASS [ ] FAIL
  └─ Rule #5 (Exit Discipline): [ ] PASS [ ] FAIL

Wingman Recommendation: [ ] PROCEED [ ] CAUTION [ ] HOLD

Pilot Decision: [ ] GO [ ] WAIT [ ] ABORT
```

---

## 📡 TRADE EXECUTION PROTOCOL

### Recording a Trade

**Format for Wingman:**
```
[TICKER] [DIRECTION] [SIZE] @ [ENTRY_PRICE], stop [STOP], target [TARGET]
```

**Example:**
```
NVDA long 100 @ 189.50, stop 188, target 192
```

**Wingman Response:**
1. Runs threat assessment
2. Displays R:R, signal alignment, rule check
3. Asks: "Proceed with entry?"
4. On "Yes": Records to positions.json, updates account, confirms entry

### Closing a Trade

**Format for Wingman:**
```
Out at [EXIT_PRICE]
```

**Example:**
```
Out at 191.20
```

**Wingman Response:**
1. Closes position
2. Calculates P&L
3. Updates files automatically
4. Reports: "✓ Position closed. +$[X] (+Y%). Daily: +$[Z]."

---

## 📊 SESSION ANALYTICS

### Today's P&L Summary

| Metric | Value |
|--------|-------|
| Trades Executed | 0 |
| Wins | 0 |
| Losses | 0 |
| Scratches | 0 |
| Daily Net | $0.00 |
| YTD Total | +$3,152.57 |
| Win Rate (Session) | N/A |

### Recent Week Performance

| Date | Trades | Daily P&L | Signal | Notes |
|------|--------|-----------|--------|-------|
| 10-17 | 1 | +$100 | WEAK (37) | SOLZ tactical |
| 10-15 | 1 | +$181 | MODERATE (70) | SPXU long |
| 10-14 | 1 | -$15 | WEAK (36) | SPY short attempt |
| 10-13 | 1 | -$100 | MODERATE (70) | NVDA short loss |
| 10-10 | 1 | +$240 | STRONG (81) | NVDA continuation |

---

## 🎯 TODAY'S PLAYBOOK

### Market Setup
- ES remains in **6,650–6,700 chop box**
- Signal tier: **MODERATE (43.5/100)** — Cautious bias
- Breadth weak (2.0/25) — Risk-off backdrop
- Deployment status: **HOLD** (wait for breadth >15/25 + signal >60/100)

### Pre-Market Checklist
- [ ] Load ES/SPX key opens (Y/W/M)
- [ ] Mark VWAP + active AVWAPs
- [ ] Set alerts: ES 6,632 (under), 6,651 (pivot), 6,700 (handle), 6,718–6,728 (20-DMA)
- [ ] Watch BTC vs. 200-DMA ($106,850)
- [ ] Track SMH 345.85/348.20; AAPL 245–251
- [ ] Monitor news: GILD earnings, banks headlines, China/rare-earths

### Trigger Stack (When Signal Improves)
1. **Setup Detection:** Price near key level + breadth confirmation
2. **Momentum:** Volume break + EMA alignment
3. **Confirmation:** VWAP + close above/below structure
4. **Entry:** Scale in at 0.25R first, add on confirmation
5. **Target:** Use DMA + fib extensions
6. **Stop:** 8-DMA or structure break + 1 tick

---

## 🔄 QUICK COMMANDS (Enhanced - Phase 3: Real Market Data)

### System Status & Intelligence
```
"wingman, status"              → Full system readout (account, positions, signal, data)
"wingman, signal"              → Current market signal (bullish/bearish), probability score
"wingman, rules"               → Active CMT Level 2 technical rules with base scores
"wingman, levels [TICKER]"     → Support/resistance levels from REAL cache data
"wingman, cache status"        → Data collector status (running/stopped, tickers, freshness, API usage)
"wingman, account rules"       → Position sizing limits, R:R minimums, daily loss limits
```

### Analysis & Decision Engine
```
"wingman, analyze [TICKER]"           → Full analysis: probability, entry/stop/target from REAL levels
"wingman, quick analyze [TICKER]"     → Rapid signal: just BUY/WAIT/AVOID + probability
"wingman, compare NVDA TSLA AAPL"     → Rank multiple tickers by probability (best setups first)
"wingman, analyze watchlist"          → Analyze all tracked tickers, ranked by probability
```

### Trade Operations
```
"wingman log"                                      → Activate trade logger (flexible format)
  ├─ "Opened NVDA long 100 @ 189.50, stop 188, target 192"
  ├─ "Closed SQQQ @ 14.85 for +$35"
  ├─ "Stopped out of NVDA @ 188 for -$50"
  └─ Or just describe it naturally

"NVDA long 100 @ 189.50, stop 188, target 192"   → Record entry with threat assessment
"Out at [PRICE]"                                   → Close position, logs P/L
"Stop loss hit [PRICE]"                           → Record stop loss hit
"Target hit [PRICE]"                              → Record target hit
"Partial out [SIZE] at [PRICE]"                   → Close part of position
```

### Data Freshness Verification (MISSION-CRITICAL)
```
"wingman verify"                      → Verify 100% data freshness before trading
  └─ Blocks if ANY section is stale
  └─ Returns: ✅ Safe to trade OR 🚫 HALT - stale data detected
```

### Data Collection Control (Phase 3)
```
"wingman, start collector"           → Begin background data daemon (5-min cycle, real Finnhub data)
"wingman, stop collector"            → Stop collection gracefully (cache remains fresh 5 min)
"wingman, restart collector"         → Stop and restart collection
"wingman, add ticker TSLA"           → Add custom ticker to watchlist (SPY/QQQ protected)
"wingman, remove ticker TSLA"        → Remove custom ticker (cannot remove SPY/QQQ)
"wingman, show watchlist"            → Display all tracked tickers
```

### End-of-Day Automation (FULLY AUTOMATED - 7 Steps)
```
"wingman, eod wrap"                  → Execute complete 7-step EOD automation:
                                        1. Collect session data
                                        2. Generate journal entry
                                        3. Update Command Center
                                        4. Update account state
                                        5. Finalize session summary
                                        6. Update Journal index
                                        7. Reset session state

  Optional: Add execution notes:
  "wingman, eod wrap
   Good discipline day - caught the dip with tight stop. Ready for tomorrow."
```

### Workflows & Reporting
```
"wingman, run research"              → Full research workflow: analyze all, rank by probability
"wingman, review performance [PERIOD]" → Performance analysis (today/week/month)
"Note: [YOUR TEXT]"                  → Record session notes and observations
```

### Pro Tips
```
Morning Routine:
  1. "wingman, start collector"
  2. "wingman, signal"
  3. "wingman, run research"

Before Entry:
  • "wingman, cache status" (verify fresh data)
  • "wingman, signal" (check signal > 67)
  • "wingman, levels [TICKER]" (find real S/R)

Phase 3 Real Data:
  ✓ Real prices from Finnhub API (not hardcoded)
  ✓ Real RSI/MACD/OBV calculated from actual data
  ✓ Real support/resistance from price history
  ✓ Updates every 5 minutes automatically
```

---

## 📍 HOW THIS SESSION WORKS

### Live Prospecting
1. **Discuss charts & setups** with Wingman during the day
2. **Observations logged** to `Research/AI/2025-10-19_SESSION_SUMMARY.md`
3. **Trades recorded** via: `[TICKER] long/short [SIZE] @ [PRICE], stop [X], target [Y]`
4. **Wingman runs threat assessment** before each entry
5. **Track P&L** as trades close

### End of Day
**Command:** `"wingman, eod wrap"`

**Wingman generates:**
- ✓ Detailed journal entry: `Journal/Log-Entries/2025-10-19_EOD_Wrap.md`
- ✓ Updates Command Center with today's trades
- ✓ Updates account balance & YTD P&L
- ✓ Finalizes session summary in Research/AI/
- ✓ Logs entry to Journal index
- ✓ Ready for tomorrow's session

### Next Session
**Command:** `"Load Wingman"`

Wingman loads all yesterday's data, refreshes market signal, and you're ready to trade.

---

## 📞 WINGMAN ALWAYS READY

**Session Status:** ✅ OPERATIONAL
**Last Updated:** 2025-10-19 19:13 UTC
**Data Freshness:** FRESH

**Your command, Pilot.** What's the mission?

---

*This Command Center is your operational hub. Wingman monitors, records, and enforces. You command. Let's fly.* 🚀
