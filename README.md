# Industrial Safety QA System

This project builds a modular AI-powered question answering system using 20 public PDFs on industrial and machine safety. It supports semantic search, hybrid reranking, and extractive answers with citations.

##  Setup

1. Clone the repo and unzip `industrial-safety-pdfs.zip` into a `pdfs/` folder.
2. Run `chunk_and_store.py` to extract and chunk text into SQLite.
3. Run `embed_and_index.py` to embed chunks and build FAISS index.
4. Start the API with `python app.py` and visit `http://127.0.0.1:5000/`.

##  How It Works

- Uses `all-MiniLM-L6-v2` for semantic embeddings.
- FAISS retrieves top-k chunks by cosine similarity.
- Hybrid reranker blends vector score with keyword match via SQLite FTS.
- Answers are extracted from top chunk if score ≥ 0.3, else system abstains.

##  Evaluation

Run `evaluate.py` to test 8 safety questions. Results are saved to `evaluation_results.json`.

| Question | Answered | Top Score | Abstained |
|----------|----------|-----------|-----------|
| What is lockout/tagout procedure? | ✅ | 0.519 | ❌ |
| ... | ... | ... | ... |

##  What I Learned

This project taught me how to build a full-stack AI retrieval system from scratch — from ingesting raw PDFs to serving answers via a web API. I learned how to balance semantic and keyword signals, handle low-confidence queries, and design a frontend that’s both functional and demo-ready. Most importantly, I saw how modular design and robust error handling make debugging and iteration far easier.
## Project Demonstration:** A walkthrough of the system's features and architecture is available in this [demo video](https://youtu.be/3INHhsTghiY).
