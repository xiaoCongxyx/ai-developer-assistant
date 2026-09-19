<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import { Plus } from '@element-plus/icons-vue'

const chatStore = useChatStore()

const handleNewChat = () => {
  chatStore.createConversation()
}
</script>

<template>
  <div class="chat-header">
    <h2 class="title">
      {{ chatStore.currentConversation?.title || 'AI Chat' }}
    </h2>
    <el-button type="primary" :icon="Plus" @click="handleNewChat"> 新建对话 </el-button>
  </div>
</template>

<style scoped>
.chat-header {
  height: 60px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--el-border-color-lighter);
  background: var(--el-bg-color);
}

.title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  letter-spacing: 0.3px;
}
</style>
