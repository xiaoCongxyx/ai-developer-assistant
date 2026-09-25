from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.prompt import Base
from app.constants.document import DocumentStatus

if TYPE_CHECKING:
    from app.models.document_content import DocumentContent
    from app.models.document_chunk import DocumentChunk

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # 外键
    # 表示这个 Document 属于哪个 KnowledgeBase。
    #
    # 一个 KnowledgeBase 可以拥有多个 Document，
    # 因此这里保存 knowledge_base 的 id。
    knowledge_base_id: Mapped[int] = mapped_column(
        ForeignKey("knowledge_bases.id"),
        nullable=False,
    )

    contents: Mapped["DocumentContent | None"] = relationship(
        "DocumentContent",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # 原始文件路径。
    #
    # 数据库通常不直接保存整个 PDF 二进制内容，
    # 而是保存文件的存储位置。
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # 文件大小，单位：bytes。
    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # ========== 处理状态 ==========
    # 统一使用 Mapped + mapped_column 风格，保持写法一致
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DocumentStatus.PENDING.value,
        index=True,  # 状态频繁筛选，加索引提升查询速度
        comment="处理状态：pending/processing/completed/failed",
    )

    # 错误信息。
    #
    # 如果文档解析失败，可以保存失败原因。
    error_message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
