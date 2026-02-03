# import weaviate
# from weaviate.classes.config import Property, DataType
# from client import get_client

# def create_schema():
#     client = get_client()

#     if client.collections.exists("DocumentChunk"):
#         print("Collection already exists")
#         return

#     client.collections.create(
#         name="DocumentChunk",
#         vectorizer_config=None,   
#         properties=[
#             Property(
#                 name="text",
#                 data_type=DataType.TEXT
#             ),
#             Property(
#                 name="source",
#                 data_type=DataType.TEXT
#             ),
#             Property(
#                 name="chunk_id",
#                 data_type=DataType.INT
#             )
#         ]
#     )

#     print("Collection created successfully")

# create_schema()