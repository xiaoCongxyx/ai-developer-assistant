from pydantic import BaseModel, Field
from typing import Literal

class ChatMessage(BaseModel):
  role: Literal['user', 'assistant']
  content: str
class ChatRequest(BaseModel):
  message: str
  # Field(default_factory=list) 比 history: list = [] 更严谨。因为 default_factory 会为每一个请求创建独立的 list。
  history: list[ChatMessage] = Field(default_factory=list)

class ChatResponse(BaseModel):
  success: bool
  content: str