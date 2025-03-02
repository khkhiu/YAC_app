## Setup
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For Unix or MacOS:
source venv/bin/activate

# Create environment file and update accordingly
echo "BOT_TOKEN=your_bot_token_here
USERS_FILE=data/users.json
CHECK_INTERVAL=3600
PROMPT_HOUR=9
PROMPT_DAY=0
MAX_HISTORY=20" > .env

# Create requirements file
echo "anyio==4.8.0
APScheduler==3.11.0
certifi==2025.1.31
h11==0.14.0
httpcore==1.0.7
httpx==0.28.1
idna==3.10
python-dotenv==1.0.1
python-telegram-bot==21.10
pytz==2025.1
sniffio==1.3.1
tzlocal==5.3" > requirements.txt

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py

## Available Commands

- `/start` - Initialize the bot and get started
- `/prompt` - Get a new reflection prompt
- `/history` - View your recent journal entries
- `/set_day` - Set your preferred day for weekly prompts
- `/set_time` - Set your preferred hour for prompts
- `/settings` - View your current prompt settings
- `/help` - Show available commands and usage

## Customization

The bot uses Singapore timezone for all users. Users can set their preferred day of the week and hour to receive prompts via the `/set_day` and `/set_time` commands.

Environment variables can be adjusted in the `.env` file:
- `PROMPT_DAY` (0-6, where 0 is Monday) - Default prompt day for new users
- `PROMPT_HOUR` (0-23) - Default prompt hour for new users
- `MAX_HISTORY` - Maximum number of journal entries displayed with /history
