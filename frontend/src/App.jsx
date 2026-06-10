// import React, {
//     useEffect,
//     useState
// } from "react";
// import { useAuth }
// from "./context/AuthContext";
// import Sidebar from "./components/Sidebar";
// import ChatBox from "./components/ChatBox";

// import {
//     ingestWebsite,
//     askQuestion,
//     getKnowledgeBases
// }
// from "./services/api";

// function App() {

//     const [url, setUrl] =
//         useState("");
//     const {
//   user,
//   login,
//   logout
// } = useAuth();
//     const [question, setQuestion] =
//         useState("");

//     // const [messages, setMessages] =
//     //     useState([]);
//     const [chatHistories, setChatHistories] =
//     useState({});
//     const [knowledgeBases,
//         setKnowledgeBases] =
//         useState({});

//     const [currentKbId,
//         setCurrentKbId] =
//         useState(null);
//     const [chatSessions,
//     setChatSessions] = useState([]);

//     const [currentChat,
//     setCurrentChat] = useState(null);

//     useEffect(() => {

//         loadKnowledgeBases();

//     }, []);
//     const chats =
// await getChatSessions(
//     user.id
// );

// setChatSessions(chats);
//     const loadKnowledgeBases =
//         async () => {

//             const data =
//                 await getKnowledgeBases();

//             setKnowledgeBases(data);
//         };

//     const handleIngest =
//         async () => {

//             if (!url) return;

//             const data =
//                 await ingestWebsite(url);

//             setCurrentKbId(
//                 data.kb_id
//             );

//             setUrl("");

//             loadKnowledgeBases();
//         };
//     const messages =
//     currentKbId
//         ? chatHistories[currentKbId] || []
//         : [];
//     const handleAsk = async () => {

//     if (!question || !currentKbId)
//         return;

//     const userMessage = {
//         role: "user",
//         content: question
//     };

//     setChatHistories(prev => ({

//         ...prev,

//         [currentKbId]: [

//             ...(prev[currentKbId] || []),

//             userMessage
//         ]
//     }));

//     const response =
//         await askQuestion(
//             question,
//             currentKbId
//         );

//     const botMessage = {

//         role: "bot",

//         content:
//             response.answer
//     };

//     setChatHistories(prev => ({

//         ...prev,

//         [currentKbId]: [

//             ...(prev[currentKbId] || []),

//             botMessage
//         ]
//     }));

//     setQuestion("");
// };
//     // const handleAsk =
//     //     async () => {

//     //         if (
//     //             !question ||
//     //             !currentKbId
//     //         ) return;

//     //         const userMessage = {
//     //             role: "user",
//     //             content: question
//     //         };

//     //         setMessages(prev => [
//     //             ...prev,
//     //             userMessage
//     //         ]);

//     //         const response =
//     //             await askQuestion(
//     //                 question,
//     //                 currentKbId
//     //             );

//     //         setMessages(prev => [
//     //             ...prev,
//     //             userMessage,
//     //             {
//     //                 role: "bot",
//     //                 content:
//     //                     response.answer
//     //             }
//     //         ]);

//     //         setQuestion("");
//     //     };

//     return (

//         <div className="app">

//             <Sidebar
//                 knowledgeBases={
//                     knowledgeBases
//                 }
//                 currentKbId={
//                     currentKbId
//                 }
//                 setCurrentKbId={
//                     setCurrentKbId
//                 }
//             />

//             <div className="main">

//                 <h1>
//                     RAG Website Chatbot
//                 </h1>

//                 <div className="ingest">

//                     <input
//                         value={url}
//                         onChange={(e) =>
//                             setUrl(
//                                 e.target.value
//                             )
//                         }
//                         placeholder="Enter Website URL"
//                     />

//                     <button
//                         onClick={
//                             handleIngest
//                         }
//                     >
//                         Ingest
//                     </button>

//                 </div>

//                 {/* <ChatBox
//                     messages={messages}
//                 /> */}
//                 <ChatBox
//     messages={
//         currentKbId
//             ? chatHistories[currentKbId] || []
//             : []
//     }
// />

//                 <div className="chat-input">

//                     <input
//                         value={question}
//                         onChange={(e) =>
//                             setQuestion(
//                                 e.target.value
//                             )
//                         }
//                         placeholder="Ask a question..."
//                     />

//                     <button
//                         onClick={handleAsk}
//                     >
//                         Send
//                     </button>

//                 </div>

//             </div>

//         </div>
//     );
// }

// export default App;


// import React, {
//     useEffect,
//     useState
// } from "react";

// import { useAuth }
// from "./context/AuthContext";

// import Sidebar
// from "./components/Sidebar";

// import ChatBox
// from "./components/ChatBox";

// // import {
// //     ingestWebsite,
// //     askQuestion,
// //     getKnowledgeBases,
// //     getChatSessions
// // }
// import {
//     ingestWebsite,
//     askQuestion,
//     getKnowledgeBases,
//     createChat,
//     getChatSessions
// }
// // from "./services/api";
// from "./services/api";

// function App() {

//     const {
//         user,
//         login,
//         logout
//     } = useAuth();

//     const [url, setUrl] =
//         useState("");

//     const [question, setQuestion] =
//         useState("");

//     const [knowledgeBases,
//         setKnowledgeBases] =
//         useState({});

//     const [currentKbId,
//         setCurrentKbId] =
//         useState(null);

//     const [chatHistories,
//         setChatHistories] =
//         useState({});

//     const [chatSessions,
//         setChatSessions] =
//         useState([]);

//     const [loading,
//         setLoading] =
//         useState(false);

//     // =====================
//     // LOAD KBs
//     // =====================

//     useEffect(() => {

//     //     loadKnowledgeBases();

//     // }, []);
//     if(user){

//         loadKnowledgeBases();
//         loadChatSessions();

//     }

// }, [user]);
//     const loadChatSessions =
// async () => {

//     const chats =
//         await getChatSessions(
//             user.id
//         );

//     setChatSessions(chats);
// };
//     const loadKnowledgeBases =
//         async () => {

//             try {

//                 const data =
//                     await getKnowledgeBases(user.id);

//                 setKnowledgeBases(data);

//             } catch (err) {

//                 console.error(err);
//             }
//         };

//     // =====================
//     // LOAD USER CHATS
//     // =====================

//     useEffect(() => {

//         if (!user) return;

//         loadChats();

//     }, [user]);

//     const loadChats =
//         async () => {

//             try {

//                 const chats =
//                     await getChatSessions(
//                         user.id
//                     );

//                 setChatSessions(chats);

//             } catch (err) {

//                 console.error(err);
//             }
//         };

//     // =====================
//     // INGEST WEBSITE
//     // =====================

//     const handleIngest =
//         async () => {

//             if (!url) return;

//             try {

//                 setLoading(true);

//                 const data =
//                     await ingestWebsite(
//                         url,
//                         user.id
//                     );
//                     const chat = await createChat(
//     user.id,
//     data.kb_id,
//     "New Chat"
// );
// setCurrentChat(chat.id);

//                 setCurrentKbId(
//                     data.kb_id
//                 );

//                 setUrl("");

//                 await loadKnowledgeBases();

//             } catch (err) {

//                 console.error(err);

//             } finally {

//                 setLoading(false);
//             }
//         };

//     // =====================
//     // ASK QUESTION
//     // =====================

//     const handleAsk =
//         async () => {

//             if (
//                 !question ||
//                 !currentKbId
//             ) return;

//             const userMessage = {

//                 role: "user",

//                 content: question
//             };

//             setChatHistories(prev => ({

//                 ...prev,

//                 [currentKbId]: [

//                     ...(prev[currentKbId] || []),

//                     userMessage
//                 ]
//             }));

//             const currentQuestion =
//                 question;

//             setQuestion("");

//             try {

//                 const response =
//                     await askQuestion(
//                         currentQuestion,
//                         currentKbId
//                     );

//                 const botMessage = {

//                     role: "bot",

//                     content:
//                         response.answer
//                 };

//                 setChatHistories(prev => ({

//                     ...prev,

//                     [currentKbId]: [

//                         ...(prev[currentKbId] || []),

//                         botMessage
//                     ]
//                 }));

//             } catch (err) {

//                 console.error(err);

//                 setChatHistories(prev => ({

//                     ...prev,

//                     [currentKbId]: [

//                         ...(prev[currentKbId] || []),

//                         {
//                             role: "bot",
//                             content:
//                                 "Something went wrong."
//                         }
//                     ]
//                 }));
//             }
//         };

//     // =====================
//     // LOGIN SCREEN
//     // =====================

//     if (!user) {

//         return (

//             <div className="login-page">

//                 <h1>
//                     RAG Website Chatbot
//                 </h1>

//                 <button
//                     onClick={login}
//                 >
//                     Continue with Google
//                 </button>

//             </div>
//         );
//     }

//     // =====================
//     // CURRENT CHAT
//     // =====================

//     const messages =
//         currentKbId
//             ? (
//                 chatHistories[
//                     currentKbId
//                 ] || []
//             )
//             : [];

//     return (

//         <div className="app">

//             <Sidebar
//                 knowledgeBases={
//                     knowledgeBases
//                 }
//                 currentKbId={
//                     currentKbId
//                 }
//                 setCurrentKbId={
//                     setCurrentKbId
//                 }
//             />

//             <div className="main">

//                 <div className="header">

//                     <h1>
//                         RAG Website Chatbot
//                     </h1>

//                     <div>

//                         <span
//                             style={{
//                                 marginRight: "15px"
//                             }}
//                         >
//                             {
//                                 user.email
//                             }
//                         </span>

//                         <button
//                             onClick={logout}
//                         >
//                             Logout
//                         </button>

//                     </div>

//                 </div>

//                 <div className="ingest">

//                     <input
//                         value={url}
//                         onChange={(e) =>
//                             setUrl(
//                                 e.target.value
//                             )
//                         }
//                         placeholder="Enter Website URL"
//                     />

//                     <button
//                         onClick={
//                             handleIngest
//                         }
//                         disabled={loading}
//                     >
//                         {
//                             loading
//                                 ? "Ingesting..."
//                                 : "Ingest"
//                         }
//                     </button>

//                 </div>

//                 <ChatBox
//                     messages={messages}
//                 />

//                 <div className="chat-input">

//                     <input
//                         value={question}
//                         onChange={(e) =>
//                             setQuestion(
//                                 e.target.value
//                             )
//                         }
//                         placeholder="Ask a question..."
//                     />

//                     <button
//                         onClick={
//                             handleAsk
//                         }
//                     >
//                         Send
//                     </button>

//                 </div>

//             </div>

//         </div>
//     );
// }

// export default App;



import React, { useEffect, useState } from "react";

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
import "./App.css"
function App() {
  const { user, login, logout } = useAuth();

  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");

  const [knowledgeBases, setKnowledgeBases] =
    useState([]);

  const [chatSessions, setChatSessions] =
    useState([]);

  const [chatHistories, setChatHistories] =
    useState({});

  const [currentKbId, setCurrentKbId] =
    useState(null);

  const [currentChat, setCurrentChat] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  // =========================
  // LOAD USER DATA
  // =========================

  useEffect(() => {
    if (!user) return;

    loadKnowledgeBases();
    loadChatSessions();

  }, [user]);
const loadKnowledgeBases = async () => {

  try {

    const data =
      await getKnowledgeBases(
        user.id
      );

    setKnowledgeBases(data);

  } catch (err) {

    console.error(
      "KB LOAD ERROR",
      err
    );
  }
};
  // const loadKnowledgeBases =
  //   async () => {

  //     try {

  //       const data =
  //         await getKnowledgeBases();

  //       setKnowledgeBases(data);

  //     } catch (err) {

  //       console.error(err);
  //     }
  //   };

  const loadChatSessions =
    async () => {

      try {

        const chats =
          await getChatSessions(
            user.id
          );
 console.log(
      "CHAT SESSIONS FROM API:",
      chats
    );
        setChatSessions(chats);

      } catch (err) {

        console.error("Load chat error",err);
      }
    };

  // =========================
  // LOAD CHAT MESSAGES
  // =========================

  useEffect(() => {

    if (!currentChat) return;

    loadMessages();

  }, [currentChat]);

  const loadMessages =
    async () => {

      try {

        const messages =
          await getMessages(
            currentChat
          );

        setChatHistories(prev => ({

          ...prev,

          [currentChat]:
            messages.map(msg => ({
              role:
                msg.role === "assistant"
                  ? "bot"
                  : "user",

              content:
                msg.content
            }))
        }));

      } catch (err) {

        console.error(err);
      }
    };

  // =========================
  // INGEST WEBSITE
  // =========================

  const handleIngest =
    async () => {

      if (!url) return;

      try {

        setLoading(true);
//      const data = await ingestWebsite(
//   url,
//   user.id
// );

// console.log("INGEST RESPONSE:", data);

// if (!data || !data.kb_id) {
//   console.error("KB ID missing");
//   return;
// }

// console.log("CALLING CREATE CHAT");

// const chat = await createChat(
//   user.id,
//   data.kb_id,
//   "New Chat"
// );

// console.log("CHAT RESPONSE:", chat);
//         // const data =
//         //   await ingestWebsite(
//         //     url,
//         //     user.id
//         //   );
//         // console.log("INGEST RESPONSE", data);
//         // console.log("KB ID:", data.kb_id);
//         // const chat =
//         //   await createChat(
//         //     user.id,
//         //     data.kb_id,
//         //     "New Chat"
//         //   );
//         //   console.log("CHAT:", chat);

//         setCurrentKbId(
//           data.kb_id
//         );

//         setCurrentChat(
//           chat.id
//         );
const data =
  await ingestWebsite(
    url,
    user.id
  );

console.log(
  "INGEST RESPONSE",
  data
);

if (!data.kb_id) {

  console.error(
    "KB ID missing"
  );

  return;
}

const chat =
  await createChat(
    user.id,
    data.kb_id,
    data.url
  );

console.log(
  "CHAT CREATED",
  chat
);

setCurrentKbId(
  data.kb_id
);

setCurrentChat(
  chat.id
);
        console.log("CHAT RESPONSE:", chat);
console.log("CHAT ID:", chat.id);

        setUrl("");

        await loadKnowledgeBases();
        await loadChatSessions();

      } catch (err) {

        console.error(err);

      } finally {

        setLoading(false);
      }
    };

  // =========================
  // ASK QUESTION
  // =========================

  const handleAsk =
     
    async () => {
console.log({
    question,
    currentKbId,
    currentChat
});
      if (
        !question ||
        !currentKbId ||
        !currentChat
      )
        return;

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

      const currentQuestion =
        question;

      setQuestion("");

      try {

        const response =
          await askQuestion(
            currentQuestion,
            currentKbId,
            currentChat
          );
          console.log(
             "ASK RESPONSE:",
              response
               );

        const botMessage = {

          role: "bot",

          content:
            response.answer
        };
        console.log("BOT MESSAGE:", botMessage);

        setChatHistories(prev => ({

          ...prev,

          [currentChat]: [

            ...(prev[currentChat] || []),

            botMessage
          ]
        }));

      } catch (err) {

        console.error(err);

        setChatHistories(prev => ({

          ...prev,

          [currentChat]: [

            ...(prev[currentChat] || []),

            {
              role: "bot",
              content:
                "Something went wrong."
            }
          ]
        }));
      }
    };

  // =========================
  // LOGIN SCREEN
  // =========================

  if (!user) {

    return (
<Login/>
      // <div className="login-page">

      //   <h1>
      //     RAG Website Chatbot
      //   </h1>

      //   <button
      //     onClick={login}
      //   >
      //     Continue with Google
      //   </button>

      // </div>
    );
  }

  const messages =
    currentChat
      ? chatHistories[currentChat] || []
      : [];
console.log("CURRENT CHAT:", currentChat);
console.log("CHAT HISTORIES:", chatHistories);
console.log("MESSAGES SENT TO CHATBOX:", messages);
  return (

    <div className="app">

      <Sidebar
        chatSessions={
          chatSessions
        }
        currentChat={
          currentChat
        }
        setCurrentChat={
          setCurrentChat
        }
      />

      <div className="main">

        <div className="header">

          <h1>
            InsightURL
          </h1>

          <div>

            <span
              style={{
                marginRight: "15px"
              }}
            >
              {user.email}
            </span>

            <button
              onClick={logout}
            >
              Logout
            </button>

          </div>

        </div>

        <div className="ingest">

          <input
            value={url}
            onChange={(e) =>
              setUrl(
                e.target.value
              )
            }
            placeholder="Enter Website URL"
          />

          <button
            onClick={
              handleIngest
            }
            disabled={loading}
          >
            {
              loading
                ? "Ingesting..."
                : "Ingest"
            }
          </button>

        </div>

        <ChatBox
          messages={messages}
        />

        <div className="chat-input">

          <input
            value={question}
            onChange={(e) =>
              setQuestion(
                e.target.value
              )
            }
            placeholder="Ask a question..."
          />

          <button
            onClick={
              handleAsk
            }
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

export default App;
