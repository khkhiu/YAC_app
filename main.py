# bot.py
import logging
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
import os
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# States
CHOOSING, COMPLETING = range(2)

# Challenge types
SELF_AWARENESS = 'self_awareness'
CONNECTION = 'connection'
GROWTH = 'growth'

# Challenge pools
SELF_AWARENESS_CHALLENGES = [
    "Share a memory that demonstrates your resilience.",
    "Reflect on a fear you've overcome and what you learned.",
    "Write about a moment when you felt truly proud of yourself.",
    "Describe a challenge that shaped who you are today.",
    "Identify three of your strongest qualities and why.",
]

CONNECTION_CHALLENGES = [
    "Thank someone who has supported you recently.",
    "Reach out to someone you've lost touch with.",
    "Write a note of appreciation to a mentor.",
    "Share a meaningful memory with a friend.",
    "Express gratitude to someone who inspired you.",
]

GROWTH_CHALLENGES = [
    "Reflect on your personal growth this month.",
    "Identify and rewrite a limiting belief.",
    "Set three meaningful goals for the next month.",
    "Write about a lesson you learned from a mistake.",
    "Plan one step toward a long-term goal.",
]

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/challenges.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    user_id INTEGER PRIMARY KEY,
                    self_awareness_count INTEGER DEFAULT 0,
                    connection_count INTEGER DEFAULT 0,
                    growth_count INTEGER DEFAULT 0,
                    last_challenge_date TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS completed_challenges (
                    user_id INTEGER,
                    challenge_type TEXT,
                    challenge_text TEXT,
                    completion_date TEXT,
                    reflection TEXT
                )
            ''')

    def get_user_progress(self, user_id):
        cursor = self.conn.execute(
            'SELECT * FROM user_progress WHERE user_id = ?', 
            (user_id,)
        )
        result = cursor.fetchone()
        if not result:
            self.conn.execute(
                'INSERT INTO user_progress (user_id) VALUES (?)',
                (user_id,)
            )
            self.conn.commit()
            return {
                'self_awareness_count': 0,
                'connection_count': 0,
                'growth_count': 0
            }
        return {
            'self_awareness_count': result[1],
            'connection_count': result[2],
            'growth_count': result[3]
        }

    def update_progress(self, user_id, challenge_type):
        column = f'{challenge_type}_count'
        with self.conn:
            self.conn.execute(
                f'UPDATE user_progress SET {column} = {column} + 1, last_challenge_date = ? WHERE user_id = ?',
                (datetime.now().isoformat(), user_id)
            )

    def log_completion(self, user_id, challenge_type, challenge_text, reflection):
        with self.conn:
            self.conn.execute(
                'INSERT INTO completed_challenges (user_id, challenge_type, challenge_text, completion_date, reflection) VALUES (?, ?, ?, ?, ?)',
                (user_id, challenge_type, challenge_text, datetime.now().isoformat(), reflection)
            )

db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    progress = db.get_user_progress(user_id)
    total_challenges = progress['self_awareness_count'] + progress['connection_count']
    
    keyboard = []
    keyboard.append([InlineKeyboardButton("Self-Awareness Challenge", callback_data=SELF_AWARENESS)])
    keyboard.append([InlineKeyboardButton("Connection Challenge", callback_data=CONNECTION)])
    
    if total_challenges >= 14:
        keyboard.append([InlineKeyboardButton("Growth Challenge", callback_data=GROWTH)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to the Daily Challenge Bot! 🌟\n\n"
        "Choose your challenge for today:",
        reply_markup=reply_markup
    )
    
    return CHOOSING

async def select_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    challenge_type = query.data
    if challenge_type == SELF_AWARENESS:
        challenge = random.choice(SELF_AWARENESS_CHALLENGES)
    elif challenge_type == CONNECTION:
        challenge = random.choice(CONNECTION_CHALLENGES)
    else:
        challenge = random.choice(GROWTH_CHALLENGES)
    
    context.user_data['current_challenge'] = {
        'type': challenge_type,
        'text': challenge
    }
    
    await query.edit_message_text(
        f"Here's your challenge:\n\n{challenge}\n\n"
        "Once you've completed it, share your reflection by replying to this message."
    )
    
    return COMPLETING

async def complete_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    reflection = update.message.text
    challenge = context.user_data['current_challenge']
    
    db.update_progress(user_id, challenge['type'])
    db.log_completion(user_id, challenge['type'], challenge['text'], reflection)
    
    progress = db.get_user_progress(user_id)
    total_challenges = progress['self_awareness_count'] + progress['connection_count']
    
    response = "Thank you for sharing your reflection! 🌟\n\n"
    if total_challenges == 14:
        response += "Congratulations! You've unlocked Growth Challenges! Use /start to choose your next challenge."
    else:
        response += "Use /start to choose another challenge when you're ready."
    
    await update.message.reply_text(response)
    return ConversationHandler.END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    progress = db.get_user_progress(user_id)
    
    await update.message.reply_text(
        f"Your Progress 📊\n\n"
        f"Self-Awareness Challenges: {progress['self_awareness_count']}\n"
        f"Connection Challenges: {progress['connection_count']}\n"
        f"Growth Challenges: {progress['growth_count']}\n\n"
        f"Total Challenges: {sum(progress.values())}"
    )

def main():
    application = Application.builder().token(os.environ['TELEGRAM_TOKEN']).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [CallbackQueryHandler(select_challenge)],
            COMPLETING: [MessageHandler(filters.TEXT & ~filters.COMMAND, complete_challenge)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('stats', stats))

    application.run_polling()

if __name__ == '__main__':
    main()