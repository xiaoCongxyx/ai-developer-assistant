"""
PromptUpdate和PromptResponse分开设计 是 API 设计中的输入模型和输出模型分离。
"""

from pydantic import BaseModel

class PromptCreate(BaseModel):
  """创建 Prompt 时的请求数据"""
  name: str
  description: str
  content: str

class PromptUpdate(BaseModel):
  """修改 Prompt 时的请求数据"""
  name: str
  description: str
  content: str

class PromptResponse(BaseModel):
  """返回给前端的 Prompt 数据"""
  id: int
  name: str
  description: str
  content: str
  is_default: bool
