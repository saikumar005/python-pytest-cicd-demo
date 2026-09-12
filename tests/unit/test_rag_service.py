import pytest
from unittest.mock import Mock
from src.rag_service import chunk_text, build_rag_prompt, retrieve_and_generate


# --- 1. Testing Text Chunking ---
def test_chunk_text_basic():
    text = "Pytest is a framework that makes building simple and scalable tests easy."
    chunks = chunk_text(text, chunk_size=30, overlap=10)

    assert len(chunks) > 1
    assert chunks[0] == text[:30]


def test_chunk_text_empty():
    assert chunk_text("") == []


def test_chunk_text_invalid_size():
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        chunk_text("Sample text", chunk_size=0)


# --- 2. Testing Prompt Construction ---
def test_build_rag_prompt():
    chunks = ["Python is great.", "Pytest helps test code."]
    question = "What is Pytest?"

    prompt = build_rag_prompt(chunks, question)

    assert "Context Information:" in prompt
    assert "Python is great." in prompt
    assert "Question: What is Pytest?" in prompt


def test_build_rag_prompt_empty_chunks():
    with pytest.raises(ValueError, match="Context chunks cannot be empty"):
        build_rag_prompt([], "What is Pytest?")


# --- 3. Testing RAG Generation with Mock LLM ---
def test_retrieve_and_generate_with_mock():
    # Arrange: Create a mock LLM response function
    mock_llm = Mock(return_value="Pytest is a Python testing framework.")
    document = "Pytest makes writing unit tests simple and scalable for backend projects."
    question = "What is Pytest?"

    # Act: Run the full RAG pipeline
    result = retrieve_and_generate(document, question, llm_fetch_fn=mock_llm)

    # Assert: Output data structure
    assert result["question"] == "What is Pytest?"
    assert result["answer"] == "Pytest is a Python testing framework."
    assert result["context_chunks_count"] > 0

    # Assert: Verify mock LLM function was called exactly once
    mock_llm.assert_called_once()
