from typing import List
from src.backend.weaviate_I.client import get_client
from src.llm.rag.embeddings.model import get_embedding_model


class Retriever:
    def __init__(self):
        self.client = get_client()
        self.collection = self.client.collections.get("DocumentChunk")
        self.embedder = get_embedding_model()  # SentenceTransformer
    
    def close(self):
        if self.client:
            self.client.close()

    def vector_search(
        self,
        query: str,
        limit: int = 5
    ) -> List[dict]:
        """
        Pure vector (semantic) search
        """
        query_vector = self.embedder.encode(
            [query],
            normalize_embeddings=True
        )[0].tolist()

        response = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            return_properties=["chunk_text", "document_id", "chunk_index"]
        )

        return [
            {
                "text": obj.properties["chunk_text"],
                "source": obj.properties["document_id"],
                "chunk_index": obj.properties["chunk_index"],
                "distance": obj.metadata.distance
            }
            for obj in response.objects
        ]

    def hybrid_search(
        self,
        query: str,
        alpha: float = 0.5,
        limit: int = 10,
        vector_text: str | None = None, 
    ) -> List[dict]:
        """
        Hybrid search: vector + BM25 (manual vector)
        """
        text_to_embed = vector_text or query
        query_vector = self.embedder.encode(
            [text_to_embed],
            normalize_embeddings=True
        )[0].tolist()

        response = self.collection.query.hybrid(
            query=query,
            vector=query_vector,  
            alpha=alpha,
            limit=limit,
            return_properties=["chunk_text", "document_id", "chunk_index"]
        )

        return [
            {
                "text": obj.properties["chunk_text"],
                "source": obj.properties["document_id"],
                "chunk_index": obj.properties["chunk_index"],
                "score":  (
                    obj.metadata.score
                    if obj.metadata.score is not None
                    else obj.metadata.distance
                )

            }
            for obj in response.objects
        ]

