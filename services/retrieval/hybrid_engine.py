# proj-grag\GRAG_V4\services\retrieval\hybrid_engine.py
from services.retrieval.vector_retriever import VectorRetriever
from services.retrieval.graph_retriever import GraphRetriever
from services.retrieval.query_processor import process_query

from services.llm.llm_client import call_llm


SYSTEM_PROMPT = """
You are a helpful assistant.

Answer ONLY based on provided context.
If answer is not present, say: "Not found in documents".
"""


class HybridQueryEngine:

    def __init__(self):
    # def __init__(self, chunk_texts, embeddings):
        self.vector_store = VectorRetriever()
        self.graph_retriever = GraphRetriever()

    def query(self, user_query):

        # -------------------------
        # Step 1: Process Query
        # -------------------------
        qp = process_query(user_query)

        query_text = qp["query"]
        query_entities = qp["entities"]

        # -------------------------
        # Step 2: Vector Retrieval
        # -------------------------
        vector_chunks = self.vector_store.search(query_text, top_k=5)

        # -------------------------
        # Step 3: Graph Retrieval
        # -------------------------
        graph_chunks = self.graph_retriever.get_related_chunks(query_entities)

        # -------------------------
        # Step 4: Combine Context
        # -------------------------
        all_chunks = list(set(vector_chunks + graph_chunks))

        context = "\n\n".join(all_chunks[:10])  # limit context

        # -------------------------
        # Step 5: Final LLM Answer
        # -------------------------
        final_prompt = f"""
            Context:
            {context}

            Question:
            {user_query}
        """

        answer = call_llm(SYSTEM_PROMPT, final_prompt)

        return {
            "answer": answer,
            "vector_chunks": vector_chunks,
            "graph_chunks": graph_chunks,
            "entities": query_entities
        }

    def close(self):
        self.graph_retriever.close()

# from services.retrieval.vector_retriever import VectorStore
# from services.retrieval.graph_retriever import GraphRetriever
# from services.retrieval.query_processor import process_query
# from services.retrieval.vector_retriever import VectorRetriever


# from services.llm.llm_client import call_llm


# SYSTEM_PROMPT = """
# You are a helpful assistant.

# Answer ONLY based on provided context.
# If answer is not present, say: "Not found in documents".
# """


# class HybridQueryEngine:

#     def __init__(self, chunk_texts, embeddings):
#         self.vector_store = VectorRetriever()
#         self.graph_retriever = GraphRetriever()

#     def query(self, user_query):

#         # -------------------------
#         # Step 1: Process Query
#         # -------------------------
#         qp = process_query(user_query)

#         query_text = qp["query"]
#         query_entities = qp["entities"]

#         # -------------------------
#         # Step 2: Vector Retrieval
#         # -------------------------
#         vector_chunks = self.vector_store.search(query_text, top_k=5)

#         # -------------------------
#         # Step 3: Graph Retrieval
#         # -------------------------
#         graph_chunks = self.graph_retriever.get_related_chunks(query_entities)

#         # -------------------------
#         # Step 4: Combine Context
#         # -------------------------
#         all_chunks = list(set(vector_chunks + graph_chunks))

#         context = "\n\n".join(all_chunks[:10])  # limit context

#         # -------------------------
#         # Step 5: Final LLM Answer
#         # -------------------------
#         final_prompt = f"""
# Context:
# {context}

# Question:
# {user_query}
# """

#         answer = call_llm(SYSTEM_PROMPT, final_prompt)

#         return {
#             "answer": answer,
#             "vector_chunks": vector_chunks,
#             "graph_chunks": graph_chunks,
#             "entities": query_entities
#         }

#     def close(self):
#         self.graph_retriever.close()