import re
import camelot
from pypdf import PdfReader

def extract_text_pypdf(file_path: str) -> str:
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

def extract_tables_camelot(file_path: str):
    tables = camelot.read_pdf(
        file_path,
        pages="all",
        flavor="lattice"
    )

    table_chunks = []

    for i, table in enumerate(tables):
        df = table.df
        markdown = df.to_markdown(index=False)

        table_chunks.append({
            "content": markdown,
            "type": "table",
            "table_id": f"table_{i+1}",
            "page": table.page
        })

    return table_chunks

def extract_document(file_path: str, mode: str):
    blocks = []

    text = extract_text_pypdf(file_path)
    if text:
        blocks.append({
            "type": "text",
            "content": text,
            "metadata": {"source": "pypdf"}
        })

    tables = extract_tables_camelot(file_path)
    for t in tables:
        blocks.append({
            "type": "table",
            "content": t["content"],
            "metadata": {
                "table_id": t.get("table_id"),
                "page": int(t.get("page")),
                "source": "camelot"
            }
        })

    return blocks
