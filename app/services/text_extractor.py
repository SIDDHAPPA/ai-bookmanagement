import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(data: bytes) -> str:
    reader = PdfReader(io.BytesIO(data))
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)
