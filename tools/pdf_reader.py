import re
from docx import Document

def sanitize_text(text):
    """
    Cleans extracted text to improve LLM processing accuracy.
    - Normalizes non-breaking spaces and invalid unicode replacement symbols.
    - Preserves single spaces and newline structures.
    """
    if not text:
        return ""
    # Normalize unicode replacement characters and special bullet separators
    text = text.replace('\ufffd', ' - ').replace('', ' - ')
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract and sanitize text from a PDF file using robust multi-engine fallback."""
    extracted_text = ""

    # Engine 1: pypdf (best space & layout preservation)
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        pages_text = []
        for page in reader.pages:
            t = page.extract_text()
            if t and t.strip():
                pages_text.append(t.strip())
        if pages_text:
            extracted_text = "\n\n".join(pages_text)
    except Exception as e1:
        print(f"pypdf extraction notice: {e1}")

    # Engine 2: pdfminer.six (if pypdf produced too short or empty text)
    if len(extracted_text.strip()) < 100:
        try:
            from pdfminer.high_level import extract_text as pdfminer_extract
            txt = pdfminer_extract(pdf_path)
            if txt and len(txt.strip()) > len(extracted_text.strip()):
                extracted_text = txt
        except Exception as e2:
            print(f"pdfminer extraction notice: {e2}")

    # Engine 3: pdfplumber (final fallback)
    if len(extracted_text.strip()) < 100:
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                pages_text = []
                for page in pdf.pages:
                    t = page.extract_text()
                    if t and t.strip():
                        pages_text.append(t.strip())
                if pages_text:
                    extracted_text = "\n\n".join(pages_text)
        except Exception as e3:
            print(f"pdfplumber extraction notice: {e3}")

    return sanitize_text(extracted_text)

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