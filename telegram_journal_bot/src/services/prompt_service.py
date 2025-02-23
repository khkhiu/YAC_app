"""Service for managing and delivering prompts."""

import random
from datetime import datetime
import pytz
from typing import Tuple, Dict
from src.models.user import User, JournalEntry
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PromptService:
    """Manages prompt selection and delivery."""

    def __init__(self, prompts: Dict[str, list]):
        """Initialize with prompt dictionary."""
        self.prompts = prompts

    def get_random_prompt(self) -> Tuple[str, str]:
        """Get a random prompt and its type."""
        prompt_type = random.choice(list(self.prompts.keys()))
        prompt = random.choice(self.prompts[prompt_type])
        return prompt, prompt_type

    def create_journal_entry(self, prompt: str, response: str, prompt_type: str) -> JournalEntry:
        """Create a new journal entry."""
        return JournalEntry(
            prompt=prompt,
            response=response,
            timestamp=datetime.now().isoformat(),
            prompt_type=prompt_type
        )

    def should_send_prompt(self, user: User, target_hour: int, target_day: int) -> bool:
        """Check if it's time to send a prompt to the user."""
        try:
            # Always use Singapore timezone
            sg_tz = pytz.timezone('Asia/Singapore')
            current_time = datetime.now(sg_tz)
            return (
                current_time.weekday() == target_day and 
                current_time.hour == target_hour
            )
        except Exception as e:
            logger.error(f"Error checking prompt time for user {user.id}: {e}")
            return False
