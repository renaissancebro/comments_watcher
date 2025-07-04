from typing import List, Dict, Optional
from config import Config
from api_client import RegulationsAPIClient
from comment_analyzer import CommentAnalyzer
from data_storage import DataStorage
from notifier import Notifier

class CommentWatcher:
    """Main orchestrator for monitoring regulations.gov comments."""

    def __init__(self):
        self.api_client = RegulationsAPIClient()
        self.analyzer = CommentAnalyzer()
        self.storage = DataStorage()
        self.notifier = Notifier()

    def run_monitoring_cycle(self, since_date: Optional[str] = None, page_size: int = None) -> Dict:
        """
        Run a complete monitoring cycle.

        Args:
            since_date: Optional date filter
            page_size: Number of comments to check

        Returns:
            Dictionary with monitoring results
        """
        print("🚀 Starting comment monitoring cycle...")
        print("=" * 60)

        # Validate configuration
        Config.validate()
        self.notifier.print_keywords(self.analyzer.keywords)

        # Step 1: Fetch comment metadata
        print(f"\n📥 STEP 1: Fetching comment metadata...")
        metadata = self.api_client.get_comments_metadata(since_date, page_size)
        print(f"📊 Retrieved {len(metadata)} comments")

        # Step 2: Find keyword matches
        print(f"\n🔍 STEP 2: Scanning for keyword matches...")
        flagged_ids = self.analyzer.find_keyword_matches(metadata)
        print(f"🎯 Found {len(flagged_ids)} potential matches")

        # Step 3: Fetch full details for flagged comments
        relevant_comments = []
        if flagged_ids:
            print(f"\n📄 STEP 3: Fetching full details for {len(flagged_ids)} flagged comments...")
            for i, (comment_id, keyword) in enumerate(flagged_ids, 1):
                try:
                    print(f"\n   📋 Processing match #{i}/{len(flagged_ids)}...")
                    comment_data = self.api_client.get_comment_details(comment_id)
                    processed_comment = self.analyzer.process_comment_details(comment_data, keyword)
                    relevant_comments.append(processed_comment)
                    print(f"   ✅ Successfully processed comment {comment_id}")
                except Exception as e:
                    print(f"   ❌ Error fetching comment {comment_id}: {e}")
        else:
            print(f"\n📄 STEP 3: No flagged comments to fetch details for.")

        # Step 4: Send alerts
        print(f"\n🚨 STEP 4: Processing alerts...")
        self.notifier.send_alert(relevant_comments)

        # Step 5: Save results
        if relevant_comments:
            print(f"\n💾 STEP 5: Saving results...")
            self.storage.save_flagged_comments(relevant_comments)
        else:
            print(f"\n💾 STEP 5: No results to save.")

        # Step 6: Print summary
        print(f"\n📊 STEP 6: Final summary...")
        self.notifier.print_summary(len(metadata), len(relevant_comments))

        print("\n" + "=" * 60)

        return {
            "total_checked": len(metadata),
            "flagged_count": len(relevant_comments),
            "flagged_comments": relevant_comments
        }

    def get_historical_data(self) -> List[Dict]:
        """
        Get all previously saved flagged comments.

        Returns:
            List of unique flagged comments
        """
        return self.storage.get_unique_comments()
