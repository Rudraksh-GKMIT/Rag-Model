import os
from dotenv import load_dotenv

load_dotenv()


class RAGConfig:
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")