from logging import Logger
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService

COLLECTION_NAME = "document_chunks"

class DocumentIndexer:
    """
    Document 索引服务。

    负责：
    DocumentChunk
        ↓
    Embedding
        ↓
    Qdrant

    文档索引编排服务 —— 完整流水线：
    DocumentChunk → 批量 Embedding → 构建向量点 → Qdrant 入库
    """

    def __init__(
        self, 
        embedding_service: EmbeddingService, 
        vector_store_service: VectorStoreService
    ) -> None:
        # 只管“编排流程”，不管“怎么转、怎么存”
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service

    async def index_chunks(self, chunks: list) -> None:
        """
        批量索引文档片段：文本 → 向量 → 入库
        
        参数：
            chunks: 含有 id/document_id/chunk_index/content 属性的对象列表
        """
        if not chunks:
            Logger.debug("index_chunks：无片段，跳过")
            return
        
        texts = [
          chunk.content
          for chunk in chunks
        ]

        # Batch Embedding 批量转向量
        embeddings = await self.embedding_service.embed_texts(texts=texts)

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Embedding 数量与 Chunk 数量不一致"
            )

        # 构建入库数据：ID 对齐 + 内容冗余 + 元数据
        points = []
        for chunk, embedding in zip(
            chunks,
            embeddings
        ):
            points.append(
                {
                    # Qdrant Point ID 与 DocumentChunk ID 对齐
                    "id": chunk.id,
                    "vector": embedding,
                    "payload": {
                        "document_id": chunk.document_id,
                        "chunk_index": chunk.chunk_index
                    }
                }
            )

        await self.vector_store_service.store_embeddings(
          collection_name=COLLECTION_NAME,
          points=points
        )
