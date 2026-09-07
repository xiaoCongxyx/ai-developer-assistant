from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.prompt import Base

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

    # 文档处理状态。
    #
    # 当前阶段先使用字符串。
    # 后面进入文档解析 / Chunk / Embedding 时，
    # 这个字段会变得非常重要。
    #
    # 例如：
    # pending    → 等待处理
    # processing → 正在处理
    # completed  → 处理完成
    # failed     → 处理失败
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending",
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
