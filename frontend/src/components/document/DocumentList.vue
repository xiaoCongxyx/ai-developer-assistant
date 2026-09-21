<script setup lang="ts">
import type { Document } from '@/types/document'
import DocumentCard from './DocumentCard.vue'

defineProps<{
  items: Document[]
  loading: boolean
}>()

const emit = defineEmits<{
  delete: [id: number]
  retry: [id: number]
}>()
</script>

<template>
  <div v-loading="loading" element-loading-text="加载中..." class="document-list-wrapper">
    <!-- 空状态 -->
    <el-empty
      v-if="!loading && items.length === 0"
      description="当前知识库还没有文档，点击「上传文档」开始构建知识库"
    />

    <!-- 文档列表 -->
    <div v-else class="document-list">
      <DocumentCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        @delete="emit('delete', $event)"
        @retry="emit('retry', $event)"
      />
    </div>
  </div>
</template>

<style scoped>
/* 容器：预留最小高度、避免布局抖动 */
.document-list-wrapper {
  min-height: 280px;
  margin-bottom: 24px;
}

/* 纵向列表：间距舒适统一 */
.document-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 滚动条适配 — 仅在需要时显示 */
.document-list-wrapper {
  overflow-y: auto;
}

.document-list-wrapper::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.document-list-wrapper::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
  border-radius: 3px;
}

.document-list-wrapper::-webkit-scrollbar-track {
  background: transparent;
}
</style>
