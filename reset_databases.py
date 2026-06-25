# reset_databases.py
import os
from neo4j import GraphDatabase
from services.vector_db.weaviate_client import WeaviateDB
from dotenv import load_dotenv

load_dotenv()

def reset_neo4j():
    print("Clearing Neo4j Graph...")
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password123")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n;")
        driver.close()
        print("Neo4j cleared successfully.")
    except Exception as e:
        print(f"Error clearing Neo4j: {e}")

def reset_weaviate():
    print("Dropping Weaviate 'Chunk' collection...")
    try:
        db = WeaviateDB()
        if db.client.collections.exists("Chunk"):
            db.client.collections.delete("Chunk")
        db.client.close()
        print("Weaviate cleared successfully.")
    except Exception as e:
        print(f"Error clearing Weaviate: {e}")

if __name__ == "__main__":
    reset_neo4j()
    reset_weaviate()
    print("All collections dropped. Ready for clean ingestion!")