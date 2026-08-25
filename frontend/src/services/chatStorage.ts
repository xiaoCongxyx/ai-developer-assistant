import type { Conversation } from '@/types/chat'
import { storage } from '@/utils/storage'
import { STORAGE_KEYS } from '@/utils/storage/keys'

export interface ChatStorageData {
  conversations: Conversation[]
  currentConversationId: string
}

export const saveChatStorage = (
  data: ChatStorageData
) => {
  storage.set(STORAGE_KEYS.CHAT, data)
}

export const loadChatStorage = (): ChatStorageData | null => {
  return storage.get<ChatStorageData>(
    STORAGE_KEYS.CHAT
  )
}

export const clearChatStorage = () => {
  storage.remove(STORAGE_KEYS.CHAT)
}