#  GitHub Repository Explainer (RAG)

An AI-powered application that lets you chat with any public GitHub repository. It uses **Retrieval-Augmented Generation (RAG)** to understand the repository's source code and answer repository-specific questions with source references.

## Features

* Clone and index public GitHub repositories
* Semantic code chunking using Tree-sitter
* Recursive chunking for text files
* Vector search with Qdrant
* Repository-aware Q&A using Google Gemini
* Conversation memory
* Streamlit frontend + FastAPI backend

## Tech Stack

* Python
* FastAPI
* Streamlit
* LangChain
* Qdrant
* Tree-sitter
* Google Gemini

## 📂 Project Workflow

```text
GitHub Repository
        │
        ▼
 Clone Repository
        │
        ▼
 Parse Source Files
        │
        ▼
 Semantic Chunking
        │
        ▼
 Generate Embeddings
        │
        ▼
   Qdrant Vector DB
        │
        ▼
     Retriever
        │
        ▼
      Gemini LLM
        │
        ▼
      Final Answer
```

## Installation

Clone the repository:

```bash
git clone https://github.com/JanishLathwal/Github-Repo-Explainer-Rag.git
cd Github-Repo-Explainer-Rag
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the backend:

```bash
cd backend
uvicorn main:app --reload
```

Run the frontend:

```bash
cd frontend
streamlit run app.py
```

## Future Improvements

* Support for `.ipynb` files
* Hybrid Search
* Reranking
* Multi-repository indexing
* Docker support

## Author

**Janish Lathwal**

