


from dotenv import load_dotenv
import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

# ==========================================
# Embeddings
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# LLM
# ==========================================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# ==========================================
# Retriever
# ==========================================

def get_retriever(kb_id):

    db_path = f"backend/chroma_db_{kb_id}"

    db = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )

    return db.as_retriever(
        search_kwargs={"k": 8}
    )

# ==========================================
# Chat Function
# ==========================================

def ask_question(question, kb_id):

    try:

        retriever = get_retriever(kb_id)

        docs = retriever.invoke(question)

        print("=" * 60)
        print("KB ID:", kb_id)
        print("QUESTION:", question)
        print("DOCS FOUND:", len(docs))
        print("=" * 60)

        if len(docs) == 0:

            return {
                "answer": """
# ❌ No Information Found

I could not find any relevant information in the selected website.

Try:
- Rephrasing the question
- Ingesting more pages
- Selecting another website
""",
                "sources": []
            }

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are ChatGPT answering questions using retrieved website content.

Rules:

1. Answer ONLY from the context provided.
2. Never invent facts.
3. If information is missing, clearly say so.
4. Choose the best format automatically:
   - paragraphs
   - bullets
   - tables
   - numbered lists
5. Keep responses clear and visually organized.
6. Avoid unnecessary headings.
7. Prioritize readability and usefulness.

Context:
{context}

User Question:
{question}
"""

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": list(
                set(
                    [
                        doc.metadata.get(
                            "source",
                            "Unknown Source"
                        )
                        for doc in docs
                    ]
                )
            )
        }

    except Exception as e:

        print("LLM ERROR:", str(e))

        return {
            "answer": f"""
# ⚠️ System Error

The chatbot encountered an error.

### Details

{str(e)}
""",
            "sources": []
        }