
import axios from "axios";
import { supabase }
from "../lib/supabase";
// const API = axios.create({
//     // baseURL: "http://127.0.0.1:8000",
//       baseURL:"http://localhost:8000"
// });
const API = axios.create({
    baseURL:
        import.meta.env.VITE_API_URL ||
        "http://127.0.0.1:8000",
});
export const getChatSessions =
async (userId) => {

    const response =
        await API.get(
            `/chat-sessions/${userId}`
        );

    return response.data;
};

export const ingestWebsite =
async (url, userId) => {

    const response =
        await API.post(
            "/ingest",
            {
                url,
                user_id: userId
            }
        );

    return response.data;
};

export const askQuestion =
async (question, kb_id,chat_id) => {

    const response =
        await API.post(
            "/ask",
            {
                question,
                kb_id,
                chat_id
            }
        );

    return response.data;
};


export const getKnowledgeBases = async (
    userId
) => {

    const response =
        await API.get(
            `/knowledge-bases/${userId}`
        );

    return response.data;
};
export const getMessages =
async (chatId) => {

    const response =
        await API.get(
            `/messages/${chatId}`
        );

    return response.data;
};

export const createChat = async (
    userId,
    kbId,
    title
) => {

    console.log("CREATE CHAT CALLED");

    console.log({
        user_id: userId,
        kb_id: kbId,
        title
    });

    const response =
        await API.post(
            "/create-chat",
            {
                user_id: userId,
                kb_id: kbId,
                title
            }
        );

    console.log(
        "CREATE CHAT RESPONSE:",
        response.data
    );

    return response.data;
};
export const deleteChat = async (chatId) => {
  const response = await API.delete(
    `/chat-session/${chatId}`
  );

  return response.data;
};