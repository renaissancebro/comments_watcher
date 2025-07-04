from typing import List, Dict

class Notifier:
    """Handles alerting and notification output."""

    def __init__(self):
        pass

    def send_alert(self, comments: List[Dict]) -> None:
        """
        Send alerts for flagged comments.

        Args:
            comments: List of flagged comment dictionaries
        """
        if not comments:
            print("✅ No flagged comments this run.")
            return

        print(f"🚨 Found {len(comments)} flagged comments!")
        print("=" * 60)

        for comment in comments:
            self._print_comment_alert(comment)

    def _print_comment_alert(self, comment: Dict) -> None:
        """
        Print formatted alert for a single comment.

        Args:
            comment: Comment dictionary
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
        print(msg)

    def print_summary(self, total_checked: int, flagged_count: int) -> None:
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

    def print_keywords(self, keywords: List[str]) -> None:
        """
        Print the keywords being monitored.

        Args:
            keywords: List of keywords being searched
        """
        print(f"🔍 Monitoring for keywords: {', '.join(keywords)}")
