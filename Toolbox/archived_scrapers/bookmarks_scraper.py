import os
import re
import sys
import time
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# ========================================================================
# SHARED CONFIGURATION (X specific)
# ========================================================================

# Output root
# Correctly locate the project's "Research" directory relative to this script.
# The script is in Scraper/, so ../Research is the target.
X_ROOT = Path(__file__).resolve().parent.parent / "Research" / "X"
X_ROOT.mkdir(parents=True, exist_ok=True)

# X (Twitter) Configuration
X_CHROME_PROFILE_PATH = r"C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data"
X_BOOKMARKS_URL = "https://x.com/i/bookmarks"
X_SCROLL_INTERVAL = 0.5  # seconds between scrolls
X_MAX_POSTS = 0          # 0 = unlimited
X_MAX_DURATION = 86400   # 24 hours (safety)

# Cutoff behavior controls
X_CUTOFF_MODE = "last_24h"     # options: "since_last", "last_24h", None
X_CUTOFF_HOURS = 24            # used if X_CUTOFF_MODE == "last_24h"

# Scroll/Wait tuning
X_MAX_NO_NEW = 30              # consecutive no-new sweeps before stopping
X_WAIT_TIMEOUT = 7             # seconds to wait for DOM growth after scroll

# ========================================================================
# UTILITIES
# ========================================================================

def sanitize_filename(name):
    """Remove invalid filename characters"""
    return re.sub(r'[<>:"/\\|?*]', '_', str(name).strip())

def load_existing_x_data(output_folder):
    """
    Load existing X bookmarks data from the most recent ARCHIVED file (today's posts only)
    Falls back to accumulating source file if no archived file exists
    Returns (existing_posts, seen_ids) tuple
    """
    output_folder = Path(output_folder)
    if not output_folder.exists():
        return [], set()

    # PRIORITY 1: Look for today's archived file (much smaller, faster)
    today = datetime.now().strftime('%Y%m%d')
    archived_file = output_folder / f'x_bookmarks_posts_{today}_archived.json'

    if archived_file.exists():
        try:
            data = json.loads(archived_file.read_text(encoding='utf-8'))
            posts = data if isinstance(data, list) else data.get("posts", [])
            seen = {p.get("tweet_id") for p in posts if p.get("tweet_id")}
            print(f"    Loading existing data from {archived_file.name} (TODAY'S ARCHIVED)")
            print(f"    Found {len(posts)} existing posts, {len(seen)} unique IDs")
            print(f"    ✓ Using archived file = FAST duplicate detection")
            return posts, seen
        except Exception as e:
            print(f"    [WARN] Failed to read archived file: {e}")
            # Fall through to source file

    # FALLBACK: Use latest source file (accumulates throughout day - slower)
    json_files = sorted(output_folder.glob('x_bookmarks_posts_*.json'), reverse=True)
    # Filter out archived files
    json_files = [f for f in json_files if '_archived' not in f.name and '_historical' not in f.name]

    if not json_files:
        return [], set()

    latest = json_files[0]
    try:
        data = json.loads(latest.read_text(encoding='utf-8'))
        posts = data if isinstance(data, list) else data.get("posts", [])
        seen = {p.get("tweet_id") for p in posts if p.get("tweet_id")}
        print(f"    Loading existing data from {latest.name} (SOURCE FILE)")
        print(f"    Found {len(posts)} existing posts, {len(seen)} unique IDs")
        print(f"    ⚠ Using source file (no archived file) = slower duplicate detection")
        return posts, seen
    except Exception:
        return [], set()

def archive_old_x_files(output_folder):
    """
    Move old x_bookmarks_posts JSON files to archive folder once per day
    Keep all files from today, archive older days
    """
    output_folder = Path(output_folder)
    archive_folder = output_folder / 'archive'
    if not output_folder.exists():
        return
    json_files = sorted(output_folder.glob('x_bookmarks_posts_*.json'), reverse=True)
    if len(json_files) <= 1:
        return
    today = datetime.now().strftime('%Y%m%d')
    for f in json_files:
        if today not in f.name:
            archive_folder.mkdir(parents=True, exist_ok=True)
            f.rename(archive_folder / f.name)

# ========================================================================
# SCRAPER
# ========================================================================

class TwitterBookmarksScraper:
    def __init__(self, profile_path, bookmarks_url, scroll_interval=0.9, max_posts=0, max_duration=0, existing_posts=None, existing_ids=None):
        self.profile_path = profile_path
        self.bookmarks_url = bookmarks_url
        self.scroll_interval = scroll_interval
        self.max_posts = max_posts
        self.max_duration = max_duration
        self.driver = None

        self.seen_ids = set()  # seen in this run
        self.existing_ids = existing_ids if existing_ids else set()
        self.posts = existing_posts if existing_posts else []
        self.new_posts_count = 0
        self.consecutive_existing = 0
        self.max_consecutive_existing = 50  # OPTIMIZED: Stop after 50 (was 500) - we've caught up!
        self.consecutive_old = 0
        self.max_consecutive_old = 50  # OPTIMIZED: Stop after 50 (was 100) - faster exit
        self.cutoff_datetime = None
        self.cutoff_reason = None
        self.cutoff_reached = False
        self.cutoff_logged = False
        self.init_time_cutoff()

    @staticmethod
    def parse_iso_datetime(value):
        """Convert ISO timestamp to timezone-aware datetime."""
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            except ValueError:
                try:
                    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                except ValueError:
                    return None

    def init_time_cutoff(self):
        """Initialize a time cutoff to avoid scrolling forever.

        OPTIMIZATION: If loading from archived file (today's bookmarks only),
        use the newest post from that file as cutoff = stop as soon as we
        catch up to where we left off (much faster than scrolling through
        500 consecutive duplicates).
        """
        mode = globals().get("X_CUTOFF_MODE", "since_last")
        hours = int(globals().get("X_CUTOFF_HOURS", 24))

        latest_dt = None
        for p in self.posts:
            dt = self.parse_iso_datetime(p.get('created_at')) if isinstance(p, dict) else None
            if dt and (latest_dt is None or dt > latest_dt):
                latest_dt = dt

        if mode == "since_last" and latest_dt:
            self.cutoff_datetime = latest_dt
            self.cutoff_reason = f"stop at previously-archived newest bookmark ({latest_dt.strftime('%H:%M:%S')} UTC)"
            print(f"    ✓ Smart cutoff enabled: will stop at {latest_dt.strftime('%H:%M:%S')} UTC")
        elif mode == "last_24h":
            self.cutoff_datetime = datetime.now(timezone.utc) - timedelta(hours=hours)
            self.cutoff_reason = f"rolling {hours}h window"
        else:
            self.cutoff_datetime = None
            self.cutoff_reason = "no cutoff"

    def _log_cutoff_once(self, msg):
        if not self.cutoff_logged:
            print(f"    {msg}")
            self.cutoff_logged = True

    def is_pinned_tweet(self, article):
        try:
            badges = article.find_elements(By.CSS_SELECTOR, 'div[data-testid="socialContext"]')
            for badge in badges:
                if "Pinned" in (badge.text or ""):
                    return True
        except Exception:
            pass
        return False

    def setup_driver(self):
        """Set up Chrome with existing profile (no global kill)."""
        scraper_profile = os.path.join(os.path.dirname(self.profile_path), "Chrome_Scraper_Profile")
        try:
            print('Skipping global Chrome kill for safety (leaving your other Chrome windows alone)')
            time.sleep(1)
        except Exception:
            pass

        options = Options()
        options.add_argument(f"user-data-dir={scraper_profile}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        self.driver.get("https://x.com")
        time.sleep(3)
        if "login" in self.driver.current_url.lower() or "i/flow/login" in self.driver.current_url:
            print("\n" + "="*60)
            print("FIRST TIME SETUP: Please log into Twitter/X in the browser")
            print("Your login will be saved for future runs")
            print("="*60 + "\n")
            input("Press ENTER after you've logged in and see your timeline...")
        else:
            print("    Already logged in - continuing...")
            time.sleep(1)

    def extract_primary_tweet(self, article):
        """Prefer the deepest tweet node that has a <time> (original content)."""
        try:
            candidates = article.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweet"]')
            for node in reversed(candidates):
                try:
                    node.find_element(By.CSS_SELECTOR, 'time')
                    return node
                except Exception:
                    continue
            return candidates[-1] if candidates else article
        except Exception:
            return article

    def extract_count_from_button(self, article, testid):
        """Extract count from button (reply, retweet, like), supporting K/M/B suffixes."""
        def parse_count(text: str) -> int:
            if not text:
                return 0
            t = text.replace(',', '').strip().lower()
            m = re.search(r'(\d+(?:\.\d+)?)([kmb])?', t)
            if not m:
                return 0
            num = float(m.group(1))
            suf = m.group(2)
            mult = 1
            if suf == 'k':
                mult = 1000
            elif suf == 'm':
                mult = 1000000
            elif suf == 'b':
                mult = 1000000000
            return int(num * mult)
        try:
            el = article.find_element(By.CSS_SELECTOR, f'div[data-testid="{testid}"]')
            label = el.get_attribute('aria-label') or el.text or ''
            return parse_count(label)
        except Exception:
            return 0

    def extract_urls(self, article):
        urls = set()
        try:
            for a in article.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"] a[href^="http"]'):
                href = a.get_attribute('href') or ''
                if href and 'x.com' not in href:
                    urls.add(href)
        except Exception:
            pass
        return sorted(urls)

    def parse_tweet(self, article):
        try:
            target_article = self.extract_primary_tweet(article)
            time_el = target_article.find_element(By.CSS_SELECTOR, 'time')
            created_at = time_el.get_attribute('datetime')

            # tweet id from anchor href
            link = target_article.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
            href = link.get_attribute('href')
            m = re.search(r'/status/(\d+)', href or '')
            tweet_id = m.group(1) if m else None
            if not tweet_id:
                return None

            # author
            author_el = target_article.find_element(By.CSS_SELECTOR, 'a[href^="/"][role="link"]')
            author_href = author_el.get_attribute('href') or ''
            author = author_href.strip('/').split('/')[0]

            # text
            try:
                text_el = target_article.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                text = text_el.text.strip()
            except Exception:
                text = ''

            reply_count = self.extract_count_from_button(target_article, 'reply')
            retweet_count = self.extract_count_from_button(target_article, 'retweet')
            like_count = self.extract_count_from_button(target_article, 'like')
            urls = self.extract_urls(target_article)
            is_pinned = self.is_pinned_tweet(target_article)

            return {
                'tweet_id': tweet_id,
                'author': author,
                'permalink': f'https://x.com/{author}/status/{tweet_id}',
                'created_at': created_at,
                'text': text,
                'reply_count': reply_count,
                'retweet_count': retweet_count,
                'like_count': like_count,
                'urls': urls,
                'is_pinned': is_pinned
            }
        except Exception:
            return None

    def harvest_once(self):
        """Harvest tweets currently visible on the page"""
        articles = self.driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]')
        added = 0
        skipped_existing = 0
        skipped_old = 0

        for article in articles:
            tweet_data = self.parse_tweet(article)
            if not tweet_data:
                continue

            tweet_id = tweet_data['tweet_id']
            is_pinned = tweet_data.get('is_pinned', False)

            if tweet_id in self.seen_ids or tweet_id in self.existing_ids:
                self.consecutive_existing += 1
                skipped_existing += 1
                if self.consecutive_existing >= self.max_consecutive_existing:
                    print(f"      ✓ Hit {self.consecutive_existing} consecutive existing posts - we've caught up!")
                    print(f"      Collected {self.new_posts_count} new posts in this run")
                    self.cutoff_reached = True
                    break
                continue  # keep scrolling to find older new posts

            # Reset consecutive existing counter: we found a new post
            self.consecutive_existing = 0

            # Check timestamp cutoff - but don't break, just skip and continue
            tweet_dt = self.parse_iso_datetime(tweet_data.get('created_at'))
            if self.cutoff_datetime and tweet_dt and tweet_dt < self.cutoff_datetime:
                if is_pinned:
                    continue
                # Track consecutive old posts
                self.consecutive_old += 1
                skipped_old += 1
                if self.consecutive_old >= self.max_consecutive_old:
                    self._log_cutoff_once(
                        f"Hit {self.consecutive_old} consecutive posts older than cutoff - stopping"
                    )
                    self.cutoff_reached = True
                    break
                continue  # Skip this old post but keep scrolling

            # Reset consecutive old counter: we found a recent post
            self.consecutive_old = 0

            # Add new post
            self.seen_ids.add(tweet_id)
            self.posts.append(tweet_data)
            self.new_posts_count += 1
            added += 1

        if added > 0 or skipped_existing > 0 or skipped_old > 0:
            status = []
            if added > 0:
                status.append(f"collected {added} new")
            if skipped_existing > 0:
                status.append(f"skipped {skipped_existing} existing")
            if skipped_old > 0:
                status.append(f"skipped {skipped_old} old")
            print(f"      {', '.join(status).capitalize()}. Total: {len(self.posts)} posts ({self.new_posts_count} new this run, {self.consecutive_old} consecutive old)")

        return added

    def wait_for_more_content(self):
        """Scroll and wait until the page height increases (new content loaded)."""
        try:
            prev_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_amount = max(600, self.driver.execute_script("return window.innerHeight") - 100)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            timeout = int(globals().get("X_WAIT_TIMEOUT", 5))
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.body.scrollHeight") > prev_height
            )
        except Exception:
            time.sleep(self.scroll_interval)

    def save_json(self, output_folder):
        """Save collected posts to JSON file"""
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        archive_old_x_files(output_folder)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = output_folder / f"x_bookmarks_posts_{timestamp}.json"
        with filename.open('w', encoding='utf-8') as f:
            json.dump(self.posts, f, ensure_ascii=False, indent=2)
        print(f"    Saved {len(self.posts)} total posts ({self.new_posts_count} new) to {filename.name}")

    def scrape(self):
        """Main scraping loop with time-based safety exit"""
        print(f"    Opening {self.bookmarks_url}")
        self.driver.get(self.bookmarks_url)
        time.sleep(2)

        print("    Starting to collect posts...")
        if self.cutoff_datetime:
            print(f"    Cutoff target: stop at posts before {self.cutoff_datetime.isoformat()} ({self.cutoff_reason})")
        if self.max_duration > 0:
            print(f"    Will run for {self.max_duration} seconds")

        start_time = time.time()
        last_new_post_time = time.time()  # Track when we last found a new post
        no_new_count = 0
        max_no_new = int(globals().get('X_MAX_NO_NEW', 5))
        stale_timeout = 300  # 5 minutes without new posts = exit (safety)

        while True:
            elapsed = time.time() - start_time

            # Check max duration
            if self.max_duration > 0 and elapsed >= self.max_duration:
                print(f"    Reached time limit of {self.max_duration} seconds")
                break

            # SAFETY EXIT: If no new posts in 5 minutes, we're likely stuck
            time_since_last_new = time.time() - last_new_post_time
            if time_since_last_new >= stale_timeout:
                print(f"    ⚠ Safety exit: No new posts found in {stale_timeout/60:.1f} minutes")
                print(f"    Collected {self.new_posts_count} new posts before stalling")
                break

            added = self.harvest_once()

            # Update last new post time if we found something
            if added > 0:
                last_new_post_time = time.time()
                no_new_count = 0
            else:
                no_new_count += 1

            if self.cutoff_reached:
                print("    Cutoff reached; stopping scrape.")
                break

            if self.max_posts > 0 and len(self.posts) >= self.max_posts:
                print(f"    Reached maximum of {self.max_posts} posts")
                break

            if no_new_count >= max_no_new:
                print("    No new posts found after multiple scrolls. Stopping.")
                break

            self.wait_for_more_content()

    def save_json_and_close(self, output_folder):
        try:
            self.save_json(output_folder)
        finally:
            try:
                print("    Closing browser...")
                self.driver.quit()
            except Exception:
                pass

# ========================================================================
# RUNNER
# ========================================================================

def run_bookmarks_scraper():
    print('''
============================================================
X (TWITTER) BOOKMARKS SCRAPER
============================================================
''')
    output_folder = X_ROOT / "Bookmarks"
    try:
        existing_posts, existing_ids = load_existing_x_data(output_folder)
        scraper = TwitterBookmarksScraper(
            profile_path=X_CHROME_PROFILE_PATH,
            bookmarks_url=X_BOOKMARKS_URL,
            scroll_interval=X_SCROLL_INTERVAL,
            max_posts=X_MAX_POSTS,
            max_duration=X_MAX_DURATION,
            existing_posts=existing_posts,
            existing_ids=existing_ids
        )
        scraper.setup_driver()
        scraper.scrape()
        scraper.save_json_and_close(output_folder)

        posts_count = len(scraper.posts)
        new_count = scraper.new_posts_count
        print(f"\n  [+] Completed: Bookmarks ({posts_count} total posts, {new_count} new)")
    except Exception as e:
        import traceback
        print(f"\n  An error occurred while processing bookmarks")
        traceback.print_exc()
        # Attempt to close any driver opened
        try:
            scraper.driver.quit()
        except Exception:
            pass

    print(f'''
============================================================
X Bookmarks scraped successfully!
============================================================

X posts saved to:
  - {output_folder}

[OK] X Bookmarks Scraping complete! Closing in 3 seconds...
''')


if __name__ == "__main__":
    run_bookmarks_scraper()
