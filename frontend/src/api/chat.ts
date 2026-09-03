import request from "@/utils/request"

// 前端真正传给后端的消息，不需要携带 id、createdAt、loading 等 UI 信息。
// 这些属于前端状态，而不是 LLM 对话数据。
// 在 API 层定义了独立的 DTO，避免前后端数据模型强耦合。
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}
export interface ChatRequest {
  // 当前用户正在发送的问题
  message: string
  // 当前问题之前的历史消息
  history: ChatMessage[]
}

export interface ChatResponse {
  success: boolean
  content: string
}

export const sendChatMessage = (data: ChatRequest): Promise<ChatResponse> => {
  return request.post('/chat', data)
}


// 流式聊天
export const streamChatMessage = async (
  data: ChatRequest, onChunk: (chunk: string) => void, signal?: AbortSignal
) => {
  const response = await fetch(
    'http://127.0.0.1:8000/chat/stream',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
      signal
    },
  )

  if(!response.ok) {
    throw new Error(`HTTP ERROR: ${response.status}`)
  }

  if(!response.body) {
    throw new Error('ReadableStream 不存在')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')

  try {
    while(true) {
      const { done, value } = await reader.read()
      if(done) break;
  
      const chunk = decoder.decode(value, {stream: true})
      onChunk(chunk)
    }
  } catch (error) {
    reader.releaseLock()
  }

}