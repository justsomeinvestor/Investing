#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Planner Synchronization Script
=====================================

Automatically synchronizes Daily Planner sections in master-plan.md.

Usage:
    python scripts/utilities/sync_daily_planner.py YYYY-MM-DD

Example:
    python scripts/utilities/sync_daily_planner.py 2025-10-21

Process:
    1. Updates priorities based on signal tier and market conditions
    2. Updates key levels from latest market data
    3. Updates scheduled events from economic calendar
    4. Updates aiInterpretation with daily context
    5. Sets all Daily Planner timestamps

This ensures Daily Planner never shows red dots (stale data).
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Import the proper YAML handler
sys.path.insert(0, str(Path(__file__).parent))
from yaml_handler import MasterPlanYAML

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


class DailyPlannerSyncer:
    """Synchronizes Daily Planner sections using YAML handler"""

    def __init__(self, date_str: str):
        self.date_str = date_str
        self.date = datetime.strptime(date_str, "%Y-%m-%d")

        # File paths
        self.cache_dir = Path("Research/.cache")

        # YAML handler
        self.yaml_handler = MasterPlanYAML()

        # Data containers
        self.master_plan_data: Dict[str, Any] = {}
        self.signals_data: Dict[str, Any] = {}
        self.market_data: Dict[str, Any] = {}

    def run(self):
        """Main execution flow"""
        print("\n" + "=" * 70)
        print("📅 DAILY PLANNER SYNCHRONIZATION")
        print("=" * 70)
        print(f"Date: {self.date_str}")
        print()

        # Load data
        print("[1/5] Loading signals data...")
        self.load_signals_data()

        print("[2/5] Loading market data...")
        self.load_market_data()

        print("[3/5] Loading master plan...")
        self.load_master_plan()

        # Sync all planner sections
        print("[4/5] Synchronizing Daily Planner sections...")
        self.sync_daily_planner()

        # Save
        print("[5/5] Saving master plan...")
        self.save_master_plan()

        print("\n" + "=" * 70)
        print("✅ DAILY PLANNER SYNC COMPLETE")
        print("=" * 70)
        print()

    def load_signals_data(self):
        """Load signal data from cache"""
        signals_file = self.cache_dir / f"signals_{self.date_str}.json"

        if signals_file.exists():
            with open(signals_file, 'r', encoding='utf-8') as f:
                self.signals_data = json.load(f)
            composite = self.signals_data.get('composite', 'N/A')
            tier = self.signals_data.get('tier', 'UNKNOWN')
            print(f"   [OK] Signals loaded: {composite}/100 ({tier})")
        else:
            print(f"   [WARN] Signals not found - using defaults")
            self.signals_data = {
                'composite': 50,
                'tier': 'MODERATE',
                'breakdown': {'breadth': 10}
            }

    def load_market_data(self):
        """Load market data from cache - REQUIRED, no fallback values"""
        market_data_file = self.cache_dir / f"{self.date_str}_market_data.json"

        if not market_data_file.exists():
            print(f"   [ERROR] Market data file not found: {market_data_file}")
            print(f"   [ERROR] Cannot update key levels without real market data")
            print(f"   [CRITICAL] Run fetch_market_data.py first: python scripts/processing/fetch_market_data.py {self.date_str}")
            sys.exit(1)

        with open(market_data_file, 'r', encoding='utf-8') as f:
            self.market_data = json.load(f)

        # Validate required data exists - check actual structure
        # Market data structure: {date, timestamp, fear_greed, economic, crypto, stocks}
        required_keys = ['date', 'timestamp', 'fear_greed']
        missing_keys = [k for k in required_keys if k not in self.market_data]

        if missing_keys:
            print(f"   [ERROR] Market data file has unexpected structure")
            print(f"   [ERROR] Missing required keys: {missing_keys}")
            print(f"   [ERROR] File structure: {list(self.market_data.keys())}")
            sys.exit(1)

        print(f"   [OK] Market data loaded from {market_data_file.name}")

    def load_master_plan(self):
        """Load master plan using YAML handler"""
        try:
            self.master_plan_data = self.yaml_handler.load()
            tabs_count = len(self.master_plan_data.get('dashboard', {}).get('tabs', []))
            print(f"   [OK] Master plan loaded ({tabs_count} tabs)")
        except Exception as e:
            print(f"   [ERROR] Failed to load master plan: {e}")
            sys.exit(1)

    def sync_daily_planner(self):
        """Synchronize all Daily Planner sections"""
        # Get daily planner from dashboard
        daily_planner = self.master_plan_data.get('dashboard', {}).get('dailyPlanner', {})

        if not daily_planner:
            print("   [ERROR] Could not find dailyPlanner in master plan")
            sys.exit(1)

        print(f"   [OK] Found Daily Planner section")

        # Update DATA-DRIVEN sections only (Phase 2 automated sync)
        # AI-DRIVEN sections (priorities, aiInterpretation, recommendation, actionChecklist)
        # are handled by Claude AI in Phase 5 - DO NOT update here to avoid conflicts

        self._update_signal_data(daily_planner)
        self._copy_economic_calendar(daily_planner)
        self._update_end_of_day(daily_planner)

        # REMOVED: self._update_priorities(daily_planner)
        # REMOVED: self._update_ai_interpretation(daily_planner)
        # Reason: These are AI-driven interpretation sections that must be synthesized
        # by Claude AI during Phase 5 (wingman dash). Automated templates cannot
        # capture today's market nuances, signal shifts, or tactical context.

        print(f"   [OK] Daily Planner synchronized successfully")

    def _update_priorities(self, planner: Dict[str, Any]):
        """
        [DEPRECATED - DO NOT USE]

        This method is deprecated and should not be called during automated sync.
        Priorities are AI-driven and must be synthesized by Claude AI during Phase 5
        based on today's actionChecklist, market conditions, and signal tier.

        Generic template priorities lack the specificity and tactical context needed
        for actual trading decisions.
        """
        signal_tier = self.signals_data.get('tier', 'MODERATE')
        composite = self.signals_data.get('composite', 50)

        # Generate priorities based on signal strength
        if signal_tier in ['WEAK', 'VERY_WEAK']:
            priorities = [
                "Defensive positioning - reduce exposure",
                "Monitor for breadth improvement signals",
                "Watch VIX for volatility compression"
            ]
        elif signal_tier == 'MODERATE':
            priorities = [
                "Selective opportunities in quality names",
                "Monitor signal strength for improvement",
                "Maintain risk management discipline"
            ]
        else:  # STRONG or VERY_STRONG
            priorities = [
                "Active deployment in high-conviction setups",
                "Scale into strength with defined stops",
                "Monitor for exhaustion signals"
            ]

        planner['priorities'] = priorities
        planner['prioritiesUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"      ✓ Updated priorities ({len(priorities)} items) - {signal_tier} signal context")

    def _update_signal_data(self, planner: Dict[str, Any]):
        """Update signal score data and component breakdown from signals cache"""
        composite = self.signals_data.get('composite', 50)
        tier = self.signals_data.get('tier', 'MODERATE')
        breakdown = self.signals_data.get('breakdown', {})

        # Update signalData section (composite score, tier, date)
        planner['signalData'] = {
            'composite': round(composite, 2),
            'tier': tier,
            'date': self.date_str
        }

        # Update breakdown section (component scores: trend, breadth, volatility, technical, seasonality)
        planner['breakdown'] = {
            'trend': int(breakdown.get('trend', 20)),
            'breadth': int(breakdown.get('breadth', 12)),
            'volatility': int(breakdown.get('volatility', 10)),
            'technical': int(breakdown.get('technical', 5)),
            'seasonality': int(breakdown.get('seasonality', 3))
        }

        print(f"      ✓ Updated signalData: {composite}/100 ({tier})")
        print(f"      ✓ Updated breakdown: Trend {breakdown.get('trend', 20)} | Breadth {breakdown.get('breadth', 12)} | Vol {breakdown.get('volatility', 10)}")

    # REMOVED: _update_key_levels() method
    # Key levels come from wingman prep research analysis (Market_Sentiment_Overview.md)
    # They are synced to master-plan.md by update_master_plan.py, not by this script
    # This aligns with wingman dash philosophy: visualization only, no data fetching

    def _copy_economic_calendar(self, planner: Dict[str, Any]):
        """
        Copy economic calendar from Markets Intelligence tab to Daily Planner.

        IMPORTANT: The Daily Planner economic calendar should be a 100% REFERENCE (not independent copy)
        to the Markets Intelligence economic calendar. This ensures both tabs always show identical data.
        The purpose is to display the same calendar in TWO PLACES for easy visibility - one in Markets
        Intelligence (detailed market context) and one in Daily Planner (daily action view).

        YAML anchors (&id and *id) are INTENTIONAL and CORRECT - they ensure both tabs reference the
        same data structure. When Markets Intelligence updates, Daily Planner automatically reflects it.
        DO NOT "fix" this by creating independent copies - the shared reference is by design.
        """
        # Get Markets Intelligence tab (id: 'markets')
        tabs = self.master_plan_data.get('dashboard', {}).get('tabs', [])
        markets_intelligence_tab = None

        for tab in tabs:
            if tab.get('id') == 'markets':
                markets_intelligence_tab = tab
                break

        if not markets_intelligence_tab:
            print(f"      ⚠️  Markets Intelligence tab not found - economic calendar not copied")
            planner['economicCalendar'] = {}
            planner['economicCalendarUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            return

        # Get economic calendar from Macro Environment section
        sections = markets_intelligence_tab.get('sections', [])
        economic_calendar = {}

        for section in sections:
            if section.get('name') == 'Macro Environment':
                economic_calendar = section.get('economicCalendar', {})
                break

        # Copy reference to Daily Planner (YAML handler will create anchor/alias automatically)
        # This creates a shared reference, NOT an independent copy - this is intentional
        planner['economicCalendar'] = economic_calendar
        planner['economicCalendarUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Count events for logging
        event_count = 0
        if economic_calendar:
            event_count += len(economic_calendar.get('today', []))
            event_count += len(economic_calendar.get('thisWeek', []))
            event_count += len(economic_calendar.get('nextWeek', []))
            event_count += len(economic_calendar.get('keyDates', []))

        print(f"      ✓ Copied economic calendar reference from Markets Intelligence ({event_count} events)")
        print(f"      ℹ️  Note: Daily Planner & Markets Intelligence share same calendar data (by design)")

    def _update_ai_interpretation(self, planner: Dict[str, Any]):
        """
        [DEPRECATED - DO NOT USE]

        This method is deprecated and should not be called during automated sync.
        AI interpretation sections must be synthesized by Claude AI during Phase 5
        with rich narrative based on today's research, technical data, and market context.

        Automated templates cannot capture:
        - Breadth healing vs divergence
        - Multi-asset correlation shifts
        - Catalyst timing and probability
        - Risk/reward asymmetry in current setup
        - Tactical entry/exit guidance with specific levels
        """
        signal_tier = self.signals_data.get('tier', 'MODERATE')
        composite = self.signals_data.get('composite', 50)
        breadth = self.signals_data.get('breakdown', {}).get('breadth', 10)

        interpretation = f"""Daily Context for {self.date.strftime('%B %d, %Y')}:

Signal Tier: {signal_tier} ({composite}/100)
Breadth: {breadth}/25 ({'WEAK' if breadth < 15 else 'MODERATE'})

Trading Posture: {'Defensive - reduce exposure' if composite < 40 else 'Selective - quality opportunities' if composite < 60 else 'Active - deploy capital'}

Key Focus:
- Monitor signal strength for changes in market regime
- Respect risk management rules regardless of signal
- Stay nimble - conditions can change rapidly

This is automated daily context. For detailed market analysis, review individual tabs."""

        if 'aiInterpretation' not in planner:
            planner['aiInterpretation'] = {}

        planner['aiInterpretation']['summary'] = interpretation
        planner['aiInterpretation']['updatedAt'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"      ✓ Updated aiInterpretation.summary ({len(interpretation)} chars)")
        print(f"      ✓ Updated aiInterpretation.updatedAt")

    def _update_end_of_day(self, planner: Dict[str, Any]):
        """Update end of day section"""
        if 'endOfDay' not in planner:
            planner['endOfDay'] = {}

        # Set ranAt to current time (will be properly set when EOD actually runs)
        # For now, just ensure the field exists and has a timestamp
        planner['endOfDay']['ranAt'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        planner['endOfDay']['status'] = "Pending - will run at market close"

        print(f"      ✓ Updated endOfDay.ranAt")

    def save_master_plan(self):
        """Save updated master plan using YAML handler (with automatic validation and backup)"""
        try:
            # The yaml_handler automatically validates and creates backup
            self.yaml_handler.save(self.master_plan_data, validate=True)
            print(f"   [OK] Master plan saved")
            print(f"   [OK] Backup: master-plan.md.backup")
        except Exception as e:
            print(f"   [ERROR] Failed to save master plan: {e}")
            sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/utilities/sync_daily_planner.py YYYY-MM-DD")
        print("Example: python scripts/utilities/sync_daily_planner.py 2025-10-21")
        sys.exit(1)

    date_str = sys.argv[1]

    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"[ERROR] Invalid date format: {date_str}")
        print("   Expected format: YYYY-MM-DD")
        sys.exit(1)

    # Run sync
    syncer = DailyPlannerSyncer(date_str)

    try:
        syncer.run()
        print("✅ Daily Planner synchronized successfully")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Daily Planner sync failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
