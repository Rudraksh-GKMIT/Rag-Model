from src.llm.rag.retrieval.search import Retriever
from src.llm.rag.retrieval.rerank import CohereReranker
from src.llm.rag.hyde import expand_query
from src.llm.rag.generation.llm_answer import generate_answer


query = "What is LAN?"

retriever = Retriever()
reranker = CohereReranker()

hyde_text = expand_query(query)

docs = retriever.hybrid_search(
    query=query,
    vector_text=hyde_text, 
    alpha=0.5,
    limit=20
)

reranked = reranker.rerank(
    query=query,
    documents=docs,
    top_k=5,
)

answer = generate_answer(
    query=query,
    chunks=reranked,
)

print("\nFINAL ANSWER:\n", answer)