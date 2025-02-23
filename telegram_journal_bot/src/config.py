"""Configuration management for the Telegram Journal Bot."""

import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Dict, List

# Hard-coded timezone for Singapore
SINGAPORE_TIMEZONE = "Asia/Singapore"

@dataclass
class Config:
    """Configuration container for the bot."""
    bot_token: str
    users_file: str
    check_interval: int
    prompt_hour: int
    prompt_day: int
    max_history: int
    timezone: str = SINGAPORE_TIMEZONE  # Always set to Singapore timezone

    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from environment variables."""
        load_dotenv()
        
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            raise ValueError("BOT_TOKEN environment variable is required")
            
        return cls(
            bot_token=bot_token,
            users_file=os.getenv('USERS_FILE', 'data/users.json'),
            check_interval=int(os.getenv('CHECK_INTERVAL', '3600')),
            prompt_hour=int(os.getenv('PROMPT_HOUR', '9')),
            prompt_day=int(os.getenv('PROMPT_DAY', '0')),  # Monday
            max_history=int(os.getenv('MAX_HISTORY', '5')),
            timezone=SINGAPORE_TIMEZONE  # Always use Singapore timezone
        )

PROMPTS = {
    'self_awareness': [
        "What emotions have you experienced most frequently this week? What triggered them?",
        "Describe a situation where you felt truly authentic. What made it special?",
        "What personal values were challenged or reinforced this week?",
        "What patterns have you noticed in your reactions to stress lately?",
        "What's one thing you'd like to change about how you handle difficult conversations?",
        "How have your priorities shifted in the past few months?",
        "What recent experience has taught you something new about yourself?"
    ],
    'connections': [
        "Which relationship in your life has grown the most recently? How?",
        "What conversation this week made you feel most understood?",
        "How have you shown appreciation to others this week?",
        "What boundaries have you set or need to set in your relationships?",
        "Who would you like to reconnect with, and what's holding you back?",
        "How has someone surprised you positively this week?",
        "What qualities do you admire most in your closest friends?"
    ]
}
