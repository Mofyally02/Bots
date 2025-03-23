from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
import pandas as pd
import io
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="mofy",
            password="MofyAlly.21#",
            database="whatsapp_bot"
        )
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

# Pydantic model for client data
class Client(BaseModel):
    name: str
    phone_number: str

# Pydantic model for sending a message
class Message(BaseModel):
    contact_ids: list[int] | None = None  # Optional list of contact IDs
    send_to_all: bool = False  # Flag to send to all contacts
    message: str

# Endpoint to add a single client
@app.post("/add_client")
async def add_client(client: Client):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO contacts (name, phone_number)
        VALUES (%s, %s)
        """
        values = (client.name, client.phone_number)

        cursor.execute(insert_query, values)
        connection.commit()

        return {"message": "Client added successfully", "client": client.dict()}

    except Error as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=400, detail="Phone number already exists")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Endpoint to fetch all contacts
@app.get("/contacts")
async def get_contacts():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        select_query = "SELECT id, name, phone_number FROM contacts"
        cursor.execute(select_query)
        contacts = cursor.fetchall()

        return {"contacts": contacts}

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Endpoint to send a message (updated to send via WhatsApp)
@app.post("/send_message")
async def send_message(message: Message):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Determine the list of contact IDs to send the message to
        if message.send_to_all:
            # Fetch all contact IDs and phone numbers if send_to_all is true
            cursor.execute("SELECT id, phone_number FROM contacts")
            contacts = cursor.fetchall()
            contact_ids = [contact[0] for contact in contacts]
            phone_numbers = [contact[1] for contact in contacts]
        else:
            # Use the provided contact_ids
            if not message.contact_ids:
                raise HTTPException(status_code=400, detail="contact_ids or send_to_all must be provided")
            contact_ids = message.contact_ids
            # Fetch phone numbers for the specified contact_ids
            phone_numbers = []
            for contact_id in contact_ids:
                cursor.execute("SELECT phone_number FROM contacts WHERE id = %s", (contact_id,))
                result = cursor.fetchone()
                if not result:
                    raise HTTPException(status_code=404, detail=f"Contact with ID {contact_id} not found")
                phone_numbers.append(result[0])

        if not contact_ids:
            raise HTTPException(status_code=404, detail="No contacts found to send the message to")

        # Send the message to each contact via WhatsApp
        for contact_id, phone_number in zip(contact_ids, phone_numbers):
            # Ensure phone number is in international format (e.g., +1234567890)
            if not phone_number.startswith("+"):
                phone_number = f"+{phone_number}"

            try:
                # Send message via Twilio WhatsApp API
                twilio_message = twilio_client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=message.message,
                    to=f"whatsapp:{phone_number}"
                )
                print(f"Message sent to {phone_number}: {twilio_message.sid}")

                # Store the message in the database
                insert_query = """
                INSERT INTO messages (contact_id, message, status)
                VALUES (%s, %s, %s)
                """
                values = (contact_id, message.message, "sent")
                cursor.execute(insert_query, values)
            except Exception as e:
                print(f"Failed to send message to {phone_number}: {str(e)}")
                # Store the message with a failed status
                insert_query = """
                INSERT INTO messages (contact_id, message, status)
                VALUES (%s, %s, %s)
                """
                values = (contact_id, message.message, "failed")
                cursor.execute(insert_query, values)

        connection.commit()

        return {"message": f"Message processed for {len(contact_ids)} contact(s)"}

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Endpoint to upload a contacts file
@app.post("/upload_contacts")
async def upload_contacts(file: UploadFile = File(...)):
    connection = None
    cursor = None
    try:
        contents = await file.read()
        file_type = file.filename.split(".")[-1].lower()

        if file_type == "csv":
            df = pd.read_csv(io.BytesIO(contents))
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use .csv or .xlsx")

        name_variations = ["name", "full_name", "Name", "Full Name"]
        phone_variations = ["phone_number", "phone", "Phone", "Phone Number", "phoneNumber"]

        name_col = None
        phone_col = None
        for col in df.columns:
            if col in name_variations:
                name_col = col
            if col in phone_variations:
                phone_col = col

        if not name_col or not phone_col:
            raise HTTPException(
                status_code=400,
                detail="File must contain a 'name' column (or variations: full_name, Name, Full Name) "
                       "and a 'phone_number' column (or variations: phone, Phone, Phone Number, phoneNumber)"
            )

        df = df.rename(columns={name_col: "name", phone_col: "phone_number"})
        df = df[["name", "phone_number"]]

        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO contacts (name, phone_number)
        VALUES (%s, %s)
        """
        for _, row in df.iterrows():
            values = (row["name"], str(row["phone_number"]))
            cursor.execute(insert_query, values)

        connection.commit()
        return {"message": "Contacts uploaded successfully"}

    except Error as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=400, detail="One or more phone numbers already exist")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "API is running"}