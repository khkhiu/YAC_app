# tests/test_handlers.py

import pytest
from telegram import Update
from telegram.ext import ContextTypes
from unittest.mock import AsyncMock, MagicMock, patch
from src.bot.handlers import start_handler, stop_handler, prompt_handler, get_subscribed_users

@pytest.fixture
def mock_update():
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock()
    update.effective_user.id = 123456
    update.effective_user.first_name = "Test User"
    update.message = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    return MagicMock(spec=ContextTypes.DEFAULT_TYPE)

@pytest.mark.asyncio
async def test_start_handler(mock_update, mock_context):
    """Test the start command handler"""
    # Execute the handler
    await start_handler(mock_update, mock_context)
    
    # Verify user was subscribed
    subscribed_users = get_subscribed_users()
    assert subscribed_users[mock_update.effective_user.id] is True
    
    # Verify welcome message was sent
    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "Welcome" in call_args
    assert "/start" in call_args
    assert "/stop" in call_args
    assert "/prompt" in call_args

@pytest.mark.asyncio
async def test_stop_handler(mock_update, mock_context):
    """Test the stop command handler"""
    # First subscribe the user
    await start_handler(mock_update, mock_context)
    
    # Then unsubscribe
    await stop_handler(mock_update, mock_context)
    
    # Verify user was unsubscribed
    subscribed_users = get_subscribed_users()
    assert subscribed_users[mock_update.effective_user.id] is False
    
    # Verify unsubscribe message was sent
    mock_update.message.reply_text.assert_called_with(
        "You've unsubscribed from weekly prompts. Send /start to subscribe again!"
    )

@pytest.mark.asyncio
async def test_prompt_handler(mock_update, mock_context):
    """Test the prompt command handler"""
    # Execute the handler
    await prompt_handler(mock_update, mock_context)
    
    # Verify prompt was sent
    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "🤔 Self-Reflection Prompt:" in call_args

@pytest.mark.asyncio
async def test_multiple_users():
    """Test handling multiple users"""
    # Create two different mock updates with different user IDs
    update1 = MagicMock(spec=Update)
    update1.effective_user = MagicMock()
    update1.effective_user.id = 111
    update1.message = AsyncMock()
    
    update2 = MagicMock(spec=Update)
    update2.effective_user = MagicMock()
    update2.effective_user.id = 222
    update2.message = AsyncMock()
    
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    
    # Subscribe both users
    await start_handler(update1, context)
    await start_handler(update2, context)
    
    # Unsubscribe one user
    await stop_handler(update1, context)
    
    # Verify correct subscription states
    subscribed_users = get_subscribed_users()
    assert subscribed_users[111] is False
    assert subscribed_users[222] is True