import type { Message } from "@/types/chat";
import { defineStore } from "pinia";
import { ref } from "vue";



export const useChatStore = defineStore('chat', () => {
  const loading = ref(false)

  // 消息列表
  const messages = ref<Message[]>([
    {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '欢迎使用 AI Developer Assistant',
      createdAt: new Date().toISOString()
    }
  ])

  // 消息列表增加消息
  const addMessage = (message: Message) => {
    messages.value.push(message)
  }

  // 清空消息列表
  const clearMessages = () => {
    messages.value = []
  }

  const setLoading = (state: boolean) => {
    loading.value = state
  }


  return {
    loading,
    messages,
    addMessage,
    clearMessages,
    setLoading
  }

})