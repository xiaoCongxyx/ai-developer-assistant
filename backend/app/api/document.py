from fastapi import APIRouter, Depends, HTTPException, Path, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from app.services.document import (
    create_document,
    delete_document,
    get_document,
    get_document_by_knowledge_base,
    get_documents,
    update_document,
)
from app.core.file import (
    MAX_FILE_SIZE,
    validate_file_extension,
    validate_file_size,
)

from app.services.file_storage import save_upload_file

router = APIRouter(
    prefix="/knowledge-bases/{knowledge_base_id}/documents",
    tags=["Document"],
)

# FastAPI 的 Depends 用来处理依赖注入。
#
# 当前这里最典型的依赖就是：
# HTTP Request
#      ↓
# 获取数据库 Session
#      ↓
# Router
#
# 后续还会用 Depends 注入：
# 用户身份
# 权限
# 当前用户
# 等等。

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document_api(knowledge_base_id: int, data: DocumentCreate, db: Session = Depends(get_db)):
    # HTTP 层负责把业务错误转换成 HTTP 错误。
    #
    # Service 层不知道 HTTP 的存在。
    # Service 抛出 ValueError，
    # Router 再转换成 HTTPException。

    # 确保请求中的 knowledge_base_id
    # 与 body 中的 knowledge_base_id 一致。

    if data.knowledge_base_id != knowledge_base_id:
        raise(
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Knowledge Base ID 不一致",
            )
        )

    try:
        return create_document(db, data)
    except ValueError as exc: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents_api(knowledge_base_id: int, db: Session = Depends(get_db)):
    # 获取某个知识库下的所有 Document。
    return get_documents(db, knowledge_base_id)

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document_api(knowledge_base_id: int, document_id: int, db: Session = Depends(get_db)):
    # 必须同时校验：
    # document_id
    # +
    # knowledge_base_id
    # 防止访问其他知识库的数据。

    document = get_document(db, document_id, knowledge_base_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document 不存在",
        )

    return document

@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
)
def update_document_api(knowledge_base_id: int, document_id: int, data: DocumentUpdate, db: Session = Depends(get_db)):
    # 更新之前同样必须校验 Document
    # 是否属于当前 KnowledgeBase。

    document = get_document_by_knowledge_base(db, knowledge_base_id, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document 不存在",
        )

    return update_document(db, document, data)

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document_api(knowledge_base_id: int, document_id: int, db: Session = Depends(get_db)):
    # 删除同样必须校验父资源关系。

    document = get_document_by_knowledge_base(db, knowledge_base_id, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document 不存在",
        )

    delete_document(db, document)

    return None

@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document_api(knowledge_base_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    UploadFile 是 FastAPI 处理文件上传的核心类型。
    File(...) 表示：
    这个参数来自 multipart/form-data。
    """

    # filename 来自客户端。
    #
    # 这里只把它当作“原始文件名”。
    # 最终保存文件名由后端生成。
    original_filename = file.filename or ""

    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件名不能为空",
        )

    # =========================
    # 1. 文件类型校验
    # =========================

    try:
        validate_file_extension(original_filename)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    # =========================
    # 2. 保存文件
    # =========================

    try:
        file_path, file_size = await save_upload_file(file, MAX_FILE_SIZE)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="文件保存失败",
        )

    # =========================
    # 3. 文件大小校验
    # =========================

    try:
        validate_file_size(file_size)
    except ValueError as exc:
        # 文件已经保存，但是发现超过大小限制。
        #
        # 不能直接返回错误。
        # 必须删除已经保存的文件。
        #
        # “文件系统和数据库一致性问题”。

        storage_path = Path(file_path)

        if storage_path.exists():
            storage_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    
    # =========================
    # 4. 创建 Document
    # =========================

    document = DocumentCreate(
      knowledge_base_id=knowledge_base_id, 
      name=original_filename, 
      file_type=Path(original_filename)
      .suffix
      .lower()
      .lstrip("."),
      file_path=file_path,
      file_size=file_size
    )

    try:
        return create_document(db, data=document)
    except Exception:
        # 如果数据库创建失败，
        # 已经保存到磁盘的文件也必须删除。
        #
        # 否则会产生“孤儿文件”。

        storage_path = Path(file_path)

        if storage_path.exists():
            storage_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document 创建失败",
        )