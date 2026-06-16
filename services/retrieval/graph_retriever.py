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