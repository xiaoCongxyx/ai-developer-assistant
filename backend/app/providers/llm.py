from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(
  api_key=settings.llm_api_key,
  base_url=settings.llm_base_url,
)

# Provider 的职责是调用具体的 LLM 服务。
#
# Provider 不负责：
# - Prompt 构建
# - RAG 检索
# - Conversation History 管理
#
# 这些属于上层业务逻辑。
#
# Provider 只接收已经构建好的 messages。


# 统一构造发送给 LLM 的 messages。
#
# 这样 chat() 和 chat_stream() 就不需要各写一套
# 消息构造逻辑，避免以后修改一处、漏改另一处。
"""
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
"""

async def chat(messages: list[dict[str, str]]) -> str:
    """
    调用 LLM，返回完整回答。

    职责：接收标准消息列表 → 调用 API → 提取文本返回
    不负责：提示词构建、历史管理、检索、格式重排
    """

    response = await client.chat.completions.create(
      model=settings.llm_model,
      messages=messages
    )

    return response.choices[0].message.content or ""


async def chat_stream(messages: list[dict[str, str]]):
    """
    调用 LLM，并以流式方式返回回答内容。

    与 chat() 接收完全相同的 messages 参数
    上层「一套消息、两种输出」
    """

    stream = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        stream=True
    )

    try:
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    finally:
        # 手动关闭流，消除 Python 3.14 异步清理异常
        try:
            await stream.close()
        except Exception:
            pass