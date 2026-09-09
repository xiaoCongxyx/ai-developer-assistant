import math

def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """
    计算两个向量的余弦相似度。

    返回值范围：[-1.0, 1.0]
        1.0 = 完全同向（最相似）
        0.0 = 不相关
       -1.0 = 完全反向
    """

    # 两个向量必须具有相同维度，
    # 否则没有办法进行逐元素计算。
    if len(vector_a) != len(vector_b):
        raise ValueError(f"向量维度不匹配: A={len(vector_a)}, B={len(vector_b)}")

    if not vector_a or not vector_b:
        raise ValueError("向量不能为空")

    # dot product（点积）
    dot_product = sum(
      a * b
      for (a, b) in zip(vector_a, vector_b)
    )

    # 向量长度
    norm_a = math.sqrt(
      sum(a * a for a in vector_a)
    )

    norm_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if norm_a == 0 or norm_b == 0:
        raise ValueError("零向量无法计算余弦相似度")

    # Cosine Similarity =
    # 两个向量的点积 / 两个向量长度的乘积
    return dot_product / (norm_a * norm_b)