from io import BytesIO
from typing import Any
import fitz
from docx import Document

def parse_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
        for page_index, page in enumerate(pdf):
            text = page.get_text("text").strip()
            if text:
                text_parts.append(f"--- Page {page_index + 1} ---\n{text}")
    return "\n\n".join(text_parts).strip()

def parse_docx(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()

def parse_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore").strip()

def parse_uploaded_file(uploaded_file: Any) -> str:
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        return parse_pdf(file_bytes)
    if filename.endswith(".docx"):
        return parse_docx(file_bytes)
    if filename.endswith(".txt"):
        return parse_txt(file_bytes)
    raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
