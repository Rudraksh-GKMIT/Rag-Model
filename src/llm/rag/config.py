import os
from dotenv import load_dotenv

load_dotenv()


class RAGConfig:
    LOG_LEVEL=os.getenv("LOG_LEVEL")
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DOCUMENT_COLLECTION = os.getenv("DOCUMENT_COLLECTION")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")