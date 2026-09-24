<script setup lang="ts">
import type { Document } from '@/types/document'
import DocumentCard from './DocumentCard.vue'
import { computed, ref, watch } from 'vue'

const props = defineProps<{
  items: Document[]
  loading: boolean
  isRetrying: (documentId: number) => boolean
}>()

const emit = defineEmits<{
  delete: [id: number]
  retry: [id: number]
  batchDelete: [ids: number[]]
}>()

// 选中的文档 ID 集合
const selectedIds = ref<number[]>([])

// 已选中数量
const selectedCount = computed(() => selectedIds.value.length)

// 是否全部选中
const isAllSelected = computed(() => {
  const total = props.items.length
  return total > 0 && selectedIds.value.length === total
})

// 是否部分选中（控制全选框中间态）
const isIndeterminate = computed(() => {
  return selectedCount.value > 0 && !isAllSelected.value
})

const toggleSelectAll = (checked: boolean) => {
  selectedIds.value = checked ? props.items.map((v) => v.id) : []
}

const toggleSelection = (documentId: number, checked: boolean) => {
  if (checked) {
    if (!selectedIds.value.includes(documentId)) {
      selectedIds.value.push(documentId)
    }
  } else {
    selectedIds.value = selectedIds.value.filter((id) => id !== documentId)
  }
}

// 清理无效选中项：列表变化时自动过滤
watch(
  () => props.items,
  (newItems) => {
    const validIds = new Set(newItems.map((item) => item.id))
    // 只保留仍在列表中的 ID
    selectedIds.value = selectedIds.value.filter((id) => validIds.has(id))
  },
  { deep: true },
)
</script>

<template>
  <div v-loading="loading" element-loading-text="加载中..." class="document-list-wrapper">
    <!-- 工具栏：全选 + 选中数量 + 批量删除 -->
    <div class="document-toolbar">
      <el-checkbox
        :model-value="isAllSelected"
        :indeterminate="isIndeterminate"
        @change="toggleSelectAll"
      >
        全选
      </el-checkbox>

      <span v-if="selectedCount > 0" class="selected-text">
        已选择 {{ selectedCount }} 个文档
      </span>

      <el-button
        v-if="selectedCount > 0"
        type="danger"
        plain
        @click="emit('batchDelete', selectedIds)"
      >
        批量删除
      </el-button>
    </div>

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
        :selected="selectedIds.includes(item.id)"
        :retrying="isRetrying(item.id)"
        @delete="emit('delete', $event)"
        @retry="emit('retry', $event)"
        @select="toggleSelection"
      />
    </div>
  </div>
</template>

<style scoped>
.document-list-wrapper {
  min-height: 280px;
  margin-bottom: 24px;
  overflow-y: auto;
}

/* 工具栏样式 */
.document-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: var(--el-bg-color-page);
  border-radius: 8px;
}

.selected-text {
  flex: 1;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.document-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 滚动条适配 */
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
