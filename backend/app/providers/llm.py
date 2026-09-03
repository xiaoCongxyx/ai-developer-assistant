from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.chat import ChatMessage
from app.prompts.default import DEFAULT_SYSTEM_PROMPT

client = AsyncOpenAI(
  api_key=settings.llm_api_key,
  base_url=settings.llm_base_url,
)

# 统一构造发送给 LLM 的 messages。
#
# 这样 chat() 和 chat_stream() 就不需要各写一套
# 消息构造逻辑，避免以后修改一处、漏改另一处。
def build_messages(message: str, history: list[ChatMessage]) -> list[dict[str, str]]:
  messages = [
    {
      "role": "system",
      "content": DEFAULT_SYSTEM_PROMPT
    }
  ]

  messages.extend([
    {
      "role": item.role,
      "content": item.content
    }
    for item in history
  ])

  messages.append({
    "role": "user",
    "content": message
  })

  return messages


async def chat(message: str, history: list[ChatMessage]) -> str:

  messages = build_messages(
    message, 
    history,
  )

  response = await client.chat.completions.create(
    model=settings.llm_model,
    messages=messages
  )

  return response.choices[0].message.content or ""


async def chat_stream(message: str, history: list[ChatMessage]):

  messages = build_messages(
    message, 
    history,
  )

  stream = await client.chat.completions.create(
    model=settings.llm_model,
    messages=messages,
    stream=True
  )

  async for chunk in stream:
    content=chunk.choices[0].delta.content

    if content:
      yield content