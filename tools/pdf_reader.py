import pdfplumber
import re
from docx import Document

def sanitize_text(text):
    """
    Cleans extracted text to improve LLM processing accuracy.
    - Normalizes multiple whitespaces into a single space.
    - Removes excessive empty lines.
    """
    if not text:
        return ""
    # Replace multiple newlines or spaces with a single space
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract and sanitize text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return sanitize_text(text)

def extract_text_from_docx(docx_path):
    """Extract and sanitize text from a .docx file."""
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"
    return sanitize_text(text)

def extract_text_from_file(file_path):
    """Extract text safely from PDF, DOCX, or TXT file."""
    lower_path = file_path.lower()
    if lower_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif lower_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sanitize_text(f.read())
        except Exception as e:
            raise ValueError(f"Unsupported or unreadable file: {str(e)}")