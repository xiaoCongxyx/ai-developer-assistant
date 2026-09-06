from pydantic import BaseModel

class KnowledgeBaseCreate(BaseModel):
    name: str
    description: str = ""

class KnowledgeBaseUpdate(BaseModel):
    name: str
    description: str = ""

class KnowledgeBaseResponse(BaseModel):
    id: int
    name: str
    description: str = ""
    create_at: str
    update_at: str