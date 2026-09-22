import json
import re

from src.llm import generate_response
from src.retriever import DocumentRetriever


def _parse_json_response(response: str) -> dict:
    """
    Extract a JSON object from the model response.
    """

    response = response.strip()

    # Remove markdown code fences if the model adds them.
    response = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response,
        flags=re.IGNORECASE
    ).strip()

    # Try parsing the complete response first.
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Try extracting the first JSON object.
    match = re.search(r"\{.*\}", response, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {}


def generate_quiz(
    retriever: DocumentRetriever,
    topic: str,
    num_questions: int = 5
) -> list[dict]:
    """
    Generate MCQs grounded in the uploaded document.

    Args:
        retriever: Document retriever for the uploaded document.
        topic: Topic for the quiz.
        num_questions: Number of questions to generate.

    Returns:
        List of quiz questions.
    """

    results = retriever.search(topic, top_k=4)

    if not results:
        return []

    context = "\n\n".join(
        f"[Document Section {index}]\n{chunk}"
        for index, (chunk, _) in enumerate(results, start=1)
    )

    prompt = f"""
You are an educational quiz generator.

Create {num_questions} multiple-choice questions about:
{topic}

Use ONLY the information in the document sections below.

Return ONLY valid JSON in this exact format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": 0,
            "explanation": "Short explanation"
        }}
    ]
}}

Rules:
- "answer" must be the zero-based index of the correct option.
- Each question must have exactly 4 options.
- Exactly one option must be correct.
- Do not use information that is not present in the document.
- Keep questions clear and suitable for a student.
- Do not include markdown.
- Return exactly {num_questions} questions.

Document sections:
{context}
""".strip()

    response = generate_response(
        prompt,
        temperature=0.2,
        max_tokens=1200
    )

    data = _parse_json_response(response)

    questions = data.get("questions", [])

    if not isinstance(questions, list):
        return []

    valid_questions = []

    for question in questions:
        if not isinstance(question, dict):
            continue

        if not all(
            key in question
            for key in ["question", "options", "answer", "explanation"]
        ):
            continue

        if not isinstance(question["options"], list):
            continue

        if len(question["options"]) != 4:
            continue

        if not isinstance(question["answer"], int):
            continue

        if not 0 <= question["answer"] < 4:
            continue

        valid_questions.append(question)

    return valid_questions[:num_questions]