# from sentence_transformers import SentenceTransformer
# from database.supabase_client import supabase

# model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )


# def generate_embedding(text):
#     return model.encode(text).tolist()


# def store_chunks(kb_id, chunks):
#     rows = []

#     for chunk in chunks:
#         rows.append({
#             "kb_id": kb_id,
#             "url": chunk.metadata.get("source", ""),
#             "content": chunk.page_content,
#             "embedding": generate_embedding(
#                 chunk.page_content
#             )
#         })

#     if rows:
#         supabase.table(
#             "website_chunks"
#         ).insert(rows).execute()

#     return len(rows)


# def search_chunks(question, kb_id, k=3):
#     query_embedding = generate_embedding(question)

#     result = supabase.rpc(
#         "match_website_chunks",
#         {
#             "query_embedding": query_embedding,
#             "match_kb_id": kb_id,
#             "match_count": k
#         }
#     ).execute()

#     return result.data


# from sentence_transformers import SentenceTransformer
# from database.supabase_client import supabase

# model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )


# def generate_embedding(text):
#     return model.encode(text).tolist()


# def insert_in_batches(rows, batch_size=20):
#     total_inserted = 0

#     for i in range(0, len(rows), batch_size):
#         batch = rows[i:i + batch_size]

#         supabase.table(
#             "website_chunks"
#         ).insert(batch).execute()

#         total_inserted += len(batch)

#         print(
#             f"Inserted {total_inserted}/{len(rows)} chunks"
#         )

#     return total_inserted


# def store_chunks(kb_id, chunks):
#     rows = []

#     for chunk in chunks:
#         source_url = (
#             chunk.metadata.get("source")
#             or chunk.metadata.get("url")
#             or ""
#         )
#         clean_text = (
#         chunk.page_content
#         .replace("\x00", "")
#         .replace("\u0000", "")
#         )

#         rows.append({
#             "kb_id": kb_id,
#             "url": source_url,
#             "content": clean_text,
#             "embedding": generate_embedding(
#                 chunk.page_content
#             )
#         })

#     if rows:
#         insert_in_batches(
#             rows,
#             batch_size=20
#         )

#     return len(rows)


# def search_chunks(question, kb_id, k=3):
#     query_embedding = generate_embedding(question)

#     result = supabase.rpc(
#         "match_website_chunks",
#         {
#             "query_embedding": query_embedding,
#             "match_kb_id": kb_id,
#             "match_count": k
#         }
#     ).execute()

#     return result.data


from sentence_transformers import SentenceTransformer
from database.supabase_client import supabase

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def clean_text(text):
    if not text:
        return ""

    return (
        text.replace("\x00", "")
        .replace("\u0000", "")
        .strip()
    )


def generate_embedding(text):
    text = clean_text(text)
    return model.encode(text).tolist()


def insert_in_batches(rows, batch_size=20):
    total_inserted = 0

    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]

        supabase.table(
            "website_chunks"
        ).insert(batch).execute()

        total_inserted += len(batch)

        print(
            f"Inserted {total_inserted}/{len(rows)} chunks"
        )

    return total_inserted


def store_chunks(kb_id, chunks):
    rows = []

    for chunk in chunks:
        source_url = (
            chunk.metadata.get("source")
            or chunk.metadata.get("url")
            or ""
        )

        text = clean_text(
            chunk.page_content
        )

        if not text:
            continue

        rows.append({
            "kb_id": kb_id,
            "url": source_url,
            "content": text[:3000],
            "embedding": generate_embedding(text)
        })

    if rows:
        insert_in_batches(
            rows,
            batch_size=20
        )

    return len(rows)


def search_chunks(question, kb_id, k=3):
    query_embedding = generate_embedding(
        question
    )

    result = supabase.rpc(
        "match_website_chunks",
        {
            "query_embedding": query_embedding,
            "match_kb_id": kb_id,
            "match_count": k
        }
    ).execute()

    return result.data