import weaviate

from src.backend.models.document import initialize_document_collection
from src.backend.models.document_chunk import initialize_document_chunk_collection
from src.backend.seed import seed_documents
from src.logger import setup_logging


def main() -> None:
    setup_logging()

    client = weaviate.connect_to_local()
    try:
        # 1. Reset DocumentChunk completely (dev-friendly)
        if client.collections.exists("DocumentChunk"):
            client.collections.delete("DocumentChunk")
            print("DocumentChunk collection deleted")

        # 2. Ensure schemas exist
        initialize_document_collection(client)
        initialize_document_chunk_collection(client)

        # 3. Seed documents (PASS client in)
        seed_documents(client)

        # 4. Verify
        print("Collections:", client.collections.list_all())

        docs = client.collections.use("Document").query.fetch_objects()
        for d in docs.objects:
            print(d.properties)

    finally:
        client.close()


    # try:
    #     collection = client.collections.use("DocumentChunk")

    #     result = collection.query.fetch_objects(
    #         limit=1,
    #         include_vector=True
    #     )

    #     obj = result.objects[0]

    #     vector = list(obj.vector.values())
    #     print("Vector dim:", len(vector))
    #     print("First 10:", vector)

    # finally:
    #     client.close()



if __name__ == "__main__":
    main()
