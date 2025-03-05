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
            check_interval=int(os.getenv('CHECK_INTERVAL', '60')),
            prompt_hour=int(os.getenv('PROMPT_HOUR', '9')),
            prompt_day=int(os.getenv('PROMPT_DAY', '0')),  # Monday
            max_history=int(os.getenv('MAX_HISTORY', '5')),
            timezone=SINGAPORE_TIMEZONE  # Always use Singapore timezone
        )

PROMPTS = {
    'self_awareness': [
        "🦕 Screen-Free Safari! 🧠 \n\n Spend an hour today without your phone or any screens—just like the good old prehistoric days! \n\n 🌿🦖 What did you do instead? How did it feel to step away from the digital jungle? 🌍✨"
    ],
    'connections': [
        "🦖 Fossilized Friendships Await! 🤝 \n\n Reconnect with someone you haven’t spoken to in a while—send them a message and see what happens!\n\n 🌍✨ Did it feel like unearthing a long-lost dino bond? Reflect and let your connections evolve!"
    ]
}
