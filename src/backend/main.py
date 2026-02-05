import logging
import weaviate

from src.backend.models.document import initialize_document_collection
from src.backend.models.document_chunk import initialize_document_chunk_collection
from backend.upload_documents import upload_documents
from src.logger import setup_logging

logger = logging.getLogger(__name__)


def initialize_database() -> None:
    setup_logging()
    logger.info("Starting backend initialization")

    client = None
    try:
        logger.info("Connecting to local Weaviate")
        client = weaviate.connect_to_local()
        logger.info("Weaviate connection established")

        logger.info("Initializing document collection")
        initialize_document_collection(client)

        logger.info("Initializing document chunk collection")
        initialize_document_chunk_collection(client)

        logger.info("Seeding documents")
        upload_documents(client)

        logger.info("Backend initialization completed successfully")

    except Exception:
        logger.exception("Backend initialization failed")
        raise

    finally:
        if client:
            logger.info("Closing Weaviate connection")
            client.close()
            logger.info("Weaviate connection closed")


if __name__ == "__main__":
    initialize_database()
