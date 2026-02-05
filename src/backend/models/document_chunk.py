import logging
from weaviate.classes.config import (
    Configure,
    Property,
    DataType,
    VectorDistances,
)

logger = logging.getLogger(__name__)

def initialize_document_chunk_collection(client) -> None:
    """
    DocumentChunk collection for RAG:
    - vectors provided manually
    - HNSW index enabled
    - supports text + table chunks
    - supports structured metadata
    """

    if client.collections.exists("DocumentChunk"):
        logger.info(
            "Collection '%s' already exists. Skipping creation.",
            "DocumentChunk",
        )
        return

    logger.info("Creating collection '%s'...", "DocumentChunk")

    client.collections.create(
        name="DocumentChunk",

        vector_index_config=Configure.VectorIndex.hnsw(
            distance_metric=VectorDistances.COSINE,
            ef_construction=128,
            max_connections=32,
        ),

        properties=[
            Property(
                name="chunk_text",
                data_type=DataType.TEXT,
            ),
            Property(
                name="chunk_type",
                data_type=DataType.TEXT,
            ),
            Property(
                name="document_id",
                data_type=DataType.TEXT,
            ),
            Property(
                name="chunk_index",
                data_type=DataType.INT,
            ),
            Property(
                name="source",
                data_type=DataType.TEXT, 
            ),
            Property(
                name="page",
                data_type=DataType.INT,
            ),
            Property(
                name="table_id",
                data_type=DataType.TEXT,
            ),
            Property(
                name="deleted_at",
                data_type=DataType.DATE,
            ),
        ],
    )

    logger.info(
        "Collection '%s' created successfully.",
        "DocumentChunk",
    )
