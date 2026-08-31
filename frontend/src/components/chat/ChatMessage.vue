<script setup lang="ts">
import type { Message } from '@/types/chat'
import md from '@/utils/markdown'
import { computed } from 'vue'

const msgProps = defineProps<{
  message: Message
}>()

const emit = defineEmits<{
  regenerate: []
}>()

const htmlContent = computed(() => {
  return md.render(msgProps.message.content)
})

// 复制消息
const copyMessage = async () => {
  try {
    await navigator.clipboard.writeText(msgProps.message.content)
  } catch (error) {
    console.error('复制失败', error)
  }
}

const handleRegenerate = () => {
  emit('regenerate')
}

const isUser = computed(() => {
  return msgProps.message.role === 'user'
})
</script>

<template>
  <div class="message" :class="msgProps.message.role">
    <div class="message-wrapper">
      <div class="bubble markdown-body">
        <div v-if="msgProps.message.loading && !msgProps.message.content" class="thinking">
          AI 正在思考...
        </div>

        <div v-else v-html="htmlContent"></div>
      </div>

      <!-- AI 消息操作 -->
      <div
        v-if="
          msgProps.message.role === 'assistant' &&
          msgProps.message.content &&
          !msgProps.message.loading &&
          !msgProps.message.isWelcome
        "
        class="message-actions"
      >
        <button @click="copyMessage">复制</button>

        <button @click="handleRegenerate">重新生成</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-wrapper {
  max-width: 70%;
}

.message-actions {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}

.message-actions button {
  padding: 3px 6px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
}

.message-actions button:hover {
  color: var(--color-primary);
}

.bubble {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  word-break: break-word;
}

.user .bubble {
  background: var(--color-primary);
  color: white;
}

.assistant .bubble {
  background: white;
  border: 1px solid var(--border-color);
}

.thinking {
  color: #909399;
  font-style: italic;
}
</style>
