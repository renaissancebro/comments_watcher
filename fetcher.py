import requests
import time
from typing import List, Dict, Optional
from config import API_KEY, BASE_URL, DEFAULT_PAGE_SIZE, REQUEST_DELAY

def fetch_metadata(since_date: Optional[str] = None, page_size: int = None) -> List[Dict]:
    """
    Fetch comment metadata from the Regulations.gov API.

    Args:
        since_date: Optional date filter (YYYY-MM-DD format)
        page_size: Number of comments to fetch

    Returns:
        List of comment metadata dictionaries
    """
    if page_size is None:
        page_size = DEFAULT_PAGE_SIZE

    params = {
        "page[size]": page_size,
        "sort": "lastModifiedDate",
    }

    # Temporarily remove date filter to test API connection
    # if since_date:
    #     params["filter[lastModifiedDate][ge]"] = since_date

    headers = {"X-Api-Key": API_KEY}

    print(f"🌐 Making request to: {BASE_URL}")
    print(f"📋 Parameters: {params}")

    resp = requests.get(BASE_URL, params=params, headers=headers)

    if resp.status_code != 200:
        print(f"❌ API Error: {resp.status_code}")
        print(f"📄 Response: {resp.text}")
        resp.raise_for_status()

    data = resp.json()["data"]

    # Log the comments being fetched
    print(f"\n📥 Fetched {len(data)} comments:")
    for i, comment in enumerate(data, 1):
        title = comment["attributes"].get("title", "No title")
        comment_id = comment["id"]
        date = comment["attributes"].get("postedDate", "No date")[:10]  # Just the date part
        print(f"  {i:2d}. [{comment_id}] {date} - {title[:60]}{'...' if len(title) > 60 else ''}")

    return data

def fetch_comment_detail(comment_id: str) -> Dict:
    """
    Fetch full details for a specific comment.

    Args:
        comment_id: The ID of the comment to fetch

    Returns:
        Comment details dictionary
    """
    url = f"{BASE_URL}/{comment_id}"
    headers = {"X-Api-Key": API_KEY}

    print(f"📄 Fetching details for comment: {comment_id}")

    resp = requests.get(url, headers=headers, params={"include": "attachments"})
    resp.raise_for_status()

    data = resp.json()["data"]
    title = data["attributes"].get("title", "No title")
    print(f"   ✅ Retrieved: {title[:50]}{'...' if len(title) > 50 else ''}")

    # Add polite delay between requests
    time.sleep(REQUEST_DELAY)

    return data
