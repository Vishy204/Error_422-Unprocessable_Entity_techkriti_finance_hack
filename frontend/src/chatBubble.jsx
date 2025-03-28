import React, { useState } from "react";
import axios from "axios";

const Loader = () => (
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      padding: "10px",
    }}
  >
    <div
      style={{
        width: "40px",
        height: "40px",
        border: "4px solid rgba(255, 255, 255, 0.3)",
        borderTop: "4px solid #1a73e8",
        borderRadius: "50%",
        animation: "spin 1s linear infinite",
      }}
    />
    <style>{`
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);

const ChatIcon = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const handleSendMessage = async () => {
    // Prevent sending if already loading or message is empty
    if (isLoading || !newMessage.trim()) return;

    const userMessage = { text: newMessage, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setNewMessage("");
    setIsLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/chat", {
        message: newMessage,
      });

      const aiMessage = { text: response.data.response, sender: "ai" };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error("Error sending message", error);
      const errorMessage = {
        text: "Sorry, there was an error processing your message.",
        sender: "ai",
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div
        className="chat-icon"
        onClick={toggleChat}
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          background: "linear-gradient(90deg, #1a73e8, #6366f1)",
          color: "white",
          borderRadius: "50%",
          width: "60px",
          height: "60px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          cursor: "pointer",
          boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        }}
      >
        💬
      </div>

      {isChatOpen && (
        <div
          className="chat-window"
          style={{
            position: "fixed",
            bottom: "90px",
            right: "20px",
            width: "300px",
            height: "400px",
            backgroundColor: "rgba(30,30,30,0.9)",
            borderRadius: "12px",
            display: "flex",
            flexDirection: "column",
            boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
          }}
        >
          <div
            className="chat-header"
            style={{
              background: "linear-gradient(90deg, #1a73e8, #6366f1)",
              color: "white",
              padding: "10px",
              borderTopLeftRadius: "12px",
              borderTopRightRadius: "12px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span>Finance Assistant</span>
            <button
              onClick={toggleChat}
              style={{
                background: "none",
                border: "none",
                color: "white",
                fontSize: "20px",
                cursor: "pointer",
              }}
            >
              ×
            </button>
          </div>

          <div
            className="chat-messages"
            style={{
              flexGrow: 1,
              overflowY: "auto",
              padding: "15px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                  background:
                    msg.sender === "user"
                      ? "linear-gradient(90deg, #1a73e8, #6366f1)"
                      : "linear-gradient(90deg, #34d399, #10b981)",
                  color: "white",
                  padding: "10px",
                  margin: "5px 0",
                  borderRadius: "10px",
                  maxWidth: "80%",
                }}
              >
                {msg.text}
              </div>
            ))}

            {/* Loader for AI response */}
            {isLoading && <Loader />}
          </div>

          <div
            className="chat-input"
            style={{
              display: "flex",
              padding: "10px",
              backgroundColor: "rgba(40,40,40,0.5)",
              borderBottomLeftRadius: "12px",
              borderBottomRightRadius: "12px",
            }}
          >
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              placeholder="Ask about your finances..."
              disabled={isLoading}
              style={{
                flexGrow: 1,
                backgroundColor: isLoading
                  ? "rgba(100,100,100,0.3)"
                  : "rgba(255,255,255,0.1)",
                border: "none",
                color: "white",
                padding: "10px",
                borderRadius: "8px",
                marginRight: "10px",
                cursor: isLoading ? "not-allowed" : "text",
              }}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading}
              style={{
                background: isLoading
                  ? "rgba(100,100,100,0.5)"
                  : "linear-gradient(90deg, #1a73e8, #6366f1)",
                color: "white",
                border: "none",
                borderRadius: "8px",
                padding: "10px 15px",
                cursor: isLoading ? "not-allowed" : "pointer",
                opacity: isLoading ? 0.5 : 1,
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatIcon;
