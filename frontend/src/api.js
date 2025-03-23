import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

// Add a new contact
export const addContact = async (name, phoneNumber) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/add_client`, {
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
    for (const contact of contacts) {
      await axios.post(`${API_BASE_URL}/add_client`, {
        name: contact.name,
        phone_number: contact.phoneNumber,
      });
    }
    return { message: "All contacts added successfully" };
  } catch (error) {
    console.error("Error adding multiple contacts:", error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || "Failed to add contacts");
  }
};

// Fetch all contacts
export const getContacts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/contacts`);
    return response.data.contacts;
  } catch (error) {
    console.error("Error fetching contacts:", error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || "Failed to fetch contacts");
  }
};

// Send a message (updated to handle multiple contacts or all contacts)
export const sendMessage = async (contactIds, message, sendToAll = false) => {
  try {
    const payload = sendToAll
      ? { send_to_all: true, message }
      : { contact_ids: contactIds, message };
    const response = await axios.post(`${API_BASE_URL}/send_message`, payload);
    return response.data;
  } catch (error) {
    console.error("Error sending message:", error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || "Failed to send message");
  }
};

// Get pending messages (not implemented in backend yet, keeping for completeness)
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
    const response = await axios.post(`${API_BASE_URL}/upload_contacts`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading contacts file:", error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || "Failed to upload file");
  }
};