import request from "@/utils/request"

export interface ChatRequest {
  message: string
}

export interface ChatResponse {
  success: boolean,
  content: string
}

export const sendChatMessage = (data: ChatRequest): Promise<ChatResponse> => {
  return request.post('/chat', data)
}


// 流式聊天
export const streamChatMessage = async (
  data: ChatRequest, onChunk: (chunk: string) => void
) => {
  const response = await fetch(
    'http://127.0.0.1:8000/chat/stream',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }
  )

  if(!response.ok) {
    throw new Error(`HTTP ERROR: ${response.status}`)
  }

  if(!response.body) {
    throw new Error('ReadableStream 不存在')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')

  while(true) {
    const { done, value } = await reader.read()
    if(done) break;

    const chunk = decoder.decode(value, {stream: true})
    onChunk(chunk)
  }

}