from pydantic import BaseModel, Field
from typing import Literal

class ChatMessage(BaseModel):
    role: Literal['user', 'assistant']
    content: str
class ChatRequest(BaseModel):
    message: str = Field(..., description="用户问题")
    history: list[ChatMessage] = Field(
        default_factory=list,
        description="历史对话消息"
    )
    knowledge_base_id: int | None = None
    """
    message: str
    # Field(default_factory=list) 比 history: list = [] 更严谨。因为 default_factory 会为每一个请求创建独立的 list。
    history: list[ChatMessage] = Field(default_factory=list),
    knowledge_base_id: int | None = None
    """

class ChatResponse(BaseModel):
    success: bool
    content: str