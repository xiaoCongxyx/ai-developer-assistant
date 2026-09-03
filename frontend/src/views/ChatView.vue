<script setup lang="ts">
import ChatHeader from '@/components/chat/ChatHeader.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'

import { useChatStore } from '@/stores/chat'
import { createMessage } from '@/utils/chat'

import { sendChatMessage, streamChatMessage } from '@/api/chat'
import { generateTitle } from '@/utils/conversation'

const chatStore = useChatStore()

// 终止请求
let abortController: AbortController | null = null

// 停止生成handle
const stopGenerating = () => {
  abortController?.abort()
}

// 抽离AI接口调用逻辑  负责公共的 AI 生成流程。
const generateAIResponse = async (content: string, loadingIndex?: number) => {
  chatStore.setLoading(true)
  // chatStore.addLoadingMessage()

  // 模拟ai回应
  try {
    if (loadingIndex === undefined) {
      chatStore.addLoadingMessage()
    } else {
      chatStore.addLoadingMessage(loadingIndex)
    }

    abortController = new AbortController()

    // 当前消息已经加入 Pinia，因此需要排除最后一条消息。
    // 最后一条就是用户刚刚发送的问题。
    const history =
      chatStore.currentConversation?.messages
        .filter((v) => !v.loading)
        .slice(0, -1)
        .map((v) => ({
          role: v.role,
          content: v.content,
        })) ?? []

    // 流式请求返回结果
    await streamChatMessage(
      { message: content, history },
      (chunk) => {
        chatStore.appendStreamingMessage(chunk)
      },
      abortController.signal,
    )
    // 完成流式请求后要设置loading状态
    chatStore.finishStreamingMessage()
  } catch (error) {
    // 如果错误类型是AbortError 代表是用户终止接口 不是接口出错 用户主动停止，不属于异常
    if (error instanceof DOMException && error.name === 'AbortError') return

    console.error(error)
    // 错误提示处理
    chatStore.replaceLoadingMessage('服务器连接失败，请稍后重试。')
  } finally {
    chatStore.setLoading(false)
    abortController = null
  }
}

// 重新生成
const handleRegenerate = async (id: string) => {
  if (chatStore.loading) return

  const conversation = chatStore.currentConversation

  if (!conversation) return

  const index = conversation.messages.findIndex((v) => v.id === id)

  if (index === -1) return

  const userMessage = chatStore.getPreviousUserMessage(id)

  if (!userMessage) return

  // 删除旧的AI回复
  chatStore.removeMessage(id)

  // 在旧 AI 消息的位置重新生成
  await generateAIResponse(userMessage.content, index)
}

// 测试流式数据
const testStream = async () => {
  const res = await streamChatMessage(
    {
      message: '你好',
    },
    (chunk) => {
      console.log(`收到 chunk：${chunk}`)
    },
  )
}

const handleSend = async (content: string) => {
  if (!content.trim()) return
  // 防止重复发送
  if (chatStore.loading) return

  // ⭐ 第一条消息生成标题
  const conversation = chatStore.currentConversation

  if (conversation && conversation.title === '新聊天' && conversation.messages.length === 1) {
    chatStore.updateConversationTitle(generateTitle(content))
  }

  // 把客户的问题push到消息列表中去
  chatStore.addMessage(createMessage('user', content))

  await generateAIResponse(content)
}
</script>

<template>
  <div class="chat-page">
    <ChatHeader />

    <ChatWindow @regenerate="handleRegenerate" />

    <ChatInput :loading="chatStore.loading" @send="handleSend" @stop="stopGenerating" />
  </div>
</template>

<style scoped>
.chat-page {
  height: 100%;

  display: flex;
  flex-direction: column;

  overflow: hidden;

  background: var(--bg-page);
}
</style>
