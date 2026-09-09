

from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService


COLLECTION_NAME = "document_chunks"

class RetrievalService:
    """
    知识检索服务。

    Query
      ↓
    Embedding
      ↓
    Vector Search
      ↓
    Top-K Chunks
    """

    def __init__(
        self, 
        embedding_service: EmbeddingService, 
        vector_store_service: VectorStoreService
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service

    async def search(self, query: str, limit: int = 5):

        # 用户问题不能为空
        query = query.strip()

        if not query:
            return []

        # Query 也必须经过 Embedding
        embeddings = await self.embedding_service.embed_texts([query])

        if not embeddings:
            return []

        query_vector = embeddings[0]

        # 向量搜索
        results = await self.vector_store_service.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit
        )

        return results
