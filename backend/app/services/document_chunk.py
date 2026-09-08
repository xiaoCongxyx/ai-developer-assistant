from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk

def get_document_chunk(db:Session, document_id: int) -> list[DocumentChunk]:
    """
    获取一个 Document 的所有 Chunk。
    """

    result = db.execute(
      select(DocumentChunk)
      .where(
          DocumentChunk.document_id == document_id
      )
      .order_by(DocumentChunk.chunk_index.asc())
    )

    return list(result.scalars().all())

def delete_document_chunks(db: Session, document_id: int) -> None:
    """
    删除一个 Document 的所有 Chunk。
    """

    db.execute(
      delete(DocumentChunk).where(
          DocumentChunk.document_id == document_id
      )
    )

def create_document_chunks(db: Session, document_id: int, chunks: list[str]) -> list[DocumentChunk]:
    """
    批量创建 Document Chunk。
    """

    document_chunks = [
        DocumentChunk(document_id=document_id, chunk_index=index, content=content, content_length=len(content))
        for index,content in enumerate(chunks)
    ]

    if not document_chunks:
        return []

    db.add_all(document_chunks)

    return document_chunks