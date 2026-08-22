from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
  content = await chat(request.message)

  return ChatResponse(
    success=True,
    content=content,
  )