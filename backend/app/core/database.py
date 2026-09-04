from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite 数据库文件
DATABASE_URL = "sqlite:///./ai_developer_assistant.db"

# ⭐ 创建数据库 Engine
# Engine 可以理解成：
# SQLAlchemy 和数据库之间的连接入口。
engine = create_engine(
  DATABASE_URL,
  connect_args={
    # SQLite 在 FastAPI 多线程环境下需要这个配置
    "check_same_thread": False
  }
)

# 创建数据库 Session
#
# Session 可以理解成：
# 我们操作数据库时使用的“工作会话”。
SessionLocal = sessionmaker(
  bind=engine,
  autoflush=False,
)