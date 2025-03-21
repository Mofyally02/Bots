import React, { useState } from "react";
import { addMultipleContacts, uploadContactsFile } from "../api";
import "../styles/styles.css";

const AddContact = () => {
  const [name, setName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [contacts, setContacts] = useState([]);
  const [file, setFile] = useState(null);
  const [disableInputs, setDisableInputs] = useState(false);

  // Add a contact manually and send to the database
  const handleAddContact = async () => {
    if (!name.trim() || !phoneNumber.trim()) {
      alert("Please enter both Name and Phone Number.");
      return;
    }

    const newContact = { name, phoneNumber };
    try {
      await addMultipleContacts([newContact]); // Save to database
      setContacts([...contacts, newContact]);
      alert("Contact added successfully!");
      setName("");
      setPhoneNumber("");
      setDisableInputs(true);
    } catch (error) {
      console.error("Error adding contact:", error);
      alert("Failed to add contact. Try again.");
    }
  };

  // Remove a contact from the list
  const handleRemoveContact = (index) => {
    const updatedContacts = contacts.filter((_, i) => i !== index);
    setContacts(updatedContacts);
    if (updatedContacts.length === 0) {
      setDisableInputs(false);
    }
  };

  // Submit all added contacts to the database
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (contacts.length === 0) {
      alert("Please add at least one contact.");
      return;
    }

    try {
      await addMultipleContacts(contacts);
      alert("Contacts added successfully!");
      setContacts([]);
      setDisableInputs(false);
    } catch (error) {
      console.error("Error adding contacts:", error);
      alert("Failed to add contacts. Try again.");
    }
  };

  // Handle file upload selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setContacts([]); // Clear manual entries
    setDisableInputs(true);
  };

  // Upload file and send data to the database
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
      alert("Failed to upload file. Try again.");
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
          placeholder="Phone Number"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          disabled={disableInputs}
        />
      </div>
      <button onClick={handleAddContact} disabled={disableInputs}>
        Add Contact
      </button>

      {/* Display added contacts */}
      {contacts.length > 0 && (
        <div className="contacts-list">
          <h3>Contacts to be Added</h3>
          <ul>
            {contacts.map((contact, index) => (
              <li key={index}>
                {contact.name} - {contact.phoneNumber}
                <button  onClick={() => handleRemoveContact(index)}  style={{ width: "60px" }} > ❌ </button>
              </li>
            ))}
          </ul>
          <button onClick={handleSubmit}>Submit Contacts</button>
        </div>
      )}

      <h3>OR</h3>

      {/* File Upload Form */}
      <form onSubmit={handleFileUpload}>
        <input
          type="file"
          accept=".xlsx, .csv"
          onChange={handleFileChange}
          disabled={contacts.length > 0}
        />
        <button type="submit" disabled={contacts.length > 0 || !file}>
          Upload File
        </button>
      </form>
    </div>
  );
};

export default AddContact;
