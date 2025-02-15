# src/bot/scheduler.py

import asyncio
from telegram.ext import Application
from ..utils.logger import get_logger
from .prompts import get_random_prompt
from .handlers import get_subscribed_users
from config.config import WEEKLY_INTERVAL

logger = get_logger(__name__)

async def send_weekly_prompts(app: Application):
    """
    Coroutine to send weekly prompts to all subscribed users
    """
    while True:
        subscribed_users = get_subscribed_users()
        
        for user_id, is_subscribed in subscribed_users.items():
            if is_subscribed:
                try:
                    prompt = get_random_prompt()
                    await app.bot.send_message(
                        chat_id=user_id,
                        text=f"🌟 Your Weekly Self-Reflection Prompt:\n\n{prompt}"
                    )
                    logger.info(f"Weekly prompt sent to user: {user_id}")
                except Exception as e:
                    logger.error(f"Failed to send prompt to user {user_id}: {str(e)}")
        
        # Wait for the next interval
        await asyncio.sleep(WEEKLY_INTERVAL)

def start_scheduler(app: Application):
    """
    Initialize the scheduler for sending weekly prompts
    """
    asyncio.create_task(send_weekly_prompts(app))
    logger.info("Weekly prompt scheduler started")