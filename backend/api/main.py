

from fastapi import FastAPI
from pydantic import BaseModel

from crawler.crawler import crawl_website
from rag.embeddings import create_vector_db
from rag.chatbot import ask_question
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from database.supabase_client import supabase
import uuid
import json
import os


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("backend/data", exist_ok=True)

CHAT_SESSION_FILE = "backend/data/chat_sessions.json"


class URLRequest(BaseModel):
    url: str
    user_id:str


class ChatRequest(BaseModel):
    question: str
    kb_id: str
    chat_id:str
class CreateChatRequest(BaseModel):
    user_id: str
    kb_id: str
    title: str



if os.path.exists(CHAT_SESSION_FILE):

    with open(
        CHAT_SESSION_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        knowledge_bases = json.load(f)

else:

    knowledge_bases = {}




@app.post("/ingest")
def ingest(data: URLRequest):

    kb_id = str(uuid.uuid4())[:8]

    try:

        pages = crawl_website(
            data.url,
            max_pages=20
        )
        title = "Website"

        if pages and len(pages) > 0:
            title = pages[0].get(
               "title",
               "Website"
          )

        file_path = (
            f"backend/data/"
            f"website_content_{kb_id}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                pages,
                f,
                indent=4,
                ensure_ascii=False
            )

        page_count, chunk_count = (
            create_vector_db(kb_id)
        )

        knowledge_bases[kb_id] = {
            "url": data.url,
            "pages": page_count,
            "chunks": chunk_count
        }
     
        result = supabase.table(
        "knowledge_bases"
        ).insert({

        "user_id": data.user_id,
        "website_url": data.url,
        "kb_id": kb_id

         }).execute()

        print("KB INSERT:")
        print(result.data)

        with open(
            CHAT_SESSION_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                knowledge_bases,
                f,
                indent=4
            )

        response= {
            "success": True,
            "kb_id": kb_id,
            "title":title,
            "url": data.url,
            "pages": page_count,
            "chunks": chunk_count
        }
        print("Ingest return",response)
        return response

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }



@app.post("/ask")
def chat(data: ChatRequest):

    print("=" * 50)
    print("QUESTION:", data.question)
    print("CHAT ID:", data.chat_id)

    try:
        chat_result = (
            supabase
            .table("chat_sessions")
            .select("kb_id")
            .eq("id", data.chat_id)
            .single()
            .execute()
        )

        real_kb_id = chat_result.data["kb_id"]

        print("REAL KB ID FROM CHAT:", real_kb_id)

        result = ask_question(
            data.question,
            real_kb_id
        )

        supabase.table("messages").insert([
            {
                "chat_id": data.chat_id,
                "role": "user",
                "content": data.question
            },
            {
                "chat_id": data.chat_id,
                "role": "assistant",
                "content": result["answer"]
            }
        ]).execute()

        return result

    except Exception as e:
        print("CHAT ERROR:", e)

        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }


@app.get("/knowledge-bases/{user_id}")
def get_knowledge_bases(user_id: str):

    result = (
        supabase
        .table("knowledge_bases")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return result.data


@app.delete("/knowledge-base/{kb_id}")
def delete_kb(kb_id: str):

    try:

        if kb_id in knowledge_bases:

            del knowledge_bases[kb_id]

            with open(
                CHAT_SESSION_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    knowledge_bases,
                    f,
                    indent=4
                )

        return {
            "success": True
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

@app.post("/create-chat")
def create_chat(data: CreateChatRequest):

    result = supabase.table(
        "chat_sessions"
    ).insert({

        "user_id": data.user_id,
        "kb_id": data.kb_id,
        "title": data.title

    }).execute()

    return result.data[0]
    

@app.get("/chat-sessions/{user_id}")
def get_chats(user_id: str):

    result = (
        supabase
        .table("chat_sessions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at",desc=True)
        .execute()
    )

    print("\nCHAT SESSIONS:")
    print(result.data)

    return result.data

@app.get("/messages/{chat_id}")
def get_messages(chat_id: str):

    result = supabase.table(
        "messages"
    ).select("*").eq(
        "chat_id",
        chat_id
    ).order(
        "created_at"
    ).execute()

    return result.data



@app.get("/")
def root():

    return {
        "message":
        "RAG Website Chatbot Backend Running"
    }