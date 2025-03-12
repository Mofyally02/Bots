# bot/logger.py

import logging
from bot.config import LOG_FILE

# Configure logging settings
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(phone, status):
    """
    Logs a message sent status.
    """
    logging.info(f"Message to {phone}: {status}")

def log_error(error_message):
    """
    Logs an error.
    """
    logging.error(error_message)
