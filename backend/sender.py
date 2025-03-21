# bot/sender.py

import pandas as pd
import pywhatkit as kit 
import time
import logging
from config import DB_CONFIG, LOG_FILE, MESSAGE_DELAY

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def send_whatsapp_messages():
    """
    Reads contacts from an Excel file and sends WhatsApp messages to each recipient.
    """
    try:
        df = pd.read_excel(DB_CONFIG)

        for index, row in df.iterrows():
            phone = row["Phone Number"]
            message = row["Message"]

            if row["Status"] == "Sent":
                continue  # Skip already sent messages

            try:
                # Send message via WhatsApp Web
                kit.sendwhatmsg_instantly(phone, message, wait_time=MESSAGE_DELAY, tab_close=True)
                
                # Update status in Excel
                df.at[index, "Status"] = "Sent"
                logging.info(f"Message sent to {phone}")

            except Exception as e:
                df.at[index, "Status"] = f"Failed: {str(e)}"
                logging.error(f"Failed to send message to {phone}: {e}")

            # Wait before sending the next message (to prevent rate-limiting)
            time.sleep(MESSAGE_DELAY)

        # Save updated Excel file
        df.to_excel(EXCEL_FILE, index=False)

    except Exception as e:
        logging.error(f"Error in sending messages: {e}")

if __name__ == "__main__":
    send_whatsapp_messages()
