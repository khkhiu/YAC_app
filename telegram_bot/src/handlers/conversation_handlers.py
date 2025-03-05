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

            # Get the next prompt for this user based on their prompt count
            # (self-awareness for odd counts, connections for even counts)
            prompt, prompt_type = self.prompt_service.get_next_prompt_for_user(user_id)
            
            # Store current prompt
            user.last_prompt = {
                'text': prompt,
                'type': prompt_type,
                'timestamp': datetime.now().isoformat()
            }
            self.storage.add_user(user)
            
            # Indicate the category to the user
            category_emoji = "🧠" if prompt_type == "self_awareness" else "🤝"
            category_name = "Self-Awareness" if prompt_type == "self_awareness" else "Connections"

            await update.message.reply_text(
                f"{category_emoji} {category_name} Dig Site! \n\n{prompt}\n\n"
                "Take your time to excavate your thoughts—your reflections will be saved in your journal! 🦴✨\n\n"
                "You can use other commands like /history while thinking - "
                "just reply directly to this message when you're ready."
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
            
            # Clear the last prompt to prevent duplicate responses
            user.last_prompt = None
            
            # Save user with updated responses and cleared prompt
            self.storage.add_user(user)

            # Give feedback based on the prompt type
            if entry.prompt_type == 'self_awareness':
                feedback = (
                    "✨ Dino-mite! Your response has been safely tucked away in your journal.🦖 \n\n"
                    "Just like a pack of raptors, strong connections start with understanding ourselves!\n"
                    #"Use /prompt when you're ready for another question."
                )
            else:
                feedback = (
                    "✨ Dino-mite! Your response has been safely tucked away in your journal.🦖\n\n"
                    "Building meaningful connections with others often starts with understanding ourselves.\n"
                    "Use /prompt when you're ready for another question."
                )
                    
            await update.message.reply_text(feedback)

        except Exception as e:
            logger.error(f"Error saving response: {e}")
            await update.message.reply_text(
                "Sorry, there was an error saving your response. "
                "Please try using /prompt to start again."
            )

        return ConversationHandler.END

    async def handle_direct_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle direct text responses to scheduled prompts.
        This function processes messages outside the conversation handler flow.
        """
        try:
            user_id = str(update.effective_user.id)
            user = self.storage.get_user(user_id)

            # If no user or no last prompt, ignore - this is likely just a random message
            if not user or not user.last_prompt:
                # Log but don't respond to avoid spamming users for normal messages
                logger.debug(f"Received text from user {user_id} without an active prompt")
                return

            # Check if the last prompt timestamp is too old (e.g., more than 24 hours)
            last_prompt_time = datetime.fromisoformat(user.last_prompt['timestamp'])
            current_time = datetime.now()
            time_difference = (current_time - last_prompt_time).total_seconds() / 3600  # hours

            # If the prompt is older than 24 hours, we might not want to save it as a response
            # to that prompt, assuming it's an unrelated message
            if time_difference > 24:
                logger.debug(f"Ignoring response for old prompt (from {time_difference:.1f} hours ago)")
                return

            # Create and save journal entry
            entry = self.prompt_service.create_journal_entry(
                prompt=user.last_prompt['text'],
                response=update.message.text,
                prompt_type=user.last_prompt['type']
            )
            user.add_response(entry)
            self.storage.add_user(user)
            logger.info(f"Saved direct response from user {user_id}")

            # Give feedback based on the prompt type
            if user.last_prompt['type'] == 'self_awareness':
                feedback = (
                    "✨ Thank you for your thoughtful reflection! Your response has been saved.\n\n"
                    "Self-awareness is a journey that takes time and patience.\n"
                    "Your next prompt will be delivered according to your scheduled preference."
                )
            else:
                feedback = (
                    "✨ Thank you for sharing! Your response has been saved.\n\n"
                    "Building meaningful connections with others often starts with understanding ourselves.\n"
                    "Your next prompt will be delivered according to your scheduled preference."
                )
                
            # Clear the last prompt to prevent duplicate responses
            user.last_prompt = None
            self.storage.add_user(user)
                
            await update.message.reply_text(feedback)

        except Exception as e:
            logger.error(f"Error saving direct response: {e}")
            await update.message.reply_text(
                "Sorry, there was an error saving your response. "
                "Please try using /prompt to start again."
            )