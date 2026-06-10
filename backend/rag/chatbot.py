
# # from dotenv import load_dotenv

# # from langchain_community.vectorstores import Chroma

# # from langchain_community.embeddings import HuggingFaceEmbeddings

# # from langchain_google_genai import ChatGoogleGenerativeAI
# # import os
# # import json
# # load_dotenv()

# # embeddings = HuggingFaceEmbeddings(
# #     model_name="sentence-transformers/all-MiniLM-L6-v2"
# # )





# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-2.5-flash",
# #     google_api_key=os.getenv("GOOGLE_API_KEY"),
# #     temperature=0
# # )
# # def get_retriever(kb_id):

# #     db = Chroma(
# #         persist_directory=f"chroma_db{kb_id}",
# #         embedding_function=embeddings
# #     )

# #     return db.as_retriever(
# #         search_kwargs={"k":3}
# #     )



# # def ask_question(question, kb_id):
# #     retriever = get_retriever(kb_id)

# #     docs = retriever.invoke(question)
    
# #     print("================================")
# #     print("KB:", kb_id)
# #     print("DOCS FOUND:", len(docs))

# #     for i, doc in enumerate(docs):
# #         print(f"DOC {i+1}:")
# #         print(doc.metadata)
# #         print(doc.page_content[:200])
# #         print("----------------")
# #     context = "\n\n".join(
# #         [doc.page_content for doc in docs]
# #     )

# #     prompt = f"""
# # Answer ONLY from the provided context.

# # Context:
# # {context}

# # Question:
# # {question}

# # Answer:
# # """

# #     response = llm.invoke(prompt)

# #     return {
# #         "answer": response.content,
# #         "sources": list( set(
# #              [
# #                  doc.metadata["source"]
# #                  for doc in docs 
# #                  ] ) ) }


# from dotenv import load_dotenv

# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# # from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
# import os

# load_dotenv()

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-2.5-flash",
# #     google_api_key=os.getenv("GOOGLE_API_KEY"),
# #     temperature=0
# # )
# llm = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"),
#     model_name="llama-3.3-70b-versatile",
#     temperature=0
# )


# def get_retriever(kb_id):

#     db_path = f"backend/chroma_db_{kb_id}"

#     db = Chroma(
#         persist_directory=db_path,
#         embedding_function=embeddings
#     )

#     return db.as_retriever(
#         search_kwargs={"k": 5}
#     )


# def ask_question(question, kb_id):

#     retriever = get_retriever(kb_id)

#     docs = retriever.invoke(question)

#     print("=" * 50)
#     print("KB:", kb_id)
#     print("DOCS FOUND:", len(docs))

#     if len(docs) == 0:

#         return {
#             "answer": "No relevant information found in this website.",
#             "sources": []
#         }

#     context = "\n\n".join(
#         [doc.page_content for doc in docs]
#     )
# prompt = f"""
#                     You are an intelligent RAG assistant.

# Rules:
# 1. Answer ONLY using the provided context.
# 2. If the answer is not in the context, say:
#    "I could not find this information in the selected website."
# 3. Format responses professionally using Markdown.

# Response Format:

# # Answer
# Provide a direct answer.

# ## Key Points
# - Point 1
# - Point 2
# - Point 3

# ## Details
# Provide explanation in paragraphs.

# ## Sources Used
# List source URLs if available.

# Context:
# {context}

# Question:
# {question}
# """
# #     prompt = f"""
# # Answer ONLY from the provided context.

# # Context:
# # {context}

# # Question:
# # {question}

# # Answer:
# # """

#     try:

#         response = llm.invoke(prompt)

#         return {
#             "answer": response.content,
#             "sources": list(
#                 set(
#                     [
#                         doc.metadata["source"]
#                         for doc in docs
#                     ]
#                 )
#             )
#         }

#     except Exception as e:
#         print("llm error:",e)
#         return {
#             "answer": f"LLM Error: {str(e)}",
#             "sources": []
#         }




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