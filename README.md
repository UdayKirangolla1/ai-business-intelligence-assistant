# AI Business Intelligence Assistant

A RAG (Retrieval-Augmented Generation) application that lets you upload business documents and ask natural language questions about them. Built with LangChain, ChromaDB, HuggingFace embeddings, and Claude AI.

---

## How It Works

```
Upload Document → Chunk → Embed → Store in ChromaDB
                                        ↓
User Question → Embed Query → Retrieve Top Chunks → Claude Synthesizes Answer
```

1. **Document Loading** — Supports PDF, DOCX, and TXT via format-aware loaders
2. **Chunking** — Splits documents into 800-character chunks with 150-character overlap
3. **Embedding** — Uses `sentence-transformers/all-MiniLM-L6-v2` locally (no API cost)
4. **Vector Store** — ChromaDB stores and retrieves embeddings by cosine similarity
5. **Answer Generation** — Claude reads the retrieved chunks and synthesizes a cited answer

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get an Anthropic API key
Sign up at [console.anthropic.com](https://console.anthropic.com) and create an API key.

### 4. Run the app
```bash
streamlit run app.py
```

Enter your Anthropic API key in the sidebar when the app opens.

---

## Project Structure

```
├── app.py                  # Streamlit UI
├── requirements.txt
├── src/
│   ├── document_loader.py  # PDF / DOCX / TXT loading
│   ├── text_splitter.py    # Recursive character splitting
│   ├── embeddings.py       # HuggingFace embeddings
│   ├── vector_store.py     # ChromaDB vector store
│   ├── retriever.py        # Similarity retriever
│   └── rag_chain.py        # Claude answer generation
└── data/
    ├── customer_feedback.txt
    ├── refund_policy.txt
    └── sales_report_q1.txt
```

---

## Sample Questions to Try

Upload `refund_policy.txt` and ask:
- "What is the refund policy for premium customers?"
- "How long does a standard refund take?"
- "Can I get a refund on a digital product?"

Upload `sales_report_q1.txt` and ask:
- "Which region had the worst sales performance?"
- "What was the best performing product category?"

---

## Tech Stack

| Component | Choice | Reason |
|---|---|---|
| UI | Streamlit | Fast to build, easy to demo |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | Free, runs locally |
| Vector Store | ChromaDB | Simple, persists to disk |
| LLM | Claude (claude-sonnet-4-20250514) | Strong instruction following, cited answers |
| Orchestration | LangChain | Modular loader/splitter abstractions |