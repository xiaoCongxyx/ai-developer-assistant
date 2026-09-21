from sqlalchemy.orm import Session

from app.schemas.retrieval import RetrievedChunk
from app.services.document_chunk import (
    get_document_chunks_by_ids,
)

from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService


COLLECTION_NAME = "document_chunks"

class RetrievalService:
    """
    知识检索服务。
    知识检索服务 —— 向量检索 + 关系库补全 + 保序返回 + 脏数据兜底
    流程：问题→转向量→Qdrant查相似→拿ID查原文→按相似度重排→返回结构化结果

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

    async def search(self, db: Session, query: str, limit: int = 5, knowledge_base_id: int | None = None) -> list[RetrievedChunk]:
        """
        检索相关文档片段
        
        参数：
            db: 数据库会话
            query: 用户问题文本
            limit: 返回最相关数量
        返回：
            按相似度降序排列的结构化文档片段
        """

        # 用户问题不能为空
        query = query.strip()

        if not query:
            return []

        # 1. Query 也必须经过 Embedding
        embeddings = await self.embedding_service.embed_texts([query])

        if not embeddings:
            return []

        query_vector = embeddings[0]

        # 2. 向量搜索 Qdrant Vector Search
        vector_results = await self.vector_store_service.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            knowledge_base_id=knowledge_base_id
        )

        if not vector_results:
            return []

        # 3. 获取 Qdrant 返回的 Chunk ID
        chunk_ids = [
            result["id"]
            for result in vector_results
        ]

        # 4. 批量查询 SQLite
        chunks = get_document_chunks_by_ids(db, chunk_ids)

        # 5. 建立 ID → Chunk 映射
        #
        # 为什么？
        # SQL IN 查询不保证返回顺序与 chunk_ids 一致。
        chunks_map = {
          chunk.id: chunk
          for chunk in chunks
        }

        # 6. 按 Qdrant 相似度排序结果重新组装
        retrieved_chunks = []

        for result in vector_results:
            chunk_id = result["id"]
            chunk = chunks_map.get(chunk_id)

            # Qdrant 中可能存在旧 Point，
            # 但 SQLite 中对应 Chunk 已不存在。
            if chunk is None:
                continue

            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    document_id=chunk.document_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    score=result["score"]
                )
            )

        return retrieved_chunks
