<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  send: [content: string]
  stop: []
}>()

// 用来维护发送按钮状态 防止用户重复发送
const props = defineProps<{ loading: boolean }>()

const inputValue = ref('')

const sendMsg = () => {
  const content = inputValue.value.trim()

  if (!content) return
  emit('send', content)

  inputValue.value = ''
}

const handleKeyDown = (event: KeyboardEvent) => {
  // Enter 发送
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
      <span class="tip"> Enter 发送 · Shift + Enter 换行 </span>

      <el-button v-if="!loading" type="primary" :loading="loading" @click="sendMsg">
        发送
      </el-button>
      <el-button v-else type="danger" @click="emit('stop')"> 停止生成 </el-button>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  padding: 16px 20px;

  background: var(--bg-card);

  border-top: 1px solid var(--border-light);
}

.el-textarea {
  width: 100%;
}

.input-footer {
  margin-top: 10px;

  display: flex;

  justify-content: space-between;

  align-items: center;
}

.tip {
  font-size: 12px;

  color: var(--text-placeholder);
}
</style>
