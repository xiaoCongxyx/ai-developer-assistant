from pydoc import text
from typing import Sequence

"""
第一版采用 递归文本切分
Chunking 的目标不是“把文字切小”，而是尽可能保持语义完整，同时控制 Chunk 大小。
Overlap 可以让相邻 Chunk 保留部分上下文   所以用chunkSize和chunkOverlap 尽量维持语义完整
"""

DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 100

SEPARATORS: Sequence[str] = (
    "\n\n",
    "\n",
    "。",
    "！",
    "？",
    ".",
    "!",
    "?",
    " ",
)

def split_text(
  text: str,
  chunk_size: int = DEFAULT_CHUNK_SIZE,
  chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
):
    """
    将文本切分成多个 Chunk。

    参数：
        text: 原始文本
        chunk_size: 每个 Chunk 的最大字符数
        chunk_overlap: 相邻 Chunk 的重叠字符数

    返回：
        Chunk 文本列表
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap 不能小于 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap 必须小于 chunk_size")

    text = text.strip()

    if not text:
        return []

    # 📌 必懂：递归切分
    # 第一步：智能拆分 → 得到很多小片段
    row_chunks = _recursive_split(text, chunk_size, separators=SEPARATORS)

    # 第二步：拼接+加重叠 → 变成最终块
    return merge_chunks(
      row_chunks,
      chunk_size,
      chunk_overlap
    )


def _recursive_split(text: str, chunk_size: int, separators: Sequence[str]) -> list[str]:
    # 如果文本已经足够小
    if len(text) <= chunk_size:
        return [text]
    
    # 没有更多分隔符了，只能硬切
    if not separators:
        return _hard_split(text, chunk_size)
    
    separator = separators[0]

    # 当前分隔符不存在
    if separator not in text:
        return _recursive_split(text, chunk_size, separators=separators[1:])

    # 按照当前分隔符进行初步切分
    parts = [
        part.strip()
        for part in text.split(separator)
        if part.strip()
    ]

    chunks: list[str] = []
    current = ""

    for part in parts:
        candidate = (
            f"{current}{separator}{part}"
            if current
            else part
        )

        if len(candidate) <= chunk_size:
            current = candidate
            continue
        
        # 当前组合超过 Chunk 大小
        if current:
            chunks.append(current)
            current = ""

        # 单独一个 part 仍然太大
        if len(part) > chunk_size:
            sub_chunks = _recursive_split(
                text=part,
                chunk_size=chunk_size,
                separators=separators[1:]
            )

            chunks.extend(sub_chunks)

        else: 
            current = part

    if current:
        chunks.append(current)
    
    return chunks


def merge_chunks(chunks: list[str], chunk_size: int, chunk_overlap: int) -> list[str]:
    if not chunks:
        return []

    result: list[str] = []
    current = ""

    for chunk in chunks:
        if not current:
            current = chunk
            continue
    
        overlap_text = current[-chunk_overlap:] if chunk_overlap > 0 else ""

        candidate = (
            overlap_text
            + chunk
        )

        if len(candidate) <= chunk_size:
            current = candidate

        else:
            result.append(current)
            current = chunk

    if current:
        result.append(current)

    return result

    


def _hard_split(
    text: str,
    chunk_size: int,
) -> list[str]:

    return [
        text[i:i + chunk_size]
        for i in range(
            0,
            len(text),
            chunk_size,
        )
    ]