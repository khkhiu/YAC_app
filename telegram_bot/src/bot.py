"""Main bot class implementing the Telegram Journal Bot."""

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from src.config import Config, PROMPTS
from src.services.storage_service import StorageService
from src.services.prompt_service import PromptService
from src.handlers.command_handlers import CommandHandlers
from src.handlers.conversation_handlers import ConversationHandlers, RESPONDING
from src.utils.logger import get_logger
import pytz
from datetime import datetime, time

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
        
        # Keep track of prompt types to alternate between them
        self.last_prompt_type = None

    async def weekly_prompt_job(self, context):
        """Job to send weekly prompts to all users according to their preferences."""
        try:
            # Get Singapore timezone
            sg_tz = pytz.timezone('Asia/Singapore')
            current_time = datetime.now(sg_tz)
            current_day = current_time.weekday()
            current_hour = current_time.hour
            
            logger.info(f"Running prompt check job at SG time: day={current_day}, hour={current_hour}")
            
            # Get all users
            users = self.storage.get_all_users()
            prompts_sent = 0
            
            for user in users.values():
                try:
                    # Check if it's time to send a prompt to this user based on their preferences
                    if user.preferred_prompt_day == current_day and user.preferred_prompt_hour == current_hour:
                        # Get the appropriate prompt for this user based on their count
                        prompt, prompt_type = self.prompt_service.get_next_prompt_for_user(user.id)
                        
                        # Indicate the category to the user
                        category_emoji = "🧠" if prompt_type == "self_awareness" else "🤝"
                        category_name = "Self-Awareness" if prompt_type == "self_awareness" else "Connections"
                        
                        await context.bot.send_message(
                            chat_id=user.id,
                            text=f"🌟 Weekly Reflection Time! {category_emoji} {category_name}\n\n{prompt}\n\n"
                            "Take a moment to pause and reflect on this question."
                        )
                        logger.info(f"Sent {prompt_type} prompt to user {user.id}")
                        prompts_sent += 1
                except Exception as e:
                    logger.error(f"Error sending prompt to user {user.id}: {e}")
            
            if prompts_sent > 0:
                logger.info(f"Sent prompts to {prompts_sent} users")
            
        except Exception as e:
            logger.error(f"Error in weekly prompt job: {e}")

    def setup_handlers(self, application: Application):
        """Set up all command and conversation handlers."""
        # Create conversation handler with fallbacks to other commands
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
            fallbacks=[
                CommandHandler('start', self.command_handlers.start),
                CommandHandler('history', self.command_handlers.view_history),
                CommandHandler('timezone', self.command_handlers.set_timezone),
                CommandHandler('help', self.command_handlers.help),
                CommandHandler('prompt', self.conversation_handlers.send_prompt)
            ],
        )

        # Add handlers
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler('start', self.command_handlers.start))
        application.add_handler(CommandHandler('history', self.command_handlers.view_history))
        application.add_handler(CommandHandler('timezone', self.command_handlers.set_timezone))
        application.add_handler(CommandHandler('help', self.command_handlers.help))
        
        # Add new command handlers for settings
        application.add_handler(CommandHandler('set_day', self.command_handlers.set_day))
        application.add_handler(CommandHandler('set_time', self.command_handlers.set_time))
        application.add_handler(CommandHandler('settings', self.command_handlers.settings))
        
        # Add callback query handler for inline keyboards
        application.add_handler(CallbackQueryHandler(self.command_handlers.handle_callback))
        
        # Add error handler
        application.add_error_handler(self.command_handlers.handle_error)

    def run(self):
        """Run the bot."""
        try:
            # Create application
            application = Application.builder().token(self.config.bot_token).build()

            # Setup handlers
            self.setup_handlers(application)

            # Set up the Singapore timezone for the job
            sg_tz = pytz.timezone('Asia/Singapore')
            
            # Setup a job that checks more frequently to handle user-specific times
            job_queue = application.job_queue
            
            # Run job every hour to check if it's time to send prompts to any users
            job_queue.run_repeating(
                self.weekly_prompt_job,
                interval=3600,  # Check every hour
                first=1  # Start 1 second after bot startup
            )
            
            logger.info(f"Scheduled prompt check job every hour")

            # Start polling
            logger.info("Starting bot...")
            application.run_polling()

        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise