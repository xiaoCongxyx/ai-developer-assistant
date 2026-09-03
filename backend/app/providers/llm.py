from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.chat import ChatMessage

client = AsyncOpenAI(
  api_key=settings.llm_api_key,
  base_url=settings.llm_base_url,
)

async def chat(message: str, history: list(ChatMessage)) -> str:

  messages=[
    {
      "role": item.role,
      "content": item.content
    }
    for item in history
  ]

  messages.append({
    "role": "user",
    "content": message
  })

  response = await client.chat.completions.create(
    model=settings.llm_model,
    messages=messages
  )

  return response.choices[0].message.content or ""


async def chat_stream(message: str, history: list(ChatMessage)):

  messages=[
    {
      "role": item.role,
      "content": item.content
    }
    for item in history
  ]

  messages.append({
    "role": "user",
    "content": message
  })

  stream = await client.chat.completions.create(
    model=settings.llm_model,
    messages=messages,
    stream=True
  )

  async for chunk in stream:
    content=chunk.choices[0].delta.content

    if content:
      yield content