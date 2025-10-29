# Trade Filter Console - Usage Guide

## Step-by-Step Instructions

### STEP 1: Open the Console in Your Browser

**Action:**
1. Navigate to: `Toolbox/PROJECTS/Trade-Filter-Console/`
2. Double-click: `trade-console.html`
3. Opens in your default browser

**Result:**
- Console window opens
- Title: "⚡ WINGMAN TRADE FILTER CONSOLE"
- Display: RED light, 0/0 conditions, waiting for analysis

**Keep this window open while you trade.** Position it beside your trading platform or on a second monitor if available.

---

### STEP 2: Load Wingman (If Not Already Loaded)

**Action:**
1. Say: "i know kung fu" (or "Load Wingman")
2. Wingman loads all protocols and context
3. Wingman confirms: "Wingman online. Cockpit initialized."

**Result:**
- Wingman is now in active trading mode
- Console is primed and ready
- All protocols are loaded

---

### STEP 3: Analyze a Trade Setup

**Action - You Describe:**
```
"I want to short SPY at $600.
Price broke below $595 yesterday,
retested $598 this morning, and now
it's rolling over. RSI is at 80 with bearish divergence."
```

**Wingman's Job:**
- Recognizes: SPY SHORT = EXTENSION_SELL setup
- Opens assessment session
- Updates console with ticker "SPY"
- Sets signal light to RED (starting state)
- Begins checking conditions as you provide details

**Console Updates:**
```
SPY
RED LIGHT
0/15 conditions passed (0%)
[Awaiting setup details...]
```

---

### STEP 4: Watch Conditions Light Up

**As you provide details, conditions update in real-time:**

#### Message 1: "RSI at 80, bearish divergence"
```
Wingman updates:
✅ RSI Level Check (RSI at 80)
✅ Divergence (price higher, RSI lower)
Progress: 2/15 (13%)
```

#### Message 2: "Volume spike on the move"
```
Wingman updates:
✅ Volume (1.3x+ average confirmed)
Progress: 3/15 (20%)
```

#### Message 3: "EMA falling, signal is STRONG"
```
Wingman updates:
✅ EMA Filter (5-min 200 EMA falling)
✅ Signal Tier (STRONG 70+/100)
Progress: 5/15 (33%)
```

**Console Display Changes:**
- Progress bar advances (0% → 33%)
- More conditions show ✅ green checkmarks
- Commentary updates with Wingman's analysis
- Signal light still RED (need more conditions)

---

### STEP 5: Continue Until GREEN LIGHT

**Keep describing the setup:**
- "Price is at 127% Fibonacci extension"
- "Close + retest was confirmed yesterday"
- "VWAP shows yellow arrow signal"
- "50% pullback target would be $580 at weekly support"
- And so on...

**With each detail:**
- More conditions light up green
- Progress bar advances
- Commentary updates
- Signal light monitors progress

**When all required conditions pass:**
```
Progress: 15/15 (100%)
Signal: 🟢 GREEN LIGHT

Wingman: "All 15/15 conditions pass. Clear to enter SPY short."
```

---

### STEP 6: Enter the Trade or Wait

**If GREEN LIGHT:**
```
🟢 GO
All conditions confirmed
Clear to enter
```
→ **You can execute the trade with confidence**

**If YELLOW LIGHT (70-90%):**
```
🟡 CAUTION
Some conditions passing, some missing
Review before entry
```
→ **Wingman tells you what's missing** → Decide if acceptable risk

**If RED LIGHT (<70%):**
```
🔴 NO GO
Not enough conditions passing
Do not enter
```
→ **Wait for better setup** or **Decide to trade with calculated risk**

---

## Real-World Example: Complete Analysis

### Setup Scenario
You're looking at **QQQ** and spot something interesting.

### Your Message:
```
"QQQ just broke below 500. Price closed at 498.50 yesterday,
bounced to 501 this morning on low volume, now selling off again.
RSI has been declining while price makes higher highs.
Volume on the selloff is 2x average."
```

### Wingman's Response:
```
Copy that. QQQ short at current market price.
Analyzing extension short setup...

✓ C+R Confirmation: Closed 498.50, retested 501, confirming breakdown
✓ Divergence: Classic bearish - price higher high, RSI declining
✓ Volume: 2x average on the selloff - strong conviction

[3/15 conditions checking...]

EMA status?
Signal tier?
Fibonacci extension level?
```

**Console at this point shows:**
- Ticker: QQQ
- Signal: 🔴 RED (20% complete)
- 3 conditions lit up green
- 12 conditions still awaiting
- Progress bar at 20%

### Your Follow-up:
```
"5-min 200 EMA is falling. Signal is MODERATE (58/100).
QQQ is at 127% of prior move extension. VWAP is yellow.
Pullback would hit 485 which is the monthly support."
```

### Wingman Updates:
```
✓ EMA Filter: Falling - short confirmed
✓ Signal Tier: MODERATE - selective approach
✓ 127% Extension: At prime reversal zone
✓ VWAP Yellow Arrow: Mean reversion triggered
✓ Pullback Target: 485 = monthly support confluence

[8/15 conditions... need more]

What about breadth (ADD)?
Higher timeframe?
Volatility regime?
```

**Console now shows:**
- Signal: Still 🔴 RED (53% complete)
- 8 conditions lit up
- Progress bar halfway
- Commentary showing momentum building

### Your Final Details:
```
"Breadth rolling over, daily is still in downtrend.
Risk would be $2.50 to 502 entry, position 90 shares = $225 risk."
```

### Wingman's Final Check:
```
✓ ADD Confirmation: Declining
✓ Higher TF Alignment: Daily downtrend
✓ Risk Calculated: $225 (within 1% guideline)

═══════════════════════════════════════════
🟢 GREEN LIGHT - ALL REQUIRED CONDITIONS PASS
═══════════════════════════════════════════

QQQ Short Setup Summary:
- Close+retest breakdown confirmed
- Bearish divergence (Rule #19) validated
- At 127% Fib extension (Rule #20)
- VWAP yellow mean reversion signal
- Pullback confluence at monthly support ($485)
- Risk defined ($225), within 1% account limit

All 15/15 conditions confirmed.

Ready to execute short 90 shares @ current market.
```

**Console displays:**
- Ticker: QQQ
- Signal: 🟢 **GREEN LIGHT**
- Progress: **15/15 (100%)**
- All conditions showing ✅
- Large GO indicator pulsing
- Full analysis in commentary

---

## Common Workflows

### Workflow 1: Morning Pre-Market Scan
1. Open console
2. Load Wingman
3. Scan watchlist
4. For each potential setup: describe → watch conditions light up
5. Trade only GREEN LIGHT setups
6. Log which setups were GREEN vs YELLOW vs RED

### Workflow 2: Mid-Day Trade Analysis
1. Console already open from morning
2. Spot a setup on charts
3. Describe it to Wingman
4. Check console for real-time confirmation
5. Execute if GREEN

### Workflow 3: Post-Trade Review
1. Open console
2. Describe a trade you took (that didn't use console)
3. Manually check each condition
4. See how many were actually GREEN LIGHT quality
5. Learn: Did you trade weak setups? Did winners have GREEN LIGHT?

### Workflow 4: Setup Education
1. Open console
2. Pull up old chart
3. Walk through historical trade setup
4. Check each condition manually
5. See what a "perfect" GREEN LIGHT setup looks like
6. Compare to a trade that lost money

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F5 | Refresh console (usually auto-refreshes) |
| F12 | Open browser developer tools (for debugging) |
| Ctrl+L | Focus address bar (to navigate to file) |
| Esc | Close developer tools |

---

## Tips for Best Results

### ✅ DO:
- ✅ Keep console visible while trading
- ✅ Describe setups **in detail** (all observations)
- ✅ Let Wingman guide you through all conditions
- ✅ Wait for GREEN LIGHT before entering
- ✅ Track which GREEN setups are winners vs losers
- ✅ Use YELLOW as "caution - review" not automatic entry
- ✅ Note RED setups you traded (to learn what you missed)

### ❌ DON'T:
- ❌ Don't skip console - it's your sanity check
- ❌ Don't force a trade if conditions aren't passing
- ❌ Don't assume you know better than the checklist
- ❌ Don't ignore YELLOW light as a warning
- ❌ Don't trade RED light setups (except with full awareness)
- ❌ Don't open 10 consoles (use one, refresh it)
- ❌ Don't assume conditions pass without describing them

---

## When to Use the Console

### Use the Console When:
- ✅ You're considering entering a trade
- ✅ You want to confirm setup quality
- ✅ You're learning to spot better setups
- ✅ You're reviewing why a trade failed
- ✅ You're backtesting historical setups
- ✅ You want visual confirmation of your analysis

### Skip the Console When:
- ❌ You're just asking general questions
- ❌ You're researching market conditions (not trading)
- ❌ You need quick data (console adds ~2 min to analysis)
- ❌ You're doing quick scalp trades (too fast for checklist)
- ❌ Setup is obviously bad (no point checking)

---

## Interpreting the Signal Light

### 🔴 RED LIGHT: NO GO
- **Meaning:** < 70% of conditions passing
- **Action:** Do NOT enter
- **Reason:** Incomplete setup, high risk
- **Exception:** Only trade RED if you fully understand what's missing and accept the risk
- **Learning:** Review what conditions failed - prevent similar trades

### 🟡 YELLOW LIGHT: CAUTION
- **Meaning:** 70-90% of conditions passing
- **Action:** Review before entering
- **Reason:** Setup is decent but incomplete
- **Exception:** Can trade YELLOW with smaller size or tighter stops
- **Learning:** Understand which conditions are "nice to have" vs "must have"

### 🟢 GREEN LIGHT: GO
- **Meaning:** 100% of required conditions passing
- **Action:** Clear to enter
- **Reason:** Setup meets all quality standards
- **Exception:** Still check your intuition - conditions are guidelines not guarantees
- **Learning:** Track GREEN LIGHT setups - these should have highest win rate

---

## Troubleshooting Checklist

### Console Not Appearing?
- [ ] Is `trade-console.html` file path correct?
- [ ] Is browser set as default for HTML files?
- [ ] Try right-click → Open With → Browser
- [ ] Check browser address bar shows file path (not blank)

### Conditions Not Updating?
- [ ] Is `live_assessment.json` in correct location?
- [ ] Is Wingman actually running in this session?
- [ ] Check browser console (F12) for errors
- [ ] Refresh page (F5) to force re-read of JSON

### Progress Bar Stuck?
- [ ] Count conditions manually - are they actually passing?
- [ ] Check that all required conditions are PASS (not PENDING)
- [ ] Verify you're checking right condition count (15 for EXTENSION, 14 for PULLBACK)
- [ ] Try refreshing console

### Signal Light Not Changing?
- [ ] Verify percentage is actually ≥70% for YELLOW, 100% for GREEN
- [ ] Check that you need 15 conditions, not fewer
- [ ] Ensure all conditions marked PASS are actually correct
- [ ] Wingman: "What are the exact condition statuses?"

---

## Performance Tips

### For Faster Analysis:
1. **Pre-open console** before market hours
2. **Keep browser minimized** but ready to expand
3. **Bookmark the file** for instant access
4. **Use second monitor** - console on one screen, charts on other
5. **Turn off auto-refresh** on other apps (reduce system load)

### For Better Accuracy:
1. **Describe all observations** - don't skip details
2. **Let Wingman ask questions** - helps ensure accuracy
3. **Confirm each condition** - "Does this match your observation?"
4. **Double-check numbers** - RSI, prices, volumes
5. **Don't rush analysis** - 5 minutes of thorough analysis > 1 minute rushed

---

## Next Steps

1. **Now:** Open `trade-console.html` and keep it ready
2. **Next trade:** Use console to analyze your next potential entry
3. **Review:** After 10 trades, compare GREEN vs YELLOW vs RED results
4. **Refine:** Adjust checklist based on your actual trade results
5. **Master:** Use console for every trade decision until it's second nature

---

## Getting Help

### If You're Stuck:
1. Read the [README.md](README.md) for overview
2. Review the [Test_Scenario_Example.md](Test_Scenario_Example.md) for real example
3. Ask Wingman: "How do I use the trade filter console?"
4. Check browser console (F12) for error messages
5. Verify all files are in correct locations

### Common Questions:
**Q: Do I have to use the console?**
A: No, but it significantly improves your discipline and setup quality.

**Q: What if GREEN LIGHT trades lose?**
A: Good - you're learning. Track which conditions matter most. Maybe one condition needs refinement.

**Q: Can I modify the checklist?**
A: No - it's based on tested rules. After 100 trades, we can discuss refinements.

**Q: How long does analysis take?**
A: 3-10 minutes per setup (includes describing, condition checking, reading commentary).

**Q: Can I use this for fast scalps?**
A: No - the checklist is for swing trades and intraday trades (5m+ timeframe). Scalps are too fast.

---

**Version:** 1.0
**Last Updated:** 2025-10-28
**Status:** Production Ready
