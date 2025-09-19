from search_and_rerank import search
import json

# 🧪 Evaluation questions
questions = [
    "What is lockout/tagout procedure?",
    "What PPE is required for industrial safety?",
    "What are common machine guarding methods?",
    "What is EN ISO 13849-1?",
    "What are the six steps to a safe machine?",
    "How does OSHA define amputation hazards?",
    "What is SISTEMA used for?",
    "What are pneumatic safety solutions?"
]

# 📊 Print table header
print(f"{'Question':<50} | {'Answered':<8} | {'Top Score':<9} | {'Abstained'}")
print("-" * 80)

results = []

# 🔁 Run each query
for q in questions:
    answer, contexts, reranker_used = search(q, k=5, mode="hybrid")
    top_score = contexts[0].get("hybrid_score", contexts[0]["vector_score"]) if contexts else 0
    abstained = answer is None

    print(f"{q[:50]:<50} | {'Yes' if answer else 'No':<8} | {top_score:.3f}     | {'Yes' if abstained else 'No'}")

    results.append({
        "question": q,
        "answer": answer,
        "reranker": reranker_used,
        "top_score": round(top_score, 3),
        "abstained": abstained,
        "contexts": [
            {
                "chunk": c["chunk"],
                "title": c["title"],
                "url": c["url"],
                "score": round(c.get("hybrid_score", c["vector_score"]), 3)
            } for c in contexts
        ]
    })

# 📝 Save to JSON
with open("evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n✅ Evaluation complete. Results saved to evaluation_results.json")