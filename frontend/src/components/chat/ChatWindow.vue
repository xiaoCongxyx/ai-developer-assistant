<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import ChatMessage from './ChatMessage.vue';
import { useChatStore } from '@/stores/chat.ts';


const chatStore = useChatStore()

const chatWindowDom = ref<HTMLDivElement>()

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()

  if(!chatWindowDom.value) return;

  // chatWindowDom.value.scrollTop = chatWindowDom.value.scrollHeight
  chatWindowDom.value.scrollTo({
    top: chatWindowDom.value.scrollHeight,
    behavior: 'smooth' 
  })

}

// 监听消息列表的变化 来决定是否需要自动滚动
watch(
  () => chatStore.messages.length,
  () => {
    scrollToBottom()
  },
  {
    immediate: true
  }
)

</script>

<template>
  <div class="chat-window" ref="chatWindowDom">
    <ChatMessage
      v-for="message in chatStore.messages"
      :key="message.id"
      :message="message"
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
}
</style>