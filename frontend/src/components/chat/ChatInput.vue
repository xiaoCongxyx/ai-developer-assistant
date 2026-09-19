<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  send: [content: string]
  stop: []
}>()

const props = defineProps<{ loading: boolean }>()
const inputValue = ref('')

const sendMsg = () => {
  const content = inputValue.value.trim()
  if (!content) return
  emit('send', content)
  inputValue.value = ''
}

const handleKeyDown = (event: KeyboardEvent) => {
  // Enter 发送 · Shift+Enter 换行
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMsg()
  }
}
</script>

<template>
  <div class="chat-input">
    <el-input
      v-model="inputValue"
      type="textarea"
      :rows="3"
      placeholder="请输入你的问题..."
      @keydown="handleKeyDown"
    />
    <div class="input-footer">
      <span class="tip">Enter 发送 · Shift + Enter 换行</span>
      <el-button v-if="!loading" type="primary" @click="sendMsg"> 发送 </el-button>
      <el-button v-else type="danger" @click="emit('stop')"> 停止生成 </el-button>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  padding: 16px 24px;
  background: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color-lighter);
}

.el-textarea {
  width: 100%;
}

:deep(.el-textarea__inner) {
  border-radius: 10px;
  border-color: var(--el-border-color-light);
  transition: all 0.2s ease;
  resize: none;
}

:deep(.el-textarea__inner:focus) {
  border-color: var(--el-color-primary);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

.input-footer {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tip {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
}
</style>
