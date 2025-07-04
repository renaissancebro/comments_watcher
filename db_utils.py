#!/usr/bin/env python3
"""
Database utilities for the Comment Watcher.
Provides tools to query, analyze, and manage the SQLite database.
"""

from storage import (
    get_statistics,
    get_comments_by_keyword,
    get_comments_by_date_range,
    load_flagged_comments,
    export_to_json,
    clear_database
)
from config import KEYWORDS

def print_statistics():
    """Print database statistics."""
    stats = get_statistics()

    print("📊 DATABASE STATISTICS")
    print("=" * 50)
    print(f"Total flagged comments: {stats['total_flagged_comments']}")
    print(f"Total seen IDs: {stats['total_seen_ids']}")
    print(f"Recent comments (7 days): {stats['recent_comments']}")

    if stats['keyword_counts']:
        print("\n📈 Comments by keyword:")
        for keyword, count in stats['keyword_counts'].items():
            print(f"  {keyword}: {count}")
    else:
        print("\n📈 No flagged comments found")

def print_recent_comments(limit: int = 10):
    """Print recent flagged comments."""
    comments = load_flagged_comments()

    print(f"📝 RECENT FLAGGED COMMENTS (showing {min(limit, len(comments))})")
    print("=" * 50)

    for i, comment in enumerate(comments[:limit], 1):
        print(f"{i}. [{comment['keyword']}] {comment['title'][:60]}{'...' if len(comment['title']) > 60 else ''}")
        print(f"   ID: {comment['id']} | Date: {comment['date']}")
        print(f"   Submitter: {comment.get('submitter_name', 'N/A')}")
        print()

def search_by_keyword(keyword: str):
    """Search and display comments by keyword."""
    comments = get_comments_by_keyword(keyword)

    print(f"🔍 COMMENTS MATCHING '{keyword}' ({len(comments)} found)")
    print("=" * 50)

    for i, comment in enumerate(comments, 1):
        print(f"{i}. {comment['title']}")
        print(f"   ID: {comment['id']} | Date: {comment['date']}")
        print(f"   Submitter: {comment.get('submitter_name', 'N/A')}")
        print(f"   Organization: {comment.get('organization', 'N/A')}")
        print(f"   Snippet: {comment['text_snippet'][:100]}...")
        print()

def search_by_date_range(start_date: str, end_date: str):
    """Search and display comments by date range."""
    comments = get_comments_by_date_range(start_date, end_date)

    print(f"📅 COMMENTS FROM {start_date} TO {end_date} ({len(comments)} found)")
    print("=" * 50)

    for i, comment in enumerate(comments, 1):
        print(f"{i}. [{comment['keyword']}] {comment['title']}")
        print(f"   ID: {comment['id']} | Date: {comment['date']}")
        print(f"   Submitter: {comment.get('submitter_name', 'N/A')}")
        print()

def export_data():
    """Export database to JSON file."""
    print("📤 Exporting data to JSON...")
    export_to_json()
    print("✅ Export completed!")

def main():
    """Main function for database utilities."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python db_utils.py <command> [args...]")
        print("\nCommands:")
        print("  stats                    - Show database statistics")
        print("  recent [limit]           - Show recent comments (default: 10)")
        print("  keyword <keyword>        - Search by keyword")
        print("  date <start> <end>       - Search by date range (YYYY-MM-DD)")
        print("  export                   - Export to JSON")
        print("  clear                    - Clear database (use with caution!)")
        return

    command = sys.argv[1].lower()

    if command == "stats":
        print_statistics()

    elif command == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print_recent_comments(limit)

    elif command == "keyword":
        if len(sys.argv) < 3:
            print("❌ Please provide a keyword")
            return
        keyword = sys.argv[2]
        search_by_keyword(keyword)

    elif command == "date":
        if len(sys.argv) < 4:
            print("❌ Please provide start and end dates (YYYY-MM-DD)")
            return
        start_date = sys.argv[2]
        end_date = sys.argv[3]
        search_by_date_range(start_date, end_date)

    elif command == "export":
        export_data()

    elif command == "clear":
        confirm = input("⚠️  Are you sure you want to clear the database? (yes/no): ")
        if confirm.lower() == "yes":
            clear_database()
        else:
            print("❌ Operation cancelled")

    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
