import type { Message, MessageRole } from "@/types/chat";

export const createMessage = (role: MessageRole, content: string, options?: Partial<Message>): Message => ({
  id: crypto.randomUUID(),
  role,
  content,
  createdAt: new Date().toISOString(),
  ...options
})