# InsightURL – RAG Powered Website Chatbot

## Overview

InsightURL is a Retrieval-Augmented Generation (RAG) based chatbot that can ingest any website URL, recursively crawl pages within the same domain, extract relevant content, and answer user questions based on the collected information.

The project combines web crawling, semantic search, vector embeddings, and Large Language Models to create a context-aware chatbot capable of understanding website content and providing accurate responses.

In addition to the core RAG pipeline, the project includes user authentication, chat session management, multiple knowledge bases, and a modern React frontend.

---

## Features

### Website Ingestion

* Accepts any website URL as input
* Recursively crawls linked pages within the same domain
* Extracts content from:

  * Headings
  * Paragraphs
  * Lists
  * Tables
* Removes irrelevant elements such as navigation bars, scripts, and footers

### RAG Pipeline

* Splits extracted content into manageable chunks
* Generates embeddings using Hugging Face Sentence Transformers
* Stores embeddings in ChromaDB
* Retrieves relevant chunks using semantic similarity search
* Uses Groq to generate context-aware answers

### Chat System

* Multiple chat sessions
* Separate knowledge bases per website
* Website-specific conversations
* Persistent chat history
* Markdown response rendering

### Authentication

* User login and signup
* Supabase authentication
* Secure session management

### User Interface

* Modern React + Vite frontend
* Sidebar-based chat navigation
* Dynamic knowledge base selection
* Responsive design

---

## Project Architecture

```text
User URL
    ↓
Website Crawler
    ↓
Content Extraction
    ↓
Chunking
    ↓
Embeddings (all-MiniLM-L6-v2)
    ↓
ChromaDB Vector Store
    ↓
Retriever
    ↓
Groq LLM
    ↓
Chat Response
```

---

## Tech Stack

### Frontend

* React
* Vite
* React Markdown
* CSS

### Backend

* FastAPI
* LangChain
* BeautifulSoup
* Requests
* ChromaDB

### AI & RAG

* Groq
* Hugging Face Embeddings
* Sentence Transformers
* LangChain Retrieval

### Database & Authentication

* Supabase

---

## Project Structure

```text
InsightURL/
│
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   └── auth.py
│   │
│   ├── crawler/
│   │   ├── crawler.py
│   │   └── scraper.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── chatbot.py
│   │   └── test_retrieval.py
│   │
│   ├── database/
│   │   └── supabase_client.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── context/
│   │
│   └── package.json
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/AthulKrishnaVK/Insighturl-ragchatbot.git

cd Insighturl-ragchatbot
```

---

## Backend Setup

Navigate to backend:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key

SUPABASE_URL=your_supabase_url

SUPABASE_KEY=your_supabase_key
```

Start backend:

```bash
uvicorn api.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

---

## Frontend Setup

Navigate to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create environment file:

```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

Start frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## How To Use

1. Login or create an account.
2. Paste a website URL.
3. Click **Ingest**.
4. Wait for crawling and indexing to finish.
5. Select the created chat session.
6. Ask questions about the website.
7. Receive answers generated using retrieved website content.

---

## Example Workflow

```text
https://fastapi.tiangolo.com
          ↓
 Crawl Website
          ↓
 Extract Content
          ↓
 Create Embeddings
          ↓
 Store in ChromaDB
          ↓
 Ask Question:
 "What is FastAPI?"
          ↓
 Retrieve Relevant Chunks
          ↓
 Gemini Generates Answer
```

---

## Current Capabilities

* Website crawling
* Same-domain recursive scraping
* Structured content extraction
* Semantic retrieval
* Multi-session chat management
* Authentication
* Knowledge base isolation

---

## Future Improvements

* PDF ingestion support
* Image understanding
* Advanced reranking
* Streaming responses
* Supabase Vector integration
* Production deployment
* Multi-language support

---

## Author

Athul Krishna

B.Tech Computer Science & Engineering

AI / Machine Learning Enthusiast

---

## License

This project is developed for learning, research, and educational purposes.
