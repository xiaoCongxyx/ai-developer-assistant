from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    """
    Embedding Provider 抽象接口。
    """

    @abstractmethod
    async def embed(self, text: list[str]) -> list[list[float]]:
        """
        将多段文本转换成向量。
        """
        raise NotImplementedError