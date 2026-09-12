# src/llm_service.py

def fetch_llm_response(prompt: str) -> str:
    """
    Simulates calling an external LLM API (e.g. OpenAI or Gemini).
    In real life, this makes a network HTTP request.
    """
    raise RuntimeError("Real LLM API call executed! Network requests should be mocked in unit tests.")


def generate_summary(prompt: str) -> str:
    """
    Business logic function that formats a prompt, calls the LLM, and formats the output.
    """
    response_text = fetch_llm_response(f"Summarize: {prompt}")
    return f"Summary: {response_text.strip()}"
