import streamlit as st
from services.ingestion.pdf_parser import extract_pages
from services.ingestion.block_extractor import extract_blocks
from services.ingestion.chunker import chunk_blocks, build_chunk_text
from services.embedding.embeddings import get_embedding
from services.graph.graph_pipeline import build_graph_from_chunks
from services.vector_db.weaviate_client import WeaviateDB
from services.retrieval.hybrid_engine import HybridQueryEngine
import uuid

st.set_page_config(page_title="Hybrid RAG System", layout="wide")
st.title("📄 Hybrid RAG: PDF Ingestion & Chat")

# Initialize Session State
if "engine" not in st.session_state: # Simplified for demo
    st.session_state.engine = HybridQueryEngine()

# --- STEP 1: UPLOAD ---
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
if uploaded_file and st.button("Process Document"):
    with st.spinner("Processing..."):
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Run your pipeline
        doc_id = str(uuid.uuid4())[:8]
        pages = extract_pages("temp.pdf")
        blocks = extract_blocks(pages)
        chunks = chunk_blocks(blocks)
        chunk_texts = [build_chunk_text(c) for c in chunks if build_chunk_text(c).strip()]
        
        db = WeaviateDB()
        for text in chunk_texts:
            db.insert_chunk(str(uuid.uuid4()), text, get_embedding(text), doc_id)
        
        build_graph_from_chunks(chunk_texts, doc_id)
        st.success(f"Document {doc_id} processed!")

# --- STEP 2: CHAT ---
st.divider()
query = st.chat_input("Ask a question about your documents...")
if query:
    st.chat_message("user").write(query)
    response = st.session_state.engine.query(query)
    st.chat_message("assistant").write(response['answer'])