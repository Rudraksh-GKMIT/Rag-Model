from weaviate.classes.config import (
    Configure,
    Property,
    DataType,
    VectorDistances,
)

def initialize_document_chunk_collection(client) -> None:
    if client.collections.exists("DocumentChunk"):
        return

    client.collections.create(
        name="DocumentChunk",

        # ❗ You generate embeddings manually (HF)
        vectorizer_config=None,

        # Vector index for similarity search
        vector_index_config=Configure.VectorIndex.hnsw(
            distance_metric=VectorDistances.COSINE,
            ef_construction=128,
            max_connections=32
        ),

        properties=[
            # Actual chunk text
            Property(
                name="chunk_text",
                data_type=DataType.TEXT,
            ),

            # Reference to parent document (UUID as TEXT)
            Property(
                name="document_id",
                data_type=DataType.TEXT,
            ),

            # Chunk position
            Property(
                name="chunk_index",
                data_type=DataType.INT,
            ),

            # Soft delete support
            Property(
                name="deleted_at",
                data_type=DataType.DATE,
            ),
        ],
    )
