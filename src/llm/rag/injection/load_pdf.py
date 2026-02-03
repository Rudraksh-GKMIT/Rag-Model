import re
from datetime import datetime, timezone
from typing import List

import weaviate
from pypdf import PdfReader


from src.llm.rag.config import RAGConfig
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(RAGConfig.EMBEDDING_MODEL_NAME)

def extract_text_from_pdf(file_path: str) -> str:
    text_parts = []

    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    text = " ".join(text_parts)
    text = re.sub(r"\s+", " ", text)
    text = "".join(c for c in text if c.isprintable())

    return text.strip()

def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80,
) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

def get_documents_without_chunks(client):
    document_collection = client.collections.use("Document")
    chunk_collection = client.collections.use("DocumentChunk")

    # 1️⃣ Fetch all documents
    documents = document_collection.query.fetch_objects(
        return_properties=["document_path"]
    )

    # 2️⃣ Fetch all chunked document IDs
    chunks = chunk_collection.query.fetch_objects(
        return_properties=["document_id"]
    )

    chunked_doc_ids = {
        obj.properties["document_id"]
        for obj in chunks.objects
    }

    # 3️⃣ Filter documents not yet chunked
    unprocessed = [
        {
            "document_id": str(doc.uuid),  # ✅ UUID always present in v4
            "document_path": doc.properties["document_path"],
        }
        for doc in documents.objects
        if str(doc.uuid) not in chunked_doc_ids
    ]

    return unprocessed

def ingest_documents():
    client = weaviate.connect_to_local()

    try:
        chunk_collection = client.collections.use("DocumentChunk")
        documents = get_documents_without_chunks(client)

        for doc in documents:
            path = doc["document_path"]
            print(f"Ingesting: {path}")

            try:
                text = extract_text_from_pdf(path)
            except FileNotFoundError:
                print(f"⚠️ File not found, skipping: {path}")
                continue
            except Exception as e:
                print(f"⚠️ Failed to read {path}: {e}")
                continue

            if not text.strip():
                print(f"⚠️ Empty content, skipping: {path}")
                continue

            chunks = chunk_text(text)
            embeddings = embedding_model.encode(chunks)

            with chunk_collection.batch.fixed_size(50) as batch:
                for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
                    batch.add_object(
                        properties={
                            "chunk_text": chunk,
                            "document_id": doc["document_id"],
                            "chunk_index": idx,
                            "deleted_at": None,
                        },
                        vector=vector.tolist(),
                    )

            print(f"Stored {len(chunks)} chunks.")

    finally:
        client.close()

