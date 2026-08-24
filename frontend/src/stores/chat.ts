import type { Message, Conversation } from "@/types/chat";
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

  // loading时的消息提示
  const addLoadingMessage = () => {
    messages.value.push({
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      createdAt: new Date().toISOString(),
      loading: true
    })
  }

  const replaceLoadingMessage = (content: string) => {
    const msg = messages.value.find(item => item.loading)

    if(!msg) return;

    msg.loading = false
    msg.content = content
  }


  return {
    loading,
    messages,
    addMessage,
    clearMessages,
    setLoading,
    addLoadingMessage,
    replaceLoadingMessage
  }

})