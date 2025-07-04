import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the comment watcher."""

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

    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        if not cls.API_KEY or cls.API_KEY == "DEMO_KEY":
            print("⚠️  Warning: Using DEMO_KEY. For production, set API_KEY in .env file")

        print(f"🔑 API Key loaded: {cls.API_KEY[:10]}..." if len(cls.API_KEY) > 10 else f"🔑 API Key loaded: {cls.API_KEY}")
        print(f"📁 Current working directory: {os.getcwd()}")
        print(f"📄 .env file exists: {os.path.exists('.env')}")
