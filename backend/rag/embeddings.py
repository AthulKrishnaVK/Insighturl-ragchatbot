


# import json
# import shutil
# import os
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_core.documents import Document


# def create_vector_db(kb_id):

#     with open(
#         f"backend/data/website_content_{kb_id}.json",
#         "r",
#         encoding="utf-8"
#     ) as f:

#         pages = json.load(f)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200
#     )

#     documents = []

#     for page in pages:

#         text = page.get("text", "").strip()

#         if not text:
#             continue

#         chunks = splitter.split_text(text)

#         for chunk in chunks:

#             if chunk.strip():

#                 documents.append(
#                     Document(
#                         page_content=chunk,
#                         metadata={
#                             "source": page["url"]
#                         }
#                     )
#                 )

#     print("Pages:", len(pages))
#     print("Documents:", len(documents))

#     if len(documents) == 0:
#         raise Exception("No valid documents found after chunking.")
#     db_path = f"chroma_db_{kb_id}" 
#     if os.path.exists(db_path):
#          shutil.rmtree(db_path)

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     Chroma.from_documents(
#         documents=documents,
#         embedding=embeddings,
#         persist_directory=f"chroma_db{kb_id}"
#     )

#     print(f"Created DB {kb_id} with {len(documents)} chunks")

#     return len(pages), len(documents)



import json
import shutil
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


def create_vector_db(kb_id):

    file_path = f"backend/data/website_content_{kb_id}.json"

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        pages = json.load(f)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    documents = []

    for page in pages:

        text = page.get("text", "").strip()

        if not text:
            continue

        chunks = splitter.split_text(text)

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": page["url"]
                    }
                )
            )

    print("Pages:", len(pages))
    print("Chunks:", len(documents))

    if len(documents) == 0:
        raise Exception(
            "No valid documents found."
        )

    db_path = f"backend/chroma_db_{kb_id}"

    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=db_path
    )

    print(
        f"Created DB {kb_id} with {len(documents)} chunks"
    )

    return len(pages), len(documents)