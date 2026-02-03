import cohere
from typing import List

class CohereReranker:
    def __init__(
        self,
        model: str = "rerank-english-v3.0"
    ):
        self.client = cohere.Client(api_key="2xx2tynNvvGHI6fDSLj23L2vScASfYq0pYAh0dWc")
        self.model = model

    def rerank(
        self,
        query: str,
        documents: List[dict],
        top_k: int = 5
    ) -> List[dict]:
        """
        documents: List[{text, source, chunk_id, score}]
        """

        texts = [doc["text"] for doc in documents]

        response = self.client.rerank(
            model=self.model,
            query=query,
            documents=texts,
            top_n=top_k
        )

        reranked_docs = []
        for r in response.results:
            doc = documents[r.index]
            doc["rerank_score"] = float(r.relevance_score)
            reranked_docs.append(doc)

        return reranked_docs
