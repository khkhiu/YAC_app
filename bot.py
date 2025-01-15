import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler
import random

BOT_TOKEN = os.environ.get('API_TOKEN')

COMMUNITY_GROUP_LINK = "https://t.me/your_community_group"

bot = telebot.TeleBot(API_TOKEN)

# Predefined challenges
challenges = {
    "Self-Awareness": [
        "Share a memory or milestone that reminds you of your resilience.",
        "Reflect on a fear or self-doubt you’ve overcome and what you learned."
    ],
    "Connection": [
        "Thank someone who has supported you and let them know why they matter to you.",
        "Send a message to someone you lost touch with and ask how they’ve been."
    ],
    "Initiative": [
        "Share a small goal for this week and one step you will take today to achieve it.",
        "Ask for advice on something you are working on."
    ],
    "Growth": [
        "Reflect on the growth you’ve experienced so far during this challenge.",
        "Identify a limiting belief and rewrite it as an empowering one."
    ]
}

# Database mock (replace with a real DB)
responses = {}

# Scheduler for daily challenges
def send_daily_challenge():
    category = random.choice(list(challenges.keys()))
    challenge = random.choice(challenges[category])
    for user_id in responses.keys():
        bot.send_message(
            user_id,
            f"**{category} Challenge:**\n{challenge}\n\nWant to discuss? Join the community: {COMMUNITY_GROUP_LINK}",
            parse_mode="Markdown"
        )

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_challenge, 'interval', hours=24)  # Send every 24 hours
scheduler.start()

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    responses[user_id] = []  # Initialize user's response log
    bot.send_message(
        user_id,
        f"Welcome to the Daily Challenges Community Bot! 🎉\n\n"
        "Each day, you'll receive a new challenge to reflect and grow. Share your response with the community or "
        "keep it private—it’s your choice!\n\n"
        f"Join the discussion here: {COMMUNITY_GROUP_LINK}"
    )

# Submit command
@bot.message_handler(commands=['submit'])
def handle_submission(message):
    user_id = message.chat.id
    msg = bot.reply_to(message, "Please share your response to today's challenge:")
    bot.register_next_step_handler(msg, save_response)

def save_response(message):
    user_id = message.chat.id
    response = message.text
    if user_id in responses:
        responses[user_id].append({"challenge": response, "timestamp": message.date})
        bot.send_message(user_id, "Thank you for sharing your response! Would you like to share it with the community?")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Share with Community", callback_data=f"share_{user_id}"))
        markup.add(InlineKeyboardButton("Keep Private", callback_data=f"private_{user_id}"))
        bot.send_message(user_id, "Choose an option:", reply_markup=markup)
    else:
        bot.send_message(user_id, "Please start the bot using /start first.")

# Handle sharing responses
@bot.callback_query_handler(func=lambda call: call.data.startswith("share_") or call.data.startswith("private_"))
def handle_response_sharing(call):
    user_id = int(call.data.split("_")[1])
    if call.data.startswith("share_"):
        bot.send_message(
            user_id,
            "Your response has been shared with the community! 🎉\nJoin the discussion here: {COMMUNITY_GROUP_LINK}"
        )
        # Post to community feed
        bot.send_message(
            COMMUNITY_GROUP_LINK,
            f"🌟 A community member shared their response:\n\n{responses[user_id][-1]['challenge']}"
        )
    elif call.data.startswith("private_"):
        bot.send_message(user_id, "Your response has been saved privately.")

# My responses command
@bot.message_handler(commands=['my_responses'])
def show_responses(message):
    user_id = message.chat.id
    if user_id in responses and responses[user_id]:
        user_responses = "\n\n".join(
            [f"📅 {resp['timestamp']}: {resp['challenge']}" for resp in responses[user_id]]
        )
        bot.send_message(user_id, f"Here are your past responses:\n\n{user_responses}")
    else:
        bot.send_message(user_id, "You haven't submitted any responses yet!")

bot.infinity_polling()
