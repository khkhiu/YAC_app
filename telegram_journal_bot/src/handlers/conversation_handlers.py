"""Conversation handlers for the Telegram Journal Bot."""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
from src.services.storage_service import StorageService
from src.services.prompt_service import PromptService
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Conversation states
RESPONDING = 1

class ConversationHandlers:
    """Handlers for bot conversations."""

    def __init__(self, storage_service: StorageService, prompt_service: PromptService):
        """Initialize conversation handlers with required services."""
        self.storage = storage_service
        self.prompt_service = prompt_service

    async def send_prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a new prompt to the user and await response."""
        try:
            user_id = str(update.effective_user.id)
            user = self.storage.get_user(user_id)

            if not user:
                await update.message.reply_text(
                    "Please start the bot with /start first!"
                )
                return ConversationHandler.END

            # Get random prompt
            prompt, prompt_type = self.prompt_service.get_random_prompt()

            # Store current prompt
            user.last_prompt = {
                'text': prompt,
                'type': prompt_type,
                'timestamp': datetime.now().isoformat()
            }
            self.storage.add_user(user)

            await update.message.reply_text(
                f"🤔 Here's your reflection prompt:\n\n{prompt}\n\n"
                "Take your time to reflect and respond when you're ready. "
                "Your response will be saved in your journal."
            )
            return RESPONDING

        except Exception as e:
            logger.error(f"Error sending prompt: {e}")
            await update.message.reply_text(
                "Sorry, there was an error getting your prompt. Please try again."
            )
            return ConversationHandler.END

    async def save_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Save the user's response to their journal."""
        try:
            user_id = str(update.effective_user.id)
            user = self.storage.get_user(user_id)

            if not user or not user.last_prompt:
                await update.message.reply_text(
                    "Sorry, I couldn't find your prompt. Please use /prompt to get a new one."
                )
                return ConversationHandler.END

            # Create and save journal entry
            entry = self.prompt_service.create_journal_entry(
                prompt=user.last_prompt['text'],
                response=update.message.text,
                prompt_type=user.last_prompt['type']
            )
            user.add_response(entry)
            self.storage.add_user(user)

            await update.message.reply_text(
                "✨ Thank you for sharing! Your response has been saved.\n\n"
                "Remember, regular reflection helps us grow and understand ourselves better.\n"
                "Use /prompt when you're ready for another question."
            )

        except Exception as e:
            logger.error(f"Error saving response: {e}")
            await update.message.reply_text(
                "Sorry, there was an error saving your response. "
                "Please try using /prompt to start again."
            )

        return ConversationHandler.END
