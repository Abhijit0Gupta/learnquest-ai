from pathlib import Path
import re

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


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text for downstream processing.

    Args:
        text: Raw extracted text.

    Returns:
        Cleaned text.
    """

    # Replace multiple spaces/tabs with a single space.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace from each line.
    lines = [line.strip() for line in text.splitlines()]

    # Remove completely empty lines at the beginning/end.
    cleaned_lines = []
    previous_blank = False

    for line in lines:
        if not line:
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
        else:
            cleaned_lines.append(line)
            previous_blank = False

    return "\n".join(cleaned_lines).strip()