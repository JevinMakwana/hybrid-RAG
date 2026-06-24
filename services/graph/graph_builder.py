# proj-grag\GRAG_V3\services\graph\graph_builder.py
# docker run --name neo4j-hybrid-rag -p 7474:7474 -p 7687:7687 -d -e NEO4J_AUTH=neo4j/password123 neo4j:latest  


import re
from neo4j import GraphDatabase

from services.graph.relation_extractor import extract_relations


URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password123"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# tx
# tx => is a transaction object 
# tx is used for running Cypher queries 
# against the Neo4j database 
# within a transaction context.
# def add_relation(tx, source, relation, target, sentence):
#     tx.run(f"""
#     MERGE (a:Entity {{name: $source}})
#     MERGE (b:Entity {{name: $target}})
#     MERGE (a)-[r:{relation}]->(b)
#     SET r.context = $sentence
#     """, source=source, target=target, sentence=sentence)


def add_relation(tx, source, relation, target, sentence, doc_id):

    relation_type = re.sub(r"[^A-Za-z0-9_]", "_", relation.upper())

    tx.run(f"""
    MERGE (a:Entity {{name: $source}})
    MERGE (b:Entity {{name: $target}})
    MERGE (a)-[r:{relation_type}]->(b)
    SET r.context = $sentence,
        r.document_id = $doc_id
    """, source=source, target=target, sentence=sentence, doc_id=doc_id)


def create_document(tx, doc_id):
    tx.run("""
    MERGE (d:Document {id: $doc_id})
    """, doc_id=doc_id)


def add_field(tx, doc_id, key, value):
    value = str(value).strip().lstrip(":：").strip()
    tx.run("""
    MATCH (d:Document {id: $doc_id})
    MERGE (f:Field {name: $key, value: $value})
    MERGE (d)-[:HAS_FIELD]->(f)
    """, doc_id=doc_id, key=key, value=value)


def add_section(tx, doc_id, section_name):
    tx.run("""
    MATCH (d:Document {id: $doc_id})
    MERGE (s:Section {name: $section_name})
    MERGE (d)-[:HAS_SECTION]->(s)
    """, doc_id=doc_id, section_name=section_name)


def add_paragraph(tx, section_name, content):
    tx.run("""
    MATCH (s:Section {name: $section_name})
    CREATE (p:Paragraph {content: $content})
    CREATE (s)-[:CONTAINS]->(p)
    """, section_name=section_name, content=content[:2000])


def build_graph(tx, doc_id, blocks):
    current_section = "UNCLASSIFIED"
    add_section(tx, doc_id, current_section)


    for b in blocks:
        btype = b["type"]

        # FIELD (merged key-value)
        if btype == "key_value" and "key" in b:
            key = b["key"].strip()
            value = b["value"].strip()

            if not key or not value:
                continue

            if len(key.split()) > 20:
                continue

            # allow dates like 30/07/2025
            if len(value) > 100:
                continue

            # Normalize patent number keys/values
            key_lower = key.lower()
            if ("patent" in key_lower and "number" in key_lower) or key_lower.startswith("patent no"):
                key = "Patent Number"
                import re
                value = re.sub(r"[^0-9]", "", value)

            add_field(tx, doc_id, key, value)
        
        # FIELD (inline key-value)
        elif btype == "key_value" and "content" in b:
            parts = b["content"].split(":", 1)

            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()

                if not key or not value:
                    continue

                if len(key.split()) > 10:
                    continue

                if sum(c.isdigit() for c in key) > 5:
                    continue

                if any(sym in key for sym in ["+", "-", "(", ")", "="]):
                    continue

                add_field(tx, doc_id, key, value)


        # SECTION (heading)
        elif btype == "heading":
            raw = b["content"].strip().lower()

            if "abstract" in raw:
                current_section = "ABSTRACT"
            elif "technical field" in raw:
                current_section = "TECHNICAL FIELD"
            elif "description" in raw:
                current_section = "DESCRIPTION"
            elif "claim" in raw:
                current_section = "CLAIMS"
            else:
                current_section = "UNCLASSIFIED"

            if current_section != "UNCLASSIFIED":
                add_section(tx, doc_id, current_section)
        

        # PARAGRAPH
        elif btype == "paragraph":
            content = b["content"].strip()

            if not content or len(content) < 10:
                continue

            add_paragraph(tx, current_section, content)

            # Extract relations from this paragraph
            relations = extract_relations(content)

            for rel in relations:

                source = rel.get("source")
                target = rel.get("target")
                relation = rel.get("relation")
                sentence = rel.get("sentence", content)

                if not source or not target or not relation:
                    continue

                if len(source.split()) < 2:
                    continue

                if len(target.split()) < 2:
                    continue

                if source == target:
                    continue


                add_relation(
                    tx,
                    source,
                    relation,
                    target,
                    sentence,
                    doc_id
                )


            
        elif btype == "numbered_clause":
            tx.run("""
            MATCH (d:Document {id: $doc_id})
            MERGE (c:Clause {text: $text})
            MERGE (d)-[:HAS_CLAUSE]->(c)
            """, doc_id=doc_id, text=b["content"])



def insert_graph(doc_id, blocks):
    # Open a Neo4j database session, that automatically closes when done
    with driver.session() as session:
        session.execute_write(create_document, doc_id)

        # Execute a write transaction that creates 
        # a Document node in Neo4j 
        # with the given document ID

        # Executes another write transaction 
        # that processes all blocks 
        # (paragraphs, sections, fields, relations, etc.) 
        # and adds them to the graph, linking them to the document
        session.execute_write(build_graph, doc_id, blocks)



def close():
    driver.close()
