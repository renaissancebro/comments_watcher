import requests
import json
from typing import List, Dict
from config import (
    TEAMS_WEBHOOK_URL,
    EMAIL_WEBHOOK_URL,
    ENABLE_TEAMS_ALERTS,
    ENABLE_EMAIL_ALERTS
)

def format_alert(comment: Dict) -> str:
    """
    Format a comment into a console alert message.

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
        f"🔗 Link: https://www.regulations.gov/comment/{comment['id']}\n"
        f"👤 Submitter: {comment.get('submitter_name', 'N/A')}\n"
        f"🏢 Organization: {comment.get('organization', 'N/A')}\n"
        f"📄 Snippet: {comment['text_snippet']}\n"
        "—" * 60
    )
    return msg

def format_teams_message(comment: Dict) -> Dict:
    """
    Format a comment for Microsoft Teams webhook.

    Args:
        comment: Comment dictionary with processed data

    Returns:
        Teams message card dictionary
    """
    # Create the comment URL
    comment_url = f"https://www.regulations.gov/comment/{comment['id']}"

    # Format the message card
    message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": f"New Comment Alert: {comment['keyword']}",
        "sections": [
            {
                "activityTitle": f"🔔 New Comment Alert: '{comment['keyword']}'",
                "activitySubtitle": f"Posted on {comment['date']}",
                "activityImage": "https://www.regulations.gov/favicon.ico",
                "facts": [
                    {
                        "name": "Title",
                        "value": comment['title']
                    },
                    {
                        "name": "Comment ID",
                        "value": comment['id']
                    },
                    {
                        "name": "Submitter",
                        "value": comment.get('submitter_name', 'N/A')
                    },
                    {
                        "name": "Organization",
                        "value": comment.get('organization', 'N/A')
                    },
                    {
                        "name": "Document Type",
                        "value": comment.get('document_type', 'N/A')
                    }
                ],
                "text": comment['text_snippet']
            }
        ],
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "View Comment",
                "targets": [
                    {
                        "os": "default",
                        "uri": comment_url
                    }
                ]
            }
        ]
    }

    return message

def format_email_message(comment: Dict) -> Dict:
    """
    Format a comment for email webhook.

    Args:
        comment: Comment dictionary with processed data

    Returns:
        Email message dictionary
    """
    comment_url = f"https://www.regulations.gov/comment/{comment['id']}"

    message = {
        "subject": f"Comment Alert: {comment['keyword']} - {comment['title'][:50]}...",
        "body": f"""
New Comment Alert

Keyword Matched: {comment['keyword']}
Title: {comment['title']}
Comment ID: {comment['id']}
Posted Date: {comment['date']}
Submitter: {comment.get('submitter_name', 'N/A')}
Organization: {comment.get('organization', 'N/A')}
Document Type: {comment.get('document_type', 'N/A')}

Snippet:
{comment['text_snippet']}

View full comment: {comment_url}

---
Comment Watcher Alert System
        """.strip(),
        "html_body": f"""
<html>
<body>
<h2>🔔 New Comment Alert</h2>
<p><strong>Keyword Matched:</strong> {comment['keyword']}</p>
<p><strong>Title:</strong> {comment['title']}</p>
<p><strong>Comment ID:</strong> {comment['id']}</p>
<p><strong>Posted Date:</strong> {comment['date']}</p>
<p><strong>Submitter:</strong> {comment.get('submitter_name', 'N/A')}</p>
<p><strong>Organization:</strong> {comment.get('organization', 'N/A')}</p>
<p><strong>Document Type:</strong> {comment.get('document_type', 'N/A')}</p>

<h3>Snippet:</h3>
<p>{comment['text_snippet']}</p>

<p><a href="{comment_url}" style="background-color: #0076D7; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Full Comment</a></p>

<hr>
<p><em>Comment Watcher Alert System</em></p>
</body>
</html>
        """.strip()
    }

    return message

def send_teams_alert(comment: Dict) -> bool:
    """
    Send alert to Microsoft Teams webhook.

    Args:
        comment: Comment dictionary with processed data

    Returns:
        True if successful, False otherwise
    """
    if not ENABLE_TEAMS_ALERTS or not TEAMS_WEBHOOK_URL:
        return False

    try:
        message = format_teams_message(comment)
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            json=message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            print(f"   ✅ Teams alert sent for comment {comment['id']}")
            return True
        else:
            print(f"   ❌ Teams alert failed for comment {comment['id']}: {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Teams alert error for comment {comment['id']}: {e}")
        return False

def send_email_alert(comment: Dict) -> bool:
    """
    Send alert via email webhook.

    Args:
        comment: Comment dictionary with processed data

    Returns:
        True if successful, False otherwise
    """
    if not ENABLE_EMAIL_ALERTS or not EMAIL_WEBHOOK_URL:
        return False

    try:
        message = format_email_message(comment)
        response = requests.post(
            EMAIL_WEBHOOK_URL,
            json=message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            print(f"   ✅ Email alert sent for comment {comment['id']}")
            return True
        else:
            print(f"   ❌ Email alert failed for comment {comment['id']}: {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Email alert error for comment {comment['id']}: {e}")
        return False

def send_alert(formatted_message: str) -> None:
    """
    Send a console alert (currently just prints, but could be extended).

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

    teams_sent = 0
    email_sent = 0

    for comment in comments:
        # Console alert
        formatted_msg = format_alert(comment)
        send_alert(formatted_msg)

        # Teams alert
        if send_teams_alert(comment):
            teams_sent += 1

        # Email alert
        if send_email_alert(comment):
            email_sent += 1

    # Summary of notifications sent
    if ENABLE_TEAMS_ALERTS or ENABLE_EMAIL_ALERTS:
        print(f"\n📧 Notification Summary:")
        if ENABLE_TEAMS_ALERTS:
            print(f"   Teams alerts: {teams_sent}/{len(comments)} sent")
        if ENABLE_EMAIL_ALERTS:
            print(f"   Email alerts: {email_sent}/{len(comments)} sent")

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

def test_notifications():
    """
    Test function to verify Teams and email notifications work.
    """
    test_comment = {
        "id": "TEST-123-456",
        "keyword": "pesticide",
        "title": "Test Comment - Pesticide Regulation Review",
        "date": "2024-01-15",
        "text_snippet": "This is a test comment about pesticide regulations and their impact on agricultural practices...",
        "full_text": "This is a test comment about pesticide regulations and their impact on agricultural practices. We need to ensure proper safety measures are in place.",
        "organization": "Test Organization",
        "submitter_name": "John Doe",
        "document_type": "Comment"
    }

    print("🧪 Testing notification systems...")
    print("=" * 50)

    # Test console output
    print("\n📺 Console Alert:")
    formatted_msg = format_alert(test_comment)
    print(formatted_msg)

    # Test Teams
    if ENABLE_TEAMS_ALERTS and TEAMS_WEBHOOK_URL:
        print(f"\n💬 Teams Alert:")
        success = send_teams_alert(test_comment)
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    else:
        print(f"\n💬 Teams Alert: Disabled (ENABLE_TEAMS_ALERTS={ENABLE_TEAMS_ALERTS}, URL={'Set' if TEAMS_WEBHOOK_URL else 'Not set'})")

    # Test Email
    if ENABLE_EMAIL_ALERTS and EMAIL_WEBHOOK_URL:
        print(f"\n📧 Email Alert:")
        success = send_email_alert(test_comment)
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    else:
        print(f"\n📧 Email Alert: Disabled (ENABLE_EMAIL_ALERTS={ENABLE_EMAIL_ALERTS}, URL={'Set' if EMAIL_WEBHOOK_URL else 'Not set'})")

    print("\n" + "=" * 50)
