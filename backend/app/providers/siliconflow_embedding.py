from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.embedding import EmbeddingProvider

class SiliconFlowEmbeddingProvider(EmbeddingProvider):
    """
    SiliconFlow Embedding Provider。
    """

    def __init__(self) -> None:
        # OpenAI-compatible API
        # SiliconFlow 提供兼容 OpenAI SDK 的接口，
        # 所以这里可以直接使用 AsyncOpenAI。
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

        self.model = settings.embedding_model

    async def embed(self, texts: list[str]) -> list[list[float]]:
        # 批量调用 Embedding API. 一次传入多个文本，执行 Batch Embedding
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts
        )

        # 按照 API 返回顺序提取向量
        # API 返回的是 Embedding 对象，
        # 我们只把真正的向量提取出来。
        embeddings = [
          item.embedding
          for item in response.data
        ]

        return embeddings

