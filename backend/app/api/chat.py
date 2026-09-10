from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import chat, chat_stream

from app.api.dependencies import get_db
from app.services.chat_service import ChatService
from app.services.embedding import EmbeddingService
from app.services.retrieval import RetrievalService
from app.services.prompt_builder import PromptBuilder
from app.services.context_builder import ContextBuilder
from app.services.vector_store import VectorStoreService
from app.providers.qdrant_vector_store import QdrantVectorStore
from app.providers.siliconflow_embedding import SiliconFlowEmbeddingProvider

router = APIRouter()

def get_chat_service() -> ChatService:
    """
    组装依赖并返回 ChatService 实例。
    生产环境建议改用 FastAPI 依赖注入系统管理生命周期。
    """

    # 1. 向量模型提供者
    embedding_provider = SiliconFlowEmbeddingProvider()
    embedding_service = EmbeddingService(embedding_provider)

    # 2. Qdrant 向量存储
    vector_store = QdrantVectorStore(
        host="localhost",
        port=6333
    )
    vector_store_service = VectorStoreService(vector_store)

    # 3. 检索服务
    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service
    )

    # 4. 构建器
    context_builder = ContextBuilder()
    prompt_builder = PromptBuilder()

    # 5. 组装 ChatService
    return ChatService(retrieval_service, context_builder, prompt_builder)


@router.post("/chat", response_model=ChatResponse)
async def chat_api(
    request: ChatRequest, 
    db: Session = Depends(get_db)
):
    """
    一次性问答接口：检索 → 生成 → 完整返回。
    """

    chat_service = get_chat_service()
    content = await chat_service.chat(
        db=db,
        message=request.message,
        history=request.history,
        knowledge_base_id=request.knowledge_base_id
    )

    return ChatResponse(
      success=True,
      content=content,
    )

@router.post('/chat/stream')
async def chat_stream_api(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    流式问答接口：逐字返回，响应更快、体验更好。
    """

    chat_service = get_chat_service()
    
    return StreamingResponse(
        chat_service.chat_stream(
            db=db,
            message=request.message,
            history=request.history,
            knowledge_base_id=request.knowledge_base_id
        ),
        media_type="text/plain",
    )