<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import ConversationItem from './ConversationItem.vue'
import { Plus } from '@element-plus/icons-vue'

const chatStore = useChatStore()

const createChat = () => {
  chatStore.createConversation()
}

const handleSelect = (id: string) => {
  chatStore.switchConversation(id)
}

const handleDelete = (id: string) => {
  chatStore.deleteConversation(id)
}
</script>

<template>
  <div class="conversation">
    <!-- 新建对话按钮 -->
    <el-button type="primary" :icon="Plus" class="new-chat" @click="createChat">
      新建对话
    </el-button>

    <!-- 分组标题 -->
    <div class="section-title">聊天记录</div>

    <!-- 会话列表 -->
    <div class="list-wrapper">
      <ConversationItem
        v-for="item in chatStore.conversations"
        :key="item.id"
        :conversation="item"
        :active="item.id === chatStore.currentConversationId"
        @select="handleSelect(item.id)"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<style scoped>
.conversation {
  padding: 16px 12px;
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 新建对话按钮 */
.new-chat {
  width: 100%;
  height: 40px;
  border-radius: 10px;
  justify-content: center;
  font-weight: 500;
}

/* 分组标题 */
.section-title {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  padding: 8px 12px 4px;
  margin-top: 4px;
}

/* 列表容器 */
.list-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* 滚动条适配明暗 */
.conversation::-webkit-scrollbar {
  width: 4px;
}
.conversation::-webkit-scrollbar-thumb {
  background: var(--el-border-color-lighter);
  border-radius: 2px;
}
.conversation::-webkit-scrollbar-track {
  background: transparent;
}
</style>
