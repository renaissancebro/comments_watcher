#!/usr/bin/env python3
"""
Comment Watcher - Monitor regulations.gov for specific keywords
Main orchestration module.
"""

from typing import List, Dict, Tuple
from config import KEYWORDS, validate_config
from fetcher import fetch_metadata, fetch_comment_detail
from filter import flag_by_keyword, recheck_full_text
from notifier import send_alerts, print_summary, print_keywords
from storage import save_flagged_comments, load_seen_ids, mark_as_seen

def process_comment(comment_data: Dict, matched_keyword: str) -> Dict:
    """
    Process a comment into a standardized format.

    Args:
        comment_data: Full comment data from API
        matched_keyword: The keyword that triggered the match

    Returns:
        Processed comment dictionary
    """
    attributes = comment_data["attributes"]
    text = attributes.get("comment", "")

    return {
        "id": comment_data["id"],
        "keyword": matched_keyword,
        "title": attributes.get("title", ""),
        "date": attributes.get("postedDate", ""),
        "text_snippet": text[:200] + ("…" if len(text) > 200 else ""),
        "full_text": text,
        "organization": attributes.get("organization", ""),
        "submitter_name": attributes.get("submitterName", ""),
        "document_type": attributes.get("documentType", "")
    }

def run_monitoring_cycle(since_date: str = None, page_size: int = None) -> Dict:
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
    validate_config()
    print_keywords(KEYWORDS)

    # Load previously seen IDs to avoid duplicates
    seen_ids = load_seen_ids()
    print(f"📚 Loaded {len(seen_ids)} previously seen comment IDs")

    # Step 1: Fetch metadata
    print(f"\n📥 STEP 1: Fetching comment metadata...")
    metadata = fetch_metadata(since_date, page_size)

    # Step 2: Flag by keyword
    print(f"\n🔍 STEP 2: Scanning for keyword matches...")
    flagged_ids = flag_by_keyword(metadata, KEYWORDS)

    # Step 3: Fetch full details and process
    relevant_comments = []
    if flagged_ids:
        print(f"\n📄 STEP 3: Fetching full details for {len(flagged_ids)} flagged comments...")
        for i, (comment_id, keyword) in enumerate(flagged_ids, 1):
            # Skip if already seen
            if comment_id in seen_ids:
                print(f"   ⏭️  Skip #{i}: Comment {comment_id} already processed")
                continue

            try:
                print(f"\n   📋 Processing match #{i}/{len(flagged_ids)}...")
                comment_data = fetch_comment_detail(comment_id)

                # Double-check with full text
                confirmed_keyword = recheck_full_text(comment_data, KEYWORDS)
                if confirmed_keyword:
                    processed_comment = process_comment(comment_data, confirmed_keyword)
                    relevant_comments.append(processed_comment)
                    mark_as_seen(comment_id)  # Mark as seen
                    print(f"   ✅ Successfully processed comment {comment_id}")
                else:
                    print(f"   ⚠️  Keyword not confirmed in full text for {comment_id}")

            except Exception as e:
                print(f"   ❌ Error fetching comment {comment_id}: {e}")
    else:
        print(f"\n📄 STEP 3: No flagged comments to fetch details for.")

    # Step 4: Send alerts
    print(f"\n🚨 STEP 4: Processing alerts...")
    send_alerts(relevant_comments)

    # Step 5: Save results
    if relevant_comments:
        print(f"\n💾 STEP 5: Saving results...")
        save_flagged_comments(relevant_comments)
    else:
        print(f"\n💾 STEP 5: No results to save.")

    # Step 6: Print summary
    print(f"\n📊 STEP 6: Final summary...")
    print_summary(len(metadata), len(relevant_comments))

    print("\n" + "=" * 60)

    return {
        "total_checked": len(metadata),
        "flagged_count": len(relevant_comments),
        "flagged_comments": relevant_comments
    }

def main():
    """Main entry point for the comment watcher application."""
    # Run a monitoring cycle
    # You can customize these parameters:
    # - since_date: "2024-01-01" for date filtering
    # - page_size: 50 for more comments per run
    results = run_monitoring_cycle(
        since_date=None,  # Get recent comments without date filter
        page_size=20      # Check 20 comments per run
    )

    print(f"\n🎉 Monitoring cycle completed!")
    print(f"📈 Results: {results['flagged_count']} flagged out of {results['total_checked']} checked")

if __name__ == "__main__":
    main()
