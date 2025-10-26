# Bug Fix Guide: technical_data.json Corruption

**Issue ID**: TECH-DATA-001
**Severity**: Medium (non-blocking, affects cache only)
**Status**: Identified - Ready for fix
**Date Identified**: October 25, 2025

---

## Problem Description

The `technical_data.json` cache file is being corrupted with incomplete data. Instead of containing the full options data structure for SPY and QQQ, the file only stores the last item from the `keyLevels` array.

### Current (Corrupted) Structure
```json
{
  "date": "2025-10-25",
  "timestamp": "2025-10-25T13:54:05.946438",
  "spy_options": {
    "strike": "656.6",
    "type": "Put Wall",
    "sentiment": "bearish",
    "reason": "Put OI cluster (11,995,973)"
  },
  "qqq_options": {
    "strike": "590.73",
    "type": "Put Wall",
    "sentiment": "bearish",
    "reason": "Put OI cluster (5,605,043)"
  }
}
```

### Expected (Correct) Structure
```json
{
  "date": "2025-10-25",
  "spy_options": {
    "ticker": "SPY",
    "maxPain": "$670.00",
    "putCallRatio": "1.49",
    "putCallRatioOI": "2.66",
    "ivPercentile": "34%",
    "totalOI": "16,502,357",
    "putVolume": "2,086,155",
    "callVolume": "1,396,514",
    "putOI": "11,995,973",
    "callOI": "4,506,384",
    "volumeFlow": {
      "puts": "59%",
      "calls": "40%",
      "premium": "N/A"
    },
    "keyLevels": [
      {"strike": "670", "type": "Max Pain", "sentiment": "neutral", "reason": "Peak OI"},
      {"strike": "676.7", "type": "Gamma Neutral", "sentiment": "neutral", "reason": "High gamma"},
      {"strike": "656.6", "type": "Put Wall", "sentiment": "bearish", "reason": "Put OI cluster"}
    ]
  }
}
```

---

## Current Impact

### ✅ No Dashboard Impact
- Dashboard displays preserved manual key levels (from Oct 18)
- Workflow runs without errors
- Users see correct data

### ⚠️ Cache Degradation
- Cache file is incomplete and unusable
- Validation scripts may trigger false warnings
- Data quality metrics appear worse than reality

### ⚠️ Future Issues
- If manual data gets overwritten, cache file won't have backup
- Diagnostics become harder without good cache data

---

## Root Cause Analysis

### Suspected Location: fetch_technical_data.py

**Flow**:
```
1. fetch_all() calls fetch_spy_options()
2. fetch_spy_options() runs scraper subprocess
3. Subprocess outputs JSON to stdout
4. fetch_spy_options() parses JSON from stdout lines
5. Parsed data stored in 'spy_options' variable
6. Data saved to JSON file via save_cache()
```

**Problem Area**: Step 4 - JSON parsing from subprocess output

### Code Under Suspicion

File: `scripts/processing/fetch_technical_data.py`, lines 104-125

```python
if result.returncode == 0:
    # Extract JSON from output
    output_lines = result.stdout.strip().split('\n')
    json_started = False
    json_lines = []

    for line in output_lines:
        if line.strip() == 'SCRAPED DATA:':
            json_started = False  # Reset if we see header again
        elif line.strip() == '{':
            json_started = True
            json_lines = [line]
        elif json_started:
            json_lines.append(line)
            if line.strip() == '}':
                break  # PROBLEM: Breaks at first closing brace

    if json_lines:
        json_str = '\n'.join(json_lines)
        scraped_data = json.loads(json_str)  # This may be parsing partial JSON
```

**Issue**: Line `if line.strip() == '}'` breaks at the **first closing brace**, which could be the end of a nested object or array, not the end of the full JSON object.

---

## How to Reproduce

### Test Procedure
1. Run workflow: `python scripts/automation/run_workflow.py 2025-10-25`
2. Check cache file: `Research/.cache/2025-10-25_technical_data.json`
3. Verify spy_options structure
4. Compare to expected structure above

### Expected Failure
```bash
$ cat Research/.cache/2025-10-25_technical_data.json | jq '.spy_options'
{
  "strike": "656.6",
  "type": "Put Wall",
  ...
}
# SHOULD BE a full options data object with ticker, maxPain, putCallRatio, etc.
```

---

## Debugging Steps

### Step 1: Add Debug Logging

**File**: `scripts/processing/fetch_technical_data.py`
**Location**: Line ~100, in `fetch_spy_options()` method

```python
def fetch_spy_options(self):
    """Fetch SPY options data via Selenium scraper"""
    print("[1/6] Fetching SPY options data...")

    try:
        # Run scrape_options_data.py for SPY
        result = subprocess.run(
            [sys.executable, 'scripts/scrapers/scrape_options_data.py', 'SPY'],
            capture_output=True,
            text=True,
            timeout=120
        )

        # ADD THIS DEBUG BLOCK:
        print(f"   [DEBUG] Subprocess return code: {result.returncode}")
        print(f"   [DEBUG] Stdout length: {len(result.stdout)} chars")
        print(f"   [DEBUG] Stderr length: {len(result.stderr)} chars")

        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            json_started = False
            json_lines = []

            # ADD THIS DEBUG BLOCK:
            print(f"   [DEBUG] Total output lines: {len(output_lines)}")

            for idx, line in enumerate(output_lines):
                if line.strip() == 'SCRAPED DATA:':
                    json_started = False
                    print(f"   [DEBUG] Found SCRAPED DATA header at line {idx}")
                elif line.strip() == '{':
                    json_started = True
                    json_lines = [line]
                    print(f"   [DEBUG] Found JSON start at line {idx}")
                elif json_started:
                    json_lines.append(line)
                    if line.strip() == '}':
                        print(f"   [DEBUG] Found JSON end at line {idx}, total lines: {len(json_lines)}")
                        break

            # ADD THIS DEBUG BLOCK:
            print(f"   [DEBUG] Parsed JSON lines: {len(json_lines)}")
            if json_lines:
                json_str = '\n'.join(json_lines)
                print(f"   [DEBUG] JSON string length: {len(json_str)}")
                print(f"   [DEBUG] First 200 chars: {json_str[:200]}")
                print(f"   [DEBUG] Last 200 chars: {json_str[-200:]}")
```

### Step 2: Check Subprocess Output

Run scraper directly to see what output looks like:

```bash
python scripts/scrapers/scrape_options_data.py SPY 2>&1 | tail -200 | head -100
```

Look for:
- Where "SCRAPED DATA:" header appears
- The full JSON object structure
- How many closing braces exist
- Any truncation or malformation

### Step 3: Inspect JSON Parsing

Add validation after parsing:

```python
try:
    scraped_data = json.loads(json_str)

    # ADD THIS VALIDATION:
    required_keys = ['ticker', 'maxPain', 'putCallRatio', 'keyLevels']
    missing_keys = [k for k in required_keys if k not in scraped_data]

    if missing_keys:
        print(f"   [ERROR] Parsed JSON missing keys: {missing_keys}")
        print(f"   [ERROR] Parsed data keys: {list(scraped_data.keys())}")
        return self.get_empty_options_data('SPY')

    return scraped_data
except json.JSONDecodeError as e:
    print(f"   [ERROR] JSON parse error: {e}")
    print(f"   [ERROR] Attempted to parse: {json_str[:500]}...")
    return self.get_empty_options_data('SPY')
```

---

## Likely Fix

### Fix Strategy: Multi-brace JSON Termination

The problem is likely that the code breaks at the first `}` it finds, which could be the closing brace of the nested `keyLevels` array or another inner object.

**Better Approach**: Count braces to find the actual end of the JSON object.

```python
def fetch_spy_options(self):
    """Fetch SPY options data via Selenium scraper"""
    print("[1/6] Fetching SPY options data...")

    try:
        result = subprocess.run(
            [sys.executable, 'scripts/scrapers/scrape_options_data.py', 'SPY'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            json_started = False
            json_lines = []
            brace_count = 0

            for line in output_lines:
                if line.strip() == 'SCRAPED DATA:':
                    json_started = False
                    brace_count = 0
                elif line.strip() == '{':
                    json_started = True
                    json_lines = [line]
                    brace_count = 1
                elif json_started:
                    json_lines.append(line)
                    # Count opening and closing braces
                    brace_count += line.count('{') - line.count('}')
                    # Only break when we've closed all braces
                    if brace_count == 0:
                        break

            if json_lines:
                json_str = '\n'.join(json_lines)
                scraped_data = json.loads(json_str)

                # Validate required fields
                if all(k in scraped_data for k in ['ticker', 'maxPain', 'keyLevels']):
                    print(f"   ✅ Scraped SPY options data successfully")
                    return scraped_data
                else:
                    print(f"   ❌ Parsed JSON missing required fields")
                    return self.get_empty_options_data('SPY')
            else:
                print(f"   ❌ Could not parse scraper output")
                return self.get_empty_options_data('SPY')
        else:
            print(f"   ❌ Scraper failed with error code {result.returncode}")
            return self.get_empty_options_data('SPY')

    except Exception as e:
        print(f"   ❌ Error running scraper: {e}")
        return self.get_empty_options_data('SPY')
```

---

## Verification Checklist

After implementing fix, verify with:

- [ ] Run scraper directly: `python scripts/scrapers/scrape_options_data.py SPY`
- [ ] Verify scraped JSON output is complete and valid
- [ ] Run workflow: `python scripts/automation/run_workflow.py 2025-10-25`
- [ ] Check technical_data.json structure is correct
- [ ] Verify spy_options contains all required keys (ticker, maxPain, putCallRatio, keyLevels)
- [ ] Verify qqq_options contains all required keys
- [ ] Run sync script: `python scripts/utilities/sync_technicals_tab.py 2025-10-25`
- [ ] Verify no validation warnings are triggered
- [ ] Check master-plan.md has updated timestamps

---

## Related Files

- `scripts/processing/fetch_technical_data.py` (main file to fix)
- `scripts/scrapers/scrape_options_data.py` (subprocess being called)
- `scripts/utilities/sync_technicals_tab.py` (uses technical_data.json)
- `Research/.cache/2025-10-25_technical_data.json` (output file)

---

## Implementation Notes

- Fix is in lines 91-136 of fetch_technical_data.py
- Same issue likely exists in `fetch_qqq_options()` method (lines 138-175)
- Should fix both methods consistently
- Add similar validation to both methods
- Consider refactoring into shared helper method for DRY

---

## Estimated Effort

- **Debugging**: 15 minutes
- **Implementation**: 10 minutes
- **Testing**: 5 minutes
- **Total**: 30 minutes

---

**Priority**: HIGH (Should fix before documenting automation as "production ready")
**Timeline**: Fix before Task 2-7 implementations
**Owner**: [Assigned to developer]
**Due**: Next work session
