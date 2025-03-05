"""AI assist message generator for the Telegram Journal Bot."""

from telegram import Update
from telegram.ext import ContextTypes
from src.utils.logger import get_logger

logger = get_logger(__name__)
from typing import List
import random

class AIAssistMessages:
    """Container for AI-generated motivational messages."""
    
    # Static collection of dinosaur-themed friendship messages
    MESSAGES = [
        {
            "title": "T-Rex-ceptional Friendships: Solid as Fossils! 🦖✨",
            "content": "Some friendships are like fossils—hidden for a while but still solid as ever. Glad you dug up that connection! Who knows what other treasures are waiting to be rediscovered? Keep those bonds evolving! 🌟💛"
        },
        """
        {
            "title": "Veloci-Rapport: Racing Back to Connection! 🦖🏃",
            "content": "Like velociraptors, true friends hunt down opportunities to reconnect! Your quick dash back to friendship shows incredible instinct. Remember, pack bonds only get stronger with time! 🌈🦖"
        },
        {
            "title": "Diplodocus-Sized Friendship: Long-Lasting Bonds! 🦕💫",
            "content": "The longest dinosaurs knew that size matters—just like the magnitude of your friendship! Standing tall through time, your connection reaches impressive heights. Keep nurturing that prehistoric bond! 🌱🦕"
        },
        {
            "title": "Stego-Spectacular Reunion: Spiky But Sweet! 🦖🍯",
            "content": "Like a stegosaurus, your friendship might have some spikes, but the heart underneath is pure gold! Embracing both the smooth and pointy parts makes your bond authentic. Celebrate that natural history! 💎🦕"
        },
        {
            "title": "Triassic Triumph: Friendships That Survive Extinction! 🦕⏳",
            "content": "While many things don't make it through time's challenges, your friendship has outlasted them all! Like dinosaurs that thrived for millions of years, your connection has proven its resilience. Extinction-proof bonds are rare—treasure yours! 🌋💖"
        }
        """
    ]
    
    @classmethod
    def get_random_message(cls) -> dict:
        """Return a random dinosaur-themed friendship message."""
        return random.choice(cls.MESSAGES)

async def send_ai_assist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Send a dinosaur-themed friendship message.
    
    This command provides users with an AI-generated motivational message
    about friendships with a fun dinosaur theme.
    """
    # Get a random dinosaur-themed message
    message = AIAssistMessages.get_random_message()
    
    # Format the message for Telegram
    formatted_message = f"**{message['title']}**\n\n**{message['content']}**"
    
    # Send the message to the user
    await update.message.reply_text(formatted_message)