#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Plan Updater - Pure Automation
======================================

Updates master-plan.md with new date and signal data.
Pure script - no AI needed for deterministic updates.

Usage:
    python scripts/automation/update_master_plan.py 2025-10-10

Updates:
    - All dates (pageTitle, dateBadge, headers, footer)
    - All tab timestamps
    - Signal data from JSON
    - X sentiment from JSON
    - Sentiment history
    - HTML dashboard

Input:
    - Research/.cache/signals_YYYY-MM-DD.json
    - Research/X/Trends/YYYY-MM-DD_trending_words.json (optional)

Output:
    - Updated master-plan/master-plan.md
    - Updated master-plan/research-dashboard.html
    - Updated Research/.processing_log.json
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

# Import dashboard automation functions
sys.path.insert(0, str(Path(__file__).parent.parent / "utilities"))
from _dashboard_automation import update_sentiment_cards, update_metrics, update_quick_actions

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


class MasterPlanUpdater:
    """Updates master plan with new date and signal data"""

    def __init__(self, date_str: str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d")
        self.date_str = date_str
        self.date_display = self.date.strftime('%B %d, %Y')  # "October 10, 2025"

        # Get repo root (absolute paths work regardless of execution directory)
        # Path(__file__) = .../scripts/automation/update_master_plan.py
        # .parents[2] = .../repo_root
        repo_root = Path(__file__).resolve().parents[2]

        # Paths - ABSOLUTE (work from any directory)
        self.master_plan_file = repo_root / "master-plan" / "master-plan.md"
        self.html_dashboard_file = repo_root / "master-plan" / "research-dashboard.html"
        self.processing_log_file = repo_root / "Research" / ".processing_log.json"
        self.cache_dir = repo_root / "Research" / ".cache"

        # Data
        self.signals: Optional[Dict] = None
        self.trending_words: Optional[Dict] = None
        self.options_meta: Optional[Dict[str, Any]] = None
        self.options_data: Dict[str, Dict[str, Any]] = {}
        self.market_data: Optional[Dict] = None
        self.master_plan_content: Optional[str] = None

    def load_data(self):
        """Load all required data"""
        print(f"\n[*] Loading data for {self.date_str}")
        print("=" * 60)

        # Load signals JSON
        signals_file = self.cache_dir / f"signals_{self.date_str}.json"
        if not signals_file.exists():
            raise FileNotFoundError(
                f"Signals not found: {signals_file}\n"
                f"Run: python scripts/processing/calculate_signals.py {self.date_str}"
            )

        with open(signals_file) as f:
            self.signals = json.load(f)

        print(f"   [OK] Signals loaded (composite: {self.signals['composite']}/100)")

        # Load trending words (optional)
        trending_file = Path("Research/X/Trends") / f"{self.date_str}_trending_words.json"
        if trending_file.exists():
            with open(trending_file) as f:
                self.trending_words = json.load(f)
            print(f"   [OK] Trending words loaded")
        else:
            print(f"   [WARN] Trending words not found (optional)")

        # Load options data (optional)
        options_file = self.cache_dir / f"{self.date_str}_options_data.json"
        if options_file.exists():
            with open(options_file) as f:
                raw_options = json.load(f)

            if isinstance(raw_options, dict) and "tickers" in raw_options:
                self.options_meta = raw_options
                self.options_data = raw_options.get("tickers", {})
            else:
                # Backward compatibility with legacy single-ticker format
                self.options_meta = None
                self.options_data = {"SPY": raw_options} if raw_options else {}

            if self.options_data:
                preview = ", ".join(
                    f"{ticker} maxPain {metrics.get('maxPain', 'N/A')}"
                    for ticker, metrics in self.options_data.items()
                )
                print(f"   [OK] Options data loaded ({preview})")
            else:
                print(f"   [WARN] Options JSON present but empty")
        else:
            print(f"   [WARN] Options data not found (optional)")

        # Load market data (optional)
        market_data_file = self.cache_dir / f"{self.date_str}_market_data.json"
        if market_data_file.exists():
            with open(market_data_file) as f:
                self.market_data = json.load(f)
            print(f"   [OK] Market data loaded")
        else:
            print(f"   [WARN] Market data not found (optional)")

        # Load master plan
        if not self.master_plan_file.exists():
            raise FileNotFoundError(f"Master plan not found: {self.master_plan_file}")

        with open(self.master_plan_file, encoding='utf-8') as f:
            self.master_plan_content = f.read()

        print(f"   [OK] Master plan loaded ({len(self.master_plan_content)} chars)")
        print()

    def update_all(self):
        """Run all updates"""
        print("[*] Updating master plan...")
        print("=" * 60)

        # Track what was updated
        updates = []

        # 1. Update dates
        print("\n[1/8] Updating dates...")
        self.update_page_title()
        updates.append("pageTitle")

        self.update_date_badge()
        updates.append("dateBadge")

        self.update_eagle_eye_header()
        updates.append("EAGLE EYE header")

        self.update_footer_dates()
        updates.append("footer dates")

        # 2. Update tab timestamps
        print("\n[2/8] Updating tab timestamps...")
        self.update_tab_timestamps()
        self.update_additional_updated_at()
        # NOTE: We do NOT auto-update section timestamps (*Updated fields)
        # They should remain stale to indicate which sections need manual AI updates
        # Run verify_timestamps.py at end of workflow to see what needs updating
        updates.append("tab timestamps")
        updates.append("additional updatedAt fields")

        # 2.5. Update economic calendar
        print("\n[2.5/8] Updating economic calendar...")
        self.update_economic_calendar()
        updates.append("economicCalendar")

        # 3. Update signal data
        print("\n[3/8] Updating signal data...")
        self.update_signal_data()
        self.update_end_of_day_signals()
        self.update_end_of_day_metadata()
        updates.append("signalData")
        updates.append("endOfDay signals")
        updates.append("endOfDay metadata")

        # 4. Update sentiment history
        print("\n[4/8] Updating sentiment history...")
        self.update_sentiment_history()
        updates.append("sentimentHistory")

        # 4.5. Auto-update dashboard sections (Market Sentiment Overview)
        print("\n[4.5/8] Auto-updating dashboard sections...")
        self.update_sentiment_cards()
        self.update_metrics()
        self.update_quick_actions()
        updates.append("sentimentCards")
        updates.append("metrics")
        updates.append("quickActions")

        # 5. Update X sentiment (if available)
        if self.trending_words:
            print("\n[5/9] Updating X sentiment...")
            self.update_x_sentiment()
            updates.append("xSentiment")
        else:
            print("\n[5/9] Skipping X sentiment (no trending words)")

        # 5.5. Update options data (if available)
        if self.options_data:
            print("\n[5.5/9] Updating options data...")
            self.update_options_data()
            updates.append("optionsData")
        else:
            print("\n[5.5/9] Skipping options data (not available)")

        # 6. Update daily planner metadata
        print("\n[6/9] Updating daily planner metadata...")
        self.update_daily_planner_metadata()
        updates.append("dailyPlanner metadata")

        # 7. Save master plan
        print("\n[7/9] Saving master plan...")
        self.save_master_plan()

        # 8. Update supporting files
        print("\n[8/9] Updating supporting files...")
        self.update_html_dashboard()
        self.update_processing_log()
        updates.append("HTML dashboard")
        updates.append("processing log")

        print(f"\n[OK] Master plan updated successfully!")
        print(f"     Updated {len(updates)} sections: {', '.join(updates)}")

        return updates

    def update_page_title(self):
        """Update pageTitle in YAML front matter"""
        # Match YAML format: pageTitle: "value"
        pattern = r'(pageTitle:\s*"Investment Research Dashboard - )[^"]+'
        replacement = rf'\1{self.date_display}'

        updated_content, replacements = re.subn(
            pattern,
            replacement,
            self.master_plan_content
        )

        if replacements:
            self.master_plan_content = updated_content
            print(f"   [OK] pageTitle updated to {self.date_display}")
        else:
            print(f"   [WARN] pageTitle pattern did not match - check YAML format")

    def update_date_badge(self):
        """Update dateBadge in YAML front matter"""
        # Match YAML format: dateBadge: "value"
        pattern = r'(dateBadge:\s*")[^"]+'
        replacement = rf'\1{self.date_display}'

        updated_content, replacements = re.subn(
            pattern,
            replacement,
            self.master_plan_content
        )

        if replacements:
            self.master_plan_content = updated_content
            print(f"   [OK] dateBadge updated to {self.date_display}")
        else:
            print(f"   [WARN] dateBadge pattern did not match - check YAML format")

    def update_eagle_eye_header(self):
        """Update EAGLE EYE MACRO OVERVIEW header"""
        pattern = r'##\s*🎯\s*EAGLE EYE MACRO OVERVIEW\s*\([^)]+\)'
        replacement = f'## 🎯 EAGLE EYE MACRO OVERVIEW ({self.date_display})'

        self.master_plan_content = re.sub(
            pattern,
            replacement,
            self.master_plan_content,
            flags=re.IGNORECASE
        )

        print(f"   [OK] EAGLE EYE header updated")

    def update_footer_dates(self):
        """Update footer dates (Last Updated, Next Review)"""
        # Last Updated
        pattern1 = r'\*Last Updated:\s*[^\*]+\*'
        replacement1 = f'*Last Updated: {self.date_display} - COMPREHENSIVE {self.date_display.upper()} MARKET INTELLIGENCE UPDATE*'

        self.master_plan_content = re.sub(
            pattern1,
            replacement1,
            self.master_plan_content
        )

        # Next Review (7 days from now)
        next_review = (self.date + timedelta(days=7)).strftime('%B %d, %Y')
        pattern2 = r'\*Next Review:\s*[^\*]+\*'
        replacement2 = f'*Next Review: {next_review} (Weekly tactical review)*'

        self.master_plan_content = re.sub(
            pattern2,
            replacement2,
            self.master_plan_content
        )

        print(f"   [OK] Footer dates updated")

    def update_tab_timestamps(self):
        """Update all tab updatedAt timestamps"""
        # Preserve existing time component, only replace the date
        tab_ids = ['markets', 'news_catalysts', 'xsentiment', 'technicals']
        replacements = 0

        for tab_id in tab_ids:
            pattern = rf'("id":\s*"{tab_id}"[^}}]*"updatedAt":\s*")(\d{{4}}-\d{{2}}-\d{{2}})(T[^"]+")'

            def repl(match):
                nonlocal replacements
                replacements += 1
                time_part = match.group(3)
                return f'{match.group(1)}{self.date_str}{time_part}'

            self.master_plan_content = re.sub(
                pattern,
                repl,
                self.master_plan_content,
                flags=re.DOTALL
            )

        if replacements:
            print(f"   [OK] Updated {replacements} tab timestamps to {self.date_str}")
        else:
            print(f"   [WARN] No tab timestamps updated")

    def update_economic_calendar(self):
        """Update economic calendar from CSV file"""
        import sys
        from pathlib import Path

        # Add processing directory to path
        processing_path = Path(__file__).parent.parent / "processing"
        if str(processing_path) not in sys.path:
            sys.path.insert(0, str(processing_path))

        try:
            from parse_economic_calendar import parse_calendar

            # Parse calendar CSV
            calendar_data = parse_calendar()
            event_count = (
                len(calendar_data.get('today', [])) +
                len(calendar_data.get('thisWeek', [])) +
                len(calendar_data.get('nextWeek', []))
            )

            # Find Markets Intelligence tab -> Macro Environment section
            tabs = self.master_plan_data.get('dashboard', {}).get('tabs', [])
            markets_tab = None

            for tab in tabs:
                if tab.get('id') == 'markets':
                    markets_tab = tab
                    break

            if not markets_tab:
                print(f"   [WARN] Markets Intelligence tab not found")
                return

            sections = markets_tab.get('sections', [])
            macro_section = None

            for section in sections:
                if 'macro' in section.get('name', '').lower():
                    macro_section = section
                    break

            if not macro_section:
                print(f"   [WARN] Macro Environment section not found")
                return

            # Update calendar
            macro_section['economicCalendar'] = calendar_data
            print(f"   [OK] Updated {event_count} events in economic calendar")
            print(f"   [OK] Summary: {calendar_data.get('summary', 'N/A')[:80]}...")

        except Exception as e:
            print(f"   [WARN] Failed to update economic calendar: {e}")
            print(f"   [INFO] Calendar will remain unchanged")

    def update_signal_data(self):
        """Update signalData section from signals JSON"""
        # Find the signalData section
        pattern = r'"signalData":\s*\{[^}]*"composite":[^}]*\}'

        # Build replacement JSON
        signal_json = {
            "composite": self.signals['composite'],
            "tier": self.signals['tier'],
            "date": self.date_str
        }

        replacement = f'"signalData": {json.dumps(signal_json)}'

        self.master_plan_content = re.sub(
            pattern,
            replacement,
            self.master_plan_content
        )

        print(f"   [OK] signalData updated (composite: {self.signals['composite']}/100, tier: {self.signals['tier']})")

    def update_end_of_day_signals(self):
        """Keep endOfDay.signals in sync with current composite/tier"""
        pattern = r'("endOfDay":\s*\{.*?"signals":\s*\{\s*"composite":\s*)(\d+\.?\d*)(,\s*"tier":\s*")[^"]+'

        def repl(match):
            new_composite = f"{self.signals['composite']}"
            new_tier = self.signals['tier']
            return f"{match.group(1)}{new_composite}{match.group(3)}{new_tier}"

        updated_content, replacements = re.subn(
            pattern,
            repl,
            self.master_plan_content,
            flags=re.DOTALL
        )

        if replacements:
            self.master_plan_content = updated_content
            print(f"   [OK] endOfDay signals updated ({self.signals['composite']}/100, {self.signals['tier']})")
        else:
            print("   [WARN] endOfDay signals block not updated")

    def update_end_of_day_metadata(self):
        """Update endOfDay date, ranAt, and summary references"""
        # Update display date
        pattern_date = r'("endOfDay":\s*\{[^}]*"date":\s*")[^"]+"'
        replacement_date = rf'\1{self.date_display}"'
        self.master_plan_content = re.sub(
            pattern_date,
            replacement_date,
            self.master_plan_content,
            flags=re.DOTALL
        )

        # Update ranAt date while preserving time
        pattern_ran = r'("endOfDay":\s*\{[^}]*"ranAt":\s*")(\d{4}-\d{2}-\d{2})(T[^"]+")'

        def repl_ran(match):
            return f'{match.group(1)}{self.date_str}{match.group(3)}'

        self.master_plan_content = re.sub(
            pattern_ran,
            repl_ran,
            self.master_plan_content,
            flags=re.DOTALL
        )

        # Update summary date reference if present
        pattern_summary = r'(Master plan updated with )[A-Za-z]+\s+\d{1,2},\s+\d{4}( data)'
        replacement_summary = rf'\1{self.date_display}\2'
        self.master_plan_content = re.sub(
            pattern_summary,
            replacement_summary,
            self.master_plan_content
        )

        print(f"   [OK] endOfDay metadata updated ({self.date_display})")

    def update_additional_updated_at(self):
        """Update standalone updatedAt fields to target date"""
        pattern = r'("updatedAt":\s*")(\d{4}-\d{2}-\d{2})(T[^"]+")'

        def repl(match):
            return f'{match.group(1)}{self.date_str}{match.group(3)}'

        self.master_plan_content, replacements = re.subn(
            pattern,
            repl,
            self.master_plan_content
        )

        if replacements:
            print(f"   [OK] updatedAt fields refreshed ({replacements} occurrences)")
        else:
            print("   [WARN] No additional updatedAt fields found")

    def update_section_timestamps(self):
        """Update all *Updated timestamp fields (sentimentCardsUpdated, metricsUpdated, etc.)"""
        # List of section timestamp fields to update
        timestamp_fields = [
            'sentimentCardsUpdated',
            'sentimentHistoryUpdated',
            'metricsUpdated',
            'riskItemsUpdated',
            'quickActionsUpdated',
            'providerConsensusUpdated',
            'prioritiesUpdated',
            'keyLevelsUpdated',
            'scheduledEventsUpdated'
        ]

        replacements = 0
        for field in timestamp_fields:
            pattern = rf'("{field}":\s*")(\d{{4}}-\d{{2}}-\d{{2}})(T[^"]+")'

            def repl(match):
                nonlocal replacements
                replacements += 1
                return f'{match.group(1)}{self.date_str}{match.group(3)}'

            self.master_plan_content = re.sub(
                pattern,
                repl,
                self.master_plan_content
            )

        if replacements:
            print(f"   [OK] Section timestamps updated ({replacements} fields to {self.date_str})")
        else:
            print("   [WARN] No section timestamp fields found")

    def update_daily_planner_metadata(self):
        """Update daily planner timestamps to target date"""
        pattern = r'("dailyPlanner":\s*\{\s*"aiInterpretation":\s*\{\s*"updatedAt":\s*")(\d{4}-\d{2}-\d{2})(T[^"]+")'

        def repl(match):
            return f'{match.group(1)}{self.date_str}{match.group(3)}'

        updated_content, replacements = re.subn(
            pattern,
            repl,
            self.master_plan_content,
            flags=re.DOTALL
        )

        if replacements:
            self.master_plan_content = updated_content
            print(f"   [OK] daily planner updatedAt set to {self.date_str}")
        else:
            print("   [WARN] daily planner updatedAt not found")

    def update_sentiment_history(self):
        """Add new entry to sentimentHistory array"""
        # Find sentimentHistory array
        pattern = r'"sentimentHistory":\s*\[(.*?)\]'

        match = re.search(pattern, self.master_plan_content, re.DOTALL)
        if not match:
            print(f"   [WARN] sentimentHistory array not found")
            return

        existing_history = match.group(1)

        # Create new entry
        new_entry = {
            "date": self.date_str,
            "score": int(self.signals['composite']),
            "label": self.signals['tier']
        }

        # Check if this date already exists
        if f'"{self.date_str}"' in existing_history:
            print(f"   [WARN] Date {self.date_str} already in history, skipping")
            return

        # Add new entry at the end
        new_entry_str = json.dumps(new_entry)

        # Build new history (add comma if history not empty)
        if existing_history.strip():
            new_history = f'{existing_history},\n    {new_entry_str}'
        else:
            new_history = f'\n    {new_entry_str}\n  '

        # Replace
        replacement = f'"sentimentHistory": [{new_history}]'

        self.master_plan_content = re.sub(
            pattern,
            replacement,
            self.master_plan_content,
            flags=re.DOTALL
        )

        print(f"   [OK] Added to sentimentHistory: {self.date_str} - {self.signals['composite']}/100 ({self.signals['tier']})")

    def update_x_sentiment(self):
        """Update xSentiment string references"""
        if not self.signals.get('x_sentiment'):
            print(f"   [WARN] No X sentiment in signals JSON")
            return

        x_crypto = self.signals['x_sentiment'].get('crypto', 50)
        x_macro = self.signals['x_sentiment'].get('macro', 50)

        # Determine labels
        crypto_label = self.get_sentiment_label(x_crypto)
        macro_label = self.get_sentiment_label(x_macro)

        # Format string
        x_sentiment_str = f"Crypto {x_crypto}/100 ({crypto_label}), Macro {x_macro}/100 ({macro_label})"

        # Update in JSON front matter
        pattern = r'"xSentiment":\s*"[^"]+"'
        replacement = f'"xSentiment": "{x_sentiment_str}"'

        self.master_plan_content = re.sub(
            pattern,
            replacement,
            self.master_plan_content
        )

        print(f"   [OK] xSentiment updated: {x_sentiment_str}")

    def get_sentiment_label(self, score: int) -> str:
        """Get sentiment label from score"""
        if score >= 80:
            return "VERY BULLISH"
        elif score >= 60:
            return "BULLISH"
        elif score >= 40:
            return "NEUTRAL"
        elif score >= 20:
            return "BEARISH"
        else:
            return "VERY BEARISH"

    def update_options_data(self):
        """Update optionsData section in technicals tab"""
        if not self.options_data:
            print(f"   [WARN] No options data available")
            return

        def build_block(ticker: str, metrics: Dict[str, Any]) -> str:
            def fmt_price(value: Any) -> str:
                if isinstance(value, (int, float)):
                    return f"{value:.2f}".rstrip("0").rstrip(".")
                return str(value) if value is not None else "N/A"

            lines = [
                f"        {ticker}:",
                f'          lastUpdated: "{metrics.get("lastUpdated", "N/A")}"',
            ]

            current_price = metrics.get("currentPrice")
            if current_price is not None:
                lines.append(f"          currentPrice: {fmt_price(current_price)}")

            if metrics.get("expiration"):
                lines.append(f'          expiration: "{metrics["expiration"]}"')

            for key in ("maxPain", "putCallRatio", "ivPercentile", "totalOI"):
                if metrics.get(key) is not None:
                    lines.append(f'          {key}: "{metrics[key]}"')

            key_levels = metrics.get("keyLevels") or []
            if key_levels:
                lines.append("          keyLevels:")
                for level in key_levels[:8]:
                    strike = level.get("strike", "")
                    level_type = level.get("type", "")
                    gamma = level.get("gamma", "N/A")
                    oi = level.get("oi", "N/A")
                    lines.append(f'            - strike: "{strike}"')
                    lines.append(f'              type: "{level_type}"')
                    lines.append(f'              gamma: "{gamma}"')
                    lines.append(f'              oi: "{oi}"')
            else:
                lines.append("          keyLevels: []")

            source = metrics.get("source")
            if source:
                lines.append(f'          source: "{source}"')

            return "\n".join(lines) + "\n"

        updated_any = False
        for ticker, metrics in self.options_data.items():
            block = build_block(ticker, metrics)
            pattern = rf'(        {re.escape(ticker)}:\n(?:\s{{10,}}.*\n)*)'
            self.master_plan_content, count = re.subn(pattern, block, self.master_plan_content)
            if count == 0:
                # Insert new ticker block right after optionsData header
                insert_pattern = r'(optionsData:\s*\n)'
                replacement = rf'\1{block}'
                self.master_plan_content, insert_count = re.subn(insert_pattern, replacement, self.master_plan_content, count=1)
                if insert_count:
                    print(f"   [OK] Added new options block for {ticker}")
                    updated_any = True
                else:
                    print(f"   [WARN] Could not locate insertion point for {ticker} block")
            else:
                print(f"   [OK] Options block updated for {ticker}")
                updated_any = True

        if updated_any:
            summary = ", ".join(
                f"{ticker}: maxPain {metrics.get('maxPain', 'N/A')} / P/C {metrics.get('putCallRatio', 'N/A')}"
                for ticker, metrics in self.options_data.items()
            )
            print(f"   [OK] Options metrics refreshed ({summary})")
        else:
            print("   [WARN] No optionsData updates were applied")

    # Dashboard automation methods (delegated to imported functions)
    def update_sentiment_cards(self):
        """Auto-generate sentimentCards based on signal tier and market data"""
        update_sentiment_cards(self)

    def update_metrics(self):
        """Auto-generate metrics based on market data"""
        update_metrics(self)

    def update_quick_actions(self):
        """Auto-generate quickActions based on signal tier"""
        update_quick_actions(self)

    def save_master_plan(self):
        """Save updated master plan"""
        # Create backup first
        backup_file = self.master_plan_file.with_suffix('.md.backup')
        with open(self.master_plan_file, encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(backup_content)

        # Save updated content
        with open(self.master_plan_file, 'w', encoding='utf-8') as f:
            f.write(self.master_plan_content)

        print(f"   [OK] Master plan saved")
        print(f"   [OK] Backup created: {backup_file}")

    def update_html_dashboard(self):
        """Update HTML dashboard title"""
        if not self.html_dashboard_file.exists():
            print(f"   [WARN] HTML dashboard not found: {self.html_dashboard_file}")
            return

        with open(self.html_dashboard_file, encoding='utf-8') as f:
            html_content = f.read()

        # Update title tag
        pattern = r'<title>Investment Research Dashboard - [^<]+</title>'
        replacement = f'<title>Investment Research Dashboard - {self.date_display}</title>'

        html_content = re.sub(pattern, replacement, html_content)

        # Save
        with open(self.html_dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"   [OK] HTML dashboard updated")

    def update_processing_log(self):
        """Update .processing_log.json"""
        if not self.processing_log_file.exists():
            log = {}
        else:
            with open(self.processing_log_file) as f:
                log = json.load(f)

        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        log['last_updated'] = timestamp
        log['last_master_plan_update'] = {
            'date': self.date_str,
            'timestamp': timestamp,
            'composite_score': self.signals['composite'],
            'tier': self.signals['tier']
        }

        log['notes'] = (
            f"Master plan updated for {self.date_str}. "
            f"Signal: {self.signals['composite']}/100 ({self.signals['tier']}). "
            f"Automated update via update_master_plan.py."
        )

        # Save
        with open(self.processing_log_file, 'w') as f:
            json.dump(log, f, indent=2)

        print(f"   [OK] Processing log updated")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/automation/update_master_plan.py YYYY-MM-DD")
        print("Example: python scripts/automation/update_master_plan.py 2025-10-10")
        sys.exit(1)

    date_str = sys.argv[1]

    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"[ERROR] Invalid date format: {date_str}")
        print("   Expected format: YYYY-MM-DD")
        sys.exit(1)

    # Update master plan
    updater = MasterPlanUpdater(date_str)

    try:
        updater.load_data()
        updates = updater.update_all()

        # Summary
        print("\n" + "=" * 60)
        print("[*] MASTER PLAN UPDATE COMPLETE")
        print("=" * 60)
        print(f"Date: {updater.date_display}")
        print(f"Signal: {updater.signals['composite']}/100 ({updater.signals['tier']})")
        print(f"Updates: {len(updates)} sections modified")
        print(f"\nFiles updated:")
        print(f"  - master-plan/master-plan.md")
        print(f"  - master-plan/research-dashboard.html")
        print(f"  - Research/.processing_log.json")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
