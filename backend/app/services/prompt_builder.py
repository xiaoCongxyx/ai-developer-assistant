from app.schemas.rag import RAGContext
from app.schemas.chat import ChatMessage

class PromptBuilder:
    """
    RAG Prompt: 提示词构建器 — 组装顺序决定 LLM 行为上限。
        
    组装顺序：
        System(角色规则) → History(对话记忆) → RAG(参考资料+约束) → Query(当前问题)

    System Prompt
        +
    Conversation History
        +
    Retrieved Context
        +
    User Query
        ↓
    LLM Messages
    """

    def build_rag_messages(
        self,
        system_prompt: str,
        history: list[ChatMessage],
        rag_context: RAGContext
    ) -> list[dict[str, str]]:
        """
        构建传给 LLM 的完整消息列表。
        
        参数：
            system_prompt: 自定义角色规则；不传用默认值
            history: 历史对话消息列表
            rag_context: 检索得到的 RAG 上下文（含资料、来源、统计）
        """
        #1. System Prompt 定义 AI 的角色和行为规则
        messages = [
            {
              "role": "system",
              "content": system_prompt
            }
        ]

        # 2.追加历史对话 保留多轮对话上下文
        messages.extend(
            {
              "role": item.role,
              "content": item.content
            }
            for item in history
        )

        # 3. 有条件插入参考资料 + 强约束  只有存在检索结果时才加入 RAG Context
        if rag_context and rag_context.context_text.strip():
            rag_instruction = f"""
请仅使用下面提供的参考资料回答问题。
- 如果参考资料中没有答案，请直接回答：根据提供的文档无法回答这个问题。
- 不要编造资料中不存在的内容。不要猜测。
- 回答时语言要准确、简洁、条理清晰。
- 可以引用参考资料编号，例如「根据参考资料1...」。

--- 参考资料开始 ---

{rag_context.context_text}

--- 参考资料结束 ---
"""

            messages.append(
                {
                    "role": "system",
                    "content": rag_instruction.strip()
                }
            )
        
        # 4. 最后才加入当前用户问题
        messages.append(
            {
                "role": "user",
                "content": rag_context.query
            }
        )

        return messages