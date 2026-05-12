import React, { useEffect, useRef, useState } from "react";
import "./App.css";

export default function App() {

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  // =========================================
  // LOAD CHAT HISTORY
  // =========================================

  useEffect(() => {
    fetchHistory();
  }, []);

  // =========================================
  // AUTO SCROLL
  // =========================================

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [chat]);

  // =========================================
  // FETCH HISTORY
  // =========================================

  const fetchHistory = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/history"
      );

      const data = await response.json();

      if (data.history) {

        // NORMALIZE HISTORY
        const normalizedHistory = data.history.map((msg) => ({
          role: msg.role,
          content:
            msg.content ||
            msg.message ||
            msg.text ||
            "",
        }));

        setChat(normalizedHistory);
      }

    } catch (error) {

      console.log("History Error:", error);

    }
  };

  // =========================================
  // SEND MESSAGE
  // =========================================

  const sendMessage = async () => {

    if (!message.trim()) return;

    // USER MESSAGE
    const userMessage = {
      role: "user",
      content: message,
    };

    setChat((prev) => [...prev, userMessage]);

    const currentMessage = message;

    setMessage("");
    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            message: currentMessage,
          }),
        }
      );

      const data = await response.json();

      // AI MESSAGE
      const aiMessage = {
        role: "assistant",
        content:
          data.response ||
          "No response from AI",
      };

      setChat((prev) => [...prev, aiMessage]);

    } catch (error) {

      console.log("Chat Error:", error);

      setChat((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Server Error",
        },
      ]);
    }

    setLoading(false);
  };

  // =========================================
  // ENTER KEY SUPPORT
  // =========================================

  const handleKeyDown = (e) => {

    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (

    <div className="container">

      {/* ================================= */}
      {/* HEADER */}
      {/* ================================= */}

      <div className="header">

        <h1 className="title">
          AI Support Agent
        </h1>

        <p className="subtitle">
          Agentic AI Customer Support System
        </p>

      </div>

      {/* ================================= */}
      {/* EXAMPLE BUTTONS */}
      {/* ================================= */}

      <div className="examples">

        <button
          onClick={() =>
            setMessage(
              "Cancel my order ORD001"
            )
          }
        >
          Cancel Order
        </button>

        <button
          onClick={() =>
            setMessage(
              "Track my order ORD1001"
            )
          }
        >
          Track Order
        </button>

        <button
          onClick={() =>
            setMessage(
              "I want refund for my order"
            )
          }
        >
          Refund
        </button>

        <button
          onClick={() =>
            setMessage(
              "Give Me FAQ"
            )
          }
        >
          FAQ
        </button>

      </div>

      {/* ================================= */}
      {/* CHAT AREA */}
      {/* ================================= */}

      <div className="chatBox">

        {chat.length === 0 && (

          <div className="welcome">

            <h2>
               How can I help you today?
            </h2>

            <p>
              Try asking:
            </p>

            <ul>
              <li>Cancel my order</li>
              <li>Track order</li>
              <li>Refund request</li>
              <li>FAQ</li>
            </ul>

          </div>
        )}

        {chat.map((msg, index) => (

          <div
            key={index}
            className={
              msg.role === "user"
                ? "userWrapper"
                : "assistantWrapper"
            }
          >

            <div
              className={
                msg.role === "user"
                  ? "userMessage"
                  : "assistantMessage"
              }
            >

              <div className="role">
                {msg.role === "user"
                  ? "You"
                  : "AI Support"}
              </div>

              <div className="content">
                {msg.content}
              </div>

            </div>

          </div>

        ))}

        {loading && (

          <div className="assistantWrapper">

            <div className="assistantMessage">

              <div className="role">
                AI Support
              </div>

              <div className="typing">
                Typing...
              </div>

            </div>

          </div>

        )}

        <div ref={bottomRef} />

      </div>

      {/* ================================= */}
      {/* INPUT AREA */}
      {/* ================================= */}

      <div className="inputArea">

        <input
          type="text"
          placeholder="Ask support..."
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          onKeyDown={handleKeyDown}
        />

        <button onClick={sendMessage}>
          Send
        </button>

      </div>

    </div>
  );
}