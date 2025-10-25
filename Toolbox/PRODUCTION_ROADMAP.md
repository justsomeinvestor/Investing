# Production Roadmap - Taking System Live

**Current Status:** Phase 2 Complete (Framework Ready)
**Next Phase:** Phase 2.5 - Production Hardening
**Target:** Full production readiness in 8-12 hours development time

---

## 🎯 IMMEDIATE ACTION ITEMS

### STEP 1: Create Data Fetcher Module (Priority: CRITICAL)

**File:** `scripts/trading/data_fetcher.py`
**Time:** 1-2 hours
**Status:** Not started

This is the single biggest blocker. Once data flows in, the rest becomes real.

```python
#!/usr/bin/env python3
"""
DATA FETCHER MODULE
Centralized data collection from all sources

Fetches:
- Live prices (yfinance)
- Historical OHLCV (for TA calculations)
- X sentiment (existing scraper)
- Analyst consensus (Yahoo Finance)
- Economic calendar (TradingEconomics)
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import logging

class DataFetcher:
    """Unified data collection from multiple sources"""

    def __init__(self, config=None):
        self.config = config or self._default_config()
        self.logger = logging.getLogger(__name__)
        self.cache = {}  # In-memory cache
        self.cache_ttl = 300  # 5 minutes

    def _default_config(self):
        return {
            "cache_enabled": True,
            "cache_ttl": 300,
            "retry_attempts": 3,
            "timeout": 10,
        }

    # ========== PRICE DATA ==========
    def get_current_price(self, ticker: str) -> float:
        """Get current market price"""
        try:
            data = yf.Ticker(ticker)
            price = data.info.get('currentPrice')
            if not price:
                # Fallback to last closing price
                hist = data.history(period='1d')
                if len(hist) > 0:
                    price = hist['Close'].iloc[-1]
            return float(price) if price else None
        except Exception as e:
            self.logger.error(f"Failed to fetch price for {ticker}: {e}")
            return None

    def get_price_history(self, ticker: str, period: str = '100d',
                         interval: str = '1d') -> pd.DataFrame:
        """
        Get historical price data

        Args:
            ticker: Stock symbol
            period: '100d', '1y', etc.
            interval: '1m', '5m', '15m', '1h', '1d'

        Returns:
            DataFrame with OHLCV
        """
        cache_key = f"{ticker}_{period}_{interval}"

        if self.config['cache_enabled'] and cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.config['cache_ttl']:
                return cached_data

        try:
            ticker_obj = yf.Ticker(ticker)
            data = ticker_obj.history(period=period, interval=interval)

            if self.config['cache_enabled']:
                self.cache[cache_key] = (data, datetime.now())

            return data

        except Exception as e:
            self.logger.error(f"Failed to fetch history for {ticker}: {e}")
            return pd.DataFrame()

    # ========== TECHNICAL INDICATORS ==========
    def get_rsi(self, ticker: str, period: int = 14) -> float:
        """Calculate RSI from price history"""
        try:
            hist = self.get_price_history(ticker, period='100d')
            if len(hist) < period:
                return None

            prices = hist['Close']
            deltas = prices.diff()
            seed = deltas[:period+1]
            up = seed[seed >= 0].sum() / period
            down = -seed[seed < 0].sum() / period
            rs = up / down if down != 0 else 0
            rsi = 100.0 - (100.0 / (1.0 + rs))
            return float(rsi)

        except Exception as e:
            self.logger.error(f"RSI calculation failed for {ticker}: {e}")
            return None

    def get_macd(self, ticker: str) -> dict:
        """Calculate MACD"""
        try:
            hist = self.get_price_history(ticker, period='100d')
            if len(hist) < 26:
                return None

            prices = hist['Close']
            ema_12 = prices.ewm(span=12).mean()
            ema_26 = prices.ewm(span=26).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9).mean()
            histogram = macd_line - signal_line

            return {
                'macd': float(macd_line.iloc[-1]),
                'signal': float(signal_line.iloc[-1]),
                'histogram': float(histogram.iloc[-1]),
                'trend': 'bullish' if macd_line.iloc[-1] > signal_line.iloc[-1] else 'bearish'
            }

        except Exception as e:
            self.logger.error(f"MACD calculation failed for {ticker}: {e}")
            return None

    def get_moving_averages(self, ticker: str) -> dict:
        """Get EMA 20, 50, 200"""
        try:
            hist = self.get_price_history(ticker, period='1y')
            prices = hist['Close']

            ma_20 = prices.ewm(span=20).mean().iloc[-1]
            ma_50 = prices.ewm(span=50).mean().iloc[-1]
            ma_200 = prices.ewm(span=200).mean().iloc[-1]
            current = prices.iloc[-1]

            return {
                'ema_20': float(ma_20),
                'ema_50': float(ma_50),
                'ema_200': float(ma_200),
                'current': float(current),
                'trend': self._determine_trend(current, ma_20, ma_50, ma_200)
            }

        except Exception as e:
            self.logger.error(f"MA calculation failed for {ticker}: {e}")
            return None

    def get_volume_analysis(self, ticker: str, periods: int = 20) -> dict:
        """Analyze volume vs 20-day average"""
        try:
            hist = self.get_price_history(ticker, period='100d')
            volumes = hist['Volume']

            current_volume = volumes.iloc[-1]
            avg_volume = volumes[-periods:].mean()
            volume_vs_avg = current_volume / avg_volume if avg_volume > 0 else 0

            return {
                'current': int(current_volume),
                'average': int(avg_volume),
                'ratio': float(volume_vs_avg),
                'status': 'high' if volume_vs_avg > 1.5 else 'normal' if volume_vs_avg > 0.8 else 'low'
            }

        except Exception as e:
            self.logger.error(f"Volume analysis failed for {ticker}: {e}")
            return None

    # ========== MARKET CONTEXT ==========
    def get_spy_context(self) -> dict:
        """Get SPY trend for market context"""
        try:
            spy_data = self.get_moving_averages('SPY')
            return {
                'current_price': spy_data.get('current'),
                'trend': spy_data.get('trend'),
                'ema_20': spy_data.get('ema_20'),
                'ema_50': spy_data.get('ema_50'),
            }
        except Exception as e:
            self.logger.error(f"SPY context failed: {e}")
            return {}

    def get_qqq_context(self) -> dict:
        """Get QQQ trend for tech stocks"""
        try:
            qqq_data = self.get_moving_averages('QQQ')
            return {
                'current_price': qqq_data.get('current'),
                'trend': qqq_data.get('trend'),
                'ema_20': qqq_data.get('ema_20'),
                'ema_50': qqq_data.get('ema_50'),
            }
        except Exception as e:
            self.logger.error(f"QQQ context failed: {e}")
            return {}

    def get_vix_level(self) -> float:
        """Get current VIX level"""
        try:
            vix_data = yf.Ticker('^VIX')
            return float(vix_data.info.get('currentPrice', 20))
        except Exception as e:
            self.logger.error(f"VIX fetch failed: {e}")
            return 20  # Default to neutral

    # ========== SENTIMENT DATA ==========
    def get_x_sentiment(self, ticker: str) -> dict:
        """
        Get X (Twitter) sentiment for ticker

        TODO: Integrate with existing X scraper system
        """
        # This would call your existing X sentiment scraper
        # Placeholder for now
        return {
            'bullish_percent': 55,
            'bearish_percent': 45,
            'neutral_percent': 0,
            'sample_size': 100,
            'trend': 'neutral'
        }

    def get_analyst_consensus(self, ticker: str) -> dict:
        """Get analyst ratings consensus"""
        try:
            data = yf.Ticker(ticker)
            info = data.info

            return {
                'recommendation': info.get('recommendationKey', 'none'),
                'target_price': info.get('targetMeanPrice', None),
                'number_of_analysts': info.get('numberOfAnalystOpinions', 0),
            }
        except Exception as e:
            self.logger.error(f"Analyst consensus fetch failed for {ticker}: {e}")
            return {}

    # ========== SUPPORT/RESISTANCE ==========
    def find_support_resistance(self, ticker: str, lookback: int = 100) -> dict:
        """
        Find support and resistance levels

        Simple algorithm: Find local minima (support) and maxima (resistance)
        """
        try:
            hist = self.get_price_history(ticker, period=f'{lookback+10}d')
            prices = hist['Close']

            # Find recent peaks and troughs
            peaks = []
            troughs = []

            for i in range(1, len(prices) - 1):
                if prices.iloc[i] > prices.iloc[i-1] and prices.iloc[i] > prices.iloc[i+1]:
                    peaks.append(prices.iloc[i])
                if prices.iloc[i] < prices.iloc[i-1] and prices.iloc[i] < prices.iloc[i+1]:
                    troughs.append(prices.iloc[i])

            resistance_levels = sorted(peaks, reverse=True)[:3] if peaks else []
            support_levels = sorted(troughs)[:3] if troughs else []

            return {
                'resistance': [float(x) for x in resistance_levels],
                'support': [float(x) for x in support_levels],
            }

        except Exception as e:
            self.logger.error(f"S/R detection failed for {ticker}: {e}")
            return {'resistance': [], 'support': []}

    # ========== UTILITY ==========
    def _determine_trend(self, current, ma20, ma50, ma200):
        """Determine trend from moving averages"""
        if current > ma20 > ma50 > ma200:
            return 'strong_uptrend'
        elif current > ma20 and ma20 > ma50:
            return 'uptrend'
        elif current < ma20 < ma50 < ma200:
            return 'strong_downtrend'
        elif current < ma20 and ma20 < ma50:
            return 'downtrend'
        else:
            return 'mixed'

    def clear_cache(self):
        """Clear all cached data"""
        self.cache = {}


# ========== COMMAND LINE TEST ==========
if __name__ == "__main__":
    fetcher = DataFetcher()

    ticker = "NVDA"
    print(f"\n=== DATA FETCH TEST: {ticker} ===\n")

    print(f"Current Price: ${fetcher.get_current_price(ticker):.2f}")
    print(f"RSI: {fetcher.get_rsi(ticker):.2f}")
    print(f"MACD: {fetcher.get_macd(ticker)}")
    print(f"Moving Averages: {fetcher.get_moving_averages(ticker)}")
    print(f"Volume: {fetcher.get_volume_analysis(ticker)}")
    print(f"S/R: {fetcher.find_support_resistance(ticker)}")
    print(f"SPY Context: {fetcher.get_spy_context()}")
    print(f"VIX: {fetcher.get_vix_level()}")
