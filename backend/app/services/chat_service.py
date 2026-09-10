from sqlalchemy.orm import Session

from app.providers.llm import chat
from app.prompts.default import DEFAULT_SYSTEM_PROMPT
from app.schemas.chat import ChatMessage
from app.services.context_builder import ContextBuilder
from app.services.prompt_builder import PromptBuilder
from app.services.retrieval import RetrievalService
from app.services.prompt import get_default_prompt

class ChatService:
    """
    AI Developer Assistant 聊天业务服务。

    完整流水线：
        检索 → 过滤格式化 → 组装提示词 → 调用LLM
    职责：只编排流程、不介入细节；依赖全部外部注入。

    当前负责：
    Retrieval
        ↓
    Context Builder
        ↓
    Prompt Builder
        ↓
    LLM
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder
    ) -> None:
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder

    async def chat(
        self,
        db: Session,
        message: str,
        history: list[ChatMessage],
        knowledge_base_id: int | None = None
    ) -> str:
        """完整返回模式：检索→整理→拼词→生成→一次性返回"""

        # 第一步：从知识库检索与当前问题相关的 Chunk。
        # 指定 knowledge_base_id 后，
        # Retrieval 只会搜索对应知识库
        retrieval_chunks = await self.retrieval_service.search(
            db,
            query=message,
            limit=5,
            knowledge_base_id=knowledge_base_id
        )

        # 第二步：将检索结果进行筛选和格式化。
        rag_context = self.context_builder.build(
            query=message,
            chunks=retrieval_chunks,
            max_chunks=5,
            min_score=0.55
        )

        default_prompt = get_default_prompt(db)
        if default_prompt is None:
            raise ValueError("默认 Prompt 不存在")

        # 第三步：将 System Prompt、
        # Conversation History、
        # RAG Context、
        # User Query
        # 组合成 LLM messages。
        messages = self.prompt_builder.build_rag_messages(
            system_prompt=default_prompt.content,
            history=history,
            rag_context=rag_context
        )

        # 第四步：将已经构建好的 messages
        # 交给 LLM Provider。
        return await chat(messages)