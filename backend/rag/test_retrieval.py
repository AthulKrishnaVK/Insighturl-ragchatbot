from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma

# from langchain_google_genai import (
#     GoogleGenerativeAIEmbeddings
# )
from langchain_community.embeddings import HuggingFaceEmbeddings
load_dotenv()

#create embeddings
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/text-embedding-004"
# )
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
#connect to chromadb
db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)
#query
results = db.similarity_search(
    "What is this website about?",
    k=3
)
for r in results:

    print("\nSOURCE:")
    print(r.metadata)

    print("\nTEXT:")
    print(r.page_content[:500])