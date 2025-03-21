import React, { useEffect, useState } from "react";
import { getPendingMessages } from "../api";
import "../styles/styles.css"; // Import the styles

const MessageList = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const fetchMessages = async () => {
      const response = await getPendingMessages();
      setMessages(response.data);
    };

    fetchMessages();
  }, []);

  return (
    <div className="container">
      <h2>Pending Messages</h2>
      <ul className="message-list">
        {messages.map((msg) => (
          <li key={msg.id} className="message-item">
            <strong>{msg.phone_number}:</strong> {msg.message}  
            <span className={`status ${msg.status.toLowerCase()}`}>
              (Status: {msg.status})
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MessageList;
