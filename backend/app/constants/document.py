from enum import Enum

class DocumentStatus(str, Enum):
    """
    文档处理状态。

    📌 必懂：状态机的核心定义。
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"