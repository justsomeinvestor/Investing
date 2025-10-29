#!/usr/bin/env python3
"""
Scraper Orchestrator - COMPLETE DATA COLLECTION
================================================

Runs all data collection scrapers in optimized parallel flow:
- Research data cleanup (keep last 3 days, archive overviews) - FIRST
- X/Twitter (lists: Crypto, Macro, Technicals + Bookmarks) - PRIORITY (longest task)
- YouTube transcripts (8 channels) - parallel with X
- RSS feeds (news articles) - parallel with X
- X data archival (convert to daily archives)
- Options data (SPY/QQQ technical data)

Note: Bookmarks are now INTEGRATED into the X scraper (no separate process needed)

Usage:
    python scripts/automation/run_all_scrapers.py

What it does (optimized execution):
    PRELIMINARY:
      0. Research data cleanup (delete old files, archive overviews)
    PARALLEL (concurrent):
      1. X/Twitter scraper (lists + bookmarks)
      2. YouTube scraper (transcripts)
      3. RSS scraper (feeds)
    SEQUENTIAL (after parallel completes):
      4. X data archival
      5. Options data scraper (SPY/QQQ)
"""

import subprocess
import sys
import time
import threading
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def relaunch_in_visible_window():
    """Relaunch this script in a visible PowerShell window."""
    if '--visible' in sys.argv:
        return False

    if sys.platform == 'win32':
        script_path = Path(__file__).resolve()
        cmd = f'python "{script_path}" --visible; Write-Host "`nPress Enter to close..."; Read-Host'

        subprocess.Popen(
            ['powershell', '-NoProfile', '-Command', cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            cwd=script_path.parent.parent.parent
        )
        return True

    return False


def print_header():
    """Print orchestrator header"""
    print("\n" + "="*70)
    print("🚀 SCRAPER ORCHESTRATOR - PARALLEL MODE")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()
    print("Execution order (OPTIMIZED - PARALLEL):")
    print("  PRELIMINARY:")
    print("    • Research data cleanup (keep last 3 days)")
    print("  PARALLEL (concurrent):")
    print("    • X/Twitter scraper (lists + bookmarks)")
    print("    • YouTube transcript scraper")
    print("    • RSS feed scraper")
    print("  SEQUENTIAL (after parallel completes):")
    print("    • X data archival")
    print("    • Options data scraper (SPY/QQQ)")
    print()
    print("Expected duration: 10-15 minutes (faster due to parallelization)")
    print("NOTE: Bookmarks are now INTEGRATED into X scraper")
    print("="*70 + "\n")


def run_scraper(script_path: Path, name: str) -> dict:
    """Run a scraper script and capture results"""
    print(f"\n{'='*70}")
    print(f"📡 Running {name}")
    print('='*70)
    print(f"Script: {script_path}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, script_path.name],
            cwd=script_path.parent,
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=1800
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        if success:
            print(f"\n✅ {name} completed successfully")
        else:
            print(f"\n❌ {name} failed (exit code: {result.returncode})")

        print(f"Duration: {elapsed:.1f} seconds")

        return {
            'success': success,
            'elapsed': elapsed,
            'returncode': result.returncode
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"\n⏱️  {name} timed out after {elapsed:.1f} seconds")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': 'timeout'
        }
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ {name} error: {e}")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': str(e)
        }


def run_scraper_parallel(script_path: Path, name: str, results: dict, start_time: float):
    """Run a scraper in a thread and store results"""
    try:
        result = subprocess.run(
            [sys.executable, script_path.name],
            cwd=script_path.parent,
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=1800
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        results[name] = {
            'success': success,
            'elapsed': elapsed,
            'returncode': result.returncode
        }

        if success:
            print(f"\n✅ {name} completed successfully ({elapsed:.1f}s)")
        else:
            print(f"\n❌ {name} failed (exit code: {result.returncode}, {elapsed:.1f}s)")

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"\n⏱️  {name} timed out after {elapsed:.1f} seconds")
        results[name] = {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': 'timeout'
        }
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ {name} error: {e}")
        results[name] = {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': str(e)
        }


def run_cleanup() -> dict:
    """Run research data cleanup"""
    print(f"\n{'='*70}")
    print("🧹 Research Data Cleanup")
    print('='*70)
    print(f"Script: scripts/automation/cleanup_research_data.py")
    print(f"Retention: Keep last 3 days")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, "scripts/automation/cleanup_research_data.py"],
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        if success:
            print(f"\n✅ Research data cleanup completed successfully")
        else:
            print(f"\n❌ Research data cleanup failed (exit code: {result.returncode})")

        print(f"Duration: {elapsed:.1f} seconds")

        return {
            'success': success,
            'elapsed': elapsed,
            'returncode': result.returncode
        }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Cleanup error: {e}")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': str(e)
        }


def run_archive(date_str: str) -> dict:
    """Run X data archival"""
    print(f"\n{'='*70}")
    print("📦 Archiving X Data")
    print('='*70)
    print(f"Date: {date_str}")
    print(f"Script: scripts/utilities/archive_x_daily.py")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, "scripts/utilities/archive_x_daily.py", date_str],
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        if success:
            print(f"\n✅ X data archived successfully")
        else:
            print(f"\n❌ X archival failed (exit code: {result.returncode})")

        print(f"Duration: {elapsed:.1f} seconds")

        return {
            'success': success,
            'elapsed': elapsed,
            'returncode': result.returncode
        }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ X archival error: {e}")
        return {
            'success': False,
            'elapsed': elapsed,
            'returncode': -1,
            'error': str(e)
        }


def print_summary(results: dict, total_time: float):
    """Print execution summary"""
    print("\n" + "="*70)
    print("📊 EXECUTION SUMMARY")
    print("="*70)

    for name, result in results.items():
        status = "✅ SUCCESS" if result.get('success') else "❌ FAILED"
        elapsed = result.get('elapsed', 0)
        print(f"{status:15} | {name:30} | {elapsed:8.1f}s")

    print("="*70)
    print(f"Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    print("="*70 + "\n")


def prompt_continue() -> bool:
    """
    Prompt user to continue or exit after scraper completion.
    Returns True to continue (re-run), False to exit.
    """
    print("\n" + "="*70)
    print("🎯 SCRAPER OPTIONS")
    print("="*70)
    print("1. Close scraper (exit)")
    print("2. Run all scrapers again")
    print("="*70)

    while True:
        try:
            choice = input("\nEnter your choice (1-2): ").strip()
            if choice == "1":
                print("\n👋 Exiting scraper...")
                return False
            elif choice == "2":
                print("\n🔄 Restarting all scrapers...\n")
                return True
            else:
                print("⚠️  Invalid choice. Please enter 1 or 2.")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Exiting scraper (interrupted)...")
            return False


def main():
    """Main orchestrator"""
    if relaunch_in_visible_window():
        return

    # Main execution loop - allows re-running scrapers
    while True:
        print_header()

        # Get today's date for archival
        today = datetime.now().strftime('%Y-%m-%d')

        # Define scrapers in execution order (for parallel execution)
        scrapers_dir = Path("Scraper")
        scrapers = [
            (scrapers_dir / "x_scraper.py", "X/Twitter Scraper"),
            (scrapers_dir / "youtube_scraper.py", "YouTube Transcript Scraper"),
            (scrapers_dir / "rss_scraper.py", "RSS Feed Scraper"),
        ]

        # Check all scrapers exist
        print("Checking scrapers...\n")
        missing = []
        for script, name in scrapers:
            if script.exists():
                print(f"  ✅ {name:30} {script}")
            else:
                print(f"  ❌ {name:30} NOT FOUND: {script}")
                missing.append(name)

        if missing:
            print(f"\n❌ ERROR: Missing scrapers: {', '.join(missing)}")
            print("Cannot proceed. Please ensure all scraper files exist.")
            sys.exit(1)

        print("\n✅ All scrapers found. Starting execution...\n")

        # Run scrapers with optimization: X first, then YouTube/RSS in parallel
        start_time = time.time()
        results = {}

        # 0. Run cleanup FIRST (before any scraping)
        cleanup_result = run_cleanup()
        results["Research Cleanup"] = cleanup_result

        print("\n" + "="*70)
        print("🚀 STARTING PARALLEL EXECUTION")
        print("="*70)
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print()
        print("Launching 3 scrapers concurrently:")
        print("  • X/Twitter Scraper (Priority - longest task)")
        print("  • YouTube Transcript Scraper")
        print("  • RSS Feed Scraper")
        print()
        print("NOTE: Output from all 3 scrapers will be mixed together in real-time")
        print("="*70 + "\n")

        # 1. X/Twitter Scraper (PRIORITY - launch first, runs longest)
        x_thread = threading.Thread(
            target=run_scraper_parallel,
            args=(scrapers_dir / "x_scraper.py", "X/Twitter Scraper", results, start_time)
        )
        x_thread.start()
        print("▶️  X/Twitter Scraper started...")

        # Give X scraper a moment to initialize, then start YouTube/RSS in parallel
        time.sleep(1)

        # 2. YouTube Scraper (parallel with X)
        youtube_thread = threading.Thread(
            target=run_scraper_parallel,
            args=(scrapers_dir / "youtube_scraper.py", "YouTube Transcript Scraper", results, start_time)
        )
        youtube_thread.start()
        print("▶️  YouTube Transcript Scraper started...")

        # 3. RSS Scraper (parallel with X and YouTube)
        rss_thread = threading.Thread(
            target=run_scraper_parallel,
            args=(scrapers_dir / "rss_scraper.py", "RSS Feed Scraper", results, start_time)
        )
        rss_thread.start()
        print("▶️  RSS Feed Scraper started...")

        # Wait for all three to complete
        print("\n⏳ Waiting for all scrapers to complete...\n")
        x_thread.join()
        youtube_thread.join()
        rss_thread.join()

        print("\n✅ All parallel scrapers complete. Now running sequential tasks...\n")

        # 4. X data archival
        archival_result = run_archive(today)
        results["X Archival"] = archival_result

        # 5. Options data scraper
        print(f"\n{'='*70}")
        print("📊 Options Data Scraper")
        print('='*70)
        print(f"Script: scripts/processing/fetch_technical_data.py")
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print()

        options_start = time.time()

        try:
            result = subprocess.run(
                [sys.executable, "scripts/processing/fetch_technical_data.py", today],
                capture_output=False,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=600
            )

            elapsed = time.time() - options_start
            success = result.returncode == 0

            if success:
                print(f"\n✅ Options data fetch completed successfully")
            else:
                print(f"\n❌ Options data fetch failed (exit code: {result.returncode})")

            print(f"Duration: {elapsed:.1f} seconds")

            results["Options Data"] = {
                'success': success,
                'elapsed': elapsed,
                'returncode': result.returncode
            }

        except Exception as e:
            elapsed = time.time() - options_start
            print(f"\n❌ Options data fetch error: {e}")
            results["Options Data"] = {
                'success': False,
                'elapsed': elapsed,
                'returncode': -1,
                'error': str(e)
            }

        total_time = time.time() - start_time
        print_summary(results, total_time)

        # Prompt user to continue or exit
        if not prompt_continue():
            break  # Exit the loop and end the program


if __name__ == "__main__":
    main()
