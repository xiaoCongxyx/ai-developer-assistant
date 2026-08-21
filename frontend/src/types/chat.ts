export type messageRole = 'user' | 'assistant'

export interface Message {
  id: string

  role: messageRole

  content: string

  createdAt: string 
}

export interface Conversation {
  id: string

  title: string

  createdAt: string

  updatedAt: string
}