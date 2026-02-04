import weaviate

from src.llm.rag.embeddings.model import get_embedding_model
from src.llm.rag.loaders.pdf_loader import extract_document
from src.llm.rag.chunking.text_chunker import recursive_semantic_chunk
from src.llm.rag.repository.document_repo import get_documents_without_chunks
from src.llm.rag.repository.chunk_repo import store_chunks


def ingest_documents():
    client = weaviate.connect_to_local()
    model = get_embedding_model()

    try:
        chunk_collection = client.collections.use("DocumentChunk")
        documents = get_documents_without_chunks(client)

        for doc in documents:
            path = doc["document_path"]
            print(f"Ingesting: {path}")

            blocks = extract_document(path, mode="camelot")

            all_chunks = []

            for block in blocks:

                if block["type"] == "text":
                    text_chunks = recursive_semantic_chunk(block["content"])

                    for tc in text_chunks:
                        tc_text = tc.get("content") if isinstance(tc, dict) else tc

                        all_chunks.append({
                            "content": tc_text,
                            "type": "text",
                            "metadata": block["metadata"]
                        })

                elif block["type"] == "table":
                    all_chunks.append({
                        "content": block["content"],
                        "type": "table",
                        "metadata": block["metadata"]
                    })

            contents = [c["content"] for c in all_chunks]
            embeddings = model.encode(contents)

            store_chunks(
                chunk_collection,
                doc["document_id"],
                all_chunks,
                embeddings,
            )

            print(f"Stored {len(all_chunks)} chunks")

    finally:
        client.close()
