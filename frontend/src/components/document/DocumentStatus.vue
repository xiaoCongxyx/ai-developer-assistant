<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
}>()

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
    statusMap[props.status as keyof typeof statusMap] ?? {
      type: 'info',
      text: props.status,
    }
  )
})
</script>

<template>
  <el-tag :type="currentStatus.type" size="small">
    {{ currentStatus.text }}
  </el-tag>
</template>
