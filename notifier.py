from typing import List, Dict

def format_alert(comment: Dict) -> str:
    """
    Format a comment into an alert message.

    Args:
        comment: Comment dictionary with processed data

    Returns:
        Formatted alert string
    """
    msg = (
        f"🔔 MATCH: '{comment['keyword']}'\n"
        f"📋 ID: {comment['id']}\n"
        f"📅 Date: {comment['date']}\n"
        f"📝 Title: {comment['title']}\n"
        f"👤 Submitter: {comment.get('submitter_name', 'N/A')}\n"
        f"🏢 Organization: {comment.get('organization', 'N/A')}\n"
        f"📄 Snippet: {comment['text_snippet']}\n"
        "—" * 60
    )
    return msg

def send_alert(formatted_message: str) -> None:
    """
    Send an alert (currently just prints, but could be extended for email/Teams).

    Args:
        formatted_message: The formatted alert message to send
    """
    print(formatted_message)

def send_alerts(comments: List[Dict]) -> None:
    """
    Send alerts for multiple flagged comments.

    Args:
        comments: List of flagged comment dictionaries
    """
    if not comments:
        print("✅ No flagged comments this run.")
        return

    print(f"🚨 Found {len(comments)} flagged comments!")
    print("=" * 60)

    for comment in comments:
        formatted_msg = format_alert(comment)
        send_alert(formatted_msg)

def print_summary(total_checked: int, flagged_count: int) -> None:
    """
    Print a summary of the monitoring run.

    Args:
        total_checked: Total number of comments checked
        flagged_count: Number of comments flagged
    """
    print(f"\n📊 SUMMARY:")
    print(f"   Comments checked: {total_checked}")
    print(f"   Comments flagged: {flagged_count}")
    print(f"   Flag rate: {(flagged_count/total_checked*100):.1f}%" if total_checked > 0 else "   Flag rate: 0%")

def print_keywords(keywords: List[str]) -> None:
    """
    Print the keywords being monitored.

    Args:
        keywords: List of keywords being searched
    """
    print(f"🔍 Monitoring for keywords: {', '.join(keywords)}")
