import re
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    parts = []

    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)

    text = " ".join(parts)
    text = re.sub(r"\s+", " ", text)
    text = "".join(c for c in text if c.isprintable())

    return text.strip()
