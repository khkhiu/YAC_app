# database/models.py
from datetime import datetime
from typing import Dict, Optional

class User:
    def __init__(self, user_id: int, username: str):
        self.data = {
            "user_id": user_id,
            "username": username,
            "joined_date": datetime.now(),
            "streak": 0,
            "last_completed": None,
            "settings": {
                "anonymous_sharing": False,
                "pairing_enabled": False
            }
        }

class Response:
    def __init__(self, user_id: int, category: str, prompt: str, response: str):
        self.data = {
            "user_id": user_id,
            "category": category,
            "prompt": prompt,
            "response": response,
            "timestamp": datetime.now(),
            "reactions": {"likes": 0, "hearts": 0}
        }
