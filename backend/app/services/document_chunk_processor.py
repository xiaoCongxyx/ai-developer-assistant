# documentChunkProcessor 负责什么时候切、从哪里拿文本、旧数据怎么办、什么时候提交事务

from sqlalchemy.orm import Session

from app.models.document import Document

from app.services.chunking import split_text

from app.services.document_chunk import (
    delete_document_chunks,
    create_document_chunks,
)

from app.services.document_content import (
    get_document_content,
)


def process_document_chunks(db: Session, document: Document) -> list:
    """
    将 DocumentContent 切分为 DocumentChunk。
    """

    # 获取已经解析好的文档内容
    document_content = get_document_content(db, Document.id)

    if document_content is None:
        raise ValueError(
            "DocumentContent 不存在，无法进行 Chunking"
        )

    # 调用纯 Chunking 算法
    chunks = split_text(document_content.content, chunk_size=500, chunk_overlap=100)

    # 重新处理时先删除旧 Chunk
    delete_document_chunks(db, document.id)

    # 创建新的 Chunk
    document_chunks = create_document_chunks(db, document.id, chunks)

    # 整个 Chunk 更新作为一个事务提交
    db.commit()

    # 刷新对象，获得数据库生成的 id
    for chunk in document_chunks:
        db.refresh(chunk)

    return document_chunks