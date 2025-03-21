import time
import requests
import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# MySQL Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "database": "whatsapp_bot"
}

FASTAPI_URL = "http://localhost:8000"

# Selenium WebDriver Setup (Use Chrome or Firefox)
chrome_driver_path = "./chromedriver"  # Change path if necessary
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./chrome_profile")  # Keeps you logged into WhatsApp
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
input("Press Enter after scanning the QR code...")  # Wait for user to scan QR code

# Function to fetch pending messages from FastAPI
def fetch_pending_messages():
    response = requests.get(f"{FASTAPI_URL}/pending_messages/")
    if response.status_code == 200:
        return response.json()
    return []

# Function to send a WhatsApp message
def send_whatsapp_message(phone_number, message):
    try:
        search_box = driver.find_element(By.XPATH, "//div[contains(@class,'copyable-text selectable-text')]")
        search_box.click()
        search_box.send_keys(phone_number)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)  # Wait for chat to load

        message_box = driver.find_element(By.XPATH, "//div[contains(@class,'_3Uu1_')]")
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        time.sleep(2)  # Wait for message to send
        return True
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")
        return False

# Function to update message status in MySQL
def update_message_status(message_id, status):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE messages SET status = %s WHERE id = %s", (status, message_id))
        conn.commit()
    except Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

# Main function to process messages
def process_messages():
    while True:
        messages = fetch_pending_messages()
        for msg in messages:
            phone_number = msg["phone_number"]
            message = msg["message"]
            message_id = msg["id"]

            if send_whatsapp_message(phone_number, message):
                update_message_status(message_id, "sent")

        time.sleep(10)  # Check for new messages every 10 seconds

if __name__ == "__main__":
    process_messages()
