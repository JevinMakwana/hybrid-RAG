# proj-grag\GRAG_V4\services\graph\neo4j_writer.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()


class Neo4jWriter:
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

    def create_chunk_with_entities_and_relations(
        self,
        chunk_id,
        text,
        entities,
        relations
    ):
        with self.driver.session() as session:

            # -----------------------------
            # Chunk Node
            # -----------------------------
            session.run(
                """
                MERGE (c:Chunk {id: $id})
                SET c.text = $text
                """,
                id=chunk_id,
                text=text
            )

            # -----------------------------
            # Entity Nodes + MENTIONS
            # -----------------------------
            for ent in entities:
                session.run(
                    """
                    MERGE (e:Entity {name: $name})
                    MERGE (c:Chunk {id: $cid})
                    MERGE (c)-[:MENTIONS]->(e)
                    """,
                    name=ent,
                    cid=chunk_id
                )

            # -----------------------------
            # RELATIONS
            # -----------------------------
            for rel in relations:
                src = rel.get("source")
                tgt = rel.get("target")
                r   = rel.get("relation")

                if not src or not tgt or not r:
                    continue

                session.run(
                    """
                    MERGE (a:Entity {name: $src})
                    MERGE (b:Entity {name: $tgt})
                    MERGE (a)-[:RELATED_TO {type: $rel}]->(b)
                    """,
                    src=src.lower(),
                    tgt=tgt.lower(),
                    rel=r.lower()
                )

# from neo4j import GraphDatabase
# import os
# from dotenv import load_dotenv

# load_dotenv()


# class Neo4jWriter:
#     def __init__(self):
#         self.driver = GraphDatabase.driver(
#             os.getenv("NEO4J_URI"),
#             auth=(
#                 os.getenv("NEO4J_USERNAME"),
#                 os.getenv("NEO4J_PASSWORD")
#             )
#         )

#     def close(self):
#         self.driver.close()

#     def create_chunk_with_entities(self, chunk_id, text, entities):
#         with self.driver.session() as session:

#             # Create chunk node
#             session.run(
#                 """
#                 MERGE (c:Chunk {id: $id})
#                 SET c.text = $text
#                 """,
#                 id=chunk_id,
#                 text=text
#             )

#             # Create & link entities
#             for ent in entities:
#                 if not ent or len(ent) < 2:
#                     continue

#                 session.run(
#                     """
#                     MERGE (e:Entity {name: $name})
#                     MERGE (c:Chunk {id: $cid})
#                     MERGE (c)-[:MENTIONS]->(e)
#                     """,
#                     name=ent.strip(),
#                     cid=chunk_id
#                 )