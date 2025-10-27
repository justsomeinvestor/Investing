#!/usr/bin/env python3
"""
Timestamp Verification Script
==============================

Verifies that all sections in master-plan.md have current timestamps.
Critical for ensuring dashboard displays current data.

Usage:
    python scripts/verify_timestamps.py [--date YYYY-MM-DD] [--strict] [--json]

Options:
    --date YYYY-MM-DD   Target date to verify against (default: today)
    --strict            Fail if ANY timestamp is not from today (default: allows yesterday)
    --json              Output machine-readable JSON for AI consumption

Exit codes:
    0 - All timestamps current
    1 - Stale or missing timestamps found

JSON Output Format:
    {
      "date": "2025-10-21",
      "total_sections": 20,
      "current_count": 15,
      "stale_sections": ["sentimentCardsUpdated", "quickActionsUpdated"],
      "missing_sections": [],
      "health_percentage": 75.0,
      "status": "needs_update"
    }
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Import YAML handler for proper path-aware extraction
sys.path.insert(0, str(Path(__file__).parent))
from yaml_handler import MasterPlanYAML

REPO_ROOT = Path(__file__).resolve().parents[2]  # Go up from scripts/utilities/ to repo root
MASTER_PLAN = REPO_ROOT / "master-plan" / "master-plan.md"

# Sections that MUST have timestamps
# NOTE: All paths must start with "dashboard." since that's the YAML root structure
# Updated 2025-10-26: Expanded to 24 critical fields (71% of 34 total timestamp fields)

REQUIRED_TIMESTAMPS = [
    # DASHBOARD-LEVEL (7 fields)
    "dashboard.lastUpdated",  # NEW - overall dashboard timestamp
    "dashboard.sentimentCardsUpdated",
    "dashboard.sentimentHistoryUpdated",
    "dashboard.metricsUpdated",
    "dashboard.riskItemsUpdated",
    "dashboard.quickActionsUpdated",
    "dashboard.providerConsensusUpdated",

    # DAILY PLANNER (8 fields - 3 NEW)
    "dashboard.dailyPlanner.prioritiesUpdated",
    "dashboard.dailyPlanner.keyLevelsUpdated",
    "dashboard.dailyPlanner.economicCalendarUpdated",
    "dashboard.dailyPlanner.aiInterpretation.updatedAt",
    "dashboard.dailyPlanner.endOfDay.ranAt",
    "dashboard.dailyPlanner.signalDataUpdated",  # NEW - automated sync (Phase 2)
    "dashboard.dailyPlanner.recommendationUpdated",  # NEW - AI-driven (Phase 5)
    "dashboard.dailyPlanner.actionChecklistUpdated",  # NEW - AI-driven (Phase 5)

    # TAB-SPECIFIC (10 fields)
    # Tab-specific timestamps (tabs are in dashboard.tabs array)
    # These require special handling - see extract_tab_timestamps()
    "tabs.portfolio.aiInterpretation.updatedAt",
    "tabs.portfolio.portfolioRecommendation.updatedAt",
    "tabs.markets.aiInterpretation.updatedAt",  # Consolidated Macro + Crypto + Tech
    "tabs.news_catalysts.aiInterpretation.updatedAt",  # Consolidated News + Media & Catalysts
    "tabs.news_catalysts.rss_updated_at",  # Daily News Flow RSS aggregation
    "tabs.news_catalysts.upcomingCatalysts_updatedAt",  # Upcoming Catalysts section
    "tabs.news_catalysts.researchHighlights_updatedAt",  # Research Highlights section
    "tabs.news_catalysts.dataAnomalies_updatedAt",  # Data Anomalies & Institutional Flows
    "tabs.news_catalysts.exhaustionSignals_updatedAt",  # Exhaustion Signals & Contrarian Warnings
    "tabs.xsentiment.aiInterpretation.updatedAt",
    "tabs.xsentiment.socialTabSyncedAt",
    "tabs.xsentiment.crypto_trending.updatedAt",  # Crypto trending tickers
    "tabs.xsentiment.macro_trending.updatedAt",  # Macro trending tickers
    "tabs.xsentiment.contrarian_detector.updatedAt",  # Contrarian analysis & opportunity detection
    "tabs.technicals.aiInterpretation.updatedAt",
    "tabs.technicals.technicalsTabSyncedAt",
    "tabs.technicals.spxTechnicals.updatedAt",  # S&P 500 technical analysis
    "tabs.technicals.bitcoinTechnicals.updatedAt",  # Bitcoin technical analysis
    "tabs.technicals.tradingSignalScore.updatedAt",  # trading signal score freshness
    "tabs.technicals.unusualActivity.updatedAt",  # NEW - unusual options activity detection
]

# VERIFICATION COVERAGE SUMMARY
# =============================
# Total timestamp fields identified in master-plan.md: 34
# Fields now tracked by this script: 33 (7 dashboard + 8 planner + 18 tab-specific)
# Coverage: 97% of all fields, 100% of critical fields
#
# Phase 2 (Automated Sync - 14 fields): sentimentCards, metrics, riskItems, quickActions,
#   providerConsensus, priorities, keyLevels, economicCalendar, signalDataUpdated, endOfDay.ranAt,
#   tradingSignalScore, unusualActivity
#
# Phase 5 (AI Synthesis - 13 fields): dailyPlanner.aiInterpretation, recommendation*,
#   actionChecklist*, tab aiInterpretations (portfolio, markets, news, xsentiment, technicals)
#
# * = newly added in this expansion
#
# Remaining 7 fields (not tracked): Provider-level updates, sub-section timestamps, etc.


def parse_args():
    parser = argparse.ArgumentParser(description="Verify master plan timestamps")
    parser.add_argument(
        "--date",
        help="Expected date in YYYY-MM-DD (defaults to today)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if ANY timestamp is not from today (default allows yesterday for some sections)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON instead of human-readable report",
    )
    return parser.parse_args()


def extract_timestamp_from_yaml(data, path):
    """
    Extract timestamp from YAML data using dot-notation path.

    Args:
        data: Parsed YAML dictionary
        path: Dot-notation path like "xsentiment.crypto_trending.updatedAt"

    Returns:
        Timestamp string or None if not found
    """
    parts = path.split('.')
    current = data

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None

    # Convert to string if datetime object
    if isinstance(current, str):
        return current
    else:
        return str(current) if current is not None else None


def extract_timestamps_yaml_aware(file_path):
    """
    Extract all required timestamps using YAML parser.
    Returns dict mapping full path to timestamp value.
    """
    try:
        yaml_handler = MasterPlanYAML(file_path)
        data = yaml_handler.load()

        timestamps = {}
        for field_path in REQUIRED_TIMESTAMPS:
            # Special handling for tab paths (tabs.{id}.field.path)
            if field_path.startswith("tabs."):
                parts = field_path.split('.', 2)  # Split into ['tabs', '{tab_id}', 'field.path']
                if len(parts) >= 3:
                    tab_id = parts[1]
                    field_in_tab = parts[2]

                    # Find the tab with matching id
                    tabs = data.get('dashboard', {}).get('tabs', [])
                    for tab in tabs:
                        if tab.get('id') == tab_id:
                            # Extract timestamp from within this tab
                            ts_value = extract_timestamp_from_yaml(tab, field_in_tab)
                            if ts_value:
                                timestamps[field_path] = ts_value
                            break
            else:
                # Direct path extraction
                ts_value = extract_timestamp_from_yaml(data, field_path)
                if ts_value:
                    timestamps[field_path] = ts_value

        return timestamps
    except Exception as e:
        print(f"[ERROR] Failed to parse YAML: {e}", file=sys.stderr)
        return {}


def parse_timestamp(ts_str):
    """Parse timestamp string to datetime object."""
    # Handle ISO format: 2025-10-15T15:45:00Z
    if 'T' in ts_str and ts_str.endswith('Z'):
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))

    # Handle other formats
    try:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M ET")
    except:
        try:
            return datetime.strptime(ts_str, "%Y-%m-%d")
        except:
            return None


def classify_timestamp(ts_datetime, target_date, strict=False):
    """Classify timestamp as CURRENT, STALE, or VERY_STALE."""
    if ts_datetime is None:
        return "INVALID"

    # Remove timezone info for comparison
    ts_date = ts_datetime.date()
    target = target_date.date()
    yesterday = (target_date - timedelta(days=1)).date()

    if ts_date == target:
        return "CURRENT"
    elif ts_date == yesterday and not strict:
        return "STALE"
    else:
        return "VERY_STALE"


def main():
    args = parse_args()

    # Determine target date
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError as exc:
            raise SystemExit(f"[ERROR] Invalid --date format: {args.date}") from exc
    else:
        target_date = datetime.now()

    # Create YAML handler for reuse
    yaml_handler = MasterPlanYAML(MASTER_PLAN)

    # Print header (skip in JSON mode)
    if not args.json:
        print(f"\n{'='*60}")
        print(f"  TIMESTAMP VERIFICATION REPORT")
        print(f"  Date: {target_date.strftime('%Y-%m-%d')}")
        print(f"  Mode: {'STRICT (today only)' if args.strict else 'NORMAL (today or yesterday)'}")
        print(f"{'='*60}\n")

    # Load master plan using YAML parser
    if not MASTER_PLAN.exists():
        raise SystemExit(f"[ERROR] Master plan not found: {MASTER_PLAN}")

    timestamps = extract_timestamps_yaml_aware(MASTER_PLAN)

    # Classify timestamps
    current = []
    stale = []
    very_stale = []
    missing = []
    invalid = []

    for field_path in REQUIRED_TIMESTAMPS:
        ts_value = timestamps.get(field_path)

        if ts_value is None:
            missing.append(field_path)
        else:
            ts_datetime = parse_timestamp(ts_value)
            classification = classify_timestamp(ts_datetime, target_date, args.strict)

            if classification == "CURRENT":
                current.append((field_path, ts_value))
            elif classification == "STALE":
                stale.append((field_path, ts_value))
            elif classification == "VERY_STALE":
                very_stale.append((field_path, ts_value))
            elif classification == "INVALID":
                invalid.append((field_path, ts_value))

    # Calculate summary statistics
    total = len(REQUIRED_TIMESTAMPS)
    current_count = len(current)
    stale_count = len(stale)
    problem_count = len(very_stale) + len(missing) + len(invalid)
    health_percentage = (current_count / total * 100) if total > 0 else 0

    # Determine return code (distinguish between CRITICAL and EXPECTED failures)
    # Exit code 2 = CRITICAL FAILURE (missing/invalid data - BLOCKS workflow)
    # Exit code 1 = WARNING (stale AI sections - EXPECTED, workflow continues)
    # Exit code 0 = SUCCESS (all current)
    if problem_count > 0:
        # CRITICAL: Missing, invalid, or very stale data = BLOCKS workflow
        # This represents actual missing/corrupted data, not just aging AI narratives
        return_code = 2  # HARD STOP - data integrity issue
    elif stale_count > 0:
        # EXPECTED: Stale AI narrative sections (yesterday's data)
        # These are normal after DASH phase and require manual AI updates (POST-DASH)
        return_code = 1  # WARNING - continue workflow, output guidance for manual updates
    else:
        return_code = 0  # All sections current

    # JSON output mode
    if args.json:
        output = {
            "date": target_date.strftime("%Y-%m-%d"),
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_sections": total,
            "current_count": current_count,
            "stale_count": stale_count,
            "very_stale_count": len(very_stale),
            "missing_count": len(missing),
            "invalid_count": len(invalid),
            "health_percentage": round(health_percentage, 1),
            "critical_sections": [field for field, ts in very_stale],  # 2+ days old
            "stale_sections": [field for field, ts in stale],  # yesterday (expected)
            "missing_sections": missing,  # data not found
            "status": "current" if return_code == 0 else ("needs_manual_update" if return_code == 1 else "critical_failure")
        }
        print(json.dumps(output, indent=2))
        sys.exit(return_code)

    # Human-readable output mode
    if current:
        print(f"[OK] CURRENT ({len(current)} sections - updated today):")
        for field, ts in current:
            print(f"   {field}: {ts}")
        print()

    if stale:
        print(f"[WARN] STALE ({len(stale)} sections - updated yesterday):")
        for field, ts in stale:
            print(f"   {field}: {ts}")
        print()

    if very_stale:
        print(f"[ERROR] VERY STALE ({len(very_stale)} sections - 2+ days old):")
        for field, ts in very_stale:
            days_old = (target_date.date() - parse_timestamp(ts).date()).days
            print(f"   {field}: {ts} ({days_old} days old)")
        print()

    if invalid:
        print(f"[WARN] INVALID TIMESTAMPS ({len(invalid)} sections):")
        for field, ts in invalid:
            print(f"   {field}: {ts}")
        print()

    if missing:
        print(f"[ERROR] MISSING TIMESTAMPS ({len(missing)} sections):")
        for field in missing:
            print(f"   {field}")
        print()

    print(f"{'='*60}")
    print(f"SUMMARY: {current_count}/{total} current")

    # Distinguish between critical failures and expected stale sections
    if return_code == 2:
        # CRITICAL: Missing or severely stale data (2+ days old)
        print(f"\n{'='*60}")
        print("[CRITICAL FAILURE] DATA INTEGRITY ISSUE")
        print(f"{'='*60}")
        print("[HARD STOP] Cannot proceed - missing or corrupted data detected")
        print(f"   Health: {health_percentage:.1f}% ({current_count}/{total} sections current)")
        print()
        print("[ACTION REQUIRED]")
        if very_stale:
            print(f"   • {len(very_stale)} VERY STALE sections (2+ days old) - requires re-run of DASH phase")
        if missing:
            print(f"   • {len(missing)} MISSING sections - data not found")
        if invalid:
            print(f"   • {len(invalid)} INVALID timestamps - corrupt data")
        print()
        print("   Fix data issues and re-run workflow completely")
        print(f"{'='*60}")
    elif return_code == 1:
        # EXPECTED: Stale AI narrative sections (yesterday's data - normal after DASH)
        print(f"\n{'='*60}")
        print("[EXPECTED STATE] AI SECTIONS NEED MANUAL UPDATES")
        print(f"{'='*60}")
        print("[OK] Workflow completed successfully")
        print(f"   Health: {health_percentage:.1f}% ({current_count}/{total} sections current)")
        print()
        print("[NEXT STEPS - Manual AI Work (10-20 minutes)]")
        print(f"   • {stale_count} stale sections (updated yesterday)")
        print("   • Each requires fresh AI narrative updates")
        print("   • See: stale_sections_{YYYY-MM-DD}.json for details")
        print()
        print("   1. Read stale sections report")
        print("   2. Update each section with fresh AI analysis")
        print("   3. Re-run verify_timestamps.py to confirm 100% health")
        print()
        print("[NOTE] This is NORMAL - stale AI sections are expected after DASH phase")
        print(f"{'='*60}")
    else:
        # SUCCESS: All sections current
        print("\n[OK] All sections are current!")
        print("[OK] 100% data freshness - ready to proceed")

    print(f"{'='*60}\n")

    # CRITICAL: Validate key levels data quality
    validate_key_levels_data(yaml_handler)

    sys.exit(return_code)


def validate_key_levels_data(yaml_handler):
    """
    Validate that key levels contain real market data, not fallback values.

    Accepts both formats:
    1) Structured objects: {asset, entry/support, stop/breakdown, target/resistance, rationale?}
    2) Legacy strings: "ASSET: $PRICE - description"

    CRITICAL: Key levels must have reasonable price ranges:
    - SPY: $400-$800 (reasonable equity range)
    - QQQ: $300-$700 (reasonable tech ETF range)
    - VIX: 10-50 (reasonable volatility range)
    - BTC: $20,000-$150,000 (reasonable crypto range)
    - ETH: $1,500-$6,000 (reasonable ETH range)
    - SOL: $50-$300 (reasonable SOL range)

    If values are outside these ranges or missing, FAIL HARD.
    """
    print(f"\n{'='*60}")
    print("[DATA QUALITY] VALIDATING KEY LEVELS")
    print(f"{'='*60}")

    data = yaml_handler.load()
    key_levels = data.get('dashboard', {}).get('dailyPlanner', {}).get('keyLevels', [])

    if not key_levels:
        print("[ERROR] Key levels data is missing!")
        print("[CRITICAL] Cannot trade without key support/resistance levels")
        sys.exit(2)

    # Define reasonable ranges (if outside this, likely fake/stale data)
    ranges = {
        'SPY': (400, 800),
        'QQQ': (300, 700),
        'VIX': (10, 50),
        'BTC': (20000, 150000),
        'ETH': (1500, 6000),
        'SOL': (50, 300)
    }

    errors = []
    warnings = []

    def parse_numeric(value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        # Extract first number from string (handles $ and commas)
        m = re.search(r'\$?([\d,]+\.?\d*)', str(value))
        if not m:
            return None
        try:
            return float(m.group(1).replace(',', ''))
        except Exception:
            return None

    for item in key_levels:
        # Object format
        if isinstance(item, dict):
            asset = str(item.get('asset') or '').strip()
            # Prefer entry/support for validation; fall back to target/resistance
            candidate = (
                item.get('entry')
                or item.get('support')
                or item.get('target')
                or item.get('resistance')
            )
            price = parse_numeric(candidate)
            if not asset or price is None:
                errors.append(f"Malformed key level object: {item}")
                continue
        else:
            # Legacy string format: "ASSET: $PRICE - description"
            level_str = str(item)
            if ':' not in level_str:
                errors.append(f"Malformed key level: {level_str}")
                continue
            asset = level_str.split(':')[0].strip()
            price = parse_numeric(level_str.split(':', 1)[1])
            if price is None:
                errors.append(f"Cannot parse price from: {level_str}")
                continue

        # Validate range
        if asset in ranges:
            min_val, max_val = ranges[asset]
            if price < min_val or price > max_val:
                errors.append(
                    f"{asset} price ${price:,.2f} outside reasonable range ${min_val:,}-${max_val:,}"
                )
            else:
                print(f"   [OK] {asset}: ${price:,.2f} (within valid range)")
        else:
            warnings.append(f"Unknown asset: {asset} (no validation range defined)")

    if errors:
        print(f"\n[ERROR] KEY LEVELS DATA VALIDATION FAILED")
        for error in errors:
            print(f"   {error}")
        print()
        print("[CRITICAL] Key levels contain invalid data - likely fake/stale values")
        print("[ACTION] Re-run workflow to fetch fresh market data")
        sys.exit(2)

    if warnings:
        print(f"\n[WARN] Key levels validation warnings:")
        for warning in warnings:
            print(f"   {warning}")

    print(f"\n[OK] All key levels validated - prices within reasonable ranges")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
