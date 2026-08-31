export type MessageRole = 'user' | 'assistant'

export interface Message {
  id: string

  role: MessageRole

  content: string

  createdAt: string 

  loading?: boolean

  isWelcome?: boolean
}

export interface Conversation {
  id: string

  title: string

  createdAt: string

  updatedAt: string

  messages: Message[]
}