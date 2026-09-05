<script setup lang="ts">
import type { Prompt } from '@/types/prompt'

defineProps<{
  prompt: Prompt
}>()

const emit = defineEmits<{
  edit: []
  delete: []
}>()

const handleEdit = () => {
  emit('edit')
}

const handleDelete = () => {
  emit('delete')
}
</script>

<template>
  <el-card class="prompt-card" shadow="hover">
    <div class="prompt-card-header">
      <div class="prompt-info">
        <div class="prompt-title">
          {{ prompt.name }}

          <el-tag v-if="prompt.is_default" type="success" size="small"> 默认 </el-tag>
        </div>

        <div class="prompt-description">
          {{ prompt.description || '暂无描述' }}
        </div>
      </div>

      <div class="prompt-actions">
        <el-button size="small" @click="handleEdit"> 编辑 </el-button>

        <el-button v-if="!prompt.is_default" size="small" type="danger" plain @click="handleDelete">
          删除
        </el-button>
      </div>
    </div>

    <el-divider />

    <div class="prompt-content">
      {{ prompt.content }}
    </div>
  </el-card>
</template>

<style scoped>
.prompt-card {
  border-radius: 8px;
}

.prompt-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.prompt-info {
  min-width: 0;
}

.prompt-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 16px;
  font-weight: 600;
}

.prompt-description {
  color: var(--text-secondary);
  font-size: 14px;
}

.prompt-actions {
  display: flex;
  flex-shrink: 0;
  gap: 8px;
}

.prompt-content {
  max-height: 160px;
  overflow-y: auto;
  padding: 12px;
  border-radius: 6px;
  background-color: var(--bg-page);
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.6;
}
</style>
