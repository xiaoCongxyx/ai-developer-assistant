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
}>()

const handleEdit = (prompt: Prompt) => {
  emit('edit', prompt)
}

const handleDelete = (prompt: Prompt) => {
  emit('delete', prompt)
}
</script>

<template>
  <div class="prompt-list">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="4" animated />
    </div>

    <el-empty v-else-if="prompts.length === 0" description="暂无 Prompt" />

    <div v-else class="prompt-items">
      <PromptCard
        v-for="prompt in prompts"
        :key="prompt.id"
        :prompt="prompt"
        @edit="handleEdit(prompt)"
        @delete="handleDelete(prompt)"
      />
    </div>
  </div>
</template>

<style scoped>
.prompt-list {
  width: 100%;
}

.loading-container {
  padding: 24px;
}

.prompt-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
