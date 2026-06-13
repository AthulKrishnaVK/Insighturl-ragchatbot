import json

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from rag.supabase_vector import store_chunks


def create_vector_db(kb_id):

    file_path = (
        f"backend/data/"
        f"website_content_{kb_id}.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        pages = json.load(f)

    documents = []

    for page in pages:

        text = (
            page.get("content")
            or page.get("text")
            or ""
        ).strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": page.get("url", "")
                }
            )
        )

    if len(documents) == 0:
        raise Exception(
            "No valid website content found."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    chunk_count = store_chunks(
        kb_id,
        chunks
    )

    print("Pages Loaded:", len(pages))
    print("Chunks Created:", chunk_count)
    print("Stored in Supabase Vector DB")

    return len(pages), chunk_count