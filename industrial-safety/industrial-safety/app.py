from flask import Flask, request, jsonify, render_template
from search_and_rerank import search

app = Flask(__name__)

# 🌐 Frontend route
@app.route("/")
def home():
    return render_template("index.html")

# 🧠 API route
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)
        q = data.get("q", "").strip()
        print(f"\n🔍 Incoming query: {q}")  # Add this
        k = int(data.get("k", 5))
        mode = data.get("mode", "hybrid")

        answer, contexts, reranker_used = search(q, k=k, mode=mode)

        return jsonify({
            "answer": answer,
            "contexts": [
                {
                    "chunk": c["chunk"],
                    "title": c["title"],
                    "url": c["url"],
                    "score": round(c.get("hybrid_score", c["vector_score"]), 3)
                } for c in contexts
            ],
            "reranker_used": reranker_used
        })

    except Exception as e:
        print(f"❌ Error: {e}")  # Add this
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)