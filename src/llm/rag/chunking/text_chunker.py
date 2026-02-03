import re
from typing import List

def recursive_semantic_chunk(
    text: str,
    chunk_size: int = 400,
) -> List[str]:

    if len(text) <= chunk_size:
        return [text]

    # Split by paragraphs
    parts = re.split(r"\n{2,}", text)
    if len(parts) > 1:
        chunks = []
        for p in parts:
            chunks.extend(recursive_semantic_chunk(p, chunk_size))
        return chunks

    # Split by sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) > 1:
        chunks, current = [], ""
        for s in sentences:
            if len(current) + len(s) <= chunk_size:
                current += " " + s
            else:
                chunks.append(current.strip())
                current = s
        if current:
            chunks.append(current.strip())
        return chunks

    # Fallback: hard(force) split
    return [
        text[:chunk_size],
        text[chunk_size:],
    ]
