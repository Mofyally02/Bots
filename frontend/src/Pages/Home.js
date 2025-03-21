import React from "react";
import AddContact from "../components/AddContact";
import SendMessage from "../components/SendMessage";
import MessageList from "../components/MessageList";

const Home = () => {
  return (
    <div>
      <h1>WhatsApp Bot Dashboard</h1>
      <AddContact />
      <SendMessage />
      <MessageList />
    </div>
  );
};

export default Home;
