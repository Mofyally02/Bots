import React, { useState, useEffect } from "react";
import { getContacts, sendMessage } from "../api";
import "../styles/styles.css";

const SendMessage = () => {
  const [contacts, setContacts] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch contacts when the component mounts (to show the total number of recipients)
  useEffect(() => {
    const fetchContacts = async () => {
      try {
        const data = await getContacts();
        setContacts(data);
      } catch (error) {
        alert(`Failed to fetch contacts: ${error.message}`);
      }
    };
    fetchContacts();
  }, []);
  // Handle sending the message to all contacts
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) {
      alert("Please enter a message.");
      return;
    }

    if (contacts.length === 0) {
      alert("No contacts available to send the message to.");
      return;
    }

    setLoading(true);
    try {
      await sendMessage([], message, true); // Send to all contacts
      alert(`Message sent successfully to ${contacts.length} contact(s)!`);
      setMessage(""); // Reset the message field
    } catch (error) {
      alert(`Failed to send message: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Send Message to All Contacts</h2>
      <p>Total Contacts: {contacts.length}</p>
      <form onSubmit={handleSendMessage}>
        <div className="form-group">
          <label>Message</label>
          <textarea
            placeholder="Enter your message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={loading}
            rows="5"
          />
        </div>
        <button type="submit" disabled={loading || contacts.length === 0}>
          {loading ? "Sending..." : "Send Message to All"}
        </button>
      </form>
    </div>
  );
};

export default SendMessage;