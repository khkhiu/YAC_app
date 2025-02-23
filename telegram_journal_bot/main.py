from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import random
import asyncio
import logging
import json
import pytz

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for conversation handler
RESPONDING = 1

class JournalBot:
    def __init__(self, token):
        self.token = token
        self.users = self.load_users()
        self.prompts = {
            'self_awareness': [
                "What emotions have you experienced most frequently this week? What triggered them?",
                "Describe a situation where you felt truly authentic. What made it special?",
                "What personal values were challenged or reinforced this week?",
                "What patterns have you noticed in your reactions to stress lately?",
                "What's one thing you'd like to change about how you handle difficult conversations?",
                "How have your priorities shifted in the past few months?",
                "What recent experience has taught you something new about yourself?"
            ],
            'connections': [
                "Which relationship in your life has grown the most recently? How?",
                "What conversation this week made you feel most understood?",
                "How have you shown appreciation to others this week?",
                "What boundaries have you set or need to set in your relationships?",
                "Who would you like to reconnect with, and what's holding you back?",
                "How has someone surprised you positively this week?",
                "What qualities do you admire most in your closest friends?"
            ]
        }

    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    async def start(self, update, context):
        user_id = str(update.effective_user.id)
        if user_id not in self.users:
            self.users[user_id] = {
                'last_prompt': None,
                'timezone': 'UTC',
                'responses': []
            }
            self.save_users()

        welcome_message = (
            "Welcome to your personal journaling companion! 🌟\n\n"
            "I'll send you weekly prompts to help you reflect on:\n"
            "• Self-awareness 🤔\n"
            "• Building meaningful connections 🤝\n\n"
            "Commands:\n"
            "/prompt - Get a new reflection prompt\n"
            "/history - View your recent journal entries\n"
            "/settz - Set your timezone\n\n"
            "Let's start your journaling journey! Use /prompt to get your first question."
        )
        await update.message.reply_text(welcome_message)

    async def send_prompt(self, update, context):
        user_id = str(update.effective_user.id)
        prompt_type = random.choice(['self_awareness', 'connections'])
        prompt = random.choice(self.prompts[prompt_type])
        
        self.users[user_id]['last_prompt'] = {
            'text': prompt,
            'timestamp': datetime.now().isoformat(),
            'type': prompt_type
        }
        self.save_users()

        await update.message.reply_text(
            f"🤔 Here's your reflection prompt:\n\n{prompt}\n\n"
            "Take your time to reflect and respond when you're ready. "
            "Your response will be saved in your journal."
        )
        return RESPONDING

    async def save_response(self, update, context):
        user_id = str(update.effective_user.id)
        if user_id in self.users and self.users[user_id].get('last_prompt'):
            response = {
                'prompt': self.users[user_id]['last_prompt']['text'],
                'response': update.message.text,
                'timestamp': datetime.now().isoformat()
            }
            self.users[user_id]['responses'].append(response)
            self.save_users()

            await update.message.reply_text(
                "✨ Thank you for sharing! Your response has been saved.\n\n"
                "Remember, regular reflection helps us grow and understand ourselves better.\n"
                "Use /prompt when you're ready for another question."
            )
        return ConversationHandler.END

    async def view_history(self, update, context):
        user_id = str(update.effective_user.id)
        if user_id not in self.users or not self.users[user_id]['responses']:
            await update.message.reply_text("You haven't made any journal entries yet. Use /prompt to start!")
            return

        recent_entries = self.users[user_id]['responses'][-5:]  # Get last 5 entries
        history_text = "📖 Your Recent Journal Entries:\n\n"
        
        for entry in recent_entries:
            date = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            history_text += f"📅 {date}\n"
            history_text += f"Q: {entry['prompt']}\n"
            history_text += f"A: {entry['response']}\n\n"

        await update.message.reply_text(history_text)

    async def set_timezone(self, update, context):
        if not context.args:
            await update.message.reply_text(
                "Please provide your timezone. Example:\n"
                "/settz America/New_York\n"
                "You can find your timezone here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            )
            return

        timezone = context.args[0]
        try:
            pytz.timezone(timezone)
            user_id = str(update.effective_user.id)
            self.users[user_id]['timezone'] = timezone
            self.save_users()
            await update.message.reply_text(f"Your timezone has been set to {timezone}!")
        except pytz.exceptions.UnknownTimeZoneError:
            await update.message.reply_text("Invalid timezone. Please check the timezone list and try again.")

    async def weekly_prompt_job(self, context):
        """Send weekly prompts to all users based on their timezone"""
        for user_id, user_data in self.users.items():
            try:
                user_tz = pytz.timezone(user_data.get('timezone', 'UTC'))
                current_time = datetime.now(user_tz)
                
                # Send prompt on Monday at 9 AM in user's timezone
                if current_time.weekday() == 0 and current_time.hour == 9:
                    prompt_type = random.choice(['self_awareness', 'connections'])
                    prompt = random.choice(self.prompts[prompt_type])
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"🌟 Weekly Reflection Time!\n\n{prompt}\n\n"
                        "Take a moment to pause and reflect on this question."
                    )
            except Exception as e:
                logger.error(f"Error sending weekly prompt to user {user_id}: {e}")

def main():
    # Load environment variables
    load_dotenv()
    
    # Get bot token from environment variables
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("No bot token found. Please set BOT_TOKEN in .env file")
        return
        
    bot = JournalBot(token)
    application = Application.builder().token(bot.token).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('prompt', bot.send_prompt)],
        states={
            RESPONDING: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.save_response)]
        },
        fallbacks=[],
    )

    # Add command handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', bot.start))
    application.add_handler(CommandHandler('history', bot.view_history))
    application.add_handler(CommandHandler('settz', bot.set_timezone))

    # Add job for weekly prompts (check every hour)
    job_queue = application.job_queue
    job_queue.run_repeating(bot.weekly_prompt_job, interval=3600)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()