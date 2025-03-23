import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AddContact from "./components/AddContact"; // Adjust path to match your structure
import SendMessage from "./components/SendMessage";
import "./App.css"; // Optional: Add some basic styling

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <h1>WhatsApp Bot Dashboard</h1>
          <ul>
            <li>
              <Link to="/">Add Contact</Link>
            </li>
            <li>
              <Link to="/send-message">Send Message</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<AddContact />} />
          <Route path="/send-message" element={<SendMessage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;