from typing import List, Dict, Tuple, Optional

def flag_by_keyword(metadata_list: List[Dict], keyword_list: List[str]) -> List[Tuple[str, str]]:
    """
    Flag comments by scanning metadata for keyword matches.

    Args:
        metadata_list: List of comment metadata dictionaries
        keyword_list: List of keywords to search for

    Returns:
        List of tuples (comment_id, matched_keyword)
    """
    flagged = []

    print(f"\n🔍 Scanning {len(metadata_list)} comments for keywords: {', '.join(keyword_list)}")

    for i, item in enumerate(metadata_list, 1):
        snippet = item["attributes"].get("highlightedContent", "") or ""
        title = item["attributes"].get("title", "") or ""
        combined = (snippet + title).lower()
        comment_id = item["id"]

        # Check each keyword
        matched_keyword = None
        for keyword in keyword_list:
            if keyword.lower() in combined:
                matched_keyword = keyword
                break

        if matched_keyword:
            flagged.append((comment_id, matched_keyword))
            print(f"  🎯 MATCH #{i}: '{matched_keyword}' in comment {comment_id}")
            print(f"     Title: {title[:50]}{'...' if len(title) > 50 else ''}")
        else:
            print(f"  ⏭️  Skip #{i}: No keywords found in comment {comment_id}")

    print(f"\n📊 Scan complete: {len(flagged)} matches found out of {len(metadata_list)} comments")

    return flagged

def recheck_full_text(full_comment: Dict, keyword_list: List[str]) -> Optional[str]:
    """
    Recheck full comment text for keyword matches (double-check after metadata scan).

    Args:
        full_comment: Full comment data dictionary
        keyword_list: List of keywords to search for

    Returns:
        Matched keyword if found, None otherwise
    """
    text = full_comment["attributes"].get("comment", "")
    title = full_comment["attributes"].get("title", "")
    combined = (text + title).lower()

    for keyword in keyword_list:
        if keyword.lower() in combined:
            return keyword

    return None
