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
from app.services.document import document_exists

import logging

from app.constants.document import DocumentStatus

logger = logging.getLogger(__name__)

async def process_document(
    db: Session, 
    document: Document, 
    document_indexer: DocumentIndexer
) -> None:
    """
    状态转换完全交给 document_tasks，本函数只负责干活和收尾；
    增加存在性 + 状态双重校验、异常防删除保护、日志增强、注释精简；直接替换即可稳定运行完整处理闭环！

    注意：状态由调用方 start_document_processing 统一管理
    本函数只需关心：
      - 成功 → 设为 completed
      - 失败 → 设为 failed + 错误信息

    文档处理总调度：解析 → 存原文 → 分块 → 入库 → 更新状态
    核心业务：同事务、原子性、失败回滚

    Document Processing 是一个状态机。

    文档处理流水线：解析 → 存原文 → 分块 → 向量化 → 入库索引

    ⚠️ 状态管理：
      - pending → processing  由 document_tasks.start_document_processing 统一原子切换
      - processing → completed  本函数：全部成功
      - processing → failed     本函数：任一步骤失败

    状态机：pending → processing → completed / failed

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

    # 状态已在 document_tasks 中原子切换为 processing 所以下面的状态转换注释 防止重复
    # 1. 修改状态为 processing
    # previous_status = document.status
    # document.status = DOCUMENT_STATUS_PROCESSING
    # document.error_message = ""
    # db.commit()

    # 防御性检查：处理过程中被删除 → 安全终止
    if not document_exists(db, document.id):
        logger.warning(
            "文档已被删除，终止处理：document_id=%s",
            document.id,
        )
        return

    # 双重确认状态（防止外部状态被篡改）
    if document.status != DocumentStatus.PROCESSING.value:
        logger.warning(
            "文档状态非 processing，跳过处理：document_id=%s, status=%s",
            document.id,
            document.status,
        )
        return

    try:
        # 1. 获取实际文件路径
        file_path = get_storage_path(document.file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 2. 文件解析  根据文件类型选择 Parser
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
        
        # 3. 检查解析结果
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
        # 清理旧向量（document_tasks 已确保是 pending 才进来，completed 表示重试）
        if document.status == DocumentStatus.COMPLETED.value:
            await document_indexer.vector_store_service.delete_document_vectors(
                collection_name=COLLECTION_NAME,
                document_id=document.id,
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
        document.status = DocumentStatus.COMPLETED.value
        document.error_message = ""
        db.commit()

        logger.info(
            "文档处理成功：document_id=%s, kb_id=%s, chunks=%d",
            document.id,
            document.knowledge_base_id,
            len(document_chunks),
        )

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
        # 任意环节失败 → 标记失败
        try:
            db.rollback()
        except Exception as rollback_err:
            logger.warning(
                "事务回滚时出现警告：document_id=%s, %s",
                document.id,
                str(rollback_err),
            )

        # 仅当文档仍存在时更新状态
        if document_exists(db, document.id):
            document.status = DocumentStatus.FAILED.value
            document.error_message = str(exc)[:200]  # 防超长
            db.commit()
            try:
                db.commit()
            except Exception as commit_err:
                logger.error(
                    "更新失败状态时出错：document_id=%s, %s",
                    document.id,
                    str(commit_err),
                )
                db.rollback()

        logger.exception(
            "文档处理失败：document_id=%s, error=%s",
            document.id,
            str(exc),
        )
        raise  # 向上抛出，供任务日志统一记录
