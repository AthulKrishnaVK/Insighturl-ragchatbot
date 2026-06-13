from sentence_transformers import SentenceTransformer
from database.supabase_client import supabase

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def generate_embedding(text):
    return model.encode(text).tolist()


def store_chunks(kb_id, chunks):
    rows = []

    for chunk in chunks:
        rows.append({
            "kb_id": kb_id,
            "url": chunk.metadata.get("source", ""),
            "content": chunk.page_content,
            "embedding": generate_embedding(
                chunk.page_content
            )
        })

    if rows:
        supabase.table(
            "website_chunks"
        ).insert(rows).execute()

    return len(rows)


def search_chunks(question, kb_id, k=3):
    query_embedding = generate_embedding(question)

    result = supabase.rpc(
        "match_website_chunks",
        {
            "query_embedding": query_embedding,
            "match_kb_id": kb_id,
            "match_count": k
        }
    ).execute()

    return result.data