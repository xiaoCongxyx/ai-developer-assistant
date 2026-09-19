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

const isUser = computed(() => msgProps.message.role === 'user')
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

      <!-- AI 消息操作区 -->
      <div
        v-if="
          msgProps.message.role === 'assistant' &&
          msgProps.message.content &&
          !msgProps.message.loading &&
          !msgProps.message.isWelcome
        "
        class="message-actions"
      >
        <el-button text size="small" @click="copyMessage">复制</el-button>
        <el-button text size="small" type="primary" @click="handleRegenerate">重新生成</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.message {
  display: flex;
  margin-bottom: 20px;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-wrapper {
  max-width: 72%;
  display: flex;
  flex-direction: column;
}

/* 消息气泡 */
.bubble {
  padding: 14px 18px;
  border-radius: 14px;
  line-height: 1.7;
  word-break: break-word;
  transition: all 0.2s ease;
}

/* 用户消息 */
.user .bubble {
  background: var(--el-color-primary);
  color: #ffffff;
  border-bottom-right-radius: 6px;
}

/* AI 消息 */
.assistant .bubble {
  background: var(--el-bg-color);
  color: var(--el-text-color-primary);
  border: 1px solid var(--el-border-color-light);
  border-bottom-left-radius: 6px;
}

/* 思考中 */
.thinking {
  color: var(--el-text-color-secondary);
  font-style: italic;
}

/* 操作按钮区 */
.message-actions {
  display: flex;
  gap: 4px;
  margin-top: 6px;
  padding-left: 8px;
}

/* Markdown 内容适配 */
.bubble :deep(p) {
  margin: 0 0 8px;
}
.bubble :deep(p:last-child) {
  margin-bottom: 0;
}
.bubble :deep(pre) {
  margin: 10px 0;
  border-radius: 8px;
}
</style>
