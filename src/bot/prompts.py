# src/bot/prompts.py

import random
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Collection of self-awareness and connection prompts
PROMPTS = [
    "What moment made you smile today? Share what made it special.",
    "Reflect on a challenge you faced this week. What did you learn about yourself?",
    "Name three things you're grateful for and why they matter to you.",
    "Think about someone who inspires you. What qualities do you admire in them?",
    "What's one small act of kindness you witnessed or performed recently?",
    "Describe a recent situation where you felt proud of how you handled it.",
    "What's one thing you'd like to improve about yourself? What small step can you take today?",
    "Share a meaningful conversation you had recently. What made it special?",
    "What boundaries did you set or maintain this week? How did it feel?",
    "Reflect on a recent decision. What values guided your choice?",
    "What's one way you showed up for someone else this week?",
    "Describe a moment when you felt truly connected to others.",
    "What self-care practice had the biggest impact on your week?",
    "Share something new you learned about yourself recently.",
    "How did you handle a difficult emotion this week?"
]

# Categorized prompts for future feature expansion
PROMPT_CATEGORIES = {
    'self_reflection': [
        "What patterns have you noticed in your behavior this week?",
        "How have your actions aligned with your values today?",
        "What emotion has been most present for you lately?"
    ],
    'relationships': [
        "How have you nurtured your relationships this week?",
        "What boundaries need to be set or reinforced in your life?",
        "Who would you like to express gratitude to and why?"
    ],
    'growth': [
        "What skill would you like to develop further?",
        "What's one habit you'd like to build or break?",
        "What's a recent mistake you learned from?"
    ]
}

def get_random_prompt() -> str:
    """
    Return a random prompt from the general collection
    """
    prompt = random.choice(PROMPTS)
    logger.debug(f"Selected prompt: {prompt}")
    return prompt

def get_categorical_prompt(category: str) -> str:
    """
    Return a random prompt from a specific category
    """
    if category in PROMPT_CATEGORIES:
        prompt = random.choice(PROMPT_CATEGORIES[category])
        logger.debug(f"Selected {category} prompt: {prompt}")
        return prompt
    else:
        logger.warning(f"Category {category} not found, returning general prompt")
        return get_random_prompt()