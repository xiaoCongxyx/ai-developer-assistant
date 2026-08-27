import type { Message, Conversation } from "@/types/chat";
import { createMessage } from "@/utils/chat";
import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";

import { saveChatStorage, loadChatStorage } from "@/services/chatStorage";



export const useChatStore = defineStore('chat', () => {

  // AI是否在处理请求loading
  const loading = ref(false)

  // 所有会话
  const conversations = ref<Conversation[]>([])

  // 当前会话
  const currentConversationId = ref('')

  // 当前会话对象
  const currentConversation = computed(() => conversations.value.find(conversation => conversation.id === currentConversationId.value))

  // 初始化会话对象
  const initConversation = () => {
    const data = loadChatStorage()

    if(!data || data.conversations.length === 0) {
      createConversation()
      return
    }

    conversations.value = data.conversations

    const currentEists = data.conversations.some(
      item => item.id === data.currentConversationId
    )

    
    if(currentEists) {
      currentConversationId.value = data.currentConversationId
      return
    }
    const firstConversation = data.conversations[0]

    if(firstConversation) {
      currentConversationId.value = firstConversation.id
    }

  }

  // watch监听自动保存  
  watch([conversations, currentConversationId], () => {
    saveChatStorage({
      conversations: conversations.value,
      currentConversationId: currentConversationId.value
    })
  },{deep: true})
  

  // 创建会话
  const createConversation = (title = '新聊天') => {
    const now = new Date().toISOString()

    const conversation: Conversation = {
      id: crypto.randomUUID(),
      title,
      createdAt: now,
      updatedAt: now,
      messages: [
        createMessage('assistant','欢迎使用 AI Developer Assistant')
      ]
    }

    conversations.value.unshift(conversation)

    currentConversationId.value = conversation.id

    return conversation

  }

  // 切换会话
  const switchConversation = (conversationId: string) => {
    const conversation = conversations.value.find(item => item.id === conversationId)

    if(!conversation) return;

    currentConversationId.value = conversation.id

  }

  // 删除会话
  const deleteConversation = (conversationId: string) => {
    conversations.value = conversations.value.filter(
      item => item.id !== conversationId
    )

    if(currentConversationId.value === conversationId) {
      // 删除最后一条会话的时候需要自动创建新对话
      const nextConversation = conversations.value[0]
      if(nextConversation) {
        currentConversationId.value = nextConversation.id
      } else {
        createConversation()
      }
    }

  }

  // 更新会话标题
  const updateConversationTitle = (title: string) => {
    const conversation = currentConversation.value

    if(!conversation) return

    conversation.title = title
    conversation.updatedAt = new Date().toISOString()
  }

  // 消息列表增加消息
  const addMessage = (message: Message) => {
    const conversation = currentConversation.value
    if(!conversation) return

    conversation.messages.push(message)
    conversation.updatedAt = new Date().toISOString()
  }

  // 追加流式消息内容
  const appendStreamingMessage = (content: string) => {
    const conversation = currentConversation.value
    if(!conversation) return;

    // 拿到消息列表最后一条消息
    const message = conversation.messages[conversation.messages.length - 1]

    if(!message?.loading) return

    message.content += content

    conversation.updatedAt = new Date().toISOString()

  }

  // 清空会话消息
  const clearMessages = () => {
    const conversation = currentConversation.value
    if(!conversation) return

    conversation.messages=[
      createMessage(
       'assistant',
       '欢迎使用 AI Developer Assistant'
      )
    ]
  }

  // 设置loading状态
  const setLoading = (state: boolean) => {
    loading.value = state
  }

  // loading时的消息提示
  const addLoadingMessage = () => {
    addMessage(
      createMessage('assistant', '', { loading: true })
    )
  }

  // 替换loading消息提示
  const replaceLoadingMessage = (content: string) => {
    const conversation = currentConversation.value
    if(!conversation) return

    // 相当于conversation.messages.findLast()，但是findLast需要较新的ES配置
    const message = [...conversation.messages].reverse().find(item => item.loading)

    if(!message?.loading) return

    message.loading = false
    message.content = content

    conversation.updatedAt = new Date().toISOString()
  }


  return {
    loading,
    conversations,
    currentConversation,
    currentConversationId,
    initConversation,
    createConversation,
    switchConversation,
    deleteConversation,
    updateConversationTitle,
    addMessage,
    clearMessages,
    setLoading,
    addLoadingMessage,
    replaceLoadingMessage,
    appendStreamingMessage
  }

})