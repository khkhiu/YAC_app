"""User model for the Telegram Journal Bot."""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from datetime import datetime
from src.config import SINGAPORE_TIMEZONE

@dataclass
class JournalEntry:
    """Represents a single journal entry."""
    prompt: str
    response: str
    timestamp: str
    prompt_type: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'JournalEntry':
        """Create a JournalEntry instance from a dictionary."""
        return cls(
            prompt=data['prompt'],
            response=data['response'],
            timestamp=data['timestamp'],
            prompt_type=data.get('prompt_type', 'unknown')
        )

    def to_dict(self) -> Dict:
        """Convert the entry to a dictionary."""
        return asdict(self)

@dataclass
class User:
    """Represents a user of the journal bot."""
    id: str
    timezone: str = SINGAPORE_TIMEZONE  # Always initialized with Singapore timezone
    last_prompt: Optional[Dict] = None
    responses: List[JournalEntry] = None
    preferred_prompt_day: int = 0  # Default is Monday (0)
    preferred_prompt_hour: int = 9  # Default is 9 AM

    def __post_init__(self):
        """Initialize empty responses list if None and ensure Singapore timezone."""
        if self.responses is None:
            self.responses = []
        # Always ensure Singapore timezone
        self.timezone = SINGAPORE_TIMEZONE

    @classmethod
    def from_dict(cls, user_id: str, data: Dict) -> 'User':
        """Create a User instance from a dictionary."""
        responses = [
            JournalEntry.from_dict(entry) 
            for entry in data.get('responses', [])
        ]
        return cls(
            id=user_id,
            timezone=SINGAPORE_TIMEZONE,  # Always use Singapore timezone
            last_prompt=data.get('last_prompt'),
            responses=responses,
            preferred_prompt_day=data.get('preferred_prompt_day', 0),
            preferred_prompt_hour=data.get('preferred_prompt_hour', 9)
        )

    def to_dict(self) -> Dict:
        """Convert the user to a dictionary."""
        return {
            'timezone': SINGAPORE_TIMEZONE,  # Always save Singapore timezone
            'last_prompt': self.last_prompt,
            'responses': [entry.to_dict() for entry in self.responses],
            'preferred_prompt_day': self.preferred_prompt_day,
            'preferred_prompt_hour': self.preferred_prompt_hour
        }

    def add_response(self, entry: JournalEntry):
        """Add a new journal entry."""
        self.responses.append(entry)

    def get_recent_entries(self, limit: int) -> List[JournalEntry]:
        """Get the most recent journal entries."""
        return sorted(
            self.responses,
            key=lambda x: datetime.fromisoformat(x.timestamp),
            reverse=True
        )[:limit]