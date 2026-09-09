from app.providers.vector_store import VectorStore


class VectorStoreService:
    """
    Vector Store 业务服务。
    """
    
    def __init__(self, vector_store: VectorStore) -> None:
        """注入向量存储抽象，可随时插拔 Qdrant/Milvus/Pinecone"""
        self.vector_store = vector_store

    async def store_embeddings(self, collection_name: str, points: list[dict]):
        # Service 负责业务层调用，
        # Provider 负责具体 Qdrant 操作。
        if not points:
            return
        try:
            return await self.vector_store.upsert(collection_name=collection_name, points=points)
        except Exception as e:
            raise RuntimeError(f"向量存储失败：{str(e)}") from e

    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 5
    ) -> list[dict]:
        if not query_vector:
            return []

        try:
          return await self.vector_store.search(
              collection_name=collection_name,
              query_vector=query_vector,
              limit=limit
          )
        except Exception as e:
            return []  # 检索失败不抛错，RAG 降级回答
