from pathlib import Path

from sqlalchemy.orm import Session

from app.core.document_status import (
    DOCUMENT_STATUS_PENDING,
    DOCUMENT_STATUS_COMPLETED,
    DOCUMENT_STATUS_FAILED,
    DOCUMENT_STATUS_PROCESSING,
)
from app.models.document import Document
from app.services.document_content import (
    create_document_content,
    get_document_content,
    update_document_content,
)
from app.services.document_parser import (
    parse_pdf,
    parse_text_file,
)
from app.services.file_storage import get_storage_path
from app.services.document_chunk_processor import (
    process_document_chunks
)
from app.services.document_indexer import COLLECTION_NAME, DocumentIndexer

async def process_document(
    db: Session, 
    document: Document, 
    document_indexer: DocumentIndexer
) -> None:
    """
    文档处理总调度：解析 → 存原文 → 分块 → 入库 → 更新状态
    核心业务：同事务、原子性、失败回滚

    Document Processing 是一个状态机。
    pending
       ↓
    processing
       ↓
    completed / failed

    文档完整处理流程。

    Document
        ↓
    Parse
        ↓
    DocumentContent
        ↓
    Chunking
        ↓
    Embedding
        ↓
    Qdrant
    """
    # Processor 负责协调：
    #
    # Document
    #   ↓
    # Parser
    #   ↓
    # DocumentContent
    #
    # 它本身不负责具体的 PDF 解析细节。

    # 1. 修改状态为 processing
    previous_status = document.status

    document.status = DOCUMENT_STATUS_PROCESSING
    document.error_message = ""


    db.commit()

    try:
        # 2. 获取实际文件路径
        file_path = get_storage_path(document.file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 3. 文件解析  根据文件类型选择 Parser
        # Parser 只负责：
        #
        # File → Text
        #
        # 不负责 Chunk / Embedding / Qdrant。
        if document.file_type == "pdf":
            text = parse_pdf(str(file_path))
        elif document.file_type in {"text", "md"}:
            text = parse_text_file(str(file_path))
        else:
            raise ValueError(
                f"不支持的文件类型: {document.file_type}"
            )
        
        # 检查解析结果
        text = text.strip()
        if not text:
            raise ValueError("解析后文本为空，文件可能是空的或无法读取")

        # 4. 保存解析结果
        document_content = get_document_content(db, document.id)
        if document_content is None:
            create_document_content(db, document.id, text)
        else:
            update_document_content(db, document_content, text)

        # 重新索引前清理旧向量
        # 避免旧向量与新 Chunk 同时存在，导致检索结果污染。
        if previous_status == DOCUMENT_STATUS_COMPLETED:
            await document_indexer.vector_store_service.delete_document_vectors(
                collection_name=COLLECTION_NAME,
                document_id=document.id
            )

        # 5. Chunking 文本 → Chunk
        document_chunks = process_document_chunks(db, document)

        if not document_chunks:
            raise ValueError(
                "Document Chunking 后没有生成 Chunk"
            )

        # 6. Chunk → Embedding → Qdrant
        await document_indexer.index_chunks(document_chunks, knowledge_base_id=document.knowledge_base_id)

        # 7. 修改状态为 completed 只有整个 Pipeline 成功才标记 completed
        document.status = DOCUMENT_STATUS_COMPLETED
        document.error_message = ""

        db.commit()

    except Exception as exc:
        # 任意一个阶段失败：
        #
        # Parse
        # Chunk
        # Embedding
        # Qdrant
        #
        # 都进入 failed。

        # ========== 任意失败：回滚业务数据 + 标记失败状态 ==========
        db.rollback()  # 关键：撤销「存原文」和「分块」，防止半成状态！

        document.status = DOCUMENT_STATUS_FAILED
        document.error_message = str(exc)

        db.commit()

        raise
