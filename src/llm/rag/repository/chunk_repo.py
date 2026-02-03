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
