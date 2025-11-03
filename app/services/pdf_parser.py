import io
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_bytes: bytes) -> str:
    with io.BytesIO(file_bytes) as pdf_file:
        text = extract_text(pdf_file)
    return text
