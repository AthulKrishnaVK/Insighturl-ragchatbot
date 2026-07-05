import React from "react";
import { deleteChat } from "../services/api";
import { FiTrash2 } from "react-icons/fi";

function Sidebar({
  chatSessions,
  currentChat,
  setCurrentChat,
  setCurrentKbId,
  onNewChat,
  loadChatSessions
}) {
  const handleDelete = async (e, chatId) => {
    e.stopPropagation();

    const confirmDelete = window.confirm("Delete this chat?");
    if (!confirmDelete) return;

    const result = await deleteChat(chatId);

    if (result.success) {
      if (currentChat === chatId) {
        setCurrentChat(null);
        setCurrentKbId(null);
      }

      await loadChatSessions();
    }
  };

  return (
    <div className="sidebar">
      <h2>Chats</h2>

      <button
        className="new-chat-button"
        onClick={onNewChat}
      >
        + New Chat
      </button>

      {!chatSessions || chatSessions.length === 0 ? (
        <p className="empty-chat-text">
          No chats yet
        </p>
      ) : (
        chatSessions.map((chat) => (
          <div
            key={chat.id}
            className={
              currentChat === chat.id
                ? "kb-item active"
                : "kb-item"
            }
            onClick={() => {
              setCurrentChat(chat.id);
              setCurrentKbId(chat.kb_id);
            }}
          >
            <div className="chat-title">
              {chat.title}
            </div>

            <button
              className="delete-btn"
              onClick={(e) => handleDelete(e, chat.id)}
              title="Delete chat"
            >
              <FiTrash2 size={17} />
            </button>
          </div>
        ))
      )}
    </div>
  );
}

export default Sidebar;