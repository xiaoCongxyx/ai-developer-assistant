<script setup lang="ts">
import type { Document } from '@/types/document'
import DocumentCard from './DocumentCard.vue'

defineProps<{
  items: Document[]
  loading: boolean
}>()

const emit = defineEmits<{
  delete: [id: number]
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
      />
    </div>
  </div>
</template>

<style scoped>
/* 容器：预留最小高度、避免空状态抖动 */
.document-list-wrapper {
  min-height: 280px;
  margin-bottom: 24px;
}

/* 纵向列表：间距与全局协调 */
.document-list {
  display: flex;
  flex-direction: column;
  gap: 12px; /* ✅ 微调间距，更舒适不拥挤 */
}

/* ✅ 滚动条适配明暗 */
.document-list-wrapper::-webkit-scrollbar {
  width: 6px;
}
.document-list-wrapper::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
  border-radius: 3px;
}
.document-list-wrapper::-webkit-scrollbar-track {
  background: transparent;
}
</style>
