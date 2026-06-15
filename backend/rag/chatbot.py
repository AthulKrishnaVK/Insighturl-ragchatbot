from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from rag.supabase_vector import search_chunks
import time
load_dotenv()



llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)



def ask_question(question, kb_id):

    try:
        docs = search_chunks(
            question=question,
            kb_id=kb_id,
            k=8
        )

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
            [doc["content"] for doc in docs]
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
                        doc.get("url", "Unknown Source")
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