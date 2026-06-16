import os
# hybrid_RAG\services\ingestion\build_graph_from_pdf.py

from services.ingestion.pdf_parser import extract_pages
from services.ingestion.block_extractor import extract_blocks
from services.graph.graph_builder import insert_graph, close

# PDF_PATH = r"C:\Users\Dell\Downloads\Internship Preparation Roadmap for CDS.pdf"
PDF_PATH = r"C:\Users\Dell\OneDrive - Indian Institute of Science\Academics\LAB\ArjunanSir-CPSdep\Federated Foundation Models on Heterogeneous Time Series (FFTS).pdf"
DOC_ID = "DOC_001"


def main():
    print("Extracting pages...")
    pages = extract_pages(PDF_PATH)

    print("Extracting blocks...")
    blocks = extract_blocks(pages)

    print("Building graph...")
    insert_graph(DOC_ID, blocks)

    close()

    print("Graph construction completed.")


if __name__ == "__main__":
    main()

