from app.rag_handler import RAGKnowledgeBase

rag = RAGKnowledgeBase('config/knowledge.json')

test_queries = [
    "cong ty ACN",
    "ACN cao bao nhieu"
]

for q in test_queries:
    print(f"\n=== {q} ===")
    results = rag.search(q, top_k=3)
    for r in results:
        print(f"{r['entry_key']}: score={r['score']}, keywords={r['matched_keywords'][:2]}")
