import React, { useState } from "react";
import { sendMessage } from "../api";
import "../styles/styles.css"; // Import the styles

const SendMessage = () => {
  const [contactId, setContactId] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await sendMessage(contactId, message);
    alert("Message sent to queue!");
    setContactId("");
    setMessage("");
  };

  return (
    <div className="container">
      <h2>Send Message</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="number"
            placeholder="Contact ID"
            value={contactId}
            onChange={(e) => setContactId(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <textarea
            placeholder="Your message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />
        </div>
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default SendMessage;
