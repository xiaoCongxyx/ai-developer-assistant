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