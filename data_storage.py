import json
from typing import List, Dict
from config import Config

class DataStorage:
    """Handles saving and loading flagged comments data."""

    def __init__(self, filename: str = None):
        self.filename = filename or Config.OUTPUT_FILE

    def save_flagged_comments(self, comments: List[Dict]) -> None:
        """
        Save flagged comments to JSON file, appending to existing data.

        Args:
            comments: List of flagged comment dictionaries
        """
        try:
            # Load existing data
            existing = self.load_flagged_comments()
        except FileNotFoundError:
            existing = []

        # Add new comments
        existing.extend(comments)

        # Save back to file
        with open(self.filename, "w") as f:
            json.dump(existing, f, indent=2)

        print(f"✅ Saved {len(comments)} flagged comments to {self.filename}")

    def load_flagged_comments(self) -> List[Dict]:
        """
        Load existing flagged comments from JSON file.

        Returns:
            List of flagged comment dictionaries

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        with open(self.filename, "r") as f:
            return json.load(f)

    def get_unique_comments(self) -> List[Dict]:
        """
        Load and return unique comments (no duplicates by ID).

        Returns:
            List of unique flagged comment dictionaries
        """
        try:
            comments = self.load_flagged_comments()
            # Remove duplicates based on comment ID
            seen_ids = set()
            unique_comments = []

            for comment in comments:
                if comment["id"] not in seen_ids:
                    seen_ids.add(comment["id"])
                    unique_comments.append(comment)

            return unique_comments
        except FileNotFoundError:
            return []
