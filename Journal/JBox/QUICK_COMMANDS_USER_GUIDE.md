# ⚡ Quick Commands User Guide

**Purpose:** Fast reference for all available commands to maximize Command Center functionality
**Audience:** Traders using Wingman Command Center
**Last Updated:** October 19, 2025

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Trading Commands](#trading-commands)
3. [Journal & Analysis Commands](#journal--analysis-commands)
4. [Research & Market Commands](#research--market-commands)
5. [System Commands](#system-commands)
6. [Advanced Workflows](#advanced-workflows)

---

## Getting Started

### Quick Commands Panel Location
- **Where:** Bottom of Command Center page
- **How to access:** Scroll down past dashboard panels
- **Layout:** Collapsible grid of clickable command cards
- **Expand/Collapse:** Click the "⚡ Quick Commands" header to toggle visibility

### Command Input Methods

**Method 1: Click a Quick Command Card**
```
1. Scroll to Quick Commands section
2. Click any command card (e.g., "wingman, status")
3. Command executes immediately
```

**Method 2: Type to Claude During Day**
```
1. Tell Claude the command naturally
2. Example: "What's my win rate?"
3. Claude executes and responds
```

**Method 3: Via Chat with Claude**
```
1. Say: "run the analysis workflow"
2. Or: "give me today's journal insights"
3. Claude knows the command patterns
```

---

## 🎯 Trading Commands

### Command: "analyze [TICKER]"

**What it does:**
Runs the decision engine on any ticker and displays full analysis in the Analyzer panel

**Usage:**
```
"analyze SPY"
"analyze NVDA"
"analyze TSLA"
```

**Output:**
- Signal (BUY/WAIT/AVOID)
- Probability score (0-100%)
- 5 component scores (TA, Context, Sentiment, Volume, Seasonality)
- Trade levels (Entry/Stop/Target/R:R)
- Position sizing recommendation
- Reasoning text

**When to use:**
- Before entering a trade (quick signal check)
- During the day (market change confirmation)
- End of day (wrap-up review)

**Example:**
```
You: "analyze SPY"
Display shows:
  Signal: BUY at 71.5%
  Entry: $585.50
  Stop: $583.25
  Target: $591.75
  R:R: 1:2.1
```

---

### Command: "entry [TICKER] [DIRECTION] @ [PRICE]"

**What it does:**
Logs a trade entry with automatic timestamp and stores in live session journal

**Usage:**
```
"entry NVDA long @ 189.50"
"entry SPY short @ 665.00"
"entry QQQ long @ 601.25"
```

**Logged Data:**
- Ticker and direction
- Entry price
- Entry time (automatic)
- Stored in: `Journal/LIVE_SESSION_YYYY-MM-DD.md`

**When to use:**
- Immediately after entering a trade
- Keep a real-time record of all entries

**Example:**
```
You: "entry NVDA long @ 189.50"
Claude: ✓ Logged - NVDA long at 189.50 (10:35 ET)
Appears in Live Session tab
```

---

### Command: "exit [TICKER] @ [PRICE] for [PNL]"

**What it does:**
Logs the exit with P&L, completes trade record in journal

**Usage:**
```
"exit NVDA @ 191.20 for +$145"
"exit SPY @ 663.75 for +$125"
"exit QQQ @ 598.50 for -$75"
```

**Logged Data:**
- Exit price
- P&L (profit/loss)
- Exit time (automatic)
- Win/loss categorization (automatic)
- Stored in: `Journal/LIVE_SESSION_YYYY-MM-DD.md`

**When to use:**
- When you exit a position
- Records complete trade for analysis

**Example:**
```
You: "exit NVDA @ 191.20 for +$145"
Claude: ✓ Logged - NVDA closed at 191.20
  Entry: $189.50
  Exit: $191.20
  P&L: +$145 ✓
  Time: 45 minutes
```

---

### Command: "position [STATUS]"

**What it does:**
Updates current position status in live journal

**Usage:**
```
"position up $450 on day"
"position down $100 YTD"
"position flat, waiting for setup"
"position: 1 trade active, 2 pending"
```

**Logged Data:**
- Current P&L status
- Number of open positions
- Overall account status
- Time logged (automatic)

**When to use:**
- Mid-day check-in
- When positions change
- End of day before wrap-up

---

### Command: "setup [SETUP_NAME]"

**What it does:**
Notes a potential setup or trade idea for later

**Usage:**
```
"setup: SPY rejection at 665 resistance"
"setup: NVDA double bottom at 188-189"
"setup: QQQ breakout above 603"
"setup: BTC consolidation pattern"
```

**Logged Data:**
- Setup description
- Ticker if mentioned
- Time noted (automatic)
- Stored for later reference

**When to use:**
- When you spot a setup but can't trade yet
- To track pattern recognition
- Build playbook examples

---

## 📓 Journal & Analysis Commands

### Command: "analyze my journal"

**What it does:**
Runs the complete analysis workflow on all your trading data

**Usage:**
```
"analyze my journal"
"run journal analysis"
"give me my insights"
```

**Execution Steps (Automatic):**
1. Analyzes all historical entries (Log-Entries/*.md)
2. Extracts trade patterns, win rates, setups
3. Identifies recurring mistakes
4. Generates AI coaching feedback
5. Updates Command Center Journal Analytics

**Output:**
- `journal_trends.json` - Statistics and patterns
- `daily_feedback.md` - AI coaching insights
- Command Center updates:
  - Live Session tab: Today's trades
  - Trends tab: Win rate charts, best setups
  - AI Feedback tab: Coaching insights
  - Trade Log tab: Searchable history

**When to use:**
- End of each trading day
- Weekly review (see weekly summary)
- When you want insights on performance

**Example Output:**
```
✅ Analysis Complete

📊 TODAY'S SUMMARY:
- Trades: 3
- Wins: 2 / Losses: 1
- Win Rate: 67% (vs 72% baseline)
- Total P&L: +$370

🤖 AI COACHING:
✓ Good: Waited for confirmation on entries
⚠️ Watch: Sized too big on trade #2
💡 Insight: Your best setup (support bounces) appeared today - you nailed it

📈 THIS WEEK:
- Best Setup: Support Bounces (78.5% WR)
- Worst Hour: 2-3 PM (45% WR)
- Most Common Mistake: "chased breakout" (4 times)
```

---

### Command: "what's my best setup?"

**What it does:**
Extracts your highest-performing setup type from historical data

**Usage:**
```
"what's my best setup?"
"which setups work best for me?"
"show me my edge"
```

**Output:**
- Setup name with win rate
- Number of trades with that setup
- Total P&L from that setup
- Examples of winning trades
- Recommendation to increase allocation

**Example:**
```
Your Best Setup: Support Bounces
- Win Rate: 78.5% (13/17 trades)
- Total P&L: +$1,850
- Avg P&L per trade: +$142

💡 Insight: This is your edge. Increase your allocation here.
```

---

### Command: "what mistakes am I repeating?"

**What it does:**
Shows the top recurring mistakes from your trade journal

**Usage:**
```
"what mistakes am I repeating?"
"show me common errors"
"what's costing me money?"
"where do I keep messing up?"
```

**Output:**
- Top 5 mistakes with frequency
- Impact analysis (how much it costs)
- Pattern description
- How to prevent it
- Action item checklist

**Example:**
```
🔴 TOP MISTAKES:

1. "No trigger stack" (6 times)
   Cost: -$450 average
   Fix: Add pre-trade checklist
   [ ] Confirm TA alignment
   [ ] Check market context
   [ ] Verify sentiment
   [ ] Check volume
   [ ] Mark seasonality

2. "Chased breakout" (4 times)
   Cost: -$200 average
   Fix: Wait for pullback confirmation

3. "Over-sized position" (3 times)
   Cost: -$180 average
   Fix: Use risk calculator before entry
```

---

### Command: "this week's summary" / "weekly review"

**What it does:**
Generates a comprehensive weekly performance summary

**Usage:**
```
"this week's summary"
"weekly review"
"how did I do this week?"
"give me weekly insights"
```

**Output:**
- Total trades and win rate for week
- Best and worst days
- Best and worst setups
- P&L breakdown
- Pattern highlights
- Action items for next week

**Example:**
```
📊 WEEKLY SUMMARY - Week of Oct 14-18

📈 PERFORMANCE:
- Total Trades: 12
- Win Rate: 72.3% (vs 72.1% baseline)
- Total P&L: +$1,820
- Best Day: Wed (+$450)
- Worst Day: Mon (-$100)

🏆 BEST SETUP THIS WEEK:
Support Bounces: 4/5 wins (+$680)

⚠️ BIGGEST ISSUE:
"No trigger stack" cost you 6 trades

💡 ACTION ITEMS FOR NEXT WEEK:
1. Create pre-trade checklist to prevent "no trigger stack"
2. Trade more support bounce setups
3. Reduce Monday size (0.5x normal)
4. Focus trading on 10-12 ET window
```

---

### Command: "psychology check"

**What it does:**
Updates your emotional/mental state for the day

**Usage:**
```
"psychology: focused and patient today"
"psychology: getting emotional after losses"
"psychology: overtrading due to boredom"
"psychology: good discipline so far"
```

**Logged Data:**
- Emotional state description
- Time noted (automatic)
- Stored in live session for analysis

**When to use:**
- Mid-day check-in
- When emotions are affecting trades
- End of day summary

---

## 🔍 Research & Market Commands

### Command: "market context"

**What it does:**
Gets current market conditions (SPY, QQQ, VIX, signal score, etc.)

**Usage:**
```
"market context"
"what's the market doing?"
"show me current levels"
```

**Output:**
- SPY price and trend
- QQQ price and trend
- VIX level and interpretation
- Composite signal score
- Breadth data if available
- Market tone (BULLISH/BEARISH/MIXED)

**Example:**
```
📊 CURRENT MARKET CONTEXT

SPY: $585.50 (holding support)
QQQ: $601.20 (near resistance)
VIX: 19.5 (constructive)
Composite Signal: 68.6/100 (MODERATE - Selective Risk)

Market Tone: MIXED
Breadth: 12/25 (weak)

Key Levels:
- SPY Resistance: 590.75
- SPY Support: 582.50
- QQQ Resistance: 605.00
- QQQ Support: 598.50
```

---

### Command: "signal status"

**What it does:**
Shows the latest composite trading signal

**Usage:**
```
"signal status"
"what's the current signal?"
"is the market good for trading?"
```

**Output:**
- Composite score (0-100)
- Signal tier (EXTREME/STRONG/MODERATE/WEAK/AVOID)
- Component breakdown
- Recommendation
- When it last changed

**Example:**
```
🎯 CURRENT SIGNAL: 68.6/100 (MODERATE)

Recommendation: SELECTIVE RISK REENTRY
- Trade only proven setups
- Reduce position size by 25%
- Maintain hedges
- Monitor resistance levels

Component Scores:
  TA: 70 (constructive but mixed)
  Context: 68 (neutral - SPY/QQQ divergence)
  Sentiment: 71 (moderately bullish)
  Volume: 66 (mixed volume profile)
  Seasonality: 64 (seasonal support weak)

Last Updated: 2 hours ago
```

---

### Command: "today's catalysts" / "what's happening?"

**What it does:**
Shows today's economic events, earnings, and market catalysts

**Usage:**
```
"today's catalysts"
"what events are happening today?"
"any earnings to watch?"
```

**Output:**
- Economic calendar events
- Earnings announcements
- Fed speakers
- Technical events to watch
- Impact assessment

---

## ⚙️ System Commands

### Command: "help" / "show me commands"

**What it does:**
Displays full list of available commands

**Usage:**
```
"help"
"show me commands"
"what can I do?"
"command list"
```

**Output:**
- Quick reference of all commands
- Brief description of each
- Usage examples
- Grouped by category

---

### Command: "status"

**What it does:**
Shows system status and data freshness

**Usage:**
```
"status"
"system status"
```

**Output:**
- Server running status
- Last analysis timestamp
- Data freshness indicators
- Connection status
- Any warnings or issues

**Example:**
```
✅ SYSTEM STATUS

Server: Running (127.0.0.1:8888)
Database: Connected
Last Analysis: 2 hours ago
Command Center: Ready
Journal System: Active

Data Freshness:
  ✓ Live Session: Fresh (real-time)
  ✓ Trends: Recent (2 hours)
  ✓ AI Feedback: Recent (2 hours)
  ✓ Trade Log: Fresh (live updates)

No issues detected
```

---

### Command: "clear [SECTION]"

**What it does:**
Clears a specific section or resets display

**Usage:**
```
"clear panel"
"clear analysis"
"reset display"
```

**What clears:**
- Analysis panel (removes current analysis)
- Live session display (doesn't delete data, just closes)
- Search filters
- Tab displays

---

## 🔄 Advanced Workflows

### Workflow: Daily Trading Session

**Morning (9:30 AM ET):**
```
1. "market context"           → See current conditions
2. "signal status"            → Check if trading is on
3. "analyze SPY"              → Get daily bias
4. "analyze QQQ"              → Tech direction
```

**Throughout Day:**
```
1. "entry NVDA long @ 189.50" → Log entry
2. "setup: SPY support at 582" → Track ideas
3. "exit NVDA @ 191.20 for +$145" → Log exit
4. "psychology: good discipline" → Track mindset
```

**End of Day (4:15 PM ET):**
```
1. "analyze my journal"       → Get analysis
2. Review Trends tab          → See patterns
3. Review AI Feedback tab     → Get coaching
4. Note top_mistakes          → Focus tomorrow
```

---

### Workflow: Weekly Review (Friday 4:30 PM)

**Steps:**
```
1. "this week's summary"      → See weekly stats
2. "what's my best setup?"    → Confirm edge
3. "what mistakes am I repeating?" → Action items
4. Review Trade Log tab       → Quality check each trade
5. Plan next week based on insights
```

---

### Workflow: Trade Setup Planning

**When you spot a setup:**
```
1. "setup: SPY double bottom at 580-582" → Document it
2. "market context"           → Confirm market conditions
3. "analyze SPY"              → Get signal
4. Plan entry/stop/target
5. Set alert and wait for confirmation
```

**When price reaches setup:**
```
1. "entry SPY long @ 581.50"  → Log entry
2. Monitor position
3. "exit SPY @ 585.00 for +$175" → Log exit
4. "psychology: [how it went]" → Update state
```

---

### Workflow: Performance Analysis

**To improve your trading:**
```
1. "what's my best setup?"    → Know your edge
2. "what mistakes am I repeating?" → Fix leaks
3. Review Trade Log           → Find patterns
4. "analyze my journal"       → Get full insights
5. "psychology check"         → Understand state
```

---

## 💡 Pro Tips

### Tip 1: Use Commands Throughout the Day
- Don't wait until end of day to log trades
- Log entry immediately: "entry NVDA long @ 189.50"
- Log exit immediately: "exit NVDA @ 191.20 for +$145"
- Real-time logging gives better analysis

### Tip 2: Track Psychology
- "psychology: feeling overconfident" → Helps pattern recognition
- "psychology: good discipline" → Reinforces positive behavior
- Psychology correlates with win rate

### Tip 3: Run Analysis Weekly
- Daily: Track trades and performance
- Weekly: Get bigger picture insights
- Monthly: Long-term pattern analysis

### Tip 4: Focus on Your Edge
- Find best performing setup with "what's my best setup?"
- Increase allocation there
- Reduce or eliminate worst performers

### Tip 5: Use Trade Log for Quality Review
- Search by date: "trades from this week"
- Search by setup: "support bounce"
- Search by result: "winning trades"
- Understand WHY you win/lose

---

## 🎯 Common Scenarios

### Scenario 1: "Should I take this trade?"
```
1. "analyze [TICKER]"        → Get signal
2. Check if signal > 60%
3. Check if it's your best setup
4. Check if it's peak trading hours
5. If all yes → "entry [TICKER]..."
```

### Scenario 2: "I'm confused about what to do"
```
1. "market context"           → Understand conditions
2. "signal status"            → Know if trading is on
3. "what's my best setup?"    → Trade your edge
4. If signal good → trade the setup
```

### Scenario 3: "I want to improve"
```
1. "this week's summary"      → See big picture
2. "what mistakes am I repeating?" → Focus area
3. "what's my best setup?"    → Know your edge
4. Create action plan
5. Next week: measure improvement
```

### Scenario 4: "Why did I lose money today?"
```
1. Review Trade Log           → See all trades
2. "what mistakes am I repeating?" → Pattern check
3. "psychology check"         → Emotional state
4. "analyze my journal"       → Full analysis
5. Find root cause
```

---

## 🚀 Cheat Sheet

**Quick Reference - Copy & Use:**

```
ANALYSIS:
• "analyze [TICKER]"
• "analyze my journal"
• "what's my best setup?"
• "what mistakes am I repeating?"

TRADING:
• "entry [TICKER] [DIR] @ [PRICE]"
• "exit [TICKER] @ [PRICE] for [PNL]"
• "position [STATUS]"
• "setup: [DESCRIPTION]"

CONTEXT:
• "market context"
• "signal status"
• "today's catalysts"

REVIEWS:
• "this week's summary"
• "psychology check"

SYSTEM:
• "help"
• "status"
• "clear [SECTION]"
```

---

**You now have everything you need to use Quick Commands effectively!**

Start with: **"analyze my journal"** to see your first insights.

Questions? Tell Claude: **"help"** for the full command list.

Happy trading! 🎯
