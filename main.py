# main.py
import asyncio
from config import Config
from bot.challenge_bot import ChallengeBot

async def main():
    bot = ChallengeBot(Config.TELEGRAM_TOKEN, Config.GROUP_CHAT_ID)
    try:
        await bot.start()
    except KeyboardInterrupt:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())