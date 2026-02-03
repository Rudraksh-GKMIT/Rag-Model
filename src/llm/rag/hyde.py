from openai import OpenAI

from src.llm.rag.config import RAGConfig

TEMPERATURE = 0.5
MODEL = "gpt-4.1-mini"

QUERY_EXPANDER_PROMPT = """
You are a query expansion utility.
Your task is to expand the given research query into a richer,
search-oriented query with additional context.
Query:
{query}


Generate a concise hypothetical answer.
"""

client = OpenAI(api_key=RAGConfig.OPENAI_API_KEY)


def expand_query(query: str) -> str:
    """
    Expands a base query using a single LLM call to provide richer context.
    This is a stateless utility function, not an agent.
    """
    try:
        response = client.responses.create(
            model=MODEL,
            temperature=TEMPERATURE,
            input=QUERY_EXPANDER_PROMPT.format(
                query=query
            ),
        )

        return response.output_text.strip()

    except Exception as e:
        return query
