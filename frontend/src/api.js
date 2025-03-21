import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; 

// Add a new contact
export const addContact = async (name, phoneNumber) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/add_contact/`, {
      name,
      phone_number: phoneNumber,
    });
    return response.data;
  } catch (error) {
    console.error("Error adding contact:", error.response?.data || error.message);
    throw error;
  }
};

// Add multiple contacts (bulk upload)
export const addMultipleContacts = async (contacts) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/add_multiple_contacts/`, {
      contacts, // Expecting an array of { name, phone_number }
    });
    return response.data;
  } catch (error) {
    console.error("Error adding multiple contacts:", error.response?.data || error.message);
    throw error;
  }
};

// Send a message
export const sendMessage = async (contactId, message) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/send_message/`, {
      contact_id: contactId,
      message: message,
    });
    return response.data;
  } catch (error) {
    console.error("Error sending message:", error.response?.data || error.message);
    throw error;
  }
};

// Get pending messages
export const getPendingMessages = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/pending_messages/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching pending messages:", error.response?.data || error.message);
    throw error;
  }
};

// Upload contacts file
export const uploadContactsFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_BASE_URL}/upload_contacts/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading contacts file:", error.response?.data || error.message);
    throw error;
  }
};
