<script setup lang="ts">
import ChatHeader from '@/components/chat/ChatHeader.vue';
import ChatInput from '@/components/chat/ChatInput.vue';
import ChatWindow from '@/components/chat/ChatWindow.vue';

import { useChatStore } from '@/stores/chat';
import { createMessage } from '@/utils/chat';

import { sendChatMessage } from '@/api/chat';

const chatStore = useChatStore()


const handleSend = async (content: string) => {
  if(!content.trim()) return;
  // 防止重复发送
  if(chatStore.loading) return;

  // 把客户的问题push到消息列表中去
  chatStore.addMessage(
    createMessage('user',content)
  )
  // chatStore.addMessage({
  //   id: crypto.randomUUID(),
  //   role: 'user',
  //   content,
  //   createdAt: new Date().toISOString()
  // })

  chatStore.setLoading(true)
  // chatStore.addLoadingMessage()

  // 模拟ai回应
  try {
    // setTimeout(() => {
    //   chatStore.addMessage(createMessage('assistant', `收到你的问题：${content}`))
    //   chatStore.setLoading(false)
    // }, 1500);
    chatStore.addLoadingMessage()
    const res = await sendChatMessage({
      message: content
    })
    
    chatStore.replaceLoadingMessage(res.content)
  } catch (error) {
    console.error(error)
    // 错误提示处理
    chatStore.replaceLoadingMessage('服务器连接失败，请稍后重试。')
  } finally {
    chatStore.setLoading(false)
  }
}

</script>

<template>
<div class="chat-page">
  <ChatHeader />

  <ChatWindow />

  <ChatInput :loading = "chatStore.loading" @send="handleSend" />
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