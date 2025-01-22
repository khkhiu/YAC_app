# app/bot.py
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from app.config import logger, CHOOSING, COMPLETING  # Added import for constants
from app.database import Database
from app.handlers import ChallengeHandler

def create_bot(token: str) -> Application:
    if not token:
        raise ValueError("No TELEGRAM_TOKEN provided!")

    application = Application.builder().token(token).build()
    
    # Initialize database and handlers
    db = Database()
    handler = ChallengeHandler(db)

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handler.start)],
        states={
            CHOOSING: [CallbackQueryHandler(handler.select_challenge)],
            COMPLETING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.complete_challenge)]
        },
        fallbacks=[CommandHandler('start', handler.start)]
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('stats', handler.stats))

    return application