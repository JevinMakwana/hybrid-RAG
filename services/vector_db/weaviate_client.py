# proj-grag\GRAG_V4\services\vector_db\weaviate_client.py
import weaviate
from weaviate.classes.config import Configure, Property
from weaviate.classes.data import DataObject
from weaviate.connect import ConnectionParams
from weaviate.config import AdditionalConfig
from weaviate.classes.config import Configure, Property, DataType

class WeaviateDB:
    def __init__(self):
        self.client = weaviate.WeaviateClient(
            connection_params=ConnectionParams.from_url(
                url="http://127.0.0.1:8080",   #  IMPORTANT (NOT localhost)
                grpc_port=50051
            ),
            additional_config=AdditionalConfig(
                timeout_config=(5, 15)
            ),
            skip_init_checks=True   #  bypass strict startup issues
        )

        self.client.connect()

    # ---------------------------
    # SCHEMA
    # ---------------------------
    def create_schema(self):
        try:
            self.client.collections.delete("Chunk")
        except:
            pass

        self.client.collections.create(
            name="Chunk",
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="chunk_id", data_type=DataType.TEXT),
            ],
            vectorizer_config=Configure.Vectorizer.none()
        )
    

    # ---------------------------
    # INSERT
    # ---------------------------
    def insert_chunk(self, chunk_id, text, embedding):

        collection = self.client.collections.get("Chunk")

        collection.data.insert(
            properties={
                "text": text,
                "chunk_id": chunk_id
            },
            vector=embedding
        )

    # ---------------------------
    # SEARCH
    # ---------------------------
    def search(self, embedding, top_k=5):

        collection = self.client.collections.get("Chunk")

        response = collection.query.near_vector(
            near_vector=embedding,
            limit=top_k
        )

        results = []

        for obj in response.objects:
            results.append(obj.properties["text"])

        return results

    # ---------------------------
    # CLOSE
    # ---------------------------
    def close(self):
        self.client.close()

# import weaviate


# class WeaviateDB:
#     def __init__(self):
#         self.client = weaviate.Client("http://localhost:8080")

#     def create_schema(self):
#         schema = {
#             "classes": [
#                 {
#                     "class": "Chunk",
#                     "vectorizer": "none",
#                     "properties": [
#                         {"name": "text", "dataType": ["text"]},
#                         {"name": "chunk_id", "dataType": ["text"]}
#                     ]
#                 }
#             ]
#         }

#         # delete old schema (optional but important during dev)
#         try:
#             self.client.schema.delete_all()
#         except:
#             pass

#         self.client.schema.create(schema)

#     def insert_chunk(self, chunk_id, text, embedding):
#         self.client.data_object.create(
#             data_object={
#                 "text": text,
#                 "chunk_id": chunk_id
#             },
#             class_name="Chunk",
#             vector=embedding
#         )

#     def search(self, embedding, top_k=5):
#         result = (
#             self.client.query
#             .get("Chunk", ["text", "chunk_id"])
#             .with_near_vector({"vector": embedding})
#             .with_limit(top_k)
#             .do()
#         )

#         return [
#             item["text"]
#             for item in result["data"]["Get"]["Chunk"]
#         ]