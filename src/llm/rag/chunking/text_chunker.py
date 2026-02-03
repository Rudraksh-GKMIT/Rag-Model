from typing import List

def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80,
) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks
