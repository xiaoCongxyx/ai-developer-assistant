from pydantic import BaseModel

class RetrievedChunk(BaseModel):
    """
    检索到的文档 Chunk。
    强类型校验 · IDE自动提示 · 序列化友好
    """

    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    score: float