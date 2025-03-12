# bot/config.py

# Define WhatsApp API mode
WHATSAPP_API = "unofficial"  # Options: "official" (Twilio/Meta) or "unofficial" (pywhatkit)

# Path to the Excel file containing contacts
EXCEL_FILE = "bot/contacts.xlsx"

# Path to the log file
LOG_FILE = "bot/logs.txt"

# Define the scheduled message sending time (24-hour format)
SCHEDULE_TIME = "08:00"  # Example: Send messages daily at 08:00 AM

# Delay (in seconds) between sending each message to avoid detection
MESSAGE_DELAY = 10
