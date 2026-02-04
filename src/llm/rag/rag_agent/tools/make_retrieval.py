from src.llm.agent_core.tool import Tool
from src.llm.rag.retrieval.search import Retriever
from src.llm.agent_core.args_schema import ArgsSchema as Args
from src.llm.rag.retrieval.rerank import CohereReranker


class GetRetrieval:
    args = [
        (
            "query",
            Args(type=str, description="modified user query", required=True),
        )
    ]


def make_retrieval():
    def get_retrieval(query: str):
        retriever = Retriever()
        try:
            docs = retriever.hybrid_search(query=query, alpha=0.5, limit=20)

            reranker = CohereReranker()
            reranked = reranker.rerank(
                query=query,
                documents=docs,
                top_k=5,
            )
            return reranked

        except Exception as e:
            raise RuntimeError(f"Failed to load the chapter {e}")

        finally:
            reranker.close()
            retriever.close()

    return Tool(
        func=get_retrieval,
        description="Fetch the related document",
        args_schema=GetRetrieval,
    )
