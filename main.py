import requests
import json
import time
import os
from dotenv import load_dotenv

# 📌 CONFIG
load_dotenv()
API_KEY = os.getenv("API_KEY", "DEMO_KEY")  # Replace with your own api.data.gov key for production
BASE_URL = "https://api.regulations.gov/v4/comments"
KEYWORDS = ["pesticide", "glyphosate", "worker safety"]

# 🧩 STEP 1: Fetch metadata
def request_comments(since_date=None, page_size=20):
    params = {
        "page[size]": page_size,
        "sort": "lastModifiedDate",
    }
    if since_date:
        params["filter[lastModifiedDate][ge]"] = since_date
    headers = {"X-Api-Key": API_KEY}
    resp = requests.get(BASE_URL, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]

# 🔍 STEP 2: Keyword scan on metadata snippet/title
def keyword_search(metadata):
    flagged = []
    for item in metadata:
        snippet = item["attributes"].get("highlightedContent", "") or ""
        title = item["attributes"].get("title", "") or ""
        combined = (snippet + title).lower()
        for kw in KEYWORDS:
            if kw.lower() in combined:
                flagged.append((item["id"], kw))
                break
    return flagged

# 📄 STEP 3: Fetch full comment text
def review_comments(flagged):
    relevant = []
    headers = {"X-Api-Key": API_KEY}
    for comment_id, kw in flagged:
        url = f"{BASE_URL}/{comment_id}"
        resp = requests.get(url, headers=headers, params={"include": "attachments"})
        resp.raise_for_status()
        data = resp.json()["data"]
        text = data["attributes"].get("comment", "")
        relevant.append({
            "id": comment_id,
            "keyword": kw,
            "title": data["attributes"].get("title", ""),
            "date": data["attributes"].get("postedDate", ""),
            "text_snippet": text[:200] + ("…" if len(text) > 200 else "")
        })
        time.sleep(0.1)  # polite pause
    return relevant

# 🚨 STEP 4: Send / print alert
def send_alert(comments):
    if not comments:
        print("✅ No flagged comments this run.")
        return
    for c in comments:
        msg = (
            f"🔔 MATCH: '{c['keyword']}'\n"
            f"ID: {c['id']}\n"
            f"Date: {c['date']}\n"
            f"Title: {c['title']}\n"
            f"Snippet: {c['text_snippet']}\n"
            "—" * 40
        )
        print(msg)
        # (Optional) Integrate email or Teams webhook here instead of print

# 💾 Optional: Save results
def save_flagged_comments(comments, filename="flagged_comments.json"):
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = []
    existing.extend(comments)
    with open(filename, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"✅ Saved {len(comments)} flagged comments to {filename}")

# 🧪 MAIN DEMO FLOW
if __name__ == "__main__":
    metadata = request_comments(since_date="2025-07-01")  # adjust as needed
    flagged = keyword_search(metadata)
    relevant = review_comments(flagged)
    send_alert(relevant)
    save_flagged_comments(relevant)
