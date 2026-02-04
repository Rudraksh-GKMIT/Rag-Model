from sentence_transformers import SentenceTransformer
from src.llm.rag.constant import RAGConstant

_embedding_model = None

def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            RAGConstant.EMBEDDING_MODEL_NAME
        )
    return _embedding_model
