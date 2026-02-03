from src.llm.rag.retrieval.rerank import CohereReranker
import weaviate
from src.llm.rag.retrieval.search import Retriever

retriever = Retriever()
reranker = CohereReranker()
query = "What is LAN?"
query_vector = retriever.embedder.encode(
    [query],
    normalize_embeddings=True
)[0].tolist()
with weaviate.connect_to_local() as client:
    collection = client.collections.get("DocumentChunk")

    response = collection.query.hybrid(
        query=query,
        vector=query_vector,  
        alpha=0.5,
        limit=5,
        return_properties=["chunk_text"]
    )

    for obj in response.objects:
        print("-" * 50)
        print(obj.properties["chunk_text"][:200])

    # response = collection.query.bm25(
    #     query="Local Area Network",
    #     limit=5,
    #     return_properties=["chunk_text", "document_id", "chunk_index"]
    # )

    # for obj in response.objects:
    #     print("-" * 50)
    #     print(obj.properties["chunk_text"][:200])

    # query_vector = retriever.embedder.encode(
    #     ["What is LAN?"], normalize_embeddings=True
    # )[0].tolist()

    # response = collection.query.near_vector(
    #     near_vector=query_vector,
    #     limit=5,
    #     return_properties=["chunk_text"]
    # )

    # for obj in response.objects:
    #     print("-" * 50)
    #     print(obj.properties["chunk_text"][:200])


