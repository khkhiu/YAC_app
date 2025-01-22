# app/handlers.py
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from app.config import (
    SELF_AWARENESS, CONNECTION, GROWTH,
    CHOOSING, COMPLETING, CHALLENGES, logger
)
from app.database import Database

class ChallengeHandler:
    def __init__(self, database: Database):
        self.db = database

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = self.db.get_user_progress(user_id)
        total_challenges = progress['self_awareness_count'] + progress['connection_count']
        
        keyboard = self._build_challenge_keyboard(total_challenges)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Welcome to the Daily Challenge Bot! 🌟\n\n"
            "Choose your challenge for today:",
            reply_markup=reply_markup
        )
        
        return CHOOSING

    def _build_challenge_keyboard(self, total_challenges: int):
        keyboard = [
            [InlineKeyboardButton("Self-Awareness Challenge", callback_data=SELF_AWARENESS)],
            [InlineKeyboardButton("Connection Challenge", callback_data=CONNECTION)]
        ]
        
        if total_challenges >= 14:
            keyboard.append([InlineKeyboardButton("Growth Challenge", callback_data=GROWTH)])
            
        return keyboard

    async def select_challenge(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        challenge_type = query.data
        challenge = random.choice(CHALLENGES[challenge_type])
        
        context.user_data['current_challenge'] = {
            'type': challenge_type,
            'text': challenge
        }
        
        await query.edit_message_text(
            f"Here's your challenge:\n\n{challenge}\n\n"
            "Once you've completed it, share your reflection by replying to this message."
        )
        
        return COMPLETING

    async def complete_challenge(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        reflection = update.message.text
        challenge = context.user_data['current_challenge']
        
        try:
            self.db.update_progress(user_id, challenge['type'])
            self.db.log_completion(user_id, challenge['type'], challenge['text'], reflection)
            
            progress = self.db.get_user_progress(user_id)
            total_challenges = progress['self_awareness_count'] + progress['connection_count']
            
            response = self._build_completion_response(total_challenges)
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error completing challenge: {e}")
            await update.message.reply_text(
                "Sorry, there was an error processing your challenge completion. Please try again."
            )
            
        return ConversationHandler.END

    def _build_completion_response(self, total_challenges: int):
        response = "Thank you for sharing your reflection! 🌟\n\n"
        if total_challenges == 14:
            response += "Congratulations! You've unlocked Growth Challenges! Use /start to choose your next challenge."
        else:
            response += "Use /start to choose another challenge when you're ready."
        return response

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = self.db.get_user_progress(user_id)
        
        await update.message.reply_text(
            f"Your Progress 📊\n\n"
            f"Self-Awareness Challenges: {progress['self_awareness_count']}\n"
            f"Connection Challenges: {progress['connection_count']}\n"
            f"Growth Challenges: {progress['growth_count']}\n\n"
            f"Total Challenges: {sum(progress.values())}"
        )
