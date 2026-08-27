<script setup lang="ts">
import type { Message } from '@/types/chat'
import md from '@/utils/markdown'
import { computed } from 'vue'

const msgProps = defineProps<{
  message: Message
}>()

const htmlContent = computed(() => {
  return md.render(msgProps.message.content)
})

const isUser = computed(() => {
  return msgProps.message.role === 'user'
})
</script>

<template>
  <div class="message" :class="msgProps.message.role">
    <div class="bubble markdown-body">
      <div v-if="msgProps.message.loading && !msgProps.message.content" class="thinking">
        AI 正在思考...
      </div>
      <div v-else v-html="htmlContent"></div>
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

.bubble {
  max-width: 70%;

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
