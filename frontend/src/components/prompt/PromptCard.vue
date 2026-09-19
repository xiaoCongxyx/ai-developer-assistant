<script setup lang="ts">
import type { Prompt } from '@/types/prompt'

defineProps<{
  prompt: Prompt
}>()

const emit = defineEmits<{
  edit: []
  delete: []
  setDefault: []
}>()

const handleEdit = () => emit('edit')
const handleDelete = () => emit('delete')
const handleSetDefault = () => emit('setDefault')
</script>

<template>
  <el-card class="prompt-card" shadow="hover">
    <!-- 头部：名称 + 操作 -->
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
        <el-button size="small" @click="handleEdit">编辑</el-button>
        <el-button v-if="!prompt.is_default" size="small" type="danger" plain @click="handleDelete">
          删除
        </el-button>
        <el-button v-if="!prompt.is_default" type="primary" link @click="handleSetDefault">
          设为默认
        </el-button>
      </div>
    </div>

    <!-- 分割线 -->
    <el-divider />

    <!-- 正文预览 -->
    <div class="prompt-content">
      {{ prompt.content }}
    </div>
  </el-card>
</template>

<style scoped>
.prompt-card {
  border-radius: 12px; /* ✅ 统一全局圆角 */
  border: 1px solid var(--el-border-color-lighter);
  background: var(--el-bg-color);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

/* 头部布局 */
.prompt-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.prompt-info {
  min-width: 0; /* ✅ 允许名称超长省略，不挤按钮 */
}

.prompt-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 15px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.prompt-description {
  color: var(--el-text-color-secondary);
  font-size: 13px;
  line-height: 1.4;
}

/* 按钮区：固定在右侧不压缩 */
.prompt-actions {
  display: flex;
  flex-shrink: 0;
  gap: 6px;
}

/* 正文预览区 */
.prompt-content {
  max-height: 160px;
  overflow-y: auto;
  padding: 14px 16px;
  border-radius: 8px;
  background-color: var(--el-fill-color-light); /* ✅ 明暗自动适配 */
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--el-text-color-regular);
  font-size: 14px;
  line-height: 1.6;
}

/* 预览区滚动条 */
.prompt-content::-webkit-scrollbar {
  width: 4px;
}
.prompt-content::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 2px;
}
</style>
