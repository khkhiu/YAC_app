import os
from app import create_bot
from app.config import logger

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    try:
        bot = create_bot(token)
        logger.info("Bot started!")
        bot.run_polling()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")