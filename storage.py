import sqlite3
import json
from typing import List, Dict, Set
from datetime import datetime
from config import OUTPUT_FILE, SEEN_IDS_FILE

# SQLite database file
DB_FILE = "comment_watcher.db"

def init_database():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create flagged comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flagged_comments (
            id TEXT PRIMARY KEY,
            keyword TEXT NOT NULL,
            title TEXT,
            date TEXT,
            text_snippet TEXT,
            full_text TEXT,
            organization TEXT,
            submitter_name TEXT,
            document_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create seen IDs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seen_ids (
            comment_id TEXT PRIMARY KEY,
            seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"🗄️  Database initialized: {DB_FILE}")

def save_flagged_comments(comment_list: List[Dict], file: str = None) -> None:
    """
    Save flagged comments to SQLite database.

    Args:
        comment_list: List of flagged comment dictionaries
        file: Ignored for SQLite (kept for compatibility)
    """
    if not comment_list:
        return

    init_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    saved_count = 0
    for comment in comment_list:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO flagged_comments
                (id, keyword, title, date, text_snippet, full_text, organization, submitter_name, document_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                comment['id'],
                comment['keyword'],
                comment['title'],
                comment['date'],
                comment['text_snippet'],
                comment.get('full_text', ''),
                comment.get('organization', ''),
                comment.get('submitter_name', ''),
                comment.get('document_type', '')
            ))
            saved_count += 1
        except sqlite3.Error as e:
            print(f"❌ Error saving comment {comment['id']}: {e}")

    conn.commit()
    conn.close()

    print(f"✅ Saved {saved_count} flagged comments to database")

def load_flagged_comments(file: str = None) -> List[Dict]:
    """
    Load existing flagged comments from SQLite database.

    Args:
        file: Ignored for SQLite (kept for compatibility)

    Returns:
        List of flagged comment dictionaries
    """
    init_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, keyword, title, date, text_snippet, full_text,
               organization, submitter_name, document_type, created_at
        FROM flagged_comments
        ORDER BY created_at DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    comments = []
    for row in rows:
        comments.append({
            'id': row[0],
            'keyword': row[1],
            'title': row[2],
            'date': row[3],
            'text_snippet': row[4],
            'full_text': row[5],
            'organization': row[6],
            'submitter_name': row[7],
            'document_type': row[8],
            'created_at': row[9]
        })

    return comments

def load_seen_ids(file: str = None) -> Set[str]:
    """
    Load previously seen comment IDs from SQLite database.

    Args:
        file: Ignored for SQLite (kept for compatibility)

    Returns:
        Set of previously seen comment IDs
    """
    init_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT comment_id FROM seen_ids')
    rows = cursor.fetchall()
    conn.close()

    return {row[0] for row in rows}

def mark_as_seen(comment_id: str, file: str = None) -> None:
    """
    Mark a comment ID as seen in SQLite database.

    Args:
        comment_id: The comment ID to mark as seen
        file: Ignored for SQLite (kept for compatibility)
    """
    init_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR REPLACE INTO seen_ids (comment_id, seen_at)
            VALUES (?, CURRENT_TIMESTAMP)
        ''', (comment_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error marking comment {comment_id} as seen: {e}")
    finally:
        conn.close()

def get_unique_comments(file: str = None) -> List[Dict]:
    """
    Load and return unique comments from SQLite database.

    Args:
        file: Ignored for SQLite (kept for compatibility)

    Returns:
        List of unique flagged comment dictionaries
    """
    return load_flagged_comments()

def get_comments_by_keyword(keyword: str) -> List[Dict]:
    """
    Get all comments that match a specific keyword.

    Args:
        keyword: The keyword to search for

    Returns:
        List of matching comment dictionaries
    """
    init_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, keyword, title, date, text_snippet, full_text,
               organization, submitter_name, document_type, created_at
        FROM flagged_comments
        WHERE keyword = ?
        ORDER BY created_at DESC
    ''', (keyword,))

    rows = cursor.fetchall()
    conn.close()

    comments = []
    for row in rows:
        comments.append({
            'id': row[0],
            'keyword': row[1],
            'title': row[2],
            'date': row[3],
            'text_snippet': row[4],
            'full_text': row[5],
            'organization': row[6],
            'submitter_name': row[7],
            'document_type': row[8],
            'created_at': row[9]
        })

    return comments

def get_comments_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    Get comments within a date range.

    Args:
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)

    Returns:
        List of comment dictionaries in date range
    """
    init_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, keyword, title, date, text_snippet, full_text,
               organization, submitter_name, document_type, created_at
        FROM flagged_comments
        WHERE date >= ? AND date <= ?
        ORDER BY date DESC
    ''', (start_date, end_date))

    rows = cursor.fetchall()
    conn.close()

    comments = []
    for row in rows:
        comments.append({
            'id': row[0],
            'keyword': row[1],
            'title': row[2],
            'date': row[3],
            'text_snippet': row[4],
            'full_text': row[5],
            'organization': row[6],
            'submitter_name': row[7],
            'document_type': row[8],
            'created_at': row[9]
        })

    return comments

def get_statistics() -> Dict:
    """
    Get database statistics.

    Returns:
        Dictionary with statistics
    """
    init_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Total flagged comments
    cursor.execute('SELECT COUNT(*) FROM flagged_comments')
    total_comments = cursor.fetchone()[0]

    # Total seen IDs
    cursor.execute('SELECT COUNT(*) FROM seen_ids')
    total_seen = cursor.fetchone()[0]

    # Comments by keyword
    cursor.execute('''
        SELECT keyword, COUNT(*)
        FROM flagged_comments
        GROUP BY keyword
    ''')
    keyword_counts = dict(cursor.fetchall())

    # Recent activity (last 7 days)
    cursor.execute('''
        SELECT COUNT(*)
        FROM flagged_comments
        WHERE created_at >= datetime('now', '-7 days')
    ''')
    recent_comments = cursor.fetchone()[0]

    conn.close()

    return {
        'total_flagged_comments': total_comments,
        'total_seen_ids': total_seen,
        'keyword_counts': keyword_counts,
        'recent_comments': recent_comments
    }

def export_to_json(filename: str = None) -> None:
    """
    Export all flagged comments to JSON file.

    Args:
        filename: Output filename (defaults to config OUTPUT_FILE)
    """
    if filename is None:
        filename = OUTPUT_FILE

    comments = load_flagged_comments()

    with open(filename, 'w') as f:
        json.dump(comments, f, indent=2)

    print(f"📤 Exported {len(comments)} comments to {filename}")

def clear_database() -> None:
    """Clear all data from the database (use with caution!)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM flagged_comments')
    cursor.execute('DELETE FROM seen_ids')

    conn.commit()
    conn.close()

    print("🗑️  Database cleared")
