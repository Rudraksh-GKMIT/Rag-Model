def store_chunks(
    collection,
    document_id: str,
    chunks,
    embeddings,
):
    with collection.batch.fixed_size(50) as batch:
        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):

            if not isinstance(chunk["content"], str):
                raise TypeError(
                    f"chunk_text must be string, got {type(chunk['content'])}"
                )

            batch.add_object(
                properties={
                    "chunk_text": chunk["content"],
                    "chunk_type": chunk["type"],
                    "document_id": document_id,
                    "chunk_index": idx,
                    "source": chunk["metadata"].get("source"),
                    "page": chunk["metadata"].get("page"),
                    "table_id": chunk["metadata"].get("table_id"),

                    "deleted_at": None,
                },
                vector=vector.tolist(),
            )
