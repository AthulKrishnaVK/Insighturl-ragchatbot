import React, {
  useEffect,
  useState
} from "react";

import { useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import Sidebar from "./components/Sidebar";
import ChatBox from "./components/ChatBox";

import {
  ingestWebsite,
  askQuestion,
  getKnowledgeBases,
  createChat,
  getChatSessions,
  getMessages
} from "./services/api";

import "./App.css";

function App() {
  const { user, logout } = useAuth();

  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");

  const [knowledgeBases, setKnowledgeBases] = useState([]);
  const [chatSessions, setChatSessions] = useState([]);
  const [chatHistories, setChatHistories] = useState({});

  const [currentKbId, setCurrentKbId] = useState(null);
  const [currentChat, setCurrentChat] = useState(null);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) return;

    loadKnowledgeBases();
    loadChatSessions();
  }, [user]);

  const loadKnowledgeBases = async () => {
    try {
      const data = await getKnowledgeBases(user.id);
      setKnowledgeBases(data);
    } catch (err) {
      console.error("KB LOAD ERROR", err);
    }
  };

  const loadChatSessions = async () => {
    try {
      const chats = await getChatSessions(user.id);

      console.log(
        "CHAT SESSIONS FROM API:",
        chats
      );

      setChatSessions(chats);
    } catch (err) {
      console.error("Load chat error", err);
    }
  };

  useEffect(() => {
    if (!currentChat) return;

    loadMessages();
  }, [currentChat]);

  const loadMessages = async () => {
    try {
      const messages = await getMessages(currentChat);

      setChatHistories(prev => ({
        ...prev,
        [currentChat]: messages.map(msg => ({
          role:
            msg.role === "assistant"
              ? "bot"
              : "user",
          content: msg.content
        }))
      }));
    } catch (err) {
      console.error("MESSAGE LOAD ERROR", err);
    }
  };

  const handleIngest = async () => {
    if (!url) return;

    try {
      setLoading(true);

      const data = await ingestWebsite(
        url,
        user.id
      );

      console.log("INGEST RESPONSE:", data);
   const kbId = data.kb_id || data.id;

if (!data.success || !kbId) {
  console.error("INGEST FAILED:", data);
  alert(data.error || "Ingest failed");
  return;
}
      // if (!data || !data.kb_id) {
      //   console.error("KB ID missing",data);
      //   alert("Ingestion failed");
      //   return;
      // }

      const chat = await createChat(
        user.id,
        kbId,
        data.url || url
      );

      console.log("CHAT CREATED:", chat);

      setCurrentKbId(data.kb_id);
      setCurrentChat(chat.id);

      setChatSessions(prev => [
        chat,
        ...prev
      ]);

      setChatHistories(prev => ({
        ...prev,
        [chat.id]: []
      }));

      setUrl("");

      await loadKnowledgeBases();
    } catch (err) {
      console.error("INGEST ERROR", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    console.log("ASK DEBUG:", {
      question,
      currentKbId,
      currentChat
    });

    if (
      !question ||
      !currentKbId ||
      !currentChat
    ) {
      alert("Please ingest or select a chat first.");
      return;
    }

    const userMessage = {
      role: "user",
      content: question
    };

    setChatHistories(prev => ({
      ...prev,
      [currentChat]: [
        ...(prev[currentChat] || []),
        userMessage
      ]
    }));

    const currentQuestion = question;
    setQuestion("");

    try {
      const response = await askQuestion(
        currentQuestion,
        currentKbId,
        currentChat
      );

      console.log("ASK RESPONSE:", response);

      const botMessage = {
        role: "bot",
        content: response.answer
      };

      setChatHistories(prev => ({
        ...prev,
        [currentChat]: [
          ...(prev[currentChat] || []),
          botMessage
        ]
      }));
    } catch (err) {
      console.error("ASK ERROR", err);

      setChatHistories(prev => ({
        ...prev,
        [currentChat]: [
          ...(prev[currentChat] || []),
          {
            role: "bot",
            content: "Something went wrong."
          }
        ]
      }));
    }
  };

  if (!user) {
    return <Login />;
  }
const handleNewChat = () => {
  setCurrentChat(null);
  setCurrentKbId(null);
  setQuestion("");
  setUrl("");
};
  const messages =
    currentChat
      ? chatHistories[currentChat] || []
      : [];

  return (
    <div className="app">
      <Sidebar
        chatSessions={chatSessions}
        currentChat={currentChat}
        setCurrentChat={setCurrentChat}
        setCurrentKbId={setCurrentKbId}
          onNewChat={handleNewChat}

      />

      <div className="main">
        <div className="header">
          <h1>InsightURL</h1>

          <div>
            <span
              style={{
                marginRight: "15px"
              }}
            >
              {user.email}
            </span>

            <button onClick={logout}>
              Logout
            </button>
          </div>
        </div>
    {!currentChat && (
  <div className="ingest">
    <input
      value={url}
      onChange={(e) =>
        setUrl(e.target.value)
      }
      placeholder="Enter Website URL"
    />

    <button
      onClick={handleIngest}
      disabled={loading}
    >
      {loading ? "Ingesting..." : "Ingest"}
    </button>
  </div>
)}
        {/* <div className="ingest">
          <input
            value={url}
            onChange={(e) =>
              setUrl(e.target.value)
            }
            placeholder="Enter Website URL"
          />

          <button
            onClick={handleIngest}
            disabled={loading}
          >
            {loading
              ? "Ingesting..."
              : "Ingest"}
          </button>
        </div> */}

        <ChatBox messages={messages} />

        <div className="chat-input">
          <input
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            placeholder="Ask a question..."
          />

          <button onClick={handleAsk}
          disabled={!currentChat}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;