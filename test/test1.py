from src.llm.rag.retrieval.search import Retriever
retriever = Retriever()

docs = retriever.hybrid_search(
    query="What is LAN?",
    alpha=0.5,
    limit=5
)

print(f"Retrieved {len(docs)} documents")
for d in docs:
    print("-" * 50)
    print(d["score"])
    print(d["text"])
