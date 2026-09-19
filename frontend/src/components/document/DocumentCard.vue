<script setup lang="ts">
import { computed } from 'vue'
import type { Document } from '@/types/document'
import DocumentStatus from './DocumentStatus.vue'
import { Document as DocumentIcon } from '@element-plus/icons-vue' // ✅ 补全图标导入

const props = defineProps<{
  item: Document
}>()

const emit = defineEmits<{
  delete: [id: number]
}>()

// ✅ 格式化文件大小：bytes → KB/MB 更易读
const formatSize = (bytes: number) => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}
const friendlySize = computed(() => formatSize(props.item.file_size))
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
      <DocumentStatus :status="item.status" />
    </div>

    <!-- 右侧：删除操作 -->
    <div class="document-actions">
      <el-button text type="danger" @click.stop="emit('delete', item.id)"> 删除 </el-button>
    </div>
  </div>
</template>

<style scoped>
/* 卡片容器：标准变量、明暗自动适配 */
.document-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 20px;
  border: 1px solid var(--el-border-color-lighter); /* ✅ EP 标准变量 */
  border-radius: 10px; /* ✅ 统一全局圆角 */
  background: var(--el-bg-color); /* ✅ 明暗自动跟随 */
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

/* hover 反馈：柔和不刺眼 */
.document-card:hover {
  border-color: var(--el-color-primary-light-5);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

/* 主内容区：防挤压 */
.document-main {
  display: flex;
  align-items: center;
  min-width: 0;
  flex: 1;
  gap: 14px;
}

/* 文件图标：主色统一 */
.document-icon {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

/* 文件名：单行省略、hover 提示完整 */
.document-info {
  min-width: 0;
  flex: 1;
}
.document-info h4 {
  margin: 0 0 4px;
  overflow: hidden;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--el-text-color-primary); /* ✅ 明暗适配 */
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 元信息：弱化显示 */
.document-meta {
  display: flex;
  gap: 12px;
  color: var(--el-text-color-secondary); /* ✅ 明暗适配 */
  font-size: 12px;
}

/* 操作区：固定右侧不压缩 */
.document-actions {
  flex-shrink: 0;
}
</style>
