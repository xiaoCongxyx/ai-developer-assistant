from collections.abc import Generator
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    获取数据库 Session。

    每个请求创建一个 Session，
    请求结束后关闭。
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()