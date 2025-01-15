# bot/handlers/stats_handlers.py
from telegram import Update
from telegram.ext import CallbackContext
from database.db import Database
from utils.helpers import format_date

async def show_journal(update: Update, context: CallbackContext, db: Database):
    user_id = update.effective_user.id
    responses = db.responses.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(10)
    
    journal_text = "📝 Your Challenge Journal (Last 10 Entries):\n\n"
    
    for response in responses:
        date = format_date(response["timestamp"])
        journal_text += (
            f"📅 {date}\n"
            f"Category: {response['category'].replace('_', ' ').title()}\n"
            f"Prompt: {response['prompt']}\n"
            f"Your Response: {response['response']}\n\n"
        )
    
    await update.message.reply_text(journal_text)

async def show_stats(update: Update, context: CallbackContext, db: Database):
    user_id = update.effective_user.id
    user = db.users.find_one({"user_id": user_id})
    
    total_challenges = db.responses.count_documents({"user_id": user_id})
    category_stats = {
        category: db.responses.count_documents({
            "user_id": user_id,
            "category": category
        })
        for category in CHALLENGES.keys()
    }
    
    stats_text = (
        "📊 Your Challenge Statistics\n\n"
        f"Current Streak: {user['streak']} days\n"
        f"Total Challenges Completed: {total_challenges}\n\n"
        "Category Breakdown:\n"
    )
    
    for category, count in category_stats.items():
        stats_text += f"- {category.replace('_', ' ').title()}: {count}\n"
    
    await update.message.reply_text(stats_text)
