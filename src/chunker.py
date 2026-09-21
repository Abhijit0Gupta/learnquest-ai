def create_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> list[str]:
    """
    Split cleaned document text into overlapping chunks.

    Args:
        text: Cleaned document text.
        chunk_size: Maximum approximate number of characters per chunk.
        overlap: Number of characters shared between consecutive chunks.

    Returns:
        List of text chunks.
    """

    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks