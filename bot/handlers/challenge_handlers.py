# bot/handlers/challenge_handlers.py
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database.db import Database
from database.models import Response
from utils.constants import CHALLENGES

async def daily_challenge_handler(update: Update, context: CallbackContext):
    category = random.choice(list(CHALLENGES.keys()))
    prompt = random.choice(CHALLENGES[category])
    
    keyboard = [
        [InlineKeyboardButton("Respond to Challenge", callback_data=f"respond_{category}")],
        [InlineKeyboardButton("See Community Responses", callback_data="view_responses")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Today's {category.replace('_', ' ').title()} Challenge:\n\n{prompt}",
        reply_markup=reply_markup
    )

async def handle_response(update: Update, context: CallbackContext, db: Database):
    if "current_challenge" not in context.user_data:
        return
    
    user_id = update.effective_user.id
    response_text = update.message.text
    challenge = context.user_data["current_challenge"]
    
    response = Response(
        user_id,
        challenge["category"],
        challenge["prompt"],
        response_text
    )
    
    db.responses.insert_one(response.data)
    
    keyboard = [
        [
            InlineKeyboardButton("Share Anonymously", callback_data="share_anon"),
            InlineKeyboardButton("Share with Username", callback_data="share_username")
        ],
        [InlineKeyboardButton("Keep Private", callback_data="share_private")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Your response has been saved! Would you like to share it with the community?",
        reply_markup=reply_markup
    )
