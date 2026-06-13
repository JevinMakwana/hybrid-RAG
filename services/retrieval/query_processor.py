# proj-grag\GRAG_V4\services\retrieval\query_processor.py
from services.graph.entity_extractor import extract_entities


def process_query(query):
    entities = extract_entities(query)

    return {
        "query": query,
        "entities": entities
    }