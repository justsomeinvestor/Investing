#!/usr/bin/env python3
"""
RSS Article Collector
Fetches configured RSS feeds and saves articles into provider folders for research workflows.
"""

import html
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

import feedparser
import requests

RSS_ROOT = Path(r'C:\Users\Iccanui\Desktop\Investing\Research\RSS')
CONFIG_PATH = Path('rss_feeds.json')
PROCESSED_LOG_NAME = '_processed_articles.json'
MAX_ARTICLES_PER_FEED = 20
REQUEST_DELAY_SECONDS = 2
USER_AGENT = 'Mozilla/5.0 (RSS Research Collector)'

TAG_RE = re.compile(r'<[^>]+>')
BR_RE = re.compile(r'<\s*br\s*/?>', re.IGNORECASE)


def sanitize_xml_text(xml_text: str) -> str:
    """Clean problematic XML characters before parsing."""
    if not xml_text:
        return ''

    sanitized = xml_text.replace('\ufeff', '').replace('\x00', '')
    sanitized = re.sub(r'&(?!#?\w+;)', '&amp;', sanitized)
    return sanitized




def sanitize_filename(name: str) -> str:
    """Replace characters that are invalid on Windows filesystems."""
    return re.sub(r'[<>:"/\\|?*]', '_', name.strip())


def load_config(config_path: Path) -> List[Dict]:
    """Load provider/feed configuration from JSON."""
    if not config_path.exists():
        raise FileNotFoundError(f'Config file not found: {config_path}')
    raw_json = config_path.read_text(encoding='utf-8-sig')
    data = json.loads(raw_json)
    if not isinstance(data, list):
        raise ValueError('rss_feeds.json must contain a list of providers')
    return data


def load_processed_ids(provider_folder: Path) -> set:
    """Load the set of previously saved article IDs for a provider."""
    log_path = provider_folder / PROCESSED_LOG_NAME
    if not log_path.exists():
        return set()
    try:
        data = json.loads(log_path.read_text(encoding='utf-8'))
        if isinstance(data, list):
            return set(data)
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f'    [WARN] Could not read processed log {log_path.name}: {exc}')
    return set()


def save_processed_ids(provider_folder: Path, processed_ids: Iterable[str]) -> None:
    """Persist processed article IDs back to disk."""
    log_path = provider_folder / PROCESSED_LOG_NAME
    try:
        ordered = sorted(set(processed_ids))
        log_path.write_text(json.dumps(ordered, indent=2), encoding='utf-8')
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f'    [WARN] Could not write processed log {log_path.name}: {exc}')


def clean_html(raw_html: str) -> str:
    """Convert HTML content into readable plain text."""
    if raw_html is None:
        return ''
    text = BR_RE.sub('\n', raw_html)
    text = TAG_RE.sub('', text)
    text = html.unescape(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_best_text(entry: Dict) -> str:
    """Return the richest textual content available for an RSS entry."""
    contents: List[str] = []

    summary = entry.get('summary') or entry.get('description')
    if summary:
        contents.append(clean_html(summary))

    for content in entry.get('content', []):
        value = content.get('value')
        if value:
            contents.append(clean_html(value))

    if not contents:
        return 'No article body provided.'

    seen = set()
    deduped: List[str] = []
    for segment in contents:
        key = segment.strip()
        if key and key not in seen:
            deduped.append(key)
            seen.add(key)

    return '\n\n'.join(deduped) if deduped else 'No article body provided.'


def make_article_id(provider: str, feed_name: str, entry: Dict) -> str:
    """Generate a deterministic identifier for an RSS entry."""
    candidates = [
        entry.get('id'),
        entry.get('guid'),
        entry.get('link'),
    ]
    for candidate in candidates:
        if candidate:
            return f'{provider}|{feed_name}|{candidate}'

    title = entry.get('title', 'untitled').strip()
    published = entry.get('published') or entry.get('updated') or ''
    return f'{provider}|{feed_name}|{title}|{published}'


def format_datetime(struct_time_obj) -> str:
    """Format structured time into ISO timestamp."""
    if not struct_time_obj:
        return ''
    try:
        dt = datetime.fromtimestamp(time.mktime(struct_time_obj))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return ''


def choose_article_date(entry: Dict) -> datetime:
    """Pick best available datetime for an entry."""
    for key in ('published_parsed', 'updated_parsed'):
        struct_time_obj = entry.get(key)
        if struct_time_obj:
            try:
                return datetime.fromtimestamp(time.mktime(struct_time_obj))
            except Exception:
                continue
    return datetime.utcnow()


def get_provider_folder(provider_name: str) -> Path:
    """Ensure provider folder exists and return it."""
    folder = RSS_ROOT / sanitize_filename(provider_name)
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    return folder


def save_article(provider: str, feed_name: str, entry: Dict, provider_folder: Path) -> Path:
    """Persist an RSS entry as a Markdown file."""
    article_dt = choose_article_date(entry)
    collected_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    published_ts = format_datetime(entry.get('published_parsed')) or format_datetime(entry.get('updated_parsed')) or 'Unknown'

    date_prefix = article_dt.strftime('%Y-%m-%d')
    safe_feed = sanitize_filename(feed_name)
    safe_title = sanitize_filename(entry.get('title', 'Untitled Article'))
    filename = provider_folder / f'{date_prefix}_{safe_feed}_{safe_title}.md'

    author = entry.get('author') or entry.get('dc_creator') or 'Unknown'
    link = entry.get('link', '')
    tags = [tag.get('term') for tag in entry.get('tags', []) if tag.get('term')]
    tag_line = ', '.join(tags) if tags else 'None'

    summary_text = clean_html(entry.get('summary', '')) or 'No summary provided.'
    content_text = extract_best_text(entry)

    markdown = f"""# {entry.get('title', 'Untitled Article')}

## Article Information
- **Provider**: {provider}
- **Feed**: {feed_name}
- **Original URL**: {link or 'N/A'}
- **Published**: {published_ts}
- **Collected**: {collected_ts}
- **Author**: {author}
- **Tags**: {tag_line}

---

## Summary

{summary_text}

---

## Content

{content_text}

---

*Saved using RSS Article Collector*
"""

    filename.write_text(markdown, encoding='utf-8')
    return filename


def fetch_feed(url: str) -> feedparser.FeedParserDict:
    """Fetch and parse an RSS/Atom feed with basic sanitization."""
    try:
        response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
        response.raise_for_status()
    except Exception as exc:
        raise RuntimeError(f'HTTP error: {exc}') from exc

    if not response.encoding or response.encoding.lower() == 'us-ascii':
        response.encoding = response.apparent_encoding or 'utf-8'

    parsed = feedparser.parse(response.content)

    if getattr(parsed, 'bozo', False):
        sanitized_text = sanitize_xml_text(response.text)
        parsed = feedparser.parse(sanitized_text)

    if getattr(parsed, 'bozo', False):
        exc = getattr(parsed, 'bozo_exception', None)
        raise RuntimeError(exc or 'Unknown parsing error')

    return parsed


def process_feed(provider: str, feed: Dict, processed_ids: set, provider_folder: Path) -> Dict[str, int]:
    """Process an individual feed and return stats."""
    stats = {'downloaded': 0, 'skipped': 0, 'errors': 0}

    if not feed.get('enabled', True):
        print(f"  [SKIP] Feed disabled: {feed.get('name', 'Unnamed feed')}")
        return stats

    url = feed.get('url')
    if not url:
        print(f'  [WARN] Feed missing URL: {feed}')
        stats['errors'] += 1
        return stats

    print(f"  Fetching {feed.get('name')} -> {url}")
    try:
        parsed = fetch_feed(url)
    except Exception as exc:
        print(f"    [ERROR] Could not parse feed: {exc}")
        stats['errors'] += 1
        return stats

    entries = parsed.entries[:MAX_ARTICLES_PER_FEED]
    if not entries:
        print('    [INFO] No entries returned')
        return stats

    for entry in entries:
        article_id = make_article_id(provider, feed.get('name', 'Feed'), entry)
        if article_id in processed_ids:
            stats['skipped'] += 1
            continue

        try:
            filepath = save_article(provider, feed.get('name', 'Feed'), entry, provider_folder)
            processed_ids.add(article_id)
            stats['downloaded'] += 1
            print(f'    [OK] Saved: {filepath.name}')
        except Exception as exc:
            print(f'    [ERROR] Failed to save article: {exc}')
            stats['errors'] += 1

    return stats


def process_provider(provider_cfg: Dict) -> None:
    """Process every feed for a provider."""
    provider_name = provider_cfg.get('provider', 'Unknown Provider')
    if not provider_cfg.get('enabled', True):
        print(f'\n[SKIP] Provider disabled: {provider_name}')
        return

    feeds = provider_cfg.get('feeds', [])
    if not feeds:
        print(f'\n[WARN] Provider has no feeds configured: {provider_name}')
        return

    print(f'\nProcessing provider: {provider_name}')
    print('-' * 60)

    provider_folder = get_provider_folder(provider_name)
    processed_ids = load_processed_ids(provider_folder)
    before_count = len(processed_ids)

    totals = {'downloaded': 0, 'skipped': 0, 'errors': 0}

    for feed in feeds:
        stats = process_feed(provider_name, feed, processed_ids, provider_folder)
        for key, value in stats.items():
            totals[key] += value
        time.sleep(REQUEST_DELAY_SECONDS)

    if len(processed_ids) != before_count:
        save_processed_ids(provider_folder, processed_ids)

    print(f"  Summary for {provider_name}: {totals['downloaded']} new, {totals['skipped']} skipped, {totals['errors']} errors")


def main() -> None:
    print('=' * 60)
    print('RSS Article Collector')
    print('=' * 60)

    try:
        config = load_config(CONFIG_PATH)
    except Exception as exc:
        print(f'\nERROR: {exc}')
        return

    if not config:
        print('\nNo providers configured in rss_feeds.json')
        return

    for provider_cfg in config:
        try:
            process_provider(provider_cfg)
        except Exception as exc:
            print(f"\n[ERROR] Unexpected failure for {provider_cfg.get('provider', 'Unknown Provider')}: {exc}")
            continue

    print('\n' + '=' * 60)
    print('All providers processed!')
    print(f'Articles saved to: {RSS_ROOT}')
    print('=' * 60)


if __name__ == '__main__':
    main()
    input('\nPress Enter to exit...')


