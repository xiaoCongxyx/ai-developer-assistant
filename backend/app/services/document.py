from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.document import DocumentCreate, DocumentUpdate
from app.models.document import Document
from app.models.knowledge_base import KnowledgeBase
from app.services.vector_store import VectorStoreService
from app.services.file_storage import get_storage_path
import logging

from app.constants.document import DocumentStatus

logger = logging.getLogger(__name__)


def create_document(db: Session, data: DocumentCreate) -> Document:
    """
    创建 Document
    """

    # 跨表业务校验
    #
    # Document 必须属于一个已经存在的 KnowledgeBase。
    # 所以创建 Document 之前，先检查父资源是否存在。
    result = db.execute(
        select(KnowledgeBase).where(
            KnowledgeBase.id == data.knowledge_base_id
        )
    )

    knowledge_base = result.scalar_one_or_none()

    if knowledge_base is None:
        # Service 层这里暂时先使用 ValueError。
        #
        # 为什么不是 HTTPException？
        # 因为 Service 负责业务逻辑，
        # 不应该强依赖 HTTP。
        raise ValueError("Knowledge Base 不存在")

    # 创建Document orm 对象
    document = Document(
        knowledge_base_id=data.knowledge_base_id,
        name=data.name,
        file_type=data.file_type,
        file_path=data.file_path,
        file_size=data.file_size,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

def get_documents(db: Session, knowledge_base_id: int) -> list[Document]:
    """
    获取 所有 Document
    """

    # Document 是属于某个 KnowledgeBase 的，
    # 所以列表查询必须带 knowledge_base_id。
    result = db.execute(
      select(Document)
      .where(Document.knowledge_base_id == knowledge_base_id)
      .order_by(Document.created_at.desc())
    )

    return list(result.scalars().all())

def get_document(db: Session, knowledge_base_id: int, document_id: int) -> Document | None:
    """
    双重校验查询 —— 存在性 + 归属关系，防越权。
    企业实践：后续加用户/租户隔离只需改此一处
    """
    # 嵌套路由必须同时校验：
    #
    # 1. Document 是否存在
    # 2. Document 是否属于当前 KnowledgeBase
    #
    # 不能只通过 document_id 查询。
    #
    # 这种查询实际上也是一种数据隔离。
    # 后续做权限系统、多租户系统时，这个思想非常重要。
    if knowledge_base_id <= 0 or document_id <= 0:
        return None

    result = db.execute(
      select(Document).where(
        Document.id == document_id,
        Document.knowledge_base_id == knowledge_base_id
      )
    )

    return result.scalar_one_or_none()
# def get_document(db: Session, document_id: int) -> Document | None:
#     """
#     根据 documnet_id 查询 Document
#     """

#     result = db.execute(
#         select(Document)
#         .where(Document.id == document_id)
#     )

#     return result.scalar_one_or_none()

def retry_document(db: Session, document: Document) -> Document:
    """
    重置失败文档，准备重新处理。

    这个方法只负责修改数据库中的任务状态，
    不负责执行解析、分块、Embedding 和向量入库。

    状态修改与后台任务执行分离，
    便于测试、维护和后续扩展任务队列。
    """

    # 1. 基础 ID 校验
    if document.id <= 0:
        raise ValueError("Document ID 必须是正整数")

    # 2. 只允许失败状态重试
    if document.status != DocumentStatus.FAILED.value:
        raise ValueError(
            f"当前文档状态不允许重试：{document.status}"
        )

    try:
        # 3. 重制文档状态
        document.status = DocumentStatus.PENDING.value

        # 4. 清理上一次处理失败的错误信息
        document.error_message = ""

        # 5. 提交事务
        db.flush()
        db.commit()

        # 6. 刷新对象，确保返回最新数据库数据
        db.refresh(document)

        logger.info(
            "文档重试状态重置成功：document_id=%s",
            document.id,
        )

        return document

    except Exception:
        db.rollback()

        logger.exception(
            "文档重试状态重置失败：document_id=%s",
            document.id,
        )

        raise



def update_document(db: Session, document: Document, data: DocumentUpdate) -> Document:
    """
    更新 Document
    """

    # 当前阶段：
    # 只允许修改文档名称。
    #
    # knowledge_base_id、file_path、file_type 等字段
    # 暂时不允许通过普通更新接口修改。
    document.name = data.name

    db.commit()
    db.refresh(document)

    return document

async def delete_document(
    db: Session, 
    document: Document,
    vector_store_service: VectorStoreService,
    collection_name: str
) -> None:
    """
    删除文档及其关联资源。

    删除流程：
    1. 删除 Qdrant 中的文档向量
    2. 删除本地文件
    3. 删除数据库中的 Document
    """

    if document.id <= 0:
        raise ValueError("Document ID 必须是正整数")
    if not collection_name.strip():
        raise ValueError("集合名称不能为空")

    document_id = document.id
    file_path = document.file_path
    
    try:
        # 1. 删除文档对应的全部向量  删除 Qdrant 向量
        await vector_store_service.delete_document_vectors(
            collection_name=collection_name,
            document_id=document_id
        )

        # 2. 删除本地文件
        if file_path:
            storage_path = get_storage_path(file_path)

            if storage_path.exists():
                storage_path.unlink()

                logger.info(
                    "本地文件删除成功：document_id=%s, path=%s",
                    document_id,
                    file_path,
                )

        # 3. 删除数据库中的 Document
        db.delete(document)
        db.commit()

        logger.info(
            "文档删除成功：document_id=%s",
            document_id,
        )

    except Exception:
        db.rollback()

        logger.exception(
            "文档删除失败：document_id=%s",
            document_id,
        )

        raise


async def batch_delete_document(
    db: Session,
    documents: list[Document],
    vector_store_service: VectorStoreService,
    collection_name: str
):
    """
    批量删除文档。

    删除顺序：
    1. 删除向量数据
    2. 删除本地文件
    3. 删除数据库记录
    """

    if not documents:
        raise ValueError("没有需要删除的文档")

    try:
        for document in documents:
            if document.id <= 0:
                raise ValueError(
                    f"无效的文档 ID：{document.id}"
                )

            # 1. 删除Qdrant向量
            await vector_store_service.delete_document_vectors(
                collection_name=collection_name, 
                document_id=document.id
            )

            # 2. 删除本地文件
            if document.file_path:
                file_path = get_storage_path(document.file_path)

                if file_path.exists():
                    file_path.unlink()

            # 3. 删除数据库记录
            db.delete(document)
        
        db.commit()

        logger.info(
            "批量删除文档成功，数量：%d",
            len(documents),
        )
    except Exception:
        # 删除失败 回滚数据库事务，不能回滚 Qdrant 和文件系统
        db.rollback()

        logger.exception(
            "批量删除文档失败"
        )

        raise

def start_document_processing(db: Session, document_id: int) -> Document | None:
    """
    将 pending 文档原子地转换为 processing。

    只有 pending 状态的文档才能成功转换。
    """

    statement = select(Document).where(
        Document.id == document_id,
        Document.status == DocumentStatus.PENDING.value
    )

    document = db.execute(
        statement
    ).scalar_one_or_none()

    if document is None:
        return None
    
    document.status = DocumentStatus.PROCESSING.value

    db.commit()
    db.refresh(document)

    return document

def document_exists(db: Session, document_id: int) -> bool:
    """
    查询 document_id 这条记录是否还存在
    """
    statement = select(Document.id).where(Document.id == document_id)

    return db.execute(statement).scalar_one_or_none() is not None