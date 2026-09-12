# src/rag_service.py
"""
RAG (Retrieval-Augmented Generation) pipeline components for unit testing.
"""

def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    """
    Splits input document text into fixed-size character chunks with overlap.
    """
    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
        if start >= text_length and end >= text_length:
            break

    return chunks


def build_rag_prompt(chunks: list[str], question: str) -> str:
    """
    Constructs a RAG prompt combining retrieved context chunks and the user question.
    """
    if not chunks:
        raise ValueError("Context chunks cannot be empty")
    
    context = "\n---\n".join(chunks)
    prompt = (
        f"Context Information:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer the question strictly using the provided context."
    )
    return prompt


def retrieve_and_generate(document: str, question: str, llm_fetch_fn=None) -> dict:
    """
    Complete RAG workflow:
    1. Chunks document.
    2. Builds context prompt.
    3. Fetches response from LLM (mocked or real).
    """
    chunks = chunk_text(document, chunk_size=100, overlap=20)
    prompt = build_rag_prompt(chunks, question)

    if llm_fetch_fn is None:
        raise RuntimeError("Real LLM call attempted! Provide a mock or function handler.")

    response = llm_fetch_fn(prompt)
    return {
        "question": question,
        "context_chunks_count": len(chunks),
        "answer": response
    }
