# hybrid_RAG\services\graph\graph_pipeline.py
import uuid

from services.graph.entity_extractor import extract_entities
from services.graph.relation_extractor import extract_relations
from services.graph.neo4j_writer import Neo4jWriter


def build_graph_from_chunks(chunk_texts):
    writer = Neo4jWriter()

    for idx, text in enumerate(chunk_texts):
        print(f"Processing chunk {idx + 1}/{len(chunk_texts)}")

        if not text.strip():
            continue

        try:
            # -----------------
            # Extract entities
            # -----------------
            entities = extract_entities(text)

            # -----------------
            # Extract relations
            # -----------------
            relations = extract_relations(text)

            # -----------------
            # Create graph
            # -----------------
            chunk_id = str(uuid.uuid4())

            writer.create_chunk_with_entities_and_relations(
                chunk_id=chunk_id,
                text=text,
                entities=entities,
                relations=relations
            )

        except Exception as e:
            print("Error in chunk:", idx)
            print(e)

    writer.close()




# import uuid
# from services.graph.entity_extractor import extract_entities
# from services.graph.neo4j_writer import Neo4jWriter


# def build_graph_from_chunks(chunk_texts):
#     writer = Neo4jWriter()

#     for idx, text in enumerate(chunk_texts):
#         print(f"Linking chunk {idx + 1}/{len(chunk_texts)}")

#         if not text.strip():
#             continue

#         try:
#             # Step 1: extract entities
#             entities = extract_entities(text)

#             # Step 2: assign chunk ID
#             chunk_id = str(uuid.uuid4())

#             # Step 3: write to Neo4j
#             writer.create_chunk_with_entities(
#                 chunk_id=chunk_id,
#                 text=text,
#                 entities=entities
#             )

#         except Exception as e:
#             print("Error in chunk:", idx)
#             print(e)

#     writer.close()