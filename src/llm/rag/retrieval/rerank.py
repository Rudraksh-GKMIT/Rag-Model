import cohere
from typing import List
from src.llm.rag.config import RAGConfig
from src.llm.rag.constant import RAGConstant


class CohereReranker:
    def __init__(
        self,
        model: str = RAGConstant.COHERE_RERANK_MODEL
    ):
        self.client = cohere.Client(api_key=RAGConfig.COHERE_API_KEY)
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
