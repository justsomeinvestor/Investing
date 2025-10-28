#!/usr/bin/env python3
"""
Research Data Cleanup Automation
=================================

Automatically cleans up old research data (RSS, YouTube, X/Twitter, Technicals)
while preserving Overview summaries.

Features:
- Configurable retention period (default: 3 days)
- Auto-archive Overview files before deletion
- Handles multiple data sources: RSS, YouTube, X/Twitter, Technicals
- Cleans up JSON scraper output files
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
        self.x_dir = self.base_dir / "Research" / "X"
        self.technicals_dir = self.base_dir / "Research" / "Technicals"

        # Archive directories
        self.rss_archive = self.rss_dir / "_archives"
        self.youtube_archive = self.youtube_dir / "_archives"
        self.x_archive = self.x_dir / "_archives"
        self.technicals_archive = self.technicals_dir / "_archives"

        # Statistics
        self.stats = {
            'rss_archived': 0,
            'youtube_archived': 0,
            'x_archived': 0,
            'technicals_archived': 0,
            'rss_deleted': 0,
            'youtube_deleted': 0,
            'x_deleted': 0,
            'technicals_deleted': 0
        }

    def calculate_cutoff_date(self):
        """Calculate the cutoff date based on retention period."""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        return cutoff.strftime('%Y-%m-%d')

    def ensure_archive_structure(self, year_month):
        """
        Ensure archive directory structure exists for all data sources.

        Args:
            year_month: String in format 'YYYY-MM'

        Returns:
            Tuple of (rss_path, youtube_path, x_path, technicals_path)
        """
        rss_archive_path = self.rss_archive / year_month
        youtube_archive_path = self.youtube_archive / year_month
        x_archive_path = self.x_archive / year_month
        technicals_archive_path = self.technicals_archive / year_month

        if not self.dry_run:
            rss_archive_path.mkdir(parents=True, exist_ok=True)
            youtube_archive_path.mkdir(parents=True, exist_ok=True)
            x_archive_path.mkdir(parents=True, exist_ok=True)
            technicals_archive_path.mkdir(parents=True, exist_ok=True)

        return rss_archive_path, youtube_archive_path, x_archive_path, technicals_archive_path

    def archive_overview_files(self):
        """Archive all Overview and Summary files before cleanup."""
        logger.info("📦 Archiving Overview and Summary files...")

        # Get current year-month
        year_month = datetime.now().strftime('%Y-%m')
        rss_archive_path, youtube_archive_path, x_archive_path, technicals_archive_path = self.ensure_archive_structure(year_month)

        # Archive RSS overviews and summaries
        rss_files = list(self.rss_dir.rglob("*Overview*.md")) + list(self.rss_dir.rglob("*Summary.md"))
        for overview in rss_files:
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

        # Archive YouTube overviews and summaries
        youtube_files = list(self.youtube_dir.rglob("*Overview*.md")) + list(self.youtube_dir.rglob("*Summary.md"))
        for overview in youtube_files:
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

        # Archive X overviews and summaries (if X directory exists)
        if self.x_dir.exists():
            x_files = list(self.x_dir.rglob("*Overview*.md")) + list(self.x_dir.rglob("*Summary.md"))
            for x_file in x_files:
                # Skip if already in archive
                if "_archives" in str(x_file):
                    continue

                dest = x_archive_path / x_file.name
                if self.dry_run:
                    logger.info(f"  [DRY RUN] Would archive: {x_file.name}")
                else:
                    if x_file.exists() and not dest.exists():
                        shutil.copy2(x_file, dest)
                        self.stats['x_archived'] += 1
                        if self.verbose:
                            logger.info(f"  ✓ Archived: {x_file.name}")

        # Archive Technicals overviews and summaries (if directory exists)
        if self.technicals_dir.exists():
            tech_files = list(self.technicals_dir.rglob("*Overview*.md")) + list(self.technicals_dir.rglob("*Summary.md"))
            for tech_file in tech_files:
                # Skip if already in archive
                if "_archives" in str(tech_file):
                    continue

                dest = technicals_archive_path / tech_file.name
                if self.dry_run:
                    logger.info(f"  [DRY RUN] Would archive: {tech_file.name}")
                else:
                    if tech_file.exists() and not dest.exists():
                        shutil.copy2(tech_file, dest)
                        self.stats['technicals_archived'] += 1
                        if self.verbose:
                            logger.info(f"  ✓ Archived: {tech_file.name}")

        if not self.dry_run:
            logger.info(f"  ✓ Archived {self.stats['rss_archived']} RSS, {self.stats['youtube_archived']} YouTube, {self.stats['x_archived']} X, {self.stats['technicals_archived']} Technicals files")

    def cleanup_old_files(self):
        """Delete old data files based on retention period."""
        cutoff_date = self.calculate_cutoff_date()
        logger.info(f"🗑️  Cleaning up files older than {cutoff_date} (keeping last {self.retention_days} days)...")

        # Clean RSS files
        logger.info("  Cleaning RSS files...")
        for file_path in self.rss_dir.rglob("2025-*.md"):
            # Skip archives and overviews/summaries
            if "_archives" in str(file_path) or "Overview" in file_path.name or "Summary" in file_path.name:
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
            # Skip archives and overviews/summaries
            if "_archives" in str(file_path) or "Overview" in file_path.name or "Summary" in file_path.name:
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

        # Clean X/Twitter files (if directory exists)
        if self.x_dir.exists():
            logger.info("  Cleaning X/Twitter files...")

            # Clean markdown summaries (format: YYYY-MM-DD_X_*.md)
            for file_path in self.x_dir.rglob("2025-*.md"):
                # Skip archives and overviews/summaries
                if "_archives" in str(file_path) or "Overview" in file_path.name or "Summary" in file_path.name:
                    continue

                try:
                    file_date = file_path.name[:10]
                    if file_date < cutoff_date:
                        if self.dry_run:
                            logger.info(f"    [DRY RUN] Would delete: {file_path.relative_to(self.base_dir)}")
                            self.stats['x_deleted'] += 1
                        else:
                            file_path.unlink()
                            self.stats['x_deleted'] += 1
                            if self.verbose:
                                logger.info(f"    ✓ Deleted: {file_path.name}")
                except (ValueError, IndexError):
                    continue

            # Clean X JSON scraper output files (format: x_list_posts_YYYYMMDD*.json)
            for subdir in [d for d in self.x_dir.iterdir() if d.is_dir() and "_archives" not in str(d) and "_scripts" not in str(d)]:
                for file_path in subdir.glob("x_list_posts_*.json"):
                    # Protect last_run file
                    if "last_run" in file_path.name:
                        continue

                    try:
                        # Extract date from filename (format: x_list_posts_YYYYMMDDHHMMSS.json)
                        name_parts = file_path.name.replace(".json", "").split("_")
                        if len(name_parts) >= 4:
                            date_str = name_parts[3]  # YYYYMMDD or YYYYMMDDHHMMSS
                            # Convert YYYYMMDD to YYYY-MM-DD
                            if len(date_str) >= 8:
                                file_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                                if file_date < cutoff_date:
                                    if self.dry_run:
                                        logger.info(f"    [DRY RUN] Would delete: {file_path.relative_to(self.base_dir)}")
                                        self.stats['x_deleted'] += 1
                                    else:
                                        file_path.unlink()
                                        self.stats['x_deleted'] += 1
                                        if self.verbose:
                                            logger.info(f"    ✓ Deleted: {file_path.name}")
                    except (ValueError, IndexError, TypeError):
                        continue

        # Clean Technicals files (if directory exists)
        if self.technicals_dir.exists():
            logger.info("  Cleaning Technicals files...")
            for file_path in self.technicals_dir.rglob("2025-*.md"):
                # Skip archives and overviews/summaries
                if "_archives" in str(file_path) or "Overview" in file_path.name or "Summary" in file_path.name:
                    continue

                try:
                    file_date = file_path.name[:10]
                    if file_date < cutoff_date:
                        if self.dry_run:
                            logger.info(f"    [DRY RUN] Would delete: {file_path.relative_to(self.base_dir)}")
                            self.stats['technicals_deleted'] += 1
                        else:
                            file_path.unlink()
                            self.stats['technicals_deleted'] += 1
                            if self.verbose:
                                logger.info(f"    ✓ Deleted: {file_path.name}")
                except (ValueError, IndexError):
                    continue

        logger.info(f"  ✓ {'Would delete' if self.dry_run else 'Deleted'} {self.stats['rss_deleted']} RSS, {self.stats['youtube_deleted']} YouTube, {self.stats['x_deleted']} X, {self.stats['technicals_deleted']} Technicals files")

    def cleanup_empty_directories(self):
        """Remove empty directories after cleanup."""
        logger.info("📁 Cleaning up empty directories...")

        empty_count = 0
        dirs_to_check = [self.rss_dir, self.youtube_dir, self.x_dir, self.technicals_dir]
        for dir_path in dirs_to_check:
            if not dir_path.exists():
                continue
            for subdir in dir_path.rglob("*"):
                if subdir.is_dir() and not any(subdir.iterdir()) and "_archives" not in str(subdir) and "_scripts" not in str(subdir):
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
            logger.info(f"  ARCHIVED:")
            logger.info(f"    - RSS: {self.stats['rss_archived']}")
            logger.info(f"    - YouTube: {self.stats['youtube_archived']}")
            logger.info(f"    - X/Twitter: {self.stats['x_archived']}")
            logger.info(f"    - Technicals: {self.stats['technicals_archived']}")
            logger.info(f"  DELETED:")
            logger.info(f"    - RSS: {self.stats['rss_deleted']}")
            logger.info(f"    - YouTube: {self.stats['youtube_deleted']}")
            logger.info(f"    - X/Twitter: {self.stats['x_deleted']}")
            logger.info(f"    - Technicals: {self.stats['technicals_deleted']}")
            total_cleaned = sum(self.stats.values())
            logger.info(f"  - Total files processed: {total_cleaned}")
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
        default=1,
        help='Number of days to retain (default: 1)'
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
