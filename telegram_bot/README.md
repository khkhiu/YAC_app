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
