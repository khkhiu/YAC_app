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
from src.utils.constants import DAYS_OF_WEEK
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

        # Dictionary to track user-specific job IDs
        self.user_jobs = {}
        
        # Initialize handlers with scheduling callback
        self.command_handlers = CommandHandlers(
            self.storage_service,
            self.prompt_service,
            config.max_history,
            schedule_callback=self.schedule_user_prompt  # Pass the scheduling function
        )
        
        self.conversation_handlers = ConversationHandlers(
            self.storage_service,
            self.prompt_service
        )
        
    async def send_prompt_to_user(self, context):
        """Send a prompt to a specific user."""
        job = context.job
        user_id = job.data  # User ID stored in job.data
        
        try:
            user = self.storage_service.get_user(user_id)
            if not user:
                logger.error(f"User {user_id} not found for scheduled prompt")
                return
                
            # Get the appropriate prompt for this user based on their count
            prompt, prompt_type = self.prompt_service.get_next_prompt_for_user(user_id)
            
            # Save this prompt as the user's last prompt so they can respond to it
            user.last_prompt = {
                'text': prompt,
                'type': prompt_type,
                'timestamp': datetime.now().isoformat()
            }
            self.storage_service.add_user(user)
            
            # Indicate the category to the user
            category_emoji = "🧠" if prompt_type == "self_awareness" else "🤝"
            category_name = "Self-Awareness" if prompt_type == "self_awareness" else "Connections"
            
            await context.bot.send_message(
                chat_id=user_id,
                text=f"🌟 Weekly Reflection Time! {category_emoji} {category_name}\n\n{prompt}\n\n"
                "Take a moment to pause and reflect on this question. Simply reply to this message with your thoughts."
            )
            logger.info(f"Sent scheduled {prompt_type} prompt to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error sending scheduled prompt to user {user_id}: {e}")

    def schedule_user_prompt(self, application, user_id):
        """Schedule a prompt job for a specific user based on their preferences."""
        try:
            user = self.storage_service.get_user(user_id)
            if not user:
                logger.error(f"Cannot schedule prompt for non-existent user {user_id}")
                return
                
            # Cancel existing job for this user if it exists
            self.cancel_user_prompt_job(application, user_id)
            
            # Get Singapore timezone
            sg_tz = pytz.timezone('Asia/Singapore')
            
            # Create time object for the user's preferred hour
            prompt_time = time(hour=user.preferred_prompt_hour, minute=0)
            
            # Schedule the job to run weekly on the user's preferred day and time
            job = application.job_queue.run_daily(
                callback=self.send_prompt_to_user,
                time=prompt_time,
                days=(user.preferred_prompt_day,),
                data=user_id,  # Pass the user_id as job data
                name=f"prompt_job_{user_id}",
                timezone=sg_tz
            )
            
            # Save the job for later reference
            self.user_jobs[user_id] = job
            
            day_name = DAYS_OF_WEEK[user.preferred_prompt_day]
            hour_12 = user.preferred_prompt_hour % 12 or 12
            am_pm = "AM" if user.preferred_prompt_hour < 12 else "PM"
            
            logger.info(f"Scheduled prompt for user {user_id} on {day_name} at {hour_12} {am_pm} (SGT)")
            
        except Exception as e:
            logger.error(f"Error scheduling prompt for user {user_id}: {e}")

    def cancel_user_prompt_job(self, application, user_id):
        """Cancel an existing prompt job for a user."""
        if user_id in self.user_jobs:
            job = self.user_jobs[user_id]
            job.schedule_removal()
            logger.info(f"Removed existing prompt schedule for user {user_id}")
            del self.user_jobs[user_id]

    def setup_user_prompt_schedules(self, application):
        """Set up prompt schedules for all existing users."""
        users = self.storage_service.get_all_users()
        for user_id in users:
            self.schedule_user_prompt(application, user_id)
            
        logger.info(f"Set up prompt schedules for {len(users)} users")

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
        
        # Add a general message handler to capture responses to scheduled prompts
        # This needs to be added AFTER the ConversationHandler to avoid conflicts
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.conversation_handlers.handle_direct_response
            )
        )
        
        # Add error handler
        application.add_error_handler(self.command_handlers.handle_error)

    def run(self):
        """Run the bot."""
        try:
            # Create application
            application = Application.builder().token(self.config.bot_token).build()

            # Setup handlers
            self.setup_handlers(application)
            
            # Set up prompt schedules for all existing users
            self.setup_user_prompt_schedules(application)

            # Start polling
            logger.info("Starting bot...")
            application.run_polling()

        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise