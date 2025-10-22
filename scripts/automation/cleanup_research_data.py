#!/usr/bin/env python3
"""
Research Data Cleanup Automation
=================================

Automatically cleans up old RSS and YouTube research data while preserving Overview summaries.

Features:
- Configurable retention period (default: 3 days)
- Auto-archive Overview files before deletion
- Dry-run mode to preview changes
- Logging for audit trail
- Integration with existing scraper workflow

Usage:
    # Dry run (preview only)
    python scripts/automation/cleanup_research_data.py --dry-run

    # Execute cleanup (3 days retention)
    python scripts/automation/cleanup_research_data.py

    # Custom retention period
    python scripts/automation/cleanup_research_data.py --days 7

    # Verbose output
    python scripts/automation/cleanup_research_data.py --verbose
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ResearchDataCleanup:
    """Manages cleanup of old research data files."""

    def __init__(self, retention_days=3, dry_run=False, verbose=False):
        """
        Initialize cleanup manager.

        Args:
            retention_days: Number of days of data to keep (default: 3)
            dry_run: If True, only preview changes without executing
            verbose: If True, show detailed output
        """
        self.retention_days = retention_days
        self.dry_run = dry_run
        self.verbose = verbose

        # Base directories
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.rss_dir = self.base_dir / "Research" / "RSS"
        self.youtube_dir = self.base_dir / "Research" / "YouTube"

        # Archive directories
        self.rss_archive = self.rss_dir / "_archives"
        self.youtube_archive = self.youtube_dir / "_archives"

        # Statistics
        self.stats = {
            'rss_archived': 0,
            'youtube_archived': 0,
            'rss_deleted': 0,
            'youtube_deleted': 0
        }

    def calculate_cutoff_date(self):
        """Calculate the cutoff date based on retention period."""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        return cutoff.strftime('%Y-%m-%d')

    def ensure_archive_structure(self, year_month):
        """
        Ensure archive directory structure exists.

        Args:
            year_month: String in format 'YYYY-MM'
        """
        rss_archive_path = self.rss_archive / year_month
        youtube_archive_path = self.youtube_archive / year_month

        if not self.dry_run:
            rss_archive_path.mkdir(parents=True, exist_ok=True)
            youtube_archive_path.mkdir(parents=True, exist_ok=True)

        return rss_archive_path, youtube_archive_path

    def archive_overview_files(self):
        """Archive all Overview files before cleanup."""
        logger.info("📦 Archiving Overview files...")

        # Get current year-month
        year_month = datetime.now().strftime('%Y-%m')
        rss_archive_path, youtube_archive_path = self.ensure_archive_structure(year_month)

        # Archive RSS overviews
        rss_overviews = list(self.rss_dir.rglob("*Overview*.md"))
        for overview in rss_overviews:
            # Skip if already in archive
            if "_archives" in str(overview):
                continue

            dest = rss_archive_path / overview.name
            if self.dry_run:
                logger.info(f"  [DRY RUN] Would archive: {overview.name}")
            else:
                if overview.exists() and not dest.exists():
                    shutil.copy2(overview, dest)
                    self.stats['rss_archived'] += 1
                    if self.verbose:
                        logger.info(f"  ✓ Archived: {overview.name}")

        # Archive YouTube overviews
        youtube_overviews = list(self.youtube_dir.rglob("*Overview*.md"))
        for overview in youtube_overviews:
            # Skip if already in archive
            if "_archives" in str(overview):
                continue

            dest = youtube_archive_path / overview.name
            if self.dry_run:
                logger.info(f"  [DRY RUN] Would archive: {overview.name}")
            else:
                if overview.exists() and not dest.exists():
                    shutil.copy2(overview, dest)
                    self.stats['youtube_archived'] += 1
                    if self.verbose:
                        logger.info(f"  ✓ Archived: {overview.name}")

        if not self.dry_run:
            logger.info(f"  ✓ Archived {self.stats['rss_archived']} RSS and {self.stats['youtube_archived']} YouTube overviews")

    def cleanup_old_files(self):
        """Delete old data files based on retention period."""
        cutoff_date = self.calculate_cutoff_date()
        logger.info(f"🗑️  Cleaning up files older than {cutoff_date} (keeping last {self.retention_days} days)...")

        # Clean RSS files
        logger.info("  Cleaning RSS files...")
        for file_path in self.rss_dir.rglob("2025-*.md"):
            # Skip archives and overviews
            if "_archives" in str(file_path) or "Overview" in file_path.name:
                continue

            # Extract date from filename (format: YYYY-MM-DD)
            try:
                file_date = file_path.name[:10]  # Get first 10 chars (YYYY-MM-DD)
                if file_date < cutoff_date:
                    if self.dry_run:
                        logger.info(f"    [DRY RUN] Would delete: {file_path.relative_to(self.base_dir)}")
                        self.stats['rss_deleted'] += 1
                    else:
                        file_path.unlink()
                        self.stats['rss_deleted'] += 1
                        if self.verbose:
                            logger.info(f"    ✓ Deleted: {file_path.name}")
            except (ValueError, IndexError):
                # Skip files that don't match expected date format
                continue

        # Clean YouTube files
        logger.info("  Cleaning YouTube files...")
        for file_path in self.youtube_dir.rglob("2025-*.md"):
            # Skip archives and overviews
            if "_archives" in str(file_path) or "Overview" in file_path.name:
                continue

            # Extract date from filename
            try:
                file_date = file_path.name[:10]
                if file_date < cutoff_date:
                    if self.dry_run:
                        logger.info(f"    [DRY RUN] Would delete: {file_path.relative_to(self.base_dir)}")
                        self.stats['youtube_deleted'] += 1
                    else:
                        file_path.unlink()
                        self.stats['youtube_deleted'] += 1
                        if self.verbose:
                            logger.info(f"    ✓ Deleted: {file_path.name}")
            except (ValueError, IndexError):
                continue

        logger.info(f"  ✓ {'Would delete' if self.dry_run else 'Deleted'} {self.stats['rss_deleted']} RSS and {self.stats['youtube_deleted']} YouTube files")

    def cleanup_empty_directories(self):
        """Remove empty directories after cleanup."""
        logger.info("📁 Cleaning up empty directories...")

        empty_count = 0
        for dir_path in [self.rss_dir, self.youtube_dir]:
            for subdir in dir_path.rglob("*"):
                if subdir.is_dir() and not any(subdir.iterdir()) and "_archives" not in str(subdir):
                    if self.dry_run:
                        logger.info(f"  [DRY RUN] Would remove empty: {subdir.relative_to(self.base_dir)}")
                        empty_count += 1
                    else:
                        subdir.rmdir()
                        empty_count += 1
                        if self.verbose:
                            logger.info(f"  ✓ Removed: {subdir.relative_to(self.base_dir)}")

        if empty_count > 0:
            logger.info(f"  ✓ {'Would remove' if self.dry_run else 'Removed'} {empty_count} empty directories")

    def run(self):
        """Execute the complete cleanup workflow."""
        logger.info("=" * 70)
        logger.info("🧹 Research Data Cleanup Tool")
        logger.info("=" * 70)
        logger.info(f"Mode: {'DRY RUN (preview only)' if self.dry_run else 'LIVE EXECUTION'}")
        logger.info(f"Retention: Keep last {self.retention_days} days")
        logger.info(f"Cutoff date: {self.calculate_cutoff_date()}")
        logger.info("=" * 70)

        try:
            # Step 1: Archive overviews
            self.archive_overview_files()

            # Step 2: Cleanup old files
            self.cleanup_old_files()

            # Step 3: Remove empty directories
            self.cleanup_empty_directories()

            # Summary
            logger.info("=" * 70)
            logger.info("✅ Cleanup Summary:")
            logger.info(f"  - RSS overviews archived: {self.stats['rss_archived']}")
            logger.info(f"  - YouTube overviews archived: {self.stats['youtube_archived']}")
            logger.info(f"  - RSS files deleted: {self.stats['rss_deleted']}")
            logger.info(f"  - YouTube files deleted: {self.stats['youtube_deleted']}")
            logger.info(f"  - Total files cleaned: {self.stats['rss_deleted'] + self.stats['youtube_deleted']}")
            logger.info("=" * 70)

            if self.dry_run:
                logger.info("ℹ️  This was a DRY RUN. No files were actually modified.")
                logger.info("ℹ️  Run without --dry-run to execute cleanup.")
            else:
                logger.info("✅ Cleanup completed successfully!")

        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Cleanup old research data while preserving Overview summaries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--days',
        type=int,
        default=3,
        help='Number of days to retain (default: 3)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without executing'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # Set verbose logging if requested
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Run cleanup
    cleanup = ResearchDataCleanup(
        retention_days=args.days,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    cleanup.run()


if __name__ == '__main__':
    main()
