#  模拟AI
import asyncio


async def chat(message: str) -> str:
  return f"收到消息：{message}"

# 模拟AI流式输出
async def chat_stream(message: str):
  chunks = [
    "你好",
    "这是一个",
    "AI 流式",
    "输出测试",
  ]

  for chunk in chunks:
    await asyncio.sleep(0.5)
    yield chunk