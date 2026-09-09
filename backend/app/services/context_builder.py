from app.schemas.rag import RetrievedContext, RAGContext
from app.schemas.retrieval import RetrievedChunk

class ContextBuilder:
    """
    RAG Context 构建器。

    RetrievedChunk[]
          ↓
    ContextBuilder
          ↓
    RAGContext
    """

    def build(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        max_chunks: int = 5,
        min_score: float = 0.0
    ) -> RAGContext:

        # Query 去掉首尾空格
        query = query.strip()

        if not query:
            return RAGContext(
              query="",
              contexts=[],
              context_text=""
            )

        # 过滤低相似度结果
        filtered_chunks = [
            chunk
            for chunk in chunks
            if chunk.score >= min_score
        ]

        # 只取 Top-K 限制最终进入 LLM 的 Chunk 数量
        selected_chunks = filtered_chunks[:max_chunks]

        contexts = [
            RetrievedContext(
              content=chunk.content,
              score=chunk.score,
              chunk_id=chunk.chunk_id,
              document_id=chunk.document_id
            )
            for chunk in selected_chunks
        ]

        # 将结构化 Chunk 转换为 LLM Context
        context_parts = []

        for index, context in enumerate(contexts, start=1):
            context_parts.append(
                f"[参考资料 {index}]\n"
                f"{context.content}"
            )

        context_text = "\n\n".join(context_parts)

        return RAGContext(
          query=query,
          contexts=contexts,
          context_text=context_text
        )