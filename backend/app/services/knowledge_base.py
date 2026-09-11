from sqlalchemy import null, select
from sqlalchemy.orm import Session

from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseUpdate
from app.models.knowledge_base import KnowledgeBase


def create_knowledge_base(db: Session, data: KnowledgeBaseCreate) -> KnowledgeBase:
    """
    创建 knowledge
    """

    knowledge_base = KnowledgeBase(
        name=data.name,
        description=data.description
    )

    db.add(knowledge_base)
    db.commit()
    db.refresh(knowledge_base)

    return knowledge_base

def get_knowledge_bases(db: Session):
    """
    获取所有 knowledge 
    """
    
    result = db.execute(
        select(KnowledgeBase).order_by(
            KnowledgeBase.created_at.desc()
        )
    )

    return list(result.scalars().all())
  
def get_knowledge_base(db: Session, knowledge_base_id: int) -> KnowledgeBase | None:
    """
    根据 id 查询 knowledge
    """

    result = db.execute(
        select(KnowledgeBase).where(
            KnowledgeBase.id == knowledge_base_id
        )
    )

    return result.scalar_one_or_none()

def update_knowledge_base(db: Session, knowledge_base: KnowledgeBase, data: KnowledgeBaseUpdate) -> KnowledgeBase:
    """
    更新 knowledge
    """

    knowledge_base.name = data.name
    knowledge_base.description = data.description

    db.commit()
    db.refresh(knowledge_base)

    return knowledge_base

def delete__knowledge_base(db: Session, knowledge_base: KnowledgeBase):
    """
    删除 knowledge
    """

    db.delete(knowledge_base)
    db.commit()