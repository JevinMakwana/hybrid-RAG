# app.py
import streamlit as st
import os
import uuid
from services.ingestion.pdf_parser import extract_pages
from services.ingestion.block_extractor import extract_blocks
from services.ingestion.chunker import chunk_blocks, build_chunk_text
from services.embedding.embeddings import get_embedding
from services.graph.graph_pipeline import build_graph_from_chunks
from services.vector_db.weaviate_client import WeaviateDB
from services.retrieval.hybrid_engine import HybridQueryEngine

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Hybrid RAG System", layout="wide")

# --- CACHED RESOURCES ---
# This ensures Weaviate and Neo4j connections remain open and don't reconnect on every keystroke
@st.cache_resource
def init_services():
    db = WeaviateDB()
    # CRITICAL: reset=False ensures we DO NOT wipe existing documents on startup
    db.create_schema(reset=False) 
    engine = HybridQueryEngine()
    return db, engine

db, engine = init_services()

# --- SESSION STATE INITIALIZATION ---
# 1. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Track processed files to prevent duplicate ingestion in the current session
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# --- SIDEBAR: DOCUMENT INGESTION ---
with st.sidebar:
    st.title("📄 Document Library")
    
    uploaded_file = st.file_uploader("Upload a new PDF", type="pdf")
    
    if uploaded_file:
        # Check if we already processed this exact file this session
        if uploaded_file.name in st.session_state.processed_files:
            st.info(f"✅ '{uploaded_file.name}' is already in the database.")
        else:
            if st.button("Process & Index Document"):
                with st.spinner("Extracting and Indexing..."):
                    temp_path = "temp.pdf"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Generate unique Document ID
                    doc_id = f"DOC_{str(uuid.uuid4())[:8]}"
                    
                    # Run Pipeline
                    pages = extract_pages(temp_path)
                    blocks = extract_blocks(pages)
                    chunks = chunk_blocks(blocks, max_tokens=300, overlap_tokens=50)
                    chunk_texts = [build_chunk_text(c) for c in chunks if build_chunk_text(c).strip()]
                    
                    # Insert into Weaviate
                    for i, text in enumerate(chunk_texts):
                        try:
                            emb = get_embedding(text)
                            cid = str(uuid.uuid4())
                            db.insert_chunk(chunk_id=cid, text=text, embedding=emb, doc_id=doc_id)
                        except Exception as e:
                            st.error(f"Failed to embed chunk {i}: {e}")
                    
                    # Insert into Neo4j
                    build_graph_from_chunks(chunk_texts, doc_id)
                    
                    # Cleanup and record success
                    os.remove(temp_path)
                    st.session_state.processed_files.add(uploaded_file.name)
                    st.success(f"Indexed successfully as {doc_id}")

    st.divider()
    st.caption("Indexed files persist in the databases even if you refresh the page.")

# --- MAIN WINDOW: CHAT INTERFACE ---
st.title("🧠 Hybrid RAG Assistant")

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user query
if prompt := st.chat_input("Ask a question about your documents..."):
    # 1. Display user prompt and add to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Query Engine and display response
    with st.chat_message("assistant"):
        with st.spinner("Searching Vector and Graph databases..."):
            response = engine.query(prompt)
            answer = response["answer"]
            st.markdown(answer)
            
            # Optional: Show debug expander with retrieved context
            with st.expander("View Retrieval Diagnostics"):
                st.write(f"**Vector Chunks Found:** {len(response['vector_chunks'])}")
                st.write(f"**Graph Chunks Found:** {len(response['graph_chunks'])}")
                st.write(f"**Entities Extracted:** {response['entities']}")
                
    # 3. Save assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": answer})