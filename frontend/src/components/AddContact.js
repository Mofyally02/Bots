import React, { useState } from "react";
import { addMultipleContacts, uploadContactsFile } from "../api";
import "../styles/styles.css";

const AddContact = () => {
  const [name, setName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [file, setFile] = useState(null);
  const [disableInputs, setDisableInputs] = useState(false);

  const validatePhoneNumber = (number) => {
    // Basic validation for international format (e.g., +1234567890)
    const phoneRegex = /^\+\d{10,15}$/;
    return phoneRegex.test(number);
  };

  const handleAddContact = async () => {
    if (!name.trim() || !phoneNumber.trim()) {
      alert("Please enter both Name and Phone Number.");
      return;
    }

    if (!validatePhoneNumber(phoneNumber)) {
      alert("Please enter a valid phone number in international format (e.g., +1234567890).");
      return;
    }

    const newContact = { name, phoneNumber };
    try {
      await addMultipleContacts([newContact]);
      alert("Contact added successfully!");
      setName("");
      setPhoneNumber("");
      setDisableInputs(false);
    } catch (error) {
      console.error("Error adding contact:", error);
      alert(`Failed to add contact: ${error.message || "Try again."}`);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setDisableInputs(true);
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    try {
      await uploadContactsFile(file);
      alert("Contacts file uploaded and saved successfully!");
      setFile(null);
      setDisableInputs(false);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert(`Failed to upload file: ${error.message || "Try again."}`);
    }
  };

  return (
    <div className="container">
      <h2>Add Contact</h2>

      {/* Single Contact Form */}
      <div className="form-group">
        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={disableInputs}
        />
      </div>
      <div className="form-group">
        <input
          type="text"
          placeholder="Phone Number (e.g., +1234567890)"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          disabled={disableInputs}
        />
      </div>
      <button onClick={handleAddContact} disabled={disableInputs}>
        Add Contact
      </button>

      <h3>OR</h3>

      {/* File Upload Form */}
      <form onSubmit={handleFileUpload}>
        <input
          type="file"
          accept=".xlsx, .csv"
          onChange={handleFileChange}
          disabled={disableInputs && !file}
        />
        <button type="submit" disabled={!file}>
          Upload File
        </button>
      </form>
    </div>
  );
};

export default AddContact;