from qdrant_client import AsyncQdrantClient
from qdrant_client import models
from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, PointStruct, VectorParams
import logging


from app.providers.vector_store import VectorStore

logger = logging.getLogger(__name__)
class QdrantVectorStore(VectorStore):
    """
    Qdrant Vector Store 向量存储实现。
    余弦相似度 · 幂等建集合 · 空值校验 · 统一返回格式
    - 余弦相似度
    - 幂等建集合（已存在不报错）
    - 全链路参数校验 + 异常日志
    - 支持按知识库/文档隔离
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        prefer_grpc: bool = True
    ) -> None:
        """初始化异步客户端，默认启用 gRPC 提升吞吐"""
        # AsyncQdrantClient 用于异步访问 Qdrant。
        if not host.strip():
            raise ValueError("Qdrant host 不能为空")
        if not (1 <= port <= 65535):
            raise ValueError(f"端口号无效: {port}")

        self.host = host
        self.port = port
        self.client = AsyncQdrantClient(host=host, port=port,prefer_grpc=prefer_grpc)

    async def close(self) -> None:
        """优雅关闭客户端连接（应用退出时调用）"""
        await self.client.close()
        logger.debug("Qdrant 客户端已关闭")

    async def create_collection(self, collection_name: str, vector_size: int) -> None:
        """创建集合（已存在静默跳过，不报错）"""

        if not collection_name.strip():
            raise ValueError("集合名称不能为空")
        if vector_size <= 0:
            raise ValueError(f"向量维度必须大于 0: {vector_size}")

        try:
            # 先查是否已存在 → 存在就跳过，不报错
            collections = await self.client.get_collections()
            exists = any(c.name == collection_name for c in collections.collections)

            if exists:
                logger.debug(f"集合已存在，跳过创建: {collection_name}")
                return

            # if exists:
            #     logger.warning(f"强制重建集合: {collection_name}")
            #     await self.client.delete_collection(collection_name)

            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"向量集合创建成功: {collection_name}, 维度={vector_size}")

        except Exception as e:
            logger.error(f"创建集合失败 {collection_name}: {e}")
            raise RuntimeError(f"向量存储初始化失败: {e}") from e

    async def upsert(self, collection_name: str, points: list[dict]) -> None:
        """
        upsert = insert + update
        upsert = 不存在则创建，存在则更新
        批量写入/更新向量点。

        如果 Point 不存在 → 创建
        如果 Point 已存在 → 更新
        """

        if not collection_name.strip():
            raise ValueError("集合名称不能为空")
        if not points:
            logger.debug("upsert 空列表，跳过")
            return 0

        try:
            qdrant_points = [
                PointStruct(
                    id=point["id"],
                    vector=point["vector"],
                    payload=point.get("payload", {})
                )
                for point in points
            ]

            if not qdrant_points:
                return
            
            await self.client.upsert(
                collection_name=collection_name,
                points=qdrant_points,
            )

        except Exception as e:
            logger.error(f"写入向量失败 {collection_name}: {e}")
            raise RuntimeError(f"向量写入失败: {e}") from e

    async def search(
      self, 
      collection_name: str, 
      query_vector: list[float], 
      limit: int = 5,
      knowledge_base_id: int | None = None
    ) -> list[dict]:
        """
        相似度检索，返回 Top-limit 最相关结果。
        :param min_score: 最低相似度阈值，过滤低分结果
        返回格式：[{"id": "...", "score": 相似度, document_id, content...}]
        """

        if not collection_name.strip():
            raise ValueError("集合名称不能为空")
        if not query_vector:
            raise ValueError("查询向量不能为空")
        if limit <= 0:
            raise ValueError("limit 必须大于 0")

        try:
            query_filter = None

            if knowledge_base_id is not None:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="knowledge_base_id",
                            match=MatchValue(
                                value=knowledge_base_id
                            )
                        )
                    ]
                )

            results = await self.client.query_points(
                collection_name=collection_name,
                query=query_vector,
                query_filter=query_filter,
                limit=limit,
                with_payload=True
            )

            return [
                {
                    "id": point.id,
                    "score": point.score,
                    "payload": point.payload or {}
                }
                for point in results.points
            ]
        except Exception as e:
            logger.error(f"向量检索失败 {collection_name}: {e}")
            raise RuntimeError(f"检索失败: {e}") from e


    async def delete_by_document_id(
        self,
        collection_name: str,
        document_id: int,
    ) -> None:
        """
        删除指定文档关联的所有向量点。
        """

        if not collection_name.strip():
            raise ValueError("集合名称不能为空")
        if document_id <= 0:
            raise ValueError(f"文档 ID 无效: {document_id}")

        try:
            # 使用 Payload Filter 定位指定文档的所有向量
            await self.client.delete(
                collection_name=collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="document_id",
                                match=models.MatchValue(value=document_id)
                            )
                        ]
                    )
                ),
                wait=True
            )
            logger.info(
                f"文档向量删除请求完成: "
                f"collection={collection_name}, "
                f"document_id={document_id}"
            )

        except Exception as e:
            logger.exception(
                "删除向量失败：collection=%s, document_id=%s, error=%s",
                collection_name,
                document_id,
                str(e),
            )
            raise