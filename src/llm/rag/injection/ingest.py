import weaviate

from src.llm.rag.embeddings.model import get_embedding_model
from src.llm.rag.loaders.pdf_loader import extract_text_from_pdf
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

            try:
                text = extract_text_from_pdf(path)
            except Exception as e:
                print(f"---- Skipping {path}: {e}")
                continue

            if not text:
                continue

            chunks = recursive_semantic_chunk(text)
            embeddings = model.encode(chunks)

            store_chunks(
                chunk_collection,
                doc["document_id"],
                chunks,
                embeddings,
            )

            print(f"Stored {len(chunks)} chunks")

    finally:
        client.close()
