"""Constants used throughout the Telegram Journal Bot."""

from enum import Enum

class LogLevel(Enum):
    """Log levels for the application."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class TimeFormat(Enum):
    """Time formats used in the application."""
    TIMESTAMP = "%Y-%m-%d %H:%M:%S"
    DATE = "%Y-%m-%d"
    TIME = "%H:%M:%S"
    DATETIME = "%Y-%m-%d %I:%M %p"

# Logging constants
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "bot.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 5

# Bot response constants
MAX_MESSAGE_LENGTH = 4096  # Telegram's max message length
DEFAULT_TIMEZONE = "UTC"
WEEKLY_PROMPT_DAY = 0  # Monday
WEEKLY_PROMPT_HOUR = 9  # 9 AM

# Storage constants
DEFAULT_USERS_FILE = "data/users.json"
DEFAULT_MAX_HISTORY = 5

# Error messages
ERROR_MESSAGES = {
    "no_user": "Please start the bot with /start first!",
    "invalid_timezone": "Invalid timezone. Please check the timezone list and try again.",
    "general_error": "Sorry, something went wrong. Please try again later.",
    "no_history": "You haven't made any journal entries yet. Use /prompt to start!",
    "save_error": "Error saving your response. Please try again.",
}

# Success messages
SUCCESS_MESSAGES = {
    "response_saved": "✨ Thank you for sharing! Your response has been saved.",
    "timezone_set": "✅ Your timezone has been set to {}!",
    "prompt_sent": "🤔 Here's your reflection prompt:",
}

# Command descriptions
COMMAND_DESCRIPTIONS = {
    "start": "Initialize the bot and get started",
    "prompt": "Get a new reflection prompt",
    "history": "View your recent journal entries",
    "help": "Show available commands and usage",
}
