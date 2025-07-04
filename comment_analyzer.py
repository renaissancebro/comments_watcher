from typing import List, Dict, Tuple
from config import Config

class CommentAnalyzer:
    """Analyzes comments for keyword matches and processes relevant data."""

    def __init__(self, keywords: List[str] = None):
        self.keywords = keywords or Config.KEYWORDS

    def find_keyword_matches(self, metadata: List[Dict]) -> List[Tuple[str, str]]:
        """
        Scan comment metadata for keyword matches.

        Args:
            metadata: List of comment metadata dictionaries

        Returns:
            List of tuples (comment_id, matched_keyword)
        """
        flagged = []

        print(f"\n🔍 Scanning {len(metadata)} comments for keywords: {', '.join(self.keywords)}")

        for i, item in enumerate(metadata, 1):
            snippet = item["attributes"].get("highlightedContent", "") or ""
            title = item["attributes"].get("title", "") or ""
            combined = (snippet + title).lower()
            comment_id = item["id"]

            # Check each keyword
            matched_keyword = None
            for keyword in self.keywords:
                if keyword.lower() in combined:
                    matched_keyword = keyword
                    break

            if matched_keyword:
                flagged.append((comment_id, matched_keyword))
                print(f"  🎯 MATCH #{i}: '{matched_keyword}' in comment {comment_id}")
                print(f"     Title: {title[:50]}{'...' if len(title) > 50 else ''}")
            else:
                print(f"  ⏭️  Skip #{i}: No keywords found in comment {comment_id}")

        print(f"\n📊 Scan complete: {len(flagged)} matches found out of {len(metadata)} comments")

        return flagged

    def process_comment_details(self, comment_data: Dict, matched_keyword: str) -> Dict:
        """
        Process full comment details into a standardized format.

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
