import React from "react";
import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";
function ChatBox({ messages }) {
console.log("CHATBOX RECEIVED:", messages);
    return (
        <div className="chat-box">

            {messages.map(
                (message, index) => (

                    <div
                        key={index}
                        className={message.role}
                    >
                        <div className="bubble">

                            {/* {message.content} */}
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
    {message.content}
</ReactMarkdown>

                        </div>
                    </div>
                )
            )}

        </div>
    );
}

export default ChatBox;