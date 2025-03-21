import os

# Database Configuration (Update with your credentials)
DB_CONFIG = {
    "host": "127.0.0.1",        # MySQL server host
    "user": "root",    # MySQL username
    "password": "MofyAlly.21#",  # MySQL password
    "database": "whatsapp_bot",  # Database name
}

# Logging configuration
LOG_FILE = "bot.log"

# Time delay settings (in seconds)
MESSAGE_DELAY = 5  # Delay between messages
SCROLL_DELAY = 2   # Delay when scrolling WhatsApp chats

# WebDriver settings
WHATSAPP_WEB_URL = "https://web.whatsapp.com/"

# Correct ChromeDriver path
CHROME_DRIVER_PATH = "/Users/mofyally/Develop Projects/WhatsApp Bot/chromedriver_mac64/chromedriver"

# Validate if ChromeDriver exists
if not os.path.exists(CHROME_DRIVER_PATH):
    raise FileNotFoundError(f"❌ ChromeDriver not found at: {CHROME_DRIVER_PATH}. Please check the path.")

print("✅ Config loaded successfully. Using MySQL database.")
