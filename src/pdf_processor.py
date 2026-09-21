from pathlib import Path
import pymupdf


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from every page of a PDF.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Combined text extracted from the PDF.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The provided file is not a PDF.")

    text_parts = []

    with pymupdf.open(path) as document:
        for page in document:
            text_parts.append(page.get_text())

    return "\n".join(text_parts)