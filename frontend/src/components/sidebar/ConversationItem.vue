<script setup lang="ts">
import type { Conversation } from '@/types/chat'
import { Close } from '@element-plus/icons-vue'

const props = defineProps<{
  conversation: Conversation
  active: boolean
}>()

const emit = defineEmits<{
  select: []
  delete: [id: string]
}>()

const handleClick = () => {
  emit('select')
}

const handleDelete = (e: MouseEvent) => {
  e.stopPropagation() // 阻止冒泡 → 不触发选中
  emit('delete', props.conversation.id)
}
</script>

<template>
  <div class="conversation-item" :class="{ active }" @click="handleClick">
    <span class="title">{{ conversation.title }}</span>
    <el-button text :icon="Close" class="delete-btn" @click="handleDelete" />
  </div>
</template>

<style scoped>
.conversation-item {
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

/* 悬停态 */
.conversation-item:hover {
  background: var(--el-fill-color-light);
}

/* 选中态 */
.conversation-item.active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  font-weight: 500;
}

/* 标题文本：超长省略 */
.title {
  flex: 1;
  min-width: 0;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  line-height: 1.5;
}

/* 删除按钮：hover 才显示，更干净 */
.delete-btn {
  opacity: 0;
  transition: opacity 0.15s ease;
  padding: 2px;
  font-size: 14px;
}
.conversation-item:hover .delete-btn {
  opacity: 0.7;
}
.conversation-item:hover .delete-btn:hover {
  opacity: 1;
  color: var(--el-color-danger);
}
</style>
