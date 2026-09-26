
from app.constants.document import DocumentStatus


class DocumentStatusTransition:
    """
    Document 状态转换规则。

      - 统一管理文档生命周期。
        状态机 / 状态转换。
        避免业务代码随意修改状态。

    允许的状态流转图：
              pending
                 ↓
             processing
             ↙    ↘
        completed   failed
           ↑         ↑
        (重处理)    (重试→pending)
    """

    # 状态转换规则：当前状态 → 可转入的目标状态集合
    _TRANSITION: dict[
        DocumentStatus,
        set[DocumentStatus]
    ] = {
        DocumentStatus.PENDING: {
            DocumentStatus.PROCESSING
        },
        DocumentStatus.PROCESSING: {
            DocumentStatus.COMPLETED,
            DocumentStatus.FAILED
        },
        DocumentStatus.FAILED: {
            DocumentStatus.PENDING,  # 重试：回到待处理队列
        },
        DocumentStatus.COMPLETED: set()
    }

    @classmethod
    def can_transition(
        cls,
        current: DocumentStatus,
        target: DocumentStatus
    ) -> bool:
        """
        检查是否允许从当前状态转入目标状态
        
        Args:
            current: 当前状态枚举
            target: 目标状态枚举
        
        Returns:
            bool: True=允许跳转，False=非法跳转
        """
        if current is target:
            return True  # 相同状态恒允许

        return target in cls._TRANSITION.get(
            current,
            set()
        )

    @classmethod
    def transition(
        cls,
        current: DocumentStatus,
        target: DocumentStatus
    ) -> DocumentStatus:
        """
        执行状态转换校验，通过则返回目标状态，失败抛 ValueError
        
        Args:
            current: 当前状态（支持枚举/字符串两种入参）
            target: 目标状态（支持枚举/字符串两种入参）
        
        Returns:
            DocumentStatus: 标准化后的目标状态枚举
        
        Raises:
            ValueError: 非法转换时抛出，含清晰错误信息
        """
        
        if not cls.can_transition(
            current,
            target
        ):
            raise ValueError(
                f"非法的文档状态转换："
                f"{current.value} -> {target.value}"
            )

        return target