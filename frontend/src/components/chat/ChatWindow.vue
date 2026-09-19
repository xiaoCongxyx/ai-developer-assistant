<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import ChatMessage from './ChatMessage.vue'
import { useChatStore } from '@/stores/chat.ts'

const chatStore = useChatStore()

const chatWindowDom = ref<HTMLDivElement>()

const emit = defineEmits<{
  regenerate: [messageId: string]
}>()

// 判断是否靠近底部：误差范围内视为"在底部"
const isNearBottom = (el: HTMLElement) => {
  const { scrollTop, clientHeight, scrollHeight } = el
  return scrollHeight - scrollTop - clientHeight < 150
}

// 智能滚动：仅当用户在底部时才自动滚到底
const scrollToBottom = async (force = false) => {
  await nextTick()

  const el = chatWindowDom.value

  if (!el) return

  // 用户正在向上浏览 → 不强制滚动
  if (!force && !isNearBottom(el)) return

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
  async (_, oldList) => {
    // 初始化或切换会话 → 强制滚到底
    if (!oldList || oldList.length === 0) {
      await scrollToBottom(true)
    } else {
      // 新增消息 → 智能判断是否跟随
      await scrollToBottom(false)
    }
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
  gap: 4px;
  overflow-y: auto;
  scroll-behavior: smooth;
  overflow-anchor: none; /* 防止浏览器自动锚定导致跳动 */
  background: var(--el-bg-color-page);
}

/* ✅ 滚动条样式适配明暗模式 */
.chat-window::-webkit-scrollbar {
  width: 6px;
}
.chat-window::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
  border-radius: 3px;
}
.chat-window::-webkit-scrollbar-track {
  background: transparent;
}
</style>
