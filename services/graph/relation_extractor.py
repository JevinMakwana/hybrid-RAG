# proj-grag\GRAG_V3\services\graph\relation_extractor.py
import json
from services.llm.llm_client import call_llm


SYSTEM_PROMPT = """
Extract relationships between entities from the text.

Return ONLY JSON.

Format:
{
  "relations": [
    {"source": "entity1", "target": "entity2", "relation": "relation_type"}
  ]
}

Rules:
- Entities must be meaningful
- relation should be short (e.g., "causes", "uses", "contains", "affects")
- Do not include explanations
"""


def extract_relations(text):
    response = call_llm(SYSTEM_PROMPT, text)

    try:
        data = json.loads(response)
        return data.get("relations", [])
    except Exception:
        return []


# import spacy

# nlp = spacy.load("en_core_web_sm")

# def is_valid_entity(text):
#     text = text.lower().strip()
#     words = text.split()

#     # must be meaningful phrase
#     if len(words) < 2:
#         return False

#     if len(text) < 6:
#         return False

#     # reject patent boilerplate
#     boilerplate = {
#         "embodiment", "embodiments",
#         "application", "invention",
#         "variation", "variations",
#         "aspect", "aspects"
#     }

#     if any(w in boilerplate for w in words):
#         return False

#     # reject admin/table words
#     noise_words = {
#         "grantee", "patentee", "address",
#         "sheet", "number", "renewal", "certificate"
#     }

#     if any(w in noise_words for w in words):
#         return False

#     # reject bad endings
#     if words[-1] in {"and", "or", "of", "with", "wherein"}:
#         return False

#     # reject numeric-dominant phrases
#     digit_count = sum(c.isdigit() for c in text)
#     if digit_count > 2:
#         return False

#     if not any(c.isalpha() for c in text):
#         return False

#     return True

# def extract_entities(doc):
#     entities = []

#     for chunk in doc.noun_chunks:
#         text = chunk.text.strip().lower()

#         # remove leading determiners
#         tokens = text.split()
#         if tokens and tokens[0] in {"the", "a", "an", "this", "that"}:
#             tokens = tokens[1:]

#         text = " ".join(tokens)

#         if not text:
#             continue

#         # reject noisy phrases
#         if len(text.split()) < 2:
#             continue

#         if any(w in {"grantee", "patentee", "address", "sheet", "number"} for w in text.split()):
#             continue

#         if any(char.isdigit() for char in text) and len(text) > 20:
#             continue

#         entities.append(text)

#     return list(set(entities))


# def normalize(text):
#     text = text.lower().strip()

#     # remove leading numbers
#     text = " ".join([w for w in text.split() if not w.isdigit()])

#     return text


# def extract_relations(text):
#     doc = nlp(text)
#     relations = []

#     for sent in doc.sents:
#         sentence = sent.text.lower()

#         #   create spacy doc for this sentence
#         sent_doc = nlp(sent.text)

#         #   extract entities for THIS sentence
#         sent_entities = extract_entities(sent_doc)

#         # COMPONENT_OF
#         for entity in sent_entities:
#             if f"{entity} of" in sentence:
#                 parts = sentence.split(f"{entity} of")

#                 if len(parts) > 1:
#                     target_doc = nlp(parts[1])
#                     target_chunks = [c.text.strip().lower() for c in target_doc.noun_chunks]

#                     if not target_chunks:
#                         continue

#                     target = target_chunks[0]

#                     if target.startswith(("the ", "a ", "an ")):
#                         target = " ".join(target.split()[1:])

#                     if is_valid_entity(entity) and is_valid_entity(target):
#                         relations.append({
#                             "source": normalize(entity),
#                             "relation": "COMPONENT_OF",
#                             "target": normalize(target),
#                             "sentence": sent.text
#                         })
    
#     return relations
