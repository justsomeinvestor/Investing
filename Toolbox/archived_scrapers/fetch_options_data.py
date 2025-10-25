#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Options Data Fetcher - Workflow Integration
============================================

Fetches options data for SPY and QQQ and formats for master-plan workflow.
Uses the proven options_fetch_3x_daily.py logic with yfinance.

Usage:
    python scripts/fetch_options_data.py YYYY-MM-DD [TICKER]
    python scripts/fetch_options_data.py 2025-10-16 SPY

Output:
    Research/.cache/YYYY-MM-DD_options_data.json
"""

import os
import sys
import json
import time
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    import pandas as pd
except ImportError:
    print("[ERROR] pandas is required. pip install pandas requests yfinance")
    sys.exit(1)

try:
    import yfinance as yf
except Exception:
    yf = None

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

CACHE_DIR = Path("Research/.cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "").strip()

# ---------- Token Bucket Rate Limiter ----------
class TokenBucket:
    def __init__(self, rate_per_sec=float(os.getenv("OPTIONS_FETCH_RATE_PER_SEC", "0.2")), burst=int(os.getenv("OPTIONS_FETCH_BURST", "1"))):
        self.rate = rate_per_sec
        self.capacity = burst
        self.tokens = burst
        self.timestamp = time.monotonic()

    def take(self, cost=1.0):
        now = time.monotonic()
        elapsed = now - self.timestamp
        self.timestamp = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        if self.tokens < cost:
            sleep_for = (cost - self.tokens) / self.rate
            time.sleep(sleep_for)
            self.tokens = 0
        else:
            self.tokens -= cost

BUCKET = TokenBucket()

def make_session():
    s = requests.Session()
    retry = Retry(
        total=7, read=7, connect=7,
        backoff_factor=1.2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST"])
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=2, pool_maxsize=2)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

SESSION = make_session()
SESSION.headers.update({
    "User-Agent": os.getenv(
        "OPTIONS_FETCH_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0 Safari/537.36 OptionsDashboard/1.0"
    )
})

# ---------- Cache Functions ----------
def cache_path(date_str: str, ticker: str) -> Path:
    return CACHE_DIR / f"{date_str}_{ticker}_options.json"

def load_cache(p: Path, ttl_minutes: int):
    if not p.exists():
        return None
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        ts = data.get("_fetched_at")
        if not ts:
            return None
        ts_dt = datetime.fromisoformat(ts)
        if datetime.now() - ts_dt <= timedelta(minutes=ttl_minutes):
            return data
    except Exception:
        return None
    return None

def save_cache(p: Path, data: dict):
    obj = dict(data)
    obj["_fetched_at"] = datetime.now().isoformat()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

# ---------- Calculations ----------
def calculate_max_pain(calls: pd.DataFrame, puts: pd.DataFrame, current_price: float) -> float:
    price_range = current_price * 0.10
    strikes = sorted(set(calls['strike'].tolist() + puts['strike'].tolist()))
    strikes = [s for s in strikes if abs(s - current_price) <= price_range]

    max_pain_strike = current_price
    max_pain_value = float('inf')

    for strike in strikes:
        call_df = calls[calls['strike'] > strike]
        put_df = puts[puts['strike'] < strike]

        call_pain = 0 if call_df.empty else (call_df['openInterest'] * (call_df['strike'] - strike)).sum()
        put_pain = 0 if put_df.empty else (put_df['openInterest'] * (strike - put_df['strike'])).sum()
        total = float(call_pain + put_pain)
        if total < max_pain_value:
            max_pain_value = total
            max_pain_strike = strike

    return float(max_pain_strike)

def put_call_ratio(calls: pd.DataFrame, puts: pd.DataFrame) -> float:
    call_oi = float(calls['openInterest'].sum())
    put_oi = float(puts['openInterest'].sum())
    return (put_oi / call_oi) if call_oi > 0 else 0.0

def iv_percentile_estimate(calls: pd.DataFrame, puts: pd.DataFrame) -> float:
    try:
        all_opts = pd.concat([calls, puts])
        if 'impliedVolatility' not in all_opts.columns:
            return 50.0
        atm_iv = float(all_opts['impliedVolatility'].median())
        min_iv = float(all_opts['impliedVolatility'].min())
        max_iv = float(all_opts['impliedVolatility'].max())
        if max_iv > min_iv:
            return 100.0 * (atm_iv - min_iv) / (max_iv - min_iv)
        return 50.0
    except Exception:
        return 50.0

def identify_key_levels(calls: pd.DataFrame, puts: pd.DataFrame, current_price: float, max_pain: float):
    levels = []
    mp_calls = calls[calls['strike'] == max_pain]
    mp_puts = puts[puts['strike'] == max_pain]
    if not mp_calls.empty or not mp_puts.empty:
        total_oi = int((mp_calls['openInterest'].sum() if not mp_calls.empty else 0) +
                       (mp_puts['openInterest'].sum() if not mp_puts.empty else 0))
        levels.append({'strike': f"{max_pain:.0f}", 'type': 'Max Pain', 'gamma': 'N/A', 'oi': f"{total_oi/1000:.0f}K"})

    cw = calls.nlargest(1, 'openInterest')
    if not cw.empty:
        levels.append({'strike': f"{cw['strike'].iloc[0]:.0f}", 'type': 'Call Wall', 'gamma': 'N/A',
                       'oi': f"{int(cw['openInterest'].iloc[0])/1000:.0f}K"})

    pw = puts.nlargest(1, 'openInterest')
    if not pw.empty:
        levels.append({'strike': f"{pw['strike'].iloc[0]:.0f}", 'type': 'Put Wall', 'gamma': 'N/A',
                       'oi': f"{int(pw['openInterest'].iloc[0])/1000:.0f}K"})

    rng = current_price * 0.02
    near_calls = calls[abs(calls['strike'] - current_price) <= rng]
    if not near_calls.empty:
        hg = near_calls.nlargest(1, 'openInterest')
        levels.append({'strike': f"{hg['strike'].iloc[0]:.0f}", 'type': 'High Gamma', 'gamma': 'N/A',
                       'oi': f"{int(hg['openInterest'].iloc[0])/1000:.0f}K"})

    support = puts[puts['strike'] < current_price].nlargest(1, 'openInterest')
    if not support.empty:
        levels.append({'strike': f"{support['strike'].iloc[0]:.0f}", 'type': 'Put Interest', 'gamma': 'N/A',
                       'oi': f"{int(support['openInterest'].iloc[0])/1000:.0f}K"})

    return levels[:5]

# ---------- Data Provider ----------
def yfinance_chain(ticker: str):
    """Fetch options chain via yfinance"""
    if yf is None:
        raise RuntimeError("yfinance not installed")

    stock = yf.Ticker(ticker, session=SESSION)

    current = None
    if POLYGON_API_KEY:
        try:
            BUCKET.take()
            resp = SESSION.get(
                f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev",
                params={"apiKey": POLYGON_API_KEY, "adjusted": "true"},
                timeout=15,
            )
            resp.raise_for_status()
            current = float(resp.json()["results"][0]["c"])
        except Exception:
            current = None

    if current is None:
        BUCKET.take()
        hist = stock.history(period="5d")
        if hist is None or hist.empty or "Close" not in hist or hist["Close"].dropna().empty:
            BUCKET.take()
            fallback_stock = yf.Ticker(ticker)
            BUCKET.take()
            hist = fallback_stock.history(period="5d")
            if hist is None or hist.empty or "Close" not in hist or hist["Close"].dropna().empty:
                raise RuntimeError(f"yfinance: no price data for {ticker}")
        current = float(hist["Close"].dropna().iloc[-1])

    BUCKET.take()
    time.sleep(0.5 + random.random())
    expirations = list(stock.options or [])
    if not expirations:
        raise RuntimeError(f"yfinance: no options for {ticker}")

    expiry = expirations[0]
    BUCKET.take()
    time.sleep(1.0 + random.random() * 1.5)
    chain = stock.option_chain(expiry)
    calls = chain.calls.fillna(0)
    puts = chain.puts.fillna(0)
    return current, expiry, calls, puts

def fetch_options_with_retries(ticker: str):
    """Fetch with retries and backoff"""
    for attempt in range(5):
        try:
            return yfinance_chain(ticker)
        except Exception as e:
            if attempt < 4:
                sleep_time = (2 ** attempt) * 0.7 + random.random() * 0.6
                # If vendor explicitly rate-limited us, wait longer to be polite
                if "Too Many Requests" in str(e) or "429" in str(e):
                    sleep_time = max(sleep_time, 15 + attempt * 5)
                print(f"   [RETRY] Attempt {attempt+1}/5 failed: {e}")
                print(f"   [RETRY] Waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
            else:
                raise

# ---------- Main Logic ----------
def fetch_ticker_data(date_str: str, ticker: str, ttl_minutes: int = 120):
    """Fetch options data for single ticker"""
    print(f"[*] Fetching {ticker} options data...")

    p = cache_path(date_str, ticker)
    cached = load_cache(p, ttl_minutes)
    if cached:
        print(f"   [CACHE] Using cached data from {cached.get('_fetched_at', 'unknown')}")
        return cached

    print(f"   [FETCH] Fetching fresh data from yfinance...")
    try:
        current, expiry, calls, puts = fetch_options_with_retries(ticker)
        mp = calculate_max_pain(calls, puts, current)
        pcr = put_call_ratio(calls, puts)
        ivp = iv_percentile_estimate(calls, puts)
        total_oi = int(calls['openInterest'].sum() + puts['openInterest'].sum())
        levels = identify_key_levels(calls, puts, current, mp)

        payload = {
            "ticker": ticker,
            "date": date_str,
            "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M ET"),
            "currentPrice": round(current, 2),
            "expiration": expiry,
            "maxPain": f"${mp:.0f}",
            "putCallRatio": f"{pcr:.2f}",
            "ivPercentile": f"{ivp:.0f}%",
            "totalOI": f"{total_oi:,}",
            "keyLevels": levels,
            "source": "yfinance+polygon" if POLYGON_API_KEY else "yfinance"
        }

        save_cache(p, payload)
        print(f"   [OK] Max Pain: {payload['maxPain']}, P/C: {payload['putCallRatio']}")
        return payload

    except Exception as e:
        print(f"   [ERROR] Failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch options data for one or more tickers and save to cache.")
    parser.add_argument("date", help="Target date (YYYY-MM-DD)")
    parser.add_argument("tickers", nargs="*", help="Tickers to fetch (default: SPY QQQ)")
    parser.add_argument("--ttl-min", type=int, default=180, help="Cache TTL in minutes (default: 180)")
    args = parser.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"[ERROR] Invalid date format: {args.date}")
        sys.exit(1)

    tickers = [t.upper() for t in (args.tickers or ["SPY", "QQQ"])]

    print("\n" + "="*60)
    print("OPTIONS DATA FETCHER")
    print("="*60)
    print(f"Date: {args.date}")
    print(f"Tickers: {', '.join(tickers)}")
    print("="*60 + "\n")

    aggregated = {}
    failures = []

    for ticker in tickers:
        data = fetch_ticker_data(args.date, ticker, ttl_minutes=args.ttl_min)
        if data:
            aggregated[ticker] = {
                "lastUpdated": data["lastUpdated"],
                "currentPrice": data.get("currentPrice"),
                "maxPain": data.get("maxPain"),
                "putCallRatio": data.get("putCallRatio"),
                "ivPercentile": data.get("ivPercentile"),
                "totalOI": data.get("totalOI"),
                "expiration": data.get("expiration"),
                "keyLevels": data.get("keyLevels", []),
                "source": data.get("source", "yfinance")
            }
            # polite spacing between tickers
            time.sleep(2.0 + random.random() * 2.0)
        else:
            failures.append(ticker)

    if not aggregated:
        print("\n[ERROR] No options data fetched successfully")
        sys.exit(1)

    output = {
        "date": args.date,
        "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "yfinance+polygon" if POLYGON_API_KEY else "yfinance",
        "tickers": aggregated
    }

    output_file = CACHE_DIR / f"{args.date}_options_data.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("\n" + "="*60)
    print("[OK] OPTIONS DATA SAVED")
    print("="*60)
    print(f"Output: {output_file}")
    print(f"Tickers saved: {', '.join(aggregated.keys())}")
    print(f"Source: {output['source']}")
    if failures:
        print(f"Warnings: failed tickers -> {', '.join(failures)}")
    print("="*60 + "\n")

    if failures:
        sys.exit(2)

if __name__ == "__main__":
    main()
