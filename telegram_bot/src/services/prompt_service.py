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
        self.prompt_history = {}  # Track which prompts have been sent to avoid repetition
        self.user_prompt_counts = {}  # Track number of prompts per user

    def get_random_prompt(self) -> Tuple[str, str]:
        """Get a random prompt and its type."""
        prompt_type = random.choice(list(self.prompts.keys()))
        prompt = random.choice(self.prompts[prompt_type])
        return prompt, prompt_type
    
    def get_prompt_by_type(self, prompt_type: str) -> str:
        """Get a prompt of a specific type, avoiding repetition if possible."""
        if prompt_type not in self.prompts:
            logger.warning(f"Unknown prompt type: {prompt_type}, defaulting to random type")
            return self.get_random_prompt()[0]
            
        # Initialize history for this type if not exists
        if prompt_type not in self.prompt_history:
            self.prompt_history[prompt_type] = []
            
        available_prompts = [p for p in self.prompts[prompt_type] 
                            if p not in self.prompt_history[prompt_type]]
        
        # If all prompts have been used, reset history
        if not available_prompts:
            logger.info(f"All prompts of type {prompt_type} have been used, resetting history")
            self.prompt_history[prompt_type] = []
            available_prompts = self.prompts[prompt_type]
            
        prompt = random.choice(available_prompts)
        
        # Add to history
        self.prompt_history[prompt_type].append(prompt)
        
        return prompt

    def get_next_prompt_for_user(self, user_id: str) -> Tuple[str, str]:
        """
        Get the next appropriate prompt for a user based on their prompt count.
        - First prompt and all odd-numbered prompts: self_awareness
        - Even-numbered prompts: connections
        
        Returns:
            Tuple containing (prompt_text, prompt_type)
        """
        # Initialize count if this is a new user
        if user_id not in self.user_prompt_counts:
            self.user_prompt_counts[user_id] = 0
            
        # Increment the count for this user
        self.user_prompt_counts[user_id] += 1
        count = self.user_prompt_counts[user_id]
        
        # Determine prompt type based on count
        # Odd numbers (including 1) get self-awareness
        # Even numbers get building-connections
        if count % 2 == 1:  # Odd number (1, 3, 5, etc.)
            prompt_type = "self_awareness"
        else:  # Even number (2, 4, 6, etc.)
            prompt_type = "connections"
            
        logger.info(f"User {user_id} prompt count: {count}, sending {prompt_type} prompt")
        
        # Get prompt of the determined type
        prompt = self.get_prompt_by_type(prompt_type)
        return prompt, prompt_type

    def create_journal_entry(self, prompt: str, response: str, prompt_type: str) -> JournalEntry:
        """Create a new journal entry."""
        return JournalEntry(
            prompt=prompt,
            response=response,
            timestamp=datetime.now().isoformat(),
            prompt_type=prompt_type
        )

    def should_send_prompt(self, user: User) -> bool:
        """
        Check if it's time to send a prompt to the user based on their preferences.
        
        Args:
            user: The user to check
            
        Returns:
            bool: True if it's time to send a prompt, False otherwise
        """
        try:
            # Always use Singapore timezone
            sg_tz = pytz.timezone('Asia/Singapore')
            current_time = datetime.now(sg_tz)
            
            return (
                current_time.weekday() == user.preferred_prompt_day and 
                current_time.hour == user.preferred_prompt_hour
            )
        except Exception as e:
            logger.error(f"Error checking prompt time for user {user.id}: {e}")
            return False