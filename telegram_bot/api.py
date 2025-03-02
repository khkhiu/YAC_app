"""API service for the Telegram Journal Bot.

This module provides a Flask-based REST API to interact with the Telegram bot.
The API allows the Node.js server to start, stop, and check the status of the bot.
"""

from flask import Flask, jsonify, request
import threading
import os
import json
import time
import logging
from logging.handlers import RotatingFileHandler
import signal
import subprocess
import sys
from src.config import Config
from src.services.storage_service import StorageService

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'api.log')
handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Create Flask app
app = Flask(__name__)

# Global variables
bot_process = None
bot_thread = None
should_run = False
config = None
storage_service = None

def load_config():
    """Load the bot configuration."""
    global config, storage_service
    try:
        config = Config.load()
        storage_service = StorageService(config.users_file)
        return True
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return False

def run_bot():
    """Run the bot in a subprocess."""
    global bot_process, should_run
    
    if not should_run:
        return
    
    logger.info("Starting bot process...")
    
    try:
        # Get path to the main.py file
        main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
        
        # Start the bot process
        bot_process = subprocess.Popen(
            [sys.executable, main_py_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Process output in real-time
        while should_run and bot_process.poll() is None:
            stdout_line = bot_process.stdout.readline()
            if stdout_line:
                logger.info(f"Bot: {stdout_line.strip()}")
            
            stderr_line = bot_process.stderr.readline()
            if stderr_line:
                logger.error(f"Bot error: {stderr_line.strip()}")
        
        # Process has terminated
        if bot_process.poll() is not None:
            logger.info(f"Bot process terminated with code {bot_process.returncode}")
            
            # If should_run is still True, the process crashed and we should restart it
            if should_run:
                logger.info("Restarting bot in 10 seconds...")
                time.sleep(10)
                run_bot()
    
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        should_run = False

@app.route('/status', methods=['GET'])
def get_status():
    """Get the status of the bot."""
    global bot_process, should_run
    
    try:
        status = "running" if (bot_process and bot_process.poll() is None) else "stopped"
        uptime = time.time() - bot_start_time if status == "running" else 0
        
        # Get users count
        user_count = 0
        if storage_service:
            user_count = len(storage_service.get_all_users())
        
        return jsonify({
            "status": status,
            "uptime": uptime,
            "should_run": should_run,
            "user_count": user_count
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/start', methods=['POST'])
def start_bot():
    """Start the bot."""
    global bot_thread, should_run, bot_start_time
    
    try:
        # Check if bot is already running
        if bot_thread and bot_thread.is_alive():
            return jsonify({
                "status": "warning",
                "message": "Bot is already running"
            })
        
        # Set flags and start thread
        should_run = True
        bot_start_time = time.time()
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        
        logger.info("Bot started")
        return jsonify({
            "status": "success",
            "message": "Bot started successfully"
        })
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/stop', methods=['POST'])
def stop_bot():
    """Stop the bot."""
    global bot_process, should_run
    
    try:
        # Check if bot is running
        if not bot_process or bot_process.poll() is not None:
            return jsonify({
                "status": "warning",
                "message": "Bot is not running"
            })
        
        # Stop the bot
        should_run = False
        if bot_process:
            bot_process.terminate()
            try:
                bot_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                bot_process.kill()
            
        logger.info("Bot stopped")
        return jsonify({
            "status": "success",
            "message": "Bot stopped successfully"
        })
    except Exception as e:
        logger.error(f"Error stopping bot: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/users', methods=['GET'])
def get_users():
    """Get list of users."""
    try:
        if not storage_service:
            return jsonify({
                "status": "error",
                "message": "Storage service not initialized"
            }), 500
        
        users = storage_service.get_all_users()
        user_data = []
        
        for user_id, user in users.items():
            user_info = {
                "id": user.id,
                "preferred_day": user.preferred_prompt_day,
                "preferred_hour": user.preferred_prompt_hour,
                "entry_count": len(user.responses) if user.responses else 0
            }
            user_data.append(user_info)
        
        return jsonify({
            "status": "success",
            "user_count": len(users),
            "users": user_data
        })
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"})

def signal_handler(sig, frame):
    """Handle termination signals."""
    logger.info(f"Received signal {sig}, shutting down...")
    global bot_process, should_run
    
    should_run = False
    if bot_process:
        bot_process.terminate()
        try:
            bot_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            bot_process.kill()
    
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize variables
    bot_start_time = 0
    
    # Load configuration
    if not load_config():
        logger.error("Failed to load configuration, exiting")
        sys.exit(1)
    
    # Start Flask app
    logger.info("Starting API service...")
    app.run(host='0.0.0.0', port=5000)