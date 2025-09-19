import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to DB
conn = sqlite3.connect("chunks.db")
cur = conn.cursor()

# Load chunks
cur.execute("SELECT id, chunk FROM chunks")
rows = cur.fetchall()

# Embed chunks
ids = []
vectors = []
for chunk_id, text in rows:
    embedding = model.encode(text, normalize_embeddings=True)
    ids.append(chunk_id)
    vectors.append(embedding)

# Convert to numpy
vectors_np = np.vstack(vectors).astype("float32")

# Build FAISS index
index = faiss.IndexFlatIP(vectors_np.shape[1])  # Cosine similarity
index.add(vectors_np)

# Save index + ID mapping
faiss.write_index(index, "faiss.index")
with open("id_map.pkl", "wb") as f:
    pickle.dump(ids, f)

print(f"Indexed {len(ids)} chunks.")