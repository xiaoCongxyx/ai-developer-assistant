import logging
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from app.services.document import (
    create_document,
    delete_document,
    get_document,
    get_document_by_knowledge_base,
    get_documents,
    update_document,
)
from app.core.file import (
    MAX_FILE_SIZE,
    validate_file_extension,
    validate_file_size,
)

from app.services.file_storage import get_storage_path, save_upload_file
from app.services.document_indexer import DocumentIndexer
from app.providers.qdrant_vector_store import QdrantVectorStore
from app.providers.siliconflow_embedding import SiliconFlowEmbeddingProvider
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService
from app.services.document_processor import process_document
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/knowledge-bases/{knowledge_base_id}/documents",
    tags=["Document"],
)

# ==================== 依赖注入：单例模式 ====================
# 全局一次性初始化，避免每次请求重建客户端
def _build_indexer() -> DocumentIndexer:
    """组装全套索引基础设施：仅执行一次"""
    embedding_provider = SiliconFlowEmbeddingProvider()
    embedding_service = EmbeddingService(embedding_provider)
    vector_store = QdrantVectorStore(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT
    )
    vector_store_service = VectorStoreService(vector_store)
    return DocumentIndexer(embedding_service, vector_store_service)

# 懒加载单例
_indexer_instance: DocumentIndexer | None = None
def get_document_indexer() -> DocumentIndexer:
    """首次调用初始化，后续直接复用"""
    global _indexer_instance
    if _indexer_instance is None:
        _indexer_instance = _build_indexer()
    return _indexer_instance

# ==================== 辅助工具函数 ====================
def _cleanup_file(file_path: str) -> None:
    """辅助清理：静默删除，不抛异常"""
    try:
        storage_path = get_storage_path(file_path)
        if storage_path.exists():
            storage_path.unlink()
    except Exception:
        logger.warning(f"清理文件失败: {file_path}", exc_info=True)

def get_db():
    """每个请求独立数据库会话，用完自动关闭"""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


"""
def get_document_indexer() -> DocumentIndexer:
    # 负责组装文档索引所需的基础设施。
    embedding_provider = SiliconFlowEmbeddingProvider()

    embedding_service = EmbeddingService(embedding_provider)

    vector_store = QdrantVectorStore(
        host="localhost",
        port=6333
    )

    vector_store_service = VectorStoreService(vector_store)

    return DocumentIndexer(embedding_service, vector_store_service)
"""


# FastAPI 的 Depends 用来处理依赖注入。
#
# 当前这里最典型的依赖就是：
# HTTP Request
#      ↓
# 获取数据库 Session
#      ↓
# Router
#
# 后续还会用 Depends 注入：
# 用户身份
# 权限
# 当前用户
# 等等。


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document_api(knowledge_base_id: int, data: DocumentCreate, db: Session = Depends(get_db)):
    # HTTP 层负责把业务错误转换成 HTTP 错误。
    #
    # Service 层不知道 HTTP 的存在。
    # Service 抛出 ValueError，
    # Router 再转换成 HTTPException。

    # 确保请求中的 knowledge_base_id
    # 与 body 中的 knowledge_base_id 一致。

    if data.knowledge_base_id != knowledge_base_id:
        raise(
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Knowledge Base ID 不一致",
            )
        )

    try:
        return create_document(db, data)
    except ValueError as exc: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents_api(knowledge_base_id: int, db: Session = Depends(get_db)):
    # 获取某个知识库下的所有 Document。
    return get_documents(db, knowledge_base_id)

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document_api(knowledge_base_id: int, document_id: int, db: Session = Depends(get_db)):
    # 必须同时校验：
    # document_id
    # +
    # knowledge_base_id
    # 防止访问其他知识库的数据。

    document = get_document(db, document_id, knowledge_base_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document 不存在",
        )

    return document

@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
)
def update_document_api(knowledge_base_id: int, document_id: int, data: DocumentUpdate, db: Session = Depends(get_db)):
    # 更新之前同样必须校验 Document
    # 是否属于当前 KnowledgeBase。

    document = get_document_by_knowledge_base(db, knowledge_base_id, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document 不存在",
        )

    return update_document(db, document, data)

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document_api(knowledge_base_id: int, document_id: int, db: Session = Depends(get_db)):
    # 删除同样必须校验父资源关系。

    document = get_document_by_knowledge_base(db, knowledge_base_id, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document 不存在",
        )

    delete_document(db, document)

    return None

@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document_api(
    knowledge_base_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    indexer: DocumentIndexer = Depends(get_document_indexer)
):
    """
    上传文档并触发解析→分块→向量化→索引
    任何一步失败自动清理已写入文件，保证一致性

    UploadFile 是 FastAPI 处理文件上传的核心类型。
    File(...) 表示：
    这个参数来自 multipart/form-data。
    """

    # filename 来自客户端。
    #
    # 这里只把它当作“原始文件名”。
    # 最终保存文件名由后端生成。
    original_filename = file.filename or ""

    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件名不能为空",
        )

    # =========================
    # 1. 文件类型校验
    # =========================

    try:
        validate_file_extension(original_filename)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    # =========================
    # 2. 保存文件
    # =========================

    try:
        file_path, file_size = await save_upload_file(file, MAX_FILE_SIZE)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="文件保存失败",
        )

    # =========================
    # 3. 文件大小校验
    # =========================

    try:
        validate_file_size(file_size)
    except ValueError as exc:
        # 文件已经保存，但是发现超过大小限制。
        #
        # 不能直接返回错误。
        # 必须删除已经保存的文件。
        #
        # “文件系统和数据库一致性问题”。

        _cleanup_file(file_path)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    
    # =========================
    # 4. 创建 Document
    # =========================

    document = DocumentCreate(
        knowledge_base_id=knowledge_base_id, 
        name=original_filename, 
        file_type=Path(original_filename).suffix.lower().lstrip("."),
        file_path=file_path,
        file_size=file_size
    )

    try:
        document = create_document(db, data=document)

        await process_document(db, document, indexer)

        db.refresh(document)

        return document
    except Exception:
        # 如果数据库创建失败，
        # 已经保存到磁盘的文件也必须删除。
        #
        # 否则会产生“孤儿文件”。

        _cleanup_file(file_path)

        import traceback
        logger.error("Document 创建失败详情:\n%s", traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document 创建失败",
        )