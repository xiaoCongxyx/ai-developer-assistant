import logging

from app.core.config import settings
from app.services.document_indexer import DocumentIndexer
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService
from app.providers.siliconflow_embedding import SiliconFlowEmbeddingProvider
from app.providers.qdrant_vector_store import QdrantVectorStore

logger = logging.getLogger(__name__)

_indexer_instance: DocumentIndexer | None = None


def _build_indexer() -> DocumentIndexer:
    """
    组装文档索引所需的基础设施。
    """

    embedding_provider = SiliconFlowEmbeddingProvider()

    embedding_service = EmbeddingService(
        embedding_provider
    )

    vector_store = QdrantVectorStore(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )

    vector_store_service = VectorStoreService(
        vector_store
    )

    return DocumentIndexer(
        embedding_service,
        vector_store_service,
    )


def get_document_indexer() -> DocumentIndexer:
    """
    懒加载索引器实例。
    """

    global _indexer_instance

    if _indexer_instance is None:
        _indexer_instance = _build_indexer()

        logger.info("DocumentIndexer 初始化完成")

    return _indexer_instance