# bot/handlers/user_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database.db import Database
from database.models import User

async def start_handler(update: Update, context: CallbackContext, db: Database):
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    user = User(user_id, username)
    db.users.update_one(
        {"user_id": user_id},
        {"$set": user.data},
        upsert=True
    )
    
    welcome_text = (
        "Welcome to the Daily Challenge Bot! 🎯\n\n"
        "Here you can participate in daily challenges to promote personal growth "
        "and connect with like-minded individuals.\n\n"
        "Would you like to join our community group?"
    )
    
    keyboard = [
        [InlineKeyboardButton("Join Community Group", url=f"https://t.me/{context.bot_data['group_chat_id']}")],
        [InlineKeyboardButton("Start Today's Challenge", callback_data="respond_today")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
