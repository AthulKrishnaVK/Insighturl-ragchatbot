

import React from "react";

function Sidebar({
    chatSessions,
    currentChat,
    setCurrentChat
}) {

    return (

        <div className="sidebar">

            <h2>Chats</h2>

            {!chatSessions ||
            chatSessions.length === 0 ? (

                <p>No chats yet</p>

            ) : (

                chatSessions.map(chat => (

                    <div
                        key={chat.id}
                        className={
                            currentChat === chat.id
                                ? "kb-item active"
                                : "kb-item"
                        }
                        onClick={() =>
                            setCurrentChat(chat.id)
                        }
                    >
                        {chat.title}
                    </div>

                ))
            )}

        </div>
    );
}

export default Sidebar;