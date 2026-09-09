
from app.providers.embedding import EmbeddingProvider


class EmbeddingService:
    """
    Embedding 业务服务。
    """

    def __init__(self, provider: EmbeddingProvider) -> None:
        self.provider = provider
        
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        批量将文本转为向量。
        
        参数：
            texts: 文本列表
        返回：
            与输入顺序一一对应的向量列表
        """
        # Service 层负责业务编排，
        # Provider 层负责具体第三方 API 调用。
        if not texts:
            return []

        return await self.provider.embed(texts)