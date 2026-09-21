<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Document } from '@/types/document'
import DocumentStatus from './DocumentStatus.vue'
import { Document as DocumentIcon, Refresh } from '@element-plus/icons-vue' // 补全图标导入

const props = defineProps<{
  item: Document
  retrying?: boolean
}>()

const emit = defineEmits<{
  delete: [id: number]
  retry: [id: number]
}>()

// 格式化文件大小：统一单位显示
const friendlySize = computed(() => formatSize(props.item.file_size))
// 仅失败状态可重试
const canRetry = computed(() => props.item.status === 'failed')
// 重试中防重复提交
// const retrying = ref(false)

const handleRetry = () => {
  if (props.retrying) return

  emit('retry', props.item.id)
  // retrying.value = true

  // 等待父组件异步完成后重置 避免快速连击导致重复请求
  // Promise.resolve()
  //   .then(() => emit('retry', props.item.id))
  //   .finally(() => {
  //     retrying.value = false
  //   })
}

/** 格式化字节为易读单位 B/KB/MB */
const formatSize = (bytes: number): string => {
  if (!Number.isFinite(bytes) || bytes < 0) return '—'
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}
</script>

<template>
  <div class="document-card">
    <!-- 左侧：文件图标 -->
    <div class="document-main">
      <div class="document-icon">
        <el-icon :size="22"><DocumentIcon /></el-icon>
      </div>

      <!-- 中间：文件名 + 类型/大小 -->
      <div class="document-info">
        <h4 :title="item.name">
          {{ item.name }}
        </h4>
        <div class="document-meta">
          <span>{{ item.file_type.toUpperCase() }}</span>
          <span>{{ friendlySize }}</span>
        </div>
      </div>

      <!-- 状态标签：独立组件 -->
      <DocumentStatus :status="item.status" :error-message="item.error_message" />
    </div>

    <!-- 右侧：操作按钮 -->
    <div class="document-actions">
      <el-button text type="danger" @click.stop="emit('delete', item.id)"> 删除 </el-button>
      <el-button
        v-if="canRetry"
        link
        type="warning"
        :disabled="retrying"
        :loading="retrying"
        @click.stop="handleRetry"
      >
        <el-icon><Refresh /></el-icon>
        重试
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.document-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 20px;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 10px;
  background: var(--el-bg-color);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.document-card:hover {
  border-color: var(--el-color-primary-light-5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.document-main {
  display: flex;
  align-items: center;
  min-width: 0;
  flex: 1;
  gap: 14px;
}

.document-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.document-info {
  min-width: 0;
  flex: 1;
}

.document-info h4 {
  margin: 0 0 4px;
  overflow: hidden;
  color: var(--el-text-color-primary);
  font-size: 14px;
  font-weight: 600;
  line-height: 1.4;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.document-actions {
  flex-shrink: 0;
  display: flex;
  gap: 4px;
}

/* 小屏幕适配 */
@media (max-width: 640px) {
  .document-card {
    align-items: flex-start;
    padding: 12px 14px;
  }
  .document-main {
    flex-wrap: wrap;
    gap: 10px;
  }
  .document-actions {
    margin-left: auto;
  }
}
</style>
