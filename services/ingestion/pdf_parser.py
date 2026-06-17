# proj-grag\GRAG_V3\services\ingestion\pdf_parser.py
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []

    for page_num, page in enumerate(doc):
        text = page.get_text().strip()

        # OCR fallback for scanned docs or low-text pages
        if len(text) < 30:
            # 1. Render page at higher resolution (2x zoom = 144 DPI) for accurate OCR
            matrix = fitz.Matrix(2, 2)
            
            # 2. Force RGB colorspace to prevent channel mismatches (e.g., RGBA/Grayscale crashes)
            pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB)
            
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img).strip()
            source = "ocr"
        else:
            source = "text"

        structured_blocks = []

        # 3. Handle Block Generation based on source
        if source == "ocr":
            # For scanned pages, simulate blocks by splitting the text into non-empty lines.
            # This allows block_extractor.py's line-by-line heuristics to work normally.
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            for idx, line in enumerate(lines):
                structured_blocks.append({
                    "bbox": (0, 0, 0, 0),   # Bounding box coordinates aren't vital for text chunking
                    "text": line,
                    "block_no": idx,
                    "block_type": 0         # 0 denotes a standard text block
                })
        else:
            # Layout-aware extraction for normal, native text PDFs
            raw_blocks = page.get_text("blocks")
            for b in raw_blocks:
                x0, y0, x1, y1, btext, block_no, block_type = b

                if not btext.strip():
                    continue

                structured_blocks.append({
                    "bbox": (x0, y0, x1, y1),
                    "text": btext.strip(),
                    "block_no": block_no,
                    "block_type": block_type
                })

        pages_data.append({
            "page_number": page_num + 1,
            "source": source,
            "text": text,
            "blocks": structured_blocks
        })

    return pages_data

# def extract_pages(pdf_path):
#     doc = fitz.open(pdf_path)

#     pages_data = []

#     for page_num, page in enumerate(doc):
#         text = page.get_text().strip()

#         # OCR fallback for low-text pages
#         # NOT WROKING YET - NEEDS DEBUGGING 
#         if len(text) < 30:
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             text = pytesseract.image_to_string(img)
#             source = "ocr"
#         else:
#             source = "text"

#         # Layout-aware extraction
#         raw_blocks = page.get_text("blocks")

#         structured_blocks = []
#         for b in raw_blocks:
#             # (x0, y0, x1, y1) define the bounding box (bbox) of the text block
#             # x => horizontal position, y => vertical position
#             # 0 => left/top, 1 => right/bottom
#             # btext => The actual text content inside that block
#             #  block_no => index of the block within that page
#             x0, y0, x1, y1, btext, block_no, block_type = b

#             if not btext.strip():
#                 continue

#             structured_blocks.append({
#                 "bbox": (x0, y0, x1, y1),
#                 "text": btext.strip(),
#                 "block_type": block_type
#             })

#         pages_data.append({
#             "page_number": page_num + 1,
#             "source": source,
#             "text": text,
#             "blocks": structured_blocks
#         })

#     return pages_data
