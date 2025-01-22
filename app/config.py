# app/config.py
import os
import logging

# Challenge types
SELF_AWARENESS = 'self_awareness'
CONNECTION = 'connection'
GROWTH = 'growth'

# States for conversation handler
CHOOSING = 0
COMPLETING = 1

# Challenge pools
CHALLENGES = {
    SELF_AWARENESS: [
        "Share a memory that demonstrates your resilience.",
        "Reflect on a fear you've overcome and what you learned.",
        "Write about a moment when you felt truly proud of yourself.",
        "Describe a challenge that shaped who you are today.",
        "Identify three of your strongest qualities and why.",
    ],
    CONNECTION: [
        "Thank someone who has supported you recently.",
        "Reach out to someone you've lost touch with.",
        "Write a note of appreciation to a mentor.",
        "Share a meaningful memory with a friend.",
        "Express gratitude to someone who inspired you.",
    ],
    GROWTH: [
        "Reflect on your personal growth this month.",
        "Identify and rewrite a limiting belief.",
        "Set three meaningful goals for the next month.",
        "Write about a lesson you learned from a mistake.",
        "Plan one step toward a long-term goal.",
    ]
}

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database configuration
DB_DIR = 'data'
DB_FILE = 'challenges.db'
DB_PATH = os.path.join(DB_DIR, DB_FILE)
