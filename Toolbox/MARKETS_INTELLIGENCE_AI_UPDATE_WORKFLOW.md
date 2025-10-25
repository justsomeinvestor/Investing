# Markets Intelligence AI Update Workflow

## Overview

The Markets Intelligence tab now has a **dedicated AI narrative update workflow** that is automatically triggered as part of the Wingman Dash daily workflow. This ensures the tab displays **rich, synthesized AI narratives** rather than simple placeholder text.

## How It Works

### Phase Overview

When you run the Wingman Dash workflow:

```bash
python scripts/automation/wingman_dash.py 2025-10-23
```

The workflow executes 5 phases:

1. **Phase 1:** Timestamp verification (identifies stale sections)
2. **Phase 2:** Automated sync scripts (Social, Technicals, News, Daily Planner, **Markets Intelligence**)
3. **Phase 3:** Update master plan (dates, signals, data)
4. **Phase 4:** Final verification (check freshness)
5. **Phase 5:** Generate AI update prompts for Claude Code (YOU!)

### Markets Intelligence Specific Flow

**Phase 2 - Automated Sync:**
- `update_markets_intelligence.py` runs automatically
- Extracts current market data, signals, provider insights
- Generates a comprehensive AI prompt file
- Saves to `Research/.cache/markets_intelligence_prompt_{date}.txt`

**Phase 5 - Claude Code AI Updates:**
- Workflow detects `tabs.markets.aiInterpretation` needs updating
- **Explicitly instructs Claude Code** (you) to:
  - Read research sources
  - Synthesize three narrative sections
  - Update master-plan.md fields
  - Update timestamp

## What Claude Code Must Update

When the workflow prompts you, you need to update **SIX fields** in `master-plan.md`:

### 1. `tabs.markets.aiInterpretation.summary` (≤600 characters)

**Format:** Concise market context (scannable and specific)

**Content:**
- Market Structure: Signal tier, price levels, breadth assessment
- Technical Inflection Points: Key levels for SPX, QQQ, BTC
- Structural Themes: Major market narratives and dynamics
- Include actual prices, percentages, specific catalysts

**Example (389 chars):**
```
Markets at critical inflection as signal improved +28 pts (institutional buyers
entering weakness). SPX 6,656 support defending, QQQ $604 double-bottom breakout
point, BTC $107,600 floor tested. BUT breadth deteriorating 11 months (negative
divergence: indexes high, 93% of stocks lagging). Today's 8:30 AM jobless claims
= ONLY macro signal, binary catalyst.
```

### 2. `tabs.markets.aiInterpretation.keyInsight` (≤600 characters)

**Format:** The ONE critical insight (specific and actionable)

**Content:**
- Most important thing traders need to know today
- Usually a critical inflection point, divergence, or catalyst
- Be specific and data-driven

**Example (234 chars):**
```
SIGNAL TIER JUMPED +28 PTS TO MODERATE (58/100) BUT SEVERE BREADTH DETERIORATION
(11-MONTH A/D LINE COLLAPSE) = TEXTBOOK NEGATIVE DIVERGENCE: INDEXES AT HIGHS,
MAJORITY OF STOCKS LAGGING = FRAGILE RALLY STRUCTURE NEEDING CONFIRMATION.
```

### 3. `tabs.markets.aiInterpretation.action` (≤600 characters)

**Format:** Specific actionable guidance with conditionals

**Content:**
- Trading posture with specific levels
- Conditional logic (IF/THEN scenarios)
- Position sizing and risk management
- Key monitoring points

**Example (305 chars):**
```
WAIT for 8:30 AM jobless claims. STRONG/IN-LINE = deploy 30-35% equities (quality
+ quantum), 20% crypto, 10% hedges. WEAK = defensive 25% equities, 15% crypto,
25% hedges, 35% cash. Monitor: SPX 6,656, QQQ $600, BTC $107,600 supports.
Reduce sizing 10-20%, quality bias non-negotiable.
```

### 4. `tabs.markets.aiInterpretation.sentiment`

**Format:** One of the following values:
- `cautiously bullish` (most common)
- `neutral`
- `cautiously bearish`
- `bullish`
- `bearish`

### 5. `tabs.markets.aiInterpretation.confidence`

**Format:** One of the following values:
- `low`
- `medium`
- `medium-high` (most common)
- `high`

### 6. `tabs.markets.aiInterpretation.updatedAt`

**Format:** ISO 8601 timestamp

**Value:** Current time when you update the narrative
- Example: `2025-10-23T14:30:45Z`
- CRITICAL for freshness verification

## Character Limit Guidelines

**ALL AI interpretation fields have a ≤600 character limit** to ensure:
- Fields are scannable in the dashboard UI
- Content is concise and focused
- Three-section layout (Summary Pulse, Key Insight, Actionable Focus) displays properly
- Messages are tweet-length for readability

**Before submitting, validate character counts:**
```
- summary: count characters and trim if >600
- keyInsight: count characters and trim if >600
- action: count characters and trim if >600
```

## Research Sources to Read

When updating Markets Intelligence, read these files:

- `Research/.cache/{date}_Market_Sentiment_Overview.md` - Comprehensive market analysis
- `Research/{date}_Technical_Category_Overview.md` - Technical analysis by category

These files contain all the data you need to synthesize the narrative.

## Writing Guidelines

**Tone & Style:**
- Professional Bloomberg-style financial analysis
- Specific data points and actual numbers
- Include price levels, percentages, ratios
- Reference actual catalysts and timing

**Structure:**
```
Market Structure → Technical Inflection Points → Structural Themes → Consensus Action
```

**Specificity:**
- Always include actual prices (SPX 6,656, QQQ $604, BTC $107,600)
- Include percentages and data (84% earnings beats, breadth 3/10)
- Reference actual support/resistance levels
- Mention specific catalysts (jobless claims, Fed meetings)

**Relevance:**
- Focus on Macro environment
- Cover Crypto markets
- Address Tech sector dynamics
- Synthesize into unified strategy

## Example Output

Looking at the October 23, 2025 Markets Intelligence narrative:

**Summary (excerpt):**
```
CRITICAL INFLECTION POINT - SIGNAL JUMPED +28 PTS, MARKET FINDING SUPPORT BUT BREADTH STILL WEAK.
JOBLESS CLAIMS IN 90 MINUTES = BINARY CATALYST.

MARKET STRUCTURE: Signal tier improved DRAMATICALLY from WEAK (30/100) to MODERATE (58/100)...
[continues with technical detail, structural themes, etc.]
```

**Key Insight:**
```
CRITICAL INFLECTION POINT - SIGNAL JUMPED +28 PTS (30 TO 58/100), CAPITAL DEPLOYMENT WINDOW OPENING
```

**Action:**
```
WAIT for 8:30 AM jobless claims before aggressive positioning. IN-LINE/STRONG claims = deploy 30-35% equities
(quality focus + quantum names), 20% crypto (BTC/ETH infrastructure), 10% hedges. WEAK claims = hold 25% equities
max, 15% crypto, 25% hedges, 35% cash.
```

## Integration with Workflow

When you run `wingman_dash.py`, the output will explicitly tell you:

```
CRITICAL: Markets Intelligence Tab Requires RICH AI Narrative
======================================================
Markets Intelligence tab needs THREE fields updated:

1. tabs.markets.aiInterpretation.summary
   → Rich unified narrative (2-3 paragraphs)
   → Synthesize: Macro Environment + Crypto Markets + Tech Sector
   → Include: Market Structure, Technical Inflection Points, Structural Themes

2. tabs.markets.aiInterpretation.keyInsight
   → The ONE critical insight dominating today's market (1 sentence)
   → Most important takeaway for traders

3. tabs.markets.aiInterpretation.action
   → Specific actionable guidance (2-3 sentences)
   → Include: levels, catalysts, position sizing, risk management

Research Sources:
• Research/.cache/2025-10-23_Market_Sentiment_Overview.md
• Research/2025-10-23_Technical_Category_Overview.md

Writing Style: Professional Bloomberg-style with specific data/levels
```

## Workflow in Action

### Step 1: Run Wingman Dash
```bash
python scripts/automation/wingman_dash.py 2025-10-23
```

### Step 2: Workflow Runs Phases 1-4
- Verifies timestamps
- Runs sync scripts (including Markets Intelligence data gather)
- Updates master plan
- Final verification

### Step 3: Phase 5 Output
Workflow outputs the Markets Intelligence update prompt telling you:
- Which fields to update
- Where to find research sources
- What writing style to use
- CRITICAL deadline for updates

### Step 4: Claude Code (You) Updates
- Read the research files
- Synthesize rich AI narrative
- Update the three fields in master-plan.md
- Set timestamp to current time
- Save the file

### Step 5: Workflow Complete
- Dashboard reflects fresh Markets Intelligence analysis
- All three narrative sections display with updated data
- Timestamp verification shows Markets Intelligence as "current"

## Key Differences from Other Tabs

Unlike some other tabs that get simple automated updates, **Markets Intelligence requires RICH AI synthesis**:

- ❌ NOT simple templates or placeholder text
- ✅ YES rich, detailed financial analysis
- ✅ YES specific data points and levels
- ✅ YES professional Bloomberg-style writing
- ✅ YES actionable trading guidance

## Visual Display

Once updated, the Markets Intelligence tab shows:

```
┌─────────────────────────────────────────────────────────┐
│ AI NARRATIVE BRIEFING                    ⚖️ NEUTRAL     │
│ Status ● Confidence: MEDIUM-HIGH                        │
│                                                          │
│ 💡 KEY INSIGHT                                          │
│ CRITICAL INFLECTION POINT - SIGNAL JUMPED +28 PTS...    │
│                                                          │
│ 🧠 SUMMARY PULSE                                        │
│ MARKET STRUCTURE: Signal tier improved DRAMATICALLY...  │
│ [continues with 2-3 paragraphs of analysis]            │
│                                                          │
│ 🎯 ACTIONABLE FOCUS                                     │
│ WAIT for 8:30 AM jobless claims. Strong claims = deploy │
│ 30-35% equities (quality focus + quantum names)...      │
└─────────────────────────────────────────────────────────┘
```

## Common Mistakes to Avoid

1. **Don't write simple placeholder text** → Write rich analysis
2. **Don't forget specific data** → Always include actual numbers
3. **Don't forget timestamps** → Update `updatedAt` to ISO 8601
4. **Don't miss any field** → Update summary, keyInsight, AND action
5. **Don't make it too long** → Keep summary to 2-3 paragraphs
6. **Don't use vague language** → Be specific with levels and catalysts

## Verification

After updating, verify:

1. All three narrative fields are populated
2. Content is specific (includes actual prices, percentages)
3. Timestamp is current (ISO 8601 format like `2025-10-23T14:30:45Z`)
4. Run verification to confirm Markets Intelligence timestamp is "current"

```bash
python scripts/utilities/verify_timestamps.py --date 2025-10-23 --json
```

Should show Markets Intelligence with `updatedAt` timestamp matching current time.

---

**Last Updated:** October 23, 2025
**Status:** Active - integrated into Wingman Dash workflow
**Requires:** Claude Code manual update (not fully automated)
