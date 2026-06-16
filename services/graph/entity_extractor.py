# hybrid_RAG\services\graph\entity_extractor.py
import json
import re
from services.llm.llm_client import call_llm


SYSTEM_PROMPT = """
Extract key entities from the text.

Rules:
- Return ONLY JSON
- Format:
{
  "entities": ["Entity1", "Entity2", ...]
}
- Do NOT include numbers, dates, or single words like "system", "method"
- Prefer meaningful domain concepts
"""


# -----------------------------
#  NORMALIZATION FUNCTION
# -----------------------------
def normalize_entity(entity):
    if not entity:
        return None

    # lower case
    entity = entity.lower()

    # remove extra spaces
    entity = re.sub(r"\s+", " ", entity).strip()

    # remove punctuation (except internal)
    entity = re.sub(r"[^\w\s\-]", "", entity)

    # remove very short tokens
    if len(entity) < 3:
        return None

    # remove common garbage words
    stop_entities = {
        "system", "method", "device", "process", "data", "value"
    }

    if entity in stop_entities:
        return None

    return entity


def extract_entities(text):
    response = call_llm(SYSTEM_PROMPT, text)

    try:
        data = json.loads(response)
        raw_entities = data.get("entities", [])

        normalized = []

        for e in raw_entities:
            ne = normalize_entity(e)

            if ne and ne not in normalized:
                normalized.append(ne)

        return normalized

    except Exception:
        return []