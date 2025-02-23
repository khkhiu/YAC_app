"""Logging configuration for the Telegram Journal Bot."""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from .constants import (
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    LOG_FILE,
    MAX_LOG_SIZE,
    BACKUP_COUNT,
    LogLevel
)

def setup_logging(
    log_level: LogLevel = LogLevel.INFO,
    log_file: Optional[str] = None,
) -> None:
    """
    Set up logging configuration for the application.

    Args:
        log_level: The logging level to use
        log_file: Optional custom log file path
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Use provided log file or default
    log_file = log_file or str(log_dir / LOG_FILE)

    # Create formatter
    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )

    # Configure file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)

    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Get root logger and configure it
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.value)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the specified name.

    Args:
        name: Name for the logger, typically __name__

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)

# Set up logging when module is imported
setup_logging(
    log_level=LogLevel(os.getenv('LOG_LEVEL', LogLevel.INFO.value))
)
