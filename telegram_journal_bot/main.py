"""Main entry point for the Telegram Journal Bot."""

from src.config import Config
from src.bot import JournalBot
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Initialize and run the bot."""
    try:
        # Load configuration
        config = Config.load()

        # Create and run bot
        bot = JournalBot(config)
        bot.run()

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
