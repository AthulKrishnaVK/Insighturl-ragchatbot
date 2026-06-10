// import React from "react";

// function Sidebar({
//     knowledgeBases,
//     currentKbId,
//     setCurrentKbId
// }) {

//     return (
//         <div className="sidebar">

//             <h2>Knowledge Bases</h2>

//             {Object.keys(knowledgeBases).length === 0 ? (
//                 <p>No websites ingested</p>
//             ) : (
// knowledgeBases.map((kb) => (
//     <div
//         key={kb.kb_id}
//         className={
//             currentKbId === kb.kb_id
//                 ? "kb-item active"
//                 : "kb-item"
//         }
//         onClick={() =>
//             setCurrentKbId(
//                 kb.kb_id
//             )
//         }
//     >
//         {kb.website_url}
//     </div>
// ))
//                 // Object.entries(
//                 //     knowledgeBases
//                 // ).map(([kbId, kb]) => (

//                 //     <div
//                 //         key={kbId}
//                 //         className={
//                 //             currentKbId === kbId
//                 //                 ? "kb-item active"
//                 //                 : "kb-item"
//                 //         }
//                 //         onClick={() =>
//                 //             setCurrentKbId(kbId)
//                 //         }
//                 //     >
//                 //         {kb.url}
//                 //     </div>
//                 // ))
//             )}

//         </div>
//     );
// }

// export default Sidebar;

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