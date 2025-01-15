# bot/challenge_bot.py
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from database.db import Database
from bot.handlers import (
    user_handlers,
    challenge_handlers,
    community_handlers,
    stats_handlers
)

class ChallengeBot:
    def __init__(self, token: str, group_chat_id: str):
        self.application = Application.builder().token(token).build()
        self.db = Database()
        self.group_chat_id = group_chat_id
        
        # Store group_chat_id in bot_data for access in handlers
        self.application.bot_data['group_chat_id'] = group_chat_id
        
        self.register_handlers()

    def register_handlers(self):
        """Register all command and message handlers"""
        # User handlers
        self.application.add_handler(
            CommandHandler("start", lambda update, context: 
                         user_handlers.start_handler(update, context, self.db))
        )
        
        # Challenge handlers
        self.application.add_handler(
            CommandHandler("today_challenge", challenge_handlers.daily_challenge_handler)
        )
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lambda update, context: challenge_handlers.handle_response(update, context, self.db)
            )
        )
        
        # Stats handlers
        self.application.add_handler(
            CommandHandler("journal", lambda update, context:
                         stats_handlers.show_journal(update, context, self.db))
        )
        self.application.add_handler(
            CommandHandler("stats", lambda update, context:
                         stats_handlers.show_stats(update, context, self.db))
        )
        
        # Add other handlers for community features, reactions, etc.

    async def start(self):
        """Start the bot"""
        await self.application.initialize()
        await self.application.start()
        await self.application.run_polling()

    async def stop(self):
        """Stop the bot and cleanup"""
        await self.application.stop()
        self.db.close()