def store_chunks(
    collection,
    document_id: str,
    chunks,
    embeddings,
):
    with collection.batch.fixed_size(50) as batch:
        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            batch.add_object(
                properties={
                    "chunk_text": chunk,
                    "document_id": document_id,
                    "chunk_index": idx,
                    "deleted_at": None,
                },
                vector=vector.tolist(),
            )

def view_chunks(collection, limit: int = 5):
    response = collection.query.fetch_objects(
        limit=limit,
        return_properties=[
            "chunk_text",
            "document_id",
            "chunk_index",
            "deleted_at",
        ],
    )

    return [
        {
            "text": obj.properties["chunk_text"],
            "document_id": obj.properties["document_id"],
            "chunk_index": obj.properties["chunk_index"],
            "deleted_at": obj.properties["deleted_at"],
        }
        for obj in response.objects
    ]

def soft_delete_chunks(collection, document_id: str):
    chunks = collection.query.fetch_objects(
        limit=1000,
        where={
            "path": ["document_id"],
            "operator": "Equal",
            "valueString": document_id,
        },
        return_properties=["chunk_text", "document_id", "chunk_index"],
    )

    with collection.batch.fixed_size(50) as batch:
        for obj in chunks.objects:
            batch.update_object(
                uuid=obj.uuid,
                properties={
                    "deleted_at": "now()",
                },
            )