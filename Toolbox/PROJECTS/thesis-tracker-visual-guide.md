# Investment Thesis Tracker - Visual Guide

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Investment Thesis Tracker                          [⟲ Refresh]
│  Compare and analyze your investment opportunities
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  DASHBOARD WIDGETS (Horizontally Scrollable)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ Top Opportunities│  │ Score Distribution│  │ Asset Classes   │ │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤ │
│  │                  │  │      Doughnut    │  │      Donut      │ │
│  │    Bar Chart     │  │      Chart       │  │      Chart      │ │
│  │  (Top 5 Tickers)│  │  (5 Buckets)     │  │ (Stocks/Crypto) │ │
│  │                  │  │                  │  │                  │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      MAIN CONTENT AREA                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [⊞ Grid] [≡ Table] [⇔ Compare]  ← View Toggle                 │
│                                                                   │
├─────────────────────┬──────────────────────────────────────────┤
│                     │                                            │
│  FILTERS SIDEBAR    │  CONTENT GRID / TABLE / COMPARISON        │
│                     │                                            │
│  ┌─────────────────┐│  ┌────────────┐  ┌────────────┐           │
│  │ Ticker Search   ││  │ MSFT Stock │  │ NVDA Stock │           │
│  │ [           ] ││  │ Score: 84  │  │ Score: 85  │           │
│  │                 ││  │ Theme...   │  │ Theme...   │           │
│  │ Asset Class     ││  │ [Click]    │  │ [Click]    │           │
│  │ [All ▼]         ││  └────────────┘  └────────────┘           │
│  │                 ││                                            │
│  │ Score Range     ││  ┌────────────┐  ┌────────────┐           │
│  │ [====------]    ││  │ AAPL Stock │  │ AMZN Stock │           │
│  │ All scores      ││  │ Score: 78  │  │ Score: 78  │           │
│  │                 ││  │ Theme...   │  │ Theme...   │           │
│  │ Sort By         ││  │ [Click]    │  │ [Click]    │           │
│  │ [Score H→L ▼]   ││  └────────────┘  └────────────┘           │
│  │                 ││                                            │
│  ├─────────────────┤│  [More cards below...]                     │
│  │ SUMMARY         ││                                            │
│  ├─────────────────┤│                                            │
│  │ Total: 17       ││                                            │
│  │ Stocks: 16      ││                                            │
│  │ Crypto: 1       ││                                            │
│  │ Avg Score: 71   ││                                            │
│  │ Updated: Oct 28 ││                                            │
│  │                 ││                                            │
│  └─────────────────┘│                                            │
│                     │                                            │
└─────────────────────┴──────────────────────────────────────────┘
```

---

## Grid View (Card Layout)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  MSFT  Stock │ │  NVDA  Stock │ │  AAPL  Stock │
├──────────────┤ ├──────────────┤ ├──────────────┤
│ Hyperscale   │ │ AI infra     │ │ Consumer AI  │
│ AI, cloud... │ │ backbone...  │ │ + Services.. │
│              │ │              │ │              │
│ Score: 84    │ │ Score: 85    │ │ Score: 78    │
│ / 100        │ │ / 100        │ │ / 100        │
│              │ │              │ │              │
│ 27 days ago  │ │ 27 days ago  │ │ 27 days ago  │
│ Oct 1, 2025  │ │ Oct 1, 2025  │ │ Oct 1, 2025  │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## Comparison View - Radar Chart

```
When you select stocks (e.g., MSFT, NVDA, AAPL) and click "Compare":

        ╱        Management       ╲
       ╱          ●  ●  ●          ╲
      ╱        ●              ●      ╲
    Technicals ──────────────────── Fundamentals
      ╲        ●              ●      ╱
       ╲          ●  ●  ●          ╱
        ╲       Risk   Sentiment    ╱


Legend:
  ─── MSFT (Blue)
  ─── NVDA (Purple)
  ─── AAPL (Green)

Each dimension normalized to 0-100%
Hover to see exact values
```

---

## Modal Detail View

```
┌────────────────────────────────────────────────────────┐
│  MSFT          [Stock] [<  MODAL  >] [X]              │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐  ┌──────────────────────────────┐
│  │ Quick Stats      │  │ Full Thesis Content          │
│  ├──────────────────┤  ├──────────────────────────────┤
│  │                  │  │ # MSFT Investment Thesis     │
│  │ Total Score: 84  │  │                              │
│  │ / 100            │  │ **Theme:** Hyperscale AI...  │
│  │                  │  │                              │
│  │ Fundamentals: 36 │  │ ## Thesis Pillars            │
│  │ / 40             │  │ 1. AI Capex & Financing     │
│  │                  │  │ 2. Copilot Monetization     │
│  │ Technicals: 19   │  │ 3. Azure Leadership         │
│  │ / 25             │  │                              │
│  │                  │  │ ## Catalysts & Timeline      │
│  │ Updated: Oct 1   │  │ - Q1 FY26 Earnings (Oct)   │
│  │                  │  │ - Ignite Conf (Nov)         │
│  │ [Open File Btn]  │  │                              │
│  │                  │  │ ## Risk Factors              │
│  └──────────────────┘  │ - Capex digestion...        │
│                         │ - AWS competition...        │
│                         │ - Regulatory constraints..  │
│                         │                              │
│                         │ [scroll for more]           │
│                         │                              │
│                         └──────────────────────────────┘
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## Table View

```
┌────────────┬──────┬──────────────────┬────────┬────────────┐
│ Ticker     │ Class│ Theme            │ Score  │ Updated    │
├────────────┼──────┼──────────────────┼────────┼────────────┤
│ NVDA       │Stock │ AI infrastructure│ 85/100 │ Oct 1      │
│ MSFT       │Stock │ Hyperscale AI    │ 84/100 │ Oct 1      │
│ LLY        │Stock │ Healthcare AI    │ 80/100 │ Oct 1      │
│ ASML       │Stock │ Chip equipment   │ 80/100 │ Oct 1      │
│ AAPL       │Stock │ Consumer AI      │ 78/100 │ Oct 1      │
│ ...more    │      │ ...              │  ...   │ ...        │
│ SOL        │Crypto│ High-throughput  │  N/A   │ Oct 19     │
└────────────┴──────┴──────────────────┴────────┴────────────┘
```

---

## Dashboard Widget Types

### 1. Top Opportunities (Bar Chart)

```
Top Opportunities
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NVDA ├─────████████████████────| 85
MSFT ├────═══════════════────| 84
LLY  ├────═══════════════────| 80
ASML ├────═══════════════────| 80
AAPL ├───══════════════────| 78

Hover for exact values
```

### 2. Score Distribution (Doughnut)

```
Score Distribution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      🟢 High 80-100 (8)
    🟡 Med 60-80 (5)
  🔵 Fair 40-60 (2)
🟠 Low 20-40 (1)
🔴 Poor 0-20 (0)

Total: 16 stocks
```

### 3. Asset Allocation (Donut)

```
Asset Classes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔵 Stocks (16)
🟣 Crypto (1)
```

---

## Interactive Features

### 1. Search
```
Search Input: "AI"
↓
Filters theses containing:
- "AI" in ticker
- "AI" in theme
- "AI" in core idea
↓
Shows matching results in real-time
```

### 2. Asset Class Filter
```
Current Filter: "All"

Options:
┌──────────────────┐
│ ○ All Assets     │  ← Selected
│ ○ Stocks only    │
│ ○ Crypto only    │
└──────────────────┘
```

### 3. Score Range
```
Current Filter: "All scores"

Slider:
├─────●───────────────┤
0     ↑              100
    Current: 60+
```

### 4. Sorting
```
Current Sort: "Score (High → Low)"

Options:
┌──────────────────────────┐
│ ○ Score (High → Low)    │ ← Selected
│ ○ Score (Low → High)    │
│ ○ Date (Newest)         │
│ ○ Date (Oldest)         │
│ ○ Ticker (A → Z)        │
└──────────────────────────┘
```

---

## Keyboard Shortcuts

### Global
| Key | Action |
|-----|--------|
| Ctrl+F | Focus search |

### In Modal
| Key | Action |
|-----|--------|
| ← | Previous thesis |
| → | Next thesis |
| Esc | Close modal |

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│              MARKDOWN THESIS FILES                      │
│  Tickers/Stocks/Thesis/*.md + Tickers/Crypto/*.md      │
└────────────────────────┬────────────────────────────────┘
                         │ (Read files)
                         ▼
┌─────────────────────────────────────────────────────────┐
│         PYTHON PARSER                                   │
│  scripts/processing/parse_thesis_files.py              │
├─────────────────────────────────────────────────────────┤
│ - Extract scorecard                                     │
│ - Extract pillars                                       │
│ - Extract catalysts                                     │
│ - Extract risks                                         │
│ - Extract metrics                                       │
│ - Detect ticker                                         │
│ - Normalize data                                        │
└────────────────────────┬────────────────────────────────┘
                         │ (JSON output)
                         ▼
┌─────────────────────────────────────────────────────────┐
│            JSON DATA FILE                               │
│        data/thesis_data.json                            │
│  + RnD/thesis-tracker/data/thesis_data.json            │
└────────────────────────┬────────────────────────────────┘
                         │ (Load in browser)
                         ▼
┌─────────────────────────────────────────────────────────┐
│         WEB APPLICATION                                 │
│   RnD/thesis-tracker/index.html                        │
├─────────────────────────────────────────────────────────┤
│ - data-loader.js (fetch JSON)                          │
│ - app.js (main logic)                                  │
│ - filters.js (search/filter)                           │
│ - sorters.js (sorting)                                 │
│ - visualizations.js (charts)                           │
│ - formatters.js (display)                              │
└────────────────────────┬────────────────────────────────┘
                         │ (Render)
                         ▼
┌─────────────────────────────────────────────────────────┐
│           USER INTERFACE                                │
│ • Dashboard widgets                                     │
│ • Grid/Table/Comparison views                          │
│ • Filters & search                                      │
│ • Modal details                                         │
│ • Interactive charts                                    │
└─────────────────────────────────────────────────────────┘
```

---

## Color Meanings

### Conviction Level
- 🟢 **Green** (80-100): High conviction
- 🟡 **Yellow** (60-79): Medium conviction
- 🔴 **Red** (<60): Low conviction

### UI Elements
- 🟦 **Indigo** (#6366f1): Primary accent
- 🟪 **Purple** (#8b5cf6): Secondary accent
- ⬛ **Dark Blue** (#0a0e27): Background

---

## Performance Expectations

| Action | Time |
|--------|------|
| Page load | <1 second |
| Search results | Instant (<100ms) |
| View switch | <500ms |
| Chart render | ~200ms |
| Open modal | <200ms |
| Filter apply | <100ms |

---

## Responsive Behavior

### Desktop (1200px+)
```
┌─ Header ──────────────────────────────────┐
├─ Widgets (3 per row) ─────────────────────┤
├──────────┬─────────────────────────────────┤
│ Sidebar  │ Grid/Table (3-4 columns)       │
│          │                                 │
│ Filters  │ ┌─────────────┐ ┌─────────────┐│
│ • Search │ │  Card       │ │  Card       ││
│ • Filter │ └─────────────┘ └─────────────┘│
└──────────┴─────────────────────────────────┘
```

### Tablet (768px-1200px)
```
┌─ Header ──────────────────────────────┐
├─ Widgets (2 per row) ─────────────────┤
├─────────────────────────────────────┤
│ Sidebar                               │
├─────────────────────────────────────┤
│ Grid/Table (2 columns, wrapping)    │
│ ┌─────────────┐ ┌─────────────┐     │
│ │  Card       │ │  Card       │     │
│ └─────────────┘ └─────────────┘     │
│ ┌─────────────┐ ┌─────────────┐     │
│ │  Card       │ │  Card       │     │
│ └─────────────┘ └─────────────┘     │
└─────────────────────────────────────┘
```

### Mobile (<768px)
```
┌─ Header ──────────────────────┐
├─ Widgets (scroll horizontal) ──┤
├──────────────────────────────┤
│ Sidebar                       │
├──────────────────────────────┤
│ Grid/Table (1 column)        │
│ ┌──────────────────┐         │
│ │    Card          │         │
│ └──────────────────┘         │
│ ┌──────────────────┐         │
│ │    Card          │         │
│ └──────────────────┘         │
└──────────────────────────────┘
```

---

## Next Steps

1. **Open the tracker**: `RnD/thesis-tracker/index.html`
2. **Explore data**: Try all 3 views and filters
3. **Make comparisons**: Select 2-4 stocks and see radar chart
4. **Read theses**: Click cards to see full details
5. **Update thesis files**: Edit markdown and re-run parser

---

Enjoy exploring your investment thesis data! 🚀
