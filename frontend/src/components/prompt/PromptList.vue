<script setup lang="ts">
import type { Prompt } from '@/types/prompt'
import PromptCard from './PromptCard.vue'

defineProps<{
  prompts: Prompt[]
  loading: boolean
}>()

const emit = defineEmits<{
  edit: [prompt: Prompt]
  delete: [prompt: Prompt]
  setDefault: [prompt: Prompt]
}>()

const handleEdit = (prompt: Prompt) => emit('edit', prompt)
const handleDelete = (prompt: Prompt) => emit('delete', prompt)
const handleSetDefault = (prompt: Prompt) => emit('setDefault', prompt)
</script>

<template>
  <div class="prompt-list">
    <!-- 加载中：骨架屏 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="4" animated />
    </div>

    <!-- 空列表：友好提示 -->
    <el-empty v-else-if="prompts.length === 0" description="暂无 Prompt" />

    <!-- 列表：卡片流式布局 -->
    <div v-else class="prompt-items">
      <PromptCard
        v-for="prompt in prompts"
        :key="prompt.id"
        :prompt="prompt"
        @edit="handleEdit(prompt)"
        @delete="handleDelete(prompt)"
        @set-default="handleSetDefault(prompt)"
      />
    </div>
  </div>
</template>

<style scoped>
.prompt-list {
  width: 100%;
}

/* 骨架屏容器 */
.loading-container {
  padding: 20px 8px;
}

/* 卡片列表容器 */
.prompt-items {
  display: flex;
  flex-direction: column;
  gap: 12px; /* 卡片间距更紧凑、更协调 */
}

/* 空状态居中微调 */
:deep(.el-empty) {
  margin: 40px 0;
}
</style>
