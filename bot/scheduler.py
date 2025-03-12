# bot/scheduler.py

import schedule
import time
from bot.sender import send_whatsapp_messages
from bot.config import SCHEDULE_TIME
import logging

# Logging setup
logging.basicConfig(filename="bot/logs.txt", level=logging.INFO)

def job():
    logging.info("Scheduled job started: Sending WhatsApp messages")
    send_whatsapp_messages()

# Schedule the bot
schedule.every().day.at(SCHEDULE_TIME).do(job)

print(f"Scheduler started. Messages will be sent at {SCHEDULE_TIME} daily.")

while True:
    schedule.run_pending()
    time.sleep(60)  # Wait a minute before checking the schedule again
