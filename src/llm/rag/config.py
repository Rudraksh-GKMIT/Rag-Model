import os
from dotenv import load_dotenv

load_dotenv()


class RAGConfig:
    LOG_LEVEL=os.getenv("LOG_LEVEL")
    DOCUMENT_COLLECTION = os.getenv("DOCUMENT_COLLECTION")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")