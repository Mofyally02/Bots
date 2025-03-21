from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import mysql.connector

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="mofy",
    password="MofyAlly.21#",
    database="bot"
)
cursor = db.cursor()

# Endpoint to add a single contact
@app.post("/add_contact")
async def add_contact(name: str = Form(...), phone_number: str = Form(...)):
    query = "INSERT INTO contacts (name, phone_number) VALUES (%s, %s)"
    cursor.execute(query, (name, phone_number))
    db.commit()
    return {"message": "Contact added successfully"}

# Endpoint to upload a file and store multiple contacts
@app.post("/upload_contacts")
async def upload_contacts(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(contents) if file.filename.endswith(".xlsx") else pd.read_csv(contents)

    for _, row in df.iterrows():
        cursor.execute("INSERT INTO contacts (name, phone_number) VALUES (%s, %s)", (row["name"], row["phone_number"]))
    
    db.commit()
    return {"message": "Contacts uploaded successfully"}

