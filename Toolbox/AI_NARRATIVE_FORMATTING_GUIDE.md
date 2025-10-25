# AI Narrative Formatting Guide

**Purpose**: Standardized format for all AI interpretation fields across dashboard tabs
**Effective Date**: October 23, 2025
**Status**: Active

---

## Overview

All dashboard tabs with AI interpretation sections must follow these formatting guidelines to ensure consistency, readability, and proper dashboard display.

**Key Rule**: **≤600 CHARACTER LIMIT on all text fields** (summary, keyInsight, action)

---

## Applies To

### Current Implementation
- ✅ Dashboard.dailyPlanner.aiInterpretation
- ✅ Tabs.markets.aiInterpretation
- ✅ Tabs.portfolio.aiInterpretation
- ✅ Tabs.news_catalysts.aiInterpretation
- ✅ Tabs.xsentiment.aiInterpretation
- ✅ Tabs.technicals.aiInterpretation

### Future Tabs
Any new tab with AI interpretation sections should follow this guide.

---

## Field Requirements

### 1. Summary Field (≤600 characters)

**Purpose**: Concise context about today's market/situation

**Requirements**:
- Lead with most important context first
- Be specific: include prices, percentages, data points
- Cover 2-3 key areas (structure, technicals, themes)
- Make it scannable with concrete details
- Reference actual catalysts and timelines

**Structure**:
```
[Current Market Status] [Key Levels/Prices] [Technical Context]
[Breadth/Structural Issue] [Critical Catalyst/Timeline]
```

**Good Example (Markets Intelligence - 389 chars)**:
```
Markets at critical inflection as signal improved +28 pts (institutional buyers
entering weakness). SPX 6,656 support defending, QQQ $604 double-bottom breakout
point, BTC $107,600 floor tested. BUT breadth deteriorating 11 months (negative
divergence: indexes high, 93% of stocks lagging). Today's 8:30 AM jobless claims
= ONLY macro signal during shutdown, binary catalyst for direction.
```

**What NOT to do**:
- ❌ Vague: "Markets are improving slightly with mixed signals"
- ❌ Too long: 1000+ character narratives
- ❌ No data: "Crypto is up and sentiment is improving"

**Good Example (Daily Planner - 401 chars)**:
```
Daily Context for October 23, 2025:

Signal Tier: MODERATE (58.0/100)
Breadth: 15/25 (MODERATE)

Trading Posture: Selective - quality opportunities

Key Focus:
- Monitor signal strength for changes in market regime
- Respect risk management rules regardless of signal
- Stay nimble - conditions can change rapidly
```

---

### 2. KeyInsight Field (≤600 characters)

**Purpose**: The ONE critical thing traders need to know today

**Requirements**:
- Single most important insight, not a list
- Lead with the insight, not explanation
- Be extremely specific and actionable
- Reference actual data/levels
- Make it bold and memorable

**Structure**:
```
[CRITICAL FINDING] - [Specific Divergence/Setup/Catalyst] = [Market Implication]
```

**Good Example (Markets Intelligence - 234 chars)**:
```
SIGNAL TIER JUMPED +28 PTS TO MODERATE (58/100) BUT SEVERE BREADTH DETERIORATION
(11-MONTH A/D LINE COLLAPSE) = TEXTBOOK NEGATIVE DIVERGENCE: INDEXES AT HIGHS,
MAJORITY OF STOCKS LAGGING = FRAGILE RALLY STRUCTURE NEEDING CONFIRMATION.
```

**Good Example (Daily Planner - 427 chars)**:
```
THREE simultaneous inflection points: (1) Signal tier improvement (+28 pts) shows
market finding institutional buyers on weakness = regime shift from deterioration
to stabilization; (2) Jobless claims at 8:30 AM = ONLY data in shutdown void, any
surprise will swing sentiment massively; (3) Technical support levels being tested
simultaneously (SPX 6,656, QQQ $604, BTC $107,600) = market proving near-term
direction THIS WEEK.
```

**What NOT to do**:
- ❌ Multiple insights: "The market improved, sentiment is better, and technicals look good"
- ❌ Too vague: "Today is critical for direction"
- ❌ Too long: Becomes a summary instead of single insight

---

### 3. Action Field (≤600 characters)

**Purpose**: Specific actionable guidance with conditional logic

**Requirements**:
- Use IF/THEN logic for conditional scenarios
- Include specific price levels and catalysts
- Provide position sizing guidance
- Reference risk management rules
- Make it directly executable

**Structure**:
```
[PRIMARY WAIT/ACTION] [IF Scenario A THEN Do X] [IF Scenario B THEN Do Y]
[Key Monitoring Points] [Risk Management Guidelines]
```

**Good Example (Markets Intelligence - 305 chars)**:
```
WAIT for 8:30 AM jobless claims. STRONG/IN-LINE = deploy 30-35% equities (quality
+ quantum), 20% crypto, 10% hedges. WEAK = defensive 25% equities, 15% crypto,
25% hedges, 35% cash. Monitor: SPX 6,656, QQQ $600, BTC $107,600 supports. Reduce
sizing 10-20%, quality bias non-negotiable given poor breadth.
```

**Good Example (Daily Planner - 513 chars)**:
```
WAIT for 8:30 AM jobless claims before aggressive positioning. IN-LINE/STRONG
claims = BUY weakness in quality names + quantum/Bitcoin infrastructure themes
(IBM quantum, Bittensor, Ledger announcements). WEAK claims = defensive tilt,
tighten stops on all positions, reduce sizing 20%. Key monitoring: (1) Jobless
claims outcome and market reaction, (2) SPX hold above 6,656, (3) QQQ break above
$604 or below $600, (4) VIX cross $20 (fear escalation). Maintain tactical hedges
through CPI Friday + Fed Oct 28-29.
```

**What NOT to do**:
- ❌ No specificity: "Buy if it goes up, sell if it goes down"
- ❌ No levels: "Watch key support" (which support?)
- ❌ Too passive: "Monitor the market for changes"
- ❌ No conditionals: Just general observations

---

### 4. Sentiment Field

**Purpose**: Overall market sentiment classification

**Allowed Values**:
- `bullish` - Strong positive outlook
- `cautiously bullish` - Positive but with caution (most common)
- `neutral` - No directional bias
- `cautiously bearish` - Negative but waiting for confirmation
- `bearish` - Strong negative outlook

**Selection Logic**:
- Choose based on overall narrative analysis
- Usually matches tone of summary + keyInsight + action
- Use "cautiously" variant when conflicting signals exist

**Examples**:
- Markets Intelligence: `cautiously bullish` (improved signal but weak breadth)
- Daily Planner: `cautiously bullish` (moderate signal, selective opportunities)

---

### 5. Confidence Field

**Purpose**: Confidence level in the assessment

**Allowed Values**:
- `high` - Very confident in analysis (80%+ conviction)
- `medium-high` - Confident with some caveats (most common)
- `medium` - Moderate confidence, multiple scenarios possible
- `low` - Low confidence, too much uncertainty

**Selection Logic**:
- Based on data quality and clarity of signals
- Lower confidence when: conflicting signals, data void, extreme volatility
- Higher confidence when: clear trends, multiple confirmations, strong catalysts

**Examples**:
- Markets Intelligence: `medium-high` (clear inflection but breadth concerns)
- Daily Planner: `medium-high` (signal improved but waiting for catalyst)

---

### 6. UpdatedAt Field

**Format**: ISO 8601 timestamp (always)

**Example**: `2025-10-23T13:45:54Z`

**Requirements**:
- Set to **current time** when you update the narrative
- Use UTC timezone (the Z at end)
- Format: YYYY-MM-DDTHH:MM:SSZ
- CRITICAL for freshness verification

**How to Generate**:
```python
from datetime import datetime
timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
# Result: 2025-10-23T13:45:54Z
```

---

## Character Count Validation

### Before Submitting Any Narrative

Count characters in EACH field and verify:

```
Summary: XXX chars (must be ≤600)
KeyInsight: XXX chars (must be ≤600)
Action: XXX chars (must be ≤600)
```

### How to Count

**In Python**:
```python
text = "your narrative text here"
char_count = len(text)
print(f"Characters: {char_count}")
```

**Manual Count**: Copy text to online character counter (caution: may include/exclude spaces differently)

### Reducing Length

If field exceeds 600 characters:
1. Remove adjectives and filler words
2. Use abbreviations (SPX, QQQ, BTC, etc.)
3. Remove repetition
4. Shorten explanations
5. Use concise examples instead of full explanations

**Example Reduction**:

**Original (723 chars - TOO LONG)**:
```
The markets are experiencing a critical inflection point today because the signal
tier has improved by twenty-eight points from thirty to fifty-eight, which indicates
that institutional buyers have discovered weakness in the market. However, this
improvement is being masked by severe breadth deterioration that has been ongoing
for eleven months since November 2024, creating a textbook negative divergence
pattern where the major indexes are trading at or near all-time highs but the
majority of stocks, about ninety-three percent, are lagging significantly behind
and not participating in the rally, which creates a fragile structure that needs
confirmation from future price action and market internals.
```

**Revised (389 chars - GOOD)**:
```
Markets at critical inflection as signal improved +28 pts (institutional buyers
entering weakness). SPX 6,656 support defending, QQQ $604 double-bottom breakout
point, BTC $107,600 floor tested. BUT breadth deteriorating 11 months (negative
divergence: indexes high, 93% of stocks lagging). Today's 8:30 AM jobless claims
= ONLY macro signal during shutdown, binary catalyst for direction.
```

---

## Tab-Specific Examples

### Daily Planner Tab

**Fields to Update**:
- summary (≤600 chars)
- keyInsight (≤600 chars)
- action (≤600 chars)
- sentiment
- confidence
- updatedAt

**Focus**: Daily trading context, signal tier, key catalysts, position sizing

**Example Summary (401 chars)**:
```
Daily Context for October 23, 2025:

Signal Tier: MODERATE (58.0/100)
Breadth: 15/25 (MODERATE)

Trading Posture: Selective - quality opportunities

Key Focus:
- Monitor signal strength for changes in market regime
- Respect risk management rules regardless of signal
- Stay nimble - conditions can change rapidly
```

---

### Markets Intelligence Tab

**Fields to Update**:
- summary (≤600 chars)
- keyInsight (≤600 chars)
- action (≤600 chars)
- sentiment
- confidence
- updatedAt

**Focus**: Market structure, technical inflection points, structural themes, actionable levels

**Example Summary (389 chars)**:
```
Markets at critical inflection as signal improved +28 pts (institutional buyers
entering weakness). SPX 6,656 support defending, QQQ $604 double-bottom breakout
point, BTC $107,600 floor tested. BUT breadth deteriorating 11 months (negative
divergence: indexes high, 93% of stocks lagging). Today's 8:30 AM jobless claims
= ONLY macro signal during shutdown, binary catalyst for direction.
```

---

### Portfolio Tab

**Fields to Update**:
- summary (≤600 chars) - Portfolio positioning context
- keyInsight (≤600 chars) - Critical portfolio insight
- action (≤600 chars) - Portfolio action guidance
- sentiment
- confidence
- updatedAt

**Focus**: Account risk, position sizing, theme exposure, rebalancing guidance

---

### News & Catalysts Tab

**Fields to Update**:
- summary (≤600 chars)
- keyInsight (≤600 chars)
- action (≤600 chars)
- sentiment
- confidence
- updatedAt

**Focus**: Critical catalysts, earnings themes, structural stories

---

### X Sentiment Tab

**Fields to Update**:
- summary (≤600 chars)
- keyInsight (≤600 chars)
- action (≤600 chars)
- sentiment
- confidence
- updatedAt

**Focus**: Social sentiment consensus, trending narratives, crowd positioning

---

### Technicals Tab

**Fields to Update**:
- summary (≤600 chars)
- keyInsight (≤600 chars)
- action (≤600 chars)
- sentiment
- confidence
- updatedAt

**Focus**: Technical setup, key levels, pattern formations, momentum signals

---

## Writing Style Guidelines

### Tone
- Professional Bloomberg-style analysis
- Specific data points, not vague generalizations
- Actionable insights for traders
- Direct and concise language

### Structure
- Lead with most important info
- Use concrete numbers and levels
- Reference actual catalysts and timelines
- Include conditional logic (IF/THEN)

### Specificity
- Always include actual prices (SPX 6,656, not "near support")
- Always include percentages (84% beats, not "mostly positive")
- Always include ratios (P/C 1.57, not "defensive positioning")
- Always include timeframes (8:30 AM, not "soon")

### What NOT to Do
- ❌ Vague adjectives: "good", "bad", "strong", "weak" (without data)
- ❌ Filler words: "essentially", "quite", "rather", "certainly"
- ❌ Repetition: Don't say the same thing twice
- ❌ Speculation: Stick to observable facts and clear implications
- ❌ Uncertainty hedges: Avoid "might", "could", "may" without supporting data

---

## Workflow Integration

### When Workflow Prompts You

The wingman dash workflow will output something like:

```
CRITICAL: Markets Intelligence Tab Requires RICH AI NARRATIVE

Markets Intelligence tab needs SIX fields updated:

1. tabs.markets.aiInterpretation.summary (≤600 chars)
   → Concise market context synthesizing Macro + Crypto + Tech

2. tabs.markets.aiInterpretation.keyInsight (≤600 chars)
   → The ONE critical insight dominating today's market

[... etc ...]
```

### Your Process

1. **Read the prompt** - Understand what's needed
2. **Research files** - Open the listed research files
3. **Synthesize** - Create six fields following this guide
4. **Count chars** - Validate all text fields ≤600 chars
5. **Update** - Edit master-plan.md with new values
6. **Timestamp** - Set updatedAt to current ISO 8601 time
7. **Save** - Confirm file saved successfully

---

## Common Mistakes & How to Fix

### Mistake 1: Summary Too Long
**Problem**: "The market situation today is complex with multiple factors at play..."
**Fix**: "Markets at critical inflection with +28 pt signal improvement + 11-month breadth deterioration = negative divergence needing confirmation."

### Mistake 2: KeyInsight Lists Multiple Points
**Problem**: "First, the signal improved. Second, breadth is weak. Third, jobless claims matter."
**Fix**: "SIGNAL IMPROVED +28 PTS BUT BREADTH DETERIORATING 11 MONTHS = FRAGILE RALLY NEEDING CONFIRMATION."

### Mistake 3: Action Without Specificity
**Problem**: "Monitor the market and trade carefully based on conditions."
**Fix**: "WAIT for 8:30 AM jobless claims. STRONG = deploy 30-35% equities, 20% crypto. WEAK = defensive 25% equities, 35% cash. Monitor: SPX 6,656, QQQ $600."

### Mistake 4: Missing Conditional Logic
**Problem**: "The market could go up or down depending on data."
**Fix**: "IF jobless claims strong → deploy into weakness. IF weak → tighten stops, reduce sizing."

### Mistake 5: Wrong Sentiment Selection
**Problem**: Selecting "bullish" when narrative shows concerns
**Fix**: Use "cautiously bullish" when bullish structure exists but caution warranted

---

## Quality Checklist

Before submitting any AI narrative field:

- [ ] Summary field ≤600 characters?
- [ ] KeyInsight field ≤600 characters?
- [ ] Action field ≤600 characters?
- [ ] All text fields include specific data (prices, percentages, ratios)?
- [ ] KeyInsight focuses on ONE critical insight (not multiple)?
- [ ] Action includes IF/THEN conditional logic?
- [ ] Sentiment selected correctly (bullish/neutral/bearish + cautiously)?
- [ ] Confidence level makes sense given analysis certainty?
- [ ] updatedAt timestamp is current (ISO 8601 format)?
- [ ] No vague language - all claims backed by data?
- [ ] Catalysts and timeframes explicitly mentioned?
- [ ] Ready for immediate action by traders?

---

## Questions?

See: `MARKETS_INTELLIGENCE_AI_UPDATE_WORKFLOW.md` for specific Markets Intelligence guidance.

---

**Version**: 1.0.0
**Last Updated**: October 23, 2025
**Status**: Active - All tabs should follow this guide
