# proj-grag\GRAG_V4\services\ingestion\temp.py
import fitz  # PyMuPDF
import pytesseract
from PIL import Image


def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    # type(doc)= <class 'pymupdf.Document'>
    

    pages_data = []

    for page_num, page in enumerate(doc):
        # type(page)= <class 'pymupdf.Page'>
        # type(page.get_text())= <class 'str'>
        # print("---------->page_num:", page_num + 1)
        # print("---------->type(page)=", type(page))
        # print("---------->page=", page)
        text = page.get_text().strip()
        # print("---------->type(page.get_text())=", type(page.get_text()))
        # print("---------->page.get_text()=", page.get_text())
        # print("---------->page.get_text().strip()=", page.get_text().strip())

        # Case 1: Text-based page
        if len(text) > 50:
            pages_data.append({
                "page_number": page_num + 1,
                "source": "text",
                "content": text
            })

        # Case 2: OCR fallback
        else:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            ocr_text = pytesseract.image_to_string(img)

            pages_data.append({
                "page_number": page_num + 1,
                "source": "ocr",
                "content": ocr_text
            })

    return pages_data


# if __name__ == "__main__":
#     pdf_path = r"C:\Users\Jevinkumar.Palabhai\Downloads\565861.pdf"

#     print("======calling extract_pages for forming pages======")
#     pages = extract_pages(pdf_path)
#     print("pages===", pages[:2])


#     for page in pages:
#         print("\n--- PAGE", page["page_number"], "---")
#         print("Source:", page["source"])
#         print(page["content"][:500])


# C:\Users\Jevinkumar.Palabhai\AppData\Local\Programs\Tesseract-OCR