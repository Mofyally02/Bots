# backend/db.py
import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    """Establish connection to MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def fetch_contacts():
    """Retrieve all contacts from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, phone_number FROM contacts WHERE message_status='pending'")
    contacts = cursor.fetchall()
    cursor.close()
    conn.close()
    return contacts
