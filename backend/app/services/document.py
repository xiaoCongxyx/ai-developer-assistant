from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.document import DocumentCreate, DocumentUpdate
from app.models.document import Document
from app.models.knowledge_base import KnowledgeBase


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

def get_document(db: Session, document_id: int) -> Document | None:
    """
    根据 documnet_id 查询 Document
    """

    result = db.execute(
        select(Document)
        .where(Document.id == document_id)
    )

    return result.scalar_one_or_none()

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

def delete_document(db: Session, document: Document) -> None:
    """
    删除 Document
    """

    db.delete(document)
    db.commit()



def get_document_by_knowledge_base(db: Session, knowledge_base_id: int, document_id: int) -> Document | None:
    # 嵌套路由必须同时校验：
    #
    # 1. Document 是否存在
    # 2. Document 是否属于当前 KnowledgeBase
    #
    # 不能只通过 document_id 查询。
    #
    # 🏢 企业实践：
    # 这种查询实际上也是一种数据隔离。
    # 后续做权限系统、多租户系统时，这个思想非常重要。

    result = db.execute(
      select(Document).where(
        Document.id == document_id,
        Document.knowledge_base_id == knowledge_base_id
      )
    )

    return result.scalar_one_or_none()