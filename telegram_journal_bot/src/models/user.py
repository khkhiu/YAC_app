"""User model for the Telegram Journal Bot."""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from datetime import datetime

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
    timezone: str = 'UTC'
    last_prompt: Optional[Dict] = None
    responses: List[JournalEntry] = None

    def __post_init__(self):
        """Initialize empty responses list if None."""
        if self.responses is None:
            self.responses = []

    @classmethod
    def from_dict(cls, user_id: str, data: Dict) -> 'User':
        """Create a User instance from a dictionary."""
        responses = [
            JournalEntry.from_dict(entry)
            for entry in data.get('responses', [])
        ]
        return cls(
            id=user_id,
            timezone=data.get('timezone', 'UTC'),
            last_prompt=data.get('last_prompt'),
            responses=responses
        )

    def to_dict(self) -> Dict:
        """Convert the user to a dictionary."""
        return {
            'timezone': self.timezone,
            'last_prompt': self.last_prompt,
            'responses': [entry.to_dict() for entry in self.responses]
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
