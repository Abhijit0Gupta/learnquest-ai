from src.llm import generate_response
from src.retriever import DocumentRetriever


def answer_question(
    retriever: DocumentRetriever,
    question: str,
    top_k: int = 2
) -> tuple[str, list[tuple[str, float]]]:
    """
    Answer a question using relevant chunks from the uploaded document.

    Args:
        retriever: DocumentRetriever containing document chunks.
        question: Student's question.
        top_k: Number of relevant chunks to use.

    Returns:
        Generated answer and retrieved chunks with similarity scores.
    """

    results = retriever.search(
        question,
        top_k=top_k
    )

    if not results:
        return "I couldn't find relevant information in the document.", []

    context_parts = []

    for index, (chunk, score) in enumerate(results, start=1):
        context_parts.append(
            f"[Document Section {index}]\n{chunk}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a study assistant.

Answer the student's question using ONLY the information
provided in the document sections below.

If the answer cannot be found in the document, say:
"I couldn't find that information in the uploaded document."

Explain the answer clearly and simply for a student.

Document sections:
{context}

Student question:
{question}

Answer:
""".strip()

    answer = generate_response(
        prompt,
        temperature=0.2,
        max_tokens=250
    )

    return answer, results