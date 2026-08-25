<script setup lang="ts">
import type { Conversation } from '@/types/chat'

const props = defineProps<{ conversation: Conversation; active: boolean }>()
const emit = defineEmits<{
  select: []
  delete: [id: string]
}>()

const handleClick = () => {
  emit('select')
}

const handleDelete = () => {
  emit('delete', props.conversation.id)
}
</script>

<template>
  <div class="conversation-item" :class="{ active }" @click="handleClick">
    <span class="title">{{ conversation.title }}</span>
    <button class="delete-btn" @click.stop="handleDelete">×</button>
  </div>
</template>

<style scoped>
.conversation-item {
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.conversation-item:hover {
  background: var(--bg-sidebar-hover);
}

.conversation-item.active {
  background: var(--color-primary);
  color: white;
}

.title {
  flex: 1;
  min-width: 0;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-btn {
  opacity: 0;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 18px;
  color: #999;
}

.conversation-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: red;
}
</style>
