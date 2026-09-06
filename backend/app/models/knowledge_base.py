from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.prompt import Base

# KnowledgeBase 描述的是 Python 世界里的数据库表结构 knowledge_bases 才是存于数据库的 表
class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    
    id: Mapped[int] = mapped_column(
          Integer,
          primary_key=True,
          autoincrement=True,
      )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
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