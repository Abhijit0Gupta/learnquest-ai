import requests


MODEL_NAME = "Qwen/Qwen3-4B-GGUF:Q4_K_M"
API_URL = "http://127.0.0.1:8080/v1/chat/completions"


def generate_response(
    prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 300
) -> str:
    """
    Generate a response from the local llama.cpp server.

    Args:
        prompt: User prompt.
        temperature: Controls response randomness.
        max_tokens: Maximum number of tokens to generate.

    Returns:
        Generated text from the local model.
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(
        API_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]
