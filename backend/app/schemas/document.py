from datetime import datetime
from pydantic import BaseModel

from app.constants.document import DocumentStatus

class DocumentCreate(BaseModel):
    knowledge_base_id: int

    name: str

    file_type: str

    # 当前阶段先让客户端提供文件路径。
    #
    # 真正的文件上传完成后，这个字段通常不会由用户直接填写，
    # 而是由后端根据上传结果生成。
    file_path: str

    file_size: int = 0

class DocumentUpdate(BaseModel):
    # 更新文档时，暂时只允许修改名称。
    #
    # 文件本身不能通过普通更新接口随便修改。
    name: str

class DocumentResponse(BaseModel):
    id: int
    knowledge_base_id: int
    name: str
    file_type: str
    file_path: str
    file_size: int

    # status 是文档处理生命周期的一部分。
    status: DocumentStatus

    error_message: str

    created_at: datetime
    updated_at: datetime