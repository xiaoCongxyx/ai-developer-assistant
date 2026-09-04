from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.prompt import Prompt
from app.schemas.prompt import PromptCreate, PromptUpdate

def create_prompt(
  db: Session,
  data: PromptCreate,
) -> Prompt:
  """
  创建 Prompt。

  ⭐ Service 层负责业务逻辑，
  API 层不要直接处理数据库细节。
  """

  prompt = Prompt(
    name=data.name,
    description=data.description,
    content=data.content,
    is_default=False,
  )

  db.add(prompt)
  db.commit()

  # ⭐ commit 后重新读取数据库中的对象
  db.refresh(prompt)

  return prompt

def get_prompts(db: Session) -> list[Prompt]:
  """
  获取所有 Prompt。
  """

  result = db.execute(
    select(Prompt).order_by(Prompt.created_at.desc())
  )

  return list(result.scalars().all())

def get_prompt(db: Session, prompt_id: int) -> Prompt | None:
  """
  根据 ID 获取 Prompt。
  """

  result = db.execute(
    select(Prompt).where(Prompt.id == prompt_id)
  )

  return result.scalar_one_or_none()

def update_prompt(
  db: Session,
  prompt: Prompt,
  data: PromptUpdate
) -> Prompt:
  """
  更新 prompt
  """

  prompt.name = data.name
  prompt.description = data.description
  prompt.content = data.content

  db.commit()
  db.refresh(prompt)

  return prompt

def set_default_prompt(db: Session, prompt: Prompt) -> Prompt:
  # 取消当前默认 Prompt
  result = db.execute(
    select(Prompt).where(Prompt.is_default.is_(True))
  )

  current_default = result.scalar_one_or_none()

  if current_default is not None:
    current_default.is_default = False
  
  # 设置新的默认 Prompt
  prompt.is_default = True

  db.commit()
  db.refresh(prompt)

  return prompt


def delete_prompt(db: Session, prompt: Prompt) -> None:
  """
  删除 Prompt。
  """

  db.delete(prompt)
  db.commit()