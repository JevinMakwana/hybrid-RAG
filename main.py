# main_pipeline.py
import os
import uuid
from services.ingestion.pdf_parser import extract_pages
from services.ingestion.block_extractor import extract_blocks
from services.ingestion.chunker import chunk_blocks, build_chunk_text
from services.embedding.embeddings import get_embedding
from services.graph.graph_pipeline import build_graph_from_chunks
from services.vector_db.weaviate_client import WeaviateDB

# -------------------------------
# 2. INPUT CONFIGURATION
# -------------------------------
PDF_COLLECTION = {
    "DOC_001": r"C:\Users\Dell\OneDrive - Indian Institute of Science\Internship Preparation Roadmap for CDS.pdf",
    "DOC_002": r"C:\path\to\your\second\pdf_file.pdf",
    "DOC_003": r"C:\Users\Dell\OneDrive - Indian Institute of Science\Academics\LAB\ArjunanSir-CPSdep\FeDaL.pdf",
}

def run_pipeline():
    db = WeaviateDB()
    print("Initializing schema...")
    
    # CRITICAL FIX: Change reset=True to reset=False for persistence
    db.create_schema(reset=False) 

    for doc_id, pdf_path in PDF_COLLECTION.items():
        if not os.path.exists(pdf_path):
            print(f"\n[!] Skipping {doc_id}: File not found at {pdf_path}")
            continue

        print(f"\n{'='*50}\nProcessing {doc_id}: {pdf_path}\n{'='*50}")

        # Ingestion
        pages = extract_pages(pdf_path)
        blocks = extract_blocks(pages)
        chunks = chunk_blocks(blocks, max_tokens=300, overlap_tokens=50)
        
        # Build text and filter empty chunks
        chunk_texts = [build_chunk_text(c) for c in chunks if build_chunk_text(c).strip()]
        print(f"Valid chunk_texts: {len(chunk_texts)}")

        if not chunk_texts:
            continue

        # Storage
        for i, text in enumerate(chunk_texts):
            try:
                emb = get_embedding(text)
                cid = str(uuid.uuid4())
                db.insert_chunk(chunk_id=cid, text=text, embedding=emb, doc_id=doc_id)
            except Exception as e:
                print(f"Embedding failed at chunk {i}: {e}")

        # Graph Construction
        print("Building Graph in Neo4j...")
        build_graph_from_chunks(chunk_texts, doc_id)

    print("\nPipeline completed successfully.")
    db.client.close()

if __name__ == "__main__":
    run_pipeline()