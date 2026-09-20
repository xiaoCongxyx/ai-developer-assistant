from abc import ABC, abstractmethod

class VectorStore(ABC):
    """
    Vector Store 抽象接口。
    """

    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        vector_size: int
    ) -> None:
        """
        创建向量集合。
        collection_name: 集合名（如 "doc_embeddings"）
        vector_size: 向量维度（BGE-M3 = 1024）
        """

        raise NotImplementedError

    @abstractmethod
    async def upsert(
        self,
        collection_name: str,
        points: list[dict]
    ) -> None:
        """
        写入或更新向量。
        """

        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int=5,
        knowledge_base_id: int | None = None
    ) -> list[dict]:
        """
        根据向量进行相似度搜索。

        query_vector: 问题转向量
        limit: 返回最相似前 N 条
        返回: 【文档+相似度分数】列表
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_by_document_id(
        self,
        collection_name: str,
        document_id: int
    ) -> None:
        """
        删除指定文档对应的全部向量。

        📌 必懂：
        一个 Document 可能对应多个 Chunk，
        每个 Chunk 都可能对应一个向量。
        """

        raise NotImplementedError
