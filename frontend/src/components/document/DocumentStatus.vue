<script setup lang="ts">
import { computed } from 'vue'
import type { Document } from '@/types/document'
import { Loading, WarningFilled } from '@element-plus/icons-vue'

const props = defineProps<{
  status: Document['status']
  errorMessage?: string | null
}>()

/**
 * 文档状态配置
 *
 * 📌 必懂：
 * 状态映射集中管理，避免模板中出现大量 if / else。
 *
 * 🏢 企业实践：
 * 使用 as const 保留字面量类型，增强 TypeScript 类型推导。
 */
const statusMap = {
  pending: {
    type: 'info',
    text: '等待处理',
  },
  processing: {
    type: 'warning',
    text: '处理中',
  },
  completed: {
    type: 'success',
    text: '已完成',
  },
  failed: {
    type: 'danger',
    text: '处理失败',
  },
} as const

const currentStatus = computed(() => {
  return (
    statusMap[props.status] ?? {
      type: 'info',
      text: '未知状态',
    }
  )
})

/**
 * 是否显示错误详情
 *
 * 📌 必懂：
 * 只有失败状态且存在错误信息时，才展示错误提示。
 */
const hasErrorMessage = computed(() => {
  return props.status === 'failed' && Boolean(props.errorMessage?.trim())
})
</script>

<template>
  <div class="document-status">
    <el-tag
      :type="currentStatus.type"
      size="small"
      :class="{
        'is-processing': status === 'processing',
      }"
    >
      <el-icon v-if="status === 'processing'" class="status-icon is-loading">
        <Loading />
      </el-icon>

      {{ currentStatus.text }}
    </el-tag>

    <!-- 失败原因提示 -->
    <el-tooltip v-if="hasErrorMessage" :content="errorMessage ?? ''" placement="top" effect="dark">
      <el-icon class="error-icon">
        <WarningFilled />
      </el-icon>
    </el-tooltip>
  </div>
</template>

<style scoped>
.document-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.status-icon {
  margin-right: 4px;
}

.error-icon {
  color: var(--el-color-danger);
  cursor: help;
  font-size: 15px;
}

/* 处理中状态：轻微强调，避免过度动画 */
.is-processing {
  transition: opacity 0.2s ease;
}
</style>
