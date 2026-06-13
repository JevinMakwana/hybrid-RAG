# proj-grag\GRAG_V4\services\retrieval\vector_retriever.py
from services.embedding.embeddings import get_embedding
from services.vector_db.weaviate_client import WeaviateDB


class VectorRetriever:

    def __init__(self):
        self.db = WeaviateDB()

    def search(self, query, top_k=5):
        query_emb = get_embedding(query)

        results = self.db.search(query_emb, top_k=top_k)

        return results