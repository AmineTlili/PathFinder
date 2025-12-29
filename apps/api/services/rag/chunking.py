from __future__ import annotations

def chunk_text(text: str, max_chars: int = 900, overlap: int = 150) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    chunks: list[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == n:
            break

        start = max(0, end - overlap)

        if start >= end:
            start = end

    return chunks
