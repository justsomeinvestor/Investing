#!/usr/bin/env python3
"""
Scraper Orchestrator
====================

Runs YouTube, RSS, and X scrapers in sequence.
Designed to be called from AI workflow automation.

Usage:
    python scripts/run_all_scrapers.py

    What it does:
        1. Runs YouTube scraper (fetch latest video transcripts)
        2. Runs RSS scraper (fetch latest articles)
        3. Runs X/Twitter scraper (fetch latest posts)
        4. Runs X Bookmarks scraper (fetch latest bookmarked posts)
        5. Archives X data (extracts today's tweets only)    5. Reports success/failure for each

Duration: ~5-10 minutes (depending on network and content volume)

Output:
    - YouTube transcripts → Research/YouTube/{Channel}/
    - RSS articles → Research/RSS/{Provider}/
    - X posts → Research/X/{Category}/
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def relaunch_in_visible_window():
    """
    Relaunch this script in a visible PowerShell window.
    Returns True if relaunched, False if already visible.
    """
    # Check if already running in visible mode
    if '--visible' in sys.argv:
        return False

    # On Windows, relaunch in new console window
    if sys.platform == 'win32':
        script_path = Path(__file__).resolve()
        cmd = f'python "{script_path}" --visible; Write-Host "`nPress Enter to close..."; Read-Host'

        subprocess.Popen(
            ['powershell', '-NoProfile', '-Command', cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            cwd=script_path.parent.parent  # Run from Investing directory
        )
        return True

    return False


def print_header():
    """Print orchestrator header"""
    print("\n" + "="*70)
    print("🚀 SCRAPER ORCHESTRATOR")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()
    print("This will run 4 scrapers + archival + options fetch in sequence:")
    print("  1. YouTube scraper (videos + transcripts)")
    print("  2. RSS scraper (news articles)")
    print("  3. X/Twitter scraper (social posts)")
    print("  4. X Bookmarks scraper (bookmarked posts)")
    print("  5. X data archival (extract today's tweets)")
    print("  6. Options data fetch (SPY options chain from yfinance)")
    print()
    print("Expected duration: 5-10 minutes")
    print("="*70 + "\n")


def run_scraper(script_path: Path, name: str) -> dict:
    """
    Run a scraper script and capture results

    Args:
        script_path: Path to scraper Python file
        name: Human-readable scraper name

    Returns:
        dict with keys: success (bool), elapsed (float), output (str)
    """
    print(f"\n{'='*70}")
    print(f"📡 Running {name} Scraper")
    print('='*70)
    print(f"Script: {script_path}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

    start_time = time.time()

    try:
        # Run scraper from its own directory
        result = subprocess.run(
            [sys.executable, script_path.name],
            cwd=script_path.parent,
            capture_output=False,  # Show output in real-time
            text=True,
            timeout=1800  # 30 minute timeout per scraper
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        if success:
            print(f"\n✅ {name} scraper completed successfully")
        else:
            print(f"\n❌ {name} scraper failed (exit code: {result.returncode})")

        print(f"Duration: {elapsed:.1f} seconds")

        return {
            'success': success,
            'elapsed': elapsed,
            'returncode': result.returncode
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"\n⏱️  {name} scraper timed out after {elapsed:.1f} seconds")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': 'timeout'
        }
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ {name} scraper error: {e}")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': str(e)
        }


def run_options_fetch(date_str: str, ticker: str = "SPY") -> dict:
    """
    Run options data fetch for specified ticker

    Args:
        date_str: Target date in YYYY-MM-DD format
        ticker: Stock ticker symbol (default: SPY)

    Returns:
        dict with keys: success (bool), elapsed (float)
    """
    print(f"\n{'='*70}")
    print("📊 Fetching Options Data")
    print('='*70)
    print(f"Ticker: {ticker}")
    print(f"Date: {date_str}")
    print(f"Script: scripts/fetch_options_data.py")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

    start_time = time.time()

    try:
        # Run options fetch script (has built-in 5-attempt retry logic with exponential backoff)
        result = subprocess.run(
            [sys.executable, "scripts/fetch_options_data.py", date_str, ticker],
            capture_output=False,  # Show output in real-time
            text=True,
            timeout=900  # 15 minute timeout (allows retries to complete)
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        if success:
            print(f"\n✅ Options data fetch completed successfully")
            print(f"   → Saved to Research/.cache/{date_str}_options_data.json")
        else:
            print(f"\n❌ Options data fetch failed (exit code: {result.returncode})")

        print(f"Duration: {elapsed:.1f} seconds")

        return {
            'success': success,
            'elapsed': elapsed,
            'returncode': result.returncode
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"\n⏱️  Options data fetch timed out after {elapsed:.1f} seconds")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': 'timeout'
        }
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Options data fetch error: {e}")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': str(e)
        }


def run_archive(date_str: str) -> dict:
    """
    Run X data archival to extract today's tweets

    Args:
        date_str: Target date in YYYY-MM-DD format

    Returns:
        dict with keys: success (bool), elapsed (float)
    """
    print(f"\n{'='*70}")
    print("📦 Archiving X Data")
    print('='*70)
    print(f"Date: {date_str}")
    print(f"Script: scripts/archive_x_daily.py")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

    start_time = time.time()

    try:
        # Run archival script
        result = subprocess.run(
            [sys.executable, "scripts/archive_x_daily.py", date_str],
            capture_output=False,  # Show output in real-time
            text=True,
            timeout=120  # 2 minute timeout
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        if success:
            print(f"\n✅ X data archival completed successfully")
            print(f"   → Created _archived.json files for {date_str}")
        else:
            print(f"\n❌ X data archival failed (exit code: {result.returncode})")

        print(f"Duration: {elapsed:.1f} seconds")

        return {
            'success': success,
            'elapsed': elapsed,
            'returncode': result.returncode
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"\n⏱️  X data archival timed out after {elapsed:.1f} seconds")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': 'timeout'
        }
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ X data archival error: {e}")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': str(e)
        }


def print_summary(results: dict, total_time: float):
    """Print final summary of all scrapers"""
    print("\n" + "="*70)
    print("SCRAPER ORCHESTRATOR SUMMARY")
    print("="*70)

    for name, result in results.items():
        status = "[OK] SUCCESS" if result['success'] else "[FAIL] FAILED"
        duration = result['elapsed']
        note = result.get('note', '')
        print(f"{name:20} {status:15} ({duration:.1f}s)")
        if note:
            print(f"{' ':20} [INFO] {note}")

    print("-"*70)
    print(f"Total Time: {total_time:.1f}s ({total_time/60:.1f} min)")

    # Count successes (required vs optional)
    youtube_ok = results.get('YouTube', {}).get('success', False)
    rss_ok = results.get('RSS', {}).get('success', False)
    x_ok = results.get('X/Twitter', {}).get('success', False)
    archive_ok = results.get('X Archive', {}).get('success', False)

    required_ok = youtube_ok and rss_ok

    print("="*70)
    if required_ok and x_ok and archive_ok:
        print("[SUCCESS] ALL SCRAPERS + ARCHIVAL COMPLETED")
        print("="*70)
        print("\nNext steps:")
        print("  1. AI reads archived X data (Research/X/*/x_list_posts_*_archived.json)")
        print("  2. AI creates provider summaries (Step 1)")
        print("  3. Follow @Research/How to use_Research.txt")
        print()
    elif required_ok and x_ok:
        print("[SUCCESS] ALL SCRAPERS COMPLETED")
        print("[WARN] X archival failed - may need to manually archive")
        print("="*70)
        print("\nNext steps:")
        print("  1. Run: python scripts/archive_x_daily.py YYYY-MM-DD")
        print("  2. AI creates provider summaries (Step 1)")
        print("  3. Follow @Research/How to use_Research.txt")
        print()
    elif required_ok:
        print("[SUCCESS] CORE SCRAPERS COMPLETED (YouTube + RSS)")
        print("[INFO] X scraper/archival had issues - using existing data")
        print("="*70)
        print("\nNext steps:")
        print("  1. Check X data availability")
        print("  2. AI creates provider summaries (Step 1)")
        print("  3. Follow @Research/How to use_Research.txt")
        print()
    else:
        print("[FAIL] REQUIRED SCRAPERS FAILED")
        print("="*70)
        print("\nCannot proceed without YouTube and RSS data.")
        print("Check error messages above and retry.")
        print()

    print("="*70 + "\n")


def main():
    """Main orchestrator entry point"""
    # Relaunch in visible window if not already visible
    if relaunch_in_visible_window():
        print("Launching scrapers in visible window...")
        return  # Exit this hidden instance

    print_header()

    # Define scraper paths
    scraper_dir = Path("Scraper")

    scrapers = [
        (scraper_dir / "youtube_scraper.py", "YouTube"),
        (scraper_dir / "rss_scraper.py", "RSS"),
        (scraper_dir / "x_scraper.py", "X/Twitter"),
        (scraper_dir / "bookmarks_scraper.py", "X Bookmarks")
    ]

    # Check all scrapers exist before starting
    print("🔍 Pre-flight check:")
    missing = []
    for script, name in scrapers:
        if script.exists():
            print(f"  ✅ {name:20} {script}")
        else:
            print(f"  ❌ {name:20} NOT FOUND: {script}")
            missing.append(name)

    if missing:
        print(f"\n❌ ERROR: Missing scrapers: {', '.join(missing)}")
        print("Cannot proceed. Please ensure all scraper files exist.")
        sys.exit(1)

    print("\n✅ All scrapers found. Starting execution...\n")

    # Get today's date (needed for archival and options fetch)
    today = datetime.now().strftime('%Y-%m-%d')

    # Run scrapers in sequence
    start_time = time.time()
    results = {}

    for script, name in scrapers:
        # Special handling for X scraper - make it optional
        if name in ["X/Twitter", "X Bookmarks"]:
            print(f"\n[INFO] Running optional scraper: {name}")
            print("[INFO] If this fails, workflow will continue with existing X data")
            try:
                result = run_scraper(script, name)
                results[name] = result
            except Exception as e:
                print(f"\n[WARN] {name} scraper failed: {e}")
                print("[INFO] Continuing with existing X data from morning run")
                results[name] = {
                    'success': False,
                    'elapsed': 0,
                    'returncode': -1,
                    'error': str(e),
                    'note': 'Using existing X data - not critical'
                }
        else:
            # Required scrapers (YouTube, RSS)
            result = run_scraper(script, name)
            results[name] = result

            if not result['success']:
                print(f"\n[ERROR] Required scraper {name} failed!")
                # Don't exit yet, let summary show what happened

        # Add small delay between scrapers
        if name != scrapers[-1][1]:
            time.sleep(2)

    # After all scrapers complete, run X data archival
    # Only if X scraper succeeded
    x_scraper_ok = results.get('X/Twitter', {}).get('success', False)

    if x_scraper_ok:
        print("\n[INFO] X scraper succeeded - running archival to extract today's tweets")
        time.sleep(2)

        try:
            archive_result = run_archive(today)
            results['X Archive'] = archive_result

            if archive_result['success']:
                print(f"\n[SUCCESS] X data archived successfully")
                print(f"[INFO] AI can now read: Research/X/*/x_list_posts_{today.replace('-', '')}_archived.json")
            else:
                print(f"\n[WARN] X archival failed - AI may read large source files")
                print(f"[ACTION] Manually run: python scripts/archive_x_daily.py {today}")
        except Exception as e:
            print(f"\n[WARN] X archival error: {e}")
            print(f"[ACTION] Manually run: python scripts/archive_x_daily.py {today}")
            results['X Archive'] = {
                'success': False,
                'elapsed': 0,
                'returncode': -1,
                'error': str(e),
                'note': 'Archival failed - not critical'
            }
    else:
        print("\n[SKIP] X scraper failed - skipping archival")
        print("[INFO] Cannot archive without fresh X data")
        results['X Archive'] = {
            'success': False,
            'elapsed': 0,
            'returncode': -1,
            'note': 'Skipped - X scraper failed'
        }

    # Run options data fetch
    print("\n[INFO] Fetching options data for SPY")
    time.sleep(2)

    try:
        options_result = run_options_fetch(today, "SPY")
        results['Options Data'] = options_result

        if options_result['success']:
            print(f"\n[SUCCESS] Options data fetched successfully")
            print(f"[INFO] Data saved to: Research/.cache/{today}_options_data.json")
        else:
            print(f"\n[WARN] Options data fetch failed")
            print(f"[ACTION] Manually run: python scripts/fetch_options_data.py {today} SPY")
    except Exception as e:
        print(f"\n[WARN] Options fetch error: {e}")
        print(f"[ACTION] Manually run: python scripts/fetch_options_data.py {today} SPY")
        results['Options Data'] = {
            'success': False,
            'elapsed': 0,
            'returncode': -1,
            'error': str(e),
            'note': 'Options fetch failed - not critical'
        }

    total_time = time.time() - start_time

    # Print summary
    print_summary(results, total_time)

    # Exit with appropriate code
    youtube_ok = results.get('YouTube', {}).get('success', False)
    rss_ok = results.get('RSS', {}).get('success', False)

    if youtube_ok and rss_ok:
        sys.exit(0)  # Success - core scrapers worked
    else:
        sys.exit(1)  # Failure - core scrapers failed


if __name__ == "__main__":
    main()
