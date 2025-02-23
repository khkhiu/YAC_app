"""Command handlers for the Telegram Journal Bot."""

from telegram import Update
from telegram.ext import ContextTypes
import pytz
from datetime import datetime
from typing import Optional
from src.models.user import User
from src.services.storage_service import StorageService
from src.services.prompt_service import PromptService
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CommandHandlers:
    """Handlers for bot commands."""
    
    def __init__(
        self,
        storage_service: StorageService,
        prompt_service: PromptService,
        max_history: int
    ):
        """
        Initialize command handlers with required services.
        
        Args:
            storage_service: Service for managing user data
            prompt_service: Service for managing prompts
            max_history: Maximum number of history entries to show
        """
        self.storage = storage_service
        self.prompt_service = prompt_service
        self.max_history = max_history

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /start command.
        
        Creates a new user if they don't exist and sends welcome message.
        """
        if not update.effective_user:
            logger.error("No effective user found in update")
            return

        user_id = str(update.effective_user.id)
        
        if not self.storage.get_user(user_id):
            user = User(id=user_id)
            self.storage.add_user(user)
            logger.info(f"Created new user with ID: {user_id}")

        welcome_message = (
            "Welcome to your personal journaling companion! 🌟\n\n"
            "I'll send you weekly prompts to help you reflect on:\n"
            "• Self-awareness 🤔\n"
            "• Building meaningful connections 🤝\n\n"
            "Commands:\n"
            "/prompt - Get a new reflection prompt\n"
            "/history - View your recent journal entries\n"
            "/timezone - Check prompt timings\n"
            "/help - shows all available commands\n\n"
            "Let's start your journaling journey! Use /prompt to get your first question."
        )
        await update.message.reply_text(welcome_message)

    async def view_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /history command.
        
        Shows the user their recent journal entries.
        """
        if not update.effective_user:
            logger.error("No effective user found in update")
            return

        user_id = str(update.effective_user.id)
        user = self.storage.get_user(user_id)
        
        if not user:
            await update.message.reply_text(
                "Please start the bot with /start first!"
            )
            return
        
        if not user.responses:
            await update.message.reply_text(
                "You haven't made any journal entries yet. Use /prompt to start!"
            )
            return

        try:
            recent_entries = user.get_recent_entries(self.max_history)
            history_text = "📖 Your Recent Journal Entries:\n\n"
            
            for entry in recent_entries:
                date = datetime.fromisoformat(entry.timestamp).strftime('%Y-%m-%d %H:%M')
                history_text += f"📅 {date}\n"
                history_text += f"Q: {entry.prompt}\n"
                history_text += f"A: {entry.response}\n\n"

            # Split message if it's too long
            if len(history_text) > 4000:
                chunks = [history_text[i:i+4000] for i in range(0, len(history_text), 4000)]
                for chunk in chunks:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(history_text)

        except Exception as e:
            logger.error(f"Error displaying history for user {user_id}: {e}")
            await update.message.reply_text(
                "Sorry, there was an error retrieving your history. Please try again."
            )

    async def set_timezone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /timezone command.
        
        Informs users that timezone is fixed to Singapore time.
        """
        await update.message.reply_text(
            "This bot operates on Singapore timezone (Asia/Singapore) for all users.\n"
            "Weekly prompts will be sent according to Singapore time."
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /help command.
        
        Shows available commands and their usage.
        """
        help_text = (
            "🤖 Available Commands:\n\n"
            "• /start - Initialize the bot and get started\n"
            "• /prompt - Get a new reflection prompt\n"
            "• /history - View your recent journal entries\n"
            "• /help - Show this help message\n\n"
            "📝 How to use:\n"
            "1. Use /start to begin\n"
            "2. Get prompts with /prompt\n"
            "3. View your entries with /history\n\n"
            "✨ The bot will also send you weekly prompts "
            "every Monday at 9 AM in your timezone."
        )
        await update.message.reply_text(help_text)

    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        General error handler for all commands.
        
        Logs errors and sends a user-friendly message.
        """
        logger.error(f"Update {update} caused error {context.error}")
        error_message = (
            "Sorry, something went wrong while processing your request. "
            "Please try again later or use /help for available commands."
        )
        if update.effective_message:
            await update.effective_message.reply_text(error_message)