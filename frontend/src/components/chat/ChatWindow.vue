<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import ChatMessage from './ChatMessage.vue'
import { useChatStore } from '@/stores/chat.ts'

const chatStore = useChatStore()

const chatWindowDom = ref<HTMLDivElement>()

const emit = defineEmits<{
  regenerate: [messageId: string]
}>()

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()

  const el = chatWindowDom.value

  if (!el) return

  // 用requestAnimationFrame是因为有时候DOM更新了，但是浏览器布局还没完成，使用requestAnimationFrame等待浏览器下一次绘制更加稳定
  requestAnimationFrame(() => {
    el.scrollTo({
      top: el.scrollHeight,
      behavior: 'smooth',
    })
  })
}

// 监听消息列表的变化 来决定是否需要自动滚动
watch(
  () => chatStore.currentConversation?.messages,
  () => {
    scrollToBottom()
  },
  {
    deep: true,
    immediate: true,
  },
)
</script>

<template>
  <div class="chat-window" ref="chatWindowDom">
    <ChatMessage
      v-for="message in chatStore.currentConversation?.messages"
      :key="message.id"
      :message="message"
      @regenerate="emit('regenerate', message.id)"
    />
  </div>
</template>

<style scoped>
.chat-window {
  flex: 1;
  min-height: 0;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  scroll-behavior: smooth;
  overflow-anchor: none;
}
</style>
