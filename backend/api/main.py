from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from crawler.crawler import crawl_website
from rag.embeddings import create_vector_db
from rag.chatbot import ask_question
from database.supabase_client import supabase
import time
import uuid
import json
import os
from cache.redis_cache import (
    get_cached_answer,
    save_answer_to_cache
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
         "https://insighturl-ragchatbot.vercel.app",
         "https://athul93-insighturl-backend.hf.space"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("backend/data", exist_ok=True)

CHAT_SESSION_FILE = "backend/data/chat_sessions.json"


class URLRequest(BaseModel):
    url: str
    user_id: str


class ChatRequest(BaseModel):
    question: str
    kb_id: str
    chat_id: str


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


def normalize_url(url: str):
    return url.strip().rstrip("/")


def get_existing_knowledge_base(user_id: str, url: str):
    normalized_url = normalize_url(url)

    result = (
        supabase
        .table("knowledge_bases")
        .select("*")
        .eq("user_id", user_id)
        .eq("website_url", normalized_url)
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None


@app.post("/ingest")
def ingest(data: URLRequest):
    
    try:
        normalized_url = normalize_url(data.url)

        existing_kb = get_existing_knowledge_base(
            data.user_id,
            normalized_url
        )

        if existing_kb:
            response = {
                "success": True,
                "cached": True,
                "message": "Website already ingested",
                "kb_id": existing_kb["kb_id"],
                "title": existing_kb.get("title", "Website"),
                "url": existing_kb["website_url"],
                "pages": existing_kb.get("pages", 0),
                "chunks": existing_kb.get("chunks", 0)
            }

            print("CACHE HIT:")
            print(response)

            return response

        kb_id = str(uuid.uuid4())[:8]
        start = time.time()
        pages = crawl_website(
            normalized_url,
            max_pages=5,
            max_workers=10
        )
        print("CRAWLING TIME:", time.time() - start)
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
        start = time.time()
        page_count, chunk_count = create_vector_db(kb_id)
        print("EMBEDDING TIME:", time.time() - start)
        knowledge_bases[kb_id] = {
            "url": normalized_url,
            "pages": page_count,
            "chunks": chunk_count,
            "title": title
        }

        result = (
            supabase
            .table("knowledge_bases")
            .insert({
                "user_id": data.user_id,
                "website_url": normalized_url,
                "kb_id": kb_id,
                
            })
            .execute()
        )

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

        response = {
            "success": True,
            "cached": False,
            "message": "Website ingested successfully",
            "kb_id": kb_id,
            "title": title,
            "url": normalized_url,
            "pages": page_count,
            "chunks": chunk_count
        }

        print("INGEST RETURN:")
        print(response)

        return response

    # except Exception as e:
    #     print("INGEST ERROR:", e)

    #     return {
    #         "success": False,
    #         "cached": False,
    #         "error": str(e)
    #     }
    except Exception as e:
         print("INGEST ERROR:", e)

         return {
        "success": False,
        "cached": False,
        "kb_id": None,
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

        cached_result = get_cached_answer(
            real_kb_id,
            data.question
        )

        if cached_result:
            print("REDIS CACHE HIT")
            result = cached_result

        else:
            print("REDIS CACHE MISS")

            result = ask_question(
                data.question,
                real_kb_id
            )

            save_answer_to_cache(
                real_kb_id,
                data.question,
                result
            )

        (
            supabase
            .table("messages")
            .insert([
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
            ])
            .execute()
        )

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

        (
            supabase
            .table("knowledge_bases")
            .delete()
            .eq("kb_id", kb_id)
            .execute()
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

    result = (
        supabase
        .table("chat_sessions")
        .insert({
            "user_id": data.user_id,
            "kb_id": data.kb_id,
            "title": data.title
        })
        .execute()
    )

    return result.data[0]


@app.get("/chat-sessions/{user_id}")
def get_chats(user_id: str):

    result = (
        supabase
        .table("chat_sessions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    print("\nCHAT SESSIONS:")
    print(result.data)

    return result.data


@app.get("/messages/{chat_id}")
def get_messages(chat_id: str):

    result = (
        supabase
        .table("messages")
        .select("*")
        .eq("chat_id", chat_id)
        .order("created_at")
        .execute()
    )

    return result.data


@app.get("/")
def root():

    return {
        "message": "RAG Website Chatbot Backend Running"
    }