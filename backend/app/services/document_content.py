from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_content import DocumentContent

def get_document_content(db: Session, document_id: int) -> DocumentContent | None:
    # 根据 Document ID 查询对应的解析内容。

    result = db.execute(
      select(DocumentContent).where(
        DocumentContent.document_id == document_id
      )
      .order_by(DocumentContent.id.desc())  # 有多个时取最新
      .limit(1)  # 最多返回 1 条
    )

    return result.scalar_one_or_none()

def create_document_content(db: Session, document_id: int, content: str) -> DocumentContent:
    # Parser 得到文本后，
    # 由这个 Service 将解析结果保存到数据库。

     # ✅ 先检查是否已存在
    # existing = get_document_content(db, document_id)
    # if existing:
    #     # 已存在 → 更新而不是新建
    #     existing.content = content
    #     existing.content_length = len(content)
    #     db.commit()
    #     return existing

    document_content = DocumentContent(document_id=document_id, content=content, content_length = len(content))

    db.add(document_content)
    db.commit()
    db.refresh(document_content)

    return document_content

def update_document_content(db: Session, document_content: DocumentContent, content: str) -> DocumentContent:
    document_content.content = content
    document_content.content_length = len(content)

    db.commit()
    db.refresh(document_content)

    return document_content