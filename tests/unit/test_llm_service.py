import pytest
from unittest.mock import patch
from src.llm_service import generate_summary

def test_generate_summary_with_mock():
    """
    Test generate_summary without calling the real external LLM API.
    Uses unittest.mock.patch to replace fetch_llm_response.
    """
    with patch("src.llm_service.fetch_llm_response") as mock_fetch:
        mock_fetch.return_value = "Python is a popular programming language."

        result = generate_summary("Tell me about Python")

        assert result == "Summary: Python is a popular programming language."
        mock_fetch.assert_called_once_with("Summarize: Tell me about Python")
