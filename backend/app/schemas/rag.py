from pydantic import BaseModel

class RetrievedContext(BaseModel):
    """
    RAG 检索上下文。
    """
    content: str
    score: float
    chunk_id: int
    document_id: int

class RAGContext(BaseModel):
    """
    最终提供给 LLM 的 RAG Context。
    """

    query: str
    contexts: list[RetrievedContext]
    context_text: str