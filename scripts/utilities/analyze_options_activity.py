#!/usr/bin/env python3
"""
Options Activity Analyzer
==========================

Detects unusual options activity by comparing current data vs historical data.
Identifies put/call ratio spikes, volume spikes, IV extremes, and max pain shifts.

Usage:
    analyzer = OptionsActivityAnalyzer('2025-10-26')
    alerts = analyzer.analyze()
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class OptionsActivityAnalyzer:
    """Analyzes options activity for unusual patterns"""

    def __init__(self, date_str: str = None, cache_dir: str = None):
        """Initialize analyzer

        Args:
            date_str: Date in YYYY-MM-DD format (defaults to today)
            cache_dir: Cache directory path (defaults to Research/.cache)
        """
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')

        self.date_str = date_str
        self.date = datetime.strptime(date_str, '%Y-%m-%d')
        self.cache_dir = Path(cache_dir or 'Research/.cache')

        self.today_data = None
        self.yesterday_data = None
        self.alerts = {'SPY': [], 'QQQ': []}

        # Detection thresholds
        self.SPIKE_THRESHOLD = 20  # 20% change = SPIKE
        self.ELEVATED_THRESHOLD = 10  # 10% change = ELEVATED
        self.PCR_EXTREME_HIGH = 1.8  # P/C ratio > 1.8 = bearish
        self.PCR_EXTREME_LOW = 0.6  # P/C ratio < 0.6 = bullish
        self.IV_PERCENTILE_HIGH = 80  # IV > 80th percentile = high
        self.IV_PERCENTILE_LOW = 20  # IV < 20th percentile = low
        self.MAX_PAIN_SHIFT = 5  # $5 shift = potential repositioning

    def load_technical_data(self, date_str: str) -> Optional[Dict]:
        """Load technical data from cache"""
        cache_file = self.cache_dir / f"{date_str}_technical_data.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"   [Analyzer] ⚠️  Could not load {cache_file}: {e}")
            return None

    def load_today_and_yesterday(self):
        """Load current and previous day's data"""
        self.today_data = self.load_technical_data(self.date_str)

        yesterday = self.date - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        self.yesterday_data = self.load_technical_data(yesterday_str)

        if not self.today_data:
            raise ValueError(f"No technical data found for {self.date_str}")

    def parse_ratio(self, value: str) -> Optional[float]:
        """Parse put/call ratio string to float"""
        try:
            return float(str(value).strip())
        except (ValueError, TypeError, AttributeError):
            return None

    def parse_price(self, value: str) -> Optional[float]:
        """Parse price string to float"""
        try:
            return float(str(value).replace('$', '').strip())
        except (ValueError, TypeError, AttributeError):
            return None

    def parse_percentage(self, value: str) -> Optional[float]:
        """Parse percentage string to float"""
        try:
            return float(str(value).replace('%', '').strip())
        except (ValueError, TypeError, AttributeError):
            return None

    def parse_volume(self, value: str) -> Optional[int]:
        """Parse volume string to int"""
        try:
            return int(str(value).replace(',', '').strip())
        except (ValueError, TypeError, AttributeError):
            return None

    def calculate_change_pct(self, current: float, previous: float) -> float:
        """Calculate percentage change"""
        if not previous or previous == 0:
            return 0
        return ((current - previous) / previous) * 100

    def classify_status(self, change_pct: float, absolute_value: float = None) -> str:
        """Classify alert status based on change percentage

        Returns: 'SPIKE', 'ELEVATED', 'NORMAL'
        """
        # Check for extreme absolute values first
        if absolute_value is not None:
            if 1.5 <= absolute_value <= 1.8:
                return 'ELEVATED'
            elif absolute_value > 1.8 or absolute_value < 0.6:
                return 'SPIKE'

        # Check percentage change
        if abs(change_pct) >= self.SPIKE_THRESHOLD:
            return 'SPIKE'
        elif abs(change_pct) >= self.ELEVATED_THRESHOLD:
            return 'ELEVATED'
        else:
            return 'NORMAL'

    def analyze_pcr(self, ticker: str):
        """Analyze Put/Call Ratio changes"""
        today_opt = self.today_data.get(f'{ticker.lower()}_options', {})
        today_pcr = self.parse_ratio(today_opt.get('putCallRatio'))

        if not today_pcr:
            return

        # If no yesterday data, still flag if extreme
        if not self.yesterday_data:
            if today_pcr > self.PCR_EXTREME_HIGH:
                self.alerts[ticker].append({
                    'metric': 'putCallRatio',
                    'current': today_pcr,
                    'previous': None,
                    'change': None,
                    'status': 'ELEVATED',
                    'signal': f'Defensive positioning (P/C {today_pcr:.2f})',
                    'direction': 'bearish'
                })
            elif today_pcr < self.PCR_EXTREME_LOW:
                self.alerts[ticker].append({
                    'metric': 'putCallRatio',
                    'current': today_pcr,
                    'previous': None,
                    'change': None,
                    'status': 'ELEVATED',
                    'signal': f'Bullish positioning (P/C {today_pcr:.2f})',
                    'direction': 'bullish'
                })
            return

        yesterday_opt = self.yesterday_data.get(f'{ticker.lower()}_options', {})
        yesterday_pcr = self.parse_ratio(yesterday_opt.get('putCallRatio'))

        if not yesterday_pcr:
            return

        change_pct = self.calculate_change_pct(today_pcr, yesterday_pcr)
        status = self.classify_status(change_pct, today_pcr)

        if status != 'NORMAL':
            direction = 'bearish' if today_pcr > yesterday_pcr else 'bullish'
            signal = f'{"High" if today_pcr > 1.5 else "Elevated"} defensive positioning'
            if abs(change_pct) >= self.SPIKE_THRESHOLD:
                signal = f'SPIKE: Put buying intensifying (+{change_pct:.1f}%)'

            self.alerts[ticker].append({
                'metric': 'putCallRatio',
                'current': f'{today_pcr:.2f}',
                'previous': f'{yesterday_pcr:.2f}',
                'change': f'{change_pct:+.1f}%',
                'status': status,
                'signal': signal,
                'direction': direction
            })

    def analyze_volume(self, ticker: str):
        """Analyze options volume changes"""
        today_opt = self.today_data.get(f'{ticker.lower()}_options', {})
        today_put_vol = self.parse_volume(today_opt.get('putVolume'))
        today_call_vol = self.parse_volume(today_opt.get('callVolume'))

        if not today_put_vol or not today_call_vol:
            return

        today_total = today_put_vol + today_call_vol

        # If no yesterday data, can't compare
        if not self.yesterday_data:
            return

        yesterday_opt = self.yesterday_data.get(f'{ticker.lower()}_options', {})
        yesterday_put_vol = self.parse_volume(yesterday_opt.get('putVolume'))
        yesterday_call_vol = self.parse_volume(yesterday_opt.get('callVolume'))

        if not yesterday_put_vol or not yesterday_call_vol:
            return

        yesterday_total = yesterday_put_vol + yesterday_call_vol

        vol_change_pct = self.calculate_change_pct(today_total, yesterday_total)
        status = self.classify_status(vol_change_pct)

        if status != 'NORMAL':
            self.alerts[ticker].append({
                'metric': 'totalVolume',
                'current': f'{today_total:,.0f}',
                'previous': f'{yesterday_total:,.0f}',
                'change': f'{vol_change_pct:+.1f}%',
                'status': status,
                'signal': f'Options volume {"elevated" if vol_change_pct > 0 else "depressed"}',
                'direction': 'neutral'
            })

    def analyze_iv_percentile(self, ticker: str):
        """Analyze IV Percentile changes"""
        today_opt = self.today_data.get(f'{ticker.lower()}_options', {})
        today_iv = self.parse_percentage(today_opt.get('ivPercentile'))

        if today_iv is None:
            return

        # Check for extremes
        if today_iv > self.IV_PERCENTILE_HIGH:
            self.alerts[ticker].append({
                'metric': 'ivPercentile',
                'current': f'{today_iv:.0f}%',
                'previous': None,
                'change': None,
                'status': 'ELEVATED',
                'signal': f'Elevated IV (high fear/uncertainty)',
                'direction': 'bearish'
            })
        elif today_iv < self.IV_PERCENTILE_LOW:
            self.alerts[ticker].append({
                'metric': 'ivPercentile',
                'current': f'{today_iv:.0f}%',
                'previous': None,
                'change': None,
                'status': 'ELEVATED',
                'signal': f'Low IV (complacency zone)',
                'direction': 'bullish'
            })

    def analyze_max_pain(self, ticker: str):
        """Analyze Max Pain shifts"""
        today_opt = self.today_data.get(f'{ticker.lower()}_options', {})
        today_mp = self.parse_price(today_opt.get('maxPain'))

        if not today_mp:
            return

        # If no yesterday data, can't compare
        if not self.yesterday_data:
            return

        yesterday_opt = self.yesterday_data.get(f'{ticker.lower()}_options', {})
        yesterday_mp = self.parse_price(yesterday_opt.get('maxPain'))

        if not yesterday_mp:
            return

        mp_change = today_mp - yesterday_mp
        mp_change_pct = self.calculate_change_pct(today_mp, yesterday_mp)

        if abs(mp_change) >= self.MAX_PAIN_SHIFT:
            status = 'ELEVATED' if abs(mp_change_pct) >= self.ELEVATED_THRESHOLD else 'NORMAL'

            if status != 'NORMAL':
                direction = 'bullish' if mp_change > 0 else 'bearish'
                self.alerts[ticker].append({
                    'metric': 'maxPain',
                    'current': f'${today_mp:.2f}',
                    'previous': f'${yesterday_mp:.2f}',
                    'change': f'${mp_change:+.2f} ({mp_change_pct:+.1f}%)',
                    'status': status,
                    'signal': f'Dealer repositioning detected',
                    'direction': direction
                })

    def filter_and_sort_alerts(self):
        """Filter out NORMAL alerts and sort by severity"""
        severity_order = {'SPIKE': 0, 'ELEVATED': 1, 'NORMAL': 2}

        for ticker in self.alerts:
            # Keep only non-NORMAL alerts
            self.alerts[ticker] = [
                alert for alert in self.alerts[ticker]
                if alert['status'] != 'NORMAL'
            ]

            # Sort by severity
            self.alerts[ticker].sort(
                key=lambda a: severity_order.get(a['status'], 999)
            )

    def analyze(self) -> Dict:
        """Run complete analysis"""
        try:
            self.load_today_and_yesterday()
        except Exception as e:
            print(f"   [Analyzer] Error loading data: {e}")
            return self.alerts

        # Analyze both tickers
        for ticker in ['SPY', 'QQQ']:
            self.analyze_pcr(ticker)
            self.analyze_volume(ticker)
            self.analyze_iv_percentile(ticker)
            self.analyze_max_pain(ticker)

        # Filter and sort
        self.filter_and_sort_alerts()

        return self.alerts

    def to_dict(self) -> Dict:
        """Convert to dictionary for master-plan.md"""
        return {
            'updatedAt': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'SPY': self.alerts['SPY'],
            'QQQ': self.alerts['QQQ']
        }


def main():
    """Test the analyzer"""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze options activity')
    parser.add_argument('--date', default=None, help='Date in YYYY-MM-DD format')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    analyzer = OptionsActivityAnalyzer(args.date)
    alerts = analyzer.analyze()

    if args.json:
        print(json.dumps(analyzer.to_dict(), indent=2))
    else:
        print(f"\n{'='*70}")
        print(f"OPTIONS ACTIVITY ANALYSIS - {analyzer.date_str}")
        print(f"{'='*70}\n")

        for ticker in ['SPY', 'QQQ']:
            print(f"\n{ticker}:")
            if alerts[ticker]:
                for alert in alerts[ticker]:
                    status_str = '[SPIKE]' if alert['status'] == 'SPIKE' else '[ALERT]'
                    change_str = f"({alert['change']})" if alert['change'] else ""
                    prev_str = f"[from {alert['previous']}]" if alert['previous'] else ""

                    print(f"  {status_str} {alert['metric']}: {alert['current']} {change_str} {prev_str}")
                    print(f"     -> {alert['signal']}")
            else:
                print(f"  [OK] No unusual activity detected")


if __name__ == '__main__':
    main()
