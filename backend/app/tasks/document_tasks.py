import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.document import get_document
from app.models.document import Document
from app.services.document_processor import process_document
from app.dependencies.indexer import get_document_indexer

logger = logging.getLogger(__name__)


def _get_document_safe(
    db: Session,
    document_id: int,
) -> Optional["Document"]:
    """
    安全获取文档 —— 先查基本归属：
    1. 查到文档 → 补充 kb_id 再走校验查询
    2. 未查到 / 校验不通过 → 返回 None
    """
    # 临时用基础查询拿到 kb_id
    basic_doc = db.scalar(
        db.query(Document).where(Document.id == document_id)
    )
    if basic_doc is None:
        return None

    # 用带归属校验的接口统一验证
    return get_document(
        db=db,
        knowledge_base_id=basic_doc.knowledge_base_id,
        document_id=document_id,
    )

async def process_document_task(document_id: int) -> None:
    """
    后台处理文档任务。
    流程：校验存在 → 解析 → 分块 → 向量化 → 入库索引
    异常全捕获，不崩溃、完整日志
    """

    if document_id <= 0:
        logger.warning("无效的 document_id: %s", document_id)
        return

    # 上下文管理器自动关闭，finally 不再遗漏
    with SessionLocal() as db:
        try:
            # 1. 安全获取文档（含归属校验
            document = _get_document_safe(db=db, document_id=document_id)
            if document is None:
                logger.warning(
                    "后台处理失败：文档不存在，document_id=%s",
                    document_id,
                )
                return

            # 2. 获取索引器（与 API 端单例完全一致）
            document_indexer = get_document_indexer()

            # 3. 执行完整处理流水线
            await process_document(db=db, document=document, document_indexer=document_indexer)

            logger.info(
                "后台文档处理成功：document_id=%s",
                document_id,
            )

        except Exception:
            logger.exception(
                "后台文档处理失败：document_id=%s",
                document_id,
            )