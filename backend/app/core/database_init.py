from sqlalchemy import select

from app.core.database import engine, SessionLocal
from app.prompts.default import DEFAULT_SYSTEM_PROMPT
from app.models.prompt import Base,Prompt

def init_database():
  """
  初始化数据库。

  1. 创建不存在的数据表
  2. 初始化默认 Prompt
  """

  # ⭐ 根据 Model 创建数据库表
  Base.metadata.create_all(bind=engine)

  # 创建数据库 Session
  db = SessionLocal()

  try:
    # 查询是否已经存在默认 Prompt
    result = db.execute(
      select(Prompt).where(Prompt.is_default.is_(True))
    )

    default_prompt = result.scalar_one_or_none()

    # 如果不存在，则创建一个默认 Prompt
    if default_prompt is None:
      prompt = Prompt(
        name="默认助手",
        description="AI Developer Assistant 默认 Prompt",
        content=DEFAULT_SYSTEM_PROMPT,
        is_default=True,
      )

      db.add(prompt)
      db.commit()

  finally:
    # ⭐ 无论成功还是失败，都关闭数据库 Session
    db.close()