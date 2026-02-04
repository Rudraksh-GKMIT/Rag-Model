from typing import List
from openai import OpenAI

from src.llm.rag.config import RAGConfig
from src.llm.rag.constants import RagConstants

client = OpenAI(api_key=RAGConfig.OPENAI_API_KEY)

prompt = """
    You are a helpful assistant.
    Answer the question ONLY using the context below.
    Answer in an explanatory manner.
    If the answer is not present, say:
    "I don't know based on the provided documents."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """


def generate_answer(
    query: str,
    chunks: List[dict]
) -> str:
    """
    Generate a grounded answer using retrieved context.
    """
    context = "\n\n".join(
        f"[{i+1}] {c['text']}"
        for i, c in enumerate(chunks)
    )
    try:
        response = client.responses.create(
            model=RagConstants.MODEL,
            temperature=RagConstants.TEMPERATURE,
            input=prompt.format(
                context= context,
                query=query
            ),
        )
        return response.output_text.strip()

    except Exception as e:
        return query
