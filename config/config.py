# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

# Scheduling Configuration
WEEKLY_INTERVAL = 7 * 24 * 60 * 60  # 7 days in seconds

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'bot.log'

# Feature Flags
ENABLE_CATEGORIES = False  # For future feature of categorized prompts
ENABLE_ANALYTICS = False   # For future analytics feature

# Application Metadata
BOT_VERSION = '1.0.0'
BOT_NAME = 'Self-Awareness Bot'
BOT_DESCRIPTION = 'A Telegram bot for personal growth and self-reflection'

# Message Templates
MESSAGES = {
    'welcome': "Welcome to the Self-Awareness Bot! 🌟\n\nYou'll receive weekly prompts to help you reflect and build meaningful connections.",
    'prompt_prefix': "🤔 Self-Reflection Prompt:\n\n",
    'weekly_prefix': "🌟 Your Weekly Self-Reflection Prompt:\n\n",
    'unsubscribe': "You've unsubscribed from weekly prompts. Send /start to subscribe again!",
}