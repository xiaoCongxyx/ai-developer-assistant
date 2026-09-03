from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import chat, chat_stream

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
  content = await chat(request.message, request.history)

  return ChatResponse(
    success=True,
    content=content,
  )

@router.post('/chat/stream')
async def chat_stream_api(request: ChatRequest):

  return StreamingResponse(
    chat_stream(request.message, request.history),
    media_type="text/plain",
  )