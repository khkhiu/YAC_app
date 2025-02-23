"""Main bot class implementing the Telegram Journal Bot."""

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from src.config import Config, PROMPTS
from src.services.storage_service import StorageService
from src.services.prompt_service import PromptService
from src.handlers.command_handlers import CommandHandlers
from src.handlers.conversation_handlers import ConversationHandlers, RESPONDING
from src.utils.logger import get_logger

logger = get_logger(__name__)

class JournalBot:
    """Main bot class that sets up and runs the Telegram bot."""

    def __init__(self, config: Config):
        """Initialize the bot with configuration."""
        self.config = config

        # Initialize services
        self.storage_service = StorageService(config.users_file)
        self.prompt_service = PromptService(PROMPTS)

        # Initialize handlers
        self.command_handlers = CommandHandlers(
            self.storage_service,
            self.prompt_service,
            config.max_history
        )
        self.conversation_handlers = ConversationHandlers(
            self.storage_service,
            self.prompt_service
        )

    async def weekly_prompt_job(self, context):
        """Job to send weekly prompts to all users."""
        try:
            for user in self.storage_service.get_all_users().values():
                if self.prompt_service.should_send_prompt(
                    user,
                    self.config.prompt_hour,
                    self.config.prompt_day
                ):
                    prompt, prompt_type = self.prompt_service.get_random_prompt()
                    await context.bot.send_message(
                        chat_id=user.id,
                        text=f"🌟 Weekly Reflection Time!\n\n{prompt}\n\n"
                        "Take a moment to pause and reflect on this question."
                    )
        except Exception as e:
            logger.error(f"Error in weekly prompt job: {e}")

    def setup_handlers(self, application: Application):
        """Set up all command and conversation handlers."""
        # Create conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('prompt', self.conversation_handlers.send_prompt)],
            states={
                RESPONDING: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.conversation_handlers.save_response
                    )
                ]
            },
            fallbacks=[],
        )

        # Add handlers
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler('start', self.command_handlers.start))
        application.add_handler(CommandHandler('history', self.command_handlers.view_history))
        application.add_handler(CommandHandler('timezone', self.command_handlers.set_timezone))
        application.add_handler(CommandHandler('help', self.command_handlers.help))

    def run(self):
        """Run the bot."""
        try:
            # Create application
            application = Application.builder().token(self.config.bot_token).build()

            # Setup handlers
            self.setup_handlers(application)

            # Setup weekly job
            job_queue = application.job_queue
            job_queue.run_repeating(
                self.weekly_prompt_job,
                interval=self.config.check_interval
            )

            # Start polling
            logger.info("Starting bot...")
            application.run_polling()

        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise
