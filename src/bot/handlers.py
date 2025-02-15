# src/bot/handlers.py

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from ..utils.logger import get_logger
from .prompts import get_random_prompt
from config.config import TELEGRAM_BOT_TOKEN

logger = get_logger(__name__)

# Dictionary to store user subscription status
subscribed_users = {}

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    subscribed_users[user_id] = True
    
    welcome_message = (
        f"Welcome {user_name} to the Self-Awareness Bot! 🌟\n\n"
        "You'll receive weekly prompts to help you reflect and build meaningful connections.\n\n"
        "Commands:\n"
        "/start - Start receiving weekly prompts\n"
        "/stop - Stop receiving prompts\n"
        "/prompt - Get an immediate prompt"
    )
    logger.info(f"New user subscribed: {user_id}")
    await update.message.reply_text(welcome_message)

async def stop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /stop command"""
    user_id = update.effective_user.id
    subscribed_users[user_id] = False
    logger.info(f"User unsubscribed: {user_id}")
    await update.message.reply_text("You've unsubscribed from weekly prompts. Send /start to subscribe again!")

async def prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /prompt command"""
    prompt = get_random_prompt()
    user_id = update.effective_user.id
    logger.info(f"Prompt requested by user: {user_id}")
    await update.message.reply_text(f"🤔 Self-Reflection Prompt:\n\n{prompt}")

def setup_handlers() -> Application:
    """Initialize and configure the bot with all handlers"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("stop", stop_handler))
    app.add_handler(CommandHandler("prompt", prompt_handler))
    
    return app

def get_subscribed_users():
    """Return the dictionary of subscribed users"""
    return subscribed_users