<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import ConversationItem from './ConversationItem.vue'

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
    <button class="new-chat" @click="createChat">+ 新建聊天</button>

    <div class="title">聊天记录</div>

    <ConversationItem
      v-for="item in chatStore.conversations"
      :key="item.id"
      :conversation="item"
      :active="item.id === chatStore.currentConversationId"
      @select="handleSelect(item.id)"
      @delete="handleDelete"
    />
  </div>
</template>

<style scoped>
.conversation {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
}

.new-chat {
  width: 100%;
  height: 40px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: white;
  cursor: pointer;
}

.title {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 20px 0 10px;
}
</style>
