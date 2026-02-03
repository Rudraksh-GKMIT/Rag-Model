from typing import List
from openai import OpenAI

from src.llm.rag.config import RAGConfig

TEMPERATURE = 0.5
MODEL = "gpt-4.1-mini"

client = OpenAI(api_key=RAGConfig.OPENAI_API_KEY)

prompt = """
    You are a helpful assistant.
    Answer the question ONLY using the context below.
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
            model=MODEL,
            temperature=TEMPERATURE,
            input=prompt.format(
                context= context,
                query=query
            ),
        )
        return response.output_text.strip()

    except Exception as e:
        return query
