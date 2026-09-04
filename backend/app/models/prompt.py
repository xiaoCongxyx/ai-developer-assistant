from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  """
  所有数据库 Model 的基类。

  ⭐ 面试重点：
  SQLAlchemy 通过 Base 管理 ORM Model。
  后面的 User、Conversation、Message 等数据表
  都可以继承这个 Base。
  """

  pass

class Prompt(Base):
  """
  Prompt 数据库模型。
  这个类会映射到数据库中的 prompts 表。
  """

  __tablename__ = "prompts"

  # 主键
  id: Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  # Prompt 名称
  name: Mapped[str] = mapped_column(
      String(100),
      nullable=False,
  )

  # Prompt 描述
  description: Mapped[str] = mapped_column(
      String(500),
      nullable=False,
      default="",
  )

  # 真正发送给 LLM 的 System Prompt
  # ⭐ Text 而不是 String：
  # Prompt 内容可能比较长，因此使用 Text。

  content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
  )

  # 是否为默认 Prompt
  is_default: Mapped[bool] = mapped_column(
      Boolean,
      default=False,
      nullable=False,
  )

  # 创建时间
  created_at: Mapped[datetime] = mapped_column(
      DateTime,
      default=datetime.now(timezone.utc),
      nullable=False,
  )

  # 更新时间
  updated_at: Mapped[datetime] = mapped_column(
      DateTime,
      default=datetime.now(timezone.utc),
      onupdate=datetime.now(timezone.utc),
      nullable=False,
  )