from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.providers.vector_store import VectorStore

class QdrantVectorStore(VectorStore):
    """
    Qdrant Vector Store 实现。
    余弦相似度 · 幂等建集合 · 空值校验 · 统一返回格式
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333
    ) -> None:
        # AsyncQdrantClient 用于异步访问 Qdrant。
        self.client = AsyncQdrantClient(host=host, port=port)

    async def create_collection(self, collection_name: str, vector_size: int) -> None:
        """创建集合（已存在静默跳过，不报错）"""
        # 先查是否已存在 → 存在就跳过，不报错
        collections = await self.client.get_collections()
        exists = any(c.name == collection_name for c in collections.collections)
        if exists:
            return

        # Collection 必须明确向量维度和距离计算方式。
        await self.client.create_collection(
            collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    async def upsert(self, collection_name: str, points: list[dict]) -> None:
        """
        upsert = insert + update
        upsert = 不存在则创建，存在则更新
        批量写入/更新向量点。

        如果 Point 不存在 → 创建
        如果 Point 已存在 → 更新
        """
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
            points=qdrant_points
        )

    async def search(self, collection_name: str, query_vector: list[float], limit: int = 5) -> list[dict]:
        """
        相似度检索，返回 Top-limit 最相关结果。
        返回格式：[{"id": "...", "score": 相似度, document_id, content...}]
        """
        # 向量不能为空
        if not query_vector:
            raise ValueError("查询向量不能为空")

        # limit 必须是正数
        if limit <= 0:
            raise ValueError("limit 必须大于 0")

        results = await self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
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