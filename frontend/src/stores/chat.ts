import type { Message, Conversation } from "@/types/chat";
import { createMessage } from "@/utils/chat";
import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";

import { saveChatStorage, loadChatStorage } from "@/services/chatStorage";



export const useChatStore = defineStore('chat', () => {

  /**
   * 我把请求状态和消息状态分开管理。loading 表示当前是否存在进行中的 AI 请求，streamingMessageId 用于定位具体正在生成的消息。这样不仅支持普通发送，也能支持历史消息重新生成，避免依赖消息数组最后一项。
   */

  // AI是否在处理请求loading
  const loading = ref(false)

  // 当前正在流式生成的消息 ID
  const streamingMessageId = ref<string | null>(null)

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
        createMessage('assistant','欢迎使用 AI Developer Assistant', { isWelcome: true })
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

  // 插入消息
  const insertMessage = (index: number, message: Message) => {
    const conversation = currentConversation.value
    if(!conversation) return;
    conversation.messages.splice(index, 0, message)
    conversation.updatedAt = new Date().toISOString()
  }

  // 移除消息 
  const removeMessage = (messageId: string) => {
    const conversation = currentConversation.value
    if(!conversation) return;

    conversation.messages = conversation.messages.filter(v => {
      return v.id !== messageId
    })

    // 如果正在生成的消息被删除，我们应该同步清理
    if (streamingMessageId.value === messageId) {
      streamingMessageId.value = null
    }

    conversation.updatedAt = new Date().toISOString()

  }

  // 获取上一条用户消息
  const getPreviousUserMessage = (messageId: string) => {
    const conversation = currentConversation.value
    if(!conversation) return

    const index = conversation.messages.findIndex(v => v.id === messageId)

    if(index <= 0) return null

    for(let i = index -1; i >= 0; i--) {
      const message = conversation.messages[i]

      if(message?.role === 'user') {
        return message
      }
    }

    return null

  }

  // 追加流式消息内容
  const appendStreamingMessage = (content: string) => {
    const conversation = currentConversation.value
    if(!conversation) return;

    if(!streamingMessageId.value) return

    // 拿到消息列表最后一条消息
    const message = conversation.messages.find(v => v.id === streamingMessageId.value)

    if(!message?.loading) return

    message.content += content

    conversation.updatedAt = new Date().toISOString()

  }

  // 流式请求完成 
  const finishStreamingMessage = () => {
    const conversation = currentConversation.value

    if(!conversation) return

    if(!streamingMessageId.value) return

    const message = conversation.messages.find(v => (v.id === streamingMessageId.value))

    if(!message?.loading) return

    message.loading = false

    conversation.updatedAt = new Date().toISOString()

    // 表示当前没有正在生成的消息
    streamingMessageId.value = null

  }

  // 清空会话消息
  const clearMessages = () => {
    const conversation = currentConversation.value
    if(!conversation) return

    conversation.messages=[
      createMessage(
       'assistant',
       '欢迎使用 AI Developer Assistant',
       {
        isWelcome: true
       }
      )
    ]
    conversation.updatedAt = new Date().toISOString()
  }

  // 设置loading状态
  const setLoading = (state: boolean) => {
    loading.value = state
  }

  // loading时的消息提示 1.默认是插入到消息末尾 => loading切换成AI回答的情况 2.在指定位置插入 重新生成的情况
  const addLoadingMessage = (index?: number) => {

    const message = createMessage('assistant', '', { loading: true })

    if(index === undefined) {
      addMessage(message)
    } else {
      insertMessage(index, message)
    }

    streamingMessageId.value = message.id

  }

  // 替换loading消息提示
  const replaceLoadingMessage = (content: string) => {
    const conversation = currentConversation.value
    if(!conversation) return
    if(!streamingMessageId.value) return

   
    const message = conversation.messages.find(v => v.id === streamingMessageId.value)

    if(!message?.loading) return

    message.loading = false
    message.content = content

    conversation.updatedAt = new Date().toISOString()

    streamingMessageId.value = null
  }


  return {
    loading,
    conversations,
    currentConversation,
    currentConversationId,
    streamingMessageId,
    initConversation,
    createConversation,
    switchConversation,
    deleteConversation,
    updateConversationTitle,
    getPreviousUserMessage,
    addMessage,
    insertMessage,
    removeMessage,
    clearMessages,
    setLoading,
    addLoadingMessage,
    replaceLoadingMessage,
    appendStreamingMessage,
    finishStreamingMessage
  }

})