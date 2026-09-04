from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.prompt import router as prompt_router
from app.core.database_init import init_database

app = FastAPI(
    title="AI Developer Assistant API",
    version='1.0.0',
)

# ⭐ 应用启动时初始化数据库
init_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]  
)

# 注册api路由
app.include_router(chat_router)
app.include_router(prompt_router)