#  模拟AI
from app.providers.llm import chat as llm_chat
from app.providers.llm import chat_stream as llm_chat_stream
from app.schemas.chat import ChatMessage

async def chat(message: str, history: list[ChatMessage]) -> str:
  return await llm_chat(message, history)

# AI流式输出
async def chat_stream(message: str, history: list[ChatMessage]):
  async for chunk in llm_chat_stream(message, history):
    yield chunk