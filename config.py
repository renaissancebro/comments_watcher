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

# Validation
def validate_config():
    """Validate configuration settings."""
    if not API_KEY or API_KEY == "DEMO_KEY":
        print("⚠️  Warning: Using DEMO_KEY. For production, set API_KEY in .env file")

    print(f"🔑 API Key loaded: {API_KEY[:10]}..." if len(API_KEY) > 10 else f"🔑 API Key loaded: {API_KEY}")
    print(f"📁 Current working directory: {os.getcwd()}")
    print(f"📄 .env file exists: {os.path.exists('.env')}")
