from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.prompt import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.document import Document


class DocumentContent(Base):
    __tablename__ = "document_contents"

    # 一个 DocumentContent 对应一个 Document。
    #
    # 使用独立主键，而不是直接使用 document_id 作为主键，
    # 是为了让数据模型更加清晰，也方便未来扩展。

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # DocumentContent 属于哪个 Document。
    #
    # unique=True 保证一个 Document 当前最多只有一份解析内容。
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
        unique=True,
    )

    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="contents",
    )

    # Parser 最终得到的完整文本。
    #
    # Text 比 String 更适合存储长度不确定的大文本。
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    # 解析后的字符数量。
    content_length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
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