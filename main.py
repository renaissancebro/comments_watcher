#!/usr/bin/env python3
"""
Comment Watcher - Monitor regulations.gov for specific keywords
Main entry point for the application.
"""

from comment_watcher import CommentWatcher

def main():
    """Main entry point for the comment watcher application."""
    # Create the main watcher instance
    watcher = CommentWatcher()

    # Run a monitoring cycle
    # You can customize these parameters:
    # - since_date: "2024-01-01" for date filtering
    # - page_size: 50 for more comments per run
    results = watcher.run_monitoring_cycle(
        since_date=None,  # Get recent comments without date filter
        page_size=20      # Check 20 comments per run
    )

    print(f"\n🎉 Monitoring cycle completed!")
    print(f"📈 Results: {results['flagged_count']} flagged out of {results['total_checked']} checked")

if __name__ == "__main__":
    main()
