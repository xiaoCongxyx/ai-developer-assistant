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

  chatStore.setLoading(true)
  // chatStore.addLoadingMessage()

  // 模拟ai回应
  try {
    chatStore.addLoadingMessage()
    // 非流式请求
    // const res = await sendChatMessage({
    //   message: content,
    // })

    // chatStore.replaceLoadingMessage(res.content)
    abortController = new AbortController()

    // 流式请求返回结果
    await streamChatMessage(
      { message: content },
      (chunk) => {
        chatStore.appendStreamingMessage(chunk)
      },
      abortController.signal,
    )
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
</script>

<template>
  <div class="chat-page">
    <ChatHeader />

    <ChatWindow />

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
