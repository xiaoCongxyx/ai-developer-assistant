<script setup lang="ts">
import ChatHeader from '@/components/chat/ChatHeader.vue';
import ChatInput from '@/components/chat/ChatInput.vue';
import ChatWindow from '@/components/chat/ChatWindow.vue';

import { ref } from 'vue';

import type { Message } from '@/types/chat';

const messages = ref<Message[]>([
  {
    id: crypto.randomUUID(),
    role: 'assistant',
    content: '欢迎使用 AI Developer Assistant',
    createdAt: new Date().toISOString(),
  },
])

const handleSend = (content: string) => {
  if(!content.trim()) return;

  // 把客户的问题push到消息列表中去
  messages.value.push({
    id: crypto.randomUUID(),
    role: 'user',
    content,
    createdAt: new Date().toISOString()
  })

  // 模拟ai回应
  setTimeout(() => {
    messages.value.push({
      id: crypto.randomUUID(),
      role: 'assistant',
      content: `收到你的问题：${content}`,
      createdAt: new Date().toISOString()
    })
  }, 1500);
}

</script>

<template>
<div class="chat-page">
  <ChatHeader />

  <ChatWindow :messages = "messages" />

  <ChatInput @send="handleSend" />
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