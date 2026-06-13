# GRAG_V4\services\retrieval\graph_retriever.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()


class GraphRetriever:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(
                os.getenv("NEO4J_USERNAME"),
                os.getenv("NEO4J_PASSWORD")
            )
        )

    def close(self):
        self.driver.close()

    def get_related_chunks(self, entities):

        chunks = []

        with self.driver.session() as session:
            for ent in entities:

                result = session.run(
                    """
                    MATCH (e:Entity {name: $name})<-[:MENTIONS]-(c:Chunk)
                    RETURN c.text AS text
                    LIMIT 5
                    """,
                    name=ent.lower()
                )

                for record in result:
                    chunks.append(record["text"])

        return list(set(chunks))  # remove duplicates


# from neo4j import GraphDatabase

# try:
#     from GRAG_V3.services.retrieval.vector_store import STORE as VECTOR_STORE
# except Exception:
#     try:
#         from GRAG_V3.services.retrieval.vector_store import STORE as VECTOR_STORE
#     except Exception:
#         VECTOR_STORE = None

# URI = "bolt://localhost:7687"
# USERNAME = "neo4j"
# PASSWORD = "projGragTVS"

# import logging
# # Reduce noisy Neo4j driver notifications in stdout by raising logger level
# logging.getLogger("neo4j").setLevel(logging.ERROR)
# logging.getLogger("neo4j.bolt").setLevel(logging.ERROR)

# driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


# #     # WHERE toLower(f.name) CONTAINS toLower($search_text)
# # def get_fields(tx, search_text):
# #     result = tx.run("""
# #     MATCH (d:Document)-[:HAS_FIELD]->(f)
# #     WITH f,
# #          size([word IN split(toLower($search_text), ' ')
# #                WHERE toLower(f.name) CONTAINS word]) AS score
# #     WHERE score > 0
# #     RETURN f.name AS name, f.value AS value, score
# #     ORDER BY score DESC
# #     LIMIT 10
# #     """, search_text=search_text)

# #     return [ {"name": r["name"], "value": r["value"]} for r in result ]
# def get_fields(tx, search_text):
#     result = tx.run("""
#     MATCH (d:Document)-[:HAS_FIELD]->(f)
#     WHERE toLower(f.name) CONTAINS toLower($search_text)
#     RETURN f.name AS name, f.value AS value
#     LIMIT 5
#     """, search_text=search_text)

#     records = [dict(r) for r in result]

#     # If direct match found → return immediately
#     if records:
#         return records

#     # fallback: loose matching
#     result = tx.run("""
#     MATCH (d:Document)-[:HAS_FIELD]->(f)
#     WITH f,
#          size([
#             word IN split(toLower($search_text), ' ')
#             WHERE toLower(f.name) CONTAINS word
#          ]) AS score
#     WHERE score >= 1
#     RETURN f.name AS name, f.value AS value, score
#     ORDER BY score DESC
#     LIMIT 5
#     """, search_text=search_text)

#     return [dict(r) for r in result]



# def get_paragraphs(tx, search_text):
#     # stricter matching for longer queries, but lowered threshold to improve recall
#     result = tx.run("""
#     MATCH (s:Section)-[:CONTAINS]->(p:Paragraph)
#     WITH s, p,
#         size([
#             word IN split(toLower($search_text), ' ')
#             WHERE toLower(p.content) CONTAINS word
#         ]) AS score
#     WHERE score >= 2
#     RETURN s.name AS section, p.content AS paragraph, score
#     ORDER BY score DESC
#     LIMIT 20
#     """, search_text=search_text)

#     return [dict(r) for r in result]


# def get_paragraphs_loose(tx, search_text):
#      # looser matching for short queries; increase limit for better recall
#      result = tx.run("""
#      MATCH (s:Section)-[:CONTAINS]->(p:Paragraph)
#      WITH s, p,
#             size([
#                 word IN split(toLower($search_text), ' ')
#                 WHERE toLower(p.content) CONTAINS word
#             ]) AS score
#      WHERE score >= 1
#      RETURN s.name AS section, p.content AS paragraph, score
#      ORDER BY score DESC
#      LIMIT 20
#      """, search_text=search_text)

#      return [dict(r) for r in result]


# def get_paragraphs_fuzzy(tx, search_text):
#     # Very loose matching: return paragraphs that contain any token from search_text
#     result = tx.run("""
#     MATCH (s:Section)-[:CONTAINS]->(p:Paragraph)
#     WITH s, p,
#          size([
#             word IN split(toLower($search_text), ' ')
#             WHERE word <> '' AND toLower(p.content) CONTAINS word
#          ]) AS score
#     WHERE score >= 1
#     RETURN s.name AS section, p.content AS paragraph, score
#     ORDER BY score DESC
#     LIMIT 20
#     """, search_text=search_text)

#     return [dict(r) for r in result]




# # def get_relations(tx, search_text):
# #     result = tx.run("""
# #     MATCH (a:Entity)-[r]->(b:Entity)    
# #     WHERE any(word IN split(toLower($search_text), ' ')
# #         WHERE toLower(a.name) CONTAINS word
# #             OR toLower(b.name) CONTAINS word)
# #     RETURN a.name AS source, type(r) AS relation, b.name AS target
# #     LIMIT 10
# #     """, search_text=search_text)

# #     return [dict(r) for r in result]
# def get_relations(tx, search_text):
#     result = tx.run("""
#     MATCH (a:Entity)-[r]->(b:Entity)
#     WITH a, r, b,
#          size([
#             word IN split(toLower($search_text), ' ')
#             WHERE toLower(a.name) CONTAINS word
#                OR toLower(b.name) CONTAINS word
#          ]) AS score
#     WHERE score >= 3
#     RETURN a.name AS source, type(r) AS relation, b.name AS target, score
#     ORDER BY score DESC
#     LIMIT 10
#     """, search_text=search_text)

#     return [dict(r) for r in result]


# def get_paragraphs_by_ids(tx, ids):
#     # ids are numeric Neo4j internal ids
#     result = tx.run(
#         """
#         UNWIND $ids AS pid
#         MATCH (p:Paragraph) WHERE id(p) = pid
#         RETURN id(p) AS pid, p.content AS paragraph
#         """,
#         ids=[int(i) for i in ids]
#     )
#     return [dict(r) for r in result]


# def get_fields_by_value(tx, search_text):
#     # Find documents where any field value contains words from the search text,
#     # then return other fields from the same document. This helps answer
#     # entity-centric queries like "address of <company>".
#     result = tx.run("""
#     WITH split(toLower($search_text),' ') AS tokens
#     MATCH (d:Document)-[:HAS_FIELD]->(f_match)
#     WHERE any(t IN tokens WHERE t <> '' AND toLower(f_match.value) CONTAINS t)
#     WITH d, collect(f_match) AS matched
#     MATCH (d)-[:HAS_FIELD]->(f)
#     RETURN f.name AS name, f.value AS value, d.id AS doc_id
#     LIMIT 50
#     """, search_text=search_text)

#     return [dict(r) for r in result]



# def retrieve(search_text):
#     # filter out short tokens and pure-numeric tokens to reduce false matches
#     filtered = " ".join([w for w in search_text.split() if len(w) > 2 and not w.isdigit()])

#     with driver.session() as session:
#         fields = session.execute_read(get_fields, filtered)
#         # choose paragraph matcher depending on number of search tokens
#         token_count = len(filtered.split()) if filtered.strip() else 0
#         # use stricter matching for longer queries (4+ tokens), otherwise use loose
#         if token_count >= 4:
#             paragraphs = session.execute_read(get_paragraphs, filtered)
#         else:
#             paragraphs = session.execute_read(get_paragraphs_loose, filtered)

#         # if no paragraphs found, try a very fuzzy matcher to increase recall
#         if not paragraphs:
#             paragraphs = session.execute_read(get_paragraphs_fuzzy, filtered)

#         # Hybrid: if a vector store is available, try to retrieve top-k
#         # semantically similar paragraphs. This is optional and non-invasive:
#         # when no vector store exists, we skip this step.
#         vector_paragraphs = []
#         try:
#             if VECTOR_STORE and VECTOR_STORE.loaded:
#                 # If embeddings are available and the operator has precomputed
#                 # paragraph vectors (via reindex_embeddings), we can perform
#                 # a vector search by first computing a query embedding.
#                 # To avoid accidental calls, computing the embedding is
#                 # delegated to services.retrieval.embeddings.compute_embedding
#                 try:
#                     from GRAG_V3.services.retrieval.embeddings import compute_embedding
#                 except Exception:
#                     try:
#                         from GRAG_V3.services.retrieval.embeddings import compute_embedding
#                     except Exception:
#                         compute_embedding = None

#                 if compute_embedding:
#                     q_emb = None
#                     try:
#                         q_emb = compute_embedding(search_text)
#                     except Exception:
#                         q_emb = None

#                     if q_emb is not None:
#                         # increase top_k to rely more on semantic search
#                         try:
#                             hits = VECTOR_STORE.query(q_emb, top_k=12)
#                         except Exception:
#                             hits = []

#                         # fetch paragraph texts for these ids
#                         ids = [int(h[0]) for h in hits] if hits else []
#                         if ids:
#                             para_rows = session.execute_read(get_paragraphs_by_ids, ids)
#                             # merge similarity into returned paragraphs
#                             pid_to_para = {r['pid']: r['paragraph'] for r in para_rows}
#                             vector_paragraphs = []
#                             for hid, score in hits:
#                                 try:
#                                     pid = int(hid)
#                                 except Exception:
#                                     continue
#                                 para_text = pid_to_para.get(pid)
#                                 if para_text:
#                                     # include pid so downstream code can reference source
#                                     vector_paragraphs.append({
#                                         'pid': pid,
#                                         'section': None,
#                                         'paragraph': para_text,
#                                         'score': score
#                                     })
#         except Exception:
#             vector_paragraphs = []

#         # if vector_paragraphs found, prepend them to paragraphs list
#         if vector_paragraphs:
#             # avoid duplicates by paragraph text
#             existing = {p['paragraph'] for p in paragraphs}
#             merged = vector_paragraphs + [p for p in paragraphs if p['paragraph'] not in existing]
#             paragraphs = merged

#         relations = session.execute_read(get_relations, filtered)

#         # If no useful fields were found, try value-based lookup (entity-centric)
#         if not fields:
#             fields = session.execute_read(get_fields_by_value, filtered)

#     return {
#         "fields": fields,
#         "paragraphs": paragraphs,
#         "relations": relations
#     }