"""Storage service for managing user data persistence."""

import json
import os
from typing import Dict, Optional
from src.models.user import User
from src.utils.logger import get_logger

logger = get_logger(__name__)

class StorageService:
    """Handles persistence of user data."""

    def __init__(self, file_path: str):
        """Initialize storage service with file path."""
        self.file_path = file_path
        self.users: Dict[str, User] = {}
        self._ensure_storage_directory()
        self._load_users()

    def _ensure_storage_directory(self):
        """Ensure the storage directory exists."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def _load_users(self):
        """Load users from storage file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    self.users = {
                        user_id: User.from_dict(user_id, user_data)
                        for user_id, user_data in data.items()
                    }
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            self.users = {}

    def save_users(self):
        """Save users to storage file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(
                    {user_id: user.to_dict() for user_id, user in self.users.items()},
                    f,
                    indent=2
                )
        except Exception as e:
            logger.error(f"Error saving users: {e}")

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)

    def add_user(self, user: User):
        """Add or update a user."""
        self.users[user.id] = user
        self.save_users()

    def get_all_users(self) -> Dict[str, User]:
        """Get all users."""
        return self.users.copy()

    def delete_user(self, user_id: str):
        """Delete a user."""
        if user_id in self.users:
            del self.users[user_id]
            self.save_users()
