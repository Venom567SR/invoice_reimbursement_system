import fitz  # PyMuPDF
import pdfplumber
from utils.exceptions import PDFParsingError, handle_exception

@handle_exception
def extract_text_pymupdf(pdf_path: str) -> str:
    try:
        with fitz.open(pdf_path) as doc:
            return "\n".join(page.get_text() for page in doc)
    except Exception:
        raise PDFParsingError("Failed to parse PDF with PyMuPDF.")

@handle_exception
def extract_text_pdfplumber(pdf_path: str) -> str:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        raise PDFParsingError("Failed to parse PDF with pdfplumber.")

@handle_exception
def parse_pdf_with_fallback(pdf_path: str) -> str:
    try:
        return extract_text_pymupdf(pdf_path)
    except PDFParsingError:
        return extract_text_pdfplumber(pdf_path)