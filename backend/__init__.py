# bot/__init__.py

import os

# Define the bot package initialization
__version__ = "1.0.0"
__author__ = "Your Name"

# Ensure required directories exist
LOG_DIR = "bot/logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print("WhatsApp Bot package initialized.")
