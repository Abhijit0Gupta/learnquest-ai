import json

from src.llm import generate_response


def extract_topics(text: str, max_topics: int = 10) -> list[str]:
    """
    Extract the main topics from a document.

    Args:
        text: Cleaned document text.
        max_topics: Maximum number of topics to return.

    Returns:
        List of topic names.
    """

    # Limit the text sent to the model for this first version.
    sample_text = text[:12000]

    prompt = f"""
You are an educational content analyzer.

Read the document below and identify its main learning topics.

Return ONLY a valid JSON object in this exact format:

{{
    "topics": [
        "Topic 1",
        "Topic 2",
        "Topic 3"
    ]
}}

Rules:
- Return at most {max_topics} topics.
- Use short, meaningful topic names.
- Do not include explanations.
- Do not include markdown.
- Only include topics actually present in the document.

Document:
{sample_text}
""".strip()

    response = generate_response(
        prompt,
        temperature=0.1,
        max_tokens=300
    )

    try:
        data = json.loads(response)

        topics = data.get("topics", [])

        if not isinstance(topics, list):
            return []

        return [
            str(topic).strip()
            for topic in topics
            if str(topic).strip()
        ][:max_topics]

    except json.JSONDecodeError:
        return []