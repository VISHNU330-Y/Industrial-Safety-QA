import os
import json
import sqlite3
import pdfplumber
from tqdm import tqdm
import zipfile

# 📦 Unzip PDFs if not already extracted
zip_path = "industrial-safety-pdfs.zip"
pdf_dir = "pdfs"

if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(pdf_dir)
    print(f"✅ Extracted ZIP to '{pdf_dir}'")

# 📄 Load sources.json
# 📄 Load sources.json
with open("sources.json", "r", encoding="utf-8") as f:
    raw_sources = json.load(f)

# Match each entry to a PDF filename by order
pdf_filenames = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])
sources = {}

for i, entry in enumerate(raw_sources):
    if i < len(pdf_filenames):
        sources[pdf_filenames[i]] = {
            "title": entry.get("title", pdf_filenames[i]),
            "url": entry.get("url", "")
        }
# 🗃️ Connect to SQLite
conn = sqlite3.connect("chunks.db")
cur = conn.cursor()

# 🧱 Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id TEXT,
    chunk TEXT,
    title TEXT,
    url TEXT
);
""")

# ✂️ Chunking function
def chunk_text(text, min_len=200):
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 0]
    chunks = []
    buffer = ""
    for p in paragraphs:
        buffer += " " + p
        if len(buffer) > min_len:
            chunks.append(buffer.strip())
            buffer = ""
    if buffer:
        chunks.append(buffer.strip())
    return chunks

# 📚 Process PDFs
total_chunks = 0
empty_files = []

for filename in tqdm(os.listdir(pdf_dir)):
    if not filename.endswith(".pdf"):
        continue

    path = os.path.join(pdf_dir, filename)
    doc_id = filename
    meta = sources.get(filename, {"title": filename, "url": ""})

    try:
        with pdfplumber.open(path) as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            if not full_text.strip():
                empty_files.append(filename)
                print(f"⚠️ Skipped empty PDF: {filename}")
                continue

            chunks = chunk_text(full_text)
            for chunk in chunks:
                cur.execute("""
                INSERT INTO chunks (doc_id, chunk, title, url)
                VALUES (?, ?, ?, ?)
                """, (doc_id, chunk, meta["title"], meta["url"]))
            print(f"✅ {filename}: {len(chunks)} chunks inserted")
            total_chunks += len(chunks)

    except Exception as e:
        print(f"❌ Failed to process {filename}: {e}")

conn.commit()
conn.close()

# 📊 Summary
print(f"\n✅ Chunking complete. Total chunks stored: {total_chunks}")
if empty_files:
    print(f"⚠️ Skipped {len(empty_files)} empty PDFs:")
    for f in empty_files:
        print(f"  - {f}")