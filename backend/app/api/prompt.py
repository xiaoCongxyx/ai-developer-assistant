from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.prompt import PromptCreate, PromptResponse, PromptUpdate
from app.services.prompt import (
    create_prompt,
    delete_prompt,
    get_prompt,
    get_prompts,
    set_default_prompt,
    update_prompt
)

router = APIRouter(
  prefix="/prompts",
  tags=["Prompt"],
)

def get_db():
  """
  获取数据库 Session。

  ⭐ 面试重点：
  使用 FastAPI Depends 管理数据库 Session 的生命周期。
  """

  db = SessionLocal()

  try:
    yield db
  finally:
    db.close()

@router.post(
  "",
  response_model=PromptResponse,
)
def create_prompt_api(
  data: PromptCreate,
  db: Session = Depends(get_db)
):
  """
  创建prompt
  """

  return create_prompt(db, data)

@router.get(
    "",
    response_model=list[PromptResponse],
)
def get_prompts_api(db: Session = Depends(get_db)):
  """
  获取所有prompt
  """

  return get_prompts(db)


@router.get(
  "/{prompt_id}",
  response_model=PromptResponse,
)
def get_prompt_api(
  prompt_id: int,
  db: Session = Depends(get_db),
):
  """
  根据 ID 获取 prompt
  """

  prompt = get_prompt(db, prompt_id)

  if prompt is None:
    raise HTTPException(
      status_code=404,
      detail="Prompt 不存在"
    )

  return prompt

@router.put(
  "/{prompt_id}",
  response_model=PromptResponse,
)
def update_prompt_api(
  prompt_id: int,
  data: PromptUpdate,
  db: Session = Depends(get_db),
):
  """
  更新 Prompt
  """
  prompt = get_prompt(db, prompt_id)

  if prompt is None:
    raise HTTPException(
      status_code=404,
      detail="Prompt 不存在"
    )
  
  return update_prompt(db, prompt, data)

@router.post(
  "/{prompt_id}/default",
  response_model=PromptResponse,
)
def set_default_prompt_api(
  prompt_id: int,
  db: Session = Depends(get_db),
):
  prompt = get_prompt(db, prompt_id)

  if prompt is None:
    raise HTTPException(
      status_code=404,
      detail="Prompt 不存在"
    )

  return set_default_prompt(db, prompt)

@router.delete(
  "/{prompt_id}"
)
def delete_prompt_api(
  prompt_id: int,
  db: Session = Depends(get_db)
):
  """
  删除 prompt
  """

  prompt = get_prompt(db, prompt_id)

  if prompt is None:
    raise HTTPException(
      status_code=404,
      detail="Prompt 不存在"
    )

  if prompt.is_default:
    raise HTTPException(
      status_code=400,
      detail="默认 Prompt 不能删除，请先设置其他 Prompt 为默认"
    )

  delete_prompt(db, prompt)

  return {
    "success": True,
    "message": "Prompt 删除成功"
  }