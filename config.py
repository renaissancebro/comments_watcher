import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv("API_KEY", "DEMO_KEY")
BASE_URL = "https://api.regulations.gov/v4/comments"

# Search Configuration
KEYWORDS = ["pesticide", "glyphosate", "worker safety"]

# Request Configuration
DEFAULT_PAGE_SIZE = 20
REQUEST_DELAY = 0.1  # seconds between requests

# File Configuration
OUTPUT_FILE = "flagged_comments.json"
SEEN_IDS_FILE = "seen_ids.json"

# Notification Configuration
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "")
EMAIL_WEBHOOK_URL = os.getenv("EMAIL_WEBHOOK_URL", "")
ENABLE_TEAMS_ALERTS = os.getenv("ENABLE_TEAMS_ALERTS", "false").lower() == "true"
ENABLE_EMAIL_ALERTS = os.getenv("ENABLE_EMAIL_ALERTS", "false").lower() == "true"

# Validation
def validate_config():
    """Validate configuration settings."""
    if not API_KEY or API_KEY == "DEMO_KEY":
        print("⚠️  Warning: Using DEMO_KEY. For production, set API_KEY in .env file")

    print(f"🔑 API Key loaded: {API_KEY[:10]}..." if len(API_KEY) > 10 else f"🔑 API Key loaded: {API_KEY}")
    print(f"📁 Current working directory: {os.getcwd()}")
    print(f"📄 .env file exists: {os.path.exists('.env')}")

    # Check notification settings
    if ENABLE_TEAMS_ALERTS and not TEAMS_WEBHOOK_URL:
        print("⚠️  Warning: Teams alerts enabled but TEAMS_WEBHOOK_URL not set")
    if ENABLE_EMAIL_ALERTS and not EMAIL_WEBHOOK_URL:
        print("⚠️  Warning: Email alerts enabled but EMAIL_WEBHOOK_URL not set")
