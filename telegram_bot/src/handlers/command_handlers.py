"""Command handlers for the Telegram Journal Bot."""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import pytz
from datetime import datetime
from typing import Optional, Callable
from src.models.user import User
from src.services.storage_service import StorageService
from src.services.prompt_service import PromptService
from src.utils.logger import get_logger
from src.utils.constants import DAYS_OF_WEEK

logger = get_logger(__name__)

class CommandHandlers:
    """Handlers for bot commands."""
    
    def __init__(
        self,
        storage_service: StorageService,
        prompt_service: PromptService,
        max_history: int,
        schedule_callback: Optional[Callable] = None
    ):
        """
        Initialize command handlers with required services.
        
        Args:
            storage_service: Service for managing user data
            prompt_service: Service for managing prompts
            max_history: Maximum number of history entries to show
            schedule_callback: Optional callback to reschedule prompts when settings change
        """
        self.storage = storage_service
        self.prompt_service = prompt_service
        self.max_history = max_history
        self.schedule_callback = schedule_callback  # Callback for rescheduling prompts

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /start command.
        
        Creates a new user if they don't exist and sends welcome message.
        """
        if not update.effective_user:
            logger.error("No effective user found in update")
            return

        user_id = str(update.effective_user.id)
        new_user = False
        
        if not self.storage.get_user(user_id):
            user = User(id=user_id)
            self.storage.add_user(user)
            logger.info(f"Created new user with ID: {user_id}")
            new_user = True

        welcome_message = (
            "🦕 Welcome to ThyKnow! 🦖\n\n"
            "Just like dinos ruled the Earth, you’re about to rule self-awareness & connections! 🌍💡\n\n"
            "I’ll send you weekly prompts to help you reflect on:\n"
            "• Self-awareness 🤔(Because knowing yourself is a Jurassic-level skill!)\n"
            "• Building meaningful connections 🤝 (Because even T-Rex needed a buddy!)\n\n"
            "Commands:\n"
            "/prompt - Get a new reflection prompt\n"
            "/history - View your recent journal entries\n"
            "/timezone - Check prompt timings\n"
            "/set_day - Set your preferred day for prompts\n"
            "/set_time - Set your preferred time for prompts\n"
            "/settings - View your current prompt settings\n"
            "/ai_assist - Get a motivational friendship message\n"
            "/help - shows all available commands\n\n"
            "Let's start your journaling journey! Use /prompt to get your first question."
        )
        await update.message.reply_text(welcome_message)
        
        # Schedule prompts for new users
        if new_user and self.schedule_callback:
            self.schedule_callback(context.application, user_id)

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
                history_text += f"\nA: {entry.response}\n\n"

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
            "This bot operates on Singapore timezone (GMT+8) for all users.\n"
            "Use /set_day and /set_time to customize when you receive prompts."
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
            "• /set_day - Set your preferred day for weekly prompts\n"
            "• /set_time - Set your preferred hour for prompts\n"
            "• /settings - View your current prompt settings\n"
            "• /ai_assist - Get a dinosaur-themed assistance on prompts\n"
            "• /help - Show this help message\n\n"
            "📝 How to use:\n"
            "1. Use /start to begin\n"
            "2. Get prompts with /prompt\n"
            "3. Set your preferred day with /set_day\n"
            "4. Set your preferred time with /set_time\n"
            "5. View your entries with /history\n\n"
            "✨ The bot will send you weekly prompts according to your preferred settings in Singapore timezone."
        )
        await update.message.reply_text(help_text)

    async def set_day(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /set_day command to set preferred day for prompts."""
        if not update.effective_user:
            logger.error("No effective user found in update")
            return

        user_id = str(update.effective_user.id)
        user = self.storage.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please start the bot with /start first!")
            return

        # Create keyboard with days of the week
        keyboard = []
        for day_num, day_name in DAYS_OF_WEEK.items():
            button = InlineKeyboardButton(
                text=f"{'✓ ' if user.preferred_prompt_day == day_num else ''}{day_name}",
                callback_data=f"day_{day_num}"
            )
            keyboard.append([button])

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Please select the day you'd like to receive weekly prompts (in Singapore time):",
            reply_markup=reply_markup
        )

    async def set_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /set_time command to set preferred hour for prompts."""
        if not update.effective_user:
            logger.error("No effective user found in update")
            return

        user_id = str(update.effective_user.id)
        user = self.storage.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please start the bot with /start first!")
            return

        # Create keyboard with hours (0-23)
        keyboard = []
        row = []
        for hour in range(24):
            # Format as 12-hour AM/PM time
            hour_display = f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}"
            button = InlineKeyboardButton(
                text=f"{'✓ ' if user.preferred_prompt_hour == hour else ''}{hour_display}",
                callback_data=f"hour_{hour}"
            )
            row.append(button)
            
            # 4 buttons per row
            if len(row) == 4:
                keyboard.append(row)
                row = []
                
        # Add any remaining buttons
        if row:
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Please select the hour you'd like to receive prompts (in Singapore time):",
            reply_markup=reply_markup
        )

    async def settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /settings command to view current prompt settings."""
        if not update.effective_user:
            logger.error("No effective user found in update")
            return

        user_id = str(update.effective_user.id)
        user = self.storage.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please start the bot with /start first!")
            return

        # Format the current settings
        day_name = DAYS_OF_WEEK[user.preferred_prompt_day]
        hour_12 = user.preferred_prompt_hour % 12
        if hour_12 == 0:
            hour_12 = 12
        am_pm = "AM" if user.preferred_prompt_hour < 12 else "PM"
        
        settings_text = (
            "🕒 Your Current Settings:\n\n"
            f"• Prompt day: {day_name}\n"
            f"• Prompt time: {hour_12} {am_pm} (Singapore time)\n\n"
            "You can change these settings with /set_day and /set_time commands."
        )
        
        await update.message.reply_text(settings_text)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline keyboards."""
        query = update.callback_query
        await query.answer()  # Answer the callback query
        
        # Get user
        user_id = str(update.effective_user.id)
        user = self.storage.get_user(user_id)
        
        if not user:
            await query.message.reply_text("Please start the bot with /start first!")
            return
            
        callback_data = query.data
        settings_changed = False
        
        # Handle day selection
        if callback_data.startswith("day_"):
            try:
                day = int(callback_data.split("_")[1])
                if user.preferred_prompt_day != day:
                    user.preferred_prompt_day = day
                    self.storage.add_user(user)
                    settings_changed = True
                
                day_name = DAYS_OF_WEEK[day]
                await query.message.edit_text(f"✅ Your prompt day has been set to {day_name}!")
                logger.info(f"User {user_id} set preferred day to {day} ({day_name})")
                
            except Exception as e:
                logger.error(f"Error setting day preference: {e}")
                await query.message.edit_text("Sorry, there was an error setting your preference.")
        
        # Handle hour selection
        elif callback_data.startswith("hour_"):
            try:
                hour = int(callback_data.split("_")[1])
                if user.preferred_prompt_hour != hour:
                    user.preferred_prompt_hour = hour
                    self.storage.add_user(user)
                    settings_changed = True
                
                # Format for 12-hour display
                hour_12 = hour % 12
                if hour_12 == 0:
                    hour_12 = 12
                am_pm = "AM" if hour < 12 else "PM"
                
                await query.message.edit_text(f"✅ Your prompt time has been set to {hour_12} {am_pm}!")
                logger.info(f"User {user_id} set preferred hour to {hour}")
                
            except Exception as e:
                logger.error(f"Error setting time preference: {e}")
                await query.message.edit_text("Sorry, there was an error setting your preference.")
        
        # Reschedule prompts if settings were changed
        if settings_changed and self.schedule_callback:
            self.schedule_callback(context.application, user_id)
            logger.info(f"Rescheduled prompts for user {user_id} after settings change")

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