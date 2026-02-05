import weaviate
from src.backend.models.document_chunk import initialize_document_chunk_collection

client = weaviate.connect_to_local()

# Delete the entire collection
client.collections.delete("DocumentChunk")
initialize_document_chunk_collection(client)


print("DocumentChunk collection deleted")

client.close()
