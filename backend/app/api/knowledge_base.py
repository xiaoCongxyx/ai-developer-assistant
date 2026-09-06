from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseResponse, KnowledgeBaseUpdate
from app.services.knowledge_base import create_knowledge_base, delete__knowledge_base, get_knowledge_base, get_knowledge_bases, update_knowledge_base

router = APIRouter(
    prefix="/knowledge-bases",
    tags=["Knowledge Base"]
)

def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally:
        db.close()

@router.post(
    "",
    response_model=KnowledgeBaseResponse,
)
def create_knowledge_base_api(data: KnowledgeBaseCreate, db: Session = Depends(get_db)):
    """
    创建 knowledgeBase
    """

    return create_knowledge_base(data, db)

@router.get(
    "",
    response_model=list[KnowledgeBaseResponse],
)
def get_knowledge_bases_api(db: Session = Depends(get_db)):
    """
    获取 所有 knowledgeBase 表
    """

    return get_knowledge_bases(db)

@router.get(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
def get_knowledge_base_api(knowledge_base_id: int, db: Session = Depends(get_db)):
    """
    根据id 获取 knowledgeBase
    """

    knowledge_base = get_knowledge_base(db, knowledge_base_id)

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="知识库不存在",
        )

    return knowledge_base

@router.put(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
def update_knowledge_base_api(knowledge_base_id: int, data: KnowledgeBaseUpdate, db: Session = Depends(get_db)):
    """
    更新 knowledgeBase
    """

    knowledge_base = get_knowledge_base(db, knowledge_base_id)

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="知识库不存在",
        )

    return update_knowledge_base(db, knowledge_base, data)

@router.delete("/{knowledge_base_id}")
def delete_knowledge_base_api(knowledge_base_id: int, db: Session = Depends(get_db)):
    """
    删除指定 knowledgeBase
    """

    knowledge_base = get_knowledge_base(
        db,
        knowledge_base_id,
    )

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="知识库不存在",
        )

    delete__knowledge_base(db, knowledge_base)

    return {
        "message": "知识库删除成功",
    }